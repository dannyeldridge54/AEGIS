"""PREREG_S3_NOFREE"""
import sys, math, json, random
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, 'tools/weave_cm'); import weave_tools as W, weave_sweep as WS
T, TOL, score = WS.T, WS.TOL, WS._score
tau_d = complex(-0.4700812136339729, 0.9005346510920798)   # D1778 m = 1/2 minimum
W._TAU[0] = tau_d; W._TAU.setdefault(8, WS._tau_for(8))
keys = ['r1', 'r2', 'g_abs', 'g_arg', 'f_abs', 'f_arg']
def args(d, u): return {'model': 'w864', 'rung_d': 0, 'rung_u': 8, 'down': dict(zip(keys, d)), 'up': dict(zip(keys, u))}
def ev(d, u):
    try: o = W.weave_ckm(args(d, u)); return score(o), o
    except Exception: return 1e9, None
def report(s, o): return dict(score=s, fails=[k for k in T if not (1/TOL[k] <= o[k]/T[k] <= TOL[k])], ratios={k: o[k]/T[k] for k in T})
out = {}
s, o = ev([1, 1, 1, 0, 1, 0], [1, 1, 1, 0, 1, 0]); out['a_zero_free'] = report(s, o)
def search(build, n, lo, hi, seed):
    rng = random.Random(seed); f = lambda x: ev(*build(np.clip(x, lo, hi)))[0]
    st = sorted(((f(x), x) for x in (np.array([rng.uniform(lo[i], hi[i]) for i in range(n)]) for _ in range(400))), key=lambda t: t[0])
    best = (1e9, None)
    for _, x0 in st[:5]:
        r = minimize(f, x0, method='Nelder-Mead', options=dict(maxiter=4000))
        if r.fun < best[0]: best = (r.fun, np.clip(r.x, lo, hi))
    s, o = ev(*build(best[1])); rr = report(s, o); rr['x'] = list(map(float, best[1])); return rr
pb = lambda x: ([1, 1, 1, x[0], 1, x[1]], [1, 1, 1, x[2], 1, x[3]])
out['b_phases_only'] = search(pb, 4, np.array([-math.pi] * 4), np.array([math.pi] * 4), 18)
mb = lambda x: ([x[0], x[1], x[2], 0, x[3], 0], [x[4], x[5], x[6], 0, x[7], 0])
out['c_moduli_only'] = search(mb, 8, np.array([0.5] * 8), np.array([2.0] * 8), 28)
k = 0 if not out['a_zero_free']['fails'] else 4 if not out['b_phases_only']['fails'] else 8 if not out['c_moduli_only']['fails'] else '>8 (needs phases and moduli)'
out['k_free'] = k
print(json.dumps(out, indent=1, default=str))
