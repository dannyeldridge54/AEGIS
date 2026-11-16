import sympy as sp, numpy as np, itertools
from scipy.optimize import minimize
U1,U2,U3,S=sp.symbols('U1 U2 U3 S')
Pi=[1,U1,U2,U3,U2*U3,U1*U3,U1*U2,U1*U2*U3]
f=sp.symbols('f0:8'); h=sp.symbols('h0:8'); vars_=list(f)+list(h)
W=sum((f[k]-S*h[k])*Pi[k] for k in range(8))
conds=[W,sp.diff(W,U1),sp.diff(W,U2),sp.diff(W,S),sp.diff(W,U3),sp.diff(W,U1,U3),sp.diff(W,U2,U3),sp.diff(W,S,U3)]
C=[[sp.diff(c,v) for v in vars_] for c in conds]
Cf=sp.lambdify((U1,U2,S,U3),C,'numpy')
def sv(u1,u2,s):
    M=np.array(Cf(u1,u2,s,0j),dtype=complex); Mr=np.vstack([M.real,M.imag])
    return np.linalg.svd(Mr,compute_uv=False)
r3=np.sqrt(3); rho=complex(-0.5,r3/2)
gA=[rho,rho+1,1j*r3/2,1j*r3,complex(0.5,r3/2),1j,2j]
hist={};minA=(9,None)
for p in itertools.product(gA,repeat=3):
    s=sv(*p); k=int((s<1e-9).sum()); hist[k]=hist.get(k,0)+1
    r=s[-1]/s[0]
    if r<minA[0]: minA=(r,p)
def obj(x):
    x=np.array(x); re=np.clip(x[0::2],-0.5,0.5); im=np.clip(x[1::2],0.2,5)
    u=re+1j*im; s=sv(*u); return s[-1]/s[0]
rng=np.random.default_rng(935); best=(9,None)
for _ in range(200):
    x0=np.ravel([[rng.uniform(-.5,.5),rng.uniform(.2,5)] for _ in range(3)])
    res=minimize(obj,x0,method='Nelder-Mead',options={'maxiter':4000,'xatol':1e-10,'fatol':1e-14})
    if res.fun<best[0]: best=(res.fun,res.x)
x=best[1]; loc=np.clip(x[0::2],-.5,.5)+1j*np.clip(x[1::2],.2,5)
m=min(minA[0],best[0])
verdict='ZEROS EXIST' if m<1e-10 else ('NO ZEROS FOUND' if m>1e-4 else 'INCONCLUSIVE')
out=f"Part A: nullity histogram {hist}; min r {minA[0]:.3e} at {minA[1]}\nPart B: min r {best[0]:.3e} at U1,U2,S = {loc}\nverdict: {verdict}\n"
open('field_tests/results/flat_u_det_d935.txt','w').write(out); print(out)
