"""D727 (locked PREREG_D727). AI-assisted."""
import cmath, math, numpy as np
s=open('theory/modular/tr_2p1_d725.py').read(); exec(s[s.index('import cmath'):s.index('rho=complex')])
h=1e-6
# Method A: Takagi of A (no 2y factor; it is diagonal in this basis)
Ai=A(Yd(1j)); S,U,res=takagi(Ai); dA=(A(Yd(1j*(1+h)))-A(Yd(1j*(1-h))))/(2*h); P=U.conj().T@dA@U.conj()
print(f"A: SV={np.round(S,6)}, residual {res:.1e}, |P12|={abs(P[0,1]):.6f}, P12={P[0,1]:.4e}, kappa=|P12|/s={abs(P[0,1])/S[0]:.4f}")
# note: degenerate block -> basis freedom; invariant = sqrt(|det-free| ...): use eigenvalues of the imaginary block
K=(P*(-1j)).real if np.allclose(P.real,0,atol=1e-9) else None
if K is not None: print(f"   P is purely imaginary; eigenvalues of iP block: {np.round(np.linalg.eigvalsh(K),6)} (basis-invariant)")
# Method B: real eigenvectors
def ev(y):
    w,V=np.linalg.eigh(A(Yd(1j*y)).real); return w,V
w0,V0=ev(1.0); wp,Vp=ev(1+h); wm,Vm=ev(1-h)
fix=lambda V:V*np.sign(np.diag(V0.T@V))
th=(np.arcsin((V0.T@fix(Vp))[1,0])-np.arcsin((V0.T@fix(Vm))[1,0]))/(2*h)
print(f"B: eigenvalues {np.round(w0,6)} (traceless: sum={w0.sum():.1e}); theta'={th:.6f}; (l1-l2)*theta'={abs((w0[1]-w0[0])*th):.6f}; real (O^T A' O)_12={(V0.T@dA.real@V0)[0,1]:.6f}")
agree=abs(abs((w0[1]-w0[0])*th)-abs(P[0,1]))/abs(P[0,1]); print(f"   A vs B relative difference = {agree:.2e}")
if agree>0.01: print("VERDICT: NULL (locked)"); raise SystemExit
kap=abs(P[0,1])/S[0]; lam=math.sqrt(2)*kap; MP=2.435e18; m=2.65e11
for gs in (106.75,228.75):
    for x in (0.1,0.2,0.33,0.45):
        M=x*m; G=(M*lam/MP)**2*m*(1-4*x*x)**0.5/(8*math.pi); TR=(90/(math.pi**2*gs))**0.25*math.sqrt(G*MP)
        print(f"g*={gs}: M/m={x}: lambda={lam:.3f}, Gamma={G:.3e} GeV, T_R={TR:.3e} GeV")
