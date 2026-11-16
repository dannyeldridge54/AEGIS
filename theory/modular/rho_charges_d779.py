"""D779 (locked PREREG_D779). AI-assisted."""
import numpy as np, math
rng=np.random.default_rng(779)
Y=np.array([1,1j])/math.sqrt(2); n=np.array([1,-1j])/math.sqrt(2)
A=np.array([[Y[1],Y[0]],[Y[0],-Y[1]]]); c=1.0
MR=np.zeros((3,3),complex); MR[:2,:2]=A; MR[:2,2]=c*Y; MR[2,:2]=c*Y
# eigenbasis of the doublet: columns (n, Y) -- unitary, orthonormal
B=np.zeros((3,3),complex); B[:2,0]=n; B[:2,1]=Y  # DEVIATIONS D1; B[2,2]=1   # basis vectors; transform M' = B^T M B (Majorana)
Bu=B/np.linalg.norm(B,axis=0)
Mp=Bu.T@MR@Bu
print("M_R in eigenbasis (rounded):\n",np.round(Mp,6))
print("SVs:",np.sort(np.linalg.svd(Mp,compute_uv=False)))
# identify Majorana-only state (diagonal non-zero, no off-diag) and Dirac pair
nz=[(i,j) for i in range(3) for j in range(3) if abs(Mp[i,j])>1e-9]; print("non-zero entries:",nz)
q0=[i for i in range(3) if abs(Mp[i,i])>1e-9 and all(abs(Mp[i,j])<1e-9 for j in range(3) if j!=i)]
print("q=0 (pure Majorana) heavy states:",q0)
def rank_mnu(extra):
    N=3+extra; M=np.zeros((N,N),complex); M[:3,:3]=Mp
    for k in range(extra): M[3+k,3+k]=rng.uniform(0.5,2)*np.exp(2j*np.pi*rng.uniform())
    allowed=q0+list(range(3,N))
    ranks=[]
    for _ in range(1000):
        MD=np.zeros((3,N),complex)
        for j in allowed: MD[:,j]=rng.normal(size=3)+1j*rng.normal(size=3)
        mn=-MD@np.linalg.inv(M)@MD.T; s=np.linalg.svd(mn,compute_uv=False); ranks.append(int(np.sum(s>1e-9*s[0])))
    return max(set(ranks),key=ranks.count)
for extra in (0,1,2):
    print(f"extra q=0 singlet N's: {extra} -> generic rank(m_nu) = {rank_mnu(extra)}")
