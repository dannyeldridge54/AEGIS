"""PREREG_B6_RUNG: best CKM score per up-rung in two coupling boxes (w864, down rung 1)."""
import sys, math, json, random
import numpy as np
from scipy.optimize import minimize
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import weave_tools as W, weave_sweep as WS
T, TOL, score = WS.T, WS.TOL, WS._score
keys = ['r1', 'r2', 'g_abs', 'g_arg', 'f_abs', 'f_arg']
def run(u, B, bi):
    W._TAU.setdefault(u, WS._tau_for(u)); rng = random.Random(100 * u + bi)
    lo = np.array([1/B, 1/B, 1/B, -math.pi, 1/B, -math.pi] * 2); hi = np.array([B, B, B, math.pi, B, math.pi] * 2)
    def args(x): x = np.clip(x, lo, hi); return {'model': 'w864', 'rung_d': 1, 'rung_u': u, 'down': dict(zip(keys, x[:6])), 'up': dict(zip(keys, x[6:]))}
    def f(x):
        try: return score(W.weave_ckm(args(x)))
        except Exception: return 1e9
    starts = []
    for _ in range(400):
        x = np.array([math.exp(rng.uniform(math.log(lo[i]), math.log(hi[i]))) if i % 6 in (0, 1, 2, 4) else rng.uniform(-math.pi, math.pi) for i in range(12)])
        starts.append((f(x), x))
    starts.sort(key=lambda t: t[0]); best = (1e9, None)
    for s0, x0 in starts[:5]:
        r = minimize(f, x0, method='Nelder-Mead', options=dict(maxiter=4000))
        if r.fun < best[0]: best = (r.fun, np.clip(r.x, lo, hi))
    o = W.weave_ckm(args(best[1]))
    return dict(rung=u, box=B, score=score(o), fails=[k for k in T if not (1/TOL[k] <= o[k]/T[k] <= TOL[k])], obs={k: o[k] for k in T},
                eqcoef_gu_gd=(1 + 1/16) / (u + 1/16), eqcoef_pull=((1 + 1/16) / (u + 1/16) - 0.1276) / 0.0060)
def _one(t): return run(*t)
if __name__ == '__main__':   # PREREG_B6_RUNG_DEVIATIONS D1: 4 parallel processes, identical procedure and seeds
    import multiprocessing as mp
    jobs = [(u, B, bi) for bi, B in enumerate((3.0, 2.0)) for u in range(2, 11)]
    out = sys.argv[1] if len(sys.argv) > 1 else 'b6_rung.jsonl'
    with mp.Pool(4) as P, open(out, 'w') as f:
        for r in P.imap_unordered(_one, jobs): f.write(json.dumps(r) + '\n'); f.flush()
