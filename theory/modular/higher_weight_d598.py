"""D598 (locked PREREG_D598_HIGHER_WEIGHT). AI-assisted."""
import cmath, math, numpy as np
def sig(n,k): return sum(d**k for d in range(1,n+1) if n%d==0)
def E2(t): q=cmath.exp(2j*math.pi*t); return 1-24*sum(sig(n,1)*q**n for n in range(1,200))
def Y2(t): return np.array([-(1/48)*(E2(t/2)+E2((t+1)/2)-8*E2(2*t)), -(math.sqrt(3)/48)*(E2(t/2)-E2((t+1)/2))])
def mul(a,b): return np.array([a[0]*b[1]+a[1]*b[0], a[0]*b[0]-a[1]*b[1]])
Y4=lambda t:mul(Y2(t),Y2(t)); Y6=lambda t:mul(Y2(t),Y4(t)); Y8=lambda t:mul(Y4(t),Y4(t))
A=lambda Y:np.array([[Y[1],Y[0]],[Y[0],-Y[1]]])
for name,F in (('k=2',Y2),('k=4',Y4),('k=6',Y6),('k=8',Y8)):
    y=F(1j); h=1e-6; yp=(F(1j+h)-F(1j-h))/(2*h); s=cmath.sqrt(y[0]**2+y[1]**2)
    if abs(s)<1e-10: print(f"{name}: degenerate at i (s={abs(s):.1e})"); continue
    w,U=np.linalg.eig(A(y)); U=np.array([U[:,k]/cmath.sqrt(U[:,k]@U[:,k]) for k in range(2)]).T
    kap=abs((U.T@A(yp)@U)[0,1])/abs(s); YB=1.25e-11*kap/1.2635
    print(f"{name}: Y(i)={np.round(y,5)}, |s|={abs(s):.5f}, kappa={kap:.4f}, Y_B,plateau={YB:.2e} {'PASS' if YB>=8.75e-11 else 'fail'}")
