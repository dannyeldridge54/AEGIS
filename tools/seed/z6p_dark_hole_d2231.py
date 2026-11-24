"""D2231 (PREREG_D2231_DARK_HOLE): fill the rho = 3/2 exceptional tadpole hole with 1-3 hidden stacks (N <= 6); score as the dark sector."""
import os, sys, json, math, itertools, time, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.environ['RHO'] = '3/2'
src = open(os.path.join(HERE, 'z6p_scan_d2230.py')).read().split('def oddv(')[0]
g = dict(__file__=os.path.join(HERE, 'z6p_scan_d2230.py'), __name__='d2231'); exec(src, g)
FR, BULKS, img, I, O6, sym, F1, x_, y_ = (g[k] for k in ('FR', 'BULKS', 'img', 'I', 'O6', 'sym', 'F1', 'x_', 'y_'))
Z = g['Z']; T0 = time.time(); CAP = 30 * 60
O6v = np.array(O6, dtype=int)
# 1. distinct visible quadruples passing all visible filters (independent of hidden assignment)
vis = set()
for a, bb, c, d in itertools.product(BULKS, repeat=4):
    if not F1(a, bb): continue
    if 3*x_[a] + 2*x_[bb] + x_[c] + x_[d] > 8: continue
    for ca in FR[a]:
        if sym(ca) != 0: continue
        for cb in FR[bb]:
            ab, abp = I(ca, cb), I(ca, img(cb))
            if ab*abp < 0 or abs(ab + abp) != 3: continue
            sgn = 1 if ab + abp > 0 else -1
            for cc in FR[c]:
                tc = I(ca, cc), I(ca, img(cc))
                if any(sgn*t > 0 for t in tc): continue
                for cd in FR[d]:
                    td = I(ca, cd), I(ca, img(cd))
                    if any(sgn*t > 0 for t in td) or sgn*(sum(tc) + sum(td)) != -6: continue
                    vis.add((tuple(ca), tuple(cb), tuple(cc), tuple(cd)))
vis = sorted(vis); print('distinct visible quadruples', len(vis), flush=True)
# 2. hidden building blocks: every fractional cycle h of every bulk -> orientifold-even vector v = h + img(h)
blocks = [(tuple(h), tuple(int(round(v)) for v in (np.array(h) + np.array(img(h))))) for b in BULKS for h in FR[b]]
vecs = sorted(set(v for _, v in blocks)); rep = {}
for h, v in blocks: rep.setdefault(v, h)
V = {v: np.array(v) for v in vecs}
one = collections.defaultdict(list)
for v in vecs:
    for N in range(1, 7): one[tuple(N * V[v])].append(((N, v),))
two = collections.defaultdict(list)
for (k1, l1), (k2, l2) in itertools.combinations_with_replacement(list(one.items()), 2):
    s = tuple(np.array(k1) + np.array(k2))
    if len(two[s]) < 4: two[s].extend([l1[0] + l2[0]])
print('blocks', len(vecs), 'one-sums', len(one), 'two-sums', len(two), round(time.time() - T0), 's', flush=True)
def oddv(N, c): return N * (np.array(c) - np.array(img(c)))
def massless_Y(a, c, d):
    oa, oc, od = oddv(3, a), oddv(1, c), oddv(1, d)
    return any(np.all(oa + sc*3*oc + sd*3*od == 0) for sc in (1, -1) for sd in (1, -1))
hits = []; nclosed = 0; partial = False
for (ca, cb, cc, cd) in vis:
    if time.time() - T0 > CAP: partial = True; break
    base = sum(N * (np.array(c) + np.array(img(c))) for N, c in ((3, ca), (2, cb), (1, cc), (1, cd)))
    R = tuple(int(round(x)) for x in 4 * O6v - base)
    sols = [s for s in one.get(R, [])[:2]]
    sols += [s for s in two.get(R, [])[:2]]
    if not sols:
        for k1, l1 in one.items():
            rem = tuple(np.array(R) - np.array(k1))
            if rem in two: sols.append(l1[0] + two[rem][0]); break
    if not sols: continue
    nclosed += 1
    for sol in sols[:1]:
        hid = [(N, rep[v]) for N, v in (sol if isinstance(sol[0], tuple) else [sol])] if isinstance(sol, tuple) and isinstance(sol[0], tuple) else []
        if not hid:
            flat = list(sol); hid = [(flat[i], rep[flat[i + 1]]) for i in range(0, len(flat), 2)]
        D1 = bool(massless_Y(ca, cc, cd))
        t3 = sum(abs(Z.inter(list(v), list(h))) + abs(Z.inter(list(v), Z.image_ABa(list(h)))) for v in (ca, cb, cc, cd) for _, h in hid)
        st = [(3, ca), (2, cb), (1, cc), (1, cd)] + hid
        M = np.array([oddv(N, c) for N, c in st]).T; rk = np.linalg.matrix_rank(M); extra = len(st) - rk - (1 if D1 else 0)
        hits.append(dict(a=ca, b=cb, c=cc, d=cd, hidden=hid, D1_masslessY=D1, D2_T3=int(t3), D3_extra_U1=int(extra),
                         dark_candidate=bool(D1 and t3 == 0 and extra <= 2)))
nd = sum(h['dark_candidate'] for h in hits)
out = dict(rho='3/2', n_visible=len(vis), n_tadpole_closed=nclosed, n_dark_candidates=nd, partial=partial, seconds=round(time.time() - T0),
           fail_counts=dict(D1=sum(not h['D1_masslessY'] for h in hits), D2=sum(h['D2_T3'] != 0 for h in hits), D3=sum(h['D3_extra_U1'] > 2 for h in hits)),
           candidates=[h for h in hits if h['dark_candidate']][:200], closed_sample=hits[:200])
json.dump(out, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'd2231_dark_hole.json'), 'w'), default=lambda o: list(o) if isinstance(o, tuple) else (int(o) if isinstance(o, np.integer) else str(o)))
print(json.dumps({k: v for k, v in out.items() if k not in ('candidates', 'closed_sample')}))
