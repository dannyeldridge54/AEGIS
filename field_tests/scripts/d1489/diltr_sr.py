"""D1489: DILTR reheating-sensitivity forecast (PREREG_D1489)."""
import json, sys, math, mpmath as mp
sys.path.insert(0, '.')
A = {}; exec(open('field_tests/scripts/d1481/sr_check.py').read().split("if __name__")[0], A)
M = {}; exec(open('field_tests/scripts/d1485/dilmix_sr.py').read().split("if __name__")[0], M)
def pointA(C, TR):
    C = mp.mpf(C); sol, S = A['background'](C, mp.log(15) / mp.sqrt(2) + 0.3)
    Nend = sol.t_events[0][0]; phie = sol.sol(Nend)[0]; N = 50.0
    for _ in range(25):
        phis = sol.sol(Nend - N)[0]; ns, r, a = A['obs'](mp.mpf(phis), C)
        Nn = A['Nstar'](r, float(S(phis) / S(phie)), TR)
        if abs(Nn - N) < 1e-3: N = Nn; break
        N = Nn
    phis = sol.sol(Nend - N)[0]; ns, r, a = A['obs'](mp.mpf(phis), C)
    return dict(C=float(C), TR=TR, Nstar=N, ns=ns, r=r, alpha_s=a)
def pointM(al, C, TR):
    import numpy as np
    from scipy.integrate import solve_ivp
    from scipy.interpolate import CubicSpline
    x = M['XG']; P = al * x / (1 + x) + (1 - al) * (1 - 1 / (1 + x) ** 2); Vv = P * (1 + C * P / (1 - P))
    Sp = CubicSpline(M['PH'], Vv); dS = Sp.derivative(); PH = M['PH']
    Nsr = np.concatenate([[0], np.cumsum((Sp(PH[1:]) / np.maximum(dS(PH[1:]), 1e-300)) * np.diff(PH))])
    i0 = min(int(np.searchsorted(Nsr, 200.0)), len(PH) - 5)
    rhs = lambda N, u: [u[1], -(3 - u[1] ** 2 / 2) * (u[1] + dS(u[0]) / Sp(u[0]))]
    ev = lambda N, u: u[1] ** 2 / 2 - 1; ev.terminal = True; ev.direction = 1
    sol = solve_ivp(rhs, (0, 600), [PH[i0], -float(dS(PH[i0]) / Sp(PH[i0]))], events=ev, rtol=1e-10, atol=1e-12, dense_output=True)
    Nend = sol.t_events[0][0]; phie = sol.sol(Nend)[0]; V = M['Vfun'](al, C); N = 50.0
    for _ in range(25):
        phis = sol.sol(Nend - N)[0]; ns, r, a = M['obs'](V, mp.mpf(phis))
        Nn = M['Nstar'](r, float(Sp(phis) / Sp(phie)), TR)
        if abs(Nn - N) < 1e-3: N = Nn; break
        N = Nn
    phis = sol.sol(Nend - N)[0]; ns, r, a = M['obs'](V, mp.mpf(phis))
    return dict(alpha=al, C=C, TR=TR, Nstar=N, ns=ns, r=r, alpha_s=a)
band = lambda p: 0.969 <= p['ns'] <= 0.975 and 4.55e-4 <= p['r'] <= 5.7e-4
near = lambda p: abs(min(max(p['ns'], 0.969), 0.975) - p['ns']) <= 0.003 and 4.55e-4 / 1.3 <= p['r'] <= 5.7e-4 * 1.3
out = {"D": "D1489", "formA": {}, "dilmix_best": {}}
for C in (0.0, 1.25e-6):
    ref = pointA(C, 8.94e8); rows = [ref]
    for TR in (1e8, 1e10):
        p = pointA(C, TR); p.update(d_ns=p['ns'] - ref['ns'], d_r_rel=p['r'] / ref['r'] - 1); rows.append(p)
    for p in rows: p.update(in_band=band(p), near=near(p))
    rob = all(abs(p.get('d_ns', 0)) <= 0.002 and abs(p.get('d_r_rel', 0)) <= 0.10 for p in rows)
    out['formA'][f'C{C:g}'] = dict(rows=rows, verdict='robust' if rob else 'reheating-sensitive'); print('A', C, json.dumps(out['formA'][f'C{C:g}']), flush=True)
ref = pointM(0.375, 1.5e-6, 8.94e8); rows = [ref]
for TR in (1e8, 1e10):
    p = pointM(0.375, 1.5e-6, TR); p.update(d_ns=p['ns'] - ref['ns'], d_r_rel=p['r'] / ref['r'] - 1); rows.append(p)
for p in rows: p.update(in_band=band(p), near=near(p))
out['dilmix_best'] = dict(rows=rows, stays_in_band=all(p['in_band'] for p in rows)); print('M', json.dumps(out['dilmix_best']), flush=True)
json.dump(out, open('field_tests/results/D1489_diltr_sr.json', 'w'), indent=1); print('done')
