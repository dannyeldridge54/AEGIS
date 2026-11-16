import sys, math, numpy as np
sys.path.insert(0,'.')
from scipy.interpolate import CubicSpline
from tools.serapis_calc.potentials import Ehat, RHO_Y
from tools.serapis_calc.ms import Background, spectra_fast
from tools.serapis_calc.nstar import Nstar
s2=math.sqrt(2); C0=1.15e-6; TR0=6.7e9; Er=5.7833593
ph=np.linspace(np.log(RHO_Y)/s2+1e-4,np.log(3000)/s2,4000)
Eg=np.maximum(2*1.0823232337111382*np.array([Ehat(np.exp(s2*p)) for p in ph]),1e-14)
S=CubicSpline(ph,Eg); dS=S.derivative(); L=[]; res={}
for lp in (1.0,1/Er,0.05):
    C=lp*C0
    V=lambda p,lp=lp,C=C:(lambda e:(lp*e)/(lp*e+1)*(1+C*e))(float(S(p)))
    dV=lambda p,lp=lp,C=C:(lambda e,de:de*(lp*(1+C*e)/(lp*e+1)**2+C*lp*e/(lp*e+1)))(float(S(p)),float(dS(p)))
    p0=ph[min(np.searchsorted(Eg,5000/lp),len(ph)-200)]
    bg=Background(V,dV,p0)
    if bg.Nend<58.5: L.append(f"lambda'={lp:.4f}: only {bg.Nend:.1f} e-folds at C={C:.3e}: cannot give N*~50"); continue
    Ve=V(bg.sol.sol(bg.Nend)[0]); TR=TR0*lp**0.25; N=50.5
    for it in range(8):
        r=spectra_fast(bg,N); Nn=Nstar(r['r'],V(bg.sol.sol(bg.Nend-N)[0])/Ve,TR)
        if abs(Nn-N)<0.005: N=Nn; break
        N=Nn
    r=spectra_fast(bg,N); res[lp]=(N,r['ns'],r['r'])
    L.append(f"lambda'={lp:.4f}: C={C:.3e} T_R={TR:.3e} N*={N:.3f} n_s={r['ns']:.5f} r={r['r']:.4e} (Ntot {bg.Nend:.1f})")
if 1.0 in res:
    b=res[1.0]
    for lp in res:
        if lp!=1.0: d=res[lp]; L.append(f"lambda'={lp:.4f}: dN*={d[0]-b[0]:+.3f} dn_s={d[1]-b[1]:+.2e} dr/r={d[2]/b[2]-1:+.2%}")
    d=res.get(1/Er); ok=d is not None and abs(d[1]-b[1])<1e-3 and abs(d[2]/b[2]-1)<0.05
    L.append('PASS' if ok else 'FAIL')
open('field_tests/results/projH_refitC_d976.txt','w').write('\n'.join(L)+'\n'); print('\n'.join(L))
