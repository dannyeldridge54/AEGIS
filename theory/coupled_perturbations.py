"""Newtonian-gauge linear scalar/dust/perfect-radiation equations.

Reduced Planck units, no anisotropic stress: ds²=a²[-(1+2Phi)deta²+
(1-2Phi)dx²]. This is not a photon/neutrino Boltzmann hierarchy.
"""
from dataclasses import replace
import math

import numpy as np
from scipy.integrate import solve_ivp

from theory.effective_baseline import evolve


def radiation_adiabatic_initial_state(config, k_over_Href, *, primordial_phi=1e-5):
    """Regular growing mode for pure radiation and a resting scalar extremum.

    primordial_phi is the x -> 0 Newtonian potential, not a power spectrum.
    x=k*eta/sqrt(3)=k*exp(N)/sqrt(radiation_today); require 0 < x <= .01.
    Dust variables are passive test-fluid limits since its background is zero.
    See DERIVATION_CHAIN.md for the series and its restricted domain.
    """
    if not math.isfinite(k_over_Href) or k_over_Href <= 0:
        raise ValueError("Adiabatic initialization requires finite positive comoving k/Href")
    if not math.isfinite(primordial_phi) or not 0 < abs(primordial_phi) <= 1e-3:
        raise ValueError("Adiabatic potential must be finite, nonzero and within the linear bound 1e-3")
    if (config.matter_today != 0 or config.radiation_today <= 0
            or config.initial_field != 0 or config.initial_field_prime != 0
            or config.vacuum != 0):
        raise ValueError(
            "Adiabatic initialization supports only pure radiation, zero vacuum "
            "and a scalar resting at field=0; mixed fluids and rolling fields are unsupported"
        )
    try:
        config.background(config.initial_N, 0., 0.)
        x = k_over_Href * math.exp(config.initial_N) / math.sqrt(config.radiation_today)
        wave2 = 3 * x**2
    except OverflowError as error:
        raise ValueError("Adiabatic background or wavelength coefficient overflowed") from error
    if not math.isfinite(x) or not 0 < x <= .01 or wave2 == 0:
        raise ValueError("Adiabatic initialization requires resolved superhorizon 0 < x <= .01")
    x2 = x * x
    phi = primordial_phi * (1 + x2 * (-1 / 10 + x2 * (1 / 280 - x2 / 15120)))
    phi_prime = primordial_phi * x2 * (-1 / 5 + x2 * (1 / 70 - x2 / 2520))
    momentum = phi + phi_prime
    radiation_density = -2 * momentum - 2 * wave2 * phi / 3
    radiation_velocity = wave2 * momentum / 2
    dust_density = primordial_phi * (
        -3 / 2 + x2 * (-21 / 20 + x2 * (33 / 1120 - x2 / 2016))
    )
    dust_velocity = primordial_phi * x2 * (3 / 2 + x2 * (-3 / 40 + x2 / 560))
    state = np.array([0., 0., dust_density, dust_velocity,
                      radiation_density, radiation_velocity, phi])
    if not np.all(np.isfinite(state)) or radiation_velocity == 0:
        raise ValueError("Adiabatic state is not numerically resolved")
    return state


