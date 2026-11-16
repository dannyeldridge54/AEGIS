"""D777 (locked PREREG_D777). AI-assisted."""
import numpy as np, itertools, math, cmath
Y=np.array([1,1j])/math.sqrt(2)
A=np.array([[Y[1],Y[0]],[Y[0],-Y[1]]])
def blk(a,cvec_col,cvec_row):
    M=np.zeros((3,3),complex); M[:2,:2]=a; M[:2,2]=cvec_col; M[2,:2]=cvec_row; return M
sv=lambda M: np.sort(np.linalg.svd(M,compute_uv=False))
mags=[0.1,0.2,0.5,1,2,5,10]; ph=[k*math.pi/3 for k in range(6)]
for c in (0.6,1,3):
    MR=blk(A,c*Y,c*Y); s=sv(MR); print(f"c={c}: M_R SVs {s} (D725 ratio pair/single = {0.2745*c/0.38817:.4f}; here {s[0]/s[2] if s[0]==s[1] else s[1]/s[2]:.4f})")
    MRi=np.linalg.inv(MR); no=io=0; sNO=[]; sIO=[]; tot=0
    for mb,pb,mg,pg in itertools.product(mags,ph,mags,ph):
        b=mb*cmath.exp(1j*pb); g=mg*cmath.exp(1j*pg)
        MD=blk(A,b*Y,g*Y); mn=-MD@MRi@MD.T; a,bb,cc=sv(mn); tot+=1
        den=cc**2-a**2
        if den<=0: continue
        k=math.sqrt(2.5e-3/den)
        if abs((bb**2-a**2)/den/0.0297-1)<=0.1: no+=1; sNO.append(k*(a+bb+cc))
        if abs((cc**2-bb**2)/den/0.0297-1)<=0.1: io+=1; sIO.append(k*(a+bb+cc))
    f=lambda L: f"{min(L):.4f}-{max(L):.4f} eV" if L else "none"
    print(f"c={c}: points={tot} NO={no} (Sigma {f(sNO)}, <=0.064: {sum(x<=0.064 for x in sNO)}) IO={io} (Sigma {f(sIO)})")
