"""D665 (locked PREREG_D665_JANUS_EXT). AI-assisted."""
import math, numpy as np, sympy as sp, mpmath as mp
ns_i={}; ns_r={}
srcI=open('theory/modular/running_d632.py').read().splitlines()[:41]
gI={}; exec("\n".join(srcI),gI)
srcR=open('theory/modular/rho_running_d634.py').read().splitlines()
endR=[i for i,l in enumerate(srcR) if l.startswith('import numpy as np') and i>40][0]
gR={}; exec("\n".join(srcR[:endR]),gR)
X=[-0.15,-0.1,-0.05,0,0.05,0.1,0.15]
def measure(g,e,Ns):
    B=g['background'](e); lp=[]; r=None
    for x in X:
        P,Pt,ys=g['spectra'](B,Ns,math.exp(x)); lp.append(math.log(P))
        if x==0: r=Pt/P; y0=ys
    c=np.polyfit(X,lp,3)   # c[0] x^3 + c[1] x^2 + c[2] x + c[3]
    return dict(ns=1+c[2],al=2*c[1],be=6*c[0],r=r,y=y0)
data=[]
for e in (1.3e-4,1.6e-4):
    for Ns in (46.08,49.21):
        d=measure(gI,e,Ns); d.update(model='i',e=e,N=Ns); data.append(d)
        print(f"tau=i eps={e} N*={Ns}: y*={d['y']:.2f} n_s={d['ns']:.5f} r={d['r']:.3e} alpha={d['al']:.3e} beta={d['be']:.3e}",flush=True)
for Ns in (46.09,49.49):
    d=measure(gR,6e-5,Ns); d.update(model='rho',e=6e-5,N=Ns); data.append(d)
    print(f"rho eps=6e-5 N*={Ns}: y*={d['y']:.2f} n_s={d['ns']:.5f} r={d['r']:.3e} alpha={d['al']:.3e} beta={d['be']:.3e}",flush=True)
# ---- slow-roll machinery ----
mp.mp.dps=30; c0=mp.log(1728)/(2*mp.pi)
y,e=sp.symbols('y e',positive=True)
def srfuncs(V):
    D=lambda f: sp.sqrt(2)*y*sp.diff(f,y)   # d/dphi, phi = ln y/sqrt2
    V1=D(V);V2=D(V1);V3=D(V2);V4=D(V3)
    eps=(V1/V)**2/2; eta=V2/V; xi=V1*V3/V**2; vp=V1**2*V4/V**3
    ns=1-6*eps+2*eta; r=16*eps; al=16*eps*eta-24*eps**2-2*xi
    be=-192*eps**3+192*eps**2*eta-32*eps*eta**2-24*eps*xi+2*eta*xi+2*vp
    return [sp.lambdify((y,e),f,'mpmath') for f in (ns,r,al,be)]
I=y-sp.log(1728)/(2*sp.pi)
Vi=I**2/(I**2+1)+e*I/2
Lr=sp.pi*y/3-sp.log(2*y)-sp.Float(0.340372354)
Vr=I**2/(I**2+1)+e*Lr
Fi=srfuncs(Vi); Fr=srfuncs(Vr)
def invert(F,ns,r,y0,le0):
    s=mp.findroot(lambda yy,le:[F[0](yy,mp.e**le)-ns,F[1](yy,mp.e**le)-r],(y0,le0))
    return s[0],mp.e**s[1]
print("\n(A)/(B) method-B predictions vs exact:")
okA=True; okB=True
for d in data:
    F=Fi if d['model']=='i' else Fr
    yy,ee=invert(F,d['ns'],d['r'],d['y'],math.log(d['e']))
    al=float(F[2](yy,ee)); be=float(F[3](yy,ee))
    ea=100*(al/d['al']-1); eb=100*(be/d['be']-1)
    if d['model']=='rho' and abs(ea)>3: okA=False
    if abs(eb)>25: okB=False
    print(f"{d['model']} eps={d['e']} N*={d['N']}: inverted y*={float(yy):.2f} eps={float(ee):.2e} | alpha pred {al:.3e} ({ea:+.1f}%) | beta pred {be:.3e} vs exact {d['be']:.3e} ({eb:+.1f}%)")
# tau=i closed form (D640 A) on rho points
u,x,cc=sp.symbols('u x c')
nsA=1-8*u**2*((2-x)+cc*u*(5-x)); rA=64*u**4*(1+x)**2*(1+2*cc*u); aA=-32*u**4*(1+x)*((4+x)+cc*u*(23+2*x))
fA=sp.lambdify((u,x,cc),[nsA,rA,aA],'mpmath')
for d in data:
    if d['model']!='rho': continue
    g=mp.findroot(lambda uv,xv:[fA(uv,xv,c0)[0]-d['ns'],fA(uv,xv,c0)[1]-d['r']],(1/22,0.3))
    a=float(fA(g[0],g[1],c0)[2]); print(f"rho N*={d['N']}: tau=i closed form gives alpha {a:.3e} ({100*(a/d['al']-1):+.1f}%)")
# leading-order closed form for beta_s (c = 0)
U,Xs=sp.symbols('u x',positive=True)
Vlo=1-y**-2+e*y/2
Flo=None
D=lambda f: sp.sqrt(2)*y*sp.diff(f,y)
V1=D(Vlo);V2=D(V1);V3=D(V2);V4=D(V3); V=Vlo
eps=(V1/V)**2/2; eta=V2/V; xi=V1*V3/V**2; vp=V1**2*V4/V**3
be=-192*eps**3+192*eps**2*eta-32*eps*eta**2-24*eps*xi+2*eta*xi+2*vp
g=sp.simplify(be.subs(e,4*Xs/y**3).subs(y,1/U))
lead=sp.factor(sp.simplify(sp.series(g,U,0,7).removeO()))
lead=sp.factor(sum(t for t in sp.expand(lead).as_ordered_terms() if sp.degree(t,U)==6))
print("\nLeading-order closed form: beta_s =",lead)
print(f"VERDICT A (rho, method B within 3%): {'PASS' if okA else 'FAIL'};  VERDICT B (beta within 25%): {'PASS' if okB else 'FAIL'}")