def mixed_adiabatic_initial_state(config, k_over_Href, *, primordial_phi=1e-5):
    """Regular radiation/dust mode through eighth order in the initial scale factor.

    Requires radiation-era, superhorizon initialization (y <= .01, x <= .01),
    zero vacuum and a scalar resting at field=0. y=rho_m/rho_r and
    x=k*exp(N)/sqrt(radiation_today). Phi0 is the asymptotic radiation-era
    Newtonian potential, not a power spectrum. No density projection is used.
    """
    if not math.isfinite(k_over_Href) or k_over_Href <= 0:
        raise ValueError("Mixed adiabatic initialization requires finite positive comoving k/Href")
    if not math.isfinite(primordial_phi) or not 0 < abs(primordial_phi) <= 1e-3:
        raise ValueError("Adiabatic potential must be finite, nonzero and within the linear bound 1e-3")
    if (config.radiation_today <= 0 or config.initial_field != 0
            or config.initial_field_prime != 0 or config.vacuum != 0):
        raise ValueError(
            "Mixed adiabatic initialization requires positive radiation, zero vacuum "
            "and a scalar resting at field=0"
        )
    try:
        config.background(config.initial_N, 0., 0.)
        scale = math.exp(config.initial_N)
        y = config.matter_today * scale / config.radiation_today
        x = k_over_Href * scale / math.sqrt(config.radiation_today)
        wave2 = 3 * x**2 / (1 + y)
    except OverflowError as error:
        raise ValueError("Mixed adiabatic background or wavelength overflowed") from error
    if (not math.isfinite(y) or not 0 <= y <= .01
            or not math.isfinite(x) or not 0 < x <= .01 or wave2 == 0):
        raise ValueError("Mixed adiabatic initialization requires resolved y <= .01 and 0 < x <= .01")

    # Z=(delta_m, t_m/W, delta_r, t_r/W, Phi); s=a/a_initial.
    matrices = np.zeros((9, 5, 5))
    for n in range(9):
        inverse = (-y)**n
        momentum = np.array([0., 1.5 * y * (-y)**(n - 1) if n else 0.,
                             0., 2 * inverse, -1. if n == 0 else 0.])
        matrices[n, 0] = 3 * momentum
        matrices[n, 2] = 4 * momentum
        matrices[n, 4] = momentum
        matrices[n, 1, 1] = -.5 * inverse - (1.5 if n == 0 else 0.)
        matrices[n, 3, 3] = -.5 * inverse - (.5 if n == 0 else 0.)
        if n == 0:
            matrices[n, 1, 4] = 1.
            matrices[n, 3, 2] = .25
            matrices[n, 3, 4] = 1.
        if n >= 2:
            wave_coefficient = 3 * x**2 * (-y)**(n - 2)
            matrices[n, 0, 1] -= wave_coefficient
            matrices[n, 2, 3] -= 4 * wave_coefficient / 3
    coefficients = np.zeros((9, 5))
    coefficients[0] = [-1.5, .5, -2., .5, 1.]
    for n in range(1, 9):
        source = sum(matrices[j] @ coefficients[n - j] for j in range(1, n + 1))
        operator = n * np.eye(5) - matrices[0]
        if n == 1:
            # The s^1 constraint-violating mode makes the evolution system
            # singular. The independent 00 equation fixes its coefficient.
            operator[2] = [0., 0., 1.5, 6., 0.]
            source[2] = -y * (1.5 * coefficients[0, 0] + 4.5 * coefficients[0, 1])
        coefficients[n] = np.linalg.solve(operator, source)
    dm, um, dr, ur, phi = primordial_phi * coefficients.sum(axis=0)
    state = np.array([0., 0., dm, wave2 * um, dr, wave2 * ur, phi])
    if not np.all(np.isfinite(state)) or state[3] == 0 or state[5] == 0:
        raise ValueError("Mixed adiabatic state is not numerically resolved")
    return state


def subdominant_field_adiabatic_initial_state(config, k_over_Href, *, primordial_phi=1e-5,
                                              max_field_fraction=1e-6):
    """First-order-in-f adiabatic mode for a displaced/rolling subdominant scalar.

    f=(V+H2*field_prime^2/2)/(3*H2) is the scalar share of the Friedmann
    budget at the initial epoch and must be <= max_field_fraction (<= 1e-6).
    Fluid variables are the resting-scalar mixed series; its theta/(aH)
    velocities are rescaled by H2_true/H2_fluid and Phi' includes the scalar
    momentum prime*dq/2, so the 00 residual is O(f*x^2*Phi0) rather than
    O(f*Phi0). The scalar follows the common time shift dN=-delta_r/4, so
    dq=field_prime*dN and dq'=field_prime'*dN+field_prime*dN', with
    field_prime' from the background equation and dN'=-delta_r'/4 from the
    radiation equation. Nonzero vacuum enters only through f. The 00
    constraint is verified by the caller/integrate, never projected away.
    """
    if not math.isfinite(max_field_fraction) or not 0 < max_field_fraction <= 1e-6:
        raise ValueError("Subdominant-field fraction bound must lie in (0, 1e-6]")
    if config.radiation_today <= 0:
        raise ValueError("Subdominant-field initialization requires positive radiation")
    try:
        h2, epsilon = config.background(config.initial_N, config.initial_field,
                                        config.initial_field_prime)
        potential, gradient = config.potential(config.initial_field)
        fraction = (potential + h2 * config.initial_field_prime**2 / 2) / (3 * h2)
    except OverflowError as error:
        raise ValueError("Subdominant-field background overflowed") from error
    if not math.isfinite(fraction) or not 0 <= fraction <= max_field_fraction:
        raise ValueError("Scalar energy fraction exceeds the subdominant-field approximation")
    fluid_config = replace(config, initial_field=0., initial_field_prime=0., vacuum=0.)
    state = mixed_adiabatic_initial_state(fluid_config, k_over_Href,
                                          primordial_phi=primordial_phi)
    _, _, dm, tm, dr, tr, phi = state
    scale = math.exp(config.initial_N)
    matter = config.matter_today * scale**-3 / h2 if config.matter_today else 0.0
    radiation = config.radiation_today * scale**-4 / h2
    wave2 = (k_over_Href / scale)**2 / h2
    # theta/(aH) carries 1/H: rescale the fluid series' velocities (built with
    # the fluid-only H2) to the true H2, so momentum matter*um+4*rad*ur/3 is kept.
    fluid_h2 = fluid_config.background(config.initial_N, 0., 0.)[0]
    ratio = h2 / fluid_h2
    tm, tr = tm / ratio, tr / ratio
    state[3], state[5] = tm, tr
    prime = config.initial_field_prime
    shift = -dr / 4
    momentum = (matter * tm + 4 * radiation * tr / 3) / (2 * wave2) + prime * prime * shift / 2
    phi_prime = momentum - phi
    shift_prime = -(-4 * tr / 3 + 4 * phi_prime) / 4
    prime_prime = -(3 - epsilon) * prime - gradient / h2
    state[0] = prime * shift
    state[1] = prime_prime * shift + prime * shift_prime
    if not np.all(np.isfinite(state)):
        raise ValueError("Subdominant-field adiabatic state is not numerically resolved")
    return state


