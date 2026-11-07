import pytest

import bi_kahler_lambda
import bi_superpotential
import solar_lowz


def test_kahler_geometry_gives_fixed_kinetic_coupling():
    result = bi_kahler_lambda.calculate()

    assert result["kahler_metric"] == "3/(Phi + Phibar)**2"
    assert result["metric_at_Phi=phi"] == "3/(4*phi**2)"
    assert result["lambda_exact"] == "-2 sqrt(2/3)"
    assert result["residual_check(should be 0)"] == "0"
    assert result["lambda"] == pytest.approx(-2 * (2 / 3) ** 0.5)


def test_jordan_matter_coupling_has_gr_attractor_and_cassini_band():
    result = solar_lowz.calculate()
    gr_point = result["gr_points"][0]

    assert gr_point["phi_GR"] == pytest.approx(-0.5)
    assert gr_point["d2lnA"] == pytest.approx(1 / 3)
    assert gr_point["allowed_band_dchi"] == pytest.approx(0.0071938, rel=1e-4)
    assert result["verdict_reading_A"].startswith("COUPLING-MINIMUM")
    assert "not established" in result["verdict_reading_A"]
    assert "Linearized" in gr_point["band_scope"]
    assert "extra assumption" in result["reading_B"]


def test_exact_cassini_interval_saturates_the_bound():
    from stellar_weak_field import alpha_def
    result = solar_lowz.calculate()
    lower, upper = result["gr_points"][0]["exact_cassini_interval_chi"]
    assert lower < result["gr_points"][0]["chi_GR"] < upper
    for edge, sign in [(lower, -1), (upper, 1)]:
        alpha = alpha_def(edge)
        assert alpha == pytest.approx(sign * result["cassini_alpha_max"], rel=1e-10)
        assert 2 * alpha**2 / (1 + alpha**2) == pytest.approx(2.3e-5)


def test_constant_superpotential_potential_and_stationary_points():
    result = bi_superpotential.calculate()
    critical_points = {point["phi"]: point for point in result["critical_points"]}

    assert result["zeros_phi"] == ["-1"]
    assert result["V_at_GR_point_over_W2"] == pytest.approx(-1626.92849)
    assert critical_points["-2/3"]["type"] == "local minimum"
    assert critical_points["-2/3"]["V_over_W2"] < 0
    assert critical_points["-1/2"]["type"] == "local maximum"
    assert critical_points["-1/2"]["V_over_W2"] < 0
    assert "unbounded below" in result["global_stability"]
    assert result["spiral_twist_potential_derived"] is False


def test_signed_log_slope_is_only_reported_on_positive_branch():
    result = bi_superpotential.calculate()
    samples = {sample["phi"]: sample for sample in result["samples"]}

    assert samples[-0.9]["signed_log_slope_s"] is None
    assert samples[-1.0]["signed_log_slope_s"] is None
    assert samples[-1.5]["potential_sign"] == "positive"
    assert samples[-1.5]["signed_log_slope_s"] == pytest.approx(-8.1649658)
    assert samples[-2.0]["signed_log_slope_s"] < 0


def test_constant_w_cannot_generate_an_axion_potential_in_this_sector():
    result = bi_superpotential.calculate()
    assert result["constant_W_axion_force"] == "0"
    assert result["constant_W_axion_mass_squared"] == "0"
    assert "no anomaly" in result["axion_shift_scope"]
    assert result["spiral_twist_potential_derived"] is False
