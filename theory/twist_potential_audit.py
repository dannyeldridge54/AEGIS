"""Exact audit of an assumed canonical one-field EFT, not a BI derivation.

Reduced Planck units; kinetic term -1/2 (partial q)^2. No fit or file writes.
"""
import json

import sympy as sp


def harmonic_sensitivity():
    """Exact shape diagnostics for fixed illustrative, not fitted, corrections."""
    y = sp.symbols("y", nonnegative=True)
    rows = []
    for epsilon in (sp.Rational(-1, 10000), sp.Integer(0), sp.Rational(1, 10000)):
        shape = y**3 + epsilon * y
        minimum_y = sp.sqrt(-epsilon / 3) if epsilon < 0 else sp.Integer(0)
        minimum_value = sp.simplify(shape.subs(y, minimum_y))
        crossover_y = sp.sqrt(abs(epsilon))
        rows.append({
            "epsilon": str(epsilon),
            "original_minimum_mass_squared_over_A_F2": str(epsilon),
            "global_minimum_one_minus_cos_theta": str(minimum_y),
            "global_minimum_excitation_over_A": str(minimum_value),
            "minimum_stationarity_residual": (
                str(sp.simplify(sp.diff(shape, y).subs(y, minimum_y))) if epsilon < 0 else None
            ),
            "crossover_angle_radians": (
                float(sp.acos(1 - crossover_y)) if epsilon != 0 else None
            ),
            "correction_to_n3_ratio_at_angle_0_1": float(
                abs(epsilon) / (2 * sp.sin(sp.Rational(1, 20))**2)**2
            ),
        })
    return {
        "scope": "Fixed illustrative potential-shape study; no background evolution, fit, or quantum-loop calculation",
        "coordinate": "y = 1-cos(theta), physical interval [0, 2]",
        "corrected_shape_over_A": "y**3 + epsilon*y",
        "mass_normalization": "m_squared = (A/F**2)*reported_coefficient at the original minimum",
        "negative_correction_scope": "Negative excitation minimum may be offset by an independent vacuum constant; no total-density or cosmological verdict",
        "robustness_established": False,
        "rows": rows,
    }


