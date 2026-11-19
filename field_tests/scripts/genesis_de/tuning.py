import math, json, numpy as np
src=open('field_tests/scripts/genesis_de/run.py').read().split("data={")[0]; exec(src)
data={'Pantheon+':((-0.838,0.055,-0.62,0.22,0.19),-0.5549578869072045),'Union3':((-0.667,0.088,-1.09,0.31,0.27),-0.5382876371652675),'DESY5':((-0.752,0.057,-0.86,0.23,0.20),-0.5931860911995117)}
def dchi2(w0,wa,d,rho):
    m0,s0,ma,su,sd=d; s1=su if wa>ma else sd
    x=(w0-m0)/s0; y=(wa-ma)/s1; return (x*x-2*rho*x*y+y*y)/(1-rho*rho)
out={}
for beta in (2*math.sqrt(2),2.0,math.sqrt(2)):
    amps=np.geomspace(0.01,0.9,300); viable=[]; passall=[]; worst=[]
    for amp in amps:
        phii=-math.log(amp/A)/beta; VL=shoot(beta,phii)
        if VL is None: continue
        sol,H2,V=run(beta,phii,VL); aa=np.linspace(1/3,1,60); w=[]
        for a in aa:
            p,q=sol.sol(math.log(a)); H2a=(3*Om*a**-3+3*Or*a**-4+V(p))/(3-q*q/2); K=0.5*H2a*q*q; w.append((K-V(p))/(K+V(p)))
        X=np.vstack([np.ones_like(aa),1-aa]).T; w0,wa=np.linalg.lstsq(X,np.array(w),rcond=None)[0]
        m=max(dchi2(w0,wa,d,r) for d,r in data.values())
        viable.append(amp); worst.append((m,float(amp),float(w0),float(wa))); passall.append(m<=6.18)
    dl=math.log(amps[1]/amps[0]); nv=len(viable); npass=sum(passall)
    frac=npass/nv; width=npass*dl
    b=min(worst)
    out[f'beta={beta:.4f}']=dict(n_viable=nv,n_pass_all=npass,frac_viable_lnrange=frac,window_dln=width,viable_lnrange=nv*dl,
        best_minmax=dict(dchi2_max=b[0],amp=b[1],w0=b[2],wa=b[3]),
        reading='natural' if frac>=0.10 else ('mild tuning' if frac>=0.01 else 'tuned/fails'))
print(json.dumps(out,indent=1)); json.dump(out,open('field_tests/results/GENESIS_DE/tuning.json','w'),indent=1)
