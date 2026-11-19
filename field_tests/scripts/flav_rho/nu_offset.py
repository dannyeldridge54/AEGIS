import json, os, itertools, math
import numpy as np, mpmath as mp
src=open('field_tests/scripts/flav_rho/run.py').read().split('out = {}')[0]; ns={}; exec(src,ns); Y=ns['Y']
w=np.exp(2j*np.pi/3)
S=np.array([[-1,2,2],[2,-1,2],[2,2,-1]])/3; T=np.diag([1,w,w**2])
_,VST=np.linalg.eig(S@T)
def Mnu(t):
    y=[complex(v) for v in Y(t)]; Y1,Y2,Y3=y
    return np.array([[2*Y1,-Y3,-Y2],[-Y3,2*Y2,-Y1],[-Y2,-Y1,2*Y3]])
def angles(U):
    s13=abs(U[0,2])**2; c13=1-s13
    return abs(U[0,1])**2/c13, s13, abs(U[1,2])**2/c13
data=dict(s12=(0.307,0.012,0.011),s13=(0.02195,0.00054,0.00058),s23=(0.561,0.012,0.015))
def pull(k,v):
    b,u,d=data[k]; return (v-b)/(u if v>b else d)
rows=[]; best=None
for v in np.linspace(-0.15,0.15,61):
    t=complex(0,math.exp(v)); M=Mnu(t)
    H=M.conj().T@M; ev,U=np.linalg.eigh(H); m=np.sqrt(np.abs(ev))   # ascending |m|
    for perm in itertools.permutations(range(3)):
        Ul=VST[:,list(perm)]
        for order in ('NO','IO'):
            idx=[0,1,2] if order=='NO' else [1,2,0]
            Un=U[:,idx]; mm=m[idx]
            P=Ul.conj().T@Un
            s12,s13,s23=angles(P)
            dm21=mm[1]**2-mm[0]**2; dm31=abs(mm[2]**2-mm[0]**2)
            r=dm21/dm31 if dm31>0 else float('inf')
            pr=(r-0.0298)/(0.03*0.0298)
            pulls=dict(s12=pull('s12',s12),s13=pull('s13',s13),s23=pull('s23',s23),r=pr)
            chi2=sum(p*p for p in pulls.values())
            row=dict(v=float(v),u=float(abs(math.tanh(v/2))),perm=perm,order=order,s12=float(s12),s13=float(s13),s23=float(s23),r=float(r),pulls={k:float(x) for k,x in pulls.items()},chi2=float(chi2))
            rows.append(row)
            if best is None or chi2<best['chi2']: best=row
passing=[r for r in rows if r['u']<=0.1 and all(abs(x)<3 for x in r['pulls'].values())]
at_i=[r for r in rows if abs(r['v'])<1e-12]
out=dict(best=best,n_pass=len(passing),PASS=bool(passing),first_pass=passing[0] if passing else None,
         at_i_best=min(at_i,key=lambda r:r['chi2']))
print(json.dumps(out,indent=1,default=str)); os.makedirs('field_tests/results/FLAV_RHO',exist_ok=True)
json.dump(dict(out,rows=rows[::7]),open('field_tests/results/FLAV_RHO/nu_offset.json','w'),indent=1,default=str)
