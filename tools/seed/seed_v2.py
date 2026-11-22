#!/usr/bin/env python3
"""Seed engine v2 (PREREG D2080): seed = CSU SUSY 3-family model (hep-th/0107143 Table I, T6/(Z2xZ2), tilted T3, mt = m - n/2).
Step 1 calibrates (tadpoles, SUSY, 3 left quarks); step 2 spins rings k=1,2 (k integer wrappings changed by +-1) through the hard filters.
Run: python3 seed_v2.py  -> prints and writes seed_v2_results.json"""
import itertools, json, math, os
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import least_squares
H = Fr(1, 2)
# stacks: name, N, integer wrappings (n1,m1,n2,m2,n3,m3) with m3 integer; mt3 = m3 - n3/2
SEED = [('A1', 8, (0, 1, 0, -1, 2, 1)), ('A2', 2, (1, 0, 1, 0, 2, 1)), ('B1', 4, (1, 0, 1, -1, 1, 2)),
        ('B2', 2, (1, 0, 0, 1, 0, -1)), ('C1', 8, (1, -1, 1, 0, 1, 1)), ('C2', 4, (0, 1, 1, 0, 0, -1))]
def tor(w):  return [(Fr(w[0]), Fr(w[1])), (Fr(w[2]), Fr(w[3])), (Fr(w[4]), Fr(w[5]) - Fr(w[4]) * H)]
def tadpoles(S):
    t = [0, 0, 0, 0]
    for _, N, w in S:
        (a, b), (c, d), (e, f) = tor(w)
        t[0] += N*a*c*e; t[1] += N*a*d*f; t[2] += N*b*c*f; t[3] += N*b*d*e
    return t
TARGET = [16, -8, -8, -16]
def angsum(S, chi):
    r = []
    for _, N, w in S:
        s = sum(math.atan2(chi[i]*float(m), float(n)) for i, (n, m) in enumerate(tor(w)))
        r.append((s + math.pi) % (2*math.pi) - math.pi)
    return np.array(r)
def susy(S):
    best = None
    for x0 in itertools.product((-1.0, 0.0, 1.0), repeat=3):
        sol = least_squares(lambda lx: angsum(S, np.exp(lx)), np.array(x0), xtol=1e-15, ftol=1e-15, gtol=1e-15)
        res = float(np.max(np.abs(angsum(S, np.exp(sol.x)))))
        if best is None or res < best[0]: best = (res, np.exp(sol.x))
        if res < 1e-12: break
    return best
def inter(wa, wb, image=False):
    p = Fr(1)
    for (na, ma), (nb, mb) in zip(tor(wa), tor(wb)):
        if image: mb = -mb
        p *= na*mb - ma*nb
    return p
def quarks(S):
    d = {s[0]: s[2] for s in S}; return abs(inter(d['C1'], d['B1'])) + abs(inter(d['C1'], d['B1'], True))
def canon(S):
    out = []
    for name, N, w in S:
        T = tor(w); forms = []
        for img in (1, -1):
            for flips in [(1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)]:
                forms.append(tuple((f*n, f*img*m) for f, (n, m) in zip(flips, T)))
        out.append((N, min(forms)))
    return tuple(sorted(out))
def check(S):
    tp = tadpoles(S); ok_t = tp == TARGET
    q = quarks(S); r = susy(S) if ok_t else (None, None)
    ok_s = ok_t and r[0] < 1e-8
    return dict(tadpoles=[str(x) for x in tp], tadpole_ok=ok_t, susy_res=r[0], chi=None if r[1] is None else [round(float(x), 6) for x in r[1]],
                susy_ok=ok_s, quarks=str(q), quark_ok=(q == 3), passes=ok_t and ok_s and q == 3)
def ring(k):
    slots = [(i, j) for i in range(len(SEED)) for j in range(6)]; seen = set(); surv = []; n = 0; c0 = canon(SEED)
    for pos in itertools.combinations(slots, k):
        for sg in itertools.product((1, -1), repeat=k):
            S = [list(s) for s in SEED]; W = [list(s[2]) for s in SEED]
            for (i, j), s in zip(pos, sg): W[i][j] += s
            S = [(s[0], s[1], tuple(W[i])) for i, s in enumerate(SEED)]
            if any(all(x == 0 for x in w[2*t:2*t+2]) for _, _, w in S for t in range(3)): continue   # (0,0) on a torus is not a brane
            n += 1; r = check(S)
            if r['passes']:
                c = canon(S)
                if c in seen: continue
                seen.add(c); surv.append(dict(changes=[[SEED[i][0], j, s] for (i, j), s in zip(pos, sg)], same_as_seed=(c == c0), **r))
    return dict(k=k, configs=n, survivors=len(surv), new=sum(not s['same_as_seed'] for s in surv), list=surv)
if __name__ == '__main__':
    cal = check(SEED); print('CALIBRATION:', cal)
    out = {'calibration': cal}
    if not cal['passes']: print('STOP: calibration failed (PREREG D2080 step 1).')
    else:
        for k in (1, 2):
            R = ring(k); out['ring%d' % k] = R
            print('ring k=%d: configs %d, survivors %d (distinct), new (not seed-equivalent) %d' % (k, R['configs'], R['survivors'], R['new']))
            for s in R['list'][:6]: print('   ', s['changes'], 'chi', s['chi'], 'seed-equiv' if s['same_as_seed'] else 'NEW')
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seed_v2_results.json'), 'w'), indent=1, default=str)
