"""D2168 weave_core: one engine = scales (margins) + fingerprint (Jacobian) + compass + lenses + per-node optimisation.
Nodes are the D2156 VN resonance margins (unchanged equations). python3 tools/loom/weave_core.py"""
import math, time, json, sys, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lens_core import lens
src = open(os.path.join(HERE, 'resonance_d2156.py')).read()
src = src[:src.index("out = dict(variant=VAR")]            # definitions only (no breathing loop)
G = {'__name__': 'weave_core_import', '__file__': os.path.join(HERE, 'resonance_d2156.py')}
sys.argv = ['x', 'VN']; exec(compile(src, 'resonance_d2156.py', 'exec'), G)
margins, D = G['margins'], dict(G['D'])
DIALS = ['u', 'MN', 'm32', 'TR', 'split', 'dNeff']; LOG = {'u', 'MN', 'm32', 'TR'}
def to_state(z):
    s = dict(D)
    for j, k in enumerate(DIALS): s[k] = D[k] * math.exp(z[j]) if k in LOG else D[k] + z[j]
    return s
def nodes(z):
    m = margins(to_state(z)); out = {}
    for L, d in m.items():
        if isinstance(d, dict):
            for name, v in d.items(): out[f'L{L}.{name}'] = float(v)
    return out
t0 = time.time()
z0 = np.zeros(len(DIALS)); base = nodes(z0); names = list(base); m0 = np.array([base[n] for n in names])
def vec(z):
    try: b = nodes(z); return np.array([b[n] for n in names])
    except (ZeroDivisionError, ValueError, OverflowError): return np.full(len(names), -1e6)   # DEV-1
t1 = time.time(); h = 1e-3
J = np.array([(vec(z0 + h*e) - vec(z0 - h*e)) / (2*h) for e in np.eye(len(DIALS))]).T     # nodes x dials
t_fp = time.time() - t1
lz = lens(J)
compass = {}
for i, n in enumerate(names):
    g = J[i]; nrm = np.linalg.norm(g)
    if nrm < 1e-12: compass[n] = dict(direction=None, note='no dial moves this node (data-fixed or TRUST)'); continue
    d = g / nrm; hurt = [names[k] for k in range(len(names)) if k != i and J[k] @ d < -1e-9 and m0[k] >= 0]
    compass[n] = dict(direction={DIALS[j]: round(float(d[j]), 3) for j in range(len(DIALS)) if abs(d[j]) > 1e-3}, hurts=hurt)
hold = [i for i in range(len(names)) if m0[i] >= 0]
opt = {}
for i, n in enumerate(names):
    if m0[i] >= 0: continue
    best = None
    cons = [{'type': 'ineq', 'fun': (lambda z, i=i: vec(z)[i])}] + [{'type': 'ineq', 'fun': (lambda z, k=k: vec(z)[k])} for k in hold]
    rng = np.random.default_rng(i)
    for s in range(5):
        x0 = rng.normal(0, 0.3, len(DIALS)) if s else np.zeros(len(DIALS))
        r = minimize(lambda z: float(z @ z), x0, method='SLSQP', constraints=cons, bounds=[(-3, 3)]*len(DIALS), options={'maxiter': 300, 'ftol': 1e-10})
        if r.success:
            v = vec(r.x)
            if v[i] >= -1e-6 and all(v[k] >= -1e-6 for k in hold) and (best is None or r.fun < best[0]): best = (r.fun, r.x, v)
    if best is None:
        opt[n] = dict(verdict='NOT CLOSABLE BY DIALS', margin=round(float(m0[i]), 4)); continue
    st = to_state(best[1]); spent = [k for k in DIALS if (abs(st[k]/D[k] - 1) > 0.01 if k in LOG else abs(st[k] - D[k]) > 1e-9)]
    payers = [names[k] for k in hold if best[2][k] < m0[k] - 0.05]
    opt[n] = dict(verdict='CLOSABLE', margin=round(float(m0[i]), 4), move={k: round(float(best[1][j]), 4) for j, k in enumerate(DIALS) if abs(best[1][j]) > 1e-4},
                  fits_spent=spent, who_pays=payers)
res = dict(dials=DIALS, nodes={n: round(float(m0[i]), 4) for i, n in enumerate(names)}, n_nodes=len(names), n_holding=len(hold),
           fingerprint={n: {DIALS[j]: round(float(J[i, j]), 4) for j in range(len(DIALS)) if abs(J[i, j]) > 1e-6} for i, n in enumerate(names)},
           lenses=dict(rank=int(lz.shape[1]) if lz is not None else 0),
           singular_values=[round(float(x), 4) for x in np.linalg.svd(J, compute_uv=False)],
           compass=compass, per_node_optimisation=opt, seconds_fingerprint=round(t_fp, 3), seconds_total=round(time.time() - t0, 2))
json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'd2168_weave_core.json'), 'w'), indent=1, default=str)
print('nodes', res['n_nodes'], 'holding', res['n_holding'], '| singular values', res['singular_values'])
for n, v in opt.items(): print(n, v)
print('fingerprint %.3fs total %.2fs' % (t_fp, res['seconds_total']))
