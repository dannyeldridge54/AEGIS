#!/usr/bin/env python3
"""D2107 sonar-magnet v2: best-first search pulled by goalposts; sonar pings (wrap +-1, chi ladder moves) from every node;
memoised completions; QD archive; live knobs (tools/seed/sonar/knobs.json, re-read every log_every expansions)."""
import math, os, sys, time, itertools, json, heapq, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fractions import Fraction as Fr
import seed_v3 as s, exotics as e, seed_v4_ps as P
import torus as T
D = os.path.join(HERE, 'sonar'); KN = os.path.join(D, 'knobs.json'); LOG = os.path.join(D, 'nodes.jsonl'); ARCH = os.path.join(D, 'archive.json')
T_END = time.time() + float(os.environ.get('SONAR_MINUTES', '110'))*60
K = json.load(open(KN)); _memo = {}
_comp = e.completions
def completions_memo(S, chi, R, par):
    k = (tuple(chi), tuple(R), tuple(par), len(S))
    if k not in _memo: _memo[k] = _comp(S, chi, R, par)
    return _memo[k]
e.completions = completions_memo                       # echo removal: each hidden-ring problem solved once
POOL = {}
def pool(L):
    if L not in POOL: POOL[L] = T.branes(L)
    return POOL[L]
SUSY = {}
def susy_at(chi):
    k = (tuple(chi), K['L_pool'])
    if k not in SUSY: SUSY[k] = T.susy(pool(K['L_pool']), chi)
    return SUSY[k]
def score(r):
    if r is None: return None
    if r['alpha_s'] is None: return K['w_fit']
    return abs(r['alpha_s'] - 0.118)/0.0018 + K['w_exo']*(not r['safe']) + K['w_ms']*(r['Ms'] < 4e15)
def ladder(Q): return sorted({Fr(p, q) for q in range(1, Q + 1) for p in range(1, Q*Q + 1) if Fr(1, Q) <= Fr(p, q) <= Q})
def is_susy(w, chi): re, im = s.zprod(w, chi); return im == 0 and re > 0
def ps_ok(A, B, C): return s.inter(A, B) + s.inter(A, B, True) == 3 and (s.inter(A, C), s.inter(A, C, True)) in ((-3, 0), (0, -3))
def evaluate(chi, A, B, C):
    S = susy_at(chi)
    if not all(x in S for x in (A, B, C)): S = S + [x for x in (A, B, C) if x not in S]
    return T.evaluate(S, chi, A, B, C)
