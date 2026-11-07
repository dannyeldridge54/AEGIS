"""Radiation+dust scalar perturbations: photon fluid, free-streaming neutrinos, CDM, baryons.

Conformal Newtonian gauge, ds^2=a^2[-(1+2psi)dtau^2+(1-2phi)dx^2], 8 pi G=1,
k=1 so x=k*tau. Background: photons+massless neutrinos (Rnu=rho_nu/rho_r) plus
pressureless matter (CDM and optionally baryons, f_b=rho_b/rho_m), scalar or
vacuum absent, with a/a_eq=s^2+2s, s=tau/tau_1
(exact for rho_r/rho_m=a_eq/a). kt1=k*tau_1 is the only background parameter;
the equality conformal time is (sqrt2-1)*tau_1. Photons are a perfect fluid
(no photon hierarchy/polarization; baryons only tightly coupled at infinite opacity). Equations, series and domain:
DERIVATION_CHAIN.md sections 15-16. It extends neutrino_hierarchy.py, which is the
kt1->infinity limit.

State: delta_gamma, theta_gamma, delta_nu, theta_nu, F_2..F_lmax, delta_c,
theta_c, phi.
"""
import math

import numpy as np
from scipy.integrate import solve_ivp

from theory.neutrino_contract import neutrino_radiation_adiabatic_contract

MIN_LMAX = 4
MAX_LMAX = 200
MAX_SERIES_S = 0.01


def _check(neutrino_fraction, lmax, kt1, baryon_fraction=0.0):
    if not isinstance(baryon_fraction, (int, float)) or isinstance(baryon_fraction, bool) \
            or not math.isfinite(baryon_fraction) or not 0 <= baryon_fraction < 1:
        raise ValueError("Baryon fraction rho_b/rho_m must be finite and lie in [0, 1)")
    if not isinstance(neutrino_fraction, (int, float)) or isinstance(neutrino_fraction, bool) \
            or not math.isfinite(neutrino_fraction) or not 0 <= neutrino_fraction < 1:
        raise ValueError("Neutrino fraction must be finite and lie in [0, 1)")
    if not isinstance(lmax, int) or isinstance(lmax, bool) or not MIN_LMAX <= lmax <= MAX_LMAX:
        raise ValueError(f"Hierarchy lmax must be an integer in [{MIN_LMAX}, {MAX_LMAX}]")
    if not isinstance(kt1, (int, float)) or isinstance(kt1, bool) or not math.isfinite(kt1) \
            or kt1 <= 0:
        raise ValueError("kt1=k*tau_1 must be finite and positive")


def background(kt1, x):
    """Return calH/k, a^2*rho_r/k^2 and a^2*rho_m/k^2 at x=k*tau (reduced Planck units)."""
    s = x / kt1
    return (2 * (1 + s) / (x * (2 + s)), 12 / (x * x * (2 + s) ** 2),
            12 / (kt1 * x * (2 + s)))


