import sympy as sp
import pytest

import twist_potential_audit


def test_harmonic_identity_and_periodicity():
    result = twist_potential_audit.calculate()
    assert result["harmonic_identity_residual"] == "0"
    assert result["periodicity_residual"] == "0"
    assert result["harmonic_coefficients_over_A"] == ["5/2", "-15/4", "3/2", "-1/4"]


def test_minimum_is_flat_but_sixth_order_stable():
    result = twist_potential_audit.calculate()
    assert result["minimum_curvature"] == "0"
    assert result["minimum_sixth_derivative"] == "90*A/F**6"
    assert result["hilltop_curvature"] == "-12*A/F**2"


def test_lower_harmonic_changes_the_mass():
    result = twist_potential_audit.calculate()
    assert result["leading_cosine_corrected_mass_squared"] == "A*epsilon/F**2"
    assert "does not protect" in result["naturalness"]


def test_lambda_limit_and_claim_boundaries():
    result = twist_potential_audit.calculate()
    assert result["lambda_limit_residual"] == "0"
    assert result["microscopic_derivation_established"] is False
    assert result["full_bi_stability_established"] is False
    assert result["observational_fit_performed"] is False


def test_sixth_order_behavior_and_global_lower_bound():
    theta = sp.symbols("theta", real=True)
    shape = (1 - sp.cos(theta)) ** 3
    assert sp.limit(shape / theta**6, theta, 0) == sp.Rational(1, 8)
    assert sp.trigsimp(sp.expand_trig(shape - 8 * sp.sin(theta / 2) ** 6)) == 0
    real_sine = sp.symbols("real_sine", real=True)
    assert (8 * real_sine**6).is_nonnegative is True


def test_canonical_energy_conservation_identity():
    result = twist_potential_audit.calculate()
    assert result["rho_plus_pressure"] == "q_dot**2"
    assert result["continuity_eom_identity_residual"] == "0"
    assert "kinetic energy" in result["lambda_limit_scope"]


def test_free_scalar_kinetic_energy_does_not_disappear():
    a = sp.symbols("a", positive=True)
    momentum = sp.symbols("momentum", real=True)
    velocity = momentum / a**3
    assert sp.simplify(a * sp.diff(velocity, a) + 3 * velocity) == 0
    kinetic = velocity**2 / 2
    assert sp.simplify(a * sp.diff(kinetic, a) + 6 * kinetic) == 0


def test_n3_rapid_oscillation_virial_limit_is_not_cdm():
    # For V proportional to q**p, <2K> = p<V> in the rapid-oscillation limit.
    power = sp.Integer(6)
    mean_w = (power - 2) / (power + 2)
    assert mean_w == sp.Rational(1, 2)
    assert 3 * (1 + mean_w) == sp.Rational(9, 2)
    result = twist_potential_audit.calculate()
    assert result["small_oscillation_mean_w"] == str(mean_w)
    assert "rapid oscillations" in result["oscillation_scope"]


def test_full_period_curvature_identity_and_inflection():
    result = twist_potential_audit.calculate()
    assert result["curvature_factorization_residual"] == "0"
    assert result["inflection_cosine"] == "-2/3"
    q = sp.symbols("q", real=True)
    curvature = sp.diff((1 - sp.cos(q)) ** 3, q, 2)
    assert sp.simplify(curvature.subs(q, sp.acos(-sp.Rational(2, 3)))) == 0
    assert curvature.subs(q, sp.pi) < 0
    assert curvature.subs(q, sp.pi / 2) > 0


def test_canonical_propagation_not_averaged_equation_of_state():
    result = twist_potential_audit.calculate()
    assert result["perturbation_time_kinetic_coefficient"] == "1"
    assert result["perturbation_gradient_coefficient"] == "1"
    assert result["canonical_short_wavelength_sound_speed_squared"] == "1"
    assert result["canonical_short_wavelength_sound_speed_squared"] != result["small_oscillation_mean_w"]
    assert "not averaged fluid" in result["sound_speed_scope"]
    assert result["full_bi_stability_established"] is False


def test_separate_two_field_metric_curvature_is_not_a_stability_verdict():
    result = twist_potential_audit.calculate()
    assert result["separate_two_field_ricci_scalar"] == "-lambda**2/2"
    assert result["bi_slope_ricci_scalar"] == "-4/3"
    assert "not a ghost or proof" in result["field_space_scope"]
    assert result["full_bi_stability_established"] is False


def test_two_field_connection_and_exact_conservation():
    result = twist_potential_audit.calculate()
    assert result["christoffel_chi_theta_theta"] == "-lambda*exp(chi*lambda)/2"
    assert result["christoffel_theta_chi_theta"] == "lambda/2"
    assert result["two_field_continuity_eom_identity_residual"] == "0"


def test_negative_harmonic_moves_the_true_minimum():
    study = twist_potential_audit.harmonic_sensitivity()
    row = study["rows"][0]
    assert row["minimum_stationarity_residual"] == "0"
    assert sp.sympify(row["global_minimum_excitation_over_A"]) < 0
    y = sp.sympify(row["global_minimum_one_minus_cos_theta"])
    assert 0 < y < 2
    assert study["robustness_established"] is False


def test_small_positive_correction_can_dominate_small_angle_n3():
    row = twist_potential_audit.harmonic_sensitivity()["rows"][2]
    assert row["correction_to_n3_ratio_at_angle_0_1"] > 4
    assert row["crossover_angle_radians"] > 0.1
    crossover = row["crossover_angle_radians"]
    y = 2 * sp.sin(crossover / 2)**2
    assert float(y**2) == pytest.approx(1e-4)


def test_uncorrected_shape_has_no_crossover():
    row = twist_potential_audit.harmonic_sensitivity()["rows"][1]
    assert row["crossover_angle_radians"] is None
    assert row["global_minimum_excitation_over_A"] == "0"


def test_audit_never_promotes_consistency_into_physical_confirmation():
    limits = twist_potential_audit.calculate()["claim_limits"]
    assert limits["model_classification"] == "assumed effective model"
    assert limits["microscopic_confirmation_permitted"] is False
    assert limits["full_stability_claim_permitted"] is False
    assert limits["independent_observational_confirmation_permitted"] is False
