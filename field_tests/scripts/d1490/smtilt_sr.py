"""D1485: independent SR forecast + band map for DILMIX (PREREG_D1485)."""
import json, sys, math, mpmath as mp, numpy as np
sys.path.insert(0, '.')
from tools.serapis_calc.nstar import Nstar
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
mp.mp.dps = 25
Cc = mp.euler + mp.log(2) - 2
_EC = {}
def Es(y, s, x=mp.mpf(1) / 2):
    key = (mp.mpf(y)._mpf_, float(s))
    if key in _EC: return _EC[key]
    s = mp.mpf(s)
    out = 2 * mp.zeta(2 * s) * y ** s + 2 * mp.sqrt(mp.pi) * mp.gamma(s - mp.mpf(1) / 2) * mp.zeta(2 * s - 1) / mp.gamma(s) * y ** (1 - s)
    pref = 8 * mp.pi ** s / mp.gamma(s) * mp.sqrt(y)
    for n in range(1, 41):
        if 2 * mp.pi * n * y > 80: break
        sig = sum(mp.mpf(d) ** (1 - 2 * s) for d in range(1, n + 1) if n % d == 0)
        out += pref * mp.mpf(n) ** (s - mp.mpf(1) / 2) * sig * mp.cos(2 * mp.pi * n * x) * mp.besselk(s - mp.mpf(1) / 2, 2 * mp.pi * n * y)
    _EC[key] = out; return out
PH = np.linspace(float(mp.log(mp.sqrt(3) / 2) / mp.sqrt(2)) + 1e-3, float(mp.log(3000) / mp.sqrt(2)), 2500)
GR = {}
def grid(s):
    if s not in GR:
        Er = Es(mp.sqrt(3) / 2, s); GR[s] = (Er, np.array([float(Es(mp.e ** (mp.sqrt(2) * mp.mpf(p)), s) / Er) for p in PH]))
    return GR[s]
def Vfun(s, m, C):
    Er = grid(s)[0]; m, C = mp.mpf(m), mp.mpf(C)
    def V(p):
        P = 1 - (Er / Es(mp.e ** (mp.sqrt(2) * p), s)) ** m
        return P * (1 + C * P / (1 - P))
    return V
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
def point(s, m, C):
    ratio = grid(s)[1]; P = 1 - ratio ** (-m); Vv = P * (1 + C * P / (1 - P))
    Sp = CubicSpline(PH, Vv); dS = Sp.derivative()
    Nsr = np.concatenate([[0], np.cumsum((Sp(PH[1:]) / np.maximum(dS(PH[1:]), 1e-300)) * np.diff(PH))])
    i0 = min(int(np.searchsorted(Nsr, 200.0)), len(PH) - 5)
    rhs = lambda N, u: [u[1], -(3 - u[1] ** 2 / 2) * (u[1] + dS(u[0]) / Sp(u[0]))]
    ev = lambda N, u: u[1] ** 2 / 2 - 1; ev.terminal = True; ev.direction = 1
    sol = solve_ivp(rhs, (0, 600), [PH[i0], -float(dS(PH[i0]) / Sp(PH[i0]))], events=ev, rtol=1e-10, atol=1e-12, dense_output=True)
    Nend = sol.t_events[0][0]; phie = sol.sol(Nend)[0]; V = Vfun(s, m, C); N = 50.0
    for _ in range(25):
        phis = sol.sol(Nend - N)[0]; ns, r, a = obs(V, mp.mpf(phis))
        Nn = Nstar(r, float(Sp(phis) / Sp(phie)), 8.94e8)
        if abs(Nn - N) < 1e-3: N = Nn; break
        N = Nn
    phis = sol.sol(Nend - N)[0]; ns, r, a = obs(V, mp.mpf(phis))
    return dict(s=s, m=m, sm=s * m, C=C, Nstar=N, ns=ns, r=r, alpha_s=a, y_star=math.exp(math.sqrt(2) * phis),
                in_band=bool(0.969 <= ns <= 0.975 and 4.55e-4 <= r <= 5.7e-4))
if __name__ == '__main__':
    out = {"D": "D1490", "anchor": None, "side": None, "map": []}
    a = point(2.0, 1.0, 0.0); R = json.load(open('field_tests/results/SMSCAN/s2_m1.json'))
    a.update(ms_ns=R['ns'], ms_r=R['r'], d_ns=a['ns'] - R['ns'], d_r_rel=a['r'] / R['r'] - 1); out['anchor'] = a
    out['anchor_verdict'] = 'AGREE' if abs(a['d_ns']) <= 5e-4 and abs(a['d_r_rel']) <= 0.02 else 'DISAGREE'; print('anchor', json.dumps(a), flush=True)
    p2 = point(2.0, 1.0, 1.5e-6); p3 = point(3.0, 2 / 3, 1.5e-6)
    out['side'] = dict(s2=p2, s3=p3, d_ns=p3['ns'] - p2['ns'], d_r_rel=p3['r'] / p2['r'] - 1); print('side', json.dumps(out['side']), flush=True)
    for sm in (1.5, 1.7, 1.8, 1.9, 2.0, 2.2):
        for C in (0, 0.5e-6, 1e-6, 1.5e-6, 2e-6, 2.5e-6, 3e-6):
            try: p = point(2.0, sm / 2, C)
            except Exception as ex: p = dict(sm=sm, C=C, error=str(ex)[:80], in_band=False)
            out['map'].append(p); print('map', json.dumps(p), flush=True)
    out['in_band'] = [(p['sm'], p['C']) for p in out['map'] if p.get('in_band')]
    json.dump(out, open('/tmp/claude-0/-home-claude/e1153314-178b-5884-8c19-291220701fba/scratchpad/D1490_smtilt.json', 'w'), indent=1); print('done', out['anchor_verdict'], out['in_band'])
