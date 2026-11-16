"""D724 (locked PREREG_D724). AI-assisted."""
import cmath, math, numpy as np
s=open('theory/modular/tr_takagi_d721.py').read(); exec(s[s.index('def sig'):s.index('rho=complex')])
def takagi(M):
    W,S,Vh=np.linalg.svd(M); D=Vh.conj()@W.conj()  # robust: build U column-wise
    U=W.copy()
    for k in range(len(S)):
        u=W[:,k]; ph=(u.conj()@M@u.conj()); U[:,k]=u*cmath.exp(0.5j*cmath.phase(ph)) if abs(ph)>1e-14 else u
    res=np.abs(U.conj().T@M@U.conj()-np.diag(S)).max(); return S,U,res
Y4=lambda Y: np.array([2*Y[0]*Y[1], Y[0]**2-Y[1]**2])
def Mmat(t,case,b,c):
    Y=Yd(t); Yw=Y if case=="W2" else Y4(Y)
    M=np.zeros((3,3),complex); M[:2,:2]=A(Y); M[:2,2]=c*Yw; M[2,:2]=c*Yw; M[2,2]=b; return M
rho=complex(0.5,math.sqrt(3)/2); h=1e-6
for case in ("W2","W4"):
    print(f"case {case}:"); Rmin=1
    for b in (0,0.3,1,3):
        for c in (0.3,1,3):
            S,U,res=takagi(Mmat(rho,case,b,c)); R=S[-1]/S[0]; Rmin=min(Rmin,R)
            dM=(Mmat(rho+1j*h,case,b,c)-Mmat(rho-1j*h,case,b,c))/(2*h); B=U.conj().T@dM@U.conj()
            off=[abs(B[0,1]),abs(B[0,2]),abs(B[1,2])]
            print(f"  b={b} c={c}: SV={np.round(S,5)} R={R:.2e} res={res:.0e} off(12,13,23)={np.round(off,4)}")
    print(f"  min R = {Rmin:.2e}")
