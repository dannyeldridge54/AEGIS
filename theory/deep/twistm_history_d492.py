import math, sys, io, contextlib
sys.path.insert(0,'theory/deep')
with contextlib.redirect_stdout(io.StringIO()): import modular_twist_d490 as M
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
n,e=233.90,1.614e-7; k=math.sqrt(1.5)
lnV=lambda phi: M.lnV(phi/k,n,e,True)          # phi = k ln x
lam=lambda phi,h=1e-5: -(lnV(phi+h)-lnV(phi-h))/(2*h)
# end of inflation
eps=lambda u:0.5*M.d1(u,n,e,True)**2
us=[-14+0.01*i for i in range(1400)]; ue=next(brentq(lambda u:eps(u)-1,a,b) for a,b in zip(us,us[1:]) if eps(a)<1<=eps(b))
Ntot=63.5; Neq=Ntot-math.log(3400)
def parts(N,x1,ly):
    y2=math.exp(2*ly); rest=max(1-x1*x1-y2,0.0); q=math.exp(N-Neq); Or=rest/(1+q); return y2,Or,rest-Or
def rhs(N,s):   # D1: closure enforced
    phi,x1,ly=s; y2,Or,Om=parts(N,x1,ly)
    L=lam(phi); P=2*x1*x1+(4/3)*Or+Om
    return [math.sqrt(6)*x1, -3*x1+math.sqrt(1.5)*L*y2+1.5*x1*P, -math.sqrt(1.5)*L*x1+1.5*P]
phi0=k*ue; Or0=0.0075; x10=math.sqrt(1/3*(1-Or0)); y0=math.sqrt(2/3*(1-Or0))
s=solve_ivp(rhs,[0,Ntot],[phi0,x10,math.log(y0)],method='LSODA',rtol=1e-8,atol=1e-10,dense_output=True,max_step=0.05)
print(f"x_end(inflation)={math.exp(ue):.3e}; status {s.status} {s.message}")
for N in (0,2,5,10,20,40,Ntot-21,Neq,Ntot-1,Ntot):
    phi,x1,ly=s.sol(N); y2,Or,Om=parts(N,x1,ly); tot=x1*x1+y2+Or+Om
    w=(x1*x1-y2)/(x1*x1+y2) if x1*x1+y2>0 else float('nan')
    print(f"N={N:6.2f}: x={math.exp(phi/k):.4e} Omega_kin={x1*x1:.2e} Omega_V={y2:.2e} Omega_r={Or:.2e} Omega_m={Om:.2e} (sum {tot:.3f}) w_x={w:+.3f}")
