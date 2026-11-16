import mpmath as mp
mp.mp.dps=30
def Dl(y):
    t=mp.mpc(0.5,y); q=mp.exp(2j*mp.pi*t); eta=mp.exp(1j*mp.pi*t/12)*mp.qp(q)
    return -mp.log(y*abs(eta)**4)
Dr=Dl(mp.sqrt(3)/2)
s2=mp.sqrt(2)
def mk(eps):
    def V(ph):
        d=Dl(mp.exp(s2*ph))-Dr; return d**2/(d**2+1)+eps*d
    return V
def sr(V,ph,h=mp.mpf('1e-3')):
    v=V(ph); d1=mp.diff(V,ph,1); d2=mp.diff(V,ph,2); d3=mp.diff(V,ph,3)
    e=d1**2/v**2/2; et=d2/v; xi=d1*d3/v**2
    return e,et,xi,v
def janus(ns,r):
    rho=2*mp.sqrt(r)/(1-ns); x=(rho-1)/(1+rho/2); A=(1-ns)/(1-x/2)
    return -A**2/2*(1+x/4)*(1+x)
for eps in [0,1e-5,2e-5,4e-5,6e-5,8e-5,1e-4,1.5e-4]:
    V=mk(eps)
    phe=mp.findroot(lambda p: sr(V,p)[0]-1,(mp.log(1.2)/s2, mp.log(3.0)/s2),solver='bisect')
    ph=phe; N=mp.mpf(0); dph=mp.mpf('0.004'); res={}
    while N<55 and ph<6:
        d1=mp.diff(V,ph); N+=V(ph)/d1*dph; ph+=dph
        for Nt in (50,55):
            if Nt not in res and N>=Nt:
                e,et,xi,_=sr(V,ph); ns=1-6*e+2*et; r=16*e; al=16*e*et-24*e**2-2*xi
                res[Nt]=(ns,r,al,mp.exp(s2*ph))
    line=f"eps={eps:.1e}:"
    for Nt,(ns,r,al,y) in sorted(res.items()):
        line+=f" N{Nt}: ns={float(ns):.4f} r={float(r):.2e} as={float(al):.2e} y*={float(y):.1f} J/as={float(janus(ns,r)/al):.2f};"
    if eps>0:
        Vyy=mp.diff(lambda y:(lambda d:d**2/(d**2+1)+eps*d)(Dl(y)-Dr),mp.sqrt(3)/2,2)
        m2=2*(3/mp.mpf(4))*Vyy; H2=V(phe)/2; line+=f" m2/H2end={float(m2/H2):.2e}"
    print(line,flush=True)
