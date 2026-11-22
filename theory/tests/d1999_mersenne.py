#!/usr/bin/env python3
"""D1999 Mersenne exponent pattern analysis (PREREG_D1999_mersenne_pattern.md)."""
import json, math, random, sys
sys.path.insert(0, 'tools/loom'); import check as C
P = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011, 24036583, 25964951, 30402457, 32582657, 37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933, 136279841]
g = 0.5772156649015329; LPW = math.log(2) * math.exp(-g); PI8 = math.pi / 8
def isprime(n):
    if n < 2: return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0: return n == q
    d, r = n - 1, 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2, 3, 5, 7, 11, 13, 17):
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
def ks_exp(xs):
    xs = sorted(xs); n = len(xs); D = max(max((i + 1) / n - (1 - math.exp(-x)), (1 - math.exp(-x)) - i / n) for i, x in enumerate(xs))
    lam = (math.sqrt(n) + 0.12 + 0.11 / math.sqrt(n)) * D; p = 2 * sum((-1) ** (k - 1) * math.exp(-2 * k * k * lam * lam) for k in range(1, 100)); return D, max(0.0, min(1.0, p))
def chi2_p(x2, df):   # survival function via series (regularized gamma)
    a, x = df / 2.0, x2 / 2.0
    if x == 0: return 1.0
    s, t, k = 0.0, 1.0 / a, 0
    while k < 500: s += t; k += 1; t *= x / (a + k)
    return max(0.0, 1 - math.exp(-x + a * math.log(x) - math.lgamma(a)) * s)
def run(P, tag):
    L = [math.log(p) for p in P]; d = [b - a for a, b in zip(L, L[1:])]; n = len(d)
    m = sum(d) / n; sd = math.sqrt(sum((x - m) ** 2 for x in d) / (n - 1)); se = sd / math.sqrt(n)
    s = [x / LPW for x in d]; D, pks = ks_exp(s)
    out = dict(tag=tag, n_steps=n, mean_step=m, se=se, LPW=LPW, z_LPW=(m - LPW) / se, mean_ratio=math.exp(m), KS_D=D, KS_p=pks,
               B1=dict(pi8=PI8, z_pi8=(m - PI8) / se, diff_frac=(PI8 - LPW) / LPW, se_frac=se / m, verdict='NO-POWER' if abs(PI8 - LPW) < 2 * se else 'testable'))
    # B2-B4 residues vs control primes sampled log-uniformly over the same range
    random.seed(1999); ctrl = []
    lo, hi = math.log(max(P[0], 5)), math.log(P[-1])
    while len(ctrl) < 20000:
        q = int(math.exp(random.uniform(lo, hi)))
        while not isprime(q): q += 1
        ctrl.append(q)
    res = {}
    for M in (12, 24, 48):
        cls = sorted({q % M for q in ctrl}); exp_frac = {c: sum(1 for q in ctrl if q % M == c) / len(ctrl) for c in cls}
        obs = {c: sum(1 for p in P if p > 3 and p % M == c) for c in cls}; N = sum(obs.values())
        x2 = sum((obs[c] - N * exp_frac[c]) ** 2 / (N * exp_frac[c]) for c in cls); df = len(cls) - 1
        res['mod%d' % M] = dict(chi2=x2, df=df, p=chi2_p(x2, df), observed={str(c): obs[c] for c in cls})
    out['B2_B4'] = res
    # B5 arrows: lag-1 autocorrelation + runs test
    ms = sum(s) / n; ac = sum((s[i] - ms) * (s[i + 1] - ms) for i in range(n - 1)) / sum((x - ms) ** 2 for x in s)
    signs = [x > 1 for x in s]; n1 = sum(signs); n2 = n - n1; runs = 1 + sum(1 for a, b in zip(signs, signs[1:]) if a != b)
    mu = 2 * n1 * n2 / n + 1; var = 2 * n1 * n2 * (2 * n1 * n2 - n) / (n * n * (n - 1)); zr = (runs - mu) / math.sqrt(var)
    pr = math.erfc(abs(zr) / math.sqrt(2)); pac = math.erfc(abs(ac) * math.sqrt(n) / math.sqrt(2))
    out['B5'] = dict(lag1_autocorr=ac, p_autocorr=pac, runs=runs, runs_expected=mu, z_runs=zr, p_runs=pr)
    # B6 close pairs
    q = 1 - math.exp(-math.log(1.1) / LPW); k = sum(1 for x in d if x < math.log(1.1))
    pb = sum(math.comb(n, j) * q ** j * (1 - q) ** (n - j) for j in range(k, n + 1))
    out['B6'] = dict(close_pairs=k, expected=n * q, p_upper=pb)
    raw = [res['mod12']['p'], res['mod24']['p'], res['mod48']['p'], pac, pr, pb]
    out['min_raw_p'] = min(raw); out['bonferroni_hit'] = min(raw) < 0.01 / 6
    return out
A = run(P, 'all 52'); B = run(P[:51], 'verified 51'); Cc = run(P[12:], 'drop first 12')
num = C.c4_numerology(math.exp(A['mean_step']), A['se'], [math.exp(PI8), math.exp(LPW), math.sqrt(2), 1.5, (1 + 5 ** 0.5) / 2 - 0.1])
verdict = 'PATTERN BEYOND LPW' if (A['bonferroni_hit'] and Cc['bonferroni_hit']) else 'CONSISTENT WITH LPW RANDOM MODEL; no Weave pattern supported'
out = dict(prereg='PREREG_D1999_mersenne_pattern.md', all52=A, verified51=B, drop12=Cc, numerology=num[1], verdict=verdict)
json.dump(out, open('field_tests/results/d1999_mersenne.json', 'w'), indent=1); print(json.dumps(out, indent=1))
