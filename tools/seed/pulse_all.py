#!/usr/bin/env python3
"""D2100: one pulsed pass over loop-2 queue (P1-P6)."""
import math, os, sys, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
print('== P1 dark U(1) of U(12)')
ai = 2*12*40.3 + 2/(2*math.pi)*math.log(1e16/12.8); aD = 1/ai; sv = math.pi*aD**2/12.8**2*1.167e-17
print('  alpha_D(12.8 GeV) = %.3e ; sigma v = %.2e cm^3/s vs 4.4e-26 -> %s (margin x%.1f)' % (aD, sv, 'PASS' if sv >= 4.4e-26 else 'FAIL', sv/4.4e-26))
print('== P2 D7 count (estimate): (7,8) 15 D7 = %.1fx one O7 class; (14,15) 29 D7 = %.1fx' % (15/8, 29/8))
print('== P4 T_vis axion: m_a ~ m_sigma >= 4e9 GeV vs birefringence m <~ 10 H0 ~ 1.4e-41 GeV -> FAIL (must be a separate ultralight axion; c_gamma/f stays FIT)')
print('== P5: dropped (moot in KL branch)')
print('== P6 tan beta = 1.9 with universal masses')
import tanb_run as T, wino_mu as W, tsusy
r, info = T.tanb_from(1.9); m2 = T.m32**2; mHu, mHd = info['mHu']/m2, info['mHd']/m2; t2 = 1.9**2
mu2 = (mHd - t2*mHu)/(t2 - 1); c = math.sqrt(mu2); Bmu = math.sqrt((mHu + mu2)*(mHd + mu2)); B = Bmu/c
f = (2 - B)/3          # mu_W/mu from (2(1-f) - f) = B
print('  running: mHu2 %.3f mHd2 %.3f -> needs mu = %.3f m32, B = %.3f m32, mu_W/mu = %.3f' % (mHu, mHd, c, B, f))
import numpy as np
ok = []
for m32 in np.logspace(math.log10(5e4), math.log10(4e5), 400):
    mu = c*m32; mw = W.wino(m32, mu*2*1.9/(1 + 1.9**2)); mg = W.gluino(m32)
    if 670 <= mw <= 700 and mg >= 2300:
        a = W.aS(tsusy.T(mw, mg, mu, mu))
        if a and abs(a - 0.118) <= 0.0018: ok.append((m32, mw, mg, a))
if ok:
    A = np.array(ok); print('  goalposts at c=%.2f, tanb 1.9: %d pts, m32 %.0f-%.0f TeV, gluino %.2f-%.2f TeV, alpha_s %.4f-%.4f -> CONSISTENT' % (c, len(ok), A[:,0].min()/1e3, A[:,0].max()/1e3, A[:,2].min()/1e3, A[:,2].max()/1e3, A[:,3].min(), A[:,3].max()))
else: print('  goalposts at c=%.2f: none -> TENSION' % c)
print('== P3 Seed v5 pulse, L=4')
import seed_v3 as s, exotics as e
ALL4 = {}
for w in itertools.product(range(-4, 5), repeat=6):
    if any(math.gcd(w[2*t], w[2*t+1]) != 1 for t in range(3)): continue
    ALL4.setdefault(s.canon(w), w)
ALL4 = list(ALL4.values()); print('  canonical branes L=4: %d' % len(ALL4))
K, MS = 25/6, 1e16
for chi in ((Fr(1), Fr(3), Fr(2)), (Fr(3), Fr(1), Fr(2))):
    t0 = time.time(); S = [w for w in ALL4 if s.zprod(w, chi)[1] == 0 and s.zprod(w, chi)[0] > 0]; X = {w: s.X(w) for w in S}
    Wt = lambda x: x[0] - chi[1]*chi[2]*x[1] - chi[0]*chi[2]*x[2] - chi[0]*chi[1]*x[3]
    pts = comps = good = 0; found = []; to = False
    for A, B in itertools.permutations(S, 2):
        if time.time() - t0 > 300: to = True; break
        if s.inter(A, B) + s.inter(A, B, True) != 3: continue
        for C in S:
            if C in (A, B) or (s.inter(A, C), s.inter(A, C, True)) not in ((-3, 0), (0, -3)): continue
            R = tuple(t - 8*xa - 4*xb - 4*xc for t, xa, xb, xc in zip(s.TGT, X[A], X[B], X[C]))
            if Wt(R) < 0: continue
            cs = e.completions(S, chi, R, s.kcheck([(8, A), (4, B), (4, C)]))
            if not cs: continue
            pts += 1; comps += len(cs)
            for cm in cs:
                fine = True
                for N, h in cm:
                    ex = any(s.inter(h, v) or s.inter(h, v, True) for v in (A, B, C))
                    if not ex: continue
                    beta = -6 + sum(k*abs(s.inter(h, v)) for k, v in ((2, A), (1, B), (1, C)))
                    lam = MS*math.exp(-2*math.pi*K*float(s.zprod(h, chi)[0])/abs(beta)) if beta < 0 else 0
                    if not (beta < 0 and lam >= 1e4): fine = False; break
                if fine:
                    good += 1; Wz = [float(s.zprod(v, chi)[0]) for v in (A, B, C)]
                    import seed_v4_ps as P; p = P.predict(*Wz); found.append((Wz, p))
    print('  chi %s: PS points %d, completions %d, fully passing %d%s' % ([str(x) for x in chi], pts, comps, good, ' (TIMEOUT at 300 s)' if to else ''))
    for Wz, p in found[:5]: print('     Re z (a,b,c) = %s  alpha_s %s' % (Wz, 'none' if p is None else '%.4f Ms %.1e' % p))
