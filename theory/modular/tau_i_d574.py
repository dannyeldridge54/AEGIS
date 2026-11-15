"""D574 (locked PREREG_D574_TAU_I_DERIVATION). AI-assisted."""
import math, cmath, numpy as np
from scipy.optimize import brentq
from mpmath import mp, kleinj
mp.dps=40
def sig(n,k): return sum(d**k for d in range(1,n+1) if n%d==0)
def E(t,k,c):
    q=cmath.exp(2j*math.pi*t); return 1+c*sum(sig(n,k-1)*q**n for n in range(1,80))
E4=lambda t:E(t,4,240); E6=lambda t:E(t,6,-504)
J=lambda t:complex(kleinj(t))*1728
print("B: |E4(i)| =",f"{abs(E4(1j)):.6f}","|E6(i)| =",f"{abs(E6(1j)):.2e}","|E6'(i)| =",f"{abs((E6(1j+1e-6)-E6(1j-1e-6))/2e-6):.4f}","|j(i)-1728| =",f"{abs(J(1j)-1728):.2e}")
ds=np.array([1e-2,3e-3,1e-3,3e-4,1e-4])
dirs=[1,1j,cmath.exp(1j*math.pi/4)]
def slope(f):
    out=[]
    for u in dirs:
        y=[math.log(abs(f(1j+d*u))) for d in ds]; out.append(np.polyfit(np.log(ds),y,1)[0])
    return out
print("B: order of zero of j-1728 at i, slopes per direction:",[f"{s:.3f}" for s in slope(lambda t:J(t)-1728)])
I =lambda t:math.log(1+abs(J(t)-1728)**2/1728**2)/(4*math.pi)
I1=lambda t:math.log(1+abs(J(t)-1728)/1728)/(4*math.pi)
V=lambda t,p,f=I:(lambda x:x/(x+1))(f(t)**p)
for p in (1,2):
    h=1e-5; gx=(V(1j+h,p)-V(1j-h,p))/(2*h); gy=(V(1j+1j*h,p)-V(1j-1j*h,p))/(2*h)
    print(f"A: p={p} |grad V(i)| = {math.hypot(gx,gy):.2e}, V(i+0.01) = {V(1j+0.01,p):.2e}, ratio = {math.hypot(gx,gy)/V(1j+0.01,p):.2e}")
    print(f"C : SERAPIS-KL  p={p}: slope of V vs |d| =",[f"{s:.3f}" for s in slope(lambda t:V(t,p))], f"(expect {4*p})")
    print(f"C': SERAPIS-KL1 p={p}: slope of V vs |d| =",[f"{s:.3f}" for s in slope(lambda t:V(t,p,I1))], f"(expect {2*p})")
# vacuum mass for C' p=1: canonical phi = d/sqrt(2) at y=1 (alpha=1/3); m^2/H^2 = 3 V''(phi)/V_plateau, V_plateau=1
d=1e-4; Vd=V(1j+1j*d,1,I1); m2=2*Vd/(d/math.sqrt(2))**2
print(f"C': p=1 vacuum m^2/H^2 = {3*m2:.3f}, m/H = {math.sqrt(3*m2):.3f}  (radial dir); check Re dir: {math.sqrt(3*2*V(1j+d,1,I1)/(d/math.sqrt(2))**2):.3f}")
# inflation, D564 machinery with Iy -> I1(y)
def I1y(y):
    q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q)
    ljm=lj+math.log(abs(1-1728*math.exp(-lj)))
    return (math.log(math.exp(ljm-math.log(1728))+1) if ljm<300 else (ljm-math.log(1728)))/(4*math.pi)
print("check I1y(2) vs I1(2i):",f"{I1y(2):.6f} {I1(2j):.6f}")
def infl(p,N):
    qn=1/math.sqrt(2); lv=lambda u:(lambda x:math.log(x/(x+1)))(I1y(math.exp(u))**p)
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
for p in (1,2):
    for N in (52,55.6):
        r=infl(p,N)
        if r is None: print(f"KL1 p={p} N*={N}: no end"); continue
        ye,ys,ns,rr=r; print(f"KL1 p={p} N*={N}: y_end={ye:.2f} y*={ys:.1f} {'HOME-SAFE' if ys<=25 else 'outside'} n_s={ns:.4f} r={rr:.2e} ({(ns-0.9684)/0.003:+.1f} SPA, {(ns-0.9728)/0.0027:+.1f} SPA+DESI)")
