"""D1357 (locked PREREG_D1357_btr_scale.md): endpoint cut-offs and mixed BCs vs the common −4% to BTR."""
import json, math, sys, numpy as np, sympy as sp
sys.path.insert(0, '.')
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
from tools.kaluza.background import vacuum
from tools.kaluza.spectra import scalar_UJ
from tools.kaluza.scalar import kk_scalar
bg = vacuum(10, sp.Rational(3, 2)); U, J, eB = scalar_UJ(bg); c = math.sqrt(2*9/8)
def mLpi(x1, x2, th0=0.0, th1=0.0, n=2):
    y1, y2 = x1/c, x2/c; L = quad(eB, y1, y2, limit=500, epsrel=1e-10)[0]
    te = lambda m2: solve_ivp(lambda yy, t: [J(yy)*(math.cos(t[0])**2 + (m2 - U(yy))*math.sin(t[0])**2)], [y1, y2], [th0], method='LSODA', rtol=1e-9, atol=1e-11).y[0, -1]
    grid = sorted(set(np.concatenate([np.linspace(-50, 0, 6), np.logspace(-2, 3, 140)]))); out, prev = [], None
    for m2 in grid:
        v = te(m2)
        if prev is not None:
            for k in range(0, 40):
                tg = th1 + k*math.pi
                if tg > th0 and (prev[1] - tg)*(v - tg) < 0: out.append(brentq(lambda x: te(x) - tg, prev[0], m2, xtol=1e-10))
        prev = (m2, v)
        if len(out) >= n: break
    m2s = sorted(out)[:n]; return [math.sqrt(v)*L/math.pi for v in m2s if v > 0], L
R = {}; base = kk_scalar(10, 1.5)['mL_over_pi']; R['baseline'] = base
R['T2'] = {str(x1): mLpi(x1, 8.0)[0] for x1 in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6)}
R['T3'] = {str(x2): mLpi(1e-4, x2)[0] for x2 in (6.0, 7.0, 8.0, 9.0, 10.0)}
R['T4'] = {'D_then_N': mLpi(1e-4, 8.0, 0.0, math.pi/2)[0], 'N_then_D': mLpi(1e-4, 8.0, math.pi/2, math.pi)[0]}
btr = [0.97, 2.13]
def shift(v): return [round(v[i]/base[i] - 1, 5) for i in range(min(2, len(v)))]
for t in ('T2', 'T3', 'T4'):
    for k, v in R[t].items(): print(t, k, [round(x, 5) for x in v], 'shift vs baseline', shift(v), 'vs BTR', [round(v[i]/btr[i] - 1, 4) for i in range(min(2, len(v)))])
json.dump(R, open('field_tests/results/D1357_btr_scale.json', 'w'), indent=1)
