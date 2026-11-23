"""SPEED-Aion harness (A1, A2; committed per Zurvan DEV-4 / referee R79b)."""
import time, json, numpy as np
from aion import scan3s, f_ratios, hplus_br, sample
from aion_fast import scan3s_fast, mc_fast
def tm(f, n=3):
    t = []
    for _ in range(n): a = time.perf_counter(); r = f(); t.append(time.perf_counter() - a)
    return sorted(t)[n // 2], r
R = {}; w = 0; tr = tf = 0
for o in ('NO', 'IO'):
    a, ref = tm(lambda: scan3s(o), 1); b, fa = tm(lambda: scan3s_fast(o)); tr += a; tf += b
    for k in ref:
        for i in (0, 1): w = max(w, abs(ref[k][i] - fa[k][i]) / abs(ref[k][i]))
R['A1'] = dict(max_rel=w, t_ref=tr, t_fast=tf, pass_=bool(w < 1e-12))
w2 = 0; tr = tf = 0
for o in ('NO', 'IO'):
    def ref_mc():
        rng = np.random.default_rng(2188); S = sample(o, rng, 20000); BR = []; RT = []
        for i in range(20000):
            a, b = f_ratios(o, S['s12'][i], S['s23'][i], S['s13'][i], S['d'][i]); BR.append(hplus_br(a, b)); RT.append([abs(a), abs(b)])
        BR, RT = np.array(BR), np.array(RT); q = lambda x: [float(np.percentile(x, 16)), float(np.percentile(x, 84))]
        return dict(f_etau=q(RT[:, 0]), f_emu=q(RT[:, 1]), BR_e=q(BR[:, 0]), BR_mu=q(BR[:, 1]), BR_tau=q(BR[:, 2]))
    a, r1 = tm(ref_mc, 1); b, r2 = tm(lambda: mc_fast(o, np.random.default_rng(2188), 20000)); tr += a; tf += b
    for k in r1:
        for i in (0, 1): w2 = max(w2, abs(r1[k][i] - r2[k][i]) / abs(r1[k][i]))
R['A2'] = dict(max_rel=w2, t_ref=tr, t_fast=tf, pass_=bool(w2 < 1e-12))
json.dump(R, open('/home/claude/aegis/field_tests/results/speed_aion.json', 'w'), indent=1); print(json.dumps(R))
