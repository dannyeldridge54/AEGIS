import sys, math, json, os; sys.path.insert(0,'.')
import numpy as np
from scipy.interpolate import RectBivariateSpline
from scipy.integrate import solve_ivp
from tools.serapis_calc.shapes import E
Ef=lambda x,y:float(E(complex(x,y),1.5).real)
xs=np.linspace(-0.8,0.8,321); us=np.linspace(math.log(0.05),math.log(25),600)
L=np.array([[math.log(Ef(x,math.exp(u))) for u in us] for x in xs])
S=RectBivariateSpline(xs,us,L,kx=5,ky=5)
rho=complex(0.5,math.sqrt(3)/2); Erho=Ef(0.5,rho.imag); C=8e-7
def grads(x,y):
    u=math.log(y); Lx=S(x,u,dx=1)[0,0]; Lu=S(x,u,dy=1)[0,0]; Ly=Lu/y
    Lxx=S(x,u,dx=2)[0,0]; Lxy=S(x,u,dx=1,dy=1)[0,0]/y; Lyy=(S(x,u,dy=2)[0,0]-Lu)/y**2
    V0=(4/9)*y*y*(Lx*Lx+Ly*Ly); dx0=(4/9)*y*y*2*(Lx*Lxx+Ly*Lxy); dy0=(4/9)*(2*y*(Lx*Lx+Ly*Ly)+y*y*2*(Lx*Lxy+Ly*Lyy))
    Ev=math.exp(S(x,u)[0,0]); T=1+C*(Ev-Erho)
    return V0*T, dx0*T+V0*C*Ev*Lx, dy0*T+V0*C*Ev*Ly
def V0direct(x,y,h=1e-6):
    l=lambda a,b:math.log(Ef(a,b)); dx=(l(x+h,y)-l(x-h,y))/(2*h); dy=(l(x,y+h)-l(x,y-h))/(2*h); return (4/9)*y*y*(dx*dx+dy*dy)
val=max(abs(grads(x,y)[0]/(1+C*(Ef(x,y)-Erho))-V0direct(x,y)) for x,y in [(0.5,0.9),(0.3,1.2),(0.1,1.5),(0.0,2.0),(-0.4,0.3)])
print('validation',val,flush=True)
def reduce(t):
    for _ in range(200):
        t=complex(t.real-round(t.real),t.imag)
        if abs(t)<1-1e-12: t=-1/t
        else: break
    return t
def flow(x0,y0):
    def f(t,s):
        x=((s[0]+0.5)%1.0)-0.5; y=math.exp(s[1]); V,gx,gy=grads(x,y)
        return [-2*y*y*gx, -2*y*y*gy/y]
    def stop(t,s):
        x=((s[0]+0.5)%1.0)-0.5; y=math.exp(s[1]); V,gx,gy=grads(x,y); return math.hypot(gx,gy)-1e-10
    stop.terminal=True
    def low(t,s): return s[1]-math.log(0.06)
    low.terminal=True
    sol=solve_ivp(f,(0,1e4),[x0,math.log(y0)],method='LSODA',rtol=1e-8,atol=1e-11,events=[stop,low])
    t=reduce(complex(sol.y[0,-1],math.exp(sol.y[1,-1])))
    if abs(t-1j)<0.1: return 'i'
    if min(abs(t-complex(0.5,rho.imag)),abs(t-complex(-0.5,rho.imag)))<0.1: return 'rho'
    return 'other'
A=[(float(x),flow(x,3.0)) for x in np.linspace(0,0.5,201)]
rng=np.random.default_rng(7); B=[]
while len(B)<2000:
    x=rng.uniform(-0.5,0.5); w=rng.uniform(1/3.0,1.0)   # uniform in 1/y on [1/3,1] => hyperbolic-area-uniform (dA = dx dy/y^2)
    y=1/w
    if x*x+y*y<1: continue
    B.append(flow(x,y))
fi=B.count('i')/len(B); fr=B.count('rho')/len(B)
out=dict(validation=val,A=A,f_i=fi,f_rho=fr,f_other=1-fi-fr,PF3_natural=bool(fi>=0.25))
xi=[x for x,c in A if c=='i']; xr=[x for x,c in A if c=='rho']
out['A_summary']=dict(x_to_i=[min(xi),max(xi)] if xi else None,x_to_rho=[min(xr),max(xr)] if xr else None,n_i=len(xi),n_rho=len(xr))
print(json.dumps({k:v for k,v in out.items() if k!='A'},indent=1))
os.makedirs('field_tests/results/YFORK',exist_ok=True); json.dump(out,open('field_tests/results/YFORK/basins.json','w'),indent=1)
