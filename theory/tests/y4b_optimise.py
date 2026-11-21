import numpy as np, math, json, sys
from scipy.optimize import minimize
sys.path.insert(0, 'theory/tests')
from z3_modes import modes, z3_classes, TAU
rng = np.random.default_rng(3); z = rng.uniform(0, 1, 900) + TAU * rng.uniform(0, 1, 900)
L = modes(9, 1/6, 1/6, z); H = modes(18, 1/3, 1/3, z)
P = np.einsum('pi,pj->pij', L, L).reshape(len(z), -1)
c = np.linalg.lstsq(H, P, rcond=None)[0].T.reshape(9, 9, 18)
_, evL, VL, _ = z3_classes(9, 1/6, 1/6); _, evH, VH, _ = z3_classes(18, 1/3, 1/3)
cls = lambda ev: np.round(np.angle(ev) / (2 * math.pi) * 3) % 3
cL, cH = cls(evL), cls(evH)
ce = np.einsum('ia,jb,ijk,ck->abc', VL, VL, c, np.linalg.inv(VH))
def fit(T, t12, t23):
    def rat(h):
        s = np.sort(np.linalg.svd(np.einsum('ijk,k->ij', T, h), compute_uv=False)); return s[0] / s[1], s[1] / s[2]
    loss = lambda x: sum(np.log(np.array(rat(x[:6] + 1j * x[6:])) / [t12, t23]) ** 2)
    sr = np.random.default_rng(12); best = None
    for _ in range(40):
        o = minimize(loss, sr.normal(size=12), method='Nelder-Mead', options=dict(maxiter=8000, xatol=1e-10, fatol=1e-14))
        if best is None or o.fun < best.fun: best = o
    return rat(best.x[:6] + 1j * best.x[6:])
out = []
for a in range(3):
  for b in range(3):
    ia, ib = np.where(cL == a)[0], np.where(cL == b)[0]; k = (a + b) % 3
    sub = ce[np.ix_(ia, ib, range(18))]
    norms = [np.linalg.norm(sub[:, :, np.where(cH == q)[0]]) for q in range(3)]; k = int(np.argmax(norms))
    T = sub[:, :, np.where(cH == k)[0]]
    lep = fit(T, 4.84e-3, 5.95e-2); dq = fit(T, 0.050, 0.0137)
    row = dict(L=a, R=b, H=k, lep=[float(x) for x in lep], down=[float(x) for x in dq]); out.append(row); print(row)
def dev(r, t): return max(abs(r[0]/t[0]-1), abs(r[1]/t[1]-1)), max(r[0]/t[0], t[0]/r[0], r[1]/t[1], t[1]/r[1])
d = [dev(p['lep'], (4.84e-3, 5.95e-2)) for p in out]
v = 'HOSTED' if min(x[0] for x in d) < 0.1 else 'FAIL' if min(x[1] for x in d) > 2 else 'between'
dc = [dev(p['down'], (0.050, 0.0137)) for p in out]
vc = 'HOSTED' if min(x[0] for x in dc) < 0.1 else 'FAIL' if min(x[1] for x in dc) > 2 else 'between'
print('leptons', v, 'down control', vc)
json.dump(dict(pairs=out, verdict=v, control=vc), open('field_tests/results/y4b_optimise.json', 'w'), indent=1)
