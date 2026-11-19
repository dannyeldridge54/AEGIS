"""D1638 / Janus genesis G2: reverse thread with the exact SERAPIS v3 shape (PREREG_D1638_G2_THREAD_SHAPE)."""
import json, math, sys
sys.path.insert(0, '.')
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.interpolate import CubicSpline
from tools.serapis_calc import p3s
Om, Or, A, b = 0.31, 9e-5, 16 * math.pi ** 2 / 6 / (3 * 1.2020569031595942), 2 * math.sqrt(2)
C = 8e-7
phr = math.log(float(p3s.YRHO)) / math.sqrt(2)
ph = np.linspace(phr + 1e-4, math.log(3000.0) / math.sqrt(2), 6000)
fv = p3s.V_np(ph, C, 10); Sp = CubicSpline(ph, fv); dS = Sp.derivative()
f = lambda p: float(Sp(min(max(p, ph[0]), ph[-1]))); df = lambda p: float(dS(min(max(p, ph[0]), ph[-1])))
asym = lambda p: 1 - A * math.exp(-b * p)
def amp2phi(amp): return -math.log(amp / A) / b
dev = lambda amax: max(abs(f(p) / asym(p) - 1) for p in np.linspace(amp2phi(amax), ph[-1] - 1, 2000))
cal = json.load(open('field_tests/results/GENESIS_DE/rescore.json'))['calibration']
data = {'Pantheon+': (-0.838, 0.055, -0.62, 0.22, 0.19), 'Union3': (-0.667, 0.088, -1.09, 0.31, 0.27), 'DESY5': (-0.752, 0.057, -0.86, 0.23, 0.20)}
def dchi2(w0, wa, d, rho):
    m0, s0, ma, su, sd = d; s1 = su if wa > ma else sd
    x = (w0 - m0) / s0; y = (wa - ma) / s1; return (x * x - 2 * rho * x * y + y * y) / (1 - rho * rho)
def run(phii, VL):
    V = lambda p: VL * f(p); dV = lambda p: VL * df(p)
    def rhs(N, s):
        p, q = s; a = math.exp(N); rm = 3 * Om * a ** -3; rr = 3 * Or * a ** -4
        H2 = (rm + rr + V(p)) / (3 - q * q / 2); eps = (rm + 4 * rr / 3 + H2 * q * q) / (2 * H2)
        return [q, -(3 - eps) * q - dV(p) / H2]
    sol = solve_ivp(rhs, (math.log(1e-3), 0), [phii, 0.0], rtol=1e-9, atol=1e-12, dense_output=True)
    p, q = sol.y[:, -1]; H2 = (3 * Om + 3 * Or + V(p)) / (3 - q * q / 2)
    return sol, H2, V
def shoot(phii):
    g = lambda VL: run(phii, VL)[1] - 1.0
    grid = [0.5 * 2 ** k for k in range(15)]; vals = [g(v) for v in grid]
    for lo, hi, a_, b_ in zip(grid, grid[1:], vals, vals[1:]):
        if a_ < 0 < b_: return brentq(g, lo, hi, xtol=1e-12)
    return None
amps = np.geomspace(0.01, 3.0, 300); rows = []
for amp in amps:
    phii = amp2phi(amp)
    if phii <= ph[0]: rows.append(dict(amp=float(amp), viable=False, why='below rho')); continue
    VL = shoot(phii)
    if VL is None: rows.append(dict(amp=float(amp), viable=False, why='no shoot')); continue
    sol, H2, V = run(phii, VL); aa = np.linspace(1 / 3, 1, 60); w = []
    for a in aa:
        p, q = sol.sol(math.log(a)); H2a = (3 * Om * a ** -3 + 3 * Or * a ** -4 + V(p)) / (3 - q * q / 2); K = 0.5 * H2a * q * q; w.append((K - V(p)) / (K + V(p)))
    X = np.vstack([np.ones_like(aa), 1 - aa]).T; w0, wa = np.linalg.lstsq(X, np.array(w), rcond=None)[0]
    d = {k: float(dchi2(w0, wa, v, cal[k]['rho'])) for k, v in data.items()}
    rows.append(dict(amp=float(amp), viable=True, VL=VL, w0=float(w0), wa=float(wa), w_min=float(min(w)), d=d, dmax=max(d.values()), pass_all=max(d.values()) <= 6.18))
via = [r for r in rows if r['viable']]; pas = [r for r in via if r['pass_all']]
best = min(via, key=lambda r: r['dmax'])
win = (math.log(max(r['amp'] for r in pas)) - math.log(min(r['amp'] for r in pas))) if pas else 0.0
ref = dict(dmax=5.210219194495299, w0=-0.7830162101303397, wa=-0.38319005489192937, n_pass=3, window=0.045148592010002014)
shape = dict(maxdev_amp_le_0p2=dev(0.2), maxdev_amp_le_0p5=dev(0.5), f_min_grid=float(fv.min()), f_at_rho=float(fv[0]))
dw0, dwa, ddc = best['w0'] - ref['w0'], best['wa'] - ref['wa'], best['dmax'] - ref['dmax']
holds = abs(dw0) <= 0.02 and abs(dwa) <= 0.02 and abs(ddc) <= 0.5 and shape['maxdev_amp_le_0p2'] < 0.01
out = dict(D='D1638', shape=shape, n_viable=len(via), n_nonviable=len(rows) - len(via), nonviable_reasons=sorted({r.get('why') for r in rows if not r['viable']} - {None}),
           n_pass_all=len(pas), pass_window_dln=win, pass_amp_range=[min(r['amp'] for r in pas), max(r['amp'] for r in pas)] if pas else None,
           best=dict(amp=best['amp'], w0=best['w0'], wa=best['wa'], dmax=best['dmax'], d=best['d'], w_min=best['w_min']),
           ref_D1628=ref, delta=dict(w0=dw0, wa=dwa, dmax=ddc), verdict='CONTINUITY HOLDS' if holds else 'DIFFERENT', rows=rows)
json.dump(out, open('field_tests/results/D1638_G2_thread_shape.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'rows'}, indent=1))