def initial_state(neutrino_fraction, kt1, x0, lmax, *, primordial_psi=1e-5,
                  baryon_fraction=0.0):
    """Adiabatic regular mode through x0^3 (delta, phi), x0^4 (theta), x0^5 (F_2).

    e=1/kt1; coefficients solve the evolved equations plus the 0i and 00
    constraints order by order in x with exact a(tau) (section 15) and
    delta_gamma=delta_nu=(4/3)delta_c=-2psi, psi(0)=primordial_psi. Requires
    0<x0<=.01 and x0/kt1<=.01; for kt1->infinity it reduces to
    neutrino_hierarchy.initial_state. F_l (l>=4) use the leading series
    F_l=F_{l-1}x/(2l+1) and the shear F_3 starts at 2x^3/105. With
    baryon_fraction=f_b=rho_b/rho_m (tight-coupling limit, section 16) the only
    change through these orders is theta_gamma,x^4 += e*b*(4R+15)/180 with
    b=3 f_b/(4(1-R)); all other coefficients are independent of f_b.
    """
    _check(neutrino_fraction, lmax, kt1, baryon_fraction)
    neutrino_radiation_adiabatic_contract(
        neutrino_fraction, x0, primordial_psi=primordial_psi)
    if x0 / kt1 > MAX_SERIES_S:
        raise ValueError("Series start requires x0/kt1 <= .01 (radiation-dominated start)")
    R = float(neutrino_fraction)
    e = 1.0 / kt1
    x = float(x0)
    a, b, c = 2 * R + 15, 2 * R + 25, 4 * R + 75
    e2 = e * e
    dg1 = -e * (16 * R + 15) / (2 * a)
    dg2 = -(896 * R**3 + 10080 * R**2 * e2 + 17680 * R**2 - 129150 * R * e2
            + 111600 * R - 212625 * e2 + 220500) / (1260 * a * b)
    dg3 = e * (896 * R**4 + 59440 * R**3 + 1058400 * R**2 * e2 + 821700 * R**2
               - 2646000 * R * e2 + 4074000 * R - 12403125 * e2 + 6628125) / (1260 * a * b * c)
    tg2 = 3 * e * (4 * R - 5) / (8 * a)
    tg3 = (56 * R**2 * e2 - 40 * R**2 - 1820 * R * e2 - 440 * R + 1575 * e2 - 1050) / (56 * a * b)
    tg4 = -e * (1888 * R**3 + 88200 * R**2 * e2 + 7640 * R**2 - 1212750 * R * e2
                - 100000 * R + 826875 * e2 - 376250) / (672 * a * b * c)
    tn3 = (2520 * R**2 * e2 - 2024 * R**2 - 81900 * R * e2 - 24280 * R + 70875 * e2
           - 68250) / (2520 * a * b)
    tn4 = -e * (10336 * R**3 + 441000 * R**2 * e2 + 65080 * R**2 - 6063750 * R * e2
                - 325000 * R + 4134375 * e2 - 2143750) / (3360 * a * b * c)
    tc3 = (112 * R**3 + 2520 * R**2 * e2 + 860 * R**2 - 81900 * R * e2 - 900 * R
           + 70875 * e2 - 7875) / (2520 * a * b)
    tc4 = -e * (896 * R**4 + 85280 * R**3 + 2205000 * R**2 * e2 + 741200 * R**2
                - 30318750 * R * e2 + 650000 * R + 20671875 * e2 - 3500000) / (16800 * a * b * c)
    p1 = -e * (16 * R + 15) / (8 * a)
    p2 = -(896 * R**3 + 10080 * R**2 * e2 + 16000 * R**2 - 129150 * R * e2
           + 78000 * R - 212625 * e2 + 63000) / (5040 * a * b)
    p3 = e * (896 * R**4 + 66160 * R**3 + 1058400 * R**2 * e2 + 1023300 * R**2
              - 2646000 * R * e2 + 5386500 * R - 12403125 * e2 + 4659375) / (5040 * a * b * c)
    f2_3 = e * (4 * R - 5) / (15 * a)
    f2_4 = (504 * R**2 * e2 - 448 * R**2 - 16380 * R * e2 - 5720 * R + 14175 * e2
            - 17700) / (3780 * a * b)
    f2_5 = -e * (448 * R**3 + 17640 * R**2 * e2 + 3640 * R**2 - 242550 * R * e2
                 - 6250 * R + 165375 * e2 - 95875) / (1260 * a * b * c)
    f3_4 = e * (4 * R - 5) / (140 * a)
    dg = -2 + dg1 * x + dg2 * x**2 + dg3 * x**3
    dn = dg  # identical through the order kept: dn_n=dg_n for n<=3
    dc = 0.75 * dg
    tg4 += e * (3 * baryon_fraction / (4 * (1 - R))) * (4 * R + 15) / 180
    tg = x / 2 + tg2 * x**2 + tg3 * x**3 + tg4 * x**4
    tn = x / 2 + tg2 * x**2 + tn3 * x**3 + tn4 * x**4
    tc = x / 2 + tg2 * x**2 + tc3 * x**3 + tc4 * x**4
    phi = (2 * R + 5) / 5 + p1 * x + p2 * x**2 + p3 * x**3
    f = {2: 2 * x**2 / 15 + f2_3 * x**3 + f2_4 * x**4 + f2_5 * x**5,
         3: 2 * x**3 / 105 + f3_4 * x**4}
    f[4] = 2 * x**4 / 945
    for ell in range(5, lmax + 1):
        f[ell] = f[ell - 1] * x / (2 * ell + 1)
    state = np.empty(lmax + 6)
    state[0], state[1], state[2], state[3] = dg, tg, dn, tn
    state[4:lmax + 3] = [f[ell] for ell in range(2, lmax + 1)]
    state[lmax + 3], state[lmax + 4], state[lmax + 5] = dc, tc, phi
    return primordial_psi * state


