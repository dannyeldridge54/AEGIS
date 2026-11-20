import json, sys
from multiprocessing import Pool
def one(bc):
    import numpy as np
    src=open('field_tests/scripts/realdata/coupled.py').read().split("c,x=ns['fit']('coupled'")[0]; g={}; exec(src,g)
    ns=g['ns']
    def obj(x):
        Om,h,ob,amp=x
        if not(0.2<Om<0.45 and 0.6<h<0.8 and 0.018<ob<0.026 and 0.005<amp<0.9): return 1e9
        return ns['chi2_all']('coupled',Om,h,ob,[amp,bc])
    from scipy.optimize import minimize
    best=None
    for s in ([0.311,0.671,0.02244,0.16],[0.31,0.675,0.0224,0.3]):
        r=minimize(obj,s,method='Nelder-Mead',options=dict(xatol=1e-5,fatol=1e-3,maxiter=800))
        if best is None or r.fun<best.fun: best=r
    return bc,float(best.fun)-1650.3800547143892,[float(v) for v in best.x]
if __name__=='__main__':
    bcs=[-1,-0.5,-0.25,-0.1,0,0.1,0.25,0.5,1]
    with Pool(min(len(bcs),int(sys.argv[1]) if len(sys.argv)>1 else 3)) as p: res=p.map(one,bcs)
    o={str(b):dict(d=d,x=x) for b,d,x in res}
    print(json.dumps(o,indent=1)); json.dump(o,open('/home/claude/aegis/field_tests/results/coupled_scan.json','w'),indent=1)
