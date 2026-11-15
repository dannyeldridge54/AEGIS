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
# --- D497/D498 (appended after lock PREREG_D497_D498_TWISTM) ---
gs=106.75; T_end=(30*0.0075*Vs/(math.pi**2*gs))**0.25; xs=6.58e-5; a=1/(2*xs)
best=(1e99,None)
for N in [0.01*i for i in range(2001)]:
    x=math.exp(s.sol(N)[0]/k); T=T_end*math.exp(-N); r_=MP/(a*x)/T
    if r_<best[0]: best=(r_,N,x,T)
print(f"D497: a={a:.0f}, T_end={T_end:.2e} GeV, min m_KK/T={best[0]:.2f} at N={best[1]:.2f} (x={best[2]:.2f}, T={best[3]:.2e}) ->", "PASS" if best[0]>=3 else "FAIL")
Na=next(N for N in [Nt-0.001*i for i in range(60000)] if abs(math.exp(s.sol(N)[0]/k)-1)>0.01)   # last time outside 1%, scanning back from today
phi,x1,ly=s.sol(Na); dp=math.sqrt(6)*abs(x1)
y2=math.exp(2*ly); Hrel=None
# H from Omega_V: V/(3H^2 M_P^2)=y2 -> H^2 = V/(3 y2 M_P^2); V(x) = V_* * exp(lnV(x)-lnV(x*))
Vx=Vs*math.exp(M.lnV(phi/k,n,e,True)-M.lnV(math.log(xs),n,e,True)); H=math.sqrt(Vx/(3*y2))/MP
c=math.sqrt(2/3); xdot=c*1.0*H*dp; zp=2.4694e-3; g=0.7; Vol=(2*a*1.0)**1.5; Ms=0.5**0.25*math.sqrt(math.pi/Vol)*MP
R=g*g*zp*Ms**2*xdot; m2=(R/2)**(2/3); Vres=m2*m2/g**2*0+ (1.0)  # placeholder removed below
ms=1e-9
Vres=ms**2*m2/g**2; T=(30*(3*H*H*MP*MP)/(math.pi**2*gs))**0.25
share=Vres/(3*H*H*MP*MP)
print(f"D498: arrival N={Na:.2f}, |dphi/dN|={dp:.2e}, H={H:.2e} GeV, M_s={Ms:.2e} GeV, residual share (m_s=1 eV)={share:.1e}; (m_s=1e4 GeV: {share*1e26:.1e}) ->", "NO REMNANT PROBLEM" if share*1e26<1e-20 else "CHECK")
