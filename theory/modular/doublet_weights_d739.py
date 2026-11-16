"""D739 (locked PREREG_D739). AI-assisted."""
import cmath, math, numpy as np
s=open('theory/modular/tr_takagi_d721.py').read(); exec(s[s.index('def sig'):s.index('def takagi')])
rho=complex(0.5,math.sqrt(3)/2); Y=Yd(rho); n=np.array([1,-1j])
prod=lambda X:np.array([Y[1]*X[0]+Y[0]*X[1], Y[0]*X[0]-Y[1]*X[1]])
X=Y.copy(); k=2
while k<=12:
    nx=np.linalg.norm(X); ov=abs(n@X)/nx if nx>1e-12 else float('nan')
    ranks=[]
    for b in (0,1):
        M=np.zeros((3,3),complex); M[:2,:2]=A(Y); M[:2,2]=X; M[2,:2]=X; M[2,2]=b
        sv=np.linalg.svd(M,compute_uv=False); ranks.append(int((sv>1e-9*sv[0]).sum()))
    print(f"k={k:2d}: |Y_k|={nx:.3e}, |n.Y_k|/|Y_k|={ov:.3e}, rank(b=0,b=1)={ranks}, Y_k/|Y_k|={np.round(X/nx,4) if nx>1e-12 else 'zero'}")
    X=prod(X); k+=2
