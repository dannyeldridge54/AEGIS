#!/usr/bin/env python3
"""D2117: K-theory probe check for the Table-27 PS model."""
import os, sys, itertools, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z2z6p as Z
from fractions import Fraction as Fr
pm = lambda s: tuple(0 if c == '+' else 1 for c in s)
T27 = {'a': (4, (0,1,1,0,1,-1), '+++', (0,0,1), (1,1,1)), 'b': (2, (0,1,1,0,1,-1), '--+', (0,1,1), (1,1,1)),
       'c': (2, (0,1,1,0,1,-1), '-+-', (1,0,1), (1,1,1)), 'd': (2, (-1,2,2,-1,1,-1), '--+', (0,0,1), (1,1,1)),
       'e': (2, (1,0,1,0,1,0), '+--', (1,1,1), (1,1,0))}
ST = {k: (N, (lambda X, Y: (X, Y, Z.exceptional(w, pm(z), t, s, 'P2')))(*Z.XY(w))) for k, (N, w, z, t, s) in T27.items()}
VAR = [(t, tau, sig) for t in [(a, b, (a + b) % 2) for a in (0, 1) for b in (0, 1)] for tau in itertools.product((0, 1), repeat=3) for sig in itertools.product((0, 1), repeat=3)]
ck = lambda c: (c[0], c[1], tuple(c[2][k][a] for k in (1, 2, 3) for a in range(1, 6)))
probes = {}; bad = []
for w in itertools.product(range(-3, 4), repeat=6):
    if any(math.gcd(w[2*i], w[2*i+1]) != 1 for i in range(3)): continue
    X, Y = Z.XY(w)
    if Y != 0: continue
    for v in VAR:
        c = (X, Y, Z.exceptional(w, v[0], v[1], v[2], 'P2')); im = Z.image(*c)
        if ck(c) != ck(im): continue
        key = ck(c)
        if key in probes: continue
        s = sum(N*Z.chi(cx, c) for N, cx in ST.values()); probes[key] = (w, v, s)
        if s.denominator != 1 or s.numerator % 2: bad.append((w, v, str(s)))
print('invariant probe cycles (distinct):', len(probes), '| SUSY (2X+Y>0):', sum(1 for k in probes if 2*k[0] + k[1] > 0))
print('K-theory violations:', len(bad), bad[:10])
print('VERDICT', 'PASS' if not bad else 'FAIL')
