#!/usr/bin/env python3
"""D2094: golden/silver hyperbolic axes vs the UFE centres (rho, i) and steps."""
import math, random
from fractions import Fraction
phi = (1 + 5**.5)/2; sil = 1 + 2**.5; rho = complex(0.5, 3**.5/2); I = 1j
def geo_dist(z, a, b):           # distance from z to the geodesic with real endpoints a,b
    c, r = (a + b)/2, abs(a - b)/2; return math.asinh(abs(abs(z - c)**2 - r*r)/(2*r*z.imag))
def hd(z, w): return math.acosh(1 + abs(z - w)**2/(2*z.imag*w.imag))
def hit(v):
    for q in range(1, 5):
        for p in range(-6*q, 6*q + 1):
            if p and abs(v/(p/q) - 1) <= 0.01: return str(Fraction(p, q))
    return None
for name, (a, b), tr in (('golden', (phi, -1/phi), 3), ('silver', (1 + 2**.5, 1 - 2**.5), 6)):
    print('%s axis %.4f..%.4f: transl. length %.4f | dist(i) %.1e | dist(rho) %.4f' % (name, a, b, 2*math.acosh(tr/2), geo_dist(I, a, b), geo_dist(rho, a, b)))
d1 = hd(rho, I); d2 = 2*math.atanh(0.052)
print('T1 d(rho,i) = %.5f (= ln sqrt3 = %.5f)' % (d1, math.log(3)/2)); print('T2 d* = %.5f' % d2)
res = {}
for un, u in (('ln phi', math.log(phi)), ('ln silver', math.log(sil))):
    for tn, d in (('T1', d1), ('T2', d2)):
        h = hit(d/u); res[(un, tn)] = h; print('  %s / %s = %.4f -> %s' % (tn, un, d/u, h or 'no hit'))
random.seed(0); R = [math.exp(random.uniform(math.log(.3), math.log(1.2))) for _ in range(10000)]
ch = {tn: sum(1 for u in R if hit(d/u)) / len(R) for tn, d in (('T1', d1), ('T2', d2))}
print('chance hit rate: T1 %.3f  T2 %.3f' % (ch['T1'], ch['T2']))
ev = [un for un in ('ln phi', 'ln silver') if res[(un, 'T1')] and res[(un, 'T2')]]
print('VERDICT:', 'EVIDENCE?' if ev and min(ch.values()) < 1/3 else 'NO EVIDENCE', '(both-hit units: %s)' % ev)