def equations(neutrino_fraction, lmax, kt1, x, state, *, baryon_fraction=0.0):
    """Return d(state)/dx and the scaled independent 00 residual.

    residual = x^2*[phi+3 calH(phi'+calH psi)+a^2 delta_rho/2] with the 0i
    equation used for phi'; the evolution does not enforce it. Baryons
    (f_b=rho_b/rho_m>0) are tightly coupled to photons (infinite opacity):
    theta_b=theta_gamma, delta_b=(3/4)delta_gamma, photon shear dropped and
    (1+Rb)theta' = -Rb calH theta + delta_gamma/4 + (1+Rb)psi, Rb=3rho_b/(4rho_gamma).
    """
    _check(neutrino_fraction, lmax, kt1, baryon_fraction)
    state = np.asarray(state, dtype=float)
    if state.shape != (lmax + 6,) or not np.all(np.isfinite(state)):
        raise ValueError("Matter-hierarchy state has the wrong shape or is not finite")
    if not math.isfinite(x) or x <= 0:
        raise ValueError("Matter-hierarchy evaluation requires finite x > 0")
    rnu = float(neutrino_fraction)
    hub, rho_r, rho_m = background(kt1, x)
    dg, tg, dn, tn, f2 = state[0], state[1], state[2], state[3], state[4]
    dc, tc, phi = state[lmax + 3], state[lmax + 4], state[lmax + 5]
    higher = state[5:lmax + 3]  # F_3..F_lmax
    psi = phi - rnu * rho_r * f2
    fb = float(baryon_fraction)
    rb = 0.75 * fb * rho_m / ((1 - rnu) * rho_r)
    theta_sum = ((4 / 3) * rho_r * ((1 - rnu) * (1 + rb) * tg + rnu * tn)
                 + rho_m * (1 - fb) * tc)
    phi_prime = theta_sum / 2 - hub * psi
    d = np.empty_like(state)
    d[0] = -4 * tg / 3 + 4 * phi_prime
    d[1] = (dg / 4 - rb * hub * tg) / (1 + rb) + psi
    d[2] = -4 * tn / 3 + 4 * phi_prime
    d[3] = dn / 4 - f2 / 2 + psi
    f = np.concatenate(([0., 0.], [f2], higher))
    d[4] = 8 * tn / 15 - 3 * f[3] / 5
    for ell in range(3, lmax):
        d[2 + ell] = (ell * f[ell - 1] - (ell + 1) * f[ell + 1]) / (2 * ell + 1)
    d[2 + lmax] = f[lmax - 1] - (lmax + 1) * f[lmax] / x
    d[lmax + 3] = -tc + 3 * phi_prime
    d[lmax + 4] = -hub * tc + psi
    d[lmax + 5] = phi_prime
    delta_rho = (rho_r * ((1 - rnu) * dg + rnu * dn)
                 + rho_m * ((1 - fb) * dc + 0.75 * fb * dg))
    residual = x**2 * (phi + 3 * hub * (phi_prime + hub * psi) + delta_rho / 2)
    if not np.all(np.isfinite(d)) or not math.isfinite(residual):
        raise ValueError("Matter-hierarchy equations must remain finite")
    return d, float(residual)


def potentials(neutrino_fraction, lmax, kt1, x, state):
    """Return (psi, phi) for a state."""
    _, rho_r, _ = background(kt1, x)
    return state[lmax + 5] - neutrino_fraction * rho_r * state[4], state[lmax + 5]


def curvature_perturbation(neutrino_fraction, lmax, kt1, x, state, *, baryon_fraction=0.0):
    """zeta=-phi-calH*delta_rho_tot/rho_tot'; conserved for k->0 adiabatic modes.

    With rho_tot'=-3calH(rho+P): zeta=-phi+delta_rho/(3(rho+P)) per total fluid.
    """
    rnu = float(neutrino_fraction)
    _, rho_r, rho_m = background(kt1, x)
    _check(neutrino_fraction, lmax, kt1, baryon_fraction)
    fb = float(baryon_fraction)
    delta_rho = (rho_r * ((1 - rnu) * state[0] + rnu * state[2])
                 + rho_m * ((1 - fb) * state[lmax + 3] + 0.75 * fb * state[0]))
    return -state[lmax + 5] + delta_rho / (3 * (4 * rho_r / 3 + rho_m))


