"""D613 (locked PREREG_D613_RHO_NSTAR): D609 functions + D602 N* formula. AI-assisted."""
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

import numpy as np
from scipy.optimize import brentq
MP=2.435e18; As=2.1e-9; gs=106.75; lnk=math.log(0.05*4282.7); E=2.6e-5; yr=math.sqrt(3)/2
ds=np.array([1e-2,5e-3,2e-3,1e-3])
P=lambda t:(lambda x:x/(x+1))(Ic(t)**2)
vals=[P(rho+1j*d) for d in ds]; nfit,lc=np.polyfit(np.log(ds),np.log(vals),1); c12=math.exp(lc)
print(f"plateau near rho: exponent n = {nfit:.3f}, coefficient c = {c12:.3e}")
d=1e-3; mh2=2*E*(Lc(rho+1j*d)-L0)/(d/(math.sqrt(2)*yr))**2
print(f"mass term: m_hat^2 = {mh2:.3e} (V0 units, canonical)")
def infl(N):
    qn=1/math.sqrt(2); lv=lambda u:math.log(Vy(math.exp(u),E))
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn; d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2; us=[math.log(0.9)+0.003*i for i in range(2300)]
    for A,B in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(B): ue=brentq(lambda u:eps(u)-1,A,B); break
    u=ue; Na=0; du=1e-3
    while Na<N: Na+=qn*du/abs(d1(u)); u+=du
    g=d1(u); hh=d2(u); ev=0.5*g*g
    return dict(ys=math.exp(u),ns=1-6*ev+2*(hh+g*g),r=16*ev,Vs=Vy(math.exp(u),E),Vend=Vy(math.exp(ue),E))
def nstar(res,TR,w):
    Vs=1.5*math.pi**2*As*res['r']*MP**4; scale=Vs/res['Vs']; rho_end=res['Vend']*scale
    a=(math.sqrt(2)*yr)**nfit*c12; phx=(mh2/(2*a))**(1/(nfit-2)); rho_x=mh2*phx**2*scale
    rho_R=math.pi**2*gs/30*TR**4
    N=67-lnk+0.25*math.log(Vs**2/(MP**4*rho_end)); rA=max(min(rho_x,rho_end),rho_R)
    N+=(1-3*w)/(12*(1+w))*math.log(rA/rho_end)
    if rA>rho_R: N+=(1/12)*math.log(rho_R/rA)
    return N,rho_x/rho_end
wst=(nfit-2)/(nfit+2); ok=True
for TR in (1e3,1e5):
    for w,lab in ((wst,f'w={wst:.3f}'),(0.0,'w=0')):
        res=infl(50); N,rx=nstar(res,TR,w); res=infl(N); N2,rx=nstar(res,TR,w); res=infl(N2)
        ns=res['ns']-0.0003; ys=res['ys']-0.4; good=abs(ns-0.9728)<=2*0.0027 and ys<=25; ok=ok and good
        print(f"T_R={TR:.0e} {lab}: rho_x/rho_end={rx:.1e} N*={N2:.2f} y*={ys:.1f} n_s={ns:.4f} ({(ns-0.9684)/0.003:+.1f} SPA, {(ns-0.9728)/0.0027:+.1f} S+D) r={res['r']:.2e} {'ok' if good else 'FAIL'}")
print("VERDICT:", "VIABLE" if ok else "NOT VIABLE")
