#!/usr/bin/env python3
"""O6 (D1984): online FDR control across the Loom's rounds: LORD++ (Javanmard & Montanari 2015; Ramdas et al. 2017).
Each PASS-type claim the Loom makes over time is a test with a p-value; LORD++ spends alpha-wealth so that the false discovery
rate over the whole stream stays <= alpha, whenever the tests are made. Usage: lord_pp(pvalues, alpha=0.05, w0=None) -> (rejections, alphas)."""
import math
def gamma_seq(n):
    g = [0.0718 * math.log(max(j, 2)) / (j * math.exp(math.sqrt(math.log(j)))) if j >= 1 else 0 for j in range(1, n + 1)]
    s = sum(g); return [x / s for x in g] if s > 0 else g
def lord_pp(p, alpha=0.05, w0=None):
    n = len(p); w0 = alpha / 2 if w0 is None else w0; g = gamma_seq(n); rej = []; alphas = []; taus = []
    for t in range(n):
        a = g[t] * w0
        if taus: a += (alpha - w0) * g[t - taus[0]] if t - taus[0] - 1 >= 0 else 0
        a += alpha * sum(g[t - tj - 1] for tj in taus[1:] if t - tj - 1 >= 0)
        alphas.append(a); r = p[t] <= a; rej.append(r)
        if r: taus.append(t)
    return rej, alphas
if __name__ == '__main__':   # self-test (locked bar): all-null streams of length 100, 2000 sims: FDR (= FWER here) <= 0.05
    import random
    random.seed(1984); bad = 0
    for _ in range(2000):
        r, _a = lord_pp([random.random() for _ in range(100)]); bad += any(r)
    fwer = bad / 2000; print('all-null FDR (=FWER) %.4f  bar <= 0.05  %s' % (fwer, 'PASS' if fwer <= 0.05 else 'FAIL'))
    random.seed(7); hits = 0
    for _ in range(500):
        p = [random.random() * 1e-4 if i % 5 == 0 else random.random() for i in range(100)]; r, _a = lord_pp(p); hits += sum(r[i] for i in range(0, 100, 5)) / 20
    print('power with 20 strong signals: %.2f' % (hits / 500))
