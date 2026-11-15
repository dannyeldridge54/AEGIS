"""D632 (locked PREREG_D632_RUNNING): D588 MS code reused. AI-assisted."""
import math, numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
def Ljm(y): q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q); return lj+math.log(abs(1-1728*math.exp(-lj)))
def Iy(y): l=Ljm(y); return (math.log(math.exp(2*(l-math.log(1728)))+1) if l<300 else 2*(l-math.log(1728)))/(4*math.pi)
def I1y(y): l=Ljm(y); return (math.log(math.exp(l-math.log(1728))+1) if l<300 else (l-math.log(1728)))/(4*math.pi)
s2=math.sqrt(2)
def V(phi,e): y=math.exp(s2*phi); x=Iy(y)**2; return x/(x+1)+e*I1y(y)
def dlnV(phi,e,h=1e-5): return (math.log(V(phi+h,e))-math.log(V(phi-h,e)))/(2*h)
def background(e):
    phi0=math.log(40)/s2
    def rhs(N,s): p,v=s; eps=0.5*v*v; return [v,-(3-eps)*(v+dlnV(p,e))]
    def end(N,s): return 0.5*s[1]**2-1
    end.terminal=True; end.direction=1
    v0=-dlnV(phi0,e)
    sol=solve_ivp(rhs,[0,1000],[phi0,v0],events=end,rtol=1e-10,atol=1e-12,dense_output=True,max_step=0.05)
    Ne=sol.t_events[0][0]; Ns=np.linspace(0,Ne,int(Ne*400)); P,Vv=sol.sol(Ns)
    eps1=0.5*Vv**2; Hs=np.sqrt(np.array([V(p,e) for p in P])/(3-eps1))
    ln_e=np.log(eps1); eps2=np.gradient(ln_e,Ns)
    return dict(Ne=Ne,N=Ns,phi=P,eps1=CubicSpline(Ns,eps1),eps2=CubicSpline(Ns,eps2),lnH=CubicSpline(Ns,np.log(Hs)),phiS=CubicSpline(Ns,P))
def spectra(B,Nstar,kfac):
    Np=B['Ne']-Nstar; lnaH=lambda N:N+B['lnH'](N); lnk=lnaH(Np)+math.log(kfac)
    kah=lambda N:math.exp(lnk-lnaH(N))
    Ni=brentq(lambda N:math.log(kah(N))-math.log(200),0,Np); Nf=brentq(lambda N:math.log(kah(N))-math.log(1e-3),Np,B['Ne'])
    k=math.exp(lnk); a=math.exp(Ni); z=a*math.sqrt(2*B['eps1'](Ni)); r0=kah(Ni)
    v=1/math.sqrt(2*k)
    R0=v/z; Rp0=R0*(-1j*r0-1-B['eps2'](Ni)/2)
    h0=2*v/a; hp0=h0*(-1j*r0-1)
    def rhs(N,s):
        R,Rp,h,hp=s[0]+1j*s[1],s[2]+1j*s[3],s[4]+1j*s[5],s[6]+1j*s[7]; e1=B['eps1'](N); e2=B['eps2'](N); q=kah(N)**2
        Rpp=-(3-e1+e2)*Rp-q*R; hpp=-(3-e1)*hp-q*h
        return [Rp.real,Rp.imag,Rpp.real,Rpp.imag,hp.real,hp.imag,hpp.real,hpp.imag]
    sc=1/abs(R0); st=1/abs(h0)
    R0n,Rp0n,h0n,hp0n=R0*sc,Rp0*sc,h0*st,hp0*st
    y0=[R0n.real,R0n.imag,Rp0n.real,Rp0n.imag,h0n.real,h0n.imag,hp0n.real,hp0n.imag]
    sol=solve_ivp(rhs,[Ni,Nf],y0,rtol=1e-10,atol=1e-12,method='DOP853')
    R=(sol.y[0,-1]+1j*sol.y[1,-1])/sc; h=(sol.y[4,-1]+1j*sol.y[5,-1])/st
    PR=k**3*abs(R)**2/(2*math.pi**2); Pt=2*k**3*abs(h)**2/(2*math.pi**2)
    return PR,Pt,math.exp(s2*B['phiS'](Np))
# old slow-roll count (D575/D581 code)
def old(e,N):
    qn=1/math.sqrt(2); lv=lambda u:math.log((lambda x:x/(x+1))(Iy(math.exp(u))**2)+e*I1y(math.exp(u)))
    d1=lambda u,h=1e-4:(lv(u+h)-lv(u-h))/(2*h)/qn; d2=lambda u,h=1e-3:((lv(u+h)-2*lv(u)+lv(u-h))/h**2)/qn**2
    eps=lambda u:0.5*d1(u)**2; us=[0.02+0.003*i for i in range(2300)]
    for A,Bb in zip(us[::-1][1:],us[::-1][:-1]):
        if eps(A)>=1>eps(Bb): ue=brentq(lambda u:eps(u)-1,A,Bb); break
    u=ue; Na=0; du=1e-3
    while Na<N: Na+=qn*du/abs(d1(u)); u+=du
    g=d1(u); hh=d2(u); ev=0.5*g*g; return 1-6*ev+2*(hh+g*g),16*ev,math.exp(u)

import numpy as np
for name,e in (('HS-Kairos',0.0),('two-term 1.0e-4',1e-4),('two-term 1.3e-4',1.3e-4),('two-term 1.6e-4',1.6e-4)):
    B=background(e)
    for Ns in (47,50):
        S=[-0.1,-0.05,0,0.05,0.1]; lp=[math.log(spectra(B,Ns,math.exp(x))[0]) for x in S]
        ns=[1+(lp[i+1]-lp[i-1])/(S[i+1]-S[i-1]) for i in (1,2,3)]
        a=(ns[2]-ns[0])/0.1; n0=ns[1]; att=-(1-n0)**2/2
        print(f"{name} N*={Ns}: n_s={n0-0.0:.4f} alpha_s={a:.2e} attractor={att:.2e} ratio={a/att:.2f}",flush=True)
