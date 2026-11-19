# (c) Danny Lee Eldridge · AEGIS Community License
"""BBN v2 (lock PREREG_GENESIS_BBN2): FD e± background, Born weak rates, n-p-D-He4 network."""
import math, numpy as np
from scipy.integrate import quad, solve_ivp
ME=0.51099895; MN=939.0; BD=2.2246; Q=1.2933; TAU=878.4
MPL=1.22091e22; HBAR=6.582119569e-22; HBARC=1.973269804e-11  # MeV s, MeV cm
NA=6.02214076e23; Z3=1.2020569031595942
SV_NP=4.55e-20
def _e_thermo(T):
    if T<ME/40: return 0.0,0.0
    f=lambda p,k: (lambda E: (p*p*E if k==0 else p**4/(3*E))/(math.exp(min(E/T,700))+1))(math.sqrt(p*p+ME*ME))
    up=60*T+ME
    rho=4/(2*math.pi**2)*quad(lambda p:f(p,0),0,up,limit=200)[0]
    P=4/(2*math.pi**2)*quad(lambda p:f(p,1),0,up,limit=200)[0]
    return rho,P
def s_ge(T):
    re,pe=_e_thermo(T); rg=math.pi**2/15*T**4
    return (4/3*rg+re+pe)/T
def rho_ge(T): return math.pi**2/15*T**4+_e_thermo(T)[0]
q=Q/ME
_f0=quad(lambda x:x*math.sqrt(x*x-1)*(q-x)**2,1,q)[0]; K=1/(TAU*_f0)
def _fd(y): return 1/(1+math.exp(max(min(y,700),-700)))
def rates(T,Tnu):
    z=ME/T; zn=ME/Tnu
    def integ(sgn):   # sgn=+1: n->p ; -1: p->n
        g=lambda x: abs(x)*math.sqrt(x*x-1)*(sgn*q-x)**2*_fd(-x*z)*_fd((x-sgn*q)*zn)
        a=quad(g,1,60/z+q+5,limit=200)[0]+quad(g,-(60/z+q+5),-1,limit=200)[0]
        return K*a
    return integ(1),integ(-1)
def background(dneff=0.0, T0=10.0, T1=0.01, n=500):
    """table of a, T, Tnu, t (s). a=1 at T0."""
    lna=[0.0]; Ts=[T0]
    # integrate dT/dlna = -3 s/(ds/dT)
    def dT(T):
        h=T*1e-4; ds=(s_ge(T+h)-s_ge(T-h))/(2*h); return -3*s_ge(T)/ds
    T=T0; x=0.0
    while T>T1:
        step=0.01
        k1=dT(T); k2=dT(T+0.5*step*k1); k3=dT(T+0.5*step*k2); k4=dT(T+step*k3)
        T+=step*(k1+2*k2+2*k3+k4)/6; x+=step; lna.append(x); Ts.append(T)
    lna=np.array(lna); Ts=np.array(Ts); Tnu=T0*np.exp(-lna)
    rho=np.array([rho_ge(t) for t in Ts])+(3+dneff)*7/8*math.pi**2/15*Tnu**4
    H=np.sqrt(8*math.pi*rho/(3*MPL**2))/HBAR
    t=np.concatenate([[0.5/H[0]],0.5/H[0]+np.cumsum(np.diff(lna)*0.5*(1/H[1:]+1/H[:-1]))])
    return dict(lna=lna,T=Ts,Tnu=Tnu,H=H,t=t)
def run(eta=6.127e-10, dneff=0.0, dd_scale=1.0):
    bg=background(dneff)
    lna,T,Tnu,t=bg['lna'],bg['T'],bg['Tnu'],bg['t']
    # baryon density: n_b/n_gamma = eta at the end
    ngam_end=2*Z3/math.pi**2*(T[-1]/HBARC)**3
    nb=eta*ngam_end*np.exp(3*(lna[-1]-lna))         # cm^-3
    Ti=lambda tt: np.interp(tt,t,T); Tni=lambda tt: np.interp(tt,t,Tnu); nbi=lambda tt: np.interp(tt,t,nb)
    sv_dd=dd_scale*1e8/NA
    idx=np.unique(np.linspace(0,len(t)-1,160).astype(int))
    tab=np.array([rates(T[i],Tnu[i]) for i in idx]); tg=t[idx]
    llnp=np.log(np.maximum(tab[:,0],1e-300)); llpn=np.log(np.maximum(tab[:,1],1e-300))
    def lam(tt):
        return math.exp(np.interp(tt,tg,llnp)), math.exp(np.interp(tt,tg,llpn))
    def f(tt,y):
        Yn,Yp,Yd,Yh=y; Tm=Ti(tt); n_b=nbi(tt); lnp,lpn=lam(tt)
        lgam=SV_NP*(4/3)*(MN*Tm/(4*math.pi))**1.5/HBARC**3*math.exp(-BD/Tm)   # 1/s
        cap=n_b*SV_NP*Yn*Yp; dis=lgam*Yd; dd=n_b*sv_dd*Yd*Yd
        return [-lnp*Yn+lpn*Yp-cap+dis, lnp*Yn-lpn*Yp-cap+dis, cap-dis-dd, 0.5*dd]
    Xn0=1/(1+math.exp(Q/T[0]))
    tsw=float(np.interp(-0.2,-T,t))
    def fa(tt,y):
        lnp,lpn=lam(tt); Yn=y[0]; return [-lnp*Yn+lpn*(1-Yn)]
    sa=solve_ivp(fa,(t[0],tsw),[Xn0],method='BDF',rtol=1e-8,atol=1e-14,dense_output=True)
    Yn0=sa.y[0,-1]; Tm=Ti(tsw)
    lg=SV_NP*(4/3)*(MN*Tm/(4*math.pi))**1.5/HBARC**3*math.exp(-BD/Tm)
    Yd0=nbi(tsw)*SV_NP*Yn0*(1-Yn0)/lg
    sol=solve_ivp(f,(tsw,t[-1]),[Yn0,1-Yn0-Yd0,Yd0,0],method='BDF',rtol=1e-6,atol=1e-16,dense_output=True)
    Yn,Yp,Yd,Yh=sol.y[:,-1]
    tt=np.geomspace(tsw,t[-1],300); Y=sol.sol(tt)
    ta=np.geomspace(t[0],tsw,100); Ya=sa.sol(ta)[0]
    tt=np.concatenate([ta,tt]); Y=np.concatenate([np.vstack([Ya,1-Ya,0*Ya,0*Ya]),Y],axis=1)
    return dict(Yp_He=4*Yh, D_H=Yd/Yp, Xn_free=Yn, t=tt, T=Ti(tt), Yn=Y[0], Yd=Y[2], YHe=4*Y[3], ok=sol.success)
