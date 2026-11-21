import itertools, json, numpy as np
uu, ud = 1.793e-3, 2.587e-2; ub = max(uu, ud)
Q = [0, .5, 1, 1.5, 2, 2.5, 3]
mu = (5.58e-6, 2.69e-3); md = (6.86e-4, 1.37e-2); V = dict(us=0.2250, cb=0.0410, ub=0.00382)
w2 = lambda p, d: max(p / d, d / p) <= 2
w3 = lambda p, d: max(p / d, d / p) <= 3
fits = []; n = 0
for qQ1, qQ2, qu1, qu2, qd1, qd2 in itertools.product(Q, repeat=6):
    n += 1
    if not (w2(uu ** (qQ1 + qu1), mu[0]) and w2(uu ** (qQ2 + qu2), mu[1]) and w2(ud ** (qQ1 + qd1), md[0]) and w2(ud ** (qQ2 + qd2), md[1])): continue
    if w3(ub ** abs(qQ1 - qQ2), V['us']) and w3(ub ** qQ2, V['cb']) and w3(ub ** qQ1, V['ub']):
        fits.append(dict(qQ=(qQ1, qQ2, 0), qu=(qu1, qu2, 0), qd=(qd1, qd2, 0)))
f = len(fits) / n
v = 'NONE' if not fits else ('RARE-FIT' if f < 0.01 else 'COMMON')
out = dict(n=n, n_fit=len(fits), frac=f, verdict=v, fits=fits[:10])
print(json.dumps(out, indent=1)); json.dump(out, open('field_tests/results/d1828_chargescan.json', 'w'), indent=1)
