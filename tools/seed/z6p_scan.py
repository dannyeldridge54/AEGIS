"""D2146 step 3a: visible-sector scan on T6/Z6' ABa, rho = 1/2 (PREREG_D2146 addendum 4)."""
import json, os, sys, math, itertools, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__)); import z6p as Z
from fractions import Fraction as Fr
H = Fr(1, 2); T0 = time.time(); CAP = 90*60
BULKS = [tuple(b) for b in json.load(open(os.path.join(os.path.dirname(__file__), 'z6p_checks3.json')))['bulk_cycles']]
# fractional variants per bulk (from any wrapping realising it)
FR = {b: set() for b in BULKS}
rng = range(-4, 5)
for w in itertools.product(rng, repeat=6):
    n1, m1, n2, m2, n3, m3 = w
    if not (n1 % 2 and m1 % 2) or math.gcd(n1, m1) != 1 or math.gcd(n2, m2) != 1 or math.gcd(n3, m3) != 1: continue
    B = tuple(Z.bulk(w))
    if B not in FR: continue
    for sig in itertools.product((0, H), repeat=4):
        for tau in itertools.product((0, 1), repeat=3):
            FR[B].add(tuple(Z.cycle(w, sig, tau)))
FR = {b: sorted(v) for b, v in FR.items()}
Fm = Z.F; img = lambda c: Z.image_ABa(list(c))
def I(x, y): return int(round(0.25*(np.array(x) @ Fm @ np.array(y))))
O6 = Z.O6_ABa
def sym(c): ci = img(c); return (I(c, ci) - I(c, O6))/2
x_ = {b: b[0] + b[1] for b in BULKS}; y_ = {b: b[2] - b[3] for b in BULKS}
# bulk configurations
cfgs = []
for a, bb, c, d in itertools.product(BULKS, repeat=4):
    X = 3*x_[a] + 2*x_[bb] + x_[c] + x_[d]; Y = 3*y_[a] + 2*y_[bb] + y_[c] + y_[d]
    if X > 8: continue
    rx, ry = 8 - X, 24 - Y
    if rx == 0 and ry == 0: cfgs.append(((a, 3), (bb, 2), (c, 1), (d, 1))); continue
    for h1 in BULKS:
        for N1 in (1, 2, 3, 4):
            if N1*x_[h1] == rx and N1*y_[h1] == ry: cfgs.append(((a, 3), (bb, 2), (c, 1), (d, 1), (h1, N1)))
            for h2 in BULKS:
                if h2 < h1: continue
                for N2 in (1, 2, 3, 4):
                    if N1*x_[h1] + N2*x_[h2] == rx and N1*y_[h1] + N2*y_[h2] == ry:
                        cfgs.append(((a, 3), (bb, 2), (c, 1), (d, 1), (h1, N1), (h2, N2)))
print('fractional per bulk:', {str(b): len(v) for b, v in list(FR.items())[:3]}, '... bulk configs:', len(cfgs), flush=True)
surv = []; nab = 0; partial = False
for cfg in cfgs:
    if time.time() - T0 > CAP: partial = True; break
    (a, _), (bb, _), (c, _), (d, _) = cfg[:4]; hid = cfg[4:]
    for ca in FR[a]:
        if sym(ca) != 0: continue
        for cb in FR[bb]:
            ab, abp = I(ca, cb), I(ca, img(cb))
            if ab*abp < 0 or abs(ab + abp) != 3: continue
            sgn = 1 if ab + abp > 0 else -1; nab += 1
            for cc in FR[c]:
                tc = I(ca, cc), I(ca, img(cc))
                if any(sgn*t > 0 for t in tc): continue
                for cd in FR[d]:
                    td = I(ca, cd), I(ca, img(cd))
                    if any(sgn*t > 0 for t in td) or sgn*(sum(tc) + sum(td)) != -6: continue
                    base = 3*(np.array(ca) + np.array(img(ca))) + 2*(np.array(cb) + np.array(img(cb))) + (np.array(cc) + np.array(img(cc))) + (np.array(cd) + np.array(img(cd)))
                    hopts = [[(N, np.array(h) + np.array(img(h)), h) for h in FR[hb]] for hb, N in hid]
                    for combo in itertools.product(*hopts) if hopts else [()]:
                        tot = base + sum((N*v for N, v, _ in combo), np.zeros(12))
                        if np.all(tot - 4*np.array(O6) == 0):
                            surv.append(dict(a=ca, b=cb, c=cc, d=cd, hidden=[(N, h) for N, _, h in combo]))
print('a-b pairs passing:', nab, 'survivors:', len(surv), 'partial:', partial, 'time', round(time.time() - T0), flush=True)
PUB = {'a': (0, 0, 1, -1, 0, 1, -1, 0, 0, 1, -1, 0), 'b': (3, 0, 3, 0, -3, 0, -3, 0, 0, 0, 0, 0)}
found_pub = any(tuple(s['a']) == PUB['a'] and tuple(s['b']) == PUB['b'] for s in surv)
json.dump(dict(n_bulk_cfgs=len(cfgs), n_survivors=len(surv), partial=partial, published_found=found_pub, survivors=surv[:2000]),
          open(os.path.join(os.path.dirname(__file__), 'z6p_scan3a.json'), 'w'), default=lambda o: list(o) if isinstance(o, tuple) else str(o))
print('published SM among survivors:', found_pub)
