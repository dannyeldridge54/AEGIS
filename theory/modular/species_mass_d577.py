"""D577 (locked PREREG_D577_SPECIES_MASS). AI-assisted."""
import math, cmath, numpy as np
from scipy.optimize import brentq
from mpmath import mp, kleinj
mp.dps=40
def sig(n,k): return sum(d**k for d in range(1,n+1) if n%d==0)
def E2(t):
    q=cmath.exp(2j*math.pi*t); return 1-24*sum(sig(n,1)*q**n for n in range(1,120))
def lneta(t):
    q=cmath.exp(2j*math.pi*t); return 2j*math.pi*t/24+sum(cmath.log(1-q**n) for n in range(1,200))
def G2h(t): return E2(t)-3/(math.pi*t.imag)
def L(t): y=t.imag; return math.log(2*y)+4*lneta(t).real   # ln(2y|eta|^4)
J=lambda t:complex(kleinj(t))*1728
I=lambda t:math.log(1+abs(J(t)-1728)**2/1728**2)/(4*math.pi)
print(f"check |G2hat(i)| = {abs(G2h(1j)):.2e}")
t0=0.3+1.2j; h=1e-6
num=((L(t0+h)-L(t0-h))/(2*h) - 1j*(L(t0+1j*h)-L(t0-1j*h))/(2*h))/2  # d/dtau of real fn: (d_x - i d_y)/2
print(f"check d_tau ln(2y|eta|^4) = {num:.8f} vs (pi i/6)G2hat = {(math.pi*1j/6)*G2h(t0):.8f}")
def VCI(t,N0): y=t.imag; N=-6*L(t)+N0; return y*y*abs(G2h(t))**2/N**2
def Vt(t,k,N0): x=I(t)**2; return x/(x+1)+k*VCI(t,N0)
# 1D along imaginary axis (y real); for y>~8 use cusp-safe forms
def Iy(y):
    q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q); ljm=lj+math.log(abs(1-1728*math.exp(-lj)))
    return (math.log(math.exp(2*(ljm-math.log(1728)))+1) if ljm<300 else 2*(ljm-math.log(1728)))/(4*math.pi)
def VCIy(y,N0):
    q=math.exp(-2*math.pi*y); e2=1-24*sum(sig(n,1)*q**n for n in range(1,40)); g=e2-3/(math.pi*y)
    le=-math.pi*y/12+sum(math.log(1-q**n) for n in range(1,60)); N=-6*(math.log(2*y)+4*le)+N0
    return y*y*g*g/N**2
def infl(k,N0,N):
    qn=1/math.sqrt(2)
    def lv(u):
        y=math.exp(u); x=Iy(y)**2; return math.log(x/(x+1)+k*VCIy(y,N0))
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn
    d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2
    us=[0.02+0.003*i for i in range(2300)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    if ue is None: return None
    u=ue; Na=0; du=1e-3; first=True
    while Na<N and u<14:
        if not first and eps(u)>1+1e-6: return None
        Na+=qn*du/abs(d1(u)); u+=du; first=False
    if Na<N: return ('N* not reached (no viable inflation)',) if 'two_term' in __file__ else None
    g=d1(u); hh=d2(u); ev=0.5*g*g; y=math.exp(u)
    return math.exp(ue),y,1-6*ev+2*(hh+g*g),16*ev,math.exp(lv(u))
ds=np.array([1e-2,3e-3,1e-3,3e-4,1e-4])
base={}
for N in (52,55.6):
    r=infl(0,25,N); base[N]=r[2]; print(f"kappa=0 (HS-Kairos) N*={N}: y*={r[1]:.1f} n_s={r[2]:.4f} r={r[3]:.2e}")
for k in (1e-3,1e-2,1e-1):
    for N0 in (25,100):
        sl=[np.polyfit(np.log(ds),[math.log(Vt(1j+d*u,k,N0)) for d in ds],1)[0] for u in (1,1j)]
        d=1e-4; m2=2*Vt(1j+1j*d,k,N0)/(d/math.sqrt(2))**2
        for N in (52,55.6):
            r=infl(k,N0,N)
            if r is None: print(f"kappa={k:g} N0={N0} N*={N}: slopes={[round(s,3) for s in sl]} no viable inflation"); continue
            ye,ys,ns,rr,Vs=r
            print(f"kappa={k:g} N0={N0} N*={N}: slopes={[round(s,3) for s in sl]} m/H={math.sqrt(3*m2/Vs):.3f} y_end={ye:.2f} y*={ys:.1f} {'HOME-SAFE' if ys<=25 else 'outside'} n_s={ns:.4f} (dn_s={ns-base[N]:+.4f}) r={rr:.2e} ({(ns-0.9684)/0.003:+.1f} SPA, {(ns-0.9728)/0.0027:+.1f} SPA+DESI)")
