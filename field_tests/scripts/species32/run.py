"""PREREG_SPECIES32.md. Usage: python3 run.py F C  (engine F)  |  python3 run.py X C  (exact MS confirmation)"""
import json, math, sys, os, time
sys.path.insert(0, '.')
import numpy as np
from scipy.interpolate import CubicSpline
from tools.serapis_calc.shapes import E
from tools.serapis_calc.nstar import Nstar
from tools.serapis_calc.ms import Background, spectra
from tools.janus_calc.core import Model, spectra3
mode, C = sys.argv[1], float(sys.argv[2]); TR = 8.94e8; SQ2 = math.sqrt(2)
Ef = lambda y: E(complex(0.5, y), 1.5).real
yr = math.sqrt(3)/2; Er = Ef(yr)
ph = np.linspace(math.log(yr)/SQ2 + 1e-4, math.log(3000)/SQ2, 4000); ys = np.exp(SQ2*ph)
D = np.array([(math.log(Ef(y*(1 + 1e-6))) - math.log(Ef(y*(1 - 1e-6))))/(2e-6) for y in ys])
Ev = np.array([Ef(y) for y in ys])
Vt = (2*D/3)**2*(1 + C*(Ev - Er))
S = CubicSpline(ph, Vt); dS = S.derivative()
V = lambda p: float(S(p)); dV = lambda p: float(dS(p))
chk = dict(V_rho=(2/3*((math.log(Ef(yr*(1+1e-6))) - math.log(Ef(yr*(1-1e-6))))/2e-6))**2)
m = (ys > 20) & (ys < 200); chk['k_fit'] = float(-np.polyfit(np.log(ys[m]), np.log(1 - (2*D[m]/3)**2), 1)[0])
lo, hi = 10, len(ph) - 5; p0 = None
for _ in range(14):
    mid = (lo + hi)//2
    try: ne = Background(V, dV, ph[mid]).Nend
    except Exception: ne = None
    if ne is None or ne > 140: hi = mid
    else: lo = mid
    if ne is not None and 100 <= ne <= 200: p0 = ph[mid]; break
p0 = p0 if p0 is not None else ph[lo]; t = time.time()
if mode == 'F':
    M = Model(V, dV, p0, Nmax=4000); Ve = V(M.sol.sol(M.Nend)[0]); N = 50.0
    for _ in range(40):
        a = spectra3(M, N); N2 = Nstar(a['r'], V(M.sol.sol(M.Nend - N)[0])/Ve, TR)
        if abs(N2 - N) < 1e-4: N = N2; break
        N = N2
    a = spectra3(M, N); ps = M.sol.sol(M.Nend - N)[0]; r = dict(ns=a['ns'], r=a['r'], alpha_s=a['alpha_s'], Nstar=N)
else:
    bg = Background(V, dV, p0); N = 50.0
    for _ in range(20):
        res = spectra(bg, N); Nn = Nstar(res['r'], V(bg.sol.sol(bg.Nend - N)[0])/V(bg.sol.sol(bg.Nend)[0]), TR)
        if abs(Nn - N) < 0.02: N = Nn; break
        N = Nn
    res = spectra(bg, N); ps = bg.sol.sol(bg.Nend - N)[0]; r = dict(ns=res['ns'], r=res['r'], alpha_s=res['alpha_s'], Nstar=N)
inb = 0.969 <= r['ns'] <= 0.975 and 4.55e-4 <= r['r'] <= 5.7e-4
near = abs(min(max(r['ns'], 0.969), 0.975) - r['ns']) <= 0.003 and 4.55e-4/1.3 <= r['r'] <= 5.7e-4*1.3
row = dict(engine=mode, C=C, ns=float(r['ns']), r=float(r['r']), alpha_s=float(r['alpha_s']), Nstar=float(r['Nstar']),
           y_star=float(math.exp(SQ2*ps)), in_band=bool(inb), near=bool(near), checks=chk, seconds=round(time.time() - t, 1))
print(json.dumps(row), flush=True); os.makedirs('field_tests/results/SPECIES32', exist_ok=True)
json.dump(row, open(f'field_tests/results/SPECIES32/{mode}_C{C:g}.json', 'w'), indent=1)
