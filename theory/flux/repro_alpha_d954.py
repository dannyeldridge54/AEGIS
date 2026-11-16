import numpy as np, sys
sys.path.insert(0,'.')
from scipy.interpolate import CubicSpline
from tools.serapis_calc.potentials import Ehat, RHO_Y
from tools.serapis_calc.ms import Background, spectra
from tools.serapis_calc.relation import alpha_s as rel_alpha
import math
ph=np.linspace(np.log(RHO_Y)/np.sqrt(2)+1e-4,np.log(3000)/np.sqrt(2),4000)
Eg=2*1.0823232337111382*np.array([Ehat(np.exp(np.sqrt(2)*p)) for p in ph])  # DEVIATIONS D1: paper convention; Eg=np.maximum(Eg,1e-14)
S=CubicSpline(ph,Eg); dS=S.derivative()
def mk(C):
    V=lambda p:(lambda e:e/(e+1)*(1+C*e))(float(S(p)))
    dV=lambda p:(lambda e,de:de*((1+C*e)/(e+1)**2+C*e/(e+1)))(float(S(p)),float(dS(p)))
    return V,dV
L=[]; res={}
for C in (1.0e-6,1.3e-6,0.0):
    V,dV=mk(C)
    # start ~ 75 e-folds from the end: choose phi0 by slow-roll estimate N ~ Ehat/8
    bg=Background(V,dV,ph[np.searchsorted(Eg,600*1.0)] if C>0 else ph[np.searchsorted(Eg,600)])
    for Ns in ((48.4,49.9) if C>0 else (49.15,)):
        if bg.Nend<Ns+8: L.append(f'C={C} Ns={Ns}: only {bg.Nend:.1f} e-folds'); continue
        r=spectra(bg,Ns); res[(C,Ns)]=r
        ra=rel_alpha(r['ns'],r['r'],2*math.sqrt(2),1.0)
        L.append(f"C={C:.1e} N*={Ns}: ns={r['ns']:.5f} r={r['r']:.3e} alpha_s={r['alpha_s']:.3e} relation={ra:.3e} (Ntot {bg.Nend:.1f})")
cor=[res[k] for k in res if k[0]>0]
ns=[c['ns'] for c in cor]; rr=[c['r'] for c in cor]; al=[c['alpha_s'] for c in cor]
ok=len(cor)==4 and all(0.969<=x<=0.976 for x in ns) and abs(min(ns)-0.970)<=0.0015 and abs(max(ns)-0.975)<=0.0015 \
   and all(4.46e-4<=x<=5.25e-4 for x in rr) and all(-11.7e-4<=x<=-8.5e-4 for x in al)
z=res.get((0.0,49.15)); ok=ok and z is not None and abs(z['ns']-0.961)<=0.0015 and abs(z['r']/3.6e-4-1)<=0.05
L.append('PASS' if ok else 'FAIL')
open('field_tests/results/repro_alpha_d954.txt','w').write('\n'.join(L)+'\n'); print('\n'.join(L))
