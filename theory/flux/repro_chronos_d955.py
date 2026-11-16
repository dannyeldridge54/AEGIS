import sys, math, numpy as np
sys.path.insert(0,'.')
from scipy.interpolate import CubicSpline
from tools.serapis_calc.modular import I_inv
from tools.serapis_calc.ms import Background, spectra
s2=math.sqrt(2)
ph=np.linspace(1e-4,math.log(60)/s2,3000); ys=np.exp(s2*ph)
I2=np.array([I_inv(1j*y,2) for y in ys]); I1=np.array([I_inv(1j*y,1) for y in ys])
S2=CubicSpline(ph,I2); S1=CubicSpline(ph,I1); d2=S2.derivative(); d1=S1.derivative()
def mk(eps):
    V=lambda p:(lambda a:a*a/(a*a+1))(float(S2(p)))+eps*float(S1(p))
    dV=lambda p:(lambda a,da:2*a*da/(a*a+1)**2)(float(S2(p)),float(d2(p)))+eps*float(d1(p))
    return V,dV
L=[];R={}
for eps in (1.3e-4,1.6e-4,0.0):
    V,dV=mk(eps); bg=Background(V,dV,math.log(45)/s2)
    for Ns in (46.0,49.0):
        r=spectra(bg,Ns); ystar=math.exp(s2*bg.sol.sol(bg.Nend-Ns)[0]); r['y']=ystar; R[(eps,Ns)]=r
        L.append(f"eps={eps:.1e} N*={Ns}: ns={r['ns']:.5f} r={r['r']:.3e} alpha_s={r['alpha_s']:.3e} y*={ystar:.2f} (Ntot {bg.Nend:.1f})")
ch=[R[k] for k in R if k[0]>0]; ka=[R[k] for k in R if k[0]==0]
ns=[c['ns'] for c in ch]
ok=all(0.9685<=x<=0.9765 for x in ns) and abs(min(ns)-0.970)<=0.0015 and abs(max(ns)-0.975)<=0.0015 \
 and all(4.66e-4<=c['r']<=5.87e-4 for c in ch) and all(22.7<=c['y']<=24.8 for c in ch) and all(-11.2e-4<=c['alpha_s']<=-7.9e-4 for c in ch) \
 and all(0.9575<=c['ns']<=0.9625 and 3.2e-4<=c['r']<=3.8e-4 and 21.6<=c['y']<=22.9 for c in ka)
L.append('PASS' if ok else 'FAIL')
open('field_tests/results/repro_chronos_d955.txt','w').write('\n'.join(L)+'\n'); print('\n'.join(L))
