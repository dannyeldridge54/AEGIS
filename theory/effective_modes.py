"""Fixed-metric scalar modes for the canonical EFT; not coupled cosmological modes."""
import math

import numpy as np
from scipy.integrate import solve_ivp

from theory.effective_baseline import evolve


def evolve_mode(config, k_over_Href, initial_mode=1.0, initial_mode_prime=0.0,
                *, method="RK45", rtol=1e-9, atol=1e-11, max_step=None):
    """Evolve a real mode; k/Href is comoving at a_today=1, not k in Mpc^-1."""
    if not all(math.isfinite(v) for v in
               (k_over_Href, initial_mode, initial_mode_prime, rtol, atol)):
        raise ValueError("Mode inputs must be finite")
    if k_over_Href < 0 or min(rtol, atol) <= 0:
        raise ValueError("Wavenumber must be nonnegative and tolerances positive")
    if method not in ("RK45", "DOP853"):
        raise ValueError("Supported mode methods are RK45 and DOP853")
    if max_step is None:
        max_step = (config.final_N - config.initial_N) / 400
    if not math.isfinite(max_step) or max_step <= 0:
        raise ValueError("Mode maximum step must be finite and positive")
    background = evolve(config, method="DOP853", rtol=1e-11, atol=1e-13,
                        max_step=max_step)

    def rhs(N, mode):
        if not np.all(np.isfinite(mode)):
            raise ValueError("Scalar mode became nonfinite")
        field, prime = background.sol(N)
        h2, epsilon = config.background(N, field, prime)
        try:
            frequency2 = (
                (k_over_Href * math.exp(-N))**2 + config.potential_curvature(field)
            ) / h2
            acceleration = -(3 - epsilon) * mode[1] - frequency2 * mode[0]
        except OverflowError as error:
            raise ValueError("Scalar-mode coefficients overflowed") from error
        if not math.isfinite(frequency2) or not math.isfinite(acceleration):
            raise ValueError("Scalar-mode coefficients must remain finite")
        return [mode[1], acceleration]

    solution = solve_ivp(rhs, (config.initial_N, config.final_N),
                         [initial_mode, initial_mode_prime], method=method,
                         rtol=rtol, atol=atol, max_step=max_step, dense_output=True)
    if not solution.success:
        raise ValueError(f"Scalar-mode integration failed: {solution.message}")
    epochs = np.asarray(solution.t)
    states = np.asarray(solution.y)
    if (solution.sol is None or epochs.ndim != 1 or epochs.size < 2
            or states.shape != (2, epochs.size) or not np.all(np.isfinite(states))
            or not np.all(np.isfinite(epochs)) or np.any(np.diff(epochs) <= 0)
            or epochs[0] != config.initial_N or epochs[-1] != config.final_N):
        raise ValueError("Scalar-mode integration lacks finite full-interval output")
    solution.background = background
    return solution


def validate_mode(config, k_over_Href, initial_mode=1.0, initial_mode_prime=0.0):
    """Compare state components on uniform and accepted-step samples; no stability verdict."""
    step = (config.final_N - config.initial_N) / 400
    coarse = evolve_mode(config, k_over_Href, initial_mode, initial_mode_prime,
                         max_step=step)
    fine = evolve_mode(config, k_over_Href, initial_mode, initial_mode_prime,
                       method="DOP853", rtol=1e-11, atol=1e-13, max_step=step / 2)
    grid = np.unique(np.concatenate((
        np.linspace(config.initial_N, config.final_N, 201), coarse.t, fine.t,
    )))
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            fine_state, coarse_state = fine.sol(grid), coarse.sol(grid)
            shift = float(np.max(
                np.abs(coarse_state - fine_state) / np.maximum(1.0, np.abs(fine_state))
            ))
            max_amplitude = float(np.max(np.abs(fine_state[0])))
        except FloatingPointError as error:
            raise ValueError("Mode convergence comparison overflowed") from error
    if not math.isfinite(shift) or not math.isfinite(max_amplitude):
        raise ValueError("Mode convergence evidence must be finite")
    initial_state = np.array([initial_mode, initial_mode_prime])
    initial_shift = 0.0
    equation_shift = 0.0
    equation_samples = 0
    difference_step = min(1e-5, (config.final_N - config.initial_N) / 1000)
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        try:
            for solution in (coarse, fine):
                actual = np.asarray(solution.sol(config.initial_N))
                if actual.shape != (2,) or not np.all(np.isfinite(actual)):
                    raise ValueError("Mode initial state must have two finite components")
                initial_shift = max(initial_shift, float(np.max(
                    np.abs(actual - initial_state) / np.maximum(1.0, np.abs(initial_state))
                )))
            for N in grid:
                if not config.initial_N + 2 * difference_step <= N <= config.final_N - 2 * difference_step:
                    continue
                if N + difference_step == N or N - difference_step == N:
                    raise ValueError("Mode derivative interval is not numerically resolved")
                derivative = (
                    fine.sol(N - 2 * difference_step) - 8 * fine.sol(N - difference_step)
                    + 8 * fine.sol(N + difference_step) - fine.sol(N + 2 * difference_step)
                ) / (12 * difference_step)
                field, prime = fine.background.sol(N)
                h2, epsilon = config.background(N, field, prime)
                frequency2 = ((k_over_Href * math.exp(-N))**2
                              + config.potential_curvature(field)) / h2
                amplitude, velocity = fine.sol(N)
                expected = np.array([velocity, -(3 - epsilon) * velocity - frequency2 * amplitude])
                residual = float(np.max(
                    np.abs(derivative - expected) / np.maximum(1.0, np.abs(expected))
                ))
                if not math.isfinite(residual):
                    raise ValueError("Mode equation residual must be finite")
                equation_shift = max(equation_shift, residual)
                equation_samples += 1
        except (FloatingPointError, OverflowError) as error:
            raise ValueError("Mode equation validation overflowed") from error
    if not math.isfinite(initial_shift) or equation_samples == 0:
        raise ValueError("Mode validation lacks finite initial or interior derivative evidence")
    return {
        "inputs": vars(config).copy(),
        "k_over_Href": k_over_Href,
        "initial_mode": initial_mode,
        "initial_mode_prime": initial_mode_prime,
        "sample_count": int(grid.size),
        "max_scaled_mode_state_shift": shift,
        "max_sampled_absolute_mode": max_amplitude,
        "max_scaled_initial_mode_shift": initial_shift,
        "max_scaled_mode_equation_residual": equation_shift,
        "mode_equation_sample_count": equation_samples,
        "mode_equation_residual_scope": "Interior five-point dense-output derivatives, scaled by max(1,abs(rhs))",
        "numerical_gate_passed": bool(shift < 1e-7 and initial_shift < 1e-10
                                      and equation_shift < 1e-5),
        "scope": "Linear scalar on fixed FLRW metric; no metric sources or backreaction",
        "equation": "deltaq''+(3-epsilon)*deltaq'+(k^2/a^2+Vqq)/H2*deltaq=0",
        "wavenumber_units": "comoving k/Href at a_today=1; not inverse Mpc",
        "initial_condition_scope": "Explicit real mode; not an adiabatic/isocurvature spectrum",
        "full_stability_established": False,
        "scientific_baseline_ready": False,
        "missing": ["metric perturbations and gravitational constraints",
                    "matter/radiation/neutrino modes", "primordial initial spectra",
                    "Boltzmann hierarchy and observable/likelihood validation"],
    }
