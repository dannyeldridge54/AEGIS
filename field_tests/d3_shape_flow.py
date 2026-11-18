"""D1297 (locked): minimise the Gaussian energy over unit-covolume 3-tori from random starts at alpha=0.6 and 1.6."""
import sys, numpy as np, math; sys.path.insert(0,'tools/lattice'); import lattice_lab as LL
from scipy.optimize import minimize
rng=np.random.default_rng(1297)
def basis(p):
    B=np.array([[1,p[0],p[1]],[0,math.exp(p[2]),p[3]],[0,0,math.exp(p[4])]]); B=B/abs(np.linalg.det(B))**(1/3); return B
def E(p,a):
    B=basis(p); G=B.T@B
    # reduce for enumeration stability (LLL-lite: use lattice_lab norms with a modest radius)
    q=LL.norms(G, 6.0/a+3.0); q=q[q>1e-12]; return np.exp(-np.pi*a*q).sum()
def ident(p):
    B=basis(p); G=B.T@B; q=np.sort(LL.norms(G, 4.0)); q=q[q>1e-9]
    m=q[0]; n1=int(np.sum(q<m*(1+1e-3))); n2=int(np.sum((q>m*(1+1e-3))&(q<m*1.34**2)))
    return {12:'FCC',8:'BCC' if n2==6 else 'BCC?',6:'cube'}.get(n1,f'other({n1})'), n1, n2, m
for a in (1.6,0.6):
    res=[]
    for k in range(8):
        p0=np.concatenate([rng.uniform(-0.5,0.5,2),[rng.uniform(-0.6,0.6)],[rng.uniform(-0.5,0.5)],[rng.uniform(-0.6,0.6)]])
        r=minimize(E,p0,args=(a,),method='Nelder-Mead',options={'xatol':1e-7,'fatol':1e-12,'maxiter':4000,'maxfev':6000})
        name,n1,n2,m=ident(r.x); res.append(name)
        print(f"alpha={a} start {k}: E {E(p0,a):.6f} -> {r.fun:.8f}  end shape {name} (nearest {n1}, next {n2}, min norm {m:.5f})")
    print(f"alpha={a} SUMMARY: {dict((x,res.count(x)) for x in set(res))}")
# reference energies
for nm in ('FCC','BCC','Z3'):
    print(nm, 'E(1.6)=',LL.energy(nm,(1.6,))['energy'], 'E(0.6)=',LL.energy(nm,(0.6,))['energy'])
