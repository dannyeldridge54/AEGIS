"""Numerically evolve the low-energy QCD-anomaly BI axion in an early universe.

This is a homogeneous background calculation for the n=1 QCD cosine potential.
It is not a quantum-loop calculation, a derivation of the n=3 Twist potential,
or a Boltzmann/perturbation likelihood.

Run with ``python -m theory.bi_qcd_dynamics``.
"""
import json
import math
from pathlib import Path

from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from theory.bi_qcd_axion import calculate as calculate_qcd_scales

MPC_METERS = 3.0856775814913673e22
HBAR_C_EV_METERS = 1.973269804e-7


def _background_terms(log_a, equality_growth):
    matter_at_oscillation = 1.0 / (equality_growth + 1.0)
    radiation_at_oscillation = equality_growth / (equality_growth + 1.0)
    radiation = radiation_at_oscillation * math.exp(-4.0 * log_a)
    matter = matter_at_oscillation * math.exp(-3.0 * log_a)
    return radiation, matter


def cdm_replacement_split(ombh2, omch2, target_fraction):
    """Split total CDM into an oscillating scalar and ordinary CDM at equality.

    At equality, radiation and matter have equal densities. The target scalar
    fraction therefore fixes rho_scalar / rho_matter = 2 f. The
    scalar density is subtracted from, not added to, the total CDM density.
    """
    if not all(math.isfinite(value) for value in (ombh2, omch2, target_fraction)):
        raise ValueError("densities and target_fraction must be finite")
    if ombh2 < 0.0 or omch2 <= 0.0:
        raise ValueError("ombh2 must be non-negative and omch2 must be positive")
    if not 0.0 < target_fraction < 1.0:
        raise ValueError("target_fraction must be strictly between zero and one")
    omega_scalar = (
        2.0 * target_fraction * (ombh2 + omch2)
    )
    if omega_scalar >= omch2:
        raise ValueError("the requested scalar fraction cannot fit inside the CDM density")
    return {
        "omega_biqcd_h2": omega_scalar,
        "omega_ordinary_cdm_h2": omch2 - omega_scalar,
        "omega_cdm_total_h2": omch2,
        "fraction_of_total_cdm": omega_scalar / omch2,
    }


def _field_state(log_a, theta, theta_prime, equality_growth, decay_constant_mpl):
    radiation, matter = _background_terms(log_a, equality_growth)
    denominator = 1.0 - decay_constant_mpl**2 * theta_prime**2 / 6.0
    if denominator <= 0.0:
        raise ValueError("scalar kinetic energy violates the Friedmann constraint")
    potential = 3.0 * decay_constant_mpl**2 * (1.0 - math.cos(theta))
    hubble_squared = (radiation + matter + potential) / denominator
    kinetic = decay_constant_mpl**2 * hubble_squared * theta_prime**2 / 6.0
    return hubble_squared, radiation, matter, kinetic, potential