def calculate():
    q = sp.symbols("q", real=True)
    amplitude, decay = sp.symbols("A F", positive=True)
    vacuum = sp.symbols("V_Lambda", nonnegative=True)
    theta = q / decay
    potential = vacuum + amplitude * (1 - sp.cos(theta)) ** 3
    harmonics = vacuum + amplitude * (
        sp.Rational(5, 2) - sp.Rational(15, 4) * sp.cos(theta)
        + sp.Rational(3, 2) * sp.cos(2 * theta)
        - sp.Rational(1, 4) * sp.cos(3 * theta)
    )
    epsilon = sp.symbols("epsilon", real=True)
    corrected = potential + epsilon * amplitude * (1 - sp.cos(theta))
    curvature = sp.diff(potential, q, 2)
    velocity = sp.symbols("q_dot", real=True)
    rho = velocity**2 / 2 + potential
    pressure = velocity**2 / 2 - potential
    hubble, acceleration = sp.symbols("H q_ddot", real=True)
    continuity = sp.diff(rho, q) * velocity + sp.diff(rho, velocity) * acceleration
    continuity += 3 * hubble * (rho + pressure)
    eom = acceleration + 3 * hubble * velocity + sp.diff(potential, q)
    factored_curvature = (
        3 * amplitude / decay**2 * (1 - sp.cos(theta)) ** 2 * (2 + 3 * sp.cos(theta))
    )
    kinetic = sp.symbols("X", real=True)
    lagrangian = kinetic - potential
    gradient_coefficient = sp.diff(lagrangian, kinetic)
    time_coefficient = gradient_coefficient + 2 * kinetic * sp.diff(lagrangian, kinetic, 2)
    chi, slope = sp.symbols("chi lambda", real=True)
    metric_radius = sp.exp(slope * chi / 2)
    field_space_curvature = sp.simplify(-2 * sp.diff(metric_radius, chi, 2) / metric_radius)
    c_dot, t_dot, c_ddot, t_ddot, vc, vt = sp.symbols(
        "chi_dot theta_dot chi_ddot theta_ddot V_chi V_theta", real=True
    )
    metric = metric_radius**2
    chi_eom = c_ddot + 3 * hubble * c_dot - slope * metric * t_dot**2 / 2 + vc
    theta_eom = t_ddot + 3 * hubble * t_dot + slope * c_dot * t_dot + vt / metric
    rho_derivative = (
        c_dot * c_ddot + metric * t_dot * t_ddot
        + slope * metric * c_dot * t_dot**2 / 2 + vc * c_dot + vt * t_dot
    )
    two_field_continuity = rho_derivative + 3 * hubble * (c_dot**2 + metric * t_dot**2)
    two_field_residual = sp.simplify(
        two_field_continuity - c_dot * chi_eom - metric * t_dot * theta_eom
    )
    return {
        "scope": "Assumed canonical single-field EFT; not the full two-field BI system",
        "potential": str(potential),
        "harmonic_identity_residual": str(sp.trigsimp(sp.expand_trig(potential - harmonics))),
        "periodicity_residual": str(sp.trigsimp(potential.subs(q, q + 2 * sp.pi * decay) - potential)),
        "harmonic_coefficients_over_A": ["5/2", "-15/4", "3/2", "-1/4"],
        "minimum_value": str(potential.subs(q, 0)),
        "minimum_curvature": str(curvature.subs(q, 0)),
        "minimum_sixth_derivative": str(sp.diff(potential, q, 6).subs(q, 0)),
        "hilltop_curvature": str(curvature.subs(q, sp.pi * decay)),
        "curvature_factorization_residual": str(sp.trigsimp(curvature - factored_curvature)),
        "negative_curvature_domain": "cos(q/F) < -2/3",
        "inflection_cosine": "-2/3",
        "perturbation_time_kinetic_coefficient": str(time_coefficient),
        "perturbation_gradient_coefficient": str(gradient_coefficient),
        "canonical_short_wavelength_sound_speed_squared": str(gradient_coefficient / time_coefficient),
        "sound_speed_scope": "Principal part of canonical one-field perturbations; not averaged fluid sound speed or full BI stability",
        "hilltop_instability_scope": "Negative curvature can amplify long-wavelength modes; Hubble friction and gravitational coupling determine actual growth",
        "separate_two_field_metric": "diag(1, exp(lambda*chi)), reduced Planck units",
        "separate_two_field_ricci_scalar": str(field_space_curvature),
        "bi_slope_ricci_scalar": str(field_space_curvature.subs(slope, -2 * sp.sqrt(sp.Rational(2, 3)))),
        "two_field_continuity_eom_identity_residual": str(two_field_residual),
        "christoffel_chi_theta_theta": str(-sp.diff(metric, chi) / 2),
        "christoffel_theta_chi_theta": str(sp.diff(metric, chi) / (2 * metric)),
        "field_space_scope": "Negative curvature is not a ghost or proof of instability; covariant potential Hessian and trajectory turn rate are required",
        "lambda_limit_residual": str(potential.subs(amplitude, 0) - vacuum),
        "lambda_limit_scope": "Requires vanishing scalar kinetic energy; amplitude zero alone is insufficient",
        "rho_plus_pressure": str(sp.simplify(rho + pressure)),
        "continuity_eom_identity_residual": str(sp.simplify(continuity - velocity * eom)),
        "amplitude_zero_kinetic_scaling": "q_dot proportional to a**(-3); kinetic density proportional to a**(-6)",
        "small_oscillation_mean_w": "1/2",
        "small_oscillation_density_scaling": "a**(-9/2)",
        "oscillation_scope": "Scalar excitation only: small amplitude q**6, rapid oscillations relative to H, negligible constant offset in excitation energy",
        "leading_cosine_corrected_mass_squared": str(sp.diff(corrected, q, 2).subs(q, 0)),
        "kinetic_sign": "Positive canonical kinetic energy assumed; no kinetic ghost in this one-field EFT",
        "vacuum_stability": "Global minima at q = 2*pi*k*F; bounded below by V_Lambda",
        "linear_stability_scope": "Minimum is massless at quadratic order; hilltops have negative curvature",
        "naturalness": "Exact n=3 harmonic cancellations are assumed; periodicity alone does not protect them",
        "correction_scope": "Positive epsilon introduces a mass; negative epsilon destabilizes the original minimum",
        "microscopic_derivation_established": False,
        "full_bi_stability_established": False,
        "observational_fit_performed": False,
        "claim_limits": {
            "model_classification": "assumed effective model",
            "microscopic_confirmation_permitted": False,
            "full_stability_claim_permitted": False,
            "independent_observational_confirmation_permitted": False,
            "reason": "Neither algebraic identities nor in-sample fit improvement closes the missing physical gates",
        },
        "harmonic_sensitivity": harmonic_sensitivity(),
    }


if __name__ == "__main__":
    print(json.dumps(calculate(), indent=2))
