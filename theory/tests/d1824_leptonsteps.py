import math, json, numpy as np
c = math.pi * (math.sqrt(3) / 2) * 1458 / 162 ** 2; s = 1 / 6; N = 13
e = lambda n: math.exp(-c * (n + s) ** 2)
def triples(r1, r2, tol=0.1):
    out = []
    for a in range(N):
        for b in range(a + 1, N):
            if abs(e(b) / e(a) / r1 - 1) > tol: continue
            for d in range(b + 1, N):
                if abs(e(d) / e(b) / r2 - 1) <= tol: out.append((a, b, d))
    return out
T = triples(0.0595, 4.84e-3)
R = np.array([e(b) / e(a) for a in range(N) for b in range(a + 1, N)])
rng = np.random.default_rng(9); X = np.exp(rng.uniform(math.log(1e-4), 0, 20000))
f = float(np.mean(np.any(np.abs(X[:, None] / R[None, :] - 1) <= 0.1, axis=1)))
P = np.exp(rng.uniform(math.log(1e-4), 0, (3000, 2))); f2 = float(np.mean([bool(triples(p[0], p[1])) for p in P]))
v = ('SIGNAL' if f2 < 0.01 else 'HIT-BUT-VACUOUS') if T else 'MISS'
out = dict(c=c, triples=T, ratios_of_triples=[[e(b) / e(a), e(d) / e(b)] for a, b, d in T], coverage_single=f, coverage_pair=f2, verdict=v)
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1824_leptonsteps.json', 'w'), indent=1)
