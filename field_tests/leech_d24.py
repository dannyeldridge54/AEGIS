"""D1289 (locked PREREG_D1289): Leech lattice from the extended Golay code; shells <= 4; energy vs E8^3."""
import numpy as np, itertools, math, time
from fpylll import IntegerMatrix, LLL
# extended Golay code via quadratic residues mod 23
Q={(x*x)%23 for x in range(1,23)}
gen=np.zeros(23,int); gen[0]=1
for q in Q: gen[q]=1          # idempotent-style generator: 1 + sum of residues
rows=[np.roll(gen,k) for k in range(23)]
M=np.array(rows)%2
# row-reduce over GF(2) to a basis
def gf2_rank_basis(A):
    A=A.copy()%2; r=0; piv=[]
    for c in range(A.shape[1]):
        p=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if p is None: continue
        A[[r,p]]=A[[p,r]]
        for i in range(A.shape[0]):
            if i!=r and A[i,c]: A[i]^=A[r]
        r+=1
    return A[:r]
Bc=gf2_rank_basis(M)
if len(Bc)!=12:  # try complement generator (non-residues) if dimension differs
    gen=np.zeros(23,int); gen[0]=1
    for q in set(range(1,23))-Q: gen[q]=1
    Bc=gf2_rank_basis(np.array([np.roll(gen,k) for k in range(23)])%2)
Bc=np.hstack([Bc,(Bc.sum(1)%2)[:,None]])   # parity extension -> length 24
# all codewords
W=np.array([(np.array(c)@Bc)%2 for c in itertools.product([0,1],repeat=len(Bc))])
wt=W.sum(1); print("Golay: dim",len(Bc),"codewords",len(W),"weights",{int(k):int(v) for k,v in zip(*np.unique(wt,return_counts=True))})
G=[2*w for w in Bc]
for i in range(24):
    for j in range(i+1,24):
        v=np.zeros(24,int); v[i]=4; v[j]=4; G.append(v); v=v.copy(); v[j]=-4; G.append(v)
v=np.ones(24,int); v[0]=-3; G.append(v)
A=IntegerMatrix.from_matrix([list(map(int,g)) for g in G])
LLL.reduction(A)
B=np.array([[A[i,j] for j in range(24)] for i in range(A.nrows)])
B=B[np.any(B!=0,axis=1)]
print("basis rows",len(B))
Gram=(B@B.T)/8.0
print("det",round(np.linalg.det(Gram),6),"diag even:",np.allclose(np.diag(Gram)%2,0),"integral:",np.allclose(Gram,np.round(Gram)))
import sys; src=open('field_tests/e6e7_flip.py').read().split('al=np.array')[0]; ns={}; exec(src,ns); norms=ns['norms']; cartan=ns['cartan']
t=time.time(); q=norms(Gram,4.0001); vals,cnt=np.unique(np.round(q,6),return_counts=True)
print("Leech shells <=4:",dict(zip(vals.tolist(),cnt.tolist())),f"({time.time()-t:.0f}s)")
# energy: enumerated shells + literature shell counts beyond (stated as bound/estimate)
al=np.array([1.0,1.25,1.5,2.0,3.0])
lee=sum(c*np.exp(-np.pi*al*n) for n,c in zip(vals,cnt) if n>0)
tail_lee=16773120*np.exp(-6*np.pi*al)+398034000*np.exp(-8*np.pi*al)     # [literature] Leech shells 6, 8 (Conway-Sloane)
# E8^3: theta = E8-theta cubed; E8 shells 240, 2160, 6720 (norms 2,4,6) -> compute E8^3 shells to norm 6 exactly by convolution of E8 counts
e8={0:1,2:240,4:2160,6:6720,8:17520}
def conv(a,b):
    c={}
    for x,u in a.items():
        for y,w in b.items():
            if x+y<=8: c[x+y]=c.get(x+y,0)+u*w
    return c
e83=conv(conv(e8,e8),e8)
print("E8^3 shells (from E8 shells, convolution):",{k:e83[k] for k in sorted(e83)})
ee=sum(c*np.exp(-np.pi*al*n) for n,c in e83.items() if n>0)
print("alpha:", al)
print("Leech theta-1 (enum<=4)          :", ' '.join(f'{x:.6e}' for x in lee))
print("Leech + lit. shells 6,8          :", ' '.join(f'{x:.6e}' for x in lee+tail_lee))
print("E8^3 theta-1 (shells<=8)         :", ' '.join(f'{x:.6e}' for x in ee))
print("Leech lower than E8^3 at every alpha>=1 (using LOWER bound for E8^3, UPPER-ish for Leech):", bool(np.all(lee+tail_lee*1.01+1e-9 < ee)))
