# AEGIS-FP P3S-FAST · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""P3-S fast forecaster: the species-plateau inflation equation of 19 Nov 2026 (SERAPIS_FINAL_EQUATION.md v3).

    V(tau) = V_inf * ((2/3) * y d/dy ln E(tau,3/2))^2 * [1 + C*(E(tau,3/2) - E(rho,3/2))]   along Re tau = 1/2
    y = exp(b*phi),  b = sqrt(D-2)/2   (D = 10 -> b = sqrt 2, i.e. phi = ln y / sqrt 2;  D = 6 -> b = 1)
    rho = e^{i pi/3} (y_rho = sqrt3/2), where V = 0 and inflation ends.  C = w*chi/(4(2pi)^3 V)  (BBHL alpha'^3 tilt, D1566).

Speed: E and y dE/dy are evaluated from the Fourier series in closed form (no nested numerical derivatives), the background
is a spline + one ODE, and n_s, r, alpha_s come from second-order Hubble-flow slow roll (one mp.taylor of V at phi_*),
with N_* from the shared matching equation (nstar.py, T_R = 8.94e8 GeV). One point takes a few seconds instead of the
~30 min of an exact Mukhanov-Sasaki run.

Accuracy (validated in __main__ against the locked exact MS runs, see D-note): use it to SCREEN candidates and to
forecast locked runs; final numbers for a paper still need the exact MS engine (ms.spectra).
"""
import math
import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from tools.serapis_calc.nstar import Nstar

mp.mp.dps = 25
_S = mp.mpf(3) / 2
_A = 2 * mp.zeta(3)                                   # y^{3/2} coefficient
_B = 2 * mp.sqrt(mp.pi) * mp.gamma(1) * mp.zeta(2) / mp.gamma(_S)   # = 4 zeta(2): y^{-1/2} coefficient
_PREF = 8 * mp.pi ** _S / mp.gamma(_S)
_SIG = {n: sum(mp.mpf(d) ** (-2) for d in range(1, n + 1) if n % d == 0) for n in range(1, 41)}
_CACHE = {}
YRHO = mp.sqrt(3) / 2


def E_and_yDE(y):
    """(E(1/2 + iy, 3/2), y dE/dy) from the Fourier series; instanton sum stops when 2 pi n y > 80."""
    y = mp.mpf(y); key = y._mpf_
    if key in _CACHE: return _CACHE[key]
    E = _A * y ** _S + _B * y ** (1 - _S); yE = _S * _A * y ** _S + (1 - _S) * _B * y ** (1 - _S)
    for n in range(1, 41):
        a = 2 * mp.pi * n
        if a * y > 80: break
        c = _PREF * mp.mpf(n) * _SIG[n] * (-1) ** n          # n^{s-1/2} = n, cos(2 pi n / 2) = (-1)^n
        K1, K0 = mp.besselk(1, a * y), mp.besselk(0, a * y)
        E += c * mp.sqrt(y) * K1
        yE += c * mp.sqrt(y) * (-K1 / 2 - a * y * K0)        # y d/dy [sqrt(y) K1(a y)]
    _CACHE[key] = (E, yE); return E, yE


E_RHO = E_and_yDE(YRHO)[0]


def V(phi, C=0.0, D=10):
    """Potential in units of V_inf (mpmath-differentiable)."""
    y = mp.e ** (mp.sqrt(D - 2) / 2 * mp.mpf(phi))
    E, yE = E_and_yDE(y)
    return (mp.mpf(2) / 3 * yE / E) ** 2 * (1 + mp.mpf(C) * (E - E_RHO))


_An, _Bn, _Pn = float(_A), float(_B), float(_PREF)
_SIGn = {n: float(s) for n, s in _SIG.items()}
_ERn = float(E_RHO)


def V_np(phi, C=0.0, D=10):
    """Vectorised float version of V for the background grid (scipy Bessel K); same series as E_and_yDE."""
    from scipy.special import kv
    y = np.exp(math.sqrt(D - 2) / 2 * np.asarray(phi, float))
    E = _An * y ** 1.5 + _Bn / np.sqrt(y); yE = 1.5 * _An * y ** 1.5 - 0.5 * _Bn / np.sqrt(y)
    for n in range(1, 41):
        a = 2 * math.pi * n
        if a * y.min() > 80: break
        z = a * y; m = z <= 80
        c = _Pn * n * _SIGn[n] * (-1) ** n
        K1 = np.where(m, kv(1, np.where(m, z, 1.0)), 0.0); K0 = np.where(m, kv(0, np.where(m, z, 1.0)), 0.0)
        E = E + c * np.sqrt(y) * K1
        yE = yE + c * np.sqrt(y) * (-K1 / 2 - z * K0)
    return (2 / 3 * yE / E) ** 2 * (1 + C * (E - _ERn))


_CC = mp.euler + mp.log(2) - 2


def flow(Vf, phi):
    """Second-order Hubble-flow n_s, r, alpha_s at phi from one Taylor expansion (same algebra as D1485, validated there)."""
    c = mp.taylor(Vf, phi, 4); V0, V1, V2, V3, V4 = [c[k] * mp.factorial(k) for k in range(5)]
    ev1 = (V1 / V0) ** 2 / 2; ev2 = 2 * ((V1 / V0) ** 2 - V2 / V0)
    ev3 = V1 * (-V0**2 * V3 + 3 * V0 * V1 * V2 - 2 * V1**3) / (V0**2 * (V0 * V2 - V1**2))
    den4 = V0**2 * (V0**3*V2*V3 - V0**2*V1**2*V3 - 3*V0**2*V1*V2**2 + 5*V0*V1**3*V2 - 2*V1**5)
    ev4 = 0 if den4 == 0 else ((-V0**4*V1*V2*V4 + V0**4*V1*V3**2 - V0**4*V2**2*V3 + V0**3*V1**3*V4 + 6*V0**3*V1*V2**3 - V0**2*V1**4*V3
            - 14*V0**2*V1**3*V2**2 + 13*V0*V1**5*V2 - 4*V1**7) / den4)
    e1 = ev1 * (1 - ev2 / 3); e2 = ev2 * (1 - ev2 / 6 - ev3 / 3); e3 = ev3 * (1 - ev2 / 3 - ev4 / 3); e4 = ev4
    ns = 1 - 2 * e1 - e2 - (3 + 2 * _CC) * e1 * e2 - 2 * e1 ** 2 - _CC * e2 * e3
    r = 16 * e1 * (1 + _CC * e2)
    a = -(1 + e1) * (2 * e1 * e2 + e2 * e3) - (3 + 2 * _CC) * e1 * e2 * (e2 + e3) - 4 * e1 ** 2 * e2 - _CC * e2 * e3 * (e3 + e4)
    nt = -2 * e1 - 2 * e1 ** 2 - 2 * (_CC + 1) * e1 * e2   # D1555
    return dict(ns=float(ns), r=float(r), alpha_s=float(a), n_t=float(nt))


BAND = dict(ns=(0.969, 0.975), r=(4.55e-4, 5.7e-4))


def point(C=8e-7, D=10, TR=8.94e8, ymax=3000.0, npts=4000, Nfixed=None):
    """Forecast one P3-S point. Returns ns, r, alpha_s, n_t, N_*, y_*, Ntot, in_band. Nfixed overrides the N_* matching."""
    b = math.sqrt(D - 2) / 2
    ph = np.linspace(math.log(float(YRHO)) / b + 1e-4, math.log(ymax) / b, npts)
    Vv = V_np(ph, C, D)
    Sp = CubicSpline(ph, Vv); dS = Sp.derivative()
    Nsr = np.concatenate([[0], np.cumsum((Sp(ph[1:]) / np.maximum(dS(ph[1:]), 1e-300)) * np.diff(ph))])
    i0 = min(int(np.searchsorted(Nsr, 150.0)), len(ph) - 5)

    def rhs(N, u):
        p, v = u; return [v, -(3 - v * v / 2) * (v + dS(p) / Sp(p))]
    ev = lambda N, u: u[1] ** 2 / 2 - 1; ev.terminal = True; ev.direction = 1
    sol = solve_ivp(rhs, (0, 600), [ph[i0], -float(dS(ph[i0]) / Sp(ph[i0]))], events=ev,
                    rtol=1e-10, atol=1e-12, dense_output=True)
    Nend = sol.t_events[0][0]; phie = sol.sol(Nend)[0]
    Vf = lambda p: V(p, C, D)
    N = 50.0 if Nfixed is None else float(Nfixed)
    for _ in range(25):
        phis = sol.sol(Nend - N)[0]; o = flow(Vf, mp.mpf(phis))
        if Nfixed is not None: break
        Nn = Nstar(o['r'], float(Sp(phis) / Sp(phie)), TR)
        if abs(Nn - N) < 1e-3: N = Nn; break
        N = Nn
    phis = sol.sol(Nend - N)[0]; o = flow(Vf, mp.mpf(phis))
    o.update(C=C, D=D, Nstar=N, y_star=math.exp(b * phis), Ntot=float(Nend),
             in_band=bool(BAND['ns'][0] <= o['ns'] <= BAND['ns'][1] and BAND['r'][0] <= o['r'] <= BAND['r'][1]))
    return o


def tilt_for_ns(target_ns=0.97065, D=10, lo=0.0, hi=6e-6, tol=1e-6):
    """Bisect C so that n_s = target (n_s rises with C)."""
    for _ in range(40):
        mid = (lo + hi) / 2
        if point(mid, D)['ns'] < target_ns: lo = mid
        else: hi = mid
        if hi - lo < tol * max(mid, 1e-12): break
    return (lo + hi) / 2


def r_ladder(r10=5.41e-4):
    """Untilted r scales as 8/(D-2) at fixed N (D1589, SERAPIS_FINAL_EQUATION): r_D = r10 * 8/(D-2)."""
    return {D: r10 * 8 / (D - 2) for D in range(4, 11)}


# Locked exact Mukhanov-Sasaki references (other chat's runs, read-only).
REFERENCE = {
    ('SPECIES32 X, D=10', 8e-7, 10): dict(ns=0.9706477012440691, r=0.0005408069332645085, alpha_s=-0.0009677439470960906, Nstar=50.365416750265254),
    ('P3D6 X, D=6', 2.64e-6, 6): dict(ns=0.9705569396951678, r=0.0010688681342163166, alpha_s=-0.0009585219878050258, Nstar=50.56765169508966),
}

if __name__ == '__main__':
    import json, time
    rows = []
    for (tag, C, D), ref in REFERENCE.items():
        t = time.time(); p = point(C, D)
        row = dict(ref=tag, C=C, D=D, fast=p, exact=ref, d_ns=p['ns'] - ref['ns'], d_r_rel=p['r'] / ref['r'] - 1,
                   d_alpha=p['alpha_s'] - ref['alpha_s'], d_N=p['Nstar'] - ref['Nstar'], seconds=round(time.time() - t, 1))
        rows.append(row); print(json.dumps(row), flush=True)
    print(json.dumps(dict(r_ladder=r_ladder())))
