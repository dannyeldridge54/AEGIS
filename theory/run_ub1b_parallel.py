"""UB-1b, same search run in parallel (field_tests/rules/UB1_DEVIATIONS.md, D1b-1: execution only).
The sample points, the scoring, the 40 Nelder-Mead polishes and the order in which their results are read are exactly
those of unify_hyperbolic_bg_ub1b.search; only the evaluations are spread over worker processes, so the result is
identical to the serial run.   python run_ub1b_parallel.py [workers]"""
import multiprocessing as mp
import sys

import numpy as np
from scipy.optimize import minimize

import unify_hyperbolic_bg_ub1b as M


WORKERS = mp.cpu_count()


def _score(p):
    return M.miss(M.solve(p, "C"))


def _polish(p0):
    r = minimize(lambda p: M.miss(M.solve(p, "C")), p0, method="Nelder-Mead",
                 options={"maxfev": 400, "xatol": 1e-3, "fatol": 1e-4})
    return float(r.fun), r.x


def search(var, nsamp=M.NSAMP, npol=M.NPOLISH, rng=None):
    assert var == "C"
    lo, hi = M.box(var)
    pts = lo + (hi - lo) * rng.random((nsamp, len(lo)))
    with mp.Pool(WORKERS) as pool:
        scores = pool.map(_score, list(pts), chunksize=50)
        scored = sorted(zip(scores, pts), key=lambda t: t[0])
        pol = pool.map(_polish, [p0 for _, p0 in scored[:npol]], chunksize=1)
    best = None
    for fun, x in pol:                                   # same order and stopping rule as the serial loop
        if best is None or fun < best[0]:
            best = (fun, x)
        if fun == 0:
            break
    d = M.solve(best[1], var)
    return {"variant": var, "samples": nsamp, "polished": npol, "best_miss": round(float(best[0]), 4),
            "best_params(lnA, lnL, th_i, phi_i[, kappa])": [round(float(x), 4) for x in best[1]],
            "best_point": {k: (round(v, 5) if isinstance(v, float) else v) for k, v in (d or {}).items()},
            "requirements": M.met(d), "ALL_MET": bool(best[0] == 0 and all(M.met(d).values()))}


if __name__ == "__main__":
    WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else mp.cpu_count()
    M.search = search
    M.main()
