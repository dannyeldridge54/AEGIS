import json
import math

import pytest

from theory import scaling_audit as audit


@pytest.mark.parametrize("power", [1, 3])
def test_dimensionless_normalization_collapses_assumed_shape(power):
    for amplitude, decay in [(1, 1), (7, 0.2), (0.01, 5)]:
        assert audit.normalized_potential(0.3 * decay, amplitude, decay, power) == pytest.approx(
            audit.shape(0.3, power)
        )


@pytest.mark.parametrize("power", [1, 3])
def test_exponent_matches_derivative_and_small_angle_limit(power):
    assert audit.effective_exponent(1e-6, power) == pytest.approx(2 * power, rel=1e-10)
    x, step = 0.7, 1e-5
    numerical = x * (math.log(audit.shape(x + step, power))
                     - math.log(audit.shape(x - step, power))) / (2 * step)
    assert audit.effective_exponent(x, power) == pytest.approx(numerical, rel=1e-8)


def test_power_law_control_does_not_make_cosine_scale_invariant():
    result = audit.calculate()
    for row in result["rows"]:
        assert row["monomial_control_ratio"] == pytest.approx(1)
        assert row["relative_scaling_residual"] < 0
    large_angle = [row for row in result["rows"] if row["power"] == 3 and row["x"] == 1][0]
    assert abs(large_angle["relative_scaling_residual"]) > 0.5
    assert result["fractal_established"] is False
    assert result["pi_or_fibonacci_scaling_established"] is False
    assert result["quantum_to_cosmological_matching_established"] is False
    json.dumps(result, allow_nan=False)


@pytest.mark.parametrize("x,power", [(float("nan"), 1), (1, 2), (1, True)])
def test_invalid_shape_inputs(x, power):
    with pytest.raises(ValueError):
        audit.shape(x, power)


@pytest.mark.parametrize("x", [0, -1, math.pi, float("inf")])
def test_no_log_slope_at_zero_or_outside_rising_branch(x):
    with pytest.raises(ValueError):
        audit.effective_exponent(x, 3)


@pytest.mark.parametrize("power", [1, 3])
@pytest.mark.parametrize("angle", [math.nextafter(0.0, 1.0), 1e-300, 1e-100])
def test_extremely_small_angle_exponent_remains_finite(power, angle):
    assert audit.effective_exponent(angle, power) == 2 * power


@pytest.mark.parametrize("power", [1, 3])
def test_exponent_series_agrees_at_switch(power):
    below = math.nextafter(1e-4, 0.0)
    assert audit.effective_exponent(below, power) == pytest.approx(
        power * below / math.tan(below / 2), rel=1e-15
    )
