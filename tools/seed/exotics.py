#!/usr/bin/env python3
"""D2096: enumerate every hidden completion of each D2083 PS point; keep those with no hidden-visible chiral intersections."""
import json, os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seed_v3 as s
from fractions import Fraction as Fr
pts = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seed_v4_results.json')))['points']
def completions(S, chi, R, par):
    c12, c13, c23 = chi[0]*chi[1], chi[0]*chi[2], chi[1]*chi[2]; W = lambda x: x[0] - c23*x[1] - c13*x[2] - c12*x[3]
    XB = [s.X(w) for w in S]; PB = [s.parity(w) for w in S]; out = []
    def rec(i, R, par, acc):
        if i == len(S):
            if all(r == 0 for r in R) and par == (0, 0, 0, 0): out.append(acc)
            return
        c = 0
        while 2*c*W(XB[i]) <= W(R):
            rec(i + 1, tuple(r - 2*c*x for r, x in zip(R, XB[i])), tuple((p + c*q) % 2 for p, q in zip(par, PB[i])), acc + (((2*c, S[i]),) if c else ())); c += 1
    rec(0, R, par, ()); return out
res = []
for p in pts:
    chi = tuple(Fr(x) for x in p['chi']); A, B, C = (tuple(p[k]) for k in 'ABC')
    S = [w for w in s.ALL if s.zprod(w, chi)[1] == 0 and s.zprod(w, chi)[0] > 0]
    R = tuple(t - 8*xa - 4*xb - 4*xc for t, xa, xb, xc in zip(s.TGT, s.X(A), s.X(B), s.X(C)))
    comps = completions(S, chi, R, s.kcheck([(8, A), (4, B), (4, C)]))
    free = [cm for cm in comps if all(s.inter(h, v) == 0 and s.inter(h, v, True) == 0 for _, h in cm for v in (A, B, C))]
    res.append(dict(chi=p['chi'], W=p['W'], alpha_s=p['alpha_s'], completions=len(comps), exotic_free=len(free),
                    example=[(N, list(w)) for N, w in free[0]] if free else None))
    print('chi %-14s W %-16s completions %2d  exotic-free %2d  alpha_s %s' % (p['chi'], p['W'], len(comps), len(free), p['alpha_s'] and round(p['alpha_s'], 4)))
u = [r for r in res if r['W'] == ['6', '6', '6']]
print('VERDICT (unified model):', 'PASS' if any(r['exotic_free'] for r in u) else 'FAIL')
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exotics_results.json'), 'w'), indent=1)
