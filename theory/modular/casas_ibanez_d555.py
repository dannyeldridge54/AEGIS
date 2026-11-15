"""D555 (locked PREREG_D555_CASAS_IBANEZ). AI-assisted."""
import math, cmath
from scipy.optimize import brentq
from mpmath import mp, eta, mpc, exp, pi
mp.dps=30
def E2(t):
    q=exp(2j*pi*mpc(t)); s=0; n=1
    while True:
        term=n*q**n/(1-q**n); s+=term; n+=1
        if abs(term)<1e-25 or n>2000: break
    return complex(1-24*s)
def G2h(t): return E2(t)-3/(math.pi*t.imag)
def V(t):
    y=t.imag; N=-math.log(y*abs(complex(eta(t)))**4); return y*y*abs(G2h(t))**2/N**2
rho=cmath.exp(1j*math.pi/3)
print(f"G2hat(i)={abs(G2h(1j)):.2e}, G2hat(rho)={abs(G2h(rho)):.2e}")
v0=V(1j); nb=[V(1j+d) for d in (0.01,0.01j,-0.01j,0.01*cmath.exp(1j*math.pi/4))]
print(f"V(i)={v0:.2e}, neighbours={[f'{x:.2e}' for x in nb]}, min at i: {all(x>v0 for x in nb)}")
def lnV_y(y):
    q=math.exp(-2*math.pi*y); e2=1-24*sum(n*q**n/(1-q**n) for n in range(1,8)); g=e2-3/(math.pi*y)
    le=-math.pi*y/12+sum(math.log(1-q**k) for k in range(1,8)); N=-math.log(y)-4*le
    return 2*math.log(y)+2*math.log(abs(g))-2*math.log(N)
def infl(alpha,Nst):
    qn=math.sqrt(3*alpha/2)   # dphi = sqrt(3 alpha/2) d ln y
    lv=lambda u:lnV_y(math.exp(u))
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn
    d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2
    us=[0.05+0.005*i for i in range(1400)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    if ue is None: return None
    u=ue; Na=0; du=1e-3
    while Na<Nst and u<14: Na+=qn*du/abs(d1(u)); u+=du
    g=d1(u); hh=d2(u); ev=0.5*g*g
    return math.exp(ue),math.exp(u),1-6*ev+2*(hh+g*g),16*ev
for alpha in (1/3,1):
    for Nst in (52,55.6):
        r=infl(alpha,Nst)
        if r is None: print(f"alpha={alpha:.3f} N*={Nst}: no end"); continue
        ye,ys,ns,rr=r
        print(f"alpha={alpha:.3f} N*={Nst}: y_end={ye:.2f} y*={ys:.1f} n_s={ns:.4f} r={rr:.5f} ({(ns-0.9684)/0.003:+.1f} sigma SPA, {(ns-0.9728)/0.0027:+.1f} SPA+DESI)")
