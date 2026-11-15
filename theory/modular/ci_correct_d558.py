"""D558 (locked PREREG_D558_CI_CORRECT). AI-assisted."""
import math
from scipy.optimize import brentq
def lnV_y(y):
    q=math.exp(-2*math.pi*y); e2=1-24*sum(n*q**n/(1-q**n) for n in range(1,8))
    G2t=(math.pi**2/3)*e2-math.pi/y
    le=-math.pi*y/12+sum(math.log(1-q**k) for k in range(1,8))
    N=-6*(math.log(2*y)+4*le)+25.0
    return 2*math.log(abs(y*G2t))-2*math.log(N)
def infl(a,Nst):
    lv=lambda u:lnV_y(math.exp(u))
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)*a      # d/dphi = a d/du
    d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)*a*a
    eps=lambda u:0.5*d1(u)**2
    us=[0.05+0.005*i for i in range(1500)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    if ue is None: return None
    u=ue; Na=0; du=1e-3
    while Na<Nst and u<14: Na+=du/(a*abs(d1(u))); u+=du
    g=d1(u); hh=d2(u); ev=0.5*g*g
    return math.exp(u),1-6*ev+2*(hh+g*g),16*ev
for a,lab in ((math.sqrt(2),'a=sqrt2 (alpha=1/3)'),(math.sqrt(2/3),'a=sqrt(2/3)')):
    for Nst in (52,55.6,60):
        res=infl(a,Nst)
        if res is None: print(lab,Nst,'no end'); continue
        ys,ns,r=res; print(f"{lab} N*={Nst}: y*={ys:.0f} n_s={ns:.4f} r={r:.5f} ({(ns-0.9684)/0.003:+.1f} sigma SPA, {(ns-0.9728)/0.0027:+.1f} SPA+DESI)")
