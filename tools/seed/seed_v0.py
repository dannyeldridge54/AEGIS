#!/usr/bin/env python3
"""Seed engine v0 (D2078): forks x integer lenses x radii -> hard consistency filters -> fit 2 couplings -> PREDICT alpha_s (held out)."""
import itertools, math, numpy as np
from fractions import Fraction as F
grid = [F(1,4), F(1,3), F(1,2), F(1), F(2), F(3), F(4)]
inv2, invY, as0, das = 29.59, 98.37, 0.1180, 0.0009
b3, b2, bY = -3.0, 1.0, 11.0
def vol(st, chi): return math.prod(math.sqrt(float(n)**2 + float(m*c)**2) for (n, m), c in zip(st, chi))
tot = phys = hits = 0; preds = []; examples = []
for b1, bb2, rho, eps in itertools.product([F(1), F(1,2)], [F(1), F(1,2)], [F(1), F(1,3)], [1, -1]):
    for na2, nb1, nd2 in itertools.product(range(-4, 5), repeat=3):
        nc1 = (bb2/(2*b1))*(na2 + 3*rho*nd2)
        if nc1.denominator != 1: continue
        tad = 3*F(na2)/(rho*b1) + 2*F(nb1)/bb2 + F(nd2)/b1
        if tad > 16: continue
        a = [(1/b1, 0), (na2, eps*bb2), (1/rho, F(1,2))]; b = [(nb1, -eps*b1), (1/bb2, 0), (1, 3*rho/2)]
        c = [(nc1, 3*rho*eps*b1), (1/bb2, 0), (0, 1)]; d = [(1/b1, 0), (nd2, -bb2*eps/rho), (1, 3*rho/2)]
        for chi in itertools.product(grid, repeat=3):
            tot += 1; Va, Vb, Vc, Vd = vol(a, chi), vol(b, chi), vol(c, chi), vol(d, chi)
            if min(Va, Vb, Vc, Vd) <= 0: continue
            VY = Va/6 + Vc/2 + Vd/2
            # inv2 = K Vb + b2/(2pi) L ; invY = K VY + bY/(2pi) L  -> solve K, L
            M = np.array([[Vb, b2/(2*math.pi)], [VY, bY/(2*math.pi)]]); 
            try: K, L = np.linalg.solve(M, [inv2, invY])
            except np.linalg.LinAlgError: continue
            if not (K > 0 and 0 < L < 38.8): continue
            phys += 1; inv3 = K*Va + b3/(2*math.pi)*L
            if inv3 <= 0: continue
            al = 1/inv3; preds.append(al); z = (al - as0)/das
            if abs(z) <= 2:
                hits += 1
                if len(examples) < 5: examples.append(dict(beta=(str(b1), str(bb2)), rho=str(rho), eps=eps, n=(na2, nb1, nd2, int(nc1)), chi=tuple(str(x) for x in chi), alpha_s=round(al, 4), Ms_GeV='%.1e' % (91.19*math.exp(L)), tad=str(tad)))
preds = np.array(preds)
print('configurations tried %d | passed filters + physical fit %d | alpha_s hits %d (%.4f of physical)' % (tot, phys, hits, hits/max(phys, 1)))
q = np.percentile(preds, [5, 25, 50, 75, 95]); print('alpha_s prediction distribution (5/25/50/75/95%%): %s' % ', '.join('%.3f' % x for x in q))
# chance level: fraction of a smooth spread that falls in the +-2 sigma window, estimated from the local density of predictions
win = (preds > as0 - 2*das) & (preds < as0 + 2*das); near = (preds > as0 - 0.02) & (preds < as0 + 0.02)
print('hits / predictions within +-0.02 of 0.118: %d / %d = %.3f (flat-spread chance = %.3f)' % (win.sum(), near.sum(), win.sum()/max(near.sum(), 1), 4*das/0.04))
for e in examples: print('  example hit:', e)
