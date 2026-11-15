"""D564 (locked PREREG_D564_SERAPIS_P). AI-assisted."""
import math, cmath
from scipy.optimize import brentq
from mpmath import mp, kleinj
mp.dps=30
def Ic(t): return math.log(1+abs(complex(kleinj(t))*1728-1728)**2/1728**2)/(4*math.pi)
def Vc(t,p): x=Ic(t)**p; return x/(x+1)
v0=Vc(1j,2); nb=[Vc(1j+d,2) for d in (0.01,0.01j,-0.01j,0.01*cmath.exp(1j*math.pi/4))]
print(f"p=2: V(i)={v0:.2e}, neighbours min={min(nb):.2e}, minimum at i: {v0<1e-20 and min(nb)>0}")
def Iy(y):
    q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q)
    ljm=lj+math.log(abs(1-1728*math.exp(-lj)))
    return (math.log(math.exp(2*(ljm-math.log(1728)))+1) if ljm<300 else 2*(ljm-math.log(1728)))/(4*math.pi)
def infl(p,N):
    qn=1/math.sqrt(2); lv=lambda u:(lambda x:math.log(x/(x+1)))(Iy(math.exp(u))**p)
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn
    d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2
    us=[0.02+0.003*i for i in range(2300)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    if ue is None: return None
    u=ue; Na=0; du=1e-3
    while Na<N and u<14: Na+=qn*du/abs(d1(u)); u+=du
    g=d1(u); hh=d2(u); ev=0.5*g*g
    return math.exp(ue),math.exp(u),1-6*ev+2*(hh+g*g),16*ev
for p in (1,1.5,2,3):
    for N in (52,55.6):
        r=infl(p,N)
        if r is None: print(f"p={p} N*={N}: no end"); continue
        ye,ys,ns,rr=r; print(f"p={p} N*={N}: y_end={ye:.2f} y*={ys:.1f} {'HOME-SAFE' if ys<=25 else 'outside'} n_s={ns:.4f} r={rr:.2e} ({(ns-0.9684)/0.003:+.1f} SPA, {(ns-0.9728)/0.0027:+.1f} SPA+DESI) [analytic r={4/(p*p*N*N):.1e}]")
