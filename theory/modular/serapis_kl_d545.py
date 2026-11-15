"""D545 SERAPIS-KL (locked PREREG_D545_SERAPIS_KL). AI-assisted."""
import math, cmath, sys
from scipy.optimize import brentq
sys.path.insert(0,'theory/modular')
from mpmath import mp, kleinj
mp.dps=30
def jc(t): return complex(kleinj(t))*1728
def I(t): return math.log(1+abs(jc(t)-1728)**2/1728**2)/(4*math.pi)
def V(t,n): x=I(t); return (x/(x+1))**n
for n in (1,2):
    i=1j; pts={'i':i,'i+0.01':i+0.01,'i+0.01i':i+0.01j,'i-0.01i':i-0.01j,'i+0.01e^(ipi/4)':i+0.01*cmath.exp(1j*math.pi/4)}
    vals={k:V(t,n) for k,t in pts.items()}; w=cmath.exp(2j*math.pi/3)
    print(f"n={n}: "+", ".join(f"V({k})={v:.3e}" for k,v in vals.items())+f", V(omega)={V(w,n):.3e}")
    print(f"  minimum at i in all directions: {all(v>vals['i'] for k,v in vals.items() if k!='i')}; V(i)=0: {vals['i']<1e-20}")
# inflation along imaginary axis with asymptotic large-y form for |j|: use q-expansion via lnV
def lnV_y(y,n):
    q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q)
    ljm=lj+math.log(abs(1-1728*math.exp(-lj)))
    x=(math.log(math.exp(2*(ljm-math.log(1728)))+1) if ljm<300 else 2*(ljm-math.log(1728)))/(4*math.pi)
    return n*math.log(x/(x+1))
def infl(n,N):
    qn=1/math.sqrt(2); lv=lambda u:lnV_y(math.exp(u),n)
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn
    d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2
    us=[0.05+0.005*i for i in range(1400)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    u=ue; Na=0; du=1e-3
    while Na<N and u<14: Na+=qn*du/abs(d1(u)); u+=du
    g=d1(u); hh=d2(u); ev=0.5*g*g
    return math.exp(ue),math.exp(u),1-6*ev+2*(hh+g*g),16*ev
for n in (1,2):
    for N in (52,55.6):
        ye,ys,ns,r=infl(n,N)
        print(f"n={n} N*={N}: y_end={ye:.2f} y*={ys:.1f} n_s={ns:.4f} r={r:.5f} ({(ns-0.9684)/0.0030:+.1f} sigma SPA, {(ns-0.9728)/0.0027:+.1f} SPA+DESI); attractor formula n_s={1-2/N:.4f} r={4/N**2:.5f}")
