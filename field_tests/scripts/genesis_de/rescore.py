import math, json, numpy as np
from scipy.optimize import minimize_scalar
src=open('field_tests/scripts/genesis_de/run.py').read().split("data={")[0]; exec(src)
data={'Pantheon+':((-0.838,0.055,-0.62,0.22,0.19),10.7),'Union3':((-0.667,0.088,-1.09,0.31,0.27),17.4),'DESY5':((-0.752,0.057,-0.86,0.23,0.20),21.0)}
def dchi2(w0,wa,d,rho):
    m0,s0,ma,su,sd=d; s1=su if wa>ma else sd
    x=(w0-m0)/s0; y=(wa-ma)/s1; return (x*x-2*rho*x*y+y*y)/(1-rho*rho)
cal={}
for k,(d,t) in data.items():
    r=minimize_scalar(lambda rho:(dchi2(-1,0,d,rho)-t)**2,bounds=(-0.99,0.99),method='bounded')
    cal[k]=dict(rho=float(r.x),dchi2_LCDM=float(dchi2(-1,0,d,r.x)),target=t)
print('calibration',json.dumps(cal))
out={'calibration':cal}
for beta in (2*math.sqrt(2),2.0,math.sqrt(2)):
    rows=[]
    for amp in np.geomspace(0.01,0.9,40):
        phii=-math.log(amp/A)/beta; VL=shoot(beta,phii)
        if VL is None: continue
        sol,H2,V=run(beta,phii,VL); aa=np.linspace(1/3,1,60); w=[]
        for a in aa:
            p,q=sol.sol(math.log(a)); H2a=(3*Om*a**-3+3*Or*a**-4+V(p))/(3-q*q/2); K=0.5*H2a*q*q; w.append((K-V(p))/(K+V(p)))
        X=np.vstack([np.ones_like(aa),1-aa]).T; w0,wa=np.linalg.lstsq(X,np.array(w),rcond=None)[0]
        rows.append(dict(amp=float(amp),w0=float(w0),wa=float(wa),**{'d_'+k:float(dchi2(w0,wa,d,cal[k]['rho'])) for k,(d,t) in data.items()}))
    best={k:min(rows,key=lambda r:r['d_'+k]) for k in data}
    out[f'beta={beta:.4f}']={k:dict(amp=b['amp'],w0=b['w0'],wa=b['wa'],dchi2=b['d_'+k],consistent=b['d_'+k]<=6.18) for k,b in best.items()}
print(json.dumps(out,indent=1))
json.dump(out,open('field_tests/results/GENESIS_DE/rescore.json','w'),indent=1)
