"""D563 SERAPIS-NP (locked PREREG_D563_SERAPIS_NP). AI-assisted."""
import math, cmath
from scipy.optimize import brentq
from mpmath import mp, kleinj
mp.dps=30
def Vc(t): J=complex(kleinj(t))*1728; a=abs(J-1728)**2; return a/(a+1728**2)
v0=Vc(1j); nb=[Vc(1j+d) for d in (0.01,0.01j,-0.01j,0.01*cmath.exp(1j*math.pi/4))]
print(f"V(i)={v0:.2e}, neighbours min={min(nb):.2e}, minimum at i: {v0<1e-20 and min(nb)>0}")
def lnV_y(y):
    q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q)
    if lj>300: return -1728**2*math.exp(-2*lj)   # ln(1 - 1728^2/|j|^2) ~ -1728^2/|j|^2, |j-1728|~|j|
    J=math.exp(lj); a=(J-1728)**2; return math.log(a/(a+1728**2))
def infl(N):
    qn=1/math.sqrt(2); lv=lambda u:lnV_y(math.exp(u))
    d1=lambda u,h=1e-5:(lv(u+h)-lv(u-h))/(2*h)/qn
    d2=lambda u,h=1e-4:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2
    us=[0.05+0.002*i for i in range(3500)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    if ue is None: return None
    u=ue; Na=0; du=2e-5
    while Na<N and u<7: Na+=qn*du/abs(d1(u)); u+=du
    g=d1(u); hh=d2(u); ev=0.5*g*g
    return math.exp(ue),math.exp(u),1-6*ev+2*(hh+g*g),16*ev
for N in (52,55.6):
    r=infl(N)
    if r is None: print(f"N*={N}: no end found"); continue
    ye,ys,ns,rr=r; print(f"N*={N}: y_end={ye:.3f} y*={ys:.3f} n_s={ns:.4f} r={rr:.2e} ({(ns-0.9684)/0.003:+.1f} sigma SPA, {(ns-0.9728)/0.0027:+.1f} SPA+DESI); 1-2/N={1-2/N:.4f}")
