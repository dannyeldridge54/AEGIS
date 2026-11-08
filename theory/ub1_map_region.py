"""UB-1 map (exploratory, no verdict): where in variant B's box are ALL four UB-1 requirements met (UB-1 D1 code)?
A random walk restricted to the passing set (accept a step only if R2-R5 are all met), started at the UB-1 D1
passing point, plus 400 fresh random starts polished as in UB-1, to find other islands. Output: the passing points
and the 5-95% range of what they predict (F during the boost, z of the peak, f_peak, w0, kappa, |phi| today).
The ranges are then written as predictions for UB-2 and locked BEFORE any UB-2 result is read.
    python ub1_map_region.py [steps]   -> ub1_map_region.json"""
import json
import sys

import numpy as np
from scipy.optimize import minimize

import unify_hyperbolic_bg_v2 as M

START = np.array([1.2391, 22.6974, 2.426, 12.4076, -0.1452])     # UB-1 D1 variant B passing point
STEP = np.array([0.3, 0.15, 0.03, 0.3, 0.02])


def ok(p):
    d = M.solve(p, "B")
    return d is not None and M.miss(d) == 0, d


def main():
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
    rng = np.random.default_rng(20261108)
    lo, hi = M.box("B")
    pts, rows = [], []
    good, d = ok(START)
    assert good, "start point must pass"
    x = START.copy()
    acc = 0
    for i in range(steps):
        y = x + STEP * rng.standard_normal(5)
        if np.all(y >= lo) and np.all(y <= hi):
            g, dy = ok(y)
            if g:
                x, d = y, dy
                acc += 1
        pts.append(x.copy()); rows.append(d)
    islands = []
    for p0 in lo + (hi - lo) * rng.random((400, 5)):
        r = minimize(lambda p: M.miss(M.solve(p, "B")), p0, method="Nelder-Mead",
                     options={"maxfev": 300, "xatol": 1e-3, "fatol": 1e-4})
        if r.fun == 0:
            islands.append([round(float(v), 4) for v in r.x])
    keys = ["F_at_peak", "z_peak", "f_peak", "w0", "phi_today", "F_today", "f_1090"]
    q = lambda a: [round(float(np.percentile(a, 5)), 4), round(float(np.percentile(a, 50)), 4), round(float(np.percentile(a, 95)), 4)]
    P = np.array(pts)
    out = {"what": "UB-1 variant B passing region (exploratory map; predictions locked separately)",
           "walk_steps": steps, "accept_rate": round(acc / steps, 3),
           "ranges_5_50_95": {k: q([r[k] for r in rows]) for k in keys},
           "params_5_50_95": {n: q(P[:, i]) for i, n in enumerate(["lnA", "lnL", "theta_i", "phi_i", "kappa"])},
           "other_islands_from_400_random_starts": islands}
    json.dump(out, open("ub1_map_region.json", "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print(json.dumps(out, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))


if __name__ == "__main__":
    main()
