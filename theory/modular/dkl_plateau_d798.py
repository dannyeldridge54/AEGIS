import mpmath as mp, math
mp.mp.dps=30
def D(x,y):
    t=mp.mpc(x,y); q=mp.exp(2j*mp.pi*t)
    eta=mp.exp(1j*mp.pi*t/12)*mp.qp(q)
    return float(-mp.log(y*abs(eta)**4))
X0,Y0=0.5,math.sqrt(3)/2; Dr=D(X0,Y0)
best=(1e9,None)
for i in range(61):
    for k in range(61):
        x=-0.5+i/60; y=0.5+2.5*k/60
        if x*x+y*y<1: continue
        d=D(x,y)
        if d<best[0]: best=(d,(x,y))
print(f"(a) grid min Delta={best[0]:.6f} at {best[1]}; Delta(rho)={Dr:.6f}; Delta(i)={D(0,1):.6f}")
def V(x,y,p): d=D(x,y)-Dr; d=max(d,0.0); return d**p/(d**p+1)
h=1e-4
for p in (1,2):
    v0=V(X0,Y0,p); Vxx=(V(X0+h,Y0,p)-2*v0+V(X0-h,Y0,p))/h**2; Vyy=(V(X0,Y0+h,p)-2*v0+V(X0,Y0-h,p))/h**2
    print(f"(b) p={p}: Vxx={Vxx:.5e} Vyy={Vyy:.5e} R={Vxx/Vyy if Vyy else float('nan'):.6f}")
print(f"(c) dV/dx on x=1/2 at y=5: {(V(0.5+1e-5,5,1)-V(0.5-1e-5,5,1))/2e-5:.2e}")
s=math.sqrt(2/3)
for p in (1,2):
    f=lambda ph: V(0.5,math.exp(s*ph),p)
    def dd(ph,hh=1e-4): return (f(ph+hh)-f(ph-hh))/(2*hh), (f(ph+hh)-2*f(ph)+f(ph-hh))/hh**2
    def eps(ph): d1,_=dd(ph); return 0.5*(d1/f(ph))**2
    lo,hi=math.log(Y0)/s+1e-3,10.0
    for _ in range(60):
        m=(lo+hi)/2
        if eps(m)>1: lo=m
        else: hi=m
    phe=hi; ph=phe; N=0.0; dph=1e-3; out={}
    while N<56 and ph<60:
        d1,_=dd(ph); N+=f(ph)/d1*dph; ph+=dph
        for Nt in (50,55):
            if Nt not in out and N>=Nt:
                d1,d2=dd(ph); e=0.5*(d1/f(ph))**2; et=d2/f(ph); out[Nt]=(1-6*e+2*et,16*e,math.exp(s*ph))
    for Nt,(ns,r,y) in out.items(): print(f"(c) p={p} N*={Nt}: n_s={ns:.4f} r={r:.3e} y*={y:.1f}  [12/N^2={12/Nt**2:.2e}, 3/N^2={3/Nt**2:.2e}]")
