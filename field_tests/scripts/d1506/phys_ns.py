"""D1506: physical-frame n_s, r (PREREG_D1506)."""
import json, math, numpy as np, mpmath as mp
M = {}; exec(open('field_tests/scripts/d1485/dilmix_sr.py').read().split("PH = ")[0], M)   # E32 (memoised), Er, Nstar, solve_ivp, CubicSpline
src = open('field_tests/scripts/d1485/dilmix_sr.py').read(); exec('def obs' + src.split('def obs')[1].split('def point')[0], M)
E32, Er, obs, Nstar = M['E32'], M['Er'], M['obs'], M['Nstar']
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
def point(al, C, lam):
    al, C, lam = float(al), float(C), float(lam)
    ymax = 400 * (1 / lam) ** (2 / 3)
    PH = np.linspace(float(mp.log(mp.sqrt(3) / 2) / mp.sqrt(2)) + 1e-3, math.log(ymax) / math.sqrt(2), 3000)
    x = lam * np.array([float(E32(mp.e ** (mp.sqrt(2) * mp.mpf(p))) - Er) for p in PH])
    P = al * x / (1 + x) + (1 - al) * (1 - 1 / (1 + x) ** 2); Vv = P * (1 + (C / lam) * P / (1 - P))
    Sp = CubicSpline(PH, Vv); dS = Sp.derivative()
    Nsr = np.concatenate([[0], np.cumsum((Sp(PH[1:]) / np.maximum(dS(PH[1:]), 1e-300)) * np.diff(PH))])
    i0 = min(int(np.searchsorted(Nsr, 200.0)), len(PH) - 5)
    rhs = lambda N, u: [u[1], -(3 - u[1] ** 2 / 2) * (u[1] + dS(u[0]) / Sp(u[0]))]
    ev = lambda N, u: u[1] ** 2 / 2 - 1; ev.terminal = True; ev.direction = 1
    sol = solve_ivp(rhs, (0, 600), [PH[i0], -float(dS(PH[i0]) / Sp(PH[i0]))], events=ev, rtol=1e-10, atol=1e-12, dense_output=True)
    Nend = sol.t_events[0][0]; phie = sol.sol(Nend)[0]
    la, Cm, alm = mp.mpf(lam), mp.mpf(C), mp.mpf(al)
    def V(p):
        xx = la * (E32(mp.e ** (mp.sqrt(2) * p)) - Er); PP = alm * xx / (1 + xx) + (1 - alm) * (1 - 1 / (1 + xx) ** 2)
        return PP * (1 + (Cm / la) * PP / (1 - PP))
    N = 50.0
    for _ in range(25):
        phis = sol.sol(Nend - N)[0]; ns, r, a = obs(V, mp.mpf(phis))
        Nn = Nstar(r, float(Sp(phis) / Sp(phie)), 8.94e8)
        if abs(Nn - N) < 1e-3: N = Nn; break
        N = Nn
    phis = sol.sol(Nend - N)[0]; ns, r, a = obs(V, mp.mpf(phis))
    return dict(alpha=al, C=C, lam=lam, Nstar=N, y_star=math.exp(math.sqrt(2) * phis), ns=ns, r=r, alpha_s=a,
                x_star=lam * float(E32(mp.e ** (mp.sqrt(2) * mp.mpf(phis))) - Er))
out = {"D": "D1506", "rows": []}
for al, C in ((0.375, 1.5e-6), (1.0, 1.25e-6)):
    ref = point(al, C, 1.0); ref['verdict'] = 'reference'; out['rows'].append(ref); print(json.dumps(ref), flush=True)
    for a in (1993.29, 9930.90, 49618.94):
        p = point(al, C, 1 / a); p['d_ns'] = p['ns'] - ref['ns']; p['d_r_rel'] = p['r'] / ref['r'] - 1
        p['verdict'] = 'lambda=1 adequate' if abs(p['d_ns']) <= 5e-4 and abs(p['d_r_rel']) <= 0.02 else 'frame-dependent'
        out['rows'].append(p); print(json.dumps(p), flush=True)
        json.dump(out, open('field_tests/results/D1506_phys_frame_ns.json', 'w'), indent=1)
json.dump(out, open('field_tests/results/D1506_phys_frame_ns.json', 'w'), indent=1); print('done')
