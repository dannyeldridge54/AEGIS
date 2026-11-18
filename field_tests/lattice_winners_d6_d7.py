"""D1286 (locked: PREREG_D1286): winners in d=6,7 among Z, D, D*, A, A*, E, E* at unit covolume, Gaussian energy."""
import numpy as np, math, sys
sys.path.insert(0, 'field_tests'); from e6e7_flip import norms, cartan
def Dn(n):
    C=2*np.eye(n)
    for i in range(n-2): C[i,i+1]=C[i+1,i]=-1
    C[n-3,n-1]=C[n-1,n-3]=-1   # fork at node n-2 (D_n Dynkin)
    return C
def An(n):
    C=2*np.eye(n)
    for i in range(n-1): C[i,i+1]=C[i+1,i]=-1
    return C
def theta(G,al,Q):
    n=len(G); G=G/np.linalg.det(G)**(1/n); q=norms(G,Q)
    return np.exp(-np.pi*np.outer(al,q)).sum(1)-1
al=np.array([1.0,1.25,1.5,2.0,3.0])
for n in (6,7):
    fam={'Z':np.eye(n),'D':Dn(n),'A':An(n),'E':cartan(n)}
    L={}
    for k,G in fam.items():
        L[k]=G
        if k!='Z': L[k+'*']=np.linalg.inv(G)
    T={}; conv=0
    for k,G in L.items():
        t1=theta(G,al,10.0); t2=theta(G,al,12.0); T[k]=t2; conv=max(conv,np.max(abs(t2-t1)[1:]))
    print(f"d={n}  (max |Q10-Q12| at alpha>=1.25: {conv:.1e})")
    for k in T: print(f"  {k:3s}", ' '.join(f'{x:.9f}' for x in T[k]))
    for j,a in enumerate(al):
        w=min(T,key=lambda k:T[k][j]); print(f"  alpha={a}: winner {w}  ({T[w][j]:.9f})")
    # alpha<1 via Poisson: theta_L(1/a)-1 = a^{n/2} (theta_{L*}(a)) - 1  -> winner at 1/a is argmin of a^{n/2}(1+T_{L*}(a))
    dual=lambda k: 'Z' if k=='Z' else (k[:-1] if k.endswith('*') else k+'*')
    for j,a in enumerate(al[1:],1):
        vals={k:a**(n/2)*(1+T[dual(k)][j])-1 for k in T}; w=min(vals,key=vals.get); print(f"  alpha={1/a:.3f}: winner {w}  ({vals[w]:.9f})")
    for k in ('D','A','E'):
        print(f"  tie at alpha=1 {k}/{k}*: {abs(T[k][0]-T[k+'*'][0]):.1e}")
