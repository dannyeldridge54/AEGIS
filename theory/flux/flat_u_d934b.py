import sympy as sp, itertools, numpy as np
U1,U2,U3,S=sp.symbols('U1 U2 U3 S')
Pi=[1,U1,U2,U3,U2*U3,U1*U3,U1*U2,U1*U2*U3]
f=sp.symbols('f0:8'); h=sp.symbols('h0:8'); vars_=list(f)+list(h)
W=sum((f[k]-S*h[k])*Pi[k] for k in range(8))
conds=[W,sp.diff(W,U1),sp.diff(W,U2),sp.diff(W,S),sp.diff(W,U3),sp.diff(W,U1,U3),sp.diff(W,U2,U3),sp.diff(W,S,U3)]
# coefficient matrix as function of (U1,U2,S): complex 8x16, linear in fluxes
C=[[sp.diff(c,v) for v in vars_] for c in conds]
Cf=sp.lambdify((U1,U2,S,U3),C,'numpy')
pairs=[(0,7),(1,4),(2,5),(3,6)]
def Nflux(fv,hv): return sum(fv[a]*hv[b]-fv[b]*hv[a] for a,b in pairs)
I=sp.I;R=sp.Rational
grid=[I,2*I,3*I,R(1,2)+I,1+I,R(1,2)+I/2,R(1,3)+I,2+I]
H3=[[sp.diff(W,a,b) for b in (U1,U2,S)] for a in (U1,U2,S)]
cand=[];nullity={}
for p in itertools.product(grid,repeat=3):
    M=np.array(Cf(*[complex(x) for x in p],0j),dtype=complex)
    Mr=np.vstack([M.real,M.imag])
    sv=np.linalg.svd(Mr,compute_uv=False)
    k=int((sv<1e-9).sum()); nullity[k]=nullity.get(k,0)+1
    if k: cand.append(p)
acc=[]
for p1,p2,ps in cand:
    Ce=sp.Matrix(C).subs({U1:p1,U2:p2,S:ps,U3:0})
    M=sp.Matrix.vstack(Ce.applyfunc(sp.re),Ce.applyfunc(sp.im)).applyfunc(sp.nsimplify)
    ns=M.nullspace()
    ns=[v*sp.ilcm(*[sp.fraction(x)[1] for x in v]) for v in ns]
    for co in itertools.product(range(-2,3),repeat=len(ns)):
        if not any(co): continue
        v=sum((c*n for c,n in zip(co,ns)),sp.zeros(16,1))
        fv,hv=list(v[:8]),list(v[8:]); N=Nflux(fv,hv)
        if N==0 or abs(N)>32: continue
        Hm=sp.Matrix(H3).subs(dict(zip(vars_,fv+hv))).subs({U1:p1,U2:p2,S:ps,U3:I})
        if sp.simplify(Hm.det())==0: continue
        acc.append((abs(N),N,(p1,p2,ps),fv,hv))
acc.sort(key=lambda x:x[0])
with open('field_tests/results/flat_u_d934.txt','w') as o:
    o.write(f'run 2 (DEVIATIONS D1). grid points {len(grid)**3}; nullity histogram {nullity}; candidates {len(cand)}; accepted {len(acc)}\n')
    for a in acc[:10]: o.write(str(a)+'\n')
print(open('field_tests/results/flat_u_d934.txt').read())