def equations(config, background, N, state, k_over_Href):
    """Return N derivatives and independent 00 constraint.

    State: deltaq, deltaq_prime, delta_m, theta_m/(aH),
    delta_r, theta_r/(aH), Phi. k/Href is comoving, strictly positive.
    """
    state = np.asarray(state, dtype=float)
    if state.shape != (7,) or not np.all(np.isfinite(state)):
        raise ValueError("Coupled perturbation state requires seven finite components")
    if not math.isfinite(k_over_Href) or k_over_Href <= 0:
        raise ValueError("Coupled equations require finite positive comoving k/Href")
    if getattr(background, "background_config", None) != config:
        raise ValueError("Coupled background does not match the supplied configuration")
    if not math.isfinite(N) or not background.t[0] <= N <= background.t[-1]:
        raise ValueError("Coupled evaluation must lie in the background interval")
    field, prime = background.sol(N)
    h2, epsilon = config.background(N, field, prime)
    gradient = config.potential(field)[1]
    curvature = config.potential_curvature(field)
    dq, dp, dm, tm, dr, tr, phi = state
    try:
        matter = config.matter_today * math.exp(-3 * N) / h2 if config.matter_today else 0.0
        radiation = config.radiation_today * math.exp(-4 * N) / h2 if config.radiation_today else 0.0
        wave2 = (k_over_Href * math.exp(-N))**2 / h2
        if not math.isfinite(wave2) or wave2 <= 0:
            raise ValueError("Coupled wavenumber coefficient is not numerically resolved")
        momentum = (matter * tm + 4 * radiation * tr / 3) / (2 * wave2) + prime * dq / 2
        phi_prime = momentum - phi
        derivatives = np.array([
            dp,
            -(3 - epsilon) * dp - (wave2 + curvature / h2) * dq
            + 4 * prime * phi_prime - 2 * gradient * phi / h2,
            -tm + 3 * phi_prime,
            -(2 - epsilon) * tm + wave2 * phi,
            -4 * tr / 3 + 4 * phi_prime,
            -(1 - epsilon) * tr + wave2 * (dr / 4 + phi),
            phi_prime,
        ])
        density = matter * dm + radiation * dr + prime * dp - prime**2 * phi + gradient * dq / h2
        constraint = wave2 * phi + 3 * momentum + density / 2
    except OverflowError as error:
        raise ValueError("Coupled perturbation coefficients overflowed") from error
    if not np.all(np.isfinite(derivatives)) or not math.isfinite(constraint):
        raise ValueError("Coupled perturbation equations must remain finite")
    return derivatives, float(constraint)


def integrate(config, initial_state, k_over_Href, *, method="DOP853",
              rtol=1e-10, atol=1e-12, max_step=None):
    """Integrate explicit constraint-compatible modes; no primordial prescription."""
    initial_state = np.asarray(initial_state, dtype=float)
    if initial_state.shape != (7,) or not np.all(np.isfinite(initial_state)):
        raise ValueError("Initial coupled state requires seven finite components")
    if method not in ("RK45", "DOP853"):
        raise ValueError("Supported coupled methods are RK45 and DOP853")
    if not all(math.isfinite(v) and v > 0 for v in (rtol, atol)):
        raise ValueError("Coupled tolerances must be finite and positive")
    if max_step is None:
        max_step = (config.final_N - config.initial_N) / 400
    if not math.isfinite(max_step) or max_step <= 0:
        raise ValueError("Coupled maximum step must be finite and positive")
    background = evolve(config, method="DOP853", rtol=1e-12, atol=1e-14,
                        max_step=max_step / 2)
    _, constraint = equations(config, background, config.initial_N, initial_state, k_over_Href)
    # Absolute residual in dimensionless Einstein equation units.
    if abs(constraint) > 1e-10:
        raise ValueError("Initial coupled state violates the Einstein density constraint")
    solution = solve_ivp(
        lambda N, state: equations(config, background, N, state, k_over_Href)[0],
        (config.initial_N, config.final_N), initial_state, method=method,
        rtol=rtol, atol=atol, max_step=max_step, dense_output=True,
    )
    if not solution.success:
        raise ValueError(f"Coupled integration failed: {solution.message}")
    epochs = np.asarray(solution.t)
    states = np.asarray(solution.y)
    if (solution.sol is None or epochs.ndim != 1 or epochs.size < 2
            or states.shape != (7, epochs.size) or not np.all(np.isfinite(states))
            or not np.all(np.isfinite(epochs)) or np.any(np.diff(epochs) <= 0)
            or epochs[0] != config.initial_N or epochs[-1] != config.final_N):
        raise ValueError("Coupled integration lacks finite full-interval output")
    solution.background = background
    return solution


