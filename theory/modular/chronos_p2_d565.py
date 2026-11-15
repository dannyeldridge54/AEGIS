"""D565 (locked PREREG_D565_CHRONOS_P2). Reuses D564 code. AI-assisted."""
import math, sys
sys.path.insert(0,'theory/modular')
from scipy.optimize import brentq
import importlib.util
spec=importlib.util.spec_from_file_location('d564','theory/modular/serapis_p_d564.py')
src=open('theory/modular/serapis_p_d564.py').read().split('v0=Vc(1j,2)')[0]
g={}; exec(src,g)
Iy=None
def Iy_(y):
    q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q)
    ljm=lj+math.log(abs(1-1728*math.exp(-lj)))
    return (math.log(math.exp(2*(ljm-math.log(1728)))+1) if ljm<300 else 2*(ljm-math.log(1728)))/(4*math.pi)
def infl(p,d,N):
    qn=1/math.sqrt(2)
    def lv(u):
        I=Iy_(math.exp(u)); x=I**p; return math.log(x/(x+1))+2*d*math.log(I)
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn
    d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2
    us=[0.02+0.003*i for i in range(2300)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    if ue is None: return None
    u=ue; Na=0; du=1e-3
    while Na<N and u<14: Na+=qn*du/abs(d1(u)); u+=du
    gg=d1(u); hh=d2(u); ev=0.5*gg*gg
    return math.exp(u),1-6*ev+2*(hh+gg*gg),16*ev
for d in (0.002,0.0023,0.003,0.005):
    for N in (52,55.6):
        r=infl(2,d,N)
        if r is None: print(d,N,'no end'); continue
        ys,ns,rr=r; print(f"p=2 delta={d} N*={N}: y*={ys:.1f} {'HOME-SAFE' if ys<=25 else 'outside'} n_s={ns:.4f} r={rr:.2e} ({(ns-0.9684)/0.003:+.1f} SPA, {(ns-0.9728)/0.0027:+.1f} SPA+DESI)")
