import numpy as np, json, mpmath as mp
def L(x,y):
    e=mp.eta(mp.mpc(x,y)) if hasattr(mp,'eta') else None
    q=mp.exp(2j*mp.pi*mp.mpc(x,y)); eta=q**(mp.mpf(1)/24)*mp.qp(q)
    return float(-mp.pi*mp.log(y*abs(eta)**4))
best=(1e9,None)
for x in np.linspace(-0.5,0.5,101):
    for y in np.linspace(np.sqrt(max(1-x*x,0))+1e-9,6,120):
        v=L(x,y)
        if v<best[0]: best=(v,(x,y))
o=dict(min_L=best[0],at=best[1],L_i=L(0,1),L_rho=L(0.5,np.sqrt(3)/2),L_y6=L(0,6),positive_everywhere=best[0]>0)
print(json.dumps(o,indent=1)); json.dump(o,open('field_tests/results/a3_d8sign.json','w'),indent=1)
