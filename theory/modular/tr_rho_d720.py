"""D720 (locked PREREG_D720): SERAPIS-E T_R from the sterile off-diagonal decays at tau = rho, then N*. AI-assisted."""
import cmath, math, numpy as np
def sig(n,k): return sum(d**k for d in range(1,n+1) if n%d==0)
def E2(t): q=cmath.exp(2j*math.pi*t); return 1-24*sum(sig(n,1)*q**n for n in range(1,400))
def Yd(t): return np.array([-(1/48)*(E2(t/2)+E2((t+1)/2)-8*E2(2*t)), -(math.sqrt(3)/48)*(E2(t/2)-E2((t+1)/2))])
A=lambda Y:np.array([[Y[1],Y[0]],[Y[0],-Y[1]]])
rho=complex(0.5,math.sqrt(3)/2); h=1e-6
print("1. sterility check (invariant mass^2 = y^2 * |Y|^2 summed over doublet, k=2)")
inv=lambda t: (t.imag)**2*np.vdot(Yd(t),Yd(t)).real
for name,t in (("i",1j),("rho",rho)):
    gx=(inv(t+h)-inv(t-h))/(2*h); gy=(inv(t+1j*h)-inv(t-1j*h))/(2*h)
    print(f"  at {name}: inv={inv(t):.6e}, |grad|/inv={math.hypot(gx,gy)/inv(t):.2e}")
print("2. off-diagonal coupling at rho")
y=Yd(rho); yp=(Yd(rho+h)-Yd(rho-h))/(2*h); s=cmath.sqrt(y[0]**2+y[1]**2)
w,U=np.linalg.eig(A(y)); print(f"  Y(rho)={y}, s={s:.6f}, eigenvalues {w}, |w1|-|w2|={abs(w[0])-abs(w[1]):.2e}")
U=np.array([U[:,k]/cmath.sqrt(U[:,k]@U[:,k]) for k in range(2)]).T
Ap=U.T@A(yp)@U; kappa=abs(Ap[0,1])/abs(s); print(f"  (U^T A(Y') U)_12 = {Ap[0,1]:.5f}; kappa(rho) = {kappa:.4f} (D597 at i: 1.26)")
print("3. T_R grid, m = 2.2e13 GeV")
MP=2.435e18; m=2.2e13
def TR(Mr,r,gs=106.75):
    lam=math.sqrt(2)*kappa*r/2; c=Mr**2*(1-4*Mr**2)**1.5*lam**2
    G=c*m**3/(8*math.pi*MP**2); return (90/(math.pi**2*gs))**0.25*math.sqrt(G*MP)
prim=[]
for Mr in (0.1,0.2,0.33,0.45):
    row=[]
    for r in (1e-3,1e-2,0.1,0.3):
        T=TR(Mr,r); row.append(f"{T:.2e}")
        if Mr>=0.2 and r>=1e-2: prim.append(T)
    print(f"  M/m={Mr}: "+"  ".join(f"dM/M={r:g}:{v}" for r,v in zip((1e-3,1e-2,0.1,0.3),row)))
print(f"  g*=228.75 factor: {TR(0.33,0.1,228.75)/TR(0.33,0.1):.3f}")
lo,hi=min(prim),max(prim); print(f"  PRIMARY band: T_R = {lo:.2e} - {hi:.2e} GeV")
print("4. sfermion channel (D601 scaling ~ m_soft^4/(M_P^2 m)): at i, m=1.9e11 gave 350-710 GeV; at m=2.2e13 it falls by sqrt(1.9e11/2.2e13)=0.093 -> 33-66 GeV (estimate), subdominant")
print("5. N* (D719 code)")
import mpmath as mp
mp.mp.dps=20
src=open('theory/modular/bhk_tilt_d689.py').read()
exec(src[src.index('def Eser'):src.index('print("1. checks")')])
rh=mp.mpc(0.5,mp.sqrt(3)/2); Er=Eser(rh); s2=mp.sqrt(2); C=mp.mpf('1.15e-6')
Eh=lambda yy: Eser(mp.mpc(0.5,yy))-Er
V=lambda p: (lambda e: e/(e+1)*(1+C*e))(Eh(mp.e**(s2*p)))
d=lambda p,k: mp.diff(V,p,k); eps=lambda p:(d(p,1)/V(p))**2/2
pe=mp.findroot(lambda p:eps(p)-1,mp.log(1.5)/s2)
def at(N):
    ps=mp.findroot(lambda p: mp.quad(lambda w_:V(w_)/d(w_,1),[pe,p])-N, mp.log(15)/s2)
    e=eps(ps); hh=d(ps,2)/V(ps); return float(1-6*e+2*hh), float(16*e), float(V(ps)/V(pe))
As=2.1e-9; g=106.75; lnk=math.log(0.05/(67.4/299792.458))
mid=math.sqrt(lo*hi)
for T in (lo,mid,hi):
    N=49.0
    for it in range(30):
        ns,r,ratio=at(N); Vs=1.5*math.pi**2*As*r*MP**4; rho_end=1.5*Vs/ratio; rho_th=math.pi**2/30*g*T**4
        Nn=67-lnk+0.25*math.log(Vs**2/(MP**4*rho_end))+(1/12)*math.log(rho_th/rho_end)-(1/12)*math.log(g)
        if abs(Nn-N)<0.01: N=Nn; break
        N=Nn
    print(f"  T_R={T:.2e}: N*={N:.2f}, n_s={ns:.4f}, r={r:.3e}")
