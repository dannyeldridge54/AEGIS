#!/usr/bin/env python3
"""Seed engine v3 (PREREG D2082): exact consistency landscape on T6/(Z2xZ2), tilted T3 (mt = m - n/2).
Exact integer-chi SUSY (Im prod(n+i chi mt)=0, Re>0), visible 3-family pair, hidden completion counted by memoised DP over
(brane, residual tadpole charge, K-theory probe parity). Positive control = the CSU model (hep-th/0107143 Table I).
Run: python3 seed_v3.py  -> prints and writes seed_v3_results.json"""
import itertools, json, math, os, sys, time
from fractions import Fraction as Fr
from functools import lru_cache
sys.setrecursionlimit(100000)
H = Fr(1, 2); L = 3; TGT = (Fr(16), Fr(-8), Fr(-8), Fr(-16))
GRID = [Fr(1, 2), Fr(1), Fr(3, 2), Fr(2), Fr(3)]
PROBES = [(0, 1, 0, -1, 2, 1), (1, 0, 1, 0, 2, 1), (1, 0, 0, 1, 0, -1), (0, 1, 1, 0, 0, -1)]   # CSU filler cycles A1, A2, B2, C2
CSU = [(8, (0, 1, 0, -1, 2, 1)), (2, (1, 0, 1, 0, 2, 1)), (4, (1, 0, 1, -1, 1, 2)), (2, (1, 0, 0, 1, 0, -1)), (8, (1, -1, 1, 0, 1, 1)), (4, (0, 1, 1, 0, 0, -1))]
def tor(w): return ((Fr(w[0]), Fr(w[1])), (Fr(w[2]), Fr(w[3])), (Fr(w[4]), Fr(w[5]) - Fr(w[4])*H))
def X(w):
    (a, b), (c, d), (e, f) = tor(w); return (a*c*e, a*d*f, b*c*f, b*d*e)
def inter(wa, wb, img=False):
    p = Fr(1)
    for (na, ma), (nb, mb) in zip(tor(wa), tor(wb)): p *= na*(-mb if img else mb) - ma*nb
    return p
def canon(w):
    T = tor(w); fs = []
    for img in (1, -1):
        for fl in ((1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)): fs.append(tuple((f*n, f*img*m) for f, (n, m) in zip(fl, T)))
    return min(fs)
def zprod(w, chi):
    re, im = Fr(1), Fr(0)
    for (n, m), c in zip(tor(w), chi): re, im = re*n - im*c*m, re*c*m + im*n
    return re, im
def parity(w):
    out = []
    for p in PROBES:
        I = inter(w, p); assert I.denominator == 1, ('non-integer probe intersection', w, p, I); out.append(int(I) % 2)
    return tuple(out)
ALL = {}
for w in itertools.product(range(-L, L + 1), repeat=6):
    if any(math.gcd(w[2*t], w[2*t+1]) != 1 for t in range(3)): continue
    ALL.setdefault(canon(w), w)
ALL = list(ALL.values())
def kcheck(stacks):
    par = [0]*4
    for N, w in stacks:
        for i, b in enumerate(parity(w)): par[i] = (par[i] + (N//2)*b) % 2
    return tuple(par)
def run_chi(chi, budget=60.0):
    t0 = time.time(); c12, c13, c23 = chi[0]*chi[1], chi[0]*chi[2], chi[1]*chi[2]
    Wt = lambda x: x[0] - c23*x[1] - c13*x[2] - c12*x[3]
    S = []
    for w in ALL:
        re, im = zprod(w, chi)
        if im == 0 and re > 0: S.append(w)
    XB = [X(w) for w in S]; WB = [Wt(x) for x in XB]; PB = [parity(w) for w in S]; n = len(S)
    @lru_cache(maxsize=None)
    def cnt(i, R, par):
        if time.time() - t0 > budget: raise TimeoutError
        if i == n: return 1 if (all(r == 0 for r in R) and par == (0, 0, 0, 0)) else 0
        tot = 0; c = 0; Wr = Wt(R)
        while 2*c*WB[i] <= Wr:
            R2 = tuple(r - 2*c*x for r, x in zip(R, XB[i])); p2 = tuple((p + c*b) % 2 for p, b in zip(par, PB[i]))
            tot += cnt(i + 1, R2, p2); c += 1
        return tot
    pairs = []; models = 0; timeout = False
    for ia, A in enumerate(S):
        for ib, B in enumerate(S):
            if ia == ib: continue
            q = abs(inter(A, B)) + abs(inter(A, B, True))
            if q != 3: continue
            for NA in (6, 8):
                R = tuple(t - NA*xa - 4*xb for t, xa, xb in zip(TGT, X(A), X(B)))
                if Wt(R) < 0: continue
                par = kcheck([(NA, A), (4, B)])
                try: k = cnt(0, R, par)
                except TimeoutError: timeout = True; k = None
                pairs.append(dict(A=A, NA=NA, B=B, completions=k)); models += (k or 0)
                if timeout: break
            if timeout: break
        if timeout: break
    return dict(chi=[str(c) for c in chi], susy_branes=n, visible_pairs=len(pairs), pairs_completed=sum(1 for p in pairs if p['completions']),
                models=models, timeout=timeout, secs=round(time.time() - t0, 1), pairs=[p for p in pairs if p['completions']][:5])
if __name__ == '__main__':
    print('branes (canonical, |n|,|m|<=%d): %d' % (L, len(ALL)))
    kc = kcheck(CSU); print('K-theory convention check on CSU seed: parity', kc, 'PASS' if kc == (0, 0, 0, 0) else 'FAIL -> STOP')
    if kc != (0, 0, 0, 0): sys.exit(1)
    ctl = run_chi((Fr(1), Fr(3), Fr(2)), budget=300)
    hit = [p for p in ctl['pairs'] if canon(p['A']) == canon(CSU[4][1]) and canon(p['B']) == canon(CSU[2][1]) and p['NA'] == 8]
    allp = run_chi.__wrapped__ if hasattr(run_chi, '__wrapped__') else None
    print('CONTROL chi=(1,3,2):', {k: v for k, v in ctl.items() if k != 'pairs'})
    out = {'control': ctl}; R = []
    for chi in itertools.product(GRID, repeat=3):
        r = run_chi(chi); R.append(r)
        if r['visible_pairs']: print(' chi', r['chi'], 'susy', r['susy_branes'], 'pairs', r['visible_pairs'], 'completed', r['pairs_completed'], 'models', r['models'], 'TIMEOUT' if r['timeout'] else '', r['secs'], 's', flush=True)
    out['grid'] = R
    print('TOTAL: chi points %d, visible pairs %d, completed pairs %d, models %d, timeouts %d' % (len(R), sum(r['visible_pairs'] for r in R),
          sum(r['pairs_completed'] for r in R), sum(r['models'] for r in R), sum(r['timeout'] for r in R)))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seed_v3_results.json'), 'w'), indent=1, default=str)
