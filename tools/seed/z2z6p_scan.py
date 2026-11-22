#!/usr/bin/env python3
"""D2111: Z2xZ6' AAA Pati-Salam scan (visible a,b,c same bulk, <=2 hidden stacks). SHARD=i/n env."""
import os, sys, itertools, math, json, time; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z2z6p as Z
si, sn = map(int, os.environ.get('SHARD', '0/1').split('/'))
W = []
for w in itertools.product(range(-3, 4), repeat=6):
    if any(math.gcd(w[2*i], w[2*i+1]) != 1 for i in range(3)): continue
    X, Y = Z.XY(w)
    if Y == 0 and 0 < 2*X + Y <= 14: W.append((2*X + Y, w))
VAR = [(t, tau, sig) for t in [(a, b, (a + b) % 2) for a in (0, 1) for b in (0, 1)]
       for tau in itertools.product((0, 1), repeat=3) for sig in itertools.product((0, 1), repeat=3)]
def cyc(w, v, jk):
    X, Y = Z.XY(w); ex = Z.exceptional(w, v[0], v[1], v[2], jk); return (X, Y, ex)
def vec(c, N):  # 24 twisted residual contributions + bulk
    _, res = Z.tadpoles([(N, c)]); return (N*(2*c[0] + c[1]),) + tuple(res)
def same(c1, c2): return c1[0] == c2[0] and c1[1] == c2[1] and c1[2] == c2[2]
def build(jk):
    B = {}
    for t, w in W:
        for v in VAR:
            c = cyc(w, v, jk)
            for N in range(1, 16 // t + 1):
                B.setdefault(vec(c, N), []).append((N, w, v))
    return B
t0 = time.time(); POOL = {jk: build(jk) for jk in ('P1', 'P2')}; KEYS = {jk: list(POOL[jk]) for jk in POOL}
print('pool built', {k: len(v) for k, v in POOL.items()}, '%.0fs' % (time.time() - t0), flush=True)
def completions(R, jk):  # hidden stacks summing to R (bulk 16, twisted -res)
    P = POOL[jk]; out = []
    if R in P: out += [(h,) for h in P[R]]
    for k in KEYS[jk]:
        r2 = tuple(a - b for a, b in zip(R, k))
        if r2[0] <= 0 or r2 not in P: continue
        if k <= r2: out += [(h1, h2) for h1 in P[k] for h2 in P[r2]]
    return out
T27 = ((0,1,1,0,1,-1), ((0,0,0),(0,0,1),(1,1,1)), ((1,1,0),(0,1,1),(1,1,1)), ((1,0,1),(1,0,1),(1,1,1)))
ck = lambda c: (c[0], c[1], tuple(c[2][k][a] for k in (1,2,3) for a in range(1,6)))
DIST = {}; SAMPLE = {}; CTRL = []
VIS = [w for t, w in W if t == 2][si::sn]; seenR = {}; stats = dict(vis_wrap=len(VIS), ab3=0, triples=0, uniqR=0, full=0)
for w in VIS:
    C = {jk: [cyc(w, v, jk) for v in VAR] for jk in ('P1', 'P2')}
    I = {jk: [Z.image(*c) for c in C[jk]] for jk in C}
    ok = [i for i in range(256) if not same(C['P1'][i], I['P1'][i])]
    def fam(i, j, jk): return Z.chi(C[jk][i], C[jk][j]) + Z.chi(C[jk][i], I[jk][j])
    for a in ok:
        Bs = {s: [b for b in ok if fam(a, b, 'P1') == 3*s and fam(a, b, 'P2') == 3*s] for s in (1, -1)}
        stats['ab3'] += len(Bs[1]) + len(Bs[-1])
        for s in (1, -1):
            for b in Bs[s]:
                for c in Bs[-s]:
                    stats['triples'] += 1
                    Rs = {}
                    for jk in ('P1', 'P2'):
                        v = [sum(x) for x in zip(vec(C[jk][a], 4), vec(C[jk][b], 2), vec(C[jk][c], 2))]
                        Rs[jk] = (32 - v[0],) + tuple(-x for x in v[1:])
                    key = (Rs['P1'], Rs['P2'])
                    if key not in seenR: seenR[key] = None; stats['uniqR'] += 1
                    if seenR[key] is None:
                        c1 = {(tuple(sorted((h[1], h[2], h[0]) for h in hs))) for hs in completions(Rs['P1'], 'P1')}
                        c2 = {(tuple(sorted((h[1], h[2], h[0]) for h in hs))) for hs in completions(Rs['P2'], 'P2')}
                        seenR[key] = sorted(c1 & c2)
                    hsl = seenR[key]; stats['full'] += len(hsl)
                    if not hsl: continue
                    stats['triples_ok'] = stats.get('triples_ok', 0) + 1
                    vk = tuple(ck(C['P1'][i]) for i in (a, b, c))
                    for hs in hsl:
                        hk = tuple(sorted((hN, ck(cyc(hw, hv, 'P1'))) for hw, hv, hN in hs))
                        dk = (vk, hk)
                        if dk in DIST: continue
                        if len(DIST) >= 5000: DIST[dk] = None; continue
                        hc = [cyc(hw, hv, 'P1') for hw, hv, hN in hs]; vh = 0
                        for i in (a, b, c):
                            for h in hc: vh += abs(Z.chi(C['P1'][i], h)) + abs(Z.chi(C['P1'][i], Z.image(*h)))
                        DIST[dk] = {'w': w, 'a': VAR[a], 'b': VAR[b], 'c': VAR[c], 'hidden': hs, 'vis_hidden_abs': str(vh),
                            'self': {x: str(Z.chi(C['P1'][i], I['P1'][i])) for x, i in (('a', a), ('b', b), ('c', c))},
                            'ab': [str(Z.chi(C['P1'][a], C['P1'][b])), str(Z.chi(C['P1'][a], I['P1'][b]))],
                            'ac': [str(Z.chi(C['P1'][a], C['P1'][c])), str(Z.chi(C['P1'][a], I['P1'][c]))]}
                    if (w, a, b, c) not in SAMPLE and len(SAMPLE) < 500: SAMPLE[(w, a, b, c)] = (len(hsl), hsl[:20])
                    if w == T27[0] and (VAR[a], VAR[b], VAR[c]) == T27[1:]: CTRL.append(len(hsl))
    print('wrap', w, stats, '%.0fs' % (time.time() - t0), flush=True)
ms = [m for m in DIST.values() if m]; spec = {json.dumps([m['ab'], m['ac'], m['self'], m['vis_hidden_abs']]) for m in ms}
vis_d = len({k[0] for k in DIST})
print('SHARD', si, sn, 'stats', stats, '| distinct-by-cycle models', len(DIST), '(capped 5000)' if len(DIST) >= 5000 else '', '| distinct visible', vis_d,
      '| control Table27 a,b,c in shard:', bool(CTRL), CTRL, '| distinct spectra', len(spec), flush=True)
json.dump({'stats': stats, 'control': CTRL, 'n_distinct': len(DIST), 'distinct_visible': vis_d, 'spectra': sorted(spec), 'models': ms[:300],
           'sample': [[list(k), v] for k, v in list(SAMPLE.items())[:100]]},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'z2z6p_scan_%d_%d.json' % (si, sn)), 'w'), default=list)
