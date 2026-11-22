#!/usr/bin/env python3
"""D2105: (A) H89 racetrack consequences; (B) outward levels L1..L4 with backward pulse (birth levels) and convergence."""
import math, os, sys, time, itertools, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
print('== A: H89')
s0, P2 = 20.15, 2*math.pi; N, Np = 8, 9; a, b = P2/N, P2/Np; r = math.exp((a - b)*s0); BA = a/(b*r)
W0 = -r**(a/(b - a)) + BA*r**(b/(b - a)); ms = a*a*math.exp(-a*s0)*2.435e18/math.sqrt(2*s0)
mnat = math.sqrt(1.155/2)*2.435e18/4.0e4*abs(W0); eps = 128.5e3/mnat; Mt = 128.5e3**2/ms; q = math.exp(-math.pi*math.sqrt(3))
nat = [(k, W0/q**k) for k in range(1, 8) if 0.1 <= W0/q**k <= 10]
print('  B/A %.3f natural %s | eps %.2f (>=0.1 %s) | M_tree %.2f GeV = %.2f%% of wino 685 GeV | B1 natural k: %s | D7 17 vs 8 (x%.1f, estimate)'
      % (BA, 0.1 <= BA <= 10, eps, eps >= 0.1, Mt, 100*Mt/685, [(k, round(B, 3)) for k, B in nat], 17/8))
print('  H89:', 'CONSISTENT' if (0.1 <= BA <= 10 and eps >= 0.1 and Mt/685 < 0.05 and nat) else 'FAIL')
import seed_v3 as s, exotics as e, seed_v4_ps as P
def fit(Wa, Wb, Wc):
    VY = 2/3*Wa + Wc; det = Wb*P.bY/(2*math.pi) - VY*P.b2/(2*math.pi)
    return (P.inv2*P.bY/(2*math.pi) - P.invY*P.b2/(2*math.pi))/det, 91.19*math.exp((Wb*P.invY - VY*P.inv2)/det)
def branes(L):
    D = {}
    for w in itertools.product(range(-L, L + 1), repeat=6):
        if any(math.gcd(w[2*t], w[2*t+1]) != 1 for t in range(3)): continue
        D.setdefault(s.canon(w), w)
    return list(D.values())
G7 = [Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(1), Fr(3, 2), Fr(2), Fr(3)]
G12 = sorted(set(G7) | {Fr(1, 4), Fr(3, 4), Fr(4, 3), Fr(5, 2), Fr(4)})
LEVELS = [('L1', 3, G7), ('L2', 4, G7), ('L3', 4, G12), ('L4', 5, G12)]
def run_level(L, G, budget=60):
    ALL = branes(L); res = dict(ps=0, fit=0, safe=0, near=0, hits=0, timeouts=0, branes=len(ALL)); safe = []
    for chi in itertools.product(G, repeat=3):
        t0 = time.time(); S = [w for w in ALL if s.zprod(w, chi)[1] == 0 and s.zprod(w, chi)[0] > 0]
        if len(S) < 3: continue
        W = np.array([[w[0], w[1], w[2], w[3], w[4], 2*w[5] - w[4]] for w in S], dtype=np.int64)
        def I(sg):
            o = np.ones((len(S), len(S)), dtype=np.int64)
            for t in range(3): o = o*(W[:, 2*t][:, None]*sg*W[:, 2*t+1][None, :] - W[:, 2*t+1][:, None]*W[:, 2*t][None, :])
            return o
        I2, I2p = I(1), I(-1); AB = np.argwhere((I2 + I2p) == 6); ACm = ((I2 == -6) & (I2p == 0)) | ((I2 == 0) & (I2p == -6))
        Wt = lambda x: x[0] - chi[1]*chi[2]*x[1] - chi[0]*chi[2]*x[2] - chi[0]*chi[1]*x[3]; Xs = [s.X(w) for w in S]; stop = False
        for ia, ib in AB:
            if time.time() - t0 > budget: res['timeouts'] += 1; stop = True; break
            for ic in np.nonzero(ACm[ia])[0]:
                if ic in (ia, ib): continue
                R = tuple(t - 8*xa - 4*xb - 4*xc for t, xa, xb, xc in zip(s.TGT, Xs[ia], Xs[ib], Xs[ic]))
                if Wt(R) < 0: continue
                A, B, C = S[ia], S[ib], S[ic]; cs = e.completions(S, chi, R, s.kcheck([(8, A), (4, B), (4, C)]))
                if not cs: continue
                res['ps'] += 1; Wz = [float(s.zprod(v, chi)[0]) for v in (A, B, C)]; p = P.predict(*Wz)
                if p is None: continue
                res['fit'] += 1; K, MS = fit(*Wz); ok = None
                for cm in cs:
                    fine = True
                    for Nh, h in cm:
                        if not any(s.inter(h, v) or s.inter(h, v, True) for v in (A, B, C)): continue
                        beta = -6 + 2*abs(s.inter(h, A)) + abs(s.inter(h, B)) + abs(s.inter(h, C))
                        lam = MS*math.exp(-2*math.pi*K*float(s.zprod(h, chi)[0])/abs(beta)) if beta < 0 else 0
                        if lam < 1e4: fine = False; break
                    if fine: ok = cm; break
                if ok is None: continue
                res['safe'] += 1
                rec = dict(chi=chi, A=A, B=B, C=C, W=Wz, alpha_s=p[0], Ms=p[1], wrapmax=max(abs(x) for v in (A, B, C) for x in v),
                           ring_ratios=sorted(round(float(s.zprod(h, chi)[0])/Wz[0], 3) for _, h in ok))
                safe.append(rec)
                if p[1] >= 4e15:
                    res['near'] += abs(p[0] - 0.118) <= 0.02
                    res['hits'] += abs(p[0] - 0.118) <= 0.0018
    res['best'] = min((abs(r['alpha_s'] - 0.118) for r in safe), default=None)
    return res, safe
allsafe = {}; summary = []
for name, L, G in LEVELS:
    t = time.time(); res, safe = run_level(L, G)
    print('== %s (L=%d, grid %d -> %d chi): %s  [%.0f s]' % (name, L, len(G), len(G)**3, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in res.items()}, time.time() - t), flush=True)
    summary.append((name, res))
    for r in safe:
        key = (tuple(r['chi']), s.canon(r['A']), s.canon(r['B']), s.canon(r['C']))
        if key not in allsafe:
            birth = next(n for n, Lb, Gb in LEVELS if r['wrapmax'] <= Lb and all(c in Gb for c in r['chi']))
            allsafe[key] = dict(r, first_seen=name, birth=birth)
print('== backward pulse: exotic-safe models, birth level vs first seen, fingerprints')
for k, r in sorted(allsafe.items(), key=lambda kv: abs(kv[1]['alpha_s'] - 0.118))[:15]:
    print('  chi %s W %s alpha_s %.4f Ms %.1e wrapmax %d birth %s first %s ring/visible %s' % ([str(c) for c in r['chi']], r['W'], r['alpha_s'], r['Ms'], r['wrapmax'], r['birth'], r['first_seen'], r['ring_ratios']))
print('== convergence (best |d alpha_s| among exotic-safe per level):', [(n, None if r['best'] is None else round(r['best'], 4)) for n, r in summary])
print('VERDICT B:', 'PASS' if any(r['hits'] for _, r in summary) else 'FAIL')
json.dump(dict(summary=summary, safe=[dict(v, chi=[str(c) for c in v['chi']]) for v in allsafe.values()]), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outward_results.json'), 'w'), default=str, indent=1)
