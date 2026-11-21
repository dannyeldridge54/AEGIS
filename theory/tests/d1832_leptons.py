import numpy as np, math, cmath, json
qL, qe = np.array([.5, 0, 0]), np.array([1.5, 1, 0]); E = qL[:, None] + qe[None, :]
rng = np.random.default_rng(32)
def f(u):
    ok = 0
    for _ in range(4000):
        C = np.exp(rng.uniform(math.log(.5), math.log(2), (3, 3))) * np.exp(1j * rng.uniform(0, 2 * math.pi, (3, 3)))
        s = np.sort(np.linalg.svd(C * u ** E, compute_uv=False))
        r1, r2 = s[0] / s[2], s[1] / s[2]
        ok += max(r1 / 2.88e-4, 2.88e-4 / r1) <= 3 and max(r2 / 5.95e-2, 5.95e-2 / r2) <= 3
    return ok / 4000
grid = np.logspace(-5, math.log10(0.3), 26); res = [(float(g), f(g * cmath.exp(-1j * math.radians(40)))) for g in grid]
best = max(res, key=lambda r: r[1]); fd = f(0.0259 * cmath.exp(-1j * math.radians(40)))
v = 'NATURAL' if best[1] >= 0.05 else 'TUNED' if best[1] > 0 else 'NO-FIT'
out = dict(scan=res, best_u=best[0], f_max=best[1], f_at_u_d=fd, verdict=v, koide_compatible=best[0] <= 3.5e-5)
print(json.dumps({k: out[k] for k in ('best_u', 'f_max', 'f_at_u_d', 'verdict', 'koide_compatible')}, indent=1)); json.dump(out, open('field_tests/results/d1832_leptons.json', 'w'), indent=1)
