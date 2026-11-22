#!/usr/bin/env python3
"""D2004: Rodin digit rules as filters on Mersenne exponents (PREREG_D2004). Baseline: matched random primes."""
import json, math, random, sys
from collections import Counter
from sympy import randprime
from scipy.stats import chisquare, mannwhitneyu, chi2_contingency
sys.path.insert(0, 'theory/tests'); from d1999_mersenne import P
random.seed(2004)
import sympy; sympy.core.random.seed(2004)
dr = lambda n: 0 if n == 0 else 1 + (n - 1) % 9
CIRC = [1, 2, 4, 8, 7, 5]; AXIS = {3, 6, 9}
base = []
for p in P:
    lo, hi = (2, 100) if p < 50 else (p // 2, 2 * p)
    base.append([randprime(lo, hi) for _ in range(400)])
B = [q for b in base for q in b]
out = {'n_mersenne': len(P), 'n_baseline': len(B)}; pv = {}
# R1
out['R1'] = {'mersenne_pass': sum(dr(p) in CIRC for p in P) / len(P), 'baseline_pass': sum(dr(q) in CIRC for q in B) / len(B)}
# R2 circuit position (p > 3)
M2 = Counter(dr(p) for p in P if p > 3); B2 = Counter(dr(q) for q in B if q > 3)
exp = [B2[c] / sum(B2.values()) * sum(M2.values()) for c in CIRC]; obs = [M2[c] for c in CIRC]
pv['R2'] = chisquare(obs, exp).pvalue; out['R2'] = {'obs': dict(zip(CIRC, obs)), 'exp': [round(e, 1) for e in exp], 'p': pv['R2']}
# R3 digital root of 2^p - 1 via pow mod 9
r3 = lambda p: dr((pow(2, p, 9) - 1) % 9 or 9)
M3 = Counter(r3(p) for p in P if p > 3); B3 = Counter(r3(q) for q in B if q > 3); keys = sorted(set(M3) | set(B3))
exp = [B3[k] / sum(B3.values()) * sum(M3.values()) for k in keys]; obs = [M3[k] for k in keys]
pv['R3'] = chisquare(obs, exp).pvalue; out['R3'] = {'roots_seen': keys, 'obs': dict(zip(keys, obs)), 'exp': [round(e, 1) for e in exp], 'p': pv['R3']}
# R4 / R5 layer fractions
frac = lambda n, S: sum(int(c) in S for c in str(n)) / len(str(n))
for tag, S in (('R4_axis369', AXIS), ('R5_circuit', set(CIRC))):
    a = [frac(p, S) for p in P if p >= 10]; b = [frac(q, S) for q in B if q >= 10]
    pv[tag] = mannwhitneyu(a, b).pvalue; out[tag] = {'mersenne_mean': sum(a) / len(a), 'baseline_mean': sum(b) / len(b), 'p': pv[tag]}
# L1 Benford leading digit
ben = [math.log10(1 + 1 / d) for d in range(1, 10)]
ML = Counter(int(str(p)[0]) for p in P); obs = [ML[d] for d in range(1, 10)]
out['L1'] = {'obs': obs, 'benford_exp': [round(b * len(P), 1) for b in ben], 'p_vs_benford': chisquare(obs, [b * len(P) for b in ben]).pvalue}
BL = Counter(int(str(q)[0]) for q in B); tab = [obs, [BL[d] for d in range(1, 10)]]
pv['L1_vs_baseline'] = chi2_contingency(tab).pvalue; out['L1']['p_vs_baseline'] = pv['L1_vs_baseline']
# L2 lower layers
out['L2'] = {}
for k in range(1, 9):
    vals = [int(str(p)[k]) for p in P if len(str(p)) > k]
    if len(vals) < 20: continue
    c = Counter(vals); o = [c[d] for d in range(10)]
    if k == len(str(min(p for p in P if len(str(p)) > k))) - 1: pass
    pv['L2_layer%d' % (k + 1)] = chisquare(o).pvalue; out['L2']['layer%d_from_left' % (k + 1)] = {'n': len(vals), 'obs': o, 'p': pv['L2_layer%d' % (k + 1)]}
# ones digit (rightmost layer) vs baseline (primes end in 1,3,7,9)
MO = Counter(p % 10 for p in P if p > 5); BO = Counter(q % 10 for q in B if q > 5); ks = [1, 3, 7, 9]
pv['L2_ones_vs_baseline'] = chisquare([MO[k] for k in ks], [BO[k] / sum(BO.values()) * sum(MO.values()) for k in ks]).pvalue
out['L2']['ones_digit'] = {'obs': {k: MO[k] for k in ks}, 'p_vs_baseline': pv['L2_ones_vs_baseline']}
m = len(pv); out['bonferroni'] = {'m': m, 'alpha': 0.05 / m, 'min_p': min(pv.values()), 'min_test': min(pv, key=pv.get), 'any_pass': min(pv.values()) < 0.05 / m}
out['layers_of_record'] = {'p': P[-1], 'layers_ones_up': [int(c) for c in str(P[-1])[::-1]], 'digital_root_p': dr(P[-1]), 'digital_root_Mp': r3(P[-1]), 'p_mod6': P[-1] % 6}
json.dump(out, open('field_tests/results/d2004_rodin.json', 'w'), indent=1, default=float); print(json.dumps(out, indent=1, default=float))
