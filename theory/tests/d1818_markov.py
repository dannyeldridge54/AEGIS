import numpy as np, math, cmath, json
MARKOV = [1, 2, 5, 13, 29, 34, 89, 169, 194, 233]
def axes(t, C=60):
    out = []
    for c in range(1, C + 1):
        for a in range(-3 * C - t, 3 * C + t + 1):
            d = t - a; n = a * d - 1
            if n % c: continue
            b = n // c
            disc = (d - a) ** 2 + 4 * b * c
            if disc <= 0: continue
            r1, r2 = ((a - d) + math.sqrt(disc)) / (2 * c), ((a - d) - math.sqrt(disc)) / (2 * c)
            out.append(((r1 + r2) / 2, abs(r1 - r2) / 2))
    return np.array(out)
AX = {m: axes(3 * m) for m in MARKOV}
def dist(z, A):
    x, y = z.real, z.imag
    s = np.abs((x - A[:, 0]) ** 2 + y ** 2 - A[:, 1] ** 2) / (2 * A[:, 1] * y)
    return float(np.arcsinh(s.min()))
rho = complex(0.5, math.sqrt(3) / 2)
pts = {'rho': rho, 'i': 1j, 'tau_nu': 1.0685j, 'tau_d': rho + 0.0457 * cmath.exp(1j * math.radians(49)), 'tau_u': rho + 0.00311 * cmath.exp(1j * math.radians(50))}
rng = np.random.default_rng(3); R = []
while len(R) < 20000:     # hyperbolic measure dx dy / y^2 on the fundamental domain
    x = rng.uniform(-0.5, 0.5); y = 1 / rng.uniform(1e-6, 1)   # density ~ 1/y^2 for y >= 1
    if x * x + y * y >= 1: R.append(complex(x, y))
    else:
        y2 = rng.uniform(math.sqrt(1 - x * x), 1)
        if rng.uniform() < (1 / y2 ** 2) / (1 / (1 - x * x)): R.append(complex(x, y2))
out = {}
for name, z in pts.items():
    row = {}
    for m in MARKOV:
        d = dist(z, AX[m]); p = float(np.mean([dist(r, AX[m]) <= d for r in R[:4000]])) if d > 1e-9 else 0.0
        row[str(m)] = dict(d=d, p=p)
    best = min(row.items(), key=lambda kv: kv[1]['d'])
    on = best[1]['d'] <= 0.01 and best[1]['p'] < 0.002
    out[name] = dict(best_m=int(best[0]), best_d=best[1]['d'], p=best[1]['p'], identity=best[1]['d'] < 1e-9, verdict='ON' if on else 'OFF', all=row)
    print(name, 'best m', best[0], 'd=%.4g p=%.4g' % (best[1]['d'], best[1]['p']), out[name]['verdict'], '(identity)' if out[name]['identity'] else '')
json.dump(out, open('field_tests/results/d1818_markov.json', 'w'), indent=1)
