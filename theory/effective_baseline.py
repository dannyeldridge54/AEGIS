"""Separate canonical EFT background baseline, not a fit or microscopic model.

Reduced Planck units; densities in M_Pl**2 H_ref**2, N=ln(a), a_today=1.
"""
from dataclasses import dataclass
import math

import numpy as np
from scipy.integrate import solve_ivp


@dataclass(frozen=True)
class Baseline:
    amplitude: float = 2.0
    first_order: float = 0.0
    second_order: float = 0.0
    vacuum: float = 2.1
    decay: float = 1.0
    matter_today: float = 0.9
    radiation_today: float = 0.00027
    initial_N: float = -8.0
    final_N: float = 0.0
    initial_field: float = 0.5
    initial_field_prime: float = 0.0

    def __post_init__(self):
        if not all(math.isfinite(value) for value in vars(self).values()):
            raise ValueError("Baseline inputs must be finite")
        if self.amplitude <= 0 or self.decay <= 0:
            raise ValueError("Amplitude and decay must be positive")
        if min(self.matter_today, self.radiation_today) < 0:
            raise ValueError("Background densities must be nonnegative")
        if self.final_N <= self.initial_N:
            raise ValueError("Final epoch must follow the initial epoch")
        if self.initial_field_prime**2 >= 6:
            raise ValueError("Initial Friedmann kinetic denominator must be positive")

    def potential(self, field):
        if not math.isfinite(field):
            raise ValueError("Field must be finite")
        x = field / self.decay
        y = 2 * math.sin(x / 2)**2
        value = self.vacuum + self.amplitude * (
            y**3 + self.second_order * y**2 + self.first_order * y
        )
        gradient = self.amplitude * (
            3 * y**2 + 2 * self.second_order * y + self.first_order
        ) * math.sin(x) / self.decay
        if not math.isfinite(value) or not math.isfinite(gradient):
            raise ValueError("Potential and gradient must remain finite")
        return value, gradient

    def background(self, N, field, field_prime):
        if not all(math.isfinite(v) for v in (N, field, field_prime)):
            raise ValueError("Background state must be finite")
        potential, _ = self.potential(field)
        matter = self.matter_today * math.exp(-3 * N) if self.matter_today else 0.0
        radiation = self.radiation_today * math.exp(-4 * N) if self.radiation_today else 0.0
        denominator = 3 - field_prime**2 / 2
        if denominator <= 0:
            raise ValueError("Invalid Friedmann kinetic denominator")
        h2 = (matter + radiation + potential) / denominator
        if not math.isfinite(h2) or h2 <= 0:
            raise ValueError("Expansion squared must be finite and positive")
        epsilon = (matter + 4 * radiation / 3 + h2 * field_prime**2) / (2 * h2)
        if not math.isfinite(epsilon):
            raise ValueError("Expansion derivative must remain finite")
        return h2, epsilon

    def potential_curvature(self, field):
        """Second canonical-field derivative, including independent corrections."""
        if not math.isfinite(field):
            raise ValueError("Field must be finite")
        x = field / self.decay
        y = 2 * math.sin(x / 2)**2
        curvature = self.amplitude / self.decay**2 * (
            (6 * y + 2 * self.second_order) * math.sin(x)**2
            + (3 * y**2 + 2 * self.second_order * y + self.first_order) * math.cos(x)
        )
        if not math.isfinite(curvature):
            raise ValueError("Potential curvature must remain finite")
        return curvature


