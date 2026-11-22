#!/usr/bin/env python3
"""D2120a: Z_n survival tested against the full even lattice (Pi+Pi' of all fractional cycles |n,m|<=2, plus invariant cycles)."""
import os, sys, itertools, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z2z6p as Z
pm = lambda s: tuple(0 if c == '+' else 1 for c in s)
T27 = {'a': (4, (0,1,1,0,1,-1), '+++', (0,0,1), (1,1,1)), 'b': (2, (0,1,1,0,1,-1), '--+', (0,1,1), (1,1,1)),
       'c': (2, (0,1,1,0,1,-1), '-+-', (1,0,1), (1,1,1)), 'd': (2, (-1,2,2,-1,1,-1), '--+', (0,0,1), (1,1,1)),
       'e': (2, (1,0,1,0,1,0), '+--', (1,1,1), (1,1,0))}
ST = [(N, (lambda X, Y: (X, Y, Z.exceptional(w, pm(z), t, s, 'P2')))(*Z.XY(w))) for k, (N, w, z, t, s) in T27.items()]
VAR = [(t, tau, sig) for t in [(a, b, (a + b) % 2) for a in (0, 1) for b in (0, 1)] for tau in itertools.product((0, 1), repeat=3) for sig in itertools.product((0, 1), repeat=3)]
ck = lambda c: (c[0], c[1], tuple(c[2][k][a] for k in (1, 2, 3) for a in range(1, 6)))
vecs = set()   # each lattice element -> vector of (N_x * Pi_x o lambda)_x
for R, inv_only in ((2, False), (3, True)):
    for w in itertools.product(range(-R, R + 1), repeat=6):
        if any(math.gcd(w[2*i], w[2*i+1]) != 1 for i in range(3)): continue
        X, Y = Z.XY(w)
        if inv_only and Y != 0: continue
        for v in VAR:
            c = (X, Y, Z.exceptional(w, v[0], v[1], v[2], 'P2')); im = Z.image(*c)
            if inv_only:
                if ck(c) != ck(im): continue
                vec = tuple(N*Z.chi(cx, c) for N, cx in ST)
            else:
                vec = tuple(N*(Z.chi(cx, c) + Z.chi(cx, im)) for N, cx in ST)
            vecs.add(vec)
print('distinct lattice test vectors:', len(vecs), '| non-integer entries:', sum(1 for v in vecs for x in v if x.denominator != 1))
vl = [tuple(int(x) for x in v) for v in vecs if all(x.denominator == 1 for x in v)]
chiral = {'ab': (1,-1,0,0,0), "ab'": (1,1,0,0,0), 'ac': (-1,0,1,0,0), "ac'": (-1,0,-1,0,0), 'bc': (0,1,-1,0,0)}
Yk = {'ac.bc.ab': (0,0,0,0,0), "ac'.bc.ab'": (0,2,-2,0,0), "ac.bc.ab'": (0,2,0,0,0), "ac'.bc.ab": (0,0,-2,0,0)}
for n in range(2, 9):
    surv = [k for k in itertools.product(range(n), repeat=5) if math.gcd(n, *k) == 1 and all(sum(a*b for a, b in zip(k, v)) % n == 0 for v in vl)]
    if not surv: continue
    forb = {y: any(sum(a*b for a, b in zip(k, q)) % n for k in surv) for y, q in Yk.items()}
    print('Z_%d survives: %d primitive k, e.g. %s | Yukawa forbidden by some surviving Z_%d: %s' % (n, len(surv), surv[:3], n, forb))