def nkey(chi, A, B, C): return (tuple(map(str, chi)), tuple(s.canon(A)), tuple(s.canon(B)), tuple(s.canon(C)))
def neighbours(chi, A, B, C, LAD):
    V = [list(A), list(B), list(C)]
    for i in range(3):
        for j in range(6):
            for d in (1, -1):
                W2 = [list(v) for v in V]; W2[i][j] += d; w = tuple(W2[i])
                if math.gcd(w[2*(j//2)], w[2*(j//2) + 1]) != 1 or max(map(abs, w)) > K['L_pool'] or not is_susy(w, chi): continue
                yield chi, tuple(W2[0]), tuple(W2[1]), tuple(W2[2]), ('wrap', i, j, d)
    if K.get('ping_radius', 1) >= 2:
        for i in range(3):
            for j, k2 in itertools.combinations(range(6), 2):
                for d1 in (1, -1):
                    for d2 in (1, -1):
                        W2 = [list(v) for v in V]; W2[i][j] += d1; W2[i][k2] += d2; w = tuple(W2[i])
                        if any(math.gcd(w[2*t], w[2*t+1]) != 1 for t in range(3)) or max(map(abs, w)) > K['L_pool'] or not is_susy(w, chi): continue
                        yield chi, tuple(W2[0]), tuple(W2[1]), tuple(W2[2]), ('wrap2', i, j, k2, d1, d2)
    for ax in range(3):
        idx = LAD.index(chi[ax]) if chi[ax] in LAD else None
        if idx is None: continue
        for d in (1, -1):
            if 0 <= idx + d < len(LAD):
                c2 = list(chi); c2[ax] = LAD[idx + d]; c2 = tuple(c2)
                if all(is_susy(x, c2) for x in (A, B, C)): yield c2, A, B, C, ('chi', ax, d)
def seeds():
    out = []
    for f in glob.glob(os.path.join(HERE, 'torus*', 'catalog.jsonl')):
        for l in open(f):
            r = json.loads(l); out.append((tuple(Fr(c) for c in r['chi']), tuple(r['A']), tuple(r['B']), tuple(r['C'])))
    for f in ('retry_exotics_results.json', 'outward_results.json'):
        p = os.path.join(HERE, f)
        if os.path.exists(p):
            d = json.load(open(p)); recs = d.get('near', []) + d.get('hits', []) + d.get('safe', [])
            for r in recs:
                try: out.append((tuple(Fr(c) for c in (r['chi'] if isinstance(r['chi'], list) else eval(r['chi']))), tuple(r['A']), tuple(r['B']), tuple(r['C'])))
                except Exception: pass
    return out
if __name__ == '__main__':
    seen = {}; heap = []; arch = json.load(open(ARCH)) if os.path.exists(ARCH) else {}
    if os.path.exists(LOG):
        for l in open(LOG):
            r = json.loads(l); seen[tuple(map(tuple, r['key']))] = r
    def push(chi, A, B, C, src):
        k = nkey(chi, A, B, C)
        if k in seen: return
        if not ps_ok(A, B, C): seen[k] = None; return
        r = evaluate(chi, A, B, C); sc = score(r); seen[k] = r
        if r is None: return
        r.update(key=[list(x) for x in k], score=sc, src=src, t=round(time.time()))
        with open(LOG, 'a') as f: f.write(json.dumps(r, default=str) + '\n')
        cell = ','.join(str(round(math.log(float(c))*4)/4) for c in chi)
        if cell not in arch or sc < arch[cell]['score']: arch[cell] = dict(score=sc, alpha_s=r['alpha_s'], safe=r['safe'], chi=r['chi'], W=r['W'])
        if r['safe'] and r['Ms'] and r['Ms'] >= 4e15 and abs(r['alpha_s'] - 0.118) <= 0.0018: print('HIT', r, flush=True)
        heapq.heappush(heap, (sc, time.time(), [str(c) for c in chi], A, B, C))
    for chi, A, B, C in seeds(): push(chi, A, B, C, 'seed')
    for r in list(v for v in seen.values() if v):        # resume: re-queue logged nodes
        heapq.heappush(heap, (r['score'], r['t'], r['chi'], tuple(r['A']), tuple(r['B']), tuple(r['C'])))
    print('seeded: %d nodes in queue' % len(heap), flush=True); n = 0; LAD = ladder(K['Q_ladder']); expanded = set()
    while heap and time.time() < T_END:
        sc, _, chis, A, B, C = heapq.heappop(heap); chi = tuple(Fr(c) for c in chis); k = nkey(chi, A, B, C)
        if k in expanded: continue
        expanded.add(k); t0 = time.time()
        for c2, A2, B2, C2, mv in neighbours(chi, A, B, C, LAD):
            if time.time() - t0 > K['node_cap_s']: break
            push(c2, A2, B2, C2, ['ping', mv, list(chis)])
        n += 1
        if n % K['log_every'] == 0:
            K = json.load(open(KN)); LAD = ladder(K['Q_ladder']); json.dump(arch, open(ARCH, 'w'))
            best = min((v['score'] for v in arch.values()), default=None)
            print('expanded %d | nodes %d | queue %d | cells %d | best score %s | knobs %s' % (n, sum(1 for v in seen.values() if v), len(heap), len(arch), best, K), flush=True)
    json.dump(arch, open(ARCH, 'w')); print('slice end: expanded %d' % n, flush=True)
