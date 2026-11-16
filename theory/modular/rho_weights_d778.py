"""D778 (locked PREREG_D778). AI-assisted."""
import numpy as np, itertools, math, cmath
Y=np.array([1,1j])/math.sqrt(2)
def A(v): return np.array([[v[1],v[0]],[v[0],-v[1]]])
Y4=np.array([2*Y[0]*Y[1],Y[0]**2-Y[1]**2]); Y4=Y4/np.linalg.norm(Y4)
dbl={2:Y,4:Y4,8:Y}; sgl={0,6}
sv=lambda M: np.sort(np.linalg.svd(M,compute_uv=False))
vals=[m*cmath.exp(1j*p) for m in (0.2,1,5) for p in (0,2*math.pi/3,4*math.pi/3)]
for c in (0.6,1,3):
    MR=np.zeros((3,3),complex); MR[:2,:2]=A(Y); MR[:2,2]=c*Y; MR[2,:2]=c*Y; MRi=np.linalg.inv(MR)
    for wd,w3 in itertools.product((0,2,4,6,8),repeat=2):
        freeb = wd in dbl; freeg = w3 in dbl; freed = w3 in sgl
        grids=[vals if freeb else [0],vals if freeg else [0],vals if freed else [0]]
        no=io=0; sNO=[]; tot=0
        for b,g,dd in itertools.product(*grids):
            MD=np.zeros((3,3),complex)
            MD[:2,:2]=A(dbl[wd]) if wd in dbl else np.eye(2)
            if freeb: MD[:2,2]=b*dbl[wd]
            if freeg: MD[2,:2]=g*dbl[w3]
            if freed: MD[2,2]=dd
            if abs(np.linalg.det(MD))<1e-12: continue
            a,bb,cc=sv(-MD@MRi@MD.T); tot+=1; den=cc**2-a**2
            if den<=1e-14: continue
            k=math.sqrt(2.5e-3/den)
            if abs((bb**2-a**2)/den/0.0297-1)<=0.1: no+=1; sNO.append(k*(a+bb+cc))
            if abs((cc**2-bb**2)/den/0.0297-1)<=0.1: io+=1
        if no or io or (wd,w3)==(2,2):
            print(f"c={c} (w_d,w_3)=({wd},{w3}): nonsingular={tot} NO={no} IO={io} minSigma_NO={min(sNO) if sNO else float('nan'):.4f} n(Sigma<=0.064)={sum(x<=0.064 for x in sNO)}",flush=True)
