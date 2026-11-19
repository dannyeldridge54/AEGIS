import sys, json, os, cmath, math; sys.path.insert(0,'field_tests/scripts/flav_rho')
import numpy as np, mpmath as mp
import importlib.util
spec=importlib.util.spec_from_file_location('r1','field_tests/scripts/flav_rho/run.py')
src=open('field_tests/scripts/flav_rho/run.py').read().split('out = {}')[0]
ns={}; exec(src,ns); Y=ns['Y']
w=mp.e**(2j*mp.pi/3)
out={}
def Ymat(t):
    y=[complex(v) for v in Y(t)]; n=y[0]; y=[v/n for v in y]
    Y1,Y2,Y3=y; return np.array([[Y1,Y3,Y2],[Y2,Y1,Y3],[Y3,Y2,Y1]])
pts={'rho':w+1,'i':1j}
for k,t in pts.items():
    d=np.linalg.det(Ymat(t)); out['det_'+k]=[float(abs(d)),float(np.degrees(cmath.phase(d)))]
# CP-symmetric: -conj(t) equivalent to t under SL(2,Z): rho -> -1/2 + i sqrt3/2 = rho - 1 ; i -> i
out['CP_image_rho']=str(complex(-(complex(w+1).conjugate()))); out['CP_image_i']=str(complex(-(1j).conjugate()))
rng=np.random.default_rng(1)
YM={k:Ymat(t) for k,t in pts.items()}
def M(t,c): return np.diag(c)@YM[{v:k for k,v in pts.items()}[t]]
Js=[];args=set()
for _ in range(2000):
    cu=rng.normal(size=3); cd=rng.normal(size=3)
    for tu,td in [('rho','rho'),('rho','i'),('i','i')]:
        Mu=M(pts[tu],cu); Md=M(pts[td],cd)
        a=cmath.phase(np.linalg.det(Mu)*np.linalg.det(Md)); args.add(round(math.degrees(a))%360)
        Uu=np.linalg.eigh(Mu@Mu.conj().T)[1]; Ud=np.linalg.eigh(Md@Md.conj().T)[1]
        V=Uu.conj().T@Ud
        J=np.imag(V[0,0]*V[1,1]*np.conj(V[0,1])*np.conj(V[1,0])); Js.append(abs(J))
out['argdet_set_deg']=sorted(args); out['theta_bar_set_deg']=sorted({(180-a)%360 for a in args})
out['maxJ']=float(max(Js)); out['theta_quantised_pass']=0 in out['theta_bar_set_deg']; out['CKM_phase_pass']=out['maxJ']>1e-6
print(json.dumps(out,indent=1)); os.makedirs('field_tests/results/FLAV_RHO',exist_ok=True)
json.dump(out,open('field_tests/results/FLAV_RHO/run5.json','w'),indent=1)
