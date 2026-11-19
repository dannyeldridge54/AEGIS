"""D1485: independent SR forecast + band map for DILMIX (PREREG_D1485)."""
import json, sys, math, mpmath as mp, numpy as np
sys.path.insert(0, '.')
from tools.serapis_calc.nstar import Nstar
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
mp.mp.dps = 25
S = mp.mpf(3) / 2; Cc = mp.euler + mp.log(2) - 2
SIG = {n: sum(mp.mpf(d) ** (1 - 2 * S) for d in range(1, n + 1) if n % d == 0) for n in range(1, 41)}
_EC = {}
def E32(y, x=mp.mpf(1) / 2):
    key = mp.mpf(y)._mpf_
    if key in _EC: return _EC[key]
    _EC[key] = _E32(y, x); return _EC[key]
def _E32(y, x):
    out = 2 * mp.zeta(2 * S) * y ** S + 2 * mp.sqrt(mp.pi) * mp.gamma(S - mp.mpf(1) / 2) * mp.zeta(2 * S - 1) / mp.gamma(S) * y ** (1 - S)
    pref = 8 * mp.pi ** S / mp.gamma(S) * mp.sqrt(y)
    for n in range(1, 41):
        if 2 * mp.pi * n * y > 80: break
        sig = SIG[n]
        out += pref * mp.mpf(n) ** (S - mp.mpf(1) / 2) * sig * mp.cos(2 * mp.pi * n * x) * mp.besselk(S - mp.mpf(1) / 2, 2 * mp.pi * n * y)
    return out
Er = E32(mp.sqrt(3) / 2)
PH = np.linspace(float(mp.log(mp.sqrt(3) / 2) / mp.sqrt(2)) + 1e-3, float(mp.log(400) / mp.sqrt(2)), 2500)
XG = np.array([float(E32(mp.e ** (mp.sqrt(2) * mp.mpf(p))) - Er) for p in PH])
def Vfun(al, C):
    al, C = mp.mpf(al), mp.mpf(C)
    def V(p):
        x = E32(mp.e ** (mp.sqrt(2) * p)) - Er
        P = al * x / (1 + x) + (1 - al) * (1 - 1 / (1 + x) ** 2)
        return P * (1 + C * P / (1 - P))
    return V
def obs(V, phi):
    ev2f = lambda p: 2 * ((mp.diff(V, p, 1) / V(p)) ** 2 - mp.diff(V, p, 2) / V(p))
    Vp = mp.diff(V, phi) / V(phi); ev1 = Vp ** 2 / 2; ev2 = ev2f(phi)
    ev3f = lambda p: -mp.diff(ev2f, p) * (mp.diff(V, p, 1) / V(p)) / ev2f(p)
    ev3 = ev3f(phi); ev4 = -mp.diff(ev3f, phi) * Vp / ev3
    e1 = ev1 * (1 - ev2 / 3); e2 = ev2 * (1 - ev2 / 6 - ev3 / 3); e3 = ev3 * (1 - ev2 / 3 - ev4 / 3); e4 = ev4
    ns = 1 - 2 * e1 - e2 - (3 + 2 * Cc) * e1 * e2 - 2 * e1 ** 2 - Cc * e2 * e3; r = 16 * e1 * (1 + Cc * e2)
    a = -(1 + e1) * (2 * e1 * e2 + e2 * e3) - (3 + 2 * Cc) * e1 * e2 * (e2 + e3) - 4 * e1 ** 2 * e2 - Cc * e2 * e3 * (e3 + e4)
    return float(ns), float(r), float(a)
def point(al, C):
    x = XG; P = al * x / (1 + x) + (1 - al) * (1 - 1 / (1 + x) ** 2); Vv = P * (1 + C * P / (1 - P))
    Sp = CubicSpline(PH, Vv); dS = Sp.derivative()
    Nsr = np.concatenate([[0], np.cumsum((Sp(PH[1:]) / np.maximum(dS(PH[1:]), 1e-300)) * np.diff(PH))])
    i0 = min(int(np.searchsorted(Nsr, 200.0)), len(PH) - 5)
    def rhs(N, u):
        p, v = u; return [v, -(3 - v * v / 2) * (v + dS(p) / Sp(p))]
    ev = lambda N, u: u[1] ** 2 / 2 - 1; ev.terminal = True; ev.direction = 1
    sol = solve_ivp(rhs, (0, 600), [PH[i0], -float(dS(PH[i0]) / Sp(PH[i0]))], events=ev, rtol=1e-10, atol=1e-12, dense_output=True)
    Nend = sol.t_events[0][0]; phie = sol.sol(Nend)[0]; V = Vfun(al, C); N = 50.0
    for _ in range(20):
        phis = sol.sol(Nend - N)[0]; ns, r, a = obs(V, mp.mpf(phis))
        Nn = Nstar(r, float(Sp(phis) / Sp(phie)), 8.94e8)
        if abs(Nn - N) < 1e-3: N = Nn; break
        N = Nn
    phis = sol.sol(Nend - N)[0]; ns, r, a = obs(V, mp.mpf(phis))
    inb = 0.969 <= ns <= 0.975 and 4.55e-4 <= r <= 5.7e-4
    near = abs(min(max(ns, 0.969), 0.975) - ns) <= 0.003 and 4.55e-4 / 1.3 <= r <= 5.7e-4 * 1.3
    return dict(alpha=al, C=C, Nstar=N, ns=ns, r=r, alpha_s=a, Ntot=float(Nend), in_band=bool(inb), near=bool(near),
                in_frozen=bool(0.970 <= ns <= 0.975 and 4.55e-4 <= r <= 5.7e-4))
if __name__ == '__main__':
    out = {"D": "D1485", "part1": {}, "part2": [], "part3": []}
    for tag, al, C in (('A1', 1.0, 1.25e-6), ('B0', 0.0, 0.0)):
        p = point(al, C); R = json.load(open(f'field_tests/results/DILATON32/{tag}.json'))
        p.update(ms_ns=R['ns'], ms_r=R['r'], d_ns=p['ns'] - R['ns'], d_r_rel=p['r'] / R['r'] - 1); out['part1'][tag] = p; print(tag, json.dumps(p), flush=True)
    out['part1_verdict'] = 'AGREE' if all(abs(v['d_ns']) <= 5e-4 and abs(v['d_r_rel']) <= 0.02 for v in out['part1'].values()) else 'DISAGREE'
    for al in (0.25, 0.5, 0.75):
        for C in (1.25e-6, 2.5e-6):
            p = point(al, C); out['part2'].append(p); print('locked', json.dumps(p), flush=True)
    for al in np.linspace(0, 1, 9):
        for C in (0, 0.5e-6, 1e-6, 1.5e-6, 2e-6, 2.5e-6, 3e-6, 4e-6):
            p = point(float(al), C); out['part3'].append(p); print('map', json.dumps(p), flush=True)
            json.dump(out, open('field_tests/results/D1485_dilmix_sr.json', 'w'), indent=1)
    out['in_band_points'] = [(p['alpha'], p['C']) for p in out['part3'] if p['in_band']]
    json.dump(out, open('field_tests/results/D1485_dilmix_sr.json', 'w'), indent=1); print(out['part1_verdict'], out['in_band_points'])
