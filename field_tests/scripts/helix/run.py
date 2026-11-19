"""PREREG_HELIX.md. Usage: python3 run.py G s   |   python3 run.py R s' lam"""
import json, math, sys, os
sys.path.insert(0, '.')
import numpy as np
from scipy.interpolate import CubicSpline
from tools.serapis_calc.shapes import E
from tools.serapis_calc.nstar import Nstar
from tools.serapis_calc.ms import Background
from tools.janus_calc.core import Model, spectra3
strand, s = sys.argv[1], float(sys.argv[2]); lam = float(sys.argv[3]) if strand == 'R' else None
TR = 8.94e8; SQ2 = math.sqrt(2); yr = math.sqrt(3)/2
F = lambda y: E(complex(0.5, y), s).real
def Dl(y, h=1e-3):
    L = lambda t: math.log(F(y*math.exp(t)))
    return (-L(2*h) + 8*L(h) - 8*L(-h) + L(-2*h))/(12*h)
Fr = F(yr)
def V0(y):
    if strand == 'G': return (Dl(y)/s)**2
    e = max(lam*(F(y) - Fr), 1e-14); return e/(e + 1)
ph = np.linspace(math.log(yr)/SQ2 + 1e-4, math.log(3000)/SQ2, 4000); ys = np.exp(SQ2*ph)
Vt = np.array([V0(y) for y in ys])
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
row = dict(strand=strand, s=s, lam=lam)
try:
    M = Model(V, dV, p0, Nmax=4000); Ve = V(M.sol.sol(M.Nend)[0]); N = 50.0
    for _ in range(40):
        a = spectra3(M, N); N2 = Nstar(a['r'], V(M.sol.sol(M.Nend - N)[0])/Ve, TR)
        if abs(N2 - N) < 1e-4: N = N2; break
        N = N2
    a = spectra3(M, N); ps = M.sol.sol(M.Nend - N)[0]
    row.update(ns=float(a['ns']), r=float(a['r']), alpha_s=float(a['alpha_s']), Nstar=N, y_star=float(math.exp(SQ2*ps)))
except Exception as ex:
    row.update(error=str(ex)[:120])
print(json.dumps(row), flush=True); os.makedirs('field_tests/results/HELIX', exist_ok=True)
json.dump(row, open(f'field_tests/results/HELIX/{strand}_s{s:g}.json', 'w'), indent=1)
