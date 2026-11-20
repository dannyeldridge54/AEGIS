import numpy as np, json, math
src=open('field_tests/scripts/a3d6/run.py').read().split("# validation")[0]
exec(src)
def RNa(f,alpha,L=60.0,nx=81,ny=400):
    xs=np.linspace(-0.5,0.5,nx); tot=0.0; wx=np.full(nx,1.0); wx[0]=wx[-1]=0.5; dx=1.0/(nx-1)
    for i,x in enumerate(xs):
        y0=math.sqrt(1-x*x); ys=np.concatenate([np.linspace(y0,4,ny),np.geomspace(4,L,ny)[1:]])
        tot+=wx[i]*dx*np.trapezoid(np.array([f(x,y)/y**2 for y in ys]),ys)
    return tot-L**(alpha-1)/(alpha-1)
o={}
for d in (5,6):
    a=d/2; I={str(R):RNa(lambda x,y,R=R,d=d:G11(R,x,y)**d,a) for R in (1,1.25,1.5,2,3)}
    xs=np.linspace(-0.5,0.5,20001); S=-np.mean((1-xs**2)**((a-1)/2))/(a-1)
    o[f'd={d}']=dict(I=I,min=min(I.values()),shift_convergent=float(-S))
print(json.dumps(o,indent=1)); json.dump(o,open('field_tests/results/a3_d54.json','w'),indent=1)
