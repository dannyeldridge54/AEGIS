"""Radiation-era scalar perturbations: photon fluid plus free-streaming neutrino hierarchy.

Conformal Newtonian gauge, ds^2=a^2[-(1+2psi)dtau^2+(1-2phi)dx^2], 8 pi G=1,
a proportional to tau (calH=1/tau), k=1 so the independent variable is
x=k*tau. Photons are a perfect fluid (no shear, no baryons: a tight-coupling
idealisation, not a photon Boltzmann hierarchy); massless neutrinos carry the
Ma-Bertschinger hierarchy F_0..F_lmax (F_2=2 sigma) with its standard
truncation. No dust, scalar field, vacuum, primordial spectrum or CMB output.
Supported domain and equations: DERIVATION_CHAIN.md section 14.

State: delta_gamma, theta_gamma, delta_nu, theta_nu, F_2..F_lmax, phi.
"""
import math

import numpy as np
from scipy.integrate import solve_ivp

from theory.neutrino_contract import neutrino_radiation_adiabatic_contract

MIN_LMAX = 4
MAX_LMAX = 200


def _check(neutrino_fraction, lmax):
    if not isinstance(neutrino_fraction, (int, float)) or isinstance(neutrino_fraction, bool) \
            or not math.isfinite(neutrino_fraction) or not 0 <= neutrino_fraction < 1:
        raise ValueError("Neutrino fraction must be finite and lie in [0, 1)")
    if not isinstance(lmax, int) or isinstance(lmax, bool) or not MIN_LMAX <= lmax <= MAX_LMAX:
        raise ValueError(f"Hierarchy lmax must be an integer in [{MIN_LMAX}, {MAX_LMAX}]")


def initial_state(neutrino_fraction, x0, lmax, *, primordial_psi=1e-5):
    """Regular superhorizon mode through O(x0^2) in the potentials/densities.

    psi(0)=primordial_psi, 0 < x0 <= .01. Coefficients solve the full series of
    the evolved equations plus the 00 constraint (section 14); the R=0 values
    reproduce the pure-radiation solution 3(sin y - y cos y)/y^3, y=x/sqrt(3).
    F_3, F_4 use their leading series and F_l=F_{l-1}*x/(2l+1) above that.
    The 00 residual is O(x0^4*psi), neglected terms are O(x0^4) relative.
    """
    _check(neutrino_fraction, lmax)
    neutrino_radiation_adiabatic_contract(
        neutrino_fraction, x0, primordial_psi=primordial_psi)
    r = float(neutrino_fraction)
    x2 = x0 * x0
    denominator = 2 * r + 25
    g2 = -(112 * r**2 + 1370 * r + 3675) / (315 * denominator)
    a3 = -5 * (2 * r + 7) / (28 * denominator)
    b3 = -(506 * r + 2275) / (1260 * denominator)
    c4 = -(56 * r + 295) / (945 * denominator)
    p2 = -(56 * r**2 + 580 * r + 525) / (630 * denominator)
    c2 = 2 / 15
    multipoles = {2: c2 * x2 + c4 * x2 * x2, 3: c2 / 7 * x0 * x2}
    multipoles[4] = multipoles[3] * x0 / 9
    for ell in range(5, lmax + 1):
        multipoles[ell] = multipoles[ell - 1] * x0 / (2 * ell + 1)
    state = np.zeros(5 + lmax - 1)
    state[0] = -2 + g2 * x2
    state[1] = x0 / 2 + a3 * x0 * x2
    state[2] = -2 + g2 * x2
    state[3] = x0 / 2 + b3 * x0 * x2
    state[4:-1] = [multipoles[ell] for ell in range(2, lmax + 1)]
    state[-1] = 1 + 2 * r / 5 + p2 * x2
    return primordial_psi * state

def equations(neutrino_fraction, lmax, x, state):
    """Return d(state)/dx and the independent scaled 00 residual.

    residual = x^2*phi + 6*Theta/x + 1.5*delta_bar with
    Theta=(1-Rnu)theta_gamma+Rnu*theta_nu and delta_bar likewise; it follows
    from k^2 phi+3 calH(phi'+calH psi)=-a^2 delta_rho/2 and the 0i equation
    used to evolve phi, so it is not enforced by the evolution.
    """
    _check(neutrino_fraction, lmax)
    state = np.asarray(state, dtype=float)
    if state.shape != (5 + lmax - 1,) or not np.all(np.isfinite(state)):
        raise ValueError("Hierarchy state has the wrong shape or is not finite")
    if not math.isfinite(x) or x <= 0:
        raise ValueError("Hierarchy evaluation requires finite x > 0")
    rnu = float(neutrino_fraction)
    dg, tg, dn, tn, f2, phi = state[0], state[1], state[2], state[3], state[4], state[-1]
    higher = state[5:-1]  # F_3..F_lmax
    theta = (1 - rnu) * tg + rnu * tn
    psi = phi - 3 * rnu * f2 / x**2
    phi_prime = 2 * theta / x**2 - psi / x
    derivatives = np.empty_like(state)
    derivatives[0] = -4 * tg / 3 + 4 * phi_prime
    derivatives[1] = dg / 4 + psi
    derivatives[2] = -4 * tn / 3 + 4 * phi_prime
    derivatives[3] = dn / 4 - f2 / 2 + psi
    f = np.concatenate(([0., 0.], [f2], higher))  # f[l] for l=0..lmax; f[0], f[1] unused
    derivatives[4] = 8 * tn / 15 - 3 * f[3] / 5
    for ell in range(3, lmax):
        derivatives[2 + ell] = (ell * f[ell - 1] - (ell + 1) * f[ell + 1]) / (2 * ell + 1)
    derivatives[2 + lmax] = f[lmax - 1] - (lmax + 1) * f[lmax] / x
    derivatives[-1] = phi_prime
    delta = (1 - rnu) * dg + rnu * dn
    residual = x**2 * phi + 6 * theta / x + 1.5 * delta
    if not np.all(np.isfinite(derivatives)) or not math.isfinite(residual):
        raise ValueError("Hierarchy equations must remain finite")
    return derivatives, float(residual)


