#!/usr/bin/env python3
"""D2109: bulk X, Y (1209.3010 Eq 9), AAA SUSY and bulk tadpole for the Table-27 Pati-Salam model, two readings of the sum."""
import itertools, math
ST = {'a': (4, (0, 1, 1, 0, 1, -1)), 'b': (2, (0, 1, 1, 0, 1, -1)), 'c': (2, (0, 1, 1, 0, 1, -1)), 'd': (2, (-1, 2, 2, -1, 1, -1)), 'e': (2, (1, 0, 1, 0, 1, 0))}
def XY(w, mode):
    n = (w[0], w[2], w[4]); m = (w[1], w[3], w[5])
    idx = [(0, 1, 2), (1, 2, 0), (2, 0, 1)] if mode == 'R1' else list(itertools.permutations(range(3)))
    X = n[0]*n[1]*n[2] - m[0]*m[1]*m[2] - sum(n[i]*m[j]*m[k] for i, j, k in idx)
    Y = sum(n[i]*n[j]*m[k] + n[i]*m[j]*m[k] for i, j, k in idx)
    return X, Y
for mode in ('R1', 'R2'):
    for nf, nl in ((1, 'N1 (N = rank)'), (2, 'N2 (N = 2 rank)')):
        rows = {k: XY(w, mode) for k, (N, w) in ST.items()}
        susy = all(Y == 0 and 2*X + Y > 0 for X, Y in rows.values())
        tad = sum(nf*N*(2*rows[k][0] + rows[k][1]) for k, (N, w) in ST.items())
        hid = sum(nf*ST[k][0]*rows[k][0] for k in 'de')
        ok = susy and (tad == 32 or hid == 8)
        print('%s %-16s XY %s | SUSY all %s | bulk tadpole %d (need 32) | hidden N X %d (text 8) -> %s' % (mode, nl, rows, susy, tad, hid, 'PASS' if ok else 'fail'))
    L = {k: math.sqrt(sum(v*v for v in ()) + XY(ST[k][1], mode)[0]**2 + XY(ST[k][1], mode)[0]*XY(ST[k][1], mode)[1] + XY(ST[k][1], mode)[1]**2) for k in 'abc'}
    print('   %s lengths a,b,c: %s (equal -> tree-level unification)' % (mode, L))
