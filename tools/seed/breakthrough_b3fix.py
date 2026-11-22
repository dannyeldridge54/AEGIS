#!/usr/bin/env python3
"""D2102 B3 rerun (DEVIATIONS): confinement with per-model fitted K and M_s."""
import math, os, sys, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import seed_v3 as s, exotics as e, seed_v4_ps as P
def fit(Wa, Wb, Wc):
    VY = 2/3*Wa + Wc; det = Wb*P.bY/(2*math.pi) - VY*P.b2/(2*math.pi)
    K = (P.inv2*P.bY/(2*math.pi) - P.invY*P.b2/(2*math.pi))/det; L = (Wb*P.invY - VY*P.inv2)/det
    return K, 91.19*math.exp(L)
G = [Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(1), Fr(3, 2), Fr(2), Fr(3)]
pts = fitok = safe = hits = near = 0; found = []
for chi in itertools.product(G, repeat=3):
    t0 = time.time(); S = [w for w in s.ALL if s.zprod(w, chi)[1] == 0 and s.zprod(w, chi)[0] > 0]
    Wt = lambda x: x[0] - chi[1]*chi[2]*x[1] - chi[0]*chi[2]*x[2] - chi[0]*chi[1]*x[3]
    for A, B in itertools.permutations(S, 2):
        if time.time() - t0 > 30: break
        if s.inter(A, B) + s.inter(A, B, True) != 3: continue
        for C in S:
            if C in (A, B) or (s.inter(A, C), s.inter(A, C, True)) not in ((-3, 0), (0, -3)): continue
            R = tuple(t - 8*xa - 4*xb - 4*xc for t, xa, xb, xc in zip(s.TGT, s.X(A), s.X(B), s.X(C)))
            if Wt(R) < 0: continue
            cs = e.completions(S, chi, R, s.kcheck([(8, A), (4, B), (4, C)]))
            if not cs: continue
            pts += 1; Wz = [float(s.zprod(v, chi)[0]) for v in (A, B, C)]; p = P.predict(*Wz)
            if p is None: continue
            fitok += 1; K, MS = fit(*Wz); ok = False
            for cm in cs:
                fine = True
                for N, h in cm:
                    if not any(s.inter(h, v) or s.inter(h, v, True) for v in (A, B, C)): continue
                    beta = -6 + 2*abs(s.inter(h, A)) + abs(s.inter(h, B)) + abs(s.inter(h, C))
                    lam = MS*math.exp(-2*math.pi*K*float(s.zprod(h, chi)[0])/abs(beta)) if beta < 0 else 0
                    if lam < 1e4: fine = False; break
                if fine: ok = True; break
            if not ok: continue
            safe += 1
            if p[1] >= 4e15:
                near += abs(p[0] - 0.118) <= 0.02; h = abs(p[0] - 0.118) <= 0.0018; hits += h
                if h: found.append(([str(x) for x in chi], Wz, round(p[0], 4), '%.1e' % p[1]))
print('PS points %d | physical fit %d | exotic-safe (fitted K) %d | near %d | HITS %d' % (pts, fitok, safe, near, hits))
for f in found[:8]: print('  hit:', f)
print('B3 VERDICT (rerun):', 'PASS' if hits else 'FAIL')
