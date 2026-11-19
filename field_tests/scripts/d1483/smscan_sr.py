"""D1483: independent second-order SR on the SMSCAN family (PREREG_D1483)."""
import json, sys, math, mpmath as mp, numpy as np
sys.path.insert(0, '.')
from tools.serapis_calc.nstar import Nstar
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
mp.mp.dps = 30
Cc = mp.euler + mp.log(2) - 2
def Es(y, s, x=mp.mpf(1) / 2, nmax=40):
    out = 2 * mp.zeta(2 * s) * y ** s + 2 * mp.sqrt(mp.pi) * mp.gamma(s - mp.mpf(1) / 2) * mp.zeta(2 * s - 1) / mp.gamma(s) * y ** (1 - s)
    pref = 8 * mp.pi ** s / mp.gamma(s) * mp.sqrt(y)
    for n in range(1, nmax + 1):
        if 2 * mp.pi * n * y > 80: break
        sig = sum(mp.mpf(d) ** (1 - 2 * s) for d in range(1, n + 1) if n % d == 0)
        out += pref * mp.mpf(n) ** (s - mp.mpf(1) / 2) * sig * mp.cos(2 * mp.pi * n * x) * mp.besselk(s - mp.mpf(1) / 2, 2 * mp.pi * n * y)
    return out
def point(s, m):
    s, m = mp.mpf(s), mp.mpf(m); Er = Es(mp.sqrt(3) / 2, s)
    V = lambda p: 1 - (Er / Es(mp.e ** (mp.sqrt(2) * p), s)) ** m
    def flows(phi):
        ev2f = lambda p: 2 * ((mp.diff(V, p, 1) / V(p)) ** 2 - mp.diff(V, p, 2) / V(p))
        Vp = mp.diff(V, phi) / V(phi); ev1 = Vp ** 2 / 2; ev2 = ev2f(phi)
        ev3f = lambda p: -mp.diff(ev2f, p) * (mp.diff(V, p, 1) / V(p)) / ev2f(p)
        ev3 = ev3f(phi); ev4 = -mp.diff(ev3f, phi) * Vp / ev3
        return ev1, ev2, ev3, ev4
    def obs(phi):
        ev1, ev2, ev3, ev4 = flows(phi)
        e1 = ev1 * (1 - ev2 / 3); e2 = ev2 * (1 - ev2 / 6 - ev3 / 3); e3 = ev3 * (1 - ev2 / 3 - ev4 / 3); e4 = ev4
        ns = 1 - 2 * e1 - e2 - (3 + 2 * Cc) * e1 * e2 - 2 * e1 ** 2 - Cc * e2 * e3; r = 16 * e1 * (1 + Cc * e2)
        a = -(1 + e1) * (2 * e1 * e2 + e2 * e3) - (3 + 2 * Cc) * e1 * e2 * (e2 + e3) - 4 * e1 ** 2 * e2 - Cc * e2 * e3 * (e3 + e4)
        return float(ns), float(r), float(a)
    # background on a grid from just above the vacuum to deep plateau; start where 150-250 e-folds remain (SR estimate), then exact ODE
    ph = np.linspace(float(mp.log(mp.sqrt(3) / 2) / mp.sqrt(2)) + 1e-3, float(mp.log(4000) / mp.sqrt(2)), 2500)
    Vv = np.array([float(V(mp.mpf(p))) for p in ph]); Sp = CubicSpline(ph, Vv); dS = Sp.derivative()
    Nsr = np.concatenate([[0], np.cumsum((Sp(ph[1:]) / np.maximum(dS(ph[1:]), 1e-300)) * np.diff(ph))])
    i0 = min(int(np.searchsorted(Nsr, 200.0)), len(ph) - 5)
    def rhs(N, u):
        p, v = u; eps = v * v / 2
        return [v, -(3 - eps) * (v + dS(p) / Sp(p))]
    ev = lambda N, u: u[1] ** 2 / 2 - 1; ev.terminal = True; ev.direction = 1
    sol = solve_ivp(rhs, (0, 600), [ph[i0], -float(dS(ph[i0]) / Sp(ph[i0]))], events=ev, rtol=1e-10, atol=1e-12, dense_output=True)
    Nend = sol.t_events[0][0]; phie = sol.sol(Nend)[0]; N = 50.0
    for _ in range(20):
        phis = sol.sol(Nend - N)[0]; ns, r, a = obs(mp.mpf(phis))
        Nn = Nstar(r, float(Sp(phis) / Sp(phie)), 8.94e8)
        if abs(Nn - N) < 1e-3: N = Nn; break
        N = Nn
    phis = sol.sol(Nend - N)[0]; ns, r, a = obs(mp.mpf(phis))
    inb = 0.969 <= ns <= 0.975 and 4.55e-4 <= r <= 5.7e-4
    near = abs(min(max(ns, 0.969), 0.975) - ns) <= 0.003 and 4.55e-4 / 1.3 <= r <= 5.7e-4 * 1.3
    return dict(s=float(s), m=float(m), sm=float(s * m), Nstar=N, y_star=math.exp(math.sqrt(2) * phis), Ntot=float(Nend),
                ns=ns, r=r, alpha_s=a, in_band=bool(inb), near=bool(near))
if __name__ == '__main__':
    out = {"D": "D1483", "part1": {}, "part2": {}}
    for s, m, f in ((2, 0.5, 's2_m0.5'), (2, 1, 's2_m1'), (3, mp.mpf(1) / 3, 's3_m0.3333')):
        p = point(s, m); R = json.load(open(f'field_tests/results/SMSCAN/{f}.json'))
        p.update(ms_ns=R['ns'], ms_r=R['r'], ms_alpha=R['alpha_s'], ms_Nstar=R['Nstar'], d_ns=p['ns'] - R['ns'], d_r_rel=p['r'] / R['r'] - 1)
        out['part1'][f] = p; print(f, json.dumps(p), flush=True)
    out['part1_verdict'] = 'AGREE' if all(abs(v['d_ns']) <= 5e-4 and abs(v['d_r_rel']) <= 0.02 for v in out['part1'].values()) else 'DISAGREE'
    for s, m in ((3, mp.mpf(2) / 3), (3, 1), (2, mp.mpf(3) / 2), (1.5, 1), (1.5, mp.mpf(4) / 3)):
        p = point(s, m); out['part2'][f's{float(s):g}_m{float(m):.4g}'] = p; print('forecast', json.dumps(p), flush=True)
    json.dump(out, open('field_tests/results/D1483_smscan_sr.json', 'w'), indent=1); print(out['part1_verdict'])
