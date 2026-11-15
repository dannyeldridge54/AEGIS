"""D597 (locked PREREG_D597_S3_FLAVOUR). AI-assisted."""
import cmath, math, numpy as np
def sig(n,k): return sum(d**k for d in range(1,n+1) if n%d==0)
def E2(t): q=cmath.exp(2j*math.pi*t); return 1-24*sum(sig(n,1)*q**n for n in range(1,200))
def Yd(t): return np.array([-(1/48)*(E2(t/2)+E2((t+1)/2)-8*E2(2*t)), -(math.sqrt(3)/48)*(E2(t/2)-E2((t+1)/2))])
t=4j; q=cmath.exp(2j*math.pi*t); y=Yd(t)
print(f"check at tau=4i: y1={y[0]:.6f} vs 1/8+3q={1/8+3*q:.6f}; y2={y[1]:.3e} vs sqrt3 q^1/2={math.sqrt(3)*cmath.sqrt(q):.3e}")
A=lambda Y:np.array([[Y[1],Y[0]],[Y[0],-Y[1]]])
y=Yd(1j); h=1e-6; yp=(Yd(1j+h)-Yd(1j-h))/(2*h)
s=cmath.sqrt(y[0]**2+y[1]**2); print(f"Y(i) = {y}, s = {s:.6f}, Y'(i) = {yp}")
w,U=np.linalg.eig(A(y)); 
# normalise eigenvectors for complex-symmetric (Takagi-like) use: v^T v = 1
U=np.array([U[:,k]/cmath.sqrt(U[:,k]@U[:,k]) for k in range(2)]).T
Ap=U.T@A(yp)@U; kappa=abs(Ap[0,1])/abs(s)
print(f"eigenvalues {w}; off-diagonal (U^T A(Y') U)_12 = {Ap[0,1]:.5f}; kappa = {kappa:.4f}")
MP=2.435e18; m=1.9e11; M=m/3; gs=106.75; mnu=0.05e-9; v=174.
GN=mnu*M/(8*math.pi*v**2)*M
best=(0,None)
for r in np.logspace(-8,-1,15):
    dM=r*M; lam=math.sqrt(2)*kappa*r/2; c=(M/m)**2*(1-4*(M/m)**2)**1.5*lam**2
    G=c*m**3/(8*math.pi*MP**2); T=(90/(math.pi**2*gs))**0.25*math.sqrt(G*MP)
    x=dM/GN; e=x/(1+x*x); Y=(8/23)*(3/4)*(T/m)*2*e; ok=Y>=8.75e-11 and T>=150
    if Y>best[0]: best=(Y,r)
    print(f"dM/M={r:.1e}: lambda12={lam:.2e} T_RH={T:.2e} GeV x=dM/Gamma_N={x:.2e} eps={e:.2e} Y_B={Y:.2e} {'PASS' if ok else 'fail'}")
print(f"Gamma_N/M = {GN/M:.2e}; max Y_B = {best[0]:.2e} at dM/M={best[1]:.1e}")
