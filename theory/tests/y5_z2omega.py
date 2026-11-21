"""Y5 (locked PREREG_Y5_Z2OMEGA): T2/Z2 at tau=omega, 4-4-8, lepton hierarchy from Higgs direction; down-quark control."""
import numpy as np, math, json, sys
from scipy.optimize import minimize
sys.path.insert(0, 'theory/tests')
from z3_modes import modes, TAU
def even(M, z):
    P = modes(M, 0, 0, z); cols = [P[:, 0]]
    for j in range(1, M // 2): cols.append((P[:, j] + P[:, M - j]) / math.sqrt(2))
    cols.append(P[:, M // 2]); return np.array(cols).T
rng = np.random.default_rng(5); z = rng.uniform(0, 1, 600) + TAU * rng.uniform(0, 1, 600)
L = even(4, z); H = even(8, z)
P = np.einsum('pi,pj->pij', L, L).reshape(len(z), -1)
c, *_ = np.linalg.lstsq(H, P, rcond=None); res = np.linalg.norm(H @ c - P) / np.linalg.norm(P)
c = c.T.reshape(3, 3, 5); print('gate residual %.1e' % res)
def ratios(h):
    s = np.sort(np.linalg.svd(np.einsum('ijk,k->ij', c, h), compute_uv=False)); return s[0] / s[1], s[1] / s[2]
def run(t12, t23, tag):
    hr = np.random.default_rng(11); h = hr.normal(size=(50000, 5)) + 1j * hr.normal(size=(50000, 5))
    s = np.sort(np.linalg.svd(np.einsum('ijk,nk->nij', c, h), compute_uv=False), axis=1)
    r12, r23 = s[:, 0] / s[:, 1], s[:, 1] / s[:, 2]
    frac = float(((np.abs(np.log(r12 / t12)) < math.log(3)) & (np.abs(np.log(r23 / t23)) < math.log(3))).mean())
    loss = lambda x: sum(np.log(np.array(ratios(x[:5] + 1j * x[5:])) / [t12, t23]) ** 2)
    sr = np.random.default_rng(12); best = None
    for _ in range(40):
        o = minimize(loss, sr.normal(size=10), method='Nelder-Mead', options=dict(maxiter=6000, xatol=1e-10, fatol=1e-14))
        if best is None or o.fun < best.fun: best = o
    hb = best.x[:5] + 1j * best.x[5:]; hb /= np.linalg.norm(hb); rb = ratios(hb)
    dev = [abs(rb[0] / t12 - 1), abs(rb[1] / t23 - 1)]
    v = 'PASS' if frac >= 0.01 else 'HOSTED' if max(dev) < 0.1 else 'FAIL' if max(rb[0]/t12, t12/rb[0], rb[1]/t23, t23/rb[1]) > 2 else 'between'
    out = dict(tag=tag, frac=frac, best_ratios=[float(x) for x in rb], dev=dev, best_h_abs=[float(x) for x in np.abs(hb)],
               median=[float(np.median(r12)), float(np.median(r23))], verdict=v)
    print(out); return out
ctrl = run(0.050, 0.0137, 'down-quark control'); lep = run(4.84e-3, 5.95e-2, 'charged leptons')
json.dump(dict(gate=float(res), control=ctrl, leptons=lep), open('field_tests/results/y5_z2omega.json', 'w'), indent=1)
