"""D546 (locked PREREG_D546_SERAPIS_KL_CHRONOS). Reuses D545 code. AI-assisted."""
import math, cmath
from scipy.optimize import brentq
from mpmath import mp, kleinj
mp.dps=30
def Ic(t): return math.log(1+abs(complex(kleinj(t))*1728-1728)**2/1728**2)/(4*math.pi)
def Vc(t,d): x=Ic(t); return x/(x+1)*x**(2*d) if x>0 else 0.0
def lnV_y(y,d):
    q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q)
    ljm=lj+math.log(abs(1-1728*math.exp(-lj)))
    x=(math.log(math.exp(2*(ljm-math.log(1728)))+1) if ljm<300 else 2*(ljm-math.log(1728)))/(4*math.pi)
    return math.log(x/(x+1))+2*d*math.log(x)
def infl(d,N):
    qn=1/math.sqrt(2); lv=lambda u:lnV_y(math.exp(u),d)
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn
    d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2
    us=[0.05+0.005*i for i in range(1400)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    if ue is None: return None
    u=ue; Na=0; du=1e-3
    while Na<N and u<14: Na+=qn*du/abs(d1(u)); u+=du
    g=d1(u); hh=d2(u); ev=0.5*g*g
    return math.exp(u),1-6*ev+2*(hh+g*g),16*ev
d=0.0023; i=1j
vals=[Vc(t,d) for t in (i+0.01,i+0.01j,i-0.01j,i+0.01*cmath.exp(1j*math.pi/4))]
print(f"delta={d}: V(i)={Vc(i,d):.2e}, neighbours min={min(vals):.2e} -> minimum at i: {Vc(i,d)==0 and min(vals)>0}")
for dd in (0.0015,0.002,0.0023,0.003):
    for N in (52,55.6):
        res=infl(dd,N)
        if res is None: print(f"delta={dd} N*={N}: no end"); continue
        ys,ns,r=res
        print(f"delta={dd} N*={N}: y*={ys:.1f} n_s={ns:.4f} r={r:.5f} ({(ns-0.9684)/0.0030:+.1f} sigma SPA, {(ns-0.9728)/0.0027:+.1f} SPA+DESI)")
