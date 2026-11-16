"""D721 (locked PREREG_D721): SERAPIS-E T_R at rho via Takagi decomposition. AI-assisted."""
import cmath, math, numpy as np
def sig(n,k): return sum(d**k for d in range(1,n+1) if n%d==0)
def E2(t): q=cmath.exp(2j*math.pi*t); return 1-24*sum(sig(n,1)*q**n for n in range(1,400))
def Yd(t): return np.array([-(1/48)*(E2(t/2)+E2((t+1)/2)-8*E2(2*t)), -(math.sqrt(3)/48)*(E2(t/2)-E2((t+1)/2))])
A=lambda Y:np.array([[Y[1],Y[0]],[Y[0],-Y[1]]])
def takagi(M):
    W,S,Vh=np.linalg.svd(M); D=Vh.conj().T.T@W   # V^T W
    U=W@np.diag(np.sqrt(np.conj(np.diag(D))))
    best=None
    for s in ((1,1),(1,1j),(1j,1),(1j,1j)):
        Uc=U@np.diag(s); res=np.abs(Uc.conj().T@M@Uc.conj()-np.diag(S)).max()
        if best is None or res<best[0]: best=(res,Uc)
    return S,best[1],best[0]
rho=complex(0.5,math.sqrt(3)/2); y=rho.imag; h=1e-6
S,U,res=takagi(A(Yd(rho))); print(f"1. Takagi at rho: M1={S[0]:.6f}, M2={S[1]:.2e}, residual={res:.1e}")
dA=(A(Yd(rho+1j*h))-A(Yd(rho-1j*h)))/(2*h)                 # d/dy along Re tau = 1/2
K=lambda t:(2*t.imag)                                      # (2y)^{k/2}, k = 2
dAk=((K(rho+1j*h)*A(Yd(rho+1j*h)))-(K(rho-1j*h)*A(Yd(rho-1j*h))))/(2*h)
B=U.conj().T@dA@U.conj(); Bk=U.conj().T@dAk@U.conj(); Bkf=U.conj().T@(dAk-K(rho)*dA)@U.conj()
a12=abs(B[0,1]); print(f"2. a12=|(U^H dA/dy U*)_12|={a12:.6f}; diag terms {abs(B[0,0]):.3e},{abs(B[1,1]):.3e}; Kähler-factor-only off-diagonal={abs(Bkf[0,1]):.2e} (should be 0)")
print(f"   physical (2y A) off-diagonal / (2y M1) = {abs(Bk[0,1])/(K(rho)*S[0]):.6f}; a12/M1 = {a12/S[0]:.6f}")
ok=a12/S[0]>1e-10 and res<1e-10
MP=2.435e18; m=2.2e13; gs=106.75
kap=(a12/S[0])*y*math.sqrt(2/3); print(f"   coupling factor g12*M_P/M1 = {kap:.4f}")
if not ok: print("VERDICT: NULL (locked rule)"); raise SystemExit
T={}
for x in (0.1,0.2,0.33,0.45,0.9):
    g=x*m*kap/MP; G=g*g*m*(1-x*x)**2/(8*math.pi); T[x]=(90/(math.pi**2*gs))**0.25*math.sqrt(G*MP)
    print(f"3. x=M1/m={x}: g12={g:.3e}, Gamma={G:.3e} GeV, T_R={T[x]:.3e} GeV")
lo=min(T[x] for x in (0.2,0.33,0.45)); hi=max(T[x] for x in (0.2,0.33,0.45)); print(f"   PRIMARY T_R band: {lo:.3e} - {hi:.3e} GeV", flush=True)
import mpmath as mp
mp.mp.dps=15
src=open('theory/modular/bhk_tilt_d689.py').read(); exec(src[src.index('def Eser'):src.index('print("1. checks")')])
rh=mp.mpc(0.5,mp.sqrt(3)/2); Er=Eser(rh); s2=mp.sqrt(2); C=mp.mpf('1.15e-6')
Eh=lambda yy: Eser(mp.mpc(0.5,yy))-Er
V=lambda p: (lambda e: e/(e+1)*(1+C*e))(Eh(mp.e**(s2*p)))
d=lambda p,k: mp.diff(V,p,k); eps=lambda p:(d(p,1)/V(p))**2/2
pe=mp.findroot(lambda p:eps(p)-1,mp.log(1.5)/s2)
def at(N):
    ps=mp.findroot(lambda p: mp.quad(lambda w_:V(w_)/d(w_,1),[pe,p])-N, mp.log(15)/s2)
    e=eps(ps); hh=d(ps,2)/V(ps); return float(1-6*e+2*hh), float(16*e), float(V(ps)/V(pe))
As=2.1e-9; lnk=math.log(0.05/(67.4/299792.458))
for TR in (lo,hi):
    N=49.0
    for it in range(30):
        ns,r,ratio=at(N); Vs=1.5*math.pi**2*As*r*MP**4; rho_end=1.5*Vs/ratio; rho_th=math.pi**2/30*gs*TR**4
        Nn=67-lnk+0.25*math.log(Vs**2/(MP**4*rho_end))+(1/12)*math.log(min(rho_th,rho_end)/rho_end)-(1/12)*math.log(gs)
        if abs(Nn-N)<0.01: N=Nn; break
        N=Nn
    print(f"4. T_R={TR:.3e}: N*={N:.2f}, n_s={ns:.4f}, r={r:.3e}", flush=True)
