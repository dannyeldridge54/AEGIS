#!/usr/bin/env python3
"""D2114: K7 scale tension with one-loop thresholds (asymptotic forms), variants A (paper) and B (corrected v3 slope)."""
import math, json, os
from scipy.optimize import fsolve
aem, s2, MZ, as_ = 127.951, 0.23122, 91.1876, 0.1180
a0 = (0.6*(1 - s2)*aem, s2*aem, 1/as_); b = (33/5, 1, -3)
def alpha_inv(mu): L = math.log(mu/MZ); return [a0[i] - b[i]*L/(2*math.pi) for i in range(3)]
K = (2*math.pi**2*math.sqrt(3))**1.5; ln2 = math.log(2)
def thr(v1, v2, v3, var):
    s3 = 1/16 if var == 'A' else 1/48
    da = 5*(v1 + v2)/(48*math.pi) - 7*v3/(96*math.pi) - 2*ln2/math.pi**2
    db = v2/(6*math.pi) - s3*v3/math.pi - 41*ln2/(24*math.pi**2)
    dc = v1/(6*math.pi) - s3*v3/math.pi - 41*ln2/(24*math.pi**2)
    return da, db, dc
def model(v1, v2, v3, gs, MP, var):
    T = math.sqrt(v1*v2*v3)/K/(4*gs); Ms = MP*gs/math.sqrt(4*math.pi*v1*v2*v3)
    da, db, dc = thr(v1, v2, v3, var); return T, Ms, (T + da, T + db, T + dc)
def resid(x, v3, MP, var, iso):
    v1, v2, lg = (math.exp(x[0]), math.exp(x[0]), x[1]) if iso else (math.exp(x[0]), math.exp(x[1]), x[2]); gs = math.exp(lg)
    T, Ms, (A4, Ab, Ac) = model(v1, v2, v3, gs, MP, var); m = alpha_inv(Ms)
    r = [m[2] - A4, m[1] - Ab, m[0] - (0.4*A4 + 0.6*Ac)]
    return r[:2] if iso else r
out = {}
for MPn, MP in (('reduced', 2.435e18), ('nonreduced', 1.221e19)):
    for var in ('A', 'B'):
        # (i) isotropic: unknowns v, v3, gs with M_s fixed by data -> solve over (v, lg) for each v3 and pick v3 where alpha1 eq holds
        iso = []
        for v3 in [1, 3, 10, 30, 100, 300, 1000, 3000, 1e4, 3e4, 1e5]:
            best = None
            for g0 in (-6, -3, -1):
                for v0 in (2, 50, 500, 5000):
                    x, info, ok, _ = fsolve(resid, [math.log(v0), g0], args=(v3, MP, var, True), full_output=True)
                    if ok == 1 and max(abs(r) for r in resid(x, v3, MP, var, True)) < 1e-6:
                        x = [math.exp(x[0]), x[1]]
                        T, Ms, A = model(x[0], x[0], v3, math.exp(x[1]), MP, var); m = alpha_inv(Ms)
                        r1 = m[0] - (0.4*A[0] + 0.6*A[2]); best = (abs(r1), dict(v3=v3, v=x[0], gs=math.exp(x[1]), Ms=Ms, T=T, alpha1_resid=r1)); break
                if best: break
            if best: iso.append(best[1])
        sols_i = [s for s in iso if abs(s['alpha1_resid']) < 0.05 and s['v'] >= 1 and s['v3'] >= 1 and 0 < s['gs'] < 1]
        for s1, s2 in zip(iso, iso[1:]):
            if s1['alpha1_resid']*s2['alpha1_resid'] < 0 and min(s1['v'], s2['v']) >= 1 and max(s1['gs'], s2['gs']) < 1:
                sols_i.append({'bracket_v3': [s1['v3'], s2['v3']], 'v': [s1['v'], s2['v']], 'gs': [s1['gs'], s2['gs']], 'Ms': [s1['Ms'], s2['Ms']]})
        sgn = [round(s['alpha1_resid'], 2) for s in iso]
        gen = []
        for v3 in [1, 3, 10, 30, 100, 300, 1000, 3000, 1e4, 3e4, 1e5, 3e5]:
            for g0 in (-6, -4, -2):
                for v0 in ((2, 2), (300, 2), (300, 50), (3000, 300)):
                    x, info, ok, _ = fsolve(resid, [math.log(v0[0]), math.log(v0[1]), g0], args=(v3, MP, var, False), full_output=True)
                    if ok == 1 and max(abs(r) for r in resid(x, v3, MP, var, False)) < 1e-6:
                        x = [math.exp(x[0]), math.exp(x[1]), x[2]]
                        gs = math.exp(x[2]); T, Ms, A = model(x[0], x[1], v3, gs, MP, var); d = thr(x[0], x[1], v3, var)
                        gen.append(dict(v3=v3, v1=x[0], v2=x[1], gs=gs, Ms=Ms, T=T, ctrl=max(abs(t) for t in d)/T,
                                        geometric=bool(min(x[0], x[1], v3) >= 1 and 0 < gs < 1))); break
                else: continue
                break
        out['%s_%s' % (MPn, var)] = {'iso_scan_alpha1_residual_by_v3': list(zip([s['v3'] for s in iso], sgn)), 'iso_PASS': bool(sols_i), 'iso_solutions': sols_i,
                                     'general': gen, 'general_PASS': any(g['geometric'] for g in gen),
                                     'general_controlled(ctrl<0.3)': [g for g in gen if g['geometric'] and g['ctrl'] < 0.3]}
print(json.dumps(out, indent=1, default=lambda o: float(o)))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'z2z6p_scale_results.json'), 'w'), indent=1, default=float)