def integrate(neutrino_fraction, lmax, kt1, state, x0, x_final, *, rtol=1e-10, atol=1e-16,
              method="DOP853", baryon_fraction=0.0):
    """Integrate from x0 to x_final; closure reflections limit x_final <= lmax/2."""
    _check(neutrino_fraction, lmax, kt1, baryon_fraction)
    if method not in ("RK45", "DOP853"):
        raise ValueError("Supported hierarchy methods are RK45 and DOP853")
    if not all(math.isfinite(v) and v > 0 for v in (rtol, atol, x0, x_final)) or x_final <= x0:
        raise ValueError("Hierarchy x range and tolerances must be finite, positive and ordered")
    if x_final > lmax / 2:
        raise ValueError("x_final exceeds lmax/2: the truncated hierarchy reflects at the closure")
    solution = solve_ivp(lambda x, y: equations(neutrino_fraction, lmax, kt1, x, y,
                                                baryon_fraction=baryon_fraction)[0],
                         (x0, x_final), np.asarray(state, dtype=float), method=method,
                         rtol=rtol, atol=atol, dense_output=True)
    if not solution.success or solution.sol is None or not np.all(np.isfinite(solution.y)):
        raise ValueError(f"Matter-hierarchy integration failed: {solution.message}")
    return solution


def validate(neutrino_fraction, lmax, kt1, x0, x_final, *, primordial_psi=1e-5,
             baryon_fraction=0.0):
    """Constraint drift, truncation, tolerance and start-epoch refinement.

    Numerical gate only; it never asserts physical readiness.
    """
    bf = {"baryon_fraction": baryon_fraction}
    start = initial_state(neutrino_fraction, kt1, x0, lmax, primordial_psi=primordial_psi, **bf)
    coarse = integrate(neutrino_fraction, lmax, kt1, start, x0, x_final, method="RK45", **bf)
    fine = integrate(neutrino_fraction, lmax, kt1, start, x0, x_final, **bf)
    long_start = initial_state(neutrino_fraction, kt1, x0, 2 * lmax, primordial_psi=primordial_psi,
                               **bf)
    long = integrate(neutrino_fraction, 2 * lmax, kt1, long_start, x0, x_final, **bf)
    early_x0 = x0 / 2
    early = integrate(neutrino_fraction, lmax, kt1,
                      initial_state(neutrino_fraction, kt1, early_x0, lmax,
                                    primordial_psi=primordial_psi, **bf), early_x0, x_final, **bf)
    grid = np.geomspace(x0, x_final, 400)
    scale = abs(primordial_psi)
    low = fine.sol(grid)
    pick = [0, 1, 2, 3, 4, lmax + 3, lmax + 4, lmax + 5]
    long_all = long.sol(grid)
    long_pick = [0, 1, 2, 3, 4, 2 * lmax + 3, 2 * lmax + 4, 2 * lmax + 5]
    truncation = float(np.max(np.abs(low[pick] - long_all[long_pick])
                              / np.maximum(scale, np.abs(long_all[long_pick]))))
    tolerance = float(np.max(np.abs(low - coarse.sol(grid)) / np.maximum(scale, np.abs(low))))
    early_values = early.sol(grid)
    start_epoch = float(np.max(np.abs(low[pick] - early_values[pick])
                               / np.maximum(scale, np.abs(low[pick]))))
    residual = max(abs(equations(neutrino_fraction, lmax, kt1, float(x), fine.sol(x), **bf)[1])
                   for x in grid)
    initial_residual = abs(equations(neutrino_fraction, lmax, kt1, x0, start, **bf)[1])
    values = (truncation, tolerance, start_epoch, residual, initial_residual)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("Matter-hierarchy validation evidence must be finite")
    return {
        "neutrino_fraction": float(neutrino_fraction), "lmax": lmax, "kt1": float(kt1),
        "baryon_fraction": float(baryon_fraction),
        "x0": x0, "x_final": x_final, "primordial_psi": primordial_psi,
        "max_truncation_shift_over_psi": truncation,
        "max_tolerance_shift_over_psi": tolerance,
        "max_start_epoch_shift_over_psi": start_epoch,
        "max_scaled_00_residual": residual,
        "initial_scaled_00_residual": initial_residual,
        "residual_units": "x^2*[phi+3calH(phi'+calH psi)+a^2 delta_rho/2], dimensionless (k=1)",
        "numerical_gate_passed": bool(truncation < 1e-6 and tolerance < 1e-6
                                      and start_epoch < 1e-5 and residual < 1e-5 * scale),
        "scope": "radiation+CDM(+baryon) background, photon perfect fluid (baryons only in the "
                 "infinite-opacity tight-coupling limit, no opacity/recombination input), "
                 "free-streaming neutrino hierarchy, adiabatic mode",
        "primordial_initialization_established": False,
        "full_stability_established": False, "scientific_baseline_ready": False,
        "missing": ["finite-opacity photon-baryon coupling, ionization history, polarization "
                    "and photon hierarchy",
                    "scalar/vacuum coupling to the hierarchy and late-time dark energy",
                    "primordial spectrum, transfer functions and observables",
                    "independent Boltzmann validation"],
    }
