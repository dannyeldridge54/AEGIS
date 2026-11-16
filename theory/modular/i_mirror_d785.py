"""D785 (locked PREREG_D785). AI-assisted."""
import numpy as np, cmath, math, itertools, scipy.linalg as sl
def Yd(t):
    q=cmath.exp(2j*math.pi*t); qh=cmath.exp(1j*math.pi*t)
    Y1=1/8+3*q+3*q**2+12*q**3+3*q**4+18*q**5; Y2=math.sqrt(3)*qh*(1+4*q+6*q**2+8*q**3+13*q**4)
    v=np.array([Y1,Y2]); return v/np.linalg.norm(v)
r=Yd(0.5+1j*math.sqrt(3)/2); print("K4 rho: Y2/Y1 =",r[1]/r[0])
Y=Yd(1j); print("Y(i) direction:",Y, " Y2/Y1 =",Y[1]/Y[0])
A=lambda v: np.array([[v[1],v[0]],[v[0],-v[1]]])
def blk(a,col,row): M=np.zeros((3,3),complex); M[:2,:2]=a; M[:2,2]=col; M[2,:2]=row; return M
def takagi(M):
    U,s,Vh=np.linalg.svd(M); # for symmetric M: M = U S U^T up to phases; use U with phase fix
    W=U.conj().T@M@U.conj(); ph=np.sqrt(np.diag(W)/np.where(abs(np.diag(W))>0,abs(np.diag(W)),1)); return U@np.diag(ph.conj()),s
sv=lambda M: np.sort(np.linalg.svd(M,compute_uv=False))
mags=[0.1,0.2,0.5,1,2,5,10]; ph=[k*math.pi/3 for k in range(6)]
for c in (0.6,1,3):
    MR=blk(A(Y),c*Y,c*Y); s=sv(MR); MRi=np.linalg.inv(MR); UR,sR=takagi(MR)
    print(f"c={c}: M_R SVs {s}")
    deg=no=io=tot=0; colmin=1e9; colmax=0
    for mb,pb,mg,pg in itertools.product(mags,ph,mags,ph):
        MD=blk(A(Y),mb*cmath.exp(1j*pb)*Y,mg*cmath.exp(1j*pg)*Y); tot+=1
        cn=np.linalg.norm(MD@UR,axis=0); colmin=min(colmin,cn.min()/cn.max()); colmax=max(colmax,cn.max())
        a,bb,cc=sv(-MD@MRi@MD.T)
        if min(bb-a,cc-bb)<1e-9*cc: deg+=1
        den=cc**2-a**2
        if den>0:
            if abs((bb**2-a**2)/den/0.0297-1)<=0.1: no+=1
            if abs((cc**2-bb**2)/den/0.0297-1)<=0.1: io+=1
    print(f"c={c}: heavy-state lepton couplings min/max column ratio over grid = {colmin:.2e}; light: degenerate {deg}/{tot}, NO {no}, IO {io}")
