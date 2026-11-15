"""D559 (locked PREREG_D559_CI_DIAG). AI-assisted."""
import math
from scipy.optimize import brentq
def mk(mode,N0=0.0):
    def lnV_y(y):
        q=math.exp(-2*math.pi*y); e2=1-24*sum(n*q**n/(1-q**n) for n in range(1,8))
        G2t=(math.pi**2/3)*e2-math.pi/y
        le=-math.pi*y/12+sum(math.log(1-q**k) for k in range(1,8))
        N=2*math.pi*y if mode=='A' else -6*(math.log(2*y)+4*le)+N0
        return 2*math.log(abs(y*G2t))-2*math.log(N)
    return lnV_y
def infl(lnV_y,a,Nst):
    lv=lambda u:lnV_y(math.exp(u))
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)*a
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
a=math.sqrt(2/3)
for lab,f in (("A: N=2*pi*tau2",mk('A')),("B: full, N0=0",mk('B',0)),("C: full, N0=25",mk('B',25)),("D: full, N0=100",mk('B',100))):
    r=infl(f,a,60); print(lab, "no end" if r is None else f"y*={r[0]:.0f} n_s={r[1]:.4f} r={r[2]:.5f}")
print("their analytic (eq 5.29/5.30): n_s=", round(1-2/60-3/((2/3)*3600),4), " r=", round(8/((2/3)*3600),5))
