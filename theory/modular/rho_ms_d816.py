"""D816 (locked PREREG_D816): D634 code unchanged + scan. AI-assisted."""
"""D634 (locked PREREG_D634_RHO_RUNNING): D588 MS code with the D609 rho-path potential. AI-assisted."""
import math, numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

L0=0.340372354
def jy(y):
    q=-math.exp(-2*math.pi*y); return 1/q+744+196884*q+21493760*q*q+864299970*q**3
def Iry(y):
    if 2*math.pi*y>300: return 2*(2*math.pi*y-math.log(1728))/(4*math.pi)
    a=abs(jy(y)); return (math.log(1+(a/1728)**2) if a<1e150 else 2*(math.log(a)-math.log(1728)))/(4*math.pi)
def Ly(y):
    q=-math.exp(-2*math.pi*y); le=-math.pi*y/12+sum(math.log(1-q**n) for n in range(1,80)); return -(math.log(2*y)+4*le)
s2=math.sqrt(2)
def V(phi,e): y=math.exp(s2*phi); x=Iry(y)**2; return x/(x+1)+e*(Ly(y)-L0)
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


import numpy as np
e=6e-5; B=background(e)
for Ns in (47,46.09,47.61,47.96,49.49):
    S=[-0.1,-0.05,0,0.05,0.1]; out=[spectra(B,Ns,math.exp(x)) for x in S]; lp=[math.log(o[0]) for o in out]
    ns=[1+(lp[i+1]-lp[i-1])/(S[i+1]-S[i-1]) for i in (1,2,3)]
    al=(ns[2]-ns[0])/0.1; n0=ns[1]; r=out[2][1]/out[2][0]
    print(f"eps=6e-5 N*={Ns}: y*={out[2][2]:.2f} n_s={n0:.4f} r={r:.3e} alpha_s={al:.2e} in_frozen={0.969<=n0<=0.972 and 4.6e-4<=r<=5.1e-4}",flush=True)
