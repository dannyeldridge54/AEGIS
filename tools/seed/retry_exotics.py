#!/usr/bin/env python3
"""D2103: exotic-safe PS search at L=4 over the 343-point chi grid with per-model fitted K; vectorised intersections."""
import math, os, sys, time, itertools, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import seed_v3 as s, exotics as e, seed_v4_ps as P
def fit(Wa, Wb, Wc):
    VY = 2/3*Wa + Wc; det = Wb*P.bY/(2*math.pi) - VY*P.b2/(2*math.pi)
    return (P.inv2*P.bY/(2*math.pi) - P.invY*P.b2/(2*math.pi))/det, 91.19*math.exp((Wb*P.invY - VY*P.inv2)/det)
ALL4 = {}
for w in itertools.product(range(-4, 5), repeat=6):
    if any(math.gcd(w[2*t], w[2*t+1]) != 1 for t in range(3)): continue
    ALL4.setdefault(s.canon(w), w)
ALL4 = list(ALL4.values())
G = [Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(1), Fr(3, 2), Fr(2), Fr(3)]
tot = dict(chi=0, ps=0, fit=0, safe=0, near=0, hits=0, timeouts=0); hits = []; near_list = []
T0 = time.time()
for chi in itertools.product(G, repeat=3):
    t0 = time.time(); tot['chi'] += 1
    S = [w for w in ALL4 if s.zprod(w, chi)[1] == 0 and s.zprod(w, chi)[0] > 0]
    if len(S) < 3: continue
    W = np.array([[w[0], w[1], w[2], w[3], w[4], 2*w[5] - w[4]] for w in S], dtype=np.int64)   # n1 m1 n2 m2 n3 l3 (l3 = 2 mt3)
    def I(sign):
        out = np.ones((len(S), len(S)), dtype=np.int64)
        for t in range(3):
            na, ma = W[:, 2*t][:, None], W[:, 2*t+1][:, None]; nb, mb = W[:, 2*t][None, :], sign*W[:, 2*t+1][None, :]
            out = out*(na*mb - ma*nb)
        return out                                  # = 2 * true intersection (torus 3 uses l = 2 mt)
    I2, I2p = I(1), I(-1)
    AB = np.argwhere((I2 + I2p) == 6)                # I_ab + I_ab' = 3
    ACm = ((I2 == -6) & (I2p == 0)) | ((I2 == 0) & (I2p == -6))
    Wt = lambda x: x[0] - chi[1]*chi[2]*x[1] - chi[0]*chi[2]*x[2] - chi[0]*chi[1]*x[3]
    Xs = [s.X(w) for w in S]; brk = False
    for ia, ib in AB:
        if time.time() - t0 > 120: tot['timeouts'] += 1; brk = True; break
        if ia == ib: continue
        for ic in np.nonzero(ACm[ia])[0]:
            if ic in (ia, ib): continue
            R = tuple(t - 8*xa - 4*xb - 4*xc for t, xa, xb, xc in zip(s.TGT, Xs[ia], Xs[ib], Xs[ic]))
            if Wt(R) < 0: continue
            A, B, C = S[ia], S[ib], S[ic]
            cs = e.completions(S, chi, R, s.kcheck([(8, A), (4, B), (4, C)]))
            if not cs: continue
            tot['ps'] += 1; Wz = [float(s.zprod(v, chi)[0]) for v in (A, B, C)]; p = P.predict(*Wz)
            if p is None: continue
            tot['fit'] += 1; K, MS = fit(*Wz); ok = None
            for cm in cs:
                fine = True
                for N, h in cm:
                    if not any(s.inter(h, v) or s.inter(h, v, True) for v in (A, B, C)): continue
                    beta = -6 + 2*abs(s.inter(h, A)) + abs(s.inter(h, B)) + abs(s.inter(h, C))
                    lam = MS*math.exp(-2*math.pi*K*float(s.zprod(h, chi)[0])/abs(beta)) if beta < 0 else 0
                    if lam < 1e4: fine = False; break
                if fine: ok = cm; break
            if ok is None: continue
            tot['safe'] += 1; rec = dict(chi=[str(x) for x in chi], A=A, B=B, C=C, W=Wz, alpha_s=p[0], Ms=p[1], hidden=[(N, h) for N, h in ok])
            near_list.append(rec)
            if p[1] >= 4e15:
                tot['near'] += abs(p[0] - 0.118) <= 0.02
                if abs(p[0] - 0.118) <= 0.0018: tot['hits'] += 1; hits.append(rec)
print('TOTALS', tot, 'time %.0f s' % (time.time() - T0))
for h in hits[:10]: print('HIT', h['chi'], h['W'], round(h['alpha_s'], 4), '%.1e' % h['Ms'], 'A', h['A'], 'B', h['B'], 'C', h['C'])
print('best exotic-safe near-misses:')
for r in sorted(near_list, key=lambda r: abs(r['alpha_s'] - 0.118))[:6]: print('  ', r['chi'], r['W'], round(r['alpha_s'], 4), '%.1e' % r['Ms'])
print('look-elsewhere hits/near/0.09 =', ('%.2f' % (tot['hits']/tot['near']/0.09)) if tot['near'] else '-')
print('VERDICT:', 'PASS' if tot['hits'] else 'FAIL')
json.dump(dict(tot=tot, hits=hits, near=sorted(near_list, key=lambda r: abs(r['alpha_s'] - 0.118))[:20]), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'retry_exotics_results.json'), 'w'), default=str, indent=1)
