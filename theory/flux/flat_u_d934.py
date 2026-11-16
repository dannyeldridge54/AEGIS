import sympy as sp, itertools
U1,U2,U3,S=sp.symbols('U1 U2 U3 S')
Pi=[1,U1,U2,U3,U2*U3,U1*U3,U1*U2,U1*U2*U3]
f=sp.symbols('f0:8'); h=sp.symbols('h0:8')
W=sum((f[k]-S*h[k])*Pi[k] for k in range(8))
conds=[W,sp.diff(W,U1),sp.diff(W,U2),sp.diff(W,S),sp.diff(W,U3),
       sp.diff(W,U1,U3),sp.diff(W,U2,U3),sp.diff(W,S,U3)]
pairs=[(0,7),(1,4),(2,5),(3,6)]
def Nflux(fv,hv): return sum(fv[a]*hv[b]-fv[b]*hv[a] for a,b in pairs)
I=sp.I; R=sp.Rational
grid=[I,2*I,3*I,R(1,2)+I,1+I,R(1,2)+I/2,R(1,3)+I,2+I]
vars_=list(f)+list(h)
H3=[[sp.diff(W,a,b) for b in (U1,U2,S)] for a in (U1,U2,S)]
nz=0; acc=[]
for p1,p2,ps in itertools.product(grid,repeat=3):
    sub={U1:p1,U2:p2,S:ps,U3:0}
    rows=[]
    for c in conds:
        e=sp.expand(c.subs(sub))
        for part in (sp.re(e),sp.im(e)):
            rows.append([sp.nsimplify(sp.expand(part)).coeff(v) for v in vars_])
    M=sp.Matrix(rows)
    ns=M.nullspace()
    if not ns: continue
    nz+=1
    ns=[v*sp.ilcm(*[sp.fraction(x)[1] for x in v]) for v in ns]
    for co in itertools.product(range(-2,3),repeat=len(ns)):
        if not any(co): continue
        v=sum((c*n for c,n in zip(co,ns)),sp.zeros(16,1))
        fv,hv=list(v[:8]),list(v[8:])
        N=Nflux(fv,hv)
        if N==0 or abs(N)>32: continue
        Hm=sp.Matrix(H3).subs(dict(zip(vars_,fv+hv))).subs({U1:p1,U2:p2,S:ps,U3:I})
        if sp.simplify(Hm.det())==0: continue
        acc.append((abs(N),N,(p1,p2,ps),fv,hv))
acc.sort(key=lambda x:x[0])
with open('field_tests/results/flat_u_d934.txt','w') as o:
    o.write(f'grid points {len(grid)**3}; with nonzero nullspace {nz}; accepted {len(acc)}\n')
    for a in acc[:10]: o.write(str(a)+'\n')
print(open('field_tests/results/flat_u_d934.txt').read())
