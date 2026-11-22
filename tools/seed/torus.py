#!/usr/bin/env python3
"""D2106 breathing torus: banded outward search; each band OUT-1 scan, IN re-test of all catalogued PS models with the band's
hidden branes, OUT-2 neighbour probe of exotic-safe models. Resumable (tools/seed/torus/state.json, catalog.jsonl)."""
import math, os, sys, time, itertools, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from fractions import Fraction as Fr
import seed_v3 as s, exotics as e, seed_v4_ps as P
D = os.environ.get('TORUS_DIR', os.path.join(HERE, 'torus')); CAT = os.path.join(D, 'catalog.jsonl'); ST = os.path.join(D, 'state.json'); T_END = time.time() + float(os.environ.get('TORUS_MINUTES', '110'))*60
def fit(Wa, Wb, Wc):
    VY = 2/3*Wa + Wc; det = Wb*P.bY/(2*math.pi) - VY*P.b2/(2*math.pi)
    return (P.inv2*P.bY/(2*math.pi) - P.invY*P.b2/(2*math.pi))/det, 91.19*math.exp((Wb*P.invY - VY*P.inv2)/det)
def branes(L):
    Dd = {}
    for w in itertools.product(range(-L, L + 1), repeat=6):
        if any(math.gcd(w[2*t], w[2*t+1]) != 1 for t in range(3)): continue
        Dd.setdefault(s.canon(w), w)
    return list(Dd.values())
