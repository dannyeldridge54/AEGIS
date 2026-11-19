"""PREREG_DUAL.md. Usage: python3 run.py LEVEL C   (LEVEL = 10 or 8)"""
import json, math, sys, os, tempfile
sys.path.insert(0, '.')
import numpy as np
from scipy.interpolate import CubicSpline
from tools.serapis_calc.shapes import E
from tools.serapis_calc.eisenstein import E_paper
from tools.serapis_calc.nstar import Nstar
from tools.serapis_calc.ms import Background
from tools.janus_calc.core import Model, spectra3
lev, C = sys.argv[1], float(sys.argv[2]); TR = 8.94e8; SQ2 = math.sqrt(2); LAM8 = 0.063298
yr = math.sqrt(3)/2
ph = np.linspace(math.log(yr)/SQ2 + 1e-4, math.log(3000)/SQ2, 4000); ys = np.exp(SQ2*ph)
if lev == '10':
    E3 = lambda y: E(complex(0.5, y), 1.5).real
    def Dl(y, h=1e-3):
        L = lambda t: math.log(E3(y*math.exp(t)))
        return (-L(2*h) + 8*L(h) - 8*L(-h) + L(-2*h))/(12*h)
    Er = E3(yr); Vt = np.array([(2*Dl(y)/3)**2*(1 + C*(E3(y) - Er)) for y in ys])
else:
    E2r = E_paper(0.5, yr)
    e = np.array([LAM8*(E_paper(0.5, y) - E2r) for y in ys]); e = np.maximum(e, 1e-14)
    Vt = e/(e + 1)*(1 + C*e/LAM8)
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
row = dict(level=lev, C=C, lam8=LAM8 if lev == '8' else None, ns=float(a['ns']), r=float(a['r']), alpha_s=float(a['alpha_s']), Nstar=N, y_star=float(math.exp(SQ2*ps)))
print(json.dumps(row), flush=True); os.makedirs('field_tests/results/DUAL', exist_ok=True)
json.dump(row, open(f'field_tests/results/DUAL/L{lev}_C{C:g}.json', 'w'), indent=1)
