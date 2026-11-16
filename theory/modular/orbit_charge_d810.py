"""D810 (locked PREREG_D810). Read-out fix of D790; physics imported unchanged. AI-assisted."""
import sys, math, itertools, numpy as np
sys.path.insert(0,'theory/modular')
import inflaton_ad_d790 as M
from scipy.integrate import solve_ivp
from multiprocessing import Pool
RHO=complex(0.5,math.sqrt(3)/2)
IM=set()
for a,b,c,d in itertools.product(range(-3,4),repeat=4):
    if a*d-b*c==1:
        z=(a*RHO+b)/(c*RHO+d)
        if z.imag>0.05: IM.add((round(z.real,9),round(z.imag,9)))
IM=[complex(*p) for p in IM]
def run(x0):
    y0=3.0; Vx,Vy=M.grads(x0,y0); v=M.V(x0,y0); H=math.sqrt(v/3)
    s0=[x0,y0,-2*y0*y0*Vx/(3*H),-2*y0*y0*Vy/(3*H)]
    def epsev(t,s): x,y,vx,vy=s; return 1.5*((vx*vx+vy*vy)/(4*y*y))/M.rho_tot(s)*2-1
    epsev.terminal=True; epsev.direction=1
    a=solve_ivp(M.rhs,[0,1e5],s0,events=epsev,rtol=1e-10,atol=1e-12,method='DOP853')
    se=a.y_events[0][0]; Vend=M.V(se[0],se[1])
    def lowE(t,s): return M.rho_tot(s)-1e-4*Vend
    lowE.terminal=True; lowE.direction=-1
    b=solve_ivp(M.rhs,[a.t_events[0][0],5e4],se,events=[lowE],rtol=1e-10,atol=1e-12,method='DOP853',max_step=0.5,dense_output=True)
    tend=b.t_events[0][0] if len(b.t_events[0]) else b.t[-1]
    pf=b.sol(tend); tf=complex(pf[0],pf[1]); c=min(IM,key=lambda z:abs(z-tf))
    ts=np.linspace(max(b.t[0],tend-30),tend,3000); acc=0; en=0
    for t in ts:
        x,y,vx,vy=b.sol(t); tau=complex(x,y); dt=complex(vx,vy)
        w=(tau-c)/(tau-c.conjugate()); dw=dt*((tau-c.conjugate())-(tau-c))/(tau-c.conjugate())**2
        acc+=(w.conjugate()*dw).imag; en+=M.rho_tot([x,y,vx,vy])
    return x0,acc/len(ts),en/len(ts),c,tf
if __name__=="__main__":
    h=1e-4; yr=math.sqrt(3)/2
    Vyy=(M.V(0.5,yr+h)-2*M.V(0.5,yr)+M.V(0.5,yr-h))/h**2; m=math.sqrt(2*yr*yr*Vyy)
    with Pool(4) as p: res=p.map(run,(0.48,0.45,0.40,0.55))
    for x0,nbar,rbar,c,tf in res:
        eta=2*nbar/(rbar/m); dx=abs(x0-0.5)
        print(f"x0={x0}: centre c=({c.real:.4f},{c.imag:.4f}), final=({tf.real:.4f},{tf.imag:.4f}), eta={eta:+.4e}, |eta|/dx={abs(eta)/dx:.2f}",flush=True)