def grid(Q): return sorted({Fr(p, q) for p in range(1, Q + 1) for q in range(1, Q + 1) if Fr(1, Q) <= Fr(p, q) <= Q})
def bands():
    k = 0
    while True:
        yield ('B%d' % (k + 1), 4 + (k + 1)//2, 4 + k//2); k += 1
def susy(S_all, chi): return [w for w in S_all if s.zprod(w, chi)[1] == 0 and s.zprod(w, chi)[0] > 0]
def evaluate(S, chi, A, B, C):
    """Returns (record or None). Record has safe flag."""
    R = tuple(t - 8*xa - 4*xb - 4*xc for t, xa, xb, xc in zip(s.TGT, s.X(A), s.X(B), s.X(C)))
    W = lambda x: x[0] - chi[1]*chi[2]*x[1] - chi[0]*chi[2]*x[2] - chi[0]*chi[1]*x[3]
    if W(R) < 0: return None
    cs = e.completions(S, chi, R, s.kcheck([(8, A), (4, B), (4, C)]))
    if not cs: return None
    Wz = [float(s.zprod(v, chi)[0]) for v in (A, B, C)]; p = P.predict(*Wz)
    rec = dict(chi=[str(c) for c in chi], A=list(A), B=list(B), C=list(C), W=Wz, alpha_s=None if p is None else p[0], Ms=None if p is None else p[1],
               safe=False, ratios=None, direction=[round(math.log(float(c)), 4) for c in chi])
    if p is None: return rec
    K, MS = fit(*Wz)
    for cm in cs:
        fine = True
        for Nh, h in cm:
            if not any(s.inter(h, v) or s.inter(h, v, True) for v in (A, B, C)): continue
            beta = -6 + 2*abs(s.inter(h, A)) + abs(s.inter(h, B)) + abs(s.inter(h, C))
            lam = MS*math.exp(-2*math.pi*K*float(s.zprod(h, chi)[0])/abs(beta)) if beta < 0 else 0
            if lam < 1e4: fine = False; break
        if fine: rec['safe'] = True; rec['ratios'] = sorted(round(float(s.zprod(h, chi)[0])/Wz[0], 3) for _, h in cm); break
    return rec
def is_hit(r): return r['safe'] and r['Ms'] and r['Ms'] >= 4e15 and abs(r['alpha_s'] - 0.118) <= 0.0018
def is_near(r): return r['safe'] and r['Ms'] and r['Ms'] >= 4e15 and abs(r['alpha_s'] - 0.118) <= 0.02
def ps_triples(S, chi, t0, budget):
    W = np.array([[w[0], w[1], w[2], w[3], w[4], 2*w[5] - w[4]] for w in S], dtype=np.int64)
    def I(sg):
        o = np.ones((len(S), len(S)), dtype=np.int64)
        for t in range(3): o = o*(W[:, 2*t][:, None]*sg*W[:, 2*t+1][None, :] - W[:, 2*t+1][:, None]*W[:, 2*t][None, :])
        return o
    I2, I2p = I(1), I(-1); AB = np.argwhere((I2 + I2p) == 6); ACm = ((I2 == -6) & (I2p == 0)) | ((I2 == 0) & (I2p == -6))
    for ia, ib in AB:
        if time.time() - t0 > budget: return
        for ic in np.nonzero(ACm[ia])[0]:
            if ic not in (ia, ib): yield S[ia], S[ib], S[ic]
def load():
    st = json.load(open(ST)) if os.path.exists(ST) else dict(done_scan={}, band_idx=int(os.environ.get('START_BAND', '1')) - 1, phase='OUT1', history=[], null_streak=0, best=None)
    cat = [json.loads(l) for l in open(CAT)] if os.path.exists(CAT) else []
    return st, cat
def save(st): json.dump(st, open(ST, 'w'), indent=1)
def log(rec):
    with open(CAT, 'a') as f: f.write(json.dumps(rec, default=str) + '\n')
def key(r): return (tuple(r['chi']), tuple(s.canon(tuple(r['A']))), tuple(s.canon(tuple(r['B']))), tuple(s.canon(tuple(r['C']))))
if __name__ == '__main__':
    os.makedirs(D, exist_ok=True); st, cat = load(); seen = {key(r): r for r in cat}
    for bi, (bname, L, Q) in enumerate(bands()):
        if bi < st['band_idx']: continue
        ALL = branes(L); G = grid(Q); new_safe = 0; t_band = time.time()
        print('== %s L=%d Q=%d: %d branes, %d chi' % (bname, L, Q, len(ALL), len(G)**3), flush=True)
        if st['phase'] == 'OUT1':
            SH_I, SH_N = (int(x) for x in os.environ.get('SHARD', '0/1').split('/'))
            for ci, chi in enumerate(itertools.product(G, repeat=3)):
                if ci % SH_N != SH_I: continue
                if time.time() > T_END: save(st); print('time slice over; resume later', flush=True); sys.exit(0)
                ck = ','.join(map(str, chi))
                if st['done_scan'].get(ck, 0) >= L: continue
                S = susy(ALL, chi); t0 = time.time()
                if len(S) >= 3:
                    for A, B, C in ps_triples(S, chi, t0, 60):
                        r = evaluate(S, chi, A, B, C)
                        if r is None: continue
                        k = key(r)
                        if k in seen and (seen[k]['safe'] or not r['safe']): continue
                        r.update(band=bname, phase='OUT1'); seen[k] = r; log(r); new_safe += r['safe']
                        if is_hit(r): print('HIT', r, flush=True)
                st['done_scan'][ck] = L
            st['phase'] = 'IN'; save(st)
        if st['phase'] == 'IN':
            for k, r in list(seen.items()):
                if r['safe'] or not all(Fr(c) in G for c in r['chi']): continue
                chi = tuple(Fr(c) for c in r['chi']); S = susy(ALL, chi)
                r2 = evaluate(S, chi, tuple(r['A']), tuple(r['B']), tuple(r['C']))
                if r2 and r2['safe']:
                    r2.update(band=bname, phase='IN-resonance'); seen[k] = r2; log(r2); new_safe += 1
                    if is_hit(r2): print('HIT (resonance)', r2, flush=True)
            st['phase'] = 'OUT2'; save(st)
        if st['phase'] == 'OUT2':
            for k, r in list(seen.items()):
                if not r['safe'] or r.get('probed_' + bname): continue
                chi = tuple(Fr(c) for c in r['chi']); S = susy(ALL, chi); Sset = set(map(tuple, S))
                for which in 'ABC':
                    for j in range(6):
                        for d in (1, -1):
                            V = {x: list(r[x]) for x in 'ABC'}; V[which][j] += d; w = tuple(V[which])
                            if max(abs(x) for x in w) > L or w not in Sset: continue
                            A, B, C = (tuple(V[x]) for x in 'ABC')
                            if s.inter(A, B) + s.inter(A, B, True) != 3 or (s.inter(A, C), s.inter(A, C, True)) not in ((-3, 0), (0, -3)): continue
                            r2 = evaluate(S, chi, A, B, C)
                            if r2 is None: continue
                            k2 = key(r2)
                            if k2 in seen and (seen[k2]['safe'] or not r2['safe']): continue
                            r2.update(band=bname, phase='OUT2', move=[which, j, d]); seen[k2] = r2; log(r2); new_safe += r2['safe']
                            if is_hit(r2): print('HIT (neighbour)', r2, flush=True)
                r['probed_' + bname] = True
        safe_all = [r for r in seen.values() if r['safe'] and r['alpha_s']]
        best = min((abs(r['alpha_s'] - 0.118) for r in safe_all if r['Ms'] and r['Ms'] >= 4e15), default=None)
        hits = sum(is_hit(r) for r in safe_all); near = sum(is_near(r) for r in safe_all)
        improved = best is not None and (st['best'] is None or best < st['best'] - 1e-6)
        st['null_streak'] = 0 if (new_safe or improved) else st['null_streak'] + 1; st['best'] = best if improved or st['best'] is None else st['best']
        summ = dict(band=bname, L=L, Q=Q, ps=len(seen), safe=len(safe_all), new_safe=new_safe, hits=hits, near=near, best=best, secs=round(time.time() - t_band))
        st['history'].append(summ); st['band_idx'] = bi + 1; st['phase'] = 'OUT1'; save(st); print('BAND', summ, flush=True)
        if hits: print('STOP: hit found'); break
        if st['null_streak'] >= 2: print('STOP: NULL (2 bands without new safe models or improvement)'); break
