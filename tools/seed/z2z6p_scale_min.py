#!/usr/bin/env python3
"""D2119 (R1-1/R1-2/R1-3): minimise ctrl=max|delta|/T over the matching curve; norms 2pi (primary) and 1."""
import math, json, os, numpy as np
from scipy.optimize import minimize, fsolve
aem, s2, MZ, as_ = 127.951, 0.23122, 91.1876, 0.1180
a0 = (0.6*(1 - s2)*aem, s2*aem, 1/as_); b = (33/5, 1, -3)
K = (2*math.pi**2*math.sqrt(3))**1.5; ln2 = math.log(2)
def ainv(mu): L = math.log(mu/MZ); return [a0[i] - b[i]*L/(2*math.pi) for i in range(3)]
def thr(v1, v2, v3, var, nrm):
    s3 = 1/16 if var == 'A' else 1/48
    da = 5*(v1 + v2)/(48*math.pi) - 7*v3/(96*math.pi) - 2*ln2/math.pi**2
    db = v2/(6*math.pi) - s3*v3/math.pi - 41*ln2/(24*math.pi**2)
    dc = v1/(6*math.pi) - s3*v3/math.pi - 41*ln2/(24*math.pi**2)
    return nrm*da, nrm*db, nrm*dc
def parts(x, MP, var, nrm):
    v1, v2, v3, gs = math.exp(x[0]), math.exp(x[1]), math.exp(x[2]), math.exp(x[3])
    T = math.sqrt(v1*v2*v3)/K/(4*gs); Ms = MP*gs/math.sqrt(4*math.pi*v1*v2*v3); d = thr(v1, v2, v3, var, nrm)
    return v1, v2, v3, gs, T, Ms, d
def res(x, MP, var, nrm):
    try:
        v1, v2, v3, gs, T, Ms, d = parts(x, MP, var, nrm); m = ainv(Ms)
        A4, Ab, Ac = T + d[0], T + d[1], T + d[2]
        return np.array([m[2] - A4, m[1] - Ab, m[0] - (0.4*A4 + 0.6*Ac)])
    except (ValueError, OverflowError, ZeroDivisionError): return np.array([1e6]*3)
def ctrl(x, MP, var, nrm):
    try: v1, v2, v3, gs, T, Ms, d = parts(x, MP, var, nrm); return max(abs(t) for t in d)/T
    except Exception: return 1e6
rng = np.random.default_rng(2119); out = {}
for nrm_n, nrm in (('2pi', 2*math.pi), ('1', 1.0)):
    for MPn, MP in (('reduced', 2.435e18), ('nonreduced', 1.221e19)):
        for var in ('A', 'B'):
            best = None
            for _ in range(40):
                x0 = [rng.uniform(0, 9), rng.uniform(0, 6), rng.uniform(0, 10), rng.uniform(-4, 0)]
                r = minimize(ctrl, x0, args=(MP, var, nrm), method='SLSQP',
                             constraints=[{'type': 'eq', 'fun': res, 'args': (MP, var, nrm)},
                                          {'type': 'ineq', 'fun': lambda x: np.array([x[0], x[1], x[2], -x[3] - 1e-9])}],
                             options={'maxiter': 500, 'ftol': 1e-10})
                if not r.success: continue
                # re-verify on the curve: hold v3 fixed, fsolve the other three
                v3l = r.x[2]
                f = lambda y: res([y[0], y[1], v3l, y[2]], MP, var, nrm)
                y, info, ok, _ = fsolve(f, [r.x[0], r.x[1], r.x[3]], full_output=True, xtol=1e-13)
                xx = [y[0], y[1], v3l, y[2]]
                if ok != 1 or max(abs(res(xx, MP, var, nrm))) > 1e-10 or min(xx[:3]) < -1e-9 or xx[3] >= 0: continue
                c = ctrl(xx, MP, var, nrm)
                if best is None or c < best[0]: best = (c, xx)
            key = '%s_%s_%s' % (var, MPn, nrm_n)
            if best:
                v1, v2, v3, gs, T, Ms, d = parts(best[1], MP, var, nrm)
                out[key] = dict(min_ctrl=best[0], v=[v1, v2, v3], gs=gs, Ms=Ms, T=T, controlled=best[0] < 0.3)
            else: out[key] = 'no verified geometric solution'
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'z2z6p_scale_min_results.json'), 'w'), indent=1)
