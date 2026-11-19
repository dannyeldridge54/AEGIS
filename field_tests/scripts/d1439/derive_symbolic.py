import sympy as sp
w,s,B,e,C=sp.symbols('w s B e C')
V=(1-w)*(1+C*(1/w-1))
D=lambda f: sp.together(-2*sp.sqrt(2)*w*(1-B*w)*sp.diff(f,w))
V1=D(V);V2=D(V1);V3=D(V2)
eps=V1**2/V**2/2;eta=V2/V;xi=V1*V3/V**2
ns1=6*eps-2*eta; r=16*eps; al=16*eps*eta-24*eps**2-2*xi
def s_(f,n):
    f=f.subs(C,s*w**2)
    g=sp.series(f.subs(w,e*w),e,0,n).removeO().subs(e,1)
    return sp.expand(sp.series(sp.expand(g),B,0,2).removeO())
for name,f,n in (('1-ns',ns1,3),('r',r,4),('al',al,4)):
    print(name, sp.factor(s_(f,n)))
