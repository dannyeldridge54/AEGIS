import math, json, numpy as np
from scipy.stats import poisson
T = []
for m in (1, 2, 5, 13):
    mu = (3 * m + math.sqrt(9 * m * m - 4)) / 2; T += [('mu%d' % m, mu), ('sqrt_mu%d' % m, math.sqrt(mu)), ('len%d' % m, 2 * math.log(mu))]
C = dict(lambda_eff=20.15 / 6, sd_over_sv=2.0, r6_over_r10=1.07e-3 / 5.41e-4, inv_x=1 / 0.279, A=7.298, dB=2.879,
         gluino_over_wino=5565 / 680, alpha_inv=28.0, m32_over_M2=2.61e5 / 680, Nd_over_N=2.0)
hits = [(c, t, v, tv, v / tv - 1) for c, v in C.items() for t, tv in T if abs(v / tv - 1) <= 0.01]
rng = np.random.default_rng(5); X = np.exp(rng.uniform(0, math.log(400), 200000))
tv = np.array([v for _, v in T]); p1 = float(np.mean(np.any(np.abs(X[:, None] / tv[None, :] - 1) <= 0.01, axis=1)))
exp_hits = len(C) * p1; pval = float(poisson.sf(len(hits) - 1, exp_hits)) if hits else 1.0
out = dict(targets=T, hits=hits, p1=p1, expected=exp_hits, observed=len(hits), poisson_p=pval, verdict='SIGNAL' if pval < 0.01 else 'NO SIGNAL')
print(json.dumps(out, indent=1, default=str)); json.dump(out, open('field_tests/results/d1819_markovratios.json', 'w'), indent=1, default=str)
