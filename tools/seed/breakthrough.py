#!/usr/bin/env python3
"""D2102: breakthrough chart pass (B1, B4, B2, B3)."""
import math, os, sys, time, itertools, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
q = math.exp(-2*math.pi*math.sqrt(3)/2)
def natural(target, pref=1.0):
    return [(k, target/(pref*q**k)) for k in range(1, 9) if 0.1 <= target/(pref*q**k) <= 10]
def pval(lo, hi, pref=1.0, n=20000):
    random.seed(0); return sum(1 for _ in range(n) if natural(math.exp(random.uniform(math.log(lo), math.log(hi))), pref)) / n
print('== B1 W0 = B q^k, q = e^{-pi sqrt3} = %.3e' % q)
for lab, t in (('KKLT lo 2.70e-9', 2.70e-9), ('KKLT hi 2.86e-9', 2.86e-9), ('KL(7,8) 2.0e-9', 2.0e-9), ('old target 5.6e-9', 5.6e-9)):
    print('  %-18s natural (k,B): %s' % (lab, [(k, round(b, 2)) for k, b in natural(t)] or 'none'))
print('  look-elsewhere p (targets log-uniform 1e-10..1e-8) = %.2f' % pval(1e-10, 1e-8))
print('== B4 instanton mu_W')
muW = 0.25*0.551*159e3
for lab, M in (('M_s 1e16', 1e16), ('M_P', 2.435e18)):
    print('  mu_W = %.2e GeV, %-8s natural (k,C): %s  p = %.2f' % (muW, lab, [(k, round(c, 2)) for k, c in natural(muW, M)], pval(1e3, 1e5, M)))
print('== B2 tadpole estimate (families 3.1.1): cost = 3 N_vis + 1; give-back 17-34; budget 4-6')
for N in (2, 3, 5):
    c = 3*N + 1; print('  N_vis %d: cost %d -> net %d..%d vs budget <= 6 -> %s (old |M|=9: %d)' % (N, c, c - 34, c - 17, 'within' if c - 17 <= 6 else ('within if give-back >= %d' % (c - 6)) if c - 34 <= 6 else 'over', 9*N + 1))
print('== B3 exotic-safe PS scan')
import seed_v3 as s, exotics as e, seed_v4_ps as P
G = [Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(1), Fr(3, 2), Fr(2), Fr(3)]; K, MS = 25/6, 1e16
pts = safe = hits = near = to = 0; found = []
for chi in itertools.product(G, repeat=3):
    t0 = time.time(); S = [w for w in s.ALL if s.zprod(w, chi)[1] == 0 and s.zprod(w, chi)[0] > 0]
    Wt = lambda x: x[0] - chi[1]*chi[2]*x[1] - chi[0]*chi[2]*x[2] - chi[0]*chi[1]*x[3]; brk = False
    for A, B in itertools.permutations(S, 2):
        if time.time() - t0 > 30: to += 1; brk = True; break
        if s.inter(A, B) + s.inter(A, B, True) != 3: continue
        for C in S:
            if C in (A, B) or (s.inter(A, C), s.inter(A, C, True)) not in ((-3, 0), (0, -3)): continue
            R = tuple(t - 8*xa - 4*xb - 4*xc for t, xa, xb, xc in zip(s.TGT, s.X(A), s.X(B), s.X(C)))
            if Wt(R) < 0: continue
            cs = e.completions(S, chi, R, s.kcheck([(8, A), (4, B), (4, C)]))
            if not cs: continue
            pts += 1; ok = False
            for cm in cs:
                fine = True
                for N, h in cm:
                    if not any(s.inter(h, v) or s.inter(h, v, True) for v in (A, B, C)): continue
                    beta = -6 + 2*abs(s.inter(h, A)) + abs(s.inter(h, B)) + abs(s.inter(h, C))
                    lam = MS*math.exp(-2*math.pi*K*float(s.zprod(h, chi)[0])/abs(beta)) if beta < 0 else 0
                    if lam < 1e4: fine = False; break
                if fine: ok = True; break
            if not ok: continue
            safe += 1; Wz = [float(s.zprod(v, chi)[0]) for v in (A, B, C)]; p = P.predict(*Wz)
            if p and p[1] >= 4e15:
                near += abs(p[0] - 0.118) <= 0.02; h = abs(p[0] - 0.118) <= 0.0018; hits += h
                if h: found.append((str(chi), Wz, round(p[0], 4), '%.1e' % p[1]))
    if brk: continue
print('  PS points %d | exotic-safe %d | near (Ms ok) %d | HITS %d | timeouts %d chi | hits/near/0.09 = %s' % (pts, safe, near, hits, to, ('%.2f' % (hits/near/0.09)) if near else '-'))
for f in found[:8]: print('   hit:', f)
print('B3 VERDICT:', 'PASS' if hits else 'FAIL')
