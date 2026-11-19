"""D1655 / Janus genesis G9c: basin map (PREREG_D1655_G9C_BASIN). Reuses the D1653 model unchanged."""
import json, math, sys
sys.path.insert(0, '.')
import numpy as np
src = open('field_tests/scripts/janus_g/g9b_tau_plane.py').read().split('runs = {}')[0]; exec(src)
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
cal = json.load(open('field_tests/results/GENESIS_DE/rescore.json'))['calibration']
data = {'Pantheon+': (-0.838, 0.055, -0.62, 0.22, 0.19), 'Union3': (-0.667, 0.088, -1.09, 0.31, 0.27), 'DESY5': (-0.752, 0.057, -0.86, 0.23, 0.20)}
def dchi2(w0, wa, d, rho):
    m0, s0, ma, su, sd = d; s1 = su if wa > ma else sd
    x = (w0 - m0) / s0; y = (wa - ma) / s1; return (x * x - 2 * rho * x * y + y * y) / (1 - rho * rho)
runs = {}
for dx in (0.05, 0.1, 0.2, 0.3, 0.4, 0.5):
    x0 = 0.5 + dx
    grid = [0.5 * 2 ** k for k in range(12)]; vals = [H2today(g, x0) - 1 for g in grid]
    VL = next(brentq(lambda g: H2today(g, x0) - 1, lo, hi, xtol=1e-10) for lo, hi, p, q in zip(grid, grid[1:], vals, vals[1:]) if p < 0 < q)
    sol = solve_ivp(rhs_f(VL), (math.log(1e-3), math.log(50.0)), [x0, y0, 0, 0], rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.004)
    def wcurve(N):
        X, Y, U, Vv = sol.sol(N); a = np.exp(N); rm = 3 * Om * a ** -3; rr = 3 * Or * a ** -4
        Vp = VL * np.array([Vfun(x, y) for x, y in zip(np.atleast_1d(X), np.atleast_1d(Y))])
        s2 = (U * U + Vv * Vv) / (b2 * Y * Y); H2 = (rm + rr + Vp) / (3 - s2 / 2); K = 0.5 * H2 * s2
        return X, Y, a, rm, rr, Vp, K
    aa = np.linspace(1 / 3, 1, 60); _, _, _, _, _, Vp, K = wcurve(np.log(aa)); w = (K - Vp) / (K + Vp)
    w0, wa = np.linalg.lstsq(np.vstack([np.ones_like(aa), 1 - aa]).T, w, rcond=None)[0]
    dmax = max(dchi2(w0, wa, d, cal[k]['rho']) for k, d in data.items())
    N = np.linspace(0, math.log(50.0), 12001); X, Y, a, rm, rr, Vp, K = wcurve(N); rt = K + Vp; wl = (K - Vp) / (K + Vp)
    acc = -(rm + rr + rt + 3 * (rr / 3 + K - Vp)); i_acc = int(np.argmax((acc < 0) & (N > 0)))
    late = N >= 0.8 * N[-1]; xm, ym = float(np.mean(X[late])), float(np.mean(Y[late]))
    t = fd(xm, ym); di = abs(t - 1j); dr = min(abs(t - complex(0.5, math.sqrt(3) / 2)), abs(t - complex(-0.5, math.sqrt(3) / 2)))
    runs[str(dx)] = dict(VL=VL, w0=float(w0), wa=float(wa), dchi2_worst=float(dmax), a_end_acc=float(a[i_acc]), late_tau=[xm, ym],
                         fundamental=[t.real, t.imag], dist_i=di, dist_rho=dr, end_class='i-class' if di < 0.02 else ('rho-class' if dr < 0.02 else 'other'),
                         late_w=float(np.sum(wl[late] * rt[late]) / np.sum(rt[late])))
    print(dx, runs[str(dx)]['end_class'], round(w0, 3), round(wa, 3), round(dmax, 2), flush=True)
cls = {k: v['end_class'] for k, v in runs.items()}
reading = 'i is the universal end point (for this start height)' if all(c == 'i-class' for c in cls.values()) else 'basin boundary: ' + json.dumps(cls)
out = dict(D='D1655', runs=runs, classes=cls, reading=reading)
json.dump(out, open('field_tests/results/D1655_G9c_basin.json', 'w'), indent=1)
print(reading)