def evolve(config, rtol=1e-9, atol=1e-11, method="RK45", max_step=None):
    if not all(math.isfinite(v) and v > 0 for v in (rtol, atol)):
        raise ValueError("Tolerances must be finite and positive")
    if method not in ("RK45", "DOP853"):
        raise ValueError("Supported baseline methods are RK45 and DOP853")
    if max_step is None:
        max_step = (config.final_N - config.initial_N) / 200
    if not math.isfinite(max_step) or max_step <= 0:
        raise ValueError("Maximum integration step must be finite and positive")

    def rhs(N, state):
        field, prime = state
        h2, epsilon = config.background(N, field, prime)
        gradient = config.potential(field)[1]
        return [prime, -(3 - epsilon) * prime - gradient / h2]

    solution = solve_ivp(
        rhs, (config.initial_N, config.final_N),
        [config.initial_field, config.initial_field_prime],
        rtol=rtol, atol=atol, method=method, max_step=max_step, dense_output=True,
    )
    if not solution.success:
        raise ValueError(f"Baseline integration failed: {solution.message}")
    if solution.sol is None or not np.all(np.isfinite(solution.y)):
        raise ValueError("Baseline integration lacks finite dense output")
    epochs = np.asarray(solution.t)
    if (epochs.ndim != 1 or epochs.size < 2 or not np.all(np.isfinite(epochs))
            or np.asarray(solution.y).shape != (2, epochs.size)
            or np.any(np.diff(epochs) <= 0)
            or epochs[0] != config.initial_N or epochs[-1] != config.final_N):
        raise ValueError("Baseline integration does not cover the requested epoch interval")
    solution.background_config = config
    return solution


