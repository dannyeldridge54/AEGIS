#!/usr/bin/env python3
"""D2127: builder-side diff of engine (z2z6p.py, P2) vs referee blind implementation output."""
import json, os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z2z6p as Z
d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'referee_blind', 'blind_out.json')))
pm = lambda s: tuple(0 if c == '+' else 1 for c in s)
B = {'a': ((0,1,1,0,1,-1), '+++', (0,0,1), (1,1,1)), 'b': ((0,1,1,0,1,-1), '--+', (0,1,1), (1,1,1)), 'c': ((0,1,1,0,1,-1), '-+-', (1,0,1), (1,1,1)),
     'd': ((-1,2,2,-1,1,-1), '--+', (0,0,1), (1,1,1)), 'e': ((1,0,1,0,1,0), '+--', (1,1,1), (1,1,0)),
     'r1': ((1,0,1,0,1,0), '-+-', (1,0,0), (0,1,1)), 'r2': ((1,1,0,1,1,-1), '+--', (0,1,0), (1,0,1)), 'r3': ((-1,2,1,1,2,-1), '++-', (1,1,0), (0,0,1))}
C = {k: (lambda X, Y: (X, Y, Z.exceptional(w, pm(z), t, s, 'P2')))(*Z.XY(w)) for k, (w, z, t, s) in B.items()}
I = {k: Z.image(*C[k]) for k in B}
flat = lambda c: [c[0], c[1]] + [[c[2][k][a][0], c[2][k][a][1]] for k in (1, 2, 3) for a in range(1, 6)]
diff = [k for k in B if flat(C[k]) != d['cycles'][k]]
chi_diff = []
for key, v in d['chi_random'].items():
    x, y = key.split('.'); cy = I[y.rstrip("'")] if y.endswith("'") else C[y]
    if str(Z.chi(C[x], cy)) != v: chi_diff.append((key, v, str(Z.chi(C[x], cy))))
print('cycle-vector differences:', diff, '| random-brane chi differences:', chi_diff)
print('blind T27 chi:', d['chi_T27']); print('VERDICT', 'PASS' if not diff and not chi_diff else 'FAIL')
