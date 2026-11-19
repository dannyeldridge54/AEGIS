import sys, math, json, os; sys.path.insert(0,'.')
import numpy as np
from tools.serapis_calc.shapes import E
Ef=lambda x,y:float(E(complex(x,y),1.5).real)
H=1e-5
def V0(x,y):
    L=lambda a,b:math.log(Ef(a,b))
    dx=(L(x+H,y)-L(x-H,y))/(2*H); dy=(L(x,y+H)-L(x,y-H))/(2*H)
    return (4/9)*y*y*(dx*dx+dy*dy)
h=1e-4
curv=lambda y:(V0(0.5+h,y)-2*V0(0.5,y)+V0(0.5-h,y))/h**2
ys=np.exp(np.linspace(math.log(0.87),math.log(6),60))
cs=[curv(y) for y in ys]
out={'y':[float(y) for y in ys],'curv':[float(c) for c in cs]}
roots=[]
for i in range(len(ys)-1):
    if cs[i]*cs[i+1]<0 and abs(cs[i])>1e-10 and abs(cs[i+1])>1e-10:
        a,b=ys[i],ys[i+1]
        for _ in range(40):
            m=(a+b)/2
            if curv(a)*curv(m)<=0: b=m
            else: a=m
        roots.append((a+b)/2)
out['y_c']=[float(r) for r in roots]; out['FORK']=bool(roots)
if roots:
    yc=max(roots); br=[]
    for y in np.linspace(0.88,yc-1e-3,10):
        xs=np.linspace(0.5,1.0,2001)[1:]; v=[V0(x,y) for x in xs]; j=int(np.argmin(v))
        br.append(dict(y=float(y),x_min=float(xs[j]),delta=float(xs[j]-0.5),V0=float(v[j]),V0_on_line=float(V0(0.5,y))))
    out['branches']=br
print(json.dumps({k:v for k,v in out.items() if k not in('y','curv')},indent=1))
print('sign pattern:', ''.join('+' if c>0 else '-' for c in cs))
os.makedirs('field_tests/results/YFORK',exist_ok=True); json.dump(out,open('field_tests/results/YFORK/out.json','w'),indent=1)
