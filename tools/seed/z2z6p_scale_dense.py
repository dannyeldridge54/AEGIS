#!/usr/bin/env python3
"""D2116a: dense v3 re-solve of D2114 equations (imports model/resid from z2z6p_scale without running its main)."""
import math, json, os, numpy as np
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'z2z6p_scale.py')).read().split('out = {}')[0]; exec(src)
from scipy.optimize import fsolve
V3 = np.logspace(1, 6, 120); out = {}
for MPn, MP in (('reduced', 2.435e18), ('nonreduced', 1.221e19)):
    for var in ('A', 'B'):
        gen, iso = [], []
        for v3 in V3:
            seen = []
            for g0 in (-8, -5, -3, -1, 0, 1):
                for v0 in ((2, 2), (50, 50), (300, 50), (300, 300), (3000, 300), (3000, 3000), (3e4, 3e4)):
                    x, info, ok, _ = fsolve(resid, [math.log(v0[0]), math.log(v0[1]), g0], args=(v3, MP, var, False), full_output=True)
                    if ok == 1 and max(abs(r) for r in resid(x, v3, MP, var, False)) < 1e-6:
                        v1, v2, gs = math.exp(x[0]), math.exp(x[1]), math.exp(x[2])
                        if any(abs(v1 - s[0]) < 1e-3*v1 for s in seen): continue
                        seen.append((v1, v2, gs)); T, Ms, A = model(v1, v2, v3, gs, MP, var); d = thr(v1, v2, v3, var)
                        gen.append(dict(v3=float(v3), v1=v1, v2=v2, gs=gs, Ms=Ms, ctrl=max(abs(t) for t in d)/T,
                                        geometric=bool(min(v1, v2, v3) >= 1 and gs < 1)))
                x, info, ok, _ = fsolve(resid, [math.log(50), g0], args=(v3, MP, var, True), full_output=True)
                if ok == 1 and max(abs(r) for r in resid(x, v3, MP, var, True)) < 1e-6:
                    v, gs = math.exp(x[0]), math.exp(x[1]); T, Ms, A = model(v, v, v3, gs, MP, var); m = alpha_inv(Ms)
                    iso.append(dict(v3=float(v3), v=v, gs=gs, r1=m[0] - (0.4*A[0] + 0.6*A[2])))
        geo = [g for g in gen if g['geometric']]; ctl = [g for g in geo if g['ctrl'] < 0.3]
        isoroot = [i for i in iso if abs(i['r1']) < 0.05 and i['v'] >= 1 and i['gs'] < 1]
        # genuine root check on the gs<1 branch: sign change between adjacent v3 points both with gs<1, v>=1
        br = sorted([i for i in iso if i['gs'] < 1 and i['v'] >= 1], key=lambda i: i['v3'])
        sc = [(a['v3'], b['v3']) for a, b in zip(br, br[1:]) if a['r1']*b['r1'] < 0]
        out['%s_%s' % (MPn, var)] = dict(n_solutions=len(gen), n_geometric=len(geo), n_geometric_controlled=len(ctl),
            min_gs=min([g['gs'] for g in gen], default=None), min_ctrl_geometric=min([g['ctrl'] for g in geo], default=None),
            best_geometric=sorted(geo, key=lambda g: g['ctrl'])[:3], iso_roots=isoroot, iso_signchanges_gs_lt1_branch=sc,
            iso_gs_lt1_r1_range=[min([i['r1'] for i in br], default=None), max([i['r1'] for i in br], default=None)])
print(json.dumps(out, indent=1, default=float))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'z2z6p_scale_dense_results.json'), 'w'), indent=1, default=float)
