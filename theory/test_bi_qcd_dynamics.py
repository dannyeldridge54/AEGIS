import pytest

from theory.bi_qcd_dynamics import calculate, cdm_replacement_split


def test_dynamics_shoots_to_requested_equality_fraction():
    result = calculate(target_fraction=0.05)

    assert result["evolution"]["scalar_fraction_at_equality"] == pytest.approx(
        0.05, abs=1e-5
    )
    assert result["evolution"]["wkb_started"] is True
    assert result["evolution"]["integration_steps"] > 10
    assert result["evolution"]["theta_initial_rad"] > 0


def test_background_comparison_distinguishes_added_scalar_from_replacing_cdm():
    result = calculate(target_fraction=0.05)
    comparison = result["lcdm_comparison"]

    measured_fraction = result["evolution"]["scalar_fraction_at_equality"]
    assert result["evolution"]["H_ratio_if_added_to_LCDM"] == pytest.approx(
        (1.0 / (1.0 - measured_fraction)) ** 0.5, rel=1e-12
    )
    assert result["evolution"]["H_ratio_if_replaces_equal_CDM_density"] == 1.0
    assert comparison["delta_chi2"] is None
    assert "not a data likelihood" in comparison["scope"]


def test_qcd_field_is_in_pressureless_cdm_perturbation_regime_at_cmb_scales():
    result = calculate()
    regime = result["linear_perturbation_regime_at_equality"]

    assert regime["pressureless_cdm_limit_validated"] is True
    assert regime["mass_over_hubble_equality"] > 1e6
    assert regime["k_over_a_mass_at_equality"] < 1e-3
    assert regime["effective_sound_speed_squared_upper_estimate"] < 1e-20


def test_cdm_replacement_preserves_total_density_and_matches_target_fraction():
    split = cdm_replacement_split(0.0225, 0.118, 0.05)

    assert split["omega_biqcd_h2"] + split["omega_ordinary_cdm_h2"] == pytest.approx(
        split["omega_cdm_total_h2"]
    )
    matter = 0.0225 + 0.118
    radiation = matter
    scalar = split["omega_biqcd_h2"]
    assert scalar / (radiation + matter) == pytest.approx(0.05)
    assert split["omega_biqcd_h2"] == pytest.approx(2 * 0.05 * matter)
    assert 0.0 < split["fraction_of_total_cdm"] < 1.0


def test_wkb_matching_is_stable_to_transition_threshold():
    early_switch = calculate(target_fraction=0.05, wkb_threshold=150.0)
    late_switch = calculate(target_fraction=0.05, wkb_threshold=600.0)

    assert early_switch["evolution"]["theta_initial_rad"] == pytest.approx(
        late_switch["evolution"]["theta_initial_rad"], rel=0.01
    )
    assert late_switch["evolution"]["wkb_switch_log_a"] > early_switch[
        "evolution"
    ]["wkb_switch_log_a"]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"target_fraction": 0.0},
        {"target_fraction": 1.0},
        {"target_fraction": -0.1},
        {"wkb_threshold": 3.0},
        {"wkb_threshold": float("inf")},
    ],
)
def test_invalid_dynamics_inputs_are_rejected(kwargs):
    with pytest.raises(ValueError):
        calculate(**kwargs)


def test_qcd_cosine_is_not_mislabeled_as_torsion_ede_or_quantum_loop_result():
    result = calculate()

    assert result["model"].endswith("low-energy QCD anomaly")
    assert "no instanton or quantum-loop calculation" in result["quantum_input"]
    assert any("n=1" in item and "n=3" in item for item in result["assumptions_and_limits"])


def test_unreachable_target_reports_supported_shooting_domain(monkeypatch):
    from theory import bi_qcd_dynamics as dynamics
    monkeypatch.setattr(dynamics, "_evolve_to_wkb", lambda *args: {"scalar_fraction_at_equality": 0.1})
    with pytest.raises(ValueError, match="supported small-angle shooting range"):
        dynamics.calculate(target_fraction=0.2)


def test_replacement_fraction_cannot_exceed_available_cdm():
    with pytest.raises(ValueError, match="cannot fit"):
        cdm_replacement_split(0.0225, 0.118, 0.5)


def test_camb_exported_split_uses_replacement_not_additive_denominator():
    import ast
    from pathlib import Path
    source = Path(__file__).resolve().parents[1] / "cmb-fit" / "cmbfit_compare.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    assignment = next(node for node in ast.walk(tree)
                      if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id == "scalar_density"
                              for target in node.targets))
    expression = ast.Expression(assignment.value)
    density = eval(compile(expression, str(source), "eval"),
                   {"__builtins__": {}}, {"fraction": 0.05, "row": {"ombh2": 0.0225, "omch2": 0.118}})
    assert density == pytest.approx(cdm_replacement_split(0.0225, 0.118, 0.05)["omega_biqcd_h2"])
    assert density / (2 * (0.0225 + 0.118)) == pytest.approx(0.05)
