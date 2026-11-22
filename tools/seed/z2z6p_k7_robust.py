#!/usr/bin/env python3
"""D2123: K7 robustness - 2-loop SM->MSSM running, DR-bar, SUSY scale, exotics, v bounds, readings."""
import math, json, os, numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize, fsolve
MZ = 91.1876; aem, s2, as_ = 127.951, 0.23122, 0.1180
a0 = np.array([0.6*(1 - s2)*aem, s2*aem, 1/as_])
bSM = np.array([41/10, -19/6, -7]); BSM = np.array([[199/50, 27/10, 44/5], [9/10, 35/6, 12], [11/10, 9/2, -26]]); aSM = np.array([17/10, 3/2, 2])
bMS = np.array([33/5, 1, -3]); BMS = np.array([[199/25, 27/5, 88/5], [9/5, 25, 24], [11/5, 9, 14]]); aMS = np.array([26/5, 6, 4])
def rge(t, y, b, B, a, susy):
    ai = y[:3]; yt = y[3]; al = 1/ai; g2 = 4*math.pi*al
    d = -b/(2*math.pi) - (B @ g2 - a*yt**2)/(32*math.pi**3)
    if susy: dyt = yt/(16*math.pi**2)*(6*yt**2 - 16/3*g2[2] - 3*g2[1] - 13/15*g2[0])
    else: dyt = yt/(16*math.pi**2)*(4.5*yt**2 - 8*g2[2] - 9/4*g2[1] - 17/20*g2[0])
    return np.concatenate([d, [dyt]])
def table(Msusy):
    t1 = math.log(Msusy/MZ)
    s = solve_ivp(rge, [0, t1], np.concatenate([a0, [0.94]]), args=(bSM, BSM, aSM, False), rtol=1e-10, atol=1e-12)
    y = s.y[:, -1].copy(); y[:3] -= np.array([0, 2, 3])/(12*math.pi)
    ts = np.linspace(t1, math.log(1e19/MZ), 4000)
    s2_ = solve_ivp(rge, [t1, ts[-1]], y, args=(bMS, BMS, aMS, True), t_eval=ts, rtol=1e-10, atol=1e-12)
    return ts, s2_.y[:3]
def one_loop(mu): L = math.log(mu/MZ); return a0 - bMS*L/(2*math.pi)
K = (2*math.pi**2*math.sqrt(3))**1.5; ln2 = math.log(2); nrm = 2*math.pi
def thr(v1, v2, v3, var):
    s3 = 1/16 if var == 'A' else 1/48
    return nrm*np.array([5*(v1 + v2)/(48*math.pi) - 7*v3/(96*math.pi) - 2*ln2/math.pi**2,
                         v2/(6*math.pi) - s3*v3/math.pi - 41*ln2/(24*math.pi**2), v1/(6*math.pi) - s3*v3/math.pi - 41*ln2/(24*math.pi**2)])
def make(case):
    MP = 2.435e18
    if case['run'] == '1loop': ainv = one_loop
    else:
        ts, Y = table(case['Msusy'])
        ainv = lambda mu: np.array([np.interp(math.log(mu/MZ), ts, Y[i]) for i in range(3)])
    shift = -np.array([4.6, 5, 4])*math.log(100)/(2*math.pi) if case.get('exotics') else np.zeros(3)
    def parts(x):
        v1, v2, v3, gs = np.exp(x); T = math.sqrt(v1*v2*v3)/K/(4*gs); Ms = MP*gs/math.sqrt(4*math.pi*v1*v2*v3)
        return v1, v2, v3, gs, T, Ms, thr(v1, v2, v3, case['var'])
    def res(x):
        try:
            v1, v2, v3, gs, T, Ms, d = parts(x)
            if not (MZ*10 < Ms < 1e19): return np.array([1e6]*3)
            m = ainv(Ms) + shift; A4, Ab, Ac = T + d
            return np.array([m[2] - A4, m[1] - Ab, m[0] - (0.4*A4 + 0.6*Ac)])
        except Exception: return np.array([1e6]*3)
    def ctrl(x):
        try: v1, v2, v3, gs, T, Ms, d = parts(x); return max(abs(d))/T
        except Exception: return 1e6
    return parts, res, ctrl
rng = np.random.default_rng(2123)
CASES = {'R0': dict(run='1loop', var='A', vmin=1), 'R1': dict(run='2loop', Msusy=1e3, var='A', vmin=1), 'R2': dict(run='2loop', Msusy=1e4, var='A', vmin=1),
         'R3': dict(run='2loop', Msusy=1e3, var='A', vmin=1, exotics=True), 'R4': dict(run='2loop', Msusy=1e3, var='A', vmin=0.5),
         'R5': dict(run='2loop', Msusy=1e3, var='A', vmin=0.25), 'R6': dict(run='2loop', Msusy=1e3, var='B', vmin=1)}
out = {}
for name, case in CASES.items():
    parts, res, ctrl = make(case); lv = math.log(case['vmin']); best = None
    for _ in range(40):
        x0 = [rng.uniform(lv, 8), rng.uniform(lv, 6), rng.uniform(lv, 9), rng.uniform(-7, -1)]
        r = minimize(ctrl, x0, method='SLSQP', constraints=[{'type': 'eq', 'fun': res},
                     {'type': 'ineq', 'fun': lambda x: np.array([x[0] - lv, x[1] - lv, x[2] - lv, -x[3] - 1e-9])}], options={'maxiter': 500, 'ftol': 1e-10})
        if not r.success: continue
        v3l = r.x[2]; f = lambda y: res([y[0], y[1], v3l, y[2]])
        y, info, ok, _ = fsolve(f, [r.x[0], r.x[1], r.x[3]], full_output=True, xtol=1e-13); xx = [y[0], y[1], v3l, y[2]]
        if ok != 1 or max(abs(res(xx))) > 1e-9 or min(xx[:3]) < lv - 1e-9 or xx[3] >= 0: continue
        c = ctrl(xx)
        if best is None or c < best[0]: best = (c, xx)
    if best:
        v1, v2, v3, gs, T, Ms, d = parts(best[1]); out[name] = dict(case=case, min_ctrl=best[0], v=[v1, v2, v3], gs=gs, Ms=Ms, controlled=best[0] < 0.3)
    else: out[name] = dict(case=case, result='no verified solution')
rob = all(out[k].get('min_ctrl', 9) >= 0.3 for k in ('R0', 'R1', 'R2', 'R3'))
out['ITEM9'] = 'FAIL (robust)' if rob else 'not robust: ' + ','.join(k for k in ('R0', 'R1', 'R2', 'R3') if out[k].get('min_ctrl', 9) < 0.3)
print(json.dumps(out, indent=1, default=float))
