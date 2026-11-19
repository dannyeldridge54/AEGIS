"""D1481: independent second-order SR on DILATON32 form A (PREREG_D1481). Uses only the shared Nstar() from tools (read-only)."""
import json, sys, math, mpmath as mp
sys.path.insert(0, '.')
from tools.serapis_calc.nstar import Nstar
mp.mp.dps = 30
s = mp.mpf(3) / 2; Cc = mp.euler + mp.log(2) - 2
def E32(y, x=mp.mpf(1) / 2, nmax=30):
    out = 2 * mp.zeta(2 * s) * y ** s + 2 * mp.sqrt(mp.pi) * mp.gamma(s - mp.mpf(1) / 2) * mp.zeta(2 * s - 1) / mp.gamma(s) * y ** (1 - s)
    pref = 8 * mp.pi ** s / mp.gamma(s) * mp.sqrt(y)
    for n in range(1, nmax + 1):
        sig = sum(mp.mpf(d) ** (1 - 2 * s) for d in range(1, n + 1) if n % d == 0)
        out += pref * mp.mpf(n) ** (s - mp.mpf(1) / 2) * sig * mp.cos(2 * mp.pi * n * x) * mp.besselk(s - mp.mpf(1) / 2, 2 * mp.pi * n * y)
    return out
Er = E32(mp.sqrt(3) / 2)
def V(phi, C):
    e = E32(mp.e ** (mp.sqrt(2) * phi)) - Er
    return e / (e + 1) * (1 + C * e)
def flows(phi, C):
    f = lambda p: V(p, C)
    d0, d1, d2 = f(phi), mp.diff(f, phi, 1), mp.diff(f, phi, 2)
    ev2f = lambda p: 2 * ((mp.diff(f, p, 1) / f(p)) ** 2 - mp.diff(f, p, 2) / f(p))
    Vp = d1 / d0; ev1 = Vp ** 2 / 2; ev2 = ev2f(phi)
    ev3f = lambda p: -mp.diff(ev2f, p) * (mp.diff(f, p, 1) / f(p)) / ev2f(p)
    ev3 = ev3f(phi); ev4 = -mp.diff(ev3f, phi) * Vp / ev3
    return ev1, ev2, ev3, ev4
def obs(phi, C):
    ev1, ev2, ev3, ev4 = flows(phi, C)
    e1 = ev1 * (1 - ev2 / 3); e2 = ev2 * (1 - ev2 / 6 - ev3 / 3); e3 = ev3 * (1 - ev2 / 3 - ev4 / 3); e4 = ev4
    ns = 1 - 2 * e1 - e2 - (3 + 2 * Cc) * e1 * e2 - 2 * e1 ** 2 - Cc * e2 * e3; r = 16 * e1 * (1 + Cc * e2)
    a = -(1 + e1) * (2 * e1 * e2 + e2 * e3) - (3 + 2 * Cc) * e1 * e2 * (e2 + e3) - 4 * e1 ** 2 * e2 - Cc * e2 * e3 * (e3 + e4)
    return float(ns), float(r), float(a)
def background(C, phi0):
    """Exact background in N: phi'' = -(3 - eps)(phi' + V'/V) with eps = phi'^2/2, from slow-roll start; return (N, phi) samples to eps=1."""
    import numpy as np
    from scipy.integrate import solve_ivp
    from scipy.interpolate import CubicSpline
    ys = np.exp(np.sqrt(2) * np.linspace(float(phi0) - 2.2, float(phi0) + 0.6, 1500))
    ph = np.log(ys) / np.sqrt(2); Vv = np.array([float(V(mp.mpf(p), C)) for p in ph])
    S = CubicSpline(ph, Vv); dS = S.derivative()
    def rhs(N, u):
        p, v = u; eps = v * v / 2
        return [v, -(3 - eps) * (v + dS(p) / S(p))]
    v0 = -float(dS(ph[-30]) / S(ph[-30]))
    ev = lambda N, u: u[1] ** 2 / 2 - 1; ev.terminal = True; ev.direction = 1
    sol = solve_ivp(rhs, (0, 400), [ph[-30], v0], events=ev, rtol=1e-10, atol=1e-12, dense_output=True)
    return sol, S
def point(C):
    C = mp.mpf(C)
    sol, S = background(C, mp.log(15) / mp.sqrt(2) + 0.3)
    Nend = sol.t_events[0][0]; phie = sol.sol(Nend)[0]
    N = 50.0
    for _ in range(20):
        phis = sol.sol(Nend - N)[0]
        ns, r, a = obs(mp.mpf(phis), C)
        Nn = Nstar(r, float(S(phis) / S(phie)), 8.94e8)
        if abs(Nn - N) < 1e-3: N = Nn; break
        N = Nn
    phis = sol.sol(Nend - N)[0]; ns, r, a = obs(mp.mpf(phis), C)
    return dict(C=float(C), Nstar=N, phi_star=float(phis), y_star=math.exp(math.sqrt(2) * phis), Ntot_from_start=float(Nend), ns=ns, r=r, alpha_s=a)
if __name__ == '__main__':
    out = {"D": "D1481", "part1": {}, "part2": []}
    ref = {k: json.load(open(f'field_tests/results/DILATON32/{k}.json')) for k in ('A0', 'A1', 'A2')}
    for k, C in (('A0', 0.0), ('A1', 1.25e-6), ('A2', 1e-5)):
        p = point(C); R = ref[k]
        p.update(ms_ns=R['ns'], ms_r=R['r'], ms_alpha=R.get('alpha_s'), ms_Nstar=R.get('Nstar'), d_ns=p['ns'] - R['ns'], d_r_rel=p['r'] / R['r'] - 1)
        out['part1'][k] = p; print(k, json.dumps(p), flush=True)
    ok = all(abs(out['part1'][k]['d_ns']) <= 5e-4 and abs(out['part1'][k]['d_r_rel']) <= 0.02 for k in ('A0', 'A1'))
    out['part1_verdict'] = 'AGREE' if ok else 'DISAGREE'
    import numpy as np
    for C in [0.0] + list(np.logspace(-7, -5, 20)):
        p = point(C); out['part2'].append(p); print('map', json.dumps(p), flush=True)
    json.dump(out, open('field_tests/results/D1481_dilaton_sr.json', 'w'), indent=1); print(out['part1_verdict'])
