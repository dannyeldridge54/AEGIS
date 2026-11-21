import numpy as np, math, cmath, json
qL, qe = np.array([.5, 0, 0]), np.array([1.5, 1, 0]); E = qL[:, None] + qe[None, :]
u = 0.0259 * cmath.exp(-1j * math.radians(40)); UE = u ** E
rng = np.random.default_rng(37); N = 200000; B = 20000
fit = 0; k1 = 0; k2 = 0
for _ in range(N // B):
    C = np.exp(rng.uniform(math.log(.5), math.log(2), (B, 3, 3))) * np.exp(1j * rng.uniform(0, 2 * math.pi, (B, 3, 3)))
    s = np.sort(np.linalg.svd(C * UE[None], compute_uv=False), axis=1)
    r1, r2 = s[:, 0] / s[:, 2], s[:, 1] / s[:, 2]
    ok = (np.maximum(r1 / 2.88e-4, 2.88e-4 / r1) <= 3) & (np.maximum(r2 / 5.95e-2, 5.95e-2 / r2) <= 3)
    Q = s.sum(1) / np.sqrt(s).sum(1) ** 2
    fit += ok.sum(); k1 += (ok & (np.abs(Q - 2 / 3) <= 2e-5)).sum(); k2 += (ok & (np.abs(Q - 2 / 3) <= 1e-3)).sum()
out = dict(n_fit=int(fit), P_2e5=k1 / fit, P_1e3=k2 / fit, verdict='Koide is a <1e-3 accident under B' if k1 / fit < 1e-3 else 'Koide plausible under B')
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1837_koideodds.json', 'w'), indent=1)
