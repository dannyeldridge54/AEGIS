#!/usr/bin/env python3
"""D2110: full positive control of the Table-27 global Pati-Salam model (1209.3010) on Z2xZ6' AAA."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z2z6p as Z
pm = lambda s: tuple(0 if c == '+' else 1 for c in s)
T27 = {'a': (4, (0,1,1,0,1,-1), '+++', (0,0,1), (1,1,1)), 'b': (2, (0,1,1,0,1,-1), '--+', (0,1,1), (1,1,1)),
       'c': (2, (0,1,1,0,1,-1), '-+-', (1,0,1), (1,1,1)), 'd': (2, (-1,2,2,-1,1,-1), '--+', (0,0,1), (1,1,1)),
       'e': (2, (1,0,1,0,1,0), '+--', (1,1,1), (1,1,0))}
TARGET = {('a','b'): 1, ('a',"b'"): 2, ('a','c'): -1, ('a',"c'"): -2, ('b','c'): 1, ('b','d'): 1, ('b',"d'"): -3, ('b',"e'"): -1,
          ('c','d'): -1, ('c',"d'"): 3, ('c',"e'"): 1}
for jk in ('P1', 'P2'):
    cyc = {}
    for k, (N, w, z2, tau, sig) in T27.items():
        X, Y = Z.XY(w); ex = Z.exceptional(w, pm(z2), tau, sig, jk); cyc[k] = (X, Y, ex); cyc[k + "'"] = Z.image(X, Y, ex)
    bulk, res = Z.tadpoles([(T27[k][0], cyc[k]) for k in 'abcde'])
    got = {}
    for x, y in [(p, q) for p in 'abcde' for q in 'abcde' if p < q] + [(p, q + "'") for p in 'abcde' for q in 'abcde' if p <= q]:
        v = Z.chi(cyc[x], cyc[y])
        if v: got[(x, y)] = v
    for sgn in (1, -1):
        match = all(got.get(kk, 0) == sgn*v for kk, v in TARGET.items()) and all(kk in TARGET or kk[0] == kk[1].rstrip("'") for kk in got)
        print('%s sign %+d: bulk %d (32) | twisted residuals nonzero: %d of %d | chirality match: %s' % (jk, sgn, bulk, sum(1 for r in res if r), len(res), match))
    print('   chi found:', {"%s%s" % k: str(v) for k, v in got.items()})
