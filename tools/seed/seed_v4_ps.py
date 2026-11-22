#!/usr/bin/env python3
"""Seed v4 (PREREG D2083): Pati-Salam fork on the D2082 exact landscape. a=U(4) N=8, b=U(2)_L N=4, c=U(2)_R N=4; three-family
conditions (He-Li-Sun 2112.09632 Eq 3.3/3.4); exact tadpole + K completion; alpha_x^-1 ∝ Re z_x (Eq 3.5-3.8), alpha_Y^-1 = 2/3 a + c;
fit K and ln(Ms/MZ) to alpha_2, alpha_Y at MZ (one-loop MSSM, as D2078/79); predict alpha_s. Run: python3 seed_v4_ps.py"""
import itertools, json, math, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seed_v3 as s
from fractions import Fraction as Fr
from functools import lru_cache
inv2, invY, as0, das, MSMIN = 29.59, 98.37, 0.1180, 0.0009, 4e15
b3, b2, bY = -3.0, 1.0, 11.0
def predict(Wa, Wb, Wc):
    VY = 2/3*Wa + Wc; det = Wb*bY/(2*math.pi) - VY*b2/(2*math.pi)
    if det == 0: return None
    K = (inv2*bY/(2*math.pi) - invY*b2/(2*math.pi))/det; L = (Wb*invY - VY*inv2)/det
    if not (K > 0 and 0 < L < 38.8): return None
    inv3 = K*Wa + b3/(2*math.pi)*L
    if inv3 <= 0: return None
    return 1/inv3, 91.19*math.exp(L)
def run_chi(chi, budget=120.0):
    t0 = time.time(); c12, c13, c23 = chi[0]*chi[1], chi[0]*chi[2], chi[1]*chi[2]
    Wt = lambda x: x[0] - c23*x[1] - c13*x[2] - c12*x[3]
    S = [w for w in s.ALL if s.zprod(w, chi)[1] == 0 and s.zprod(w, chi)[0] > 0]
    XB = [s.X(w) for w in S]; WB = [Wt(x) for x in XB]; PB = [s.parity(w) for w in S]; n = len(S)
    @lru_cache(maxsize=None)
    def cnt(i, R, par):
        if time.time() - t0 > budget: raise TimeoutError
        if i == n: return 1 if (all(r == 0 for r in R) and par == (0, 0, 0, 0)) else 0
        tot = 0; c = 0; Wr = Wt(R)
        while 2*c*WB[i] <= Wr:
            tot += cnt(i + 1, tuple(r - 2*c*x for r, x in zip(R, XB[i])), tuple((p + c*b) % 2 for p, b in zip(par, PB[i]))); c += 1
        return tot
    out = []; timeout = False
    for ia, ib in itertools.permutations(range(n), 2):
        A, B = S[ia], S[ib]
        if s.inter(A, B) + s.inter(A, B, True) != 3: continue
        for ic in range(n):
            if ic in (ia, ib): continue
            C = S[ic]; pair = (s.inter(A, C), s.inter(A, C, True))
            if pair not in ((-3, 0), (0, -3)): continue
            R = tuple(t - 8*xa - 4*xb - 4*xc for t, xa, xb, xc in zip(s.TGT, XB[ia], XB[ib], XB[ic]))
            if Wt(R) < 0: continue
            try: k = cnt(0, R, s.kcheck([(8, A), (4, B), (4, C)]))
            except TimeoutError: timeout = True; break
            if not k: continue
            p = predict(float(WB[ia]), float(WB[ib]), float(WB[ic]))
            out.append(dict(topo=(s.canon(A), s.canon(B), s.canon(C)), A=A, B=B, C=C, completions=k, W=[str(WB[ia]), str(WB[ib]), str(WB[ic])],
                            alpha_s=None if p is None else p[0], Ms=None if p is None else p[1]))
        if timeout: break
    seen = {}; [seen.setdefault(o['topo'], o) for o in out]          # one entry per topology at this chi
    return list(seen.values()), timeout
if __name__ == '__main__':
    ctl = predict(1.0, 1.0, 1.0); print('CONTROL unified: alpha_s %.4f  Ms %.2e' % ctl)
    if not (abs(ctl[0] - 0.1168) <= 0.0010 and abs(ctl[1]/2.0e16 - 1) <= 0.10): print('STOP: control failed'); sys.exit(1)
    pts = []; topos = set(); tos = 0
    for chi in itertools.product(s.GRID, repeat=3):
        r, to = run_chi(chi); tos += to
        for o in r: o['chi'] = [str(c) for c in chi]; pts.append(o); topos.add(o['topo'])
    phys = [p for p in pts if p['alpha_s'] is not None]; g2 = [p for p in phys if p['Ms'] >= MSMIN]
    near = [p for p in g2 if abs(p['alpha_s'] - as0) <= 0.02]; hits = [p for p in g2 if abs(p['alpha_s'] - as0) <= 2*das]
    ratio = (len(hits)/len(near))/0.09 if near else 0.0
    verdict = 'SIGNAL' if (len(hits) >= 3 and ratio >= 3) else 'NULL'
    print('PS (topology,chi) points %d | topologies %d | timeouts %d | physical fit %d | G2 (Ms>=4e15) %d | near %d | JOINT HITS %d | hits/near / 0.09 = %.2f -> %s'
          % (len(pts), len(topos), tos, len(phys), len(g2), len(near), len(hits), ratio, verdict))
    for p in sorted(phys, key=lambda p: abs(p['alpha_s'] - as0))[:8]:
        print('  alpha_s %.4f Ms %.2e W %s chi %s compl %d' % (p['alpha_s'], p['Ms'], p['W'], p['chi'], p['completions']))
    json.dump(dict(control=ctl, points=[{k: v for k, v in p.items() if k != 'topo'} for p in pts], verdict=verdict, hits=len(hits), near=len(near)),
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seed_v4_results.json'), 'w'), indent=1, default=str)
