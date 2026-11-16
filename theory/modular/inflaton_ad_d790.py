"""D790 (locked PREREG_D790). D770 code path plus orbit charge. AI-assisted."""
import math, cmath
from scipy.special import kv, zeta
from scipy.integrate import solve_ivp
from multiprocessing import Pool
SIG=[0]+[sum(d**-3 for d in range(1,n+1) if n%d==0) for n in range(1,31)]
def Ese(x,y):
    s=2*zeta(4)*y*y+math.pi*zeta(3)/y
    if 2*math.pi*y<40:
        for n in range(1,31): s+=8*math.pi**2*math.sqrt(y)*n**1.5*SIG[n]*kv(1.5,2*math.pi*n*y)*math.cos(2*math.pi*n*x)
    return s
Er=Ese(0.5,math.sqrt(3)/2); C=1.15e-6
def V(x,y): e=Ese(x,y)-Er; return e/(e+1)*(1+C*e)
def grads(x,y):
    h=1e-6; return (V(x+h,y)-V(x-h,y))/(2*h),(V(x,y+h)-V(x,y-h))/(2*h)
def rho_tot(s): x,y,vx,vy=s; return (vx*vx+vy*vy)/(4*y*y)+V(x,y)
def rhs(t,s):
    x,y,vx,vy=s; Vx,Vy=grads(x,y); H=math.sqrt(max(rho_tot(s),0)/3)
    return [vx,vy,(2/y)*vx*vy-3*H*vx-2*y*y*Vx,-(vx*vx-vy*vy)/y-3*H*vy-2*y*y*Vy]
def reduce(t):
    for _ in range(500):
        t=complex(t.real-round(t.real),t.imag)
        if abs(t)<1-1e-12: t=-1/t
        else: break
    return t
RHO=complex(0.5,math.sqrt(3)/2); RHOp=complex(-0.5,math.sqrt(3)/2)

import numpy as np  # DEVIATIONS D1
RHOc=complex(0.5,math.sqrt(3)/2)
def wdisk(x,y,vx,vy):
    t=complex(x,y); w=(t-RHOc)/(t-RHOc.conjugate())
    dt=complex(vx,vy); dw=dt*((t-RHOc.conjugate())-(t-RHOc))/(t-RHOc.conjugate())**2
    return w,dw
def run(x0):
    y0=3.0; Vx,Vy=grads(x0,y0); v=V(x0,y0); H=math.sqrt(v/3)
    s0=[x0,y0,-2*y0*y0*Vx/(3*H),-2*y0*y0*Vy/(3*H)]
    def epsev(t,s): x,y,vx,vy=s; return 1.5*((vx*vx+vy*vy)/(4*y*y))/rho_tot(s)*2-1
    epsev.terminal=True; epsev.direction=1
    a=solve_ivp(rhs,[0,1e5],s0,events=epsev,rtol=1e-10,atol=1e-12,method='DOP853')
    se=a.y_events[0][0]; Vend=V(se[0],se[1])
    def lowE(t,s): return rho_tot(s)-1e-4*Vend
    lowE.terminal=True; lowE.direction=-1
    b=solve_ivp(rhs,[a.t_events[0][0],5e4],se,events=[lowE],rtol=1e-10,atol=1e-12,method='DOP853',max_step=0.5,dense_output=True)
    tend=b.t_events[0][0] if len(b.t_events[0]) else b.t[-1]
    # average charge over the last ~3 oscillation periods before tend
    ts=np.linspace(max(b.t[0],tend-30),tend,3000); acc=0; en=0
    m2=None
    for t in ts:
        x,y,vx,vy=b.sol(t)
        # map to fundamental-domain neighbourhood of rho: use reduce on tau, carrying velocity via numerical Jacobian
        w,dw=wdisk(x,y,vx,vy)
        acc+=(w.conjugate()*dw).imag; en+=rho_tot([x,y,vx,vy])
    nbar=acc/len(ts); rbar=en/len(ts)
    # canonical normalisation: metric at rho in disk coords ~ const; eta defined as n/(rho/m) with m from oscillation: m ~ omega
    # omega estimate from w phase advance
    w0,_=wdisk(*b.sol(ts[0])); w1,_=wdisk(*b.sol(ts[-1]))
    return x0,nbar,rbar,b.sol(tend)[:2]
if __name__=="__main__":
    X0=(0.5,0.499,0.49,0.45,0.4)
    with Pool(2) as p: res=p.map(run,X0)
    # mass of oscillation from Hessian of V at rho in disk coords (numerical)
    h=1e-4; yr=math.sqrt(3)/2
    Vyy=(V(0.5,yr+h)-2*V(0.5,yr)+V(0.5,yr-h))/h**2; m=math.sqrt(2*yr*yr*Vyy)   # canonical mass^2 = G^-1 V'' = 2y^2 V_yy
    # disk normalisation: near rho, |dw| = |dtau|/(2 y_rho); canonical field chi with dchi = |dtau|/(sqrt2 y) => chi = sqrt2 * |w| ; charge n_chi = 2*Im(w* dw)
    for x0,nbar,rbar,pos in res:
        eta=2*nbar/(rbar/m) if rbar>0 else float('nan')
        print(f"x0={x0}: <Im(w* dw)>={nbar:.3e}, <rho>={rbar:.3e}, m={m:.3e}, eta=n/(rho/m)={eta:.3e}, final tau=({pos[0]:.4f},{pos[1]:.4f})",flush=True)
