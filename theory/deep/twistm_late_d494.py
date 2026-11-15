import math, sys, io, contextlib
sys.path.insert(0,'theory/deep')
with contextlib.redirect_stdout(io.StringIO()): import modular_twist_d490 as M
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
e=1.614e-7; k=math.sqrt(1.5); MP=2.435e18
Vs=1.5*math.pi**2*2.1e-9*0.00453*MP**4; tgt=2.5e-47/Vs
def gap(n): xs=M.obs(n,e,True)[0]; return (M.lnV(0.0,n,e,True)-M.lnV(math.log(xs),n,e,True))-math.log(tgt)
n=brentq(gap,150,400,xtol=1e-4); print(f"D494: V_*={Vs:.2e} GeV^4, Lambda/V_*={tgt:.2e}, n={n:.3f} (was 233.90)")
lnV=lambda phi: M.lnV(phi/k,n,e,True); lam=lambda phi,h=1e-5: -(lnV(phi+h)-lnV(phi-h))/(2*h)
eps=lambda u:0.5*M.d1(u,n,e,True)**2
us=[-14+0.01*i for i in range(1400)]; ue=next(brentq(lambda u:eps(u)-1,a,b) for a,b in zip(us,us[1:]) if eps(a)<1<=eps(b))
Ntot=66.0; Neq=63.5-math.log(3400)
def parts(N,x1,ly):
    y2=math.exp(2*ly); rest=max(1-x1*x1-y2,0.0); q=math.exp(N-Neq); Or=rest/(1+q); return y2,Or,rest-Or
def rhs(N,s):
    phi,x1,ly=s; y2,Or,Om=parts(N,x1,ly); L=lam(phi); P=2*x1*x1+(4/3)*Or+Om
    return [math.sqrt(6)*x1,-3*x1+math.sqrt(1.5)*L*y2+1.5*x1*P,-math.sqrt(1.5)*L*x1+1.5*P]
Or0=0.0075; s=solve_ivp(rhs,[0,Ntot],[k*ue,math.sqrt((1-Or0)/3),math.log(math.sqrt(2*(1-Or0)/3))],method='LSODA',rtol=1e-8,atol=1e-10,dense_output=True,max_step=0.05)
def Ox(N): phi,x1,ly=s.sol(N); return x1*x1+math.exp(2*ly)
def w(N): phi,x1,ly=s.sol(N); y2=math.exp(2*ly); return (x1*x1-y2)/(x1*x1+y2)
Nt=brentq(lambda N:Ox(N)-0.69,55,Ntot)
w0=w(Nt); wa=(w(Nt-math.log(2))-w0)/0.5
print(f"D495: today N={Nt:.2f} (assumed 63.5 before), x={math.exp(s.sol(Nt)[0]/k):.5f}, w0={w0:+.4f}, wa={wa:+.4f}, Omega_x(rec)={Ox(Nt-math.log(1100)):.2e} ->", "LAMBDA-LIKE" if abs(1+w0)<0.01 and abs(wa)<0.05 else "NOT LAMBDA-LIKE")
Ns=[0.01*i for i in range(1001)]; kin=[s.sol(N)[1]**2 for N in Ns]; dk=sum(0.01 for v in kin if v>0.5)
dN=0.5*(dk-1.5); print(f"D496: kination length {dk:.2f} e-folds (D391 assumed 1.5) -> dN* = {dN:+.2f}, n_s shift ~ {2*dN/57.2**2:+.1e}")
