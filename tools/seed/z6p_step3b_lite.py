"""D2167: step 3b (lite) on the stored Z6-II survivors: hypercharge masslessness, extra massless U(1)s, chiral visible-hidden matter."""
import os, sys, json, collections
import sympy as sp
sys.path.insert(0, os.path.dirname(__file__)); import z6p as Z
d = json.load(open(os.path.join(os.path.dirname(__file__), 'z6p_scan3a.json')))
PER = (8/7) * (10.75/228.75)**(4/3)
def odd(N, c): return [N*(x - y) for x, y in zip(c, Z.image_ABa(c))]
res = collections.Counter(); extra_hist = collections.Counter(); clean = []; selfimg = 0
for i, m in enumerate(d['survivors']):
    st = [('a', 3, m['a']), ('b', 2, m['b']), ('c', 1, m['c']), ('d', 1, m['d'])] + [(f'h{k}', N, c) for k, (N, c) in enumerate(m['hidden'])]
    M = sp.Matrix([odd(N, c) for _, N, c in st]).T
    t1 = False
    for sc in (1, -1):      # DEV-1: sign of Q_c and Q_d depends on brane vs image storage
        for sd in (1, -1):
            Y = sp.Matrix([sp.Rational(1, 6), 0, sp.Rational(sc, 2), sp.Rational(sd, 2)] + [0]*(len(st) - 4))
            if (M * Y).is_zero_matrix: t1 = True
    extra = len(M.nullspace()) - 1 if t1 else None
    vis = [x for x in st[:4]]; hid = st[4:]
    t3 = 0
    for _, _, cv in vis:
        for _, _, ch in hid:
            t3 += abs(Z.inter(cv, ch)) + abs(Z.inter(cv, Z.image_ABa(ch)))
    if any(odd(1, c) == [0]*12 for n, N, c in st if n in ('c', 'd') or n.startswith('h')): selfimg += 1
    res['T1_pass' if t1 else 'T1_fail'] += 1
    if t1:
        extra_hist[extra] += 1
        res['T3_none' if t3 == 0 else 'T3_exotic'] += 1
        if t3 == 0 and extra*PER < 0.14: clean.append(i)
out = dict(n=len(d['survivors']), counts=dict(res), extra_massless_U1_hist={str(k): v for k, v in sorted(extra_hist.items())},
           dNeff_per_U1=PER, n_clean=len(clean), first_clean=clean[:20], any_self_image_U1=selfimg)
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(__file__), '..', '..', 'field_tests', 'results', 'd2167_step3b_lite_dev1.json'), 'w'), indent=1)
