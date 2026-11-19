"""PREREG_SPTILT.md. Usage: python3 run.py FAMILY f   (FAMILY in T1 T2 T3 T5)"""
import json, math, sys, os
sys.path.insert(0, '.')
import numpy as np
from scipy.interpolate import CubicSpline
from tools.serapis_calc.shapes import E
from tools.serapis_calc.nstar import Nstar
from tools.serapis_calc.ms import Background
from tools.janus_calc.core import Model, spectra3
fam, f = sys.argv[1], float(sys.argv[2]); TR = 8.94e8; SQ2 = math.sqrt(2); YS = 55.64
E3 = lambda y: E(complex(0.5, y), 1.5).real
X = {'T1': lambda y: E3(y)**(1/3), 'T2': lambda y: E3(y)**(2/3), 'T3': E3, 'T5': lambda y: E(complex(0.5, y), 2.5).real, 'TB': lambda y: E3(y)/y}[fam]  # TB added by PREREG_SPTILT_T1X
yr = math.sqrt(3)/2; Xr = X(yr); C = f*8e-4/(X(YS) - Xr)
def Dl(y, h=1e-3):
    L = lambda t: math.log(E3(y*math.exp(t)))
    return (-L(2*h) + 8*L(h) - 8*L(-h) + L(-2*h))/(12*h)
ph = np.linspace(math.log(yr)/SQ2 + 1e-4, math.log(3000)/SQ2, 4000); ys = np.exp(SQ2*ph)
Vt = np.array([(2*Dl(y)/3)**2*(1 + C*(X(y) - Xr)) for y in ys])
S = CubicSpline(ph, Vt); dS = S.derivative(); V = lambda p: float(S(p)); dV = lambda p: float(dS(p))
lo, hi = 10, len(ph) - 5; p0 = None
for _ in range(14):
    mid = (lo + hi)//2
    try: ne = Background(V, dV, ph[mid]).Nend
    except Exception: ne = None
    if ne is None or ne > 140: hi = mid
    else: lo = mid
    if ne is not None and 100 <= ne <= 200: p0 = ph[mid]; break
p0 = p0 if p0 is not None else ph[lo]
M = Model(V, dV, p0, Nmax=4000); Ve = V(M.sol.sol(M.Nend)[0]); N = 50.0
for _ in range(40):
    a = spectra3(M, N); N2 = Nstar(a['r'], V(M.sol.sol(M.Nend - N)[0])/Ve, TR)
    if abs(N2 - N) < 1e-4: N = N2; break
    N = N2
a = spectra3(M, N); ps = M.sol.sol(M.Nend - N)[0]
row = dict(family=fam, f=f, C=C, ns=float(a['ns']), r=float(a['r']), alpha_s=float(a['alpha_s']), Nstar=N, y_star=float(math.exp(SQ2*ps)),
           in_band=bool(0.969 <= a['ns'] <= 0.975 and 4.55e-4 <= a['r'] <= 5.7e-4))
print(json.dumps(row), flush=True); os.makedirs('field_tests/results/SPTILT', exist_ok=True)
json.dump(row, open(f'field_tests/results/SPTILT/{fam}_f{f:g}.json', 'w'), indent=1)
