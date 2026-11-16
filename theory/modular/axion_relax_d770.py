"""D770 (locked PREREG_D770). AI-assisted."""
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
def run(x0):
    y0=3.0; Vx,Vy=grads(x0,y0); v=V(x0,y0); H=math.sqrt(v/3)
    s0=[x0,y0,-2*y0*y0*Vx/(3*H),-2*y0*y0*Vy/(3*H)]
    # end of inflation energy: find eps=1 first
    def epsev(t,s): x,y,vx,vy=s; return 1.5*((vx*vx+vy*vy)/(4*y*y))/rho_tot(s)*2-1   # eps = 3*K/rho
    epsev.terminal=True; epsev.direction=1
    a=solve_ivp(rhs,[0,1e5],s0,events=epsev,rtol=1e-10,atol=1e-12,method='DOP853')
    se=a.y_events[0][0]; Vend=V(se[0],se[1])
    def lowE(t,s): return rho_tot(s)-1e-4*Vend
    lowE.terminal=True; lowE.direction=-1
    def lost(t,s): return s[1]-0.2
    lost.terminal=True
    b=solve_ivp(rhs,[a.t_events[0][0],5e4],se,events=[lowE,lost],rtol=1e-10,atol=1e-12,method='DOP853',max_step=0.5)
    if len(b.t_events[1]): return x0,'LOST',b.y[0,-1],b.y[1,-1],None
    if not len(b.t_events[0]): return x0,'TIMEOUT',b.y[0,-1],b.y[1,-1],None
    xf,yf=b.y_events[0][0][:2]; tr=reduce(complex(xf,yf))
    d=min(abs(tr-RHO),abs(tr-RHOp)); di=abs(tr-1j)
    out='RHO' if d<0.05 else ('I' if di<0.05 else 'OTHER')
    return x0,out,xf,yf,tr
if __name__=="__main__":
    X0=(0.5,0.45,0.4,0.3,0.2,0.1,0.05,0.02)
    with Pool(2) as p: res=p.map(run,X0)
    for x0,o,xf,yf,tr in res: print(f"x0={x0}: {o} final=({xf:.6f},{yf:.6f}) reduced={tr}")
    ok=all(o=='RHO' for x0,o,*_ in res if x0>=0.05) and abs(res[0][2]-0.5)<1e-6
    print("VERDICT:","PASS" if ok else "FAIL")
