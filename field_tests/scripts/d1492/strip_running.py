"""D1492: alpha_s, beta_s across the DILMIX in-band strip (PREREG_D1492)."""
import json, sys, math
M = {}; exec(open('field_tests/scripts/d1485/dilmix_sr.py').read().split("if __name__")[0], M)
mp, np = M['mp'], M['np']
def eps(V, phi):
    c = mp.taylor(V, phi, 4); V0, V1, V2, V3, V4 = [c[k] * mp.factorial(k) for k in range(5)]
    ev1 = (V1 / V0) ** 2 / 2; ev2 = 2 * ((V1 / V0) ** 2 - V2 / V0)
    ev3 = V1 * (-V0**2 * V3 + 3 * V0 * V1 * V2 - 2 * V1**3) / (V0**2 * (V0 * V2 - V1**2))
    ev4 = ((-V0**4*V1*V2*V4 + V0**4*V1*V3**2 - V0**4*V2**2*V3 + V0**3*V1**3*V4 + 6*V0**3*V1*V2**3 - V0**2*V1**4*V3
            - 14*V0**2*V1**3*V2**2 + 13*V0*V1**5*V2 - 4*V1**7) / (V0**2 * (V0**3*V2*V3 - V0**2*V1**2*V3 - 3*V0**2*V1*V2**2 + 5*V0*V1**3*V2 - 2*V1**5)))
    e1 = ev1 * (1 - ev2 / 3); e2 = ev2 * (1 - ev2 / 6 - ev3 / 3); e3 = ev3 * (1 - ev2 / 3 - ev4 / 3); e4 = ev4
    return [float(e1), float(e2), float(e3), float(e4)]
def phistar(al, C):
    from scipy.integrate import solve_ivp
    from scipy.interpolate import CubicSpline
    PH = M['PH']; x = M['XG']; P = al * x / (1 + x) + (1 - al) * (1 - 1 / (1 + x) ** 2); Vv = P * (1 + C * P / (1 - P))
    Sp = CubicSpline(PH, Vv); dS = Sp.derivative()
    Nsr = np.concatenate([[0], np.cumsum((Sp(PH[1:]) / np.maximum(dS(PH[1:]), 1e-300)) * np.diff(PH))])
    i0 = min(int(np.searchsorted(Nsr, 200.0)), len(PH) - 5)
    rhs = lambda N, u: [u[1], -(3 - u[1] ** 2 / 2) * (u[1] + dS(u[0]) / Sp(u[0]))]
    ev = lambda N, u: u[1] ** 2 / 2 - 1; ev.terminal = True; ev.direction = 1
    sol = solve_ivp(rhs, (0, 600), [PH[i0], -float(dS(PH[i0]) / Sp(PH[i0]))], events=ev, rtol=1e-10, atol=1e-12, dense_output=True)
    Nend = sol.t_events[0][0]; phie = sol.sol(Nend)[0]; V = M['Vfun'](al, C); N = 50.0
    for _ in range(25):
        phis = sol.sol(Nend - N)[0]; ns, r, a = M['obs'](V, mp.mpf(phis))
        Nn = M['Nstar'](r, float(Sp(phis) / Sp(phie)), 8.94e8)
        if abs(Nn - N) < 1e-3: N = Nn; break
        N = Nn
    return V, mp.mpf(sol.sol(Nend - N)[0]), N
SER = {"rho_A1": (-9.9796e-4, -2.8598e-5), "tau_i_NA12": (-8.5430e-4, -3.1256e-5)}
pts = [(0.25, 1.25e-6), (0.5, 1.25e-6), (0.25, 1.5e-6), (0.375, 1e-6), (0.375, 1.5e-6), (0.375, 2e-6), (0.5, 1.5e-6)]
out = {"D": "D1492", "points": []}
for al, C in pts:
    V, phi, N = phistar(al, C); ns, r, a = M['obs'](V, phi); e = eps(V, phi)
    b = -(1 + e[0]) * (2 * e[0] * e[1] * (e[1] + e[2]) + e[1] * e[2] * (e[2] + e[3]))
    row = dict(alpha=al, C=C, Nstar=N, ns=ns, r=r, alpha_s=a, beta_s=b, eps=e,
               dalpha_vs_rho_sigSO=(a - SER['rho_A1'][0]) / 3.3e-3, dalpha_vs_tau_sigSO=(a - SER['tau_i_NA12'][0]) / 3.3e-3)
    out['points'].append(row); print(json.dumps(row), flush=True)
A = [p['alpha_s'] for p in out['points']]; B = [p['beta_s'] for p in out['points']]
out['alpha_range'] = [min(A), max(A)]; out['beta_range'] = [min(B), max(B)]
json.dump(out, open('field_tests/results/D1492_strip_running.json', 'w'), indent=1); print('done', out['alpha_range'], out['beta_range'])
