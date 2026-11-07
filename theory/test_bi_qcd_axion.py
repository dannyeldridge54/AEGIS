import math

import bi_qcd_axion
import pytest


@pytest.mark.parametrize("name", [
    "qcd_susceptibility_quarter_gev", "reduced_planck_mass_gev",
    "decay_constant_gev", "hubble_equality_ev", "equality_temperature_ev",
    "relativistic_dof_oscillation", "entropy_dof_oscillation", "entropy_dof_equality",
])
@pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf"), True, None])
def test_invalid_physical_inputs_fail_explicitly(name, value):
    with pytest.raises(ValueError, match=name):
        bi_qcd_axion.calculate(**{name: value})


@pytest.mark.parametrize("value", [0, 1, -1, float("nan"), float("inf"), True, None])
def test_invalid_target_fraction_is_rejected(value):
    with pytest.raises(ValueError, match="target_equality_fraction"):
        bi_qcd_axion.calculate(target_equality_fraction=value)


def test_qcd_susceptibility_reproduces_published_bi_axion_mass_scale():
    result = bi_qcd_axion.calculate()

    assert 2.7e-12 < result["mass_from_susceptibility_eV"] < 3.1e-12
    assert 0.8 < result["F_phi_reduced_planck"] < 0.83


def test_bi_qcd_axion_oscillates_well_before_equality():
    result = bi_qcd_axion.calculate()

    assert result["mass_over_H_equality"] > 1e15
    assert 10 < result["radiation_dominated_oscillation_temperature_MeV"] < 100
    assert result["a_equality_over_a_oscillation"] > 1e7
    assert result["post_oscillation_equation_of_state"] == 0.0


def test_small_angle_estimate_targets_total_density_at_equality():
    result = bi_qcd_axion.calculate()
    theta = result["initial_angle_for_target_total_fraction_at_equality_rad_harmonic_estimate"]
    susceptibility_fraction = result["rho_susceptibility_over_background_at_oscillation"]
    growth = result["a_equality_over_a_oscillation"]

    estimated_fraction = 0.5 * susceptibility_fraction * (theta**2 / 2) * growth
    assert estimated_fraction == pytest.approx(result["target_total_fraction_at_equality"])
    assert theta < 1e-3
    assert "not transient n=3 EDE" in result["post_oscillation_interpretation"]


def test_derived_scales_follow_decay_constant_and_susceptibility_inputs():
    baseline = bi_qcd_axion.calculate()
    doubled_decay_constant = bi_qcd_axion.calculate(decay_constant_gev=4e18)
    doubled_susceptibility_root = bi_qcd_axion.calculate(
        qcd_susceptibility_quarter_gev=2 * 75.6e-3
    )

    assert doubled_decay_constant["mass_from_susceptibility_eV"] == pytest.approx(
        baseline["mass_from_susceptibility_eV"] / 2
    )
    assert doubled_decay_constant["radiation_dominated_oscillation_temperature_MeV"] == pytest.approx(
        baseline["radiation_dominated_oscillation_temperature_MeV"] / math.sqrt(2)
    )
    assert doubled_susceptibility_root["mass_from_susceptibility_eV"] == pytest.approx(
        baseline["mass_from_susceptibility_eV"] * 4
    )
    assert doubled_susceptibility_root["radiation_dominated_oscillation_temperature_MeV"] == pytest.approx(
        baseline["radiation_dominated_oscillation_temperature_MeV"] * 2
    )


def test_target_fraction_and_entropy_inputs_propagate_consistently():
    baseline = bi_qcd_axion.calculate()
    doubled_target = bi_qcd_axion.calculate(target_equality_fraction=0.10)
    altered_entropy = bi_qcd_axion.calculate(entropy_dof_equality=3.0)

    baseline_theta = baseline[
        "initial_angle_for_target_total_fraction_at_equality_rad_harmonic_estimate"
    ]
    doubled_target_theta = doubled_target[
        "initial_angle_for_target_total_fraction_at_equality_rad_harmonic_estimate"
    ]
    altered_entropy_theta = altered_entropy[
        "initial_angle_for_target_total_fraction_at_equality_rad_harmonic_estimate"
    ]
    assert doubled_target_theta == pytest.approx(baseline_theta * math.sqrt(2))
    assert altered_entropy_theta == pytest.approx(
        baseline_theta * (3.0 / 3.91) ** (1 / 6)
    )
    assert altered_entropy["a_equality_over_a_oscillation"] == pytest.approx(
        baseline["a_equality_over_a_oscillation"] * (3.91 / 3.0) ** (1 / 3)
    )


def test_equality_temperature_hubble_and_radiation_inputs_propagate():
    baseline = bi_qcd_axion.calculate()
    doubled_hubble = bi_qcd_axion.calculate(hubble_equality_ev=5e-28)
    doubled_equality_temperature = bi_qcd_axion.calculate(equality_temperature_ev=1.6)
    doubled_planck_mass = bi_qcd_axion.calculate(reduced_planck_mass_gev=4.87e18)
    sixteenfold_radiation_dof = bi_qcd_axion.calculate(relativistic_dof_oscillation=172.0)
    eightfold_entropy_dof = bi_qcd_axion.calculate(entropy_dof_oscillation=86.0)

    assert doubled_hubble["mass_over_H_equality"] == pytest.approx(
        baseline["mass_over_H_equality"] / 2
    )
    assert doubled_equality_temperature["a_equality_over_a_oscillation"] == pytest.approx(
        baseline["a_equality_over_a_oscillation"] / 2
    )
    assert doubled_planck_mass["radiation_dominated_oscillation_temperature_MeV"] == pytest.approx(
        baseline["radiation_dominated_oscillation_temperature_MeV"] * math.sqrt(2)
    )
    assert sixteenfold_radiation_dof["radiation_dominated_oscillation_temperature_MeV"] == pytest.approx(
        baseline["radiation_dominated_oscillation_temperature_MeV"] / 2
    )
    assert eightfold_entropy_dof["a_equality_over_a_oscillation"] == pytest.approx(
        baseline["a_equality_over_a_oscillation"] * 2
    )