def _evolve_to_wkb(theta_initial, equality_growth, decay_constant_mpl, wkb_threshold):
    equality_log_a = math.log(equality_growth)

    def derivative(log_a, state):
        theta, theta_prime = state
        hubble_squared, radiation, matter, _, _ = _field_state(
            log_a, theta, theta_prime, equality_growth, decay_constant_mpl
        )
        hubble_derivative = (
            -4.0 * radiation - 3.0 * matter
            - decay_constant_mpl**2 * hubble_squared * theta_prime**2
        )
        dln_hubble_dloga = hubble_derivative / (2.0 * hubble_squared)
        return (
            theta_prime,
            -(3.0 + dln_hubble_dloga) * theta_prime
            - 9.0 / hubble_squared * math.sin(theta),
        )

    def reached_wkb(log_a, state):
        hubble_squared, _, _, _, _ = _field_state(
            log_a, state[0], state[1], equality_growth, decay_constant_mpl
        )
        return 3.0 / math.sqrt(hubble_squared) - wkb_threshold

    reached_wkb.terminal = True
    reached_wkb.direction = 1
    solution = solve_ivp(
        derivative,
        (0.0, equality_log_a),
        (theta_initial, 0.0),
        method="DOP853",
        rtol=2e-9,
        atol=2e-12,
        max_step=0.002,
        events=reached_wkb,
    )
    if not solution.success:
        raise RuntimeError(f"scalar-field integration failed: {solution.message}")

    switch_log_a = float(solution.t[-1])
    theta, theta_prime = (float(value) for value in solution.y[:, -1])
    hubble_squared, radiation, matter, kinetic, potential = _field_state(
        switch_log_a, theta, theta_prime, equality_growth, decay_constant_mpl
    )
    scalar_density_at_switch = kinetic + potential
    if solution.t_events[0].size:
        equality_method = "WKB matter-like redshifting after m/H reached the configured threshold"
        scalar_density_at_equality = scalar_density_at_switch * math.exp(
            -3.0 * (equality_log_a - switch_log_a)
        )
    else:
        equality_method = "direct scalar integration through equality"
        scalar_density_at_equality = scalar_density_at_switch

    radiation_at_equality, matter_at_equality = _background_terms(
        equality_log_a, equality_growth
    )
    background_density_at_equality = radiation_at_equality + matter_at_equality
    total_density_at_equality = (
        background_density_at_equality + scalar_density_at_equality
    )
    return {
        "theta_initial_rad": theta_initial,
        "integration_steps": len(solution.t),
        "wkb_started": bool(solution.t_events[0].size),
        "wkb_threshold_m_over_H": wkb_threshold,
        "wkb_switch_log_a": switch_log_a,
        "equality_log_a": equality_log_a,
        "equality_method": equality_method,
        "scalar_density_normalized_at_equality": scalar_density_at_equality,
        "background_density_normalized_at_equality": background_density_at_equality,
        "scalar_fraction_at_equality": (
            scalar_density_at_equality / total_density_at_equality
        ),
        "H_ratio_if_added_to_LCDM": math.sqrt(
            total_density_at_equality / background_density_at_equality
        ),
        "H_ratio_if_replaces_equal_CDM_density": 1.0,
    }


