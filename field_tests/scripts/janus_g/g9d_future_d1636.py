"""D1658 / Janus genesis G9d (PREREG_D1658_G9D_FUTURE_D1636). Reuses the D1653 2D model; Om per dataset."""
import json, math, sys
sys.path.insert(0, '.')
import numpy as np
src = open('field_tests/scripts/janus_g/g9b_tau_plane.py').read().split('runs = {}')[0]
G = {}; exec(src, G)
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
def run(amp, Om, dx, future=True):
    G['Om'] = Om; y0 = math.sqrt(G['A'] / amp); G['y0'] = y0; x0 = 0.5 + dx
    grid = [0.5 * 2 ** k for k in range(12)]; vals = [G['H2today'](g, x0) - 1 for g in grid]
    VL = next(brentq(lambda g: G['H2today'](g, x0) - 1, lo, hi, xtol=1e-10) for lo, hi, p, q in zip(grid, grid[1:], vals, vals[1:]) if p < 0 < q)
    tend = math.log(50.0) if future else 0.0
    sol = solve_ivp(G['rhs_f'](VL), (math.log(1e-3), tend), [x0, y0, 0, 0], rtol=1e-9, atol=1e-12, dense_output=True, max_step=0.004)
    def parts(N):
        X, Y, U, Vv = sol.sol(N); a = np.exp(N); rm = 3 * Om * a ** -3; rr = 3 * G['Or'] * a ** -4
        Vp = VL * np.array([G['Vfun'](x, y) for x, y in zip(X, Y)]); s2 = (U * U + Vv * Vv) / (G['b2'] * Y * Y)
        H2 = (rm + rr + Vp) / (3 - s2 / 2); K = 0.5 * H2 * s2; return X, Y, a, rm, rr, Vp, K
    aa = np.linspace(1 / 3, 1, 60); _, _, _, _, _, Vp, K = parts(np.log(aa)); w = (K - Vp) / (K + Vp)
    w0, wa = np.linalg.lstsq(np.vstack([np.ones_like(aa), 1 - aa]).T, w, rcond=None)[0]
    out = dict(amp=amp, w0=float(w0), wa=float(wa))
    if not future: return out
    N = np.linspace(0, math.log(50.0), 12001); X, Y, a, rm, rr, Vp, K = parts(N); rt = K + Vp; wl = (K - Vp) / (K + Vp)
    acc = -(rm + rr + rt + 3 * (rr / 3 + K - Vp)); m = (acc < 0) & (N > 0)
    late = N >= 0.8 * N[-1]; t = G['fd'](float(np.mean(X[late])), float(np.mean(Y[late])))
    di = abs(t - 1j); dr = min(abs(t - complex(0.5, math.sqrt(3) / 2)), abs(t - complex(-0.5, math.sqrt(3) / 2)))
    out.update(a_end_acc=float(a[int(np.argmax(m))]) if m.any() else None, end_class='i-class' if di < 0.02 else ('rho-class' if dr < 0.02 else 'other'),
               fundamental=[t.real, t.imag], late_w=float(np.sum(wl[late] * rt[late]) / np.sum(rt[late])))
    return out
res = {}
for ds in ('pantheonplus', 'union3', 'desy5'):
    j = json.load(open(f'field_tests/results/D1636/rt10_{ds}.json')); Om, ui, w0t = j['Om'], j['best']['ui'], j['cpl_fit']['w0']
    grid = np.geomspace(0.03, 0.36, 16); w0s = []
    for amp in grid:
        try: w0s.append(run(float(amp), Om, 0.0, future=False)['w0'])
        except StopIteration: w0s.append(np.nan)
    w0s = np.array(w0s); ok = np.isfinite(w0s)
    amp_m = float(np.interp(w0t, w0s[ok][::-1], grid[ok][::-1])) if (w0s[ok].min() <= w0t <= w0s[ok].max()) else None
    r = dict(Om=Om, u_i=ui, w0_D1636=w0t, w0_grid=[float(x) for x in w0s], amp_grid=[float(x) for x in grid], amp_matched=amp_m)
    r['same_u'] = {str(dx): run(ui, Om, dx) for dx in (0.0, 1e-3)}
    if amp_m: r['matched'] = {str(dx): run(amp_m, Om, dx) for dx in (0.0, 1e-3)}
    res[ds] = r
    print(ds, amp_m, {k: (v['w0'], v['a_end_acc'], v['end_class']) for k, v in r.get('matched', {}).items()}, flush=True)
m = [v for r in res.values() for v in r.get('matched', {}).values()]
ends = [v['a_end_acc'] for v in m]
reading = dict(acceleration_still_ends=all(e is not None for e in ends) and len(m) == 6, a_end_range=[min(e for e in ends if e), max(e for e in ends if e)] if any(ends) else None,
               end_classes=sorted({v['end_class'] for v in m}))
json.dump(dict(D='D1658', results=res, reading=reading), open('field_tests/results/D1658_G9d_future_d1636.json', 'w'), indent=1)
print(json.dumps(reading))
