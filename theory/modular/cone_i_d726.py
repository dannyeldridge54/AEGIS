"""D726 (locked PREREG_D726). AI-assisted."""
import cmath, math, numpy as np
s=open('theory/modular/tr_2p1_d725.py').read(); exec(s[s.index('import cmath'):s.index('rho=complex')])
def Mdbl(t): return 2*t.imag*A(Yd(t))
h=1e-6; t0=1j; MP=2.435e18; m=1.9e11; gs=106.75; can=math.sqrt(2/3)
def analyse(name,F,deg):
    S,U,res=takagi(F(t0)); dM=(F(t0+1j*h)-F(t0-1j*h))/(2*h); P=U.conj().T@dM@U.conj()
    print(f"{name}: SV={np.round(S,6)}, residual {res:.1e}")
    PLL=P[np.ix_(deg,deg)]; ev,O=np.linalg.eigh(PLL.real); Pp=O.T@PLL@O
    print(f"   degenerate block rates (Re eig) = {np.round(ev,6)}; rotated diag={np.round(np.diag(Pp),6)}, off={Pp[0,1]:.4e}")
    for dl in (1e-4,1e-5):
        Sd=np.sort(np.linalg.svd(F(t0*(1+dl)),compute_uv=False)); s0=S[deg[0]]
        near=sorted(Sd,key=lambda v:abs(v-s0))[:2]; print(f"   delta={dl:g}: shifts/delta={np.round(sorted([(v-s0)/dl for v in near]),5)}")
    return S,P,Pp,ev
S,P,Pp,ev=analyse("doublet only",Mdbl,[0,1])
rate=max(abs(ev)); 
if rate<1e-6: print("VERDICT: NULL (quadratic)"); raise SystemExit
for x in (0.1,0.33,0.45):
    sc=x*m/S[0]; g=[abs(Pp[0,0])*sc*can/MP, abs(Pp[1,1])*sc*can/MP, abs(Pp[0,1])*sc*can/MP]
    G=(g[0]**2+g[1]**2)*m*(1-4*x*x)**1.5/(16*math.pi)+g[2]**2*m*(1-4*x*x)**1.5/(8*math.pi)
    TR=(90/(math.pi**2*gs))**0.25*math.sqrt(G*MP); print(f"   M/m={x}: g={np.round(g,12)}, T_R={TR:.3e} GeV")
for c in (0.3,1,3):
    F=lambda t,c=c:(lambda Y:2*t.imag*np.block([[A(Y),c*Y[:,None]],[c*Y[None,:],np.zeros((1,1))]]))(Yd(t))
    Sx=np.linalg.svd(F(t0),compute_uv=False); 
    d=[k for k in range(3) for l in range(3) if k<l and abs(Sx[k]-Sx[l])<1e-9]
    print(f"2+1 c={c}: SV={np.round(Sx,6)}; degenerate pairs present: {bool(d)}")
    if d: analyse(f"  2+1 c={c}",F,[d[0], [l for l in range(3) if l!=d[0] and abs(Sx[l]-Sx[d[0]])<1e-9][0]])
