"""LHC1 (locked): s*sigma = Phi(tau0) scaling; predict 13.6 from 13 TeV; one-parameter evolution correction; 14 TeV two routes."""
import sys, numpy as np, math; sys.path.insert(0,'.')
from tools.lhc import xsec as X
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar
M=X.M
out=[]
for p in X.D['processes']:
    s13=np.array(X.D['sqrt_s']['13'][p]); s136=np.array(X.D['sqrt_s']['13.6'][p])
    t13=4*M**2/13000**2; Phi=CubicSpline(np.log(t13), np.log(13.0**2*s13))
    def pred(m, rs, k=0.0): t=4*m**2/(rs*1000)**2; return math.exp(Phi(math.log(t)))/rs**2*(rs/13.0)**k
    ok=[(m,pred(m,13.6)/v-1) for m,v in zip(M,s136) if m>=200 and 4*m**2/13600**2>=t13.min()]
    r=[e for _,e in ok]; print(f"P1 {p}: pure scaling 13.6 vs table: max |dev| {max(abs(x) for x in r):.3%}, range {min(r):+.3%}..{max(r):+.3%}")
    f=lambda k: sum((pred(m,13.6,k)/v-1)**2 for m,v in zip(M,s136) if m>=200)
    k=minimize_scalar(f,bounds=(-10,10),method='bounded').x
    r2=[pred(m,13.6,k)/v-1 for m,v in zip(M,s136) if m>=200]; print(f"P2 {p}: kappa={k:+.3f}  max |dev| {max(abs(x) for x in r2):.3%}")
    rows=[]
    for m in (500,1000,1100,1500,1800):
        a=pred(m,14.0,k); b=X.sigma(m,p,14.0); rows.append((m,a,b,a/b-1))
    print(f"P3 {p} 14 TeV scaling vs log-linear: "+'  '.join(f"m={m}: {a:.4g}/{b:.4g} ({d:+.2%})" for m,a,b,d in rows))
