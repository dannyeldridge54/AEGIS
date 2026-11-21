import math, json
from scipy.optimize import brentq
W0 = 1.4e-8
def x_of(A): return brentq(lambda x: math.log(A) - x + math.log(1 + 2 * x / 3) - math.log(W0), 0.1, 60)
xs = {A: x_of(A) for A in (1, 30)}
rows = []
for N in range(2, 41):
    lo, hi = sorted(N * xs[A] / (2 * math.pi) for A in (1, 30))
    if hi >= 36.9 and lo <= 40.6: rows.append(dict(N_d=N, sigma=[lo, hi], alphaD_inv_Ms=[lo, hi]))
A_vis = brentq(lambda A: 7 * x_of(A) / (2 * math.pi) - 20.15, 1e-4, 1e4)
out = dict(x_A1=xs[1], x_A30=xs[30], allowed=rows, A_needed_visible=A_vis,
           verdict='UNIQUE' if len([r for r in rows if r['N_d'] <= 30]) == 1 else 'STABILISABLE' if any(r['N_d'] <= 30 for r in rows) else 'NOT')
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1810_darkstab.json', 'w'), indent=1)
