import sys, math, json, os; sys.path.insert(0,'.')
import numpy as np
from scipy.interpolate import RectBivariateSpline
from scipy.integrate import solve_ivp
from tools.serapis_calc.shapes import E
Ef=lambda x,y:float(E(complex(x,y),1.5).real)
xs=np.linspace(-0.3,1.3,241); us=np.linspace(math.log(0.05),math.log(25),600)
L=np.array([[math.log(Ef(x,math.exp(u))) for u in us] for x in xs])
S=RectBivariateSpline(xs,us,L,kx=5,ky=5)
rho=(0.5,math.sqrt(3)/2); Erho=Ef(*rho); C=8e-7
def parts(x,y):
    u=math.log(y)
    Lx=S(x,u,dx=1)[0,0]; Lu=S(x,u,dy=1)[0,0]; Ly=Lu/y
    Lxx=S(x,u,dx=2)[0,0]; Lxu=S(x,u,dx=1,dy=1)[0,0]; Luu=S(x,u,dy=2)[0,0]
    Lxy=Lxu/y; Lyy=(Luu-Lu)/y**2
    V0=(4/9)*y*y*(Lx*Lx+Ly*Ly)
    dV0x=(4/9)*y*y*2*(Lx*Lxx+Ly*Lxy)
    dV0y=(4/9)*(2*y*(Lx*Lx+Ly*Ly)+y*y*2*(Lx*Lxy+Ly*Lyy))
    Ev=math.exp(S(x,u)[0,0]); T=1+C*(Ev-Erho)
    V=V0*T; dVx=dV0x*T+V0*C*Ev*Lx; dVy=dV0y*T+V0*C*Ev*Ly
    return V,dVx,dVy,V0
def V0direct(x,y,h=1e-6):
    l=lambda a,b:math.log(Ef(a,b))
    dx=(l(x+h,y)-l(x-h,y))/(2*h); dy=(l(x,y+h)-l(x,y-h))/(2*h); return (4/9)*y*y*(dx*dx+dy*dy)
val=[abs(parts(x,y)[3]-V0direct(x,y)) for x,y in [(0.5,0.9),(0.3,1.2),(0.1,1.5),(0.5,3.0),(0.7,10.0),(0.4,0.1),(0.2,0.2)]]
out={'validation_maxdiff':max(val),'valid':bool(max(val)<1e-5),'runs':{}}
print('validation',out['validation_maxdiff'],out['valid'],flush=True)
def rhs(t,s):
    x,u,vx,vy=s; y=math.exp(u)
    xm=((x+0.3)%1.0)-0.3
    V,dVx,dVy,_=parts(xm,y)
    K=(vx*vx+vy*vy)/(4*y*y); H=math.sqrt(max((K+V)/3,0))
    ax=(2/y)*vx*vy-3*H*vx-2*y*y*dVx
    ay=-(vx*vx-vy*vy)/y-3*H*vy-2*y*y*dVy
    return [vx,vy/y,ax,ay]
def reduce(t):
    for _ in range(200):
        t=complex(t.real-round(t.real),t.imag)
        if abs(t)<1-1e-12: t=-1/t
        else: break
    return t
def energy_event(t,s):
    y=math.exp(s[1]); K=(s[2]**2+s[3]**2)/(4*y*y); return K+parts(((s[0]+0.3)%1)-0.3,y)[0]-1e-4
energy_event.terminal=True; energy_event.direction=-1
def low_event(t,s): return s[1]-math.log(0.06)
low_event.terminal=True; low_event.direction=-1
for dx in (0,1e-6,1e-4,1e-3,1e-2,3e-2):
    x0,y0=0.5+dx,20.0
    V,dVx,dVy,_=parts(x0,y0); H=math.sqrt(V/3); vy0=-2*y0*y0*dVy/(3*H)
    # e-fold counter via H integration
    sol=solve_ivp(lambda t,s:rhs(t,s[:4])+[math.sqrt(max(((s[2]**2+s[3]**2)/(4*math.exp(s[1])**2)+parts(((s[0]+0.3)%1)-0.3,math.exp(s[1]))[0])/3,0))],
                  (0,2000),[x0,math.log(y0),0.0,vy0,0.0],method='DOP853',rtol=1e-9,atol=1e-12,dense_output=True,events=[energy_event,low_event])
    x,y=sol.y[0,-1],math.exp(sol.y[1,-1]); xm=x%1.0
    tr=reduce(complex(x,y)); r1=complex(0.5,rho[1]); r2=complex(-0.5,rho[1])
    cls='i' if abs(tr-1j)<0.15 else ('rho' if min(abs(tr-r1),abs(tr-r2))<0.15 else 'other')
    if len(sol.t_events[1])>0: cls='toward x=1/2 cusp (left domain)'
    ymin=float(np.exp(sol.y[1].min()))
    # end of inflation: first time eps = 1, eps = 3K/(K+V)
    ts=np.linspace(0,sol.t[-1],20000); Nend=None
    for tt in ts:
        s=sol.sol(tt); yy=math.exp(s[1]); K=(s[2]**2+s[3]**2)/(4*yy**2); Vv=parts(((s[0]+0.3)%1)-0.3,yy)[0]
        if 3*K/(K+Vv)>=1: Nend=float(s[4]); yend=float(yy); xend=float(s[0]); break
    out['runs'][str(dx)]=dict(final_x_mod1=float(xm),final_y=float(y),reduced=[float(tr.real),float(tr.imag)],cls=cls,y_min=ymin,N_to_end=Nend,
        end_of_inflation_xy=[xend,yend] if Nend else None,status=sol.status,t_final=float(sol.t[-1]))
    print(dx,out['runs'][str(dx)],flush=True)
os.makedirs('field_tests/results/YFORK',exist_ok=True); json.dump(out,open('field_tests/results/YFORK/run2.json','w'),indent=1)
print(json.dumps({k:v for k,v in out.items() if k!='runs'}))
