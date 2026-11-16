"""D883 (locked PREREG_D883). rho lepton sector: oscillation fit and E4-lift epsilon. AI-assisted."""
import numpy as np
rng=np.random.default_rng(883); N=20000; mb=np.sqrt(2.51e-3)
def cg(): return (rng.normal(size=3)+1j*rng.normal(size=3))/np.sqrt(2)
def masses(yY,y1,y2,M,eps):
    m=np.outer(yY,yY)/M[0]+np.outer(y1,y1)/M[1]+eps**2*np.outer(y2,y2)/M[2]
    return np.sort(np.linalg.svd(m,compute_uv=False))
npass=0; epsl=[]
for _ in range(N):
    yY,y1,y2=cg(),cg(),cg(); M=10**rng.uniform(11,13,3)
    s=masses(yY,y1,y2,M,0.0); ma,mbb=s[1],s[2]; r=(ma/mbb)**2
    if not (0.0263<=r<=0.0331): continue
    npass+=1; scale=mb/mbb
    def m1(le): return masses(yY,y1,y2,M,10**le)[0]*scale
    target=np.sqrt(4e-9*7e-8)  # geometric middle of [4e-9,7e-8]
    lo,hi=-8.0,0.0
    if not (m1(lo)<target<m1(hi)): continue
    for _ in range(50):
        mid=(lo+hi)/2
        if m1(mid)<target: lo=mid
        else: hi=mid
    epsl.append(10**((lo+hi)/2))
epsl=np.array(epsl)
print(f"draws={N} pass(NO, both splittings 3sigma)={npass} ({100*npass/N:.2f}%)")
if len(epsl): print(f"epsilon for m1 = {np.sqrt(4e-9*7e-8):.1e} eV: median {np.median(epsl):.2e}, 5-95% [{np.percentile(epsl,5):.2e}, {np.percentile(epsl,95):.2e}], n={len(epsl)}")
