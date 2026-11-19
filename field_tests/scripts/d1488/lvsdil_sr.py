"""D1488: independent SR forecast + band map for DILMIX (PREREG_D1488)."""
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
PH = np.linspace(float(mp.log(mp.sqrt(3) / 2) / mp.sqrt(2)) + 1e-3, float(mp.log(60) / mp.sqrt(2)), 2500)
XG = np.array([float(E32(mp.e ** (mp.sqrt(2) * mp.mpf(p))) - Er) for p in PH])
def Vfun(k):
    k = mp.mpf(k); F = lambda e: e ** (mp.mpf(1) / 3) * mp.e ** (-k * e ** (mp.mpf(2) / 3)); Fr = F(Er)
    return lambda p: 1 - F(E32(mp.e ** (mp.sqrt(2) * p))) / Fr
def obs(V, phi):
    # D4: flow parameters from one Taylor expansion of V (exact algebra, sympy-derived; replaces nested mp.diff)
    c = mp.taylor(V, phi, 4); V0, V1, V2, V3, V4 = [c[k] * mp.factorial(k) for k in range(5)]
    ev1 = (V1 / V0) ** 2 / 2; ev2 = 2 * ((V1 / V0) ** 2 - V2 / V0)
    ev3 = V1 * (-V0**2 * V3 + 3 * V0 * V1 * V2 - 2 * V1**3) / (V0**2 * (V0 * V2 - V1**2))
    ev4 = ((-V0**4*V1*V2*V4 + V0**4*V1*V3**2 - V0**4*V2**2*V3 + V0**3*V1**3*V4 + 6*V0**3*V1*V2**3 - V0**2*V1**4*V3
            - 14*V0**2*V1**3*V2**2 + 13*V0*V1**5*V2 - 4*V1**7)
           / (V0**2 * (V0**3*V2*V3 - V0**2*V1**2*V3 - 3*V0**2*V1*V2**2 + 5*V0*V1**3*V2 - 2*V1**5)))
    e1 = ev1 * (1 - ev2 / 3); e2 = ev2 * (1 - ev2 / 6 - ev3 / 3); e3 = ev3 * (1 - ev2 / 3 - ev4 / 3); e4 = ev4
    ns = 1 - 2 * e1 - e2 - (3 + 2 * Cc) * e1 * e2 - 2 * e1 ** 2 - Cc * e2 * e3; r = 16 * e1 * (1 + Cc * e2)
    a = -(1 + e1) * (2 * e1 * e2 + e2 * e3) - (3 + 2 * Cc) * e1 * e2 * (e2 + e3) - 4 * e1 ** 2 * e2 - Cc * e2 * e3 * (e3 + e4)
    return float(ns), float(r), float(a)
def point(k):
    E = XG + float(Er); lr = (np.log(E) / 3 - k * E ** (2 / 3)) - (np.log(float(Er)) / 3 - k * float(Er) ** (2 / 3))   # log(F/F_rho), D1
    L = CubicSpline(PH, lr); dL = L.derivative()
    class _S:
        def __call__(self, p): return 1 - np.exp(L(p))
    class _D:
        def __call__(self, p): return -np.exp(L(p)) * dL(p)
    Sp, dS = _S(), _D()
    Nsr = np.concatenate([[0], np.cumsum((Sp(PH[1:]) / np.maximum(dS(PH[1:]), 1e-300)) * np.diff(PH))])
    i0 = min(int(np.searchsorted(Nsr, 200.0)), len(PH) - 5)
    def rhs(N, u):
        p, v = u; return [v, -(3 - v * v / 2) * (v + dS(p) / Sp(p))]
    ev = lambda N, u: u[1] ** 2 / 2 - 1; ev.terminal = True; ev.direction = 1
    sol = solve_ivp(rhs, (0, 600), [PH[i0], -float(dS(PH[i0]) / Sp(PH[i0]))], events=ev, rtol=1e-10, atol=1e-12, dense_output=True)
    Nend = sol.t_events[0][0]; phie = sol.sol(Nend)[0]; V = Vfun(k); N = 50.0
    for _ in range(20):
        phis = sol.sol(Nend - N)[0]; ns, r, a = obs(V, mp.mpf(phis))
        Nn = Nstar(r, float(Sp(phis) / Sp(phie)), 8.94e8)
        if abs(Nn - N) < 1e-3: N = Nn; break
        N = Nn
    phis = sol.sol(Nend - N)[0]; ns, r, a = obs(V, mp.mpf(phis))
    inb = 0.969 <= ns <= 0.975 and 4.55e-4 <= r <= 5.7e-4
    near = abs(min(max(ns, 0.969), 0.975) - ns) <= 0.003 and 4.55e-4 / 1.3 <= r <= 5.7e-4 * 1.3
    return dict(k=k, vacuum_at_rho=bool(k * float(Er) ** (2 / 3) > 0.5), Nstar=N, y_star=math.exp(math.sqrt(2) * phis), Ntot=float(Nend),
                ns=ns, r=r, alpha_s=a, in_band=bool(inb), near=bool(near), i0_at_grid_end=bool(i0 >= len(PH) - 5))
if __name__ == '__main__':
    out = {"D": "D1488", "points": []}
    for k in (0.15, 0.3, 0.6, 1.2):
        try: p = point(k)
        except Exception as ex: p = dict(k=k, error=str(ex)[:120])
        out['points'].append(p); print('k', json.dumps(p), flush=True)
    out['all_r_below_1e-4'] = all(p.get('r', 1) < 1e-4 for p in out['points'] if 'r' in p)
    json.dump(out, open('field_tests/results/D1488_lvsdil_sr.json', 'w'), indent=1); print('done', out['all_r_below_1e-4'])
