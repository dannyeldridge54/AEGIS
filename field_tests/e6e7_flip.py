"""D1278 follow-up (prediction logged in D1278 BEFORE this test): E6, E7 flip vs their duals; Leech/E8 do not.
Theta energy theta(a)=sum_x exp(-pi a |x|^2), covolume 1. Exact enumeration of all vectors with |x|^2<=Q (Fincke-Pohst)."""
import numpy as np, math
def cartan(n):
    C=2*np.eye(n)
    for i,j in [(1,3),(3,4),(4,5),(5,6),(6,7),(7,8),(2,4)]:
        if i<=n and j<=n: C[i-1,j-1]=C[j-1,i-1]=-1
    return C
def norms(G,Q):
    n=len(G); R=np.linalg.cholesky(G).T  # G=R^T R, upper R
    out=[]; x=np.zeros(n)
    def rec(k,rem,ctr_shift):
        # coordinate k, remaining budget rem
        c=-sum(R[k,j]*x[j] for j in range(k+1,n))/R[k,k]
        w=math.sqrt(max(rem,0))/abs(R[k,k])
        for v in range(math.ceil(c-w-1e-12),math.floor(c+w+1e-12)+1):
            x[k]=v; t=R[k,k]*(v-c); r2=rem-t*t
            if r2< -1e-9: continue
            if k==0: out.append(Q-r2)
            else: rec(k-1,r2,0)
        x[k]=0
    rec(n-1,Q,0); return np.array(out)
def theta(G,al,Q):
    n=len(G); G=G/np.linalg.det(G)**(1/n); q=norms(G,Q)
    return np.exp(-np.pi*np.outer(al,q)).sum(1), len(q)
al=np.array([1.0,1.25,1.5,2.0,3.0])
for n in (6,7,8):
    C=cartan(n); res={}
    for nm,G in (("E%d"%n,C),("E%d*"%n,np.linalg.inv(C))):
        t1,N1=theta(G,al,10.0); t2,N2=theta(G,al,12.0)
        res[nm]=t2; print(f"{nm:5s} N(Q=10,12)={N1},{N2}  conv={np.max(abs(t2-t1)):.1e}  theta={np.round(t2,12)}")
    a,b=res.values(); d=a-b
    print(f"  E{n}-E{n}*: {d}")
    # below a=1 by Poisson: theta_L(1/a)=a^{n/2} theta_L*(a) -> sign flips
    print("  winner a>=1:",["L" if x<-1e-12 else ("L*" if x>1e-12 else "tie") for x in d],
          "| a<1 (Poisson): ",["L*" if x<-1e-12 else ("L" if x>1e-12 else "tie") for x in d[1:]])