def validate(config):
    """Fixed numerical gates on this input; no tuning or fit."""
    coarse = evolve(config)
    fine = evolve(config, rtol=1e-11, atol=1e-13, method="DOP853",
                  max_step=(config.final_N - config.initial_N) / 400)
    grid = np.unique(np.concatenate((
        np.linspace(config.initial_N, config.final_N, 201), coarse.t, fine.t,
    )))
    max_expansion_shift = 0.0
    max_continuity_residual = 0.0
    max_raychaudhuri_residual = 0.0
    max_field_equation_residual = 0.0
    max_state_shift = 0.0
    initial_state = np.array([config.initial_field, config.initial_field_prime])
    max_initial_state_shift = 0.0
    for solution in (coarse, fine):
        actual_initial = solution.sol(config.initial_N)
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            try:
                initial_shift = float(np.max(
                    np.abs(actual_initial - initial_state)
                    / np.maximum(1.0, np.abs(initial_state))
                ))
            except FloatingPointError as error:
                raise ValueError("Initial-state comparison overflowed") from error
        if not math.isfinite(initial_shift):
            raise ValueError("Initial-state comparison must be finite")
        max_initial_state_shift = max(max_initial_state_shift, initial_shift)
    continuity_sample_count = 0
    step = min(1e-4, (config.final_N - config.initial_N) / 1000)

    def scalar_density(N):
        field, prime = fine.sol(N)
        h2, _ = config.background(N, field, prime)
        potential, _ = config.potential(field)
        return h2 * prime**2 / 2 + potential

    for N in grid:
        fine_state, coarse_state = fine.sol(N), coarse.sol(N)
        if not np.all(np.isfinite(fine_state)) or not np.all(np.isfinite(coarse_state)):
            raise ValueError("Validation states must be finite")
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            try:
                state_shift = float(np.max(
                    np.abs(coarse_state - fine_state) / np.maximum(1.0, np.abs(fine_state))
                ))
            except FloatingPointError as error:
                raise ValueError("State comparison overflowed") from error
        if not math.isfinite(state_shift):
            raise ValueError("State comparison must be finite")
        max_state_shift = max(max_state_shift, state_shift)
        field, prime = fine_state
        h2, epsilon = config.background(N, field, prime)
        other = config.background(N, *coarse.sol(N))[0]
        expansion_shift = float(abs(other / h2 - 1))
        if not math.isfinite(expansion_shift):
            raise ValueError("Expansion comparison must be finite")
        max_expansion_shift = max(max_expansion_shift, expansion_shift)
        if config.initial_N + step <= N <= config.final_N - step:
            before_state = fine.sol(N - step)
            after_state = fine.sol(N + step)
            if not np.all(np.isfinite(before_state)) or not np.all(np.isfinite(after_state)):
                raise ValueError("Field-equation comparison states must be finite")
            with np.errstate(over="raise", invalid="raise", divide="raise"):
                try:
                    state_derivative = (after_state - before_state) / (2 * step)
                    acceleration = -(3 - epsilon) * prime - config.potential(field)[1] / h2
                    expected_derivative = np.array([prime, acceleration])
                    equation_residual = float(np.max(
                        np.abs(state_derivative - expected_derivative)
                        / np.maximum(1.0, np.abs(expected_derivative))
                    ))
                except FloatingPointError as error:
                    raise ValueError("Field-equation comparison overflowed") from error
            if not math.isfinite(equation_residual):
                raise ValueError("Field-equation validation residual must be finite")
            max_field_equation_residual = max(max_field_equation_residual, equation_residual)
            before = config.background(N - step, *before_state)[0]
            after = config.background(N + step, *after_state)[0]
            expansion_derivative = (math.log(after) - math.log(before)) / (2 * step)
            raychaudhuri_residual = abs(expansion_derivative + 2 * epsilon)
            if not math.isfinite(raychaudhuri_residual):
                raise ValueError("Raychaudhuri validation residual must be finite")
            max_raychaudhuri_residual = max(max_raychaudhuri_residual, raychaudhuri_residual)
            derivative = (scalar_density(N + step) - scalar_density(N - step)) / (2 * step)
            residual = abs(derivative + 3 * h2 * prime**2) / (3 * h2)
            if not math.isfinite(residual):
                raise ValueError("Continuity validation residual must be finite")
            max_continuity_residual = max(max_continuity_residual, residual)
            continuity_sample_count += 1
    if continuity_sample_count == 0:
        raise ValueError("No continuity samples were evaluated; epoch interval is not numerically resolved")
    return {
        "inputs": vars(config).copy(),
        "scope": "Separate assumed canonical EFT background, not fitted data or torsion derivation",
        "sample_count": len(grid),
        "continuity_sample_count": continuity_sample_count,
        "continuity_endpoint_scope": "Central differences evaluated only inside the integration interval",
        "sampling_basis": "Uniform grid plus both solvers' accepted step points",
        "maximum_sample_gap_N": float(np.max(np.diff(grid))),
        "coarse_max_step_N": (config.final_N - config.initial_N) / 200,
        "refined_max_step_N": (config.final_N - config.initial_N) / 400,
        "max_relative_H2_shift": float(max_expansion_shift),
        "max_scaled_field_velocity_shift": max_state_shift,
        "max_scaled_initial_state_shift": max_initial_state_shift,
        "comparison_methods": ["RK45", "DOP853"],
        "state_scale_definition": "abs(coarse-fine)/max(1,abs(fine)) per field/velocity component",
        "max_continuity_residual_over_total_density": float(max_continuity_residual),
        "max_raychaudhuri_residual": float(max_raychaudhuri_residual),
        "raychaudhuri_residual_definition": "abs(d ln(H2)/dN + 2*epsilon), interior central differences",
        "max_scaled_field_equation_residual": max_field_equation_residual,
        "field_equation_residual_definition": (
            "abs(dense-output central derivative - [qprime, -(3-epsilon)*qprime-Vq/H2])"
            "/max(1,abs(expected derivative)) per component"
        ),
        "numerical_gate_passed": bool(max_expansion_shift < 1e-7 and max_state_shift < 1e-7
                                      and max_continuity_residual < 1e-5
                                      and max_raychaudhuri_residual < 1e-5
                                      and max_field_equation_residual < 1e-5
                                      and max_initial_state_shift < 1e-10),
        "H_reference_is_not_shot_to_today": True,
        "perturbation_gate": "unimplemented: gravitational/matter modes, initial spectrum and growth",
        "microscopic_gate": "unresolved",
        "scientific_baseline_ready": False,
    }