def validate(config, initial_state, k_over_Href):
    """Sample convergence and constraint drift; never assert full physical validity."""
    step = (config.final_N - config.initial_N) / 400
    coarse = integrate(config, initial_state, k_over_Href, method="RK45", max_step=step)
    fine = integrate(config, initial_state, k_over_Href, max_step=step / 2,
                     rtol=1e-12, atol=1e-14)
    grid = np.unique(np.concatenate((
        np.linspace(config.initial_N, config.final_N, 201), coarse.t, fine.t,
    )))
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            fine_states = fine.sol(grid)
            shift = float(np.max(
                np.abs(coarse.sol(grid) - fine_states) / np.maximum(1., np.abs(fine_states))
            ))
            initial_shift = max(float(np.max(np.abs(
                sol.sol(config.initial_N) - initial_state
            ) / np.maximum(1., np.abs(initial_state)))) for sol in (coarse, fine))
        except FloatingPointError as error:
            raise ValueError("Coupled validation arithmetic overflowed") from error
    constraint = max(abs(equations(config, sol.background, float(N), sol.sol(N),
                                   k_over_Href)[1])
                     for sol in (coarse, fine) for N in grid)
    if not all(math.isfinite(v) for v in (shift, initial_shift, constraint)):
        raise ValueError("Coupled validation evidence must be finite")
    equation_residual = 0.0
    equation_samples = 0
    difference_step = min(1e-5, (config.final_N - config.initial_N) / 1000)
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            for sol in (coarse, fine):
                for N in grid:
                    if not config.initial_N + 2 * difference_step <= N <= config.final_N - 2 * difference_step:
                        continue
                    if N + difference_step == N or N - difference_step == N:
                        raise ValueError("Coupled derivative interval is not numerically resolved")
                    derivative = (
                        sol.sol(N - 2 * difference_step) - 8 * sol.sol(N - difference_step)
                        + 8 * sol.sol(N + difference_step) - sol.sol(N + 2 * difference_step)
                    ) / (12 * difference_step)
                    expected = equations(config, sol.background, float(N), sol.sol(N),
                                         k_over_Href)[0]
                    residual = float(np.max(
                        np.abs(derivative - expected) / np.maximum(1., np.abs(expected))
                    ))
                    if not math.isfinite(residual):
                        raise ValueError("Coupled equation residual must be finite")
                    equation_residual = max(equation_residual, residual)
                    equation_samples += 1
        except FloatingPointError as error:
            raise ValueError("Coupled derivative validation overflowed") from error
    if equation_samples == 0:
        raise ValueError("Coupled validation lacks interior derivative evidence")
    return {
        "inputs": vars(config).copy(), "initial_state": np.asarray(initial_state).tolist(),
        "k_over_Href": k_over_Href, "sample_count": int(grid.size),
        "max_scaled_state_shift": shift, "max_scaled_initial_shift": initial_shift,
        "max_absolute_density_constraint": constraint,
        "max_scaled_equation_residual": equation_residual,
        "equation_sample_count": equation_samples,
        "equation_residual_scope": "Both solvers, interior five-point derivatives, scaled by max(1,abs(rhs))",
        "constraint_units": "dimensionless 00 Einstein equation divided by H2",
        "numerical_gate_passed": bool(shift < 1e-7 and initial_shift < 1e-10
                                      and constraint < 1e-8 and equation_residual < 1e-5),
        "scope": "Newtonian scalar/dust/perfect-radiation linear trajectory with explicit initial state",
        "primordial_initialization_established": False,
        "full_stability_established": False, "scientific_baseline_ready": False,
        "missing": ["photon/neutrino hierarchy and anisotropic stress",
                    "general-background/rolling-scalar primordial initialization and spectrum normalization",
                    "independent Boltzmann validation and observable likelihoods"],
    }
