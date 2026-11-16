"""D781 (locked PREREG_D781): D725 N* code with rho_th at T2 and a C loop. AI-assisted."""
import math
MP=2.435e18; gs=106.75
lo,hi=3.175e8,3.033e9
import mpmath as mp
mp.mp.dps=15
src=open('theory/modular/bhk_tilt_d689.py').read(); exec(src[src.index('def Eser'):src.index('print("1. checks")')])
rh=mp.mpc(0.5,mp.sqrt(3)/2); Er=Eser(rh); s2=mp.sqrt(2); C=None
Eh=lambda yy: Eser(mp.mpc(0.5,yy))-Er
V=lambda p: (lambda e: e/(e+1)*(1+CC[0]*e))(Eh(mp.e**(s2*p)))
CC=[None]
d=lambda p,k: mp.diff(V,p,k); eps=lambda p:(d(p,1)/V(p))**2/2
def at(N):
    ps=mp.findroot(lambda p: mp.quad(lambda w_:V(w_)/d(w_,1),[pe,p])-N, mp.log(15)/s2)
    e=eps(ps); hh=d(ps,2)/V(ps); return float(1-6*e+2*hh), float(16*e), float(V(ps)/V(pe))
As=2.1e-9; lnk=math.log(0.05/(67.4/299792.458))
for Cv in ('1.0e-6','1.15e-6','1.3e-6'):
  CC[0]=mp.mpf(Cv); pe=mp.findroot(lambda p:eps(p)-1,mp.log(1.5)/s2)
  for TR in (3.175e8,3e6,3e4,3e2):
    N=49.0
    for it in range(30):
        ns,r,ratio=at(N); Vs=1.5*math.pi**2*As*r*MP**4; rho_end=1.5*Vs/ratio; rho_th=math.pi**2/30*gs*TR**4
        Nn=67-lnk+0.25*math.log(Vs**2/(MP**4*rho_end))+(1/12)*math.log(min(rho_th,rho_end)/rho_end)-(1/12)*math.log(gs)
        if abs(Nn-N)<0.01: N=Nn; break
        N=Nn
    inside=0.970<=ns<=0.975 and 4.55e-4<=r<=5.12e-4
    print(f"C={Cv} T2={TR:.3e}: N*={N:.2f}, n_s={ns:.4f}, r={r:.3e} {'INSIDE' if inside else 'outside'}", flush=True)
