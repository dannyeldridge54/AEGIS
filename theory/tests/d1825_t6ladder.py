import math, json, numpy as np, itertools
cr, ci, s = 0.1511, math.pi / 8, 1 / 6
labs = list(itertools.product(range(7), repeat=3))
L = np.array([cr * (a + s) ** 2 + ci * b * b + ci * c * c for a, b, c in labs])   # -ln coupling
L = np.unique(np.round(L, 9))
def hit(r1, r2, tol=0.1):
    t1, t2 = -math.log(r1), -math.log(r2); w = math.log(1 + tol)
    for x in L:
        y = L[np.abs(L - x - t1) <= w]
        if len(y) and np.any(np.abs(L[None, :] - y[:, None] - t2) <= w): return True
    return False
h = hit(0.0595, 4.84e-3)
rng = np.random.default_rng(13); P = np.exp(rng.uniform(math.log(1e-4), 0, (2000, 2)))
f2 = float(np.mean([hit(p[0], p[1]) for p in P]))
v = ('SIGNAL' if f2 < 0.01 else 'HIT-BUT-VACUOUS') if h else 'MISS'
out = dict(distinct_levels=int(len(L)), hit=h, coverage_pair=f2, verdict=v)
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1825_t6ladder.json', 'w'), indent=1)
