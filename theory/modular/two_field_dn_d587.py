"""D587 (locked PREREG_D587_TWO_FIELD_DN). AI-assisted. Gradients in mpmath (dps=150) to avoid cancellation."""
import math
import numpy as np
from scipy.integrate import solve_ivp
from mpmath import mp, mpf, mpc, exp, log, pi, re, im, conj
mp.dps=150
EPS=mpf('1e-4'); c=[1,744,196884,21493760,864299970]
def VG(x,y):
    t=mpc(x,y); q=exp(2j*pi*t)
    f=1/q+c[1]-1728+c[2]*q+c[3]*q**2+c[4]*q**3
    fp=2j*pi*(-1/q+c[2]*q+2*c[3]*q**2+3*c[4]*q**3)
    A=abs(f)**2; Ax=2*re(conj(f)*fp); Ay=2*re(conj(f)*1j*fp)
    s=1/(4*pi); I=s*log(1+A/1728**2); Ix=s*Ax/(1728**2+A); Iy=s*Ay/(1728**2+A)
    B=abs(f); Bx=Ax/(2*B); By=Ay/(2*B); I1=s*log(1+B/1728); I1x=s*Bx/(1728+B); I1y=s*By/(1728+B)
    P=I**2; V=P/(P+1)+EPS*I1; dP=1/(P+1)**2
    Vx=dP*2*I*Ix+EPS*I1x; Vy=dP*2*I*Iy+EPS*I1y
    return float(V),float(Vx),float(Vy)
def rhs(N,s):
    x,y,px,py=s; V,Vx,Vy=VG(x,y)
    G=1/(2*y*y); eps=0.5*G*(px*px+py*py)
    ax=-(-2/y*px*py) ; ay=-(1/y*px*px-1/y*py*py)
    gx=Vx/(G*V); gy=Vy/(G*V)
    return [px,py,ax-(3-eps)*(px+gx),ay-(3-eps)*(py+gy)]
def end(N,s): x,y,px,py=s; return 0.5*(px*px+py*py)/(2*y*y)-1
end.terminal=True; end.direction=1
# single-field y* for N*=50 (D575 machinery)
from scipy.optimize import brentq
def lvy(u):
    V,_,_=VG(0,math.exp(u)); return math.log(V)
qn=1/math.sqrt(2)
d1=lambda u,h=1e-4:(lvy(u+h)-lvy(u-h))/(2*h)/qn
eps1=lambda u:0.5*d1(u)**2
us=np.arange(math.log(2.0),math.log(5.0),0.003); ue=None
for A,B in zip(us[:-1],us[1:]):
    if eps1(A)>=1>eps1(B): ue=brentq(lambda u:eps1(u)-1,A,B); break
u=ue; Na=0; du=1e-3
while Na<50: Na+=qn*du/abs(d1(u)); u+=du
y0=math.exp(u); print(f"single-field: y_end={math.exp(ue):.3f}, y*(N=50)={y0:.3f}")
res={}
for x0 in (0,1e-4,1e-3,1e-2,3e-2):
    V,Vx,Vy=VG(x0,y0); G=1/(2*y0*y0)
    p0=[-Vx/(G*V),-Vy/(G*V)]
    sol=solve_ivp(rhs,[0,80],[x0,y0]+p0,events=end,rtol=1e-11,atol=1e-14,method='DOP853')
    Ne=sol.t_events[0][0]; xe=sol.y_events[0][0][0]; res[x0]=Ne
    print(f"x0={x0:g}: N_end={Ne:.10f}  x_end={xe:.6e}  (x_end/x0={'-' if x0==0 else f'{xe/x0:.6f}'})",flush=True)
dN={k:res[k]-res[0] for k in res if k}
for k,v in dN.items(): print(f"dN(x0={k:g}) = {v:.3e}")
pts=[(k,v) for k,v in dN.items() if abs(v)>1e-9]
if pts:
    Nxx=2*np.mean([v/k**2 for k,v in pts]); print(f"N_xx ≈ {Nxx:.3e} (from {len(pts)} points)")
else:
    Nxx=0; print("all |dN| < 1e-9: N_xx below numerical noise")
H=2.2e-6; dx=math.sqrt(2)*y0*H/(2*math.pi); dNiso=0.5*abs(Nxx)*dx**2
print(f"delta x = {dx:.2e}; deltaN_iso = {dNiso:.2e}; ratio to zeta 4.6e-5 = {dNiso/4.6e-5:.2e}; |N(0)-50| = {abs(res[0]-50):.3f}")
