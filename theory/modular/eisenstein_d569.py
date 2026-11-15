"""D569 (locked PREREG_D569_EISENSTEIN). AI-assisted."""
import math, cmath
import numpy as np
from scipy.optimize import brentq
L=60
m,n=np.meshgrid(np.arange(-L,L+1),np.arange(-L,L+1)); mask=~((m==0)&(n==0)); m=m[mask].astype(float); n=n[mask].astype(float)
def E(t,s): x,y=t.real,t.imag; return np.sum(y**s/((m*x+n)**2+(m*y)**2)**s)
rho=cmath.exp(1j*math.pi/3)
for s in (1.5,2,2.5,3): print(f"s={s}: E(i)={E(1j,s):.5f}  E(rho)={E(rho,s):.5f}  -> min at {'i' if E(1j,s)<E(rho,s) else 'rho'}")
def infl(s,N):
    Emin=min(E(1j,s),E(rho,s)); qn=1/math.sqrt(2)
    def lv(u):
        y=math.exp(u)
        Ey=E(1j*y,s) if y<8 else 2*math.pi**0*0+ (2*sum(1/k**(2*s) for k in range(1,200)))*y**s + 2*math.sqrt(math.pi)*math.gamma(s-0.5)/math.gamma(s)*sum(1/k**(2*s-1) for k in range(1,200))*y**(1-s)
        return math.log(1-Emin/Ey)
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn
    d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2
    us=[0.01+0.004*i for i in range(1200)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        try:
            if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
        except ValueError: continue
    if ue is None: return None
    u=ue; Na=0; du=1e-3
    while Na<N and u<5: Na+=qn*du/abs(d1(u)); u+=du
    g=d1(u); hh=d2(u); ev=0.5*g*g
    return math.exp(ue),math.exp(u),1-6*ev+2*(hh+g*g),16*ev
for s in (2.5,3):
    if E(1j,s)>E(rho,s): print(f"s={s}: minimum at rho, not i -> conflicts with SERAPIS tau=i vacuum; inflation computed anyway along i*y toward the axis minimum")
    for N in (52,55.6):
        r=infl(s,N)
        if r is None: print(f"s={s} N*={N}: no end"); continue
        ye,ys,ns,rr=r; print(f"s={s} N*={N}: y_end={ye:.2f} y*={ys:.1f} n_s={ns:.4f} r={rr:.2e} ({(ns-0.9684)/0.003:+.1f} SPA, {(ns-0.9728)/0.0027:+.1f} SPA+DESI)")