def calculate(target_fraction=0.05, wkb_threshold=300.0, k_max_mpc_inv=10.0):
    """Solve for the initial QCD-axion angle giving a target equality fraction.

    The baseline is radiation plus matter, normalized to H=m/3 at the
    oscillation temperature calculated by :mod:`theory.bi_qcd_axion`. The
    scalar's contribution to the Friedmann constraint and Hubble friction is
    included during direct integration. Once oscillations are sufficiently
    rapid, their averaged density is continued as matter to equality.
    """
    if not 0.0 < target_fraction < 1.0:
        raise ValueError("target_fraction must be strictly between zero and one")
    if not math.isfinite(wkb_threshold) or wkb_threshold <= 3.0:
        raise ValueError("wkb_threshold must be finite and greater than 3")
    if not math.isfinite(k_max_mpc_inv) or k_max_mpc_inv <= 0.0:
        raise ValueError("k_max_mpc_inv must be finite and positive")

    qcd = calculate_qcd_scales()
    equality_growth = qcd["a_equality_over_a_oscillation"]
    decay_constant_mpl = qcd["F_phi_reduced_planck"]
    mass_mpc_inv = (
        qcd["mass_from_susceptibility_eV"] * MPC_METERS / HBAR_C_EV_METERS
    )
    hubble_equality_mpc_inv = (
        qcd["equality_Hubble_eV"] * MPC_METERS / HBAR_C_EV_METERS
    )
    scale_factor_equality = 1.0 / (1.0 + 3400.0)
    k_over_am = k_max_mpc_inv / (scale_factor_equality * mass_mpc_inv)
    sound_speed_squared = k_over_am**2 / (4.0 + k_over_am**2)

    def fraction_for_angle(theta):
        return _evolve_to_wkb(
            theta, equality_growth, decay_constant_mpl, wkb_threshold
        )["scalar_fraction_at_equality"]

    upper_angle = 0.1
    upper_fraction = fraction_for_angle(upper_angle)
    if target_fraction > upper_fraction:
        raise ValueError(
            f"target_fraction {target_fraction} exceeds the supported small-angle "
            f"shooting range [0, {upper_angle}] rad (maximum fraction {upper_fraction})"
        )
    theta_initial = brentq(
        lambda theta: fraction_for_angle(theta) - target_fraction,
        0.0,
        upper_angle,
        xtol=1e-12,
        rtol=1e-10,
    )
    evolution = _evolve_to_wkb(
        theta_initial, equality_growth, decay_constant_mpl, wkb_threshold
    )
    return {
        "model": "homogeneous BI axion with low-energy QCD anomaly",
        "potential": "V(theta) = chi_QCD * (1 - cos(theta)); theta = a / F_phi",
        "quantum_input": (
            "QCD topological susceptibility is an externally supplied low-energy "
            "effective parameter; no instanton or quantum-loop calculation is performed."
        ),
        "target_fraction_at_equality": target_fraction,
        "camb_effective_cdm_split_example": cdm_replacement_split(
            0.0225, 0.118, target_fraction
        ),
        "qcd_scales": {
            "qcd_susceptibility_quarter_MeV": qcd[
                "qcd_susceptibility_quarter_MeV"
            ],
            "F_phi_reduced_planck": decay_constant_mpl,
            "mass_from_susceptibility_eV": qcd["mass_from_susceptibility_eV"],
            "oscillation_temperature_MeV": qcd[
                "radiation_dominated_oscillation_temperature_MeV"
            ],
            "a_equality_over_a_oscillation": equality_growth,
        },
        "linear_perturbation_regime_at_equality": {
            "assumed_redshift_equality": 3400.0,
            "k_max_mpc_inverse": k_max_mpc_inv,
            "scalar_mass_mpc_inverse": mass_mpc_inv,
            "hubble_equality_mpc_inverse": hubble_equality_mpc_inv,
            "mass_over_hubble_equality": (
                mass_mpc_inv / hubble_equality_mpc_inv
            ),
            "k_over_a_mass_at_equality": k_over_am,
            "effective_sound_speed_squared_upper_estimate": sound_speed_squared,
            "pressureless_cdm_limit_validated": (
                mass_mpc_inv / hubble_equality_mpc_inv > 1e6
                and k_over_am < 1e-3
            ),
            "implementation": (
                "CAMB evolves the scalar's matched density using its existing "
                "pressureless-CDM perturbation equations; no separate scalar "
                "perturbation hierarchy is required in this validated regime."
            ),
        },
        "evolution": evolution,
        "lcdm_comparison": {
            "scope": "homogeneous background at matter-radiation equality; not a data likelihood",
            "extra_component": (
                "If the scalar density is added on top of the reference matter and "
                "radiation, the Hubble ratio is reported in evolution."
            ),
            "matched_cold_dark_matter": (
                "After rapid oscillations, this field redshifts as matter. If its "
                "density replaces the same amount of CDM, the background Hubble "
                "history is degenerate with flat LCDM after oscillation."
            ),
            "delta_chi2": None,
            "reason_no_likelihood": (
                "The separate homogeneous solver makes no likelihood evaluation. "
                "The matched CMB model uses CAMB's pressureless-CDM perturbations "
                "only after the mass and sound-speed tests in "
                "linear_perturbation_regime_at_equality pass."
            ),
        },
        "assumptions_and_limits": [
            "The dilaton is frozen; coupled dilaton-axion evolution is not solved.",
            "The QCD potential is the leading zero-temperature cosine approximation.",
            "The field starts with zero velocity at the approximate onset H=m/3.",
            "The post-onset WKB continuation assumes small-amplitude oscillations behave as matter.",
            "The homogeneous solver contains no perturbations; the matched likelihood uses the validated pressureless-CDM limit rather than a separate scalar-fluid hierarchy.",
            "No thermal QCD susceptibility or nuisance parameters are added by this background solver.",
            "This n=1 QCD axion is not the separately fitted n=3 equality-locked Twist EDE ansatz.",
        ],
    }


def main():
    result = calculate()
    output = Path(__file__).with_name("bi_qcd_dynamics.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
