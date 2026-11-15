"""D500 (locked PREREG_D500_TWISTM_CASE1). AI-assisted."""
import math, sys, io, contextlib
sys.path.insert(0,'theory/deep')
with contextlib.redirect_stdout(io.StringIO()): import modular_twist_d490 as M
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
MP,gs,g=2.435e18,106.75,0.7; c=math.sqrt(2/3); n,e=234.054,1.614e-7; xs=6.58e-5; Vs=4.95e63
a=7599; Vol=(2*a)**1.5; Ms=0.5**0.25*math.sqrt(math.pi/Vol)*MP
L0=M.lnV(math.log(xs),n,e,True)
def VM(phi):  # M_P^4 units
    return Vs/MP**4*math.exp(M.lnV(c*phi*0+phi*c if False else phi*c,n,e,True)-L0) if False else Vs/MP**4*math.exp(M.lnV(c*phi,n,e,True)-L0)
zM=lambda x:(2/math.pi)*math.atan(x)-0.5; zMp=lambda x:(2/math.pi)/(1+x*x)
eps=lambda u:0.5*M.d1(u,n,e,True)**2
us=[-14+0.01*i for i in range(1400)]; ue=next(brentq(lambda u:eps(u)-1,A,B) for A,B in zip(us,us[1:]) if eps(A)<1<=eps(B))
def run(ms):
    kFI=ms**2*Ms**2/MP**4
    V=lambda p: VM(p)+kFI*abs(zM(math.exp(c*p)))
    def dV(p,h=1e-6):
        x=math.exp(c*p); dM=(VM(p+h)-VM(p-h))/(2*h)
        return dM+kFI*math.copysign(1,zM(x))*zMp(x)*c*x
    V0=VM(c**-1*ue*c/c if False else ue/c); Or0=0.0075
    rho_r0=Or0*V0/(1-Or0)*1.5   # radiation at start: Omega_r0 of total, total = V0*1.5 (eps=1)
    def rhs(N,y):
        p,dp=y; rr=rho_r0*math.exp(-4*N); H2=(rr+V(p))/(3-0.5*dp*dp)
        epsH=0.5*dp*dp+(2/3)*rr/H2
        return [dp,-(3-epsH)*dp-dV(p)/H2]
    p0=ue/c; dp0=math.sqrt(2*(1-Or0))
    s=solve_ivp(rhs,[0,42],[p0,dp0],method='LSODA',rtol=1e-9,atol=1e-12,max_step=0.01)   # D1: no events
    Nc=[]; yc=[]
    for i in range(len(s.t)-1):
        a_,b_=s.y[0,i],s.y[0,i+1]
        if a_==0 or a_*b_<0:
            f=a_/(a_-b_) if a_!=b_ else 0.0; Nc.append(s.t[i]+f*(s.t[i+1]-s.t[i])); yc.append((0.0,s.y[1,i]+f*(s.y[1,i+1]-s.y[1,i])))
    rem=0.0
    for N,(p,dp) in zip(Nc,yc):
        rr=rho_r0*math.exp(-4*N); H2=(rr+V(p))/(3-0.5*dp*dp); H=math.sqrt(H2)*MP
        T=(30*rr*MP**4/(math.pi**2*gs))**0.25; xdot=c*1.0*H*abs(dp)
        R=g*g*zMp(1.0)*Ms**2*xdot; m2=(R/2)**(2/3); Vres=ms**2*m2/g**2
        # cap: available V_FI energy at the turning amplitude ~ k*|zeta| with amplitude from kinetic energy
        Ekin=0.5*(H*abs(dp))**2*MP**2; Vres=min(Vres,Ekin)
        rem+=Vres/(2*math.pi**2/45*gs*T**3)
    pf,dpf=s.y[:,-1]; rrf=rho_r0*math.exp(-4*42); H2f=(rrf+V(pf))/(3-0.5*dpf*dpf); Ox=(0.5*dpf*dpf*H2f+V(pf))/(3*H2f)
    xs_=[math.exp(c*q) for q in s.y[0]]
    print(f"m_s={ms:.0e} GeV: M_s={Ms:.2e} GeV; crossings {len(Nc)} (first N={Nc[0] if len(Nc) else None}); x range [{min(xs_):.3e}, {max(xs_):.3e}]; "
          f"|ln x|(N=42)={abs(c*pf):.2e}, Omega_x(N=42)={Ox:.2e}; remnant rho/s={rem:.2e} GeV (x{rem/4.3e-10:.1e} DM); status {s.status}",flush=True)
    last=Nc[-1] if len(Nc) else None; print(f"   last crossing N={last}",flush=True)
for ms in (1e-9,1e4): run(ms)
