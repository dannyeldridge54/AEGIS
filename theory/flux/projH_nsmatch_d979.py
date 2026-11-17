import sys, math, numpy as np
sys.path.insert(0,'.')
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
from tools.serapis_calc.potentials import Ehat, RHO_Y
from tools.serapis_calc.ms import Background, spectra_fast
from tools.serapis_calc.nstar import Nstar
s2=math.sqrt(2); C0=1.15e-6; TR0=6.7e9; Er=5.7833593
ph=np.linspace(np.log(RHO_Y)/s2+1e-4,np.log(3000)/s2,4000)
Eg=np.maximum(2*1.0823232337111382*np.array([Ehat(np.exp(s2*p)) for p in ph]),1e-14)
S=CubicSpline(ph,Eg); dS=S.derivative()
def run(lp,C):
    V=lambda p:(lambda e:(lp*e)/(lp*e+1)*(1+C*e))(float(S(p)))
    dV=lambda p:(lambda e,de:de*(lp*(1+C*e)/(lp*e+1)**2+C*lp*e/(lp*e+1)))(float(S(p)),float(dS(p)))
    p0=ph[min(np.searchsorted(Eg,5000/lp),len(ph)-200)]; bg=Background(V,dV,p0)
    assert bg.Nend>=58.5, f'only {bg.Nend:.1f} e-folds'
    Ve=V(bg.sol.sol(bg.Nend)[0]); TR=TR0*lp**0.25; N=50.8
    for it in range(8):
        r=spectra_fast(bg,N); Nn=Nstar(r['r'],V(bg.sol.sol(bg.Nend-N)[0])/Ve,TR)
        if abs(Nn-N)<0.005: N=Nn; break
        N=Nn
    r=spectra_fast(bg,N); return N,r['ns'],r['r']
L=[]
Nb,nb,rb=run(1.0,C0); L.append(f"baseline lambda'=1 C={C0:.3e}: N*={Nb:.3f} n_s={nb:.5f} r={rb:.4e}")
lp=1/Er
f=lambda k: run(lp,k*lp*C0)[1]-nb
k=brentq(f,0.1,3.0,xtol=1e-4)
N,n,r=run(lp,k*lp*C0)
L.append(f"Project H lambda'={lp:.4f}: C={k*lp*C0:.4e} ({k:.4f} x lambda'C0) N*={N:.3f} n_s={n:.5f} r={r:.4e} r/r_base-1={r/rb-1:+.2%}")
L.append('indistinguishable at 3%' if abs(r/rb-1)<0.03 else f'r differs by {r/rb-1:+.1%} at equal n_s: LiteBIRD-class test')
open('field_tests/results/projH_nsmatch_d979.txt','w').write('\n'.join(L)+'\n'); print('\n'.join(L))
