"""D575 (locked PREREG_D575_TWO_TERM). AI-assisted."""
import math, numpy as np
from scipy.optimize import brentq
from mpmath import mp, kleinj
mp.dps=40
J=lambda t:complex(kleinj(t))*1728
I =lambda t:math.log(1+abs(J(t)-1728)**2/1728**2)/(4*math.pi)
I1=lambda t:math.log(1+abs(J(t)-1728)/1728)/(4*math.pi)
def Ljm(y):
    q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q); return lj+math.log(abs(1-1728*math.exp(-lj)))
def Iy(y):
    l=Ljm(y); return (math.log(math.exp(2*(l-math.log(1728)))+1) if l<300 else 2*(l-math.log(1728)))/(4*math.pi)
def I1y(y):
    l=Ljm(y); return (math.log(math.exp(l-math.log(1728))+1) if l<300 else (l-math.log(1728)))/(4*math.pi)
p=2; qn=1/math.sqrt(2)
def Vy(y,e): x=Iy(y)**p; return x/(x+1)+e*I1y(y)
def infl(e,N):
    lv=lambda u:math.log(Vy(math.exp(u),e))
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn
    d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2
    us=[0.02+0.003*i for i in range(2300)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    if ue is None: return None
    u=ue; Na=0; du=1e-3; first=True
    while Na<N and u<14:
        if not first and eps(u)>1+1e-6: return ('inflation broken at y=%.1f'%math.exp(u),)
        Na+=qn*du/abs(d1(u)); u+=du; first=False
    if Na<N: return ('N* not reached (no viable inflation)',) if 'two_term' in __file__ else None
    g=d1(u); hh=d2(u); ev=0.5*g*g
    return math.exp(ue),math.exp(u),1-6*ev+2*(hh+g*g),16*ev,Vy(math.exp(u),e)
ds=np.array([1e-2,3e-3,1e-3,3e-4,1e-4])
for e in (1e-4,3e-4,1e-3,3e-3):
    V=lambda t:(lambda x:x/(x+1))(I(t)**p)+e*I1(t)
    sl=np.polyfit(np.log(ds),[math.log(V(1j+1j*d)) for d in ds],1)[0]
    d=1e-4; m2=2*V(1j+1j*d)/(d/math.sqrt(2))**2
    for N in (52,55.6):
        r=infl(e,N)
        if r is None or len(r)==1: print(f"eps={e:g} N*={N}: {r}"); continue
        ye,ys,ns,rr,Vs=r; mH=math.sqrt(3*m2/Vs)
        print(f"eps={e:g} N*={N}: slope={sl:.3f} m/H={mH:.3f} y_end={ye:.2f} y*={ys:.1f} {'HOME-SAFE' if ys<=25 else 'outside'} n_s={ns:.4f} r={rr:.2e} ({(ns-0.9684)/0.003:+.1f} SPA, {(ns-0.9728)/0.0027:+.1f} SPA+DESI)")
