import math

import pytest
import sympy as sp

import stellar_weak_field as weak


def test_conformal_coupling_and_gr_point_are_symbolically_consistent():
    result = weak.symbolic_derivation()
    x = sp.symbols("x", real=True)

    assert sp.simplify(result["alpha_DEF"] - (2 * sp.exp(sp.sqrt(sp.Rational(2, 3)) * x) - 1) / sp.sqrt(3)) == 0
    assert sp.simplify(result["gr_point_chi_over_Mpl"] + sp.sqrt(sp.Rational(3, 2)) * sp.log(2)) == 0
    assert float(result["dalpha_dchi_at_GR"]) == pytest.approx(0.4714045208)
    assert float(result["d2lnA_at_GR"]) == pytest.approx(1 / 3)


def test_cassini_gate_implies_a_small_conditional_long_range_force():
    result = weak.derive()["cassini"]

    assert result["alpha_DEF_max"] == pytest.approx(0.00339118449)
    assert result["linearized_allowed_abs_delta_chi_over_Mpl"] == pytest.approx(0.00719378865)
    assert result["max_long_range_scalar_to_tensor_acceleration_ratio"] == pytest.approx(1.150013e-5)
    assert weak.yukawa_force_ratio(result["alpha_DEF_max"], 0) == pytest.approx(
        result["max_long_range_scalar_to_tensor_acceleration_ratio"]
    )


def test_yukawa_force_is_suppressed_with_range_and_reading_b_is_zero():
    long_range = weak.yukawa_force_ratio(0.1, 0)
    finite_range = weak.yukawa_force_ratio(0.1, 1)

    assert finite_range < long_range
    assert weak.derive()["reading_b"]["direct_scalar_force_ratio"] == 0
    assert weak.derive()["not_derived"]


@pytest.mark.parametrize("alpha,mr", [(math.nan, 0), (0, math.inf), (0, -0.1)])
def test_yukawa_force_rejects_invalid_inputs(alpha, mr):
    with pytest.raises(ValueError):
        weak.yukawa_force_ratio(alpha, mr)
