import math, json, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
Om,Or,A=0.31,9e-5,16*math.pi**2/6/(3*1.2020569031595942)
def run(beta,phii,VL):
    V=lambda p:VL*(1-A*math.exp(-beta*p)); dV=lambda p:VL*A*beta*math.exp(-beta*p)
    def f(N,s):
        p,q=s; a=math.exp(N); rm=3*Om*a**-3; rr=3*Or*a**-4
        H2=(rm+rr+V(p))/(3-q*q/2)
        # dH/dN / H = -(rm + 4/3 rr + H2 q^2)/(2 H2)
        eps=(rm+4*rr/3+H2*q*q)/(2*H2)
        return [q, -(3-eps)*q - dV(p)/H2]
    sol=solve_ivp(f,(math.log(1e-3),0),[phii,0.0],rtol=1e-9,atol=1e-12,dense_output=True)
    p,q=sol.y[:,-1]; a=1.0; rm=3*Om; rr=3*Or; H2=(rm+rr+V(p))/(3-q*q/2)
    return sol,H2,V
def shoot(beta,phii):
    g=lambda VL:run(beta,phii,VL)[1]-1.0
    return brentq(g,0.5,10.0,xtol=1e-12)
data={'Pantheon+':(-0.838,0.055,-0.62,0.22,0.19),'Union3':(-0.667,0.088,-1.09,0.31,0.27)}
rho=-0.9
def dchi2(w0,wa,d):
    m0,s0,ma,su,sd=d; s1=su if wa>ma else sd
    x=(w0-m0)/s0; y=(wa-ma)/s1; return (x*x-2*rho*x*y+y*y)/(1-rho*rho)
out={}
for beta in (2*math.sqrt(2),2.0,math.sqrt(2)):
    rows=[]
    for amp in np.geomspace(0.01,3,40):
        phii=-math.log(amp/A)/beta
        VL=shoot(beta,phii); sol,H2,V=run(beta,phii,VL)
        aa=np.linspace(1/3,1,60); w=[]
        for a in aa:
            p,q=sol.sol(math.log(a)); rm=3*Om*a**-3; rr=3*Or*a**-4; H2a=(rm+rr+V(p))/(3-q*q/2)
            K=0.5*H2a*q*q; w.append((K-V(p))/(K+V(p)))
        X=np.vstack([np.ones_like(aa),1-aa]).T; w0,wa=np.linalg.lstsq(X,np.array(w),rcond=None)[0]
        row=dict(amp=float(amp),phii=float(phii),VL=float(VL),w0=float(w0),wa=float(wa),w_today=float(w[-1]))
        for k,d in data.items(): row['dchi2_'+k]=float(dchi2(w0,wa,d))
        rows.append(row)
    best={k:min(rows,key=lambda r:r['dchi2_'+k]) for k in data}
    out[f'beta={beta:.4f}']=dict(best={k:{kk:v[kk] for kk in ('amp','w0','wa','dchi2_'+k)} for k,v in best.items()},
        consistent={k:bool(best[k]['dchi2_'+k]<=6.18) for k in data},rows=rows[::4])
print(json.dumps({k:{'best':v['best'],'consistent':v['consistent']} for k,v in out.items()},indent=1))
os.makedirs('field_tests/results/GENESIS_DE',exist_ok=True); json.dump(out,open('field_tests/results/GENESIS_DE/out.json','w'),indent=1)
