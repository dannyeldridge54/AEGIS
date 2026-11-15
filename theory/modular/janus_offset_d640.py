"""D640 (locked PREREG_D640_JANUS_OFFSET). AI-assisted."""
import re, math, sympy as sp, mpmath as mp
mp.mp.dps=40
c=math.log(1728)/(2*math.pi)
pts=[]
for l in open('field_tests/results/janus_analytic_d635.txt'):
    m=re.search(r'n_s=([\d.]+) r=([\d.e-]+) alpha_exact=([-\d.e]+)',l)
    if m: pts.append((l.split(' n_s')[0],float(m.group(1)),float(m.group(2)),float(m.group(3)),float(re.search(r'err=([-\d.]+)%',l).group(1))))
# ---- slow-roll in terms of I with field map dphi = dI/(sqrt2 (I+c)) ----
I,e,cc=sp.symbols('I e c',positive=True)
def sr(V,cv):
    D=lambda f: sp.sqrt(2)*(I+cv)*sp.diff(f,I)   # d/dphi
    V1=D(V); V2=D(V1); V3=D(V2)
    eps=(V1/V)**2/2; eta=V2/V; xi2=V1*V3/V**2
    return eps,eta,xi2
# Method B: full asymptotic V
VB=I**2/(I**2+1)+e*I/2
epsB,etaB,xiB=[sp.lambdify((I,e),f,'mpmath') for f in sr(VB,c)]
def obsB(Iv,ev):
    E,H,X=epsB(Iv,ev),etaB(Iv,ev),xiB(Iv,ev)
    return 1-6*E+2*H, 16*E, 16*E*H-24*E**2-2*X
# Method A: V = 1 - I^-2 + e I/2, expand leading in 1/I at fixed x and first order in c
x,u=sp.symbols('x u',positive=True)   # u = 1/I
VA=1-I**-2+e*I/2
epsA,etaA,xiA=sr(VA,cc)
def lead(f,order):
    g=sp.simplify(f.subs(e,4*x/I**3).subs(I,1/u))
    s=sp.series(g,u,0,order+2).removeO()
    s=sp.expand(sp.series(s,cc,0,2).removeO())
    return sp.simplify(s)
# keep terms up to u^2 (n_s, eta), u^4 (r, alpha)
EA=lead(epsA,4); HA=lead(etaA,2); XA=lead(xiA,4)
nsA=sp.expand(1-6*EA+2*HA); rA=sp.expand(16*EA); aA=sp.expand(16*EA*HA-24*EA**2-2*XA)
def trunc(f,n):
    f=sp.expand(f); return sum(t for t in f.as_ordered_terms() if sp.degree(t,u)<=n and sp.degree(t,cc)<=1)
nsA=trunc(nsA,3); rA=trunc(rA,5); aA=trunc(aA,5)
print("A closed form (u=1/I*, first order in c):",flush=True)
print("  1-n_s =",sp.factor(sp.simplify(1-nsA)),flush=True)
print("  r     =",sp.factor(sp.simplify(rA)),flush=True)
print("  alpha =",sp.factor(sp.simplify(aA)),flush=True)
fA=sp.lambdify((u,x,cc),[nsA,rA,aA],'mpmath')
out=[]
for name,ns,r,al,e635 in pts:
    # B: solve (I,e) from (ns,r); starting guess from leading order
    g=mp.findroot(lambda Iv,lev:[obsB(Iv,mp.e**lev)[0]-ns,obsB(Iv,mp.e**lev)[1]-r],(22,math.log(1.2e-4) if 'two' in name else math.log(1e-6)))
    aB=obsB(g[0],mp.e**g[1])[2]
    gA=mp.findroot(lambda uv,xv:[fA(uv,xv,c)[0]-ns,fA(uv,xv,c)[1]-r],(1/22,0.3 if 'two' in name else 0.01))
    aA_=fA(gA[0],gA[1],c)[2]
    eB=100*(float(aB)-al)/abs(al)*(-1) if False else 100*(float(aB)/al-1); eA=100*(float(aA_)/al-1)
    out.append((abs(eB),abs(eA)))
    print(f"{name}: alpha_exact={al:.3e} | D635 err={e635:+.1f}% | A: {float(aA_):.3e} err={eA:+.1f}% | B: {float(aB):.3e} err={eB:+.1f}% (I*={float(g[0]):.2f}, eps={float(mp.e**g[1]):.2e})",flush=True)
mB=max(o[0] for o in out); mA=max(o[1] for o in out)
print(f"max|err| A={mA:.1f}%  B={mB:.1f}%  VERDICT(B<=3%): {'PASS' if mB<=3 else 'FAIL'}")
