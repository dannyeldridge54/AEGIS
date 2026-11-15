"""D609 (locked PREREG_D609_SERAPIS_RHO). AI-assisted."""
import math, cmath
from scipy.optimize import brentq
from mpmath import mp, kleinj
mp.dps=40
rho=cmath.exp(2j*math.pi/3)+1   # = 1/2 + i sqrt3/2
def lneta(t): q=cmath.exp(2j*math.pi*t); return 2j*math.pi*t/24+sum(cmath.log(1-q**n) for n in range(1,200))
J=lambda t:complex(kleinj(t))*1728
Ic=lambda t:math.log(1+abs(J(t))**2/1728**2)/(4*math.pi)
Lc=lambda t:-(math.log(2*t.imag)+4*lneta(t).real)
L0=Lc(rho)
def Vc(t,e): x=Ic(t)**2; return x/(x+1)+e*(Lc(t)-L0)
# along x=1/2: real q
def jy(y):
    q=-math.exp(-2*math.pi*y); return 1/q+744+196884*q+21493760*q*q+864299970*q**3
def Iy(y):
    if 2*math.pi*y>300: return 2*(2*math.pi*y-math.log(1728))/(4*math.pi)
    j=jy(y); a=abs(j)
    return (math.log(1+(a/1728)**2) if a<1e150 else 2*(math.log(a)-math.log(1728)))/(4*math.pi)
def Ly(y):
    q=-math.exp(-2*math.pi*y); le=-math.pi*y/12+sum(math.log(1-q**n) for n in range(1,80))
    return -(math.log(2*y)+4*le)
def Vy(y,e): x=Iy(y)**2; return x/(x+1)+e*(Ly(y)-L0)
print(f"check Ly(rho)={Ly(math.sqrt(3)/2):.6f} vs Lc(rho)={L0:.6f}; Iy at y=2: {Iy(2):.6f} vs Ic: {Ic(0.5+2j):.6f}")
h=1e-3
for e in (1e-4,3e-4,1e-3):
    vxx=(Vc(rho+h,e)-2*Vc(rho,e)+Vc(rho-h,e))/h**2; vyy=(Vc(rho+1j*h,e)-2*Vc(rho,e)+Vc(rho-1j*h,e))/h**2
    print(f"eps={e:g}: V(rho)={Vc(rho,e):.2e} Hess(xx,yy)=({vxx:.3e},{vyy:.3e}) V(i)={Vc(1j,e):.3e}")
def infl(e,N):
    qn=1/math.sqrt(2); lv=lambda u:math.log(Vy(math.exp(u),e))
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn; d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2; us=[math.log(0.9)+0.003*i for i in range(2300)]; ue=None
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    if ue is None: return None
    u=ue; Na=0; du=1e-3; first=True
    while Na<N and u<14:
        if not first and eps(u)>1+1e-6: return None
        Na+=qn*du/abs(d1(u)); u+=du; first=False
    if Na<N: return None
    g=d1(u); hh=d2(u); ev=0.5*g*g; return math.exp(ue),math.exp(u),1-6*ev+2*(hh+g*g),16*ev,Vy(math.exp(u),e)
for e in (1e-4,3e-4,1e-3):
    vyy=(Vc(rho+1j*h,e)-2*Vc(rho,e)+Vc(rho-1j*h,e))/h**2; m2=vyy*2*(rho.imag)**2   # canonical: dphi = dy/(sqrt2 y)
    for N in (47,50,53):
        r=infl(e,N)
        if r is None: print(f"eps={e:g} N*={N}: no viable inflation"); continue
        ye,ys,ns,rr,Vs=r; ns-=0.0003; ys-=0.4
        print(f"eps={e:g} N*={N}: y_end={ye:.2f} y*={ys:.1f} {'HS' if ys<=25 else 'OUT'} n_s={ns:.4f} ({(ns-0.9684)/0.003:+.1f} SPA, {(ns-0.9728)/0.0027:+.1f} S+D) r={rr:.2e} m_vac/H={math.sqrt(3*m2/Vs):.3f}")
