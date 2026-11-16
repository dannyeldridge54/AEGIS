import sys, math, numpy as np
sys.path.insert(0,'.')
from scipy.interpolate import CubicSpline
from tools.serapis_calc.potentials import Ehat, RHO_Y
from tools.serapis_calc.ms import Background, spectra
from tools.serapis_calc.nstar import Nstar
ph=np.linspace(np.log(RHO_Y)/np.sqrt(2)+1e-4,np.log(3000)/np.sqrt(2),4000)
Eg=np.maximum(2*1.0823232337111382*np.array([Ehat(np.exp(np.sqrt(2)*p)) for p in ph]),1e-14)
S=CubicSpline(ph,Eg); dS=S.derivative(); C=1.15e-6
V=lambda p:(lambda e:e/(e+1)*(1+C*e))(float(S(p)))
dV=lambda p:(lambda e,de:de*((1+C*e)/(e+1)**2+C*e/(e+1)))(float(S(p)),float(dS(p)))
bg=Background(V,dV,ph[np.searchsorted(Eg,600)])
Ve=V(bg.sol.sol(bg.Nend)[0])
ref={1e4:46.29,1e6:47.81,1e7:48.58,1e8:49.34,1e10:50.87}; L=[]; ok=True
for TR,N0 in ref.items():
    N=N0
    for it in range(8):
        r=spectra(bg,N,dlnk=(-0.05,0.0,0.05)); Vs=V(bg.sol.sol(bg.Nend-N)[0])
        Nn=Nstar(r['r'],Vs/Ve,TR)
        if abs(Nn-N)<0.005: N=Nn; break
        N=Nn
    good=abs(N-N0)<=0.10; ok&=good
    L.append(f"T_R={TR:.0e}: N*={N:.3f} (D719 {N0}) n_s={r['ns']:.5f} r={r['r']:.3e} V*/Ve={Vs/Ve:.4f} {'ok' if good else 'OFF'}")
L.append('PASS' if ok else 'FAIL')
open('field_tests/results/repro_nstar_d958.txt','w').write('\n'.join(L)+'\n'); print('\n'.join(L))