def integrate(neutrino_fraction, lmax, state, x0, x_final, *, rtol=1e-10, atol=1e-16,
              method="DOP853"):
    """Integrate from x0 to x_final; closure reflections limit x_final <= lmax/2."""
    _check(neutrino_fraction, lmax)
    if method not in ("RK45", "DOP853"):
        raise ValueError("Supported hierarchy methods are RK45 and DOP853")
    if not all(math.isfinite(v) and v > 0 for v in (rtol, atol, x0, x_final)) or x_final <= x0:
        raise ValueError("Hierarchy x range and tolerances must be finite, positive and ordered")
    if x_final > lmax / 2:
        raise ValueError("x_final exceeds lmax/2: the truncated hierarchy reflects at the closure")
    solution = solve_ivp(lambda x, y: equations(neutrino_fraction, lmax, x, y)[0],
                         (x0, x_final), np.asarray(state, dtype=float), method=method,
                         rtol=rtol, atol=atol, dense_output=True)
    if not solution.success or solution.sol is None or not np.all(np.isfinite(solution.y)):
        raise ValueError(f"Hierarchy integration failed: {solution.message}")
    return solution


def validate(neutrino_fraction, lmax, x0, x_final, *, primordial_psi=1e-5):
    """Constraint drift, truncation (lmax -> 2*lmax) and tolerance refinement.

    The gate is numerical only; it never asserts physical readiness.
    """
    start = initial_state(neutrino_fraction, x0, lmax, primordial_psi=primordial_psi)
    coarse = integrate(neutrino_fraction, lmax, start, x0, x_final, method="RK45", rtol=1e-10,
                           atol=1e-16)
    fine = integrate(neutrino_fraction, lmax, start, x0, x_final)
    long_start = initial_state(neutrino_fraction, x0, 2 * lmax, primordial_psi=primordial_psi)
    long = integrate(neutrino_fraction, 2 * lmax, long_start, x0, x_final)
    grid = np.geomspace(x0, x_final, 400)
    scale = abs(primordial_psi)
    low = fine.sol(grid)
    # Leading 5 and trailing phi components are compared; high multipoles differ by design.
    pick = [0, 1, 2, 3, 4, low.shape[0] - 1]
    long_pick = [0, 1, 2, 3, 4, long.sol(grid).shape[0] - 1]
    longer = long.sol(grid)[long_pick]
    truncation = float(np.max(np.abs(low[pick] - longer) / np.maximum(scale, np.abs(longer))))
    tolerance = float(np.max(np.abs(low - coarse.sol(grid)) / np.maximum(scale, np.abs(low))))
    residual = max(abs(equations(neutrino_fraction, lmax, float(x), fine.sol(x))[1])
                   for x in grid)
    initial_residual = abs(equations(neutrino_fraction, lmax, x0, start)[1])
    values = (truncation, tolerance, residual, initial_residual)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("Hierarchy validation evidence must be finite")
    return {
        "neutrino_fraction": float(neutrino_fraction), "lmax": lmax, "x0": x0,
        "x_final": x_final, "primordial_psi": primordial_psi,
        "max_truncation_shift_over_psi": truncation,
        "max_tolerance_shift_over_psi": tolerance,
        "max_scaled_00_residual": residual,
        "initial_scaled_00_residual": initial_residual,
        "residual_units": "x^2*phi+6*Theta/x+1.5*delta_bar, dimensionless (k=1)",
        "numerical_gate_passed": bool(truncation < 1e-6 and tolerance < 1e-6
                                              and residual < 1e-6 * scale),
        "scope": "radiation era, photon perfect fluid, free-streaming neutrino hierarchy, "
                 "leading-order initial mode",
        "primordial_initialization_established": False,
        "full_stability_established": False, "scientific_baseline_ready": False,
        "missing": ["photon-baryon coupling, polarization and photon hierarchy",
                    "dust/scalar/vacuum coupling to the hierarchy",
                    "primordial spectrum, transfer functions and observables",
                    "independent Boltzmann validation"],
    }
