"""Table of (w0, wa) along the full-tail curve vs heat share f (Development 78b), for the TAIL-F test. Model only, no data.
Uses tail_full_thaw.solve (Omega_m 0.31 fixed; CPL fit over z < 2). AI-assisted."""
import json, math, sys
sys.path.insert(0, "theory/darkenergy")
from tail_freeze import run
from tail_full_thaw import solve, c, n, m2, mu
rows = []
for f in [1e-4, 2e-4, 4e-4, 6e-4, 8e-4, 1.0e-3, 1.3e-3, 1.6e-3, 2.0e-3, 2.5e-3]:
    xf = run(mu, n=n, m2=m2, f=f)[0]; w0, wa, wt, xt = solve(math.log(xf) / c)
    rows.append({"f": f, "x_f": xf, "w0": w0, "wa": wa}); print(rows[-1], flush=True)
json.dump(rows, open("field_tests/results/tail_curve_table.json", "w"), indent=1)
