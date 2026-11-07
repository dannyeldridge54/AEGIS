import math

import numpy as np
import pytest

from theory import neutrino_hierarchy as nh


def analytic_potential(x, psi0):
    y = x / math.sqrt(3)
    return 3 * psi0 * (math.sin(y) - y * math.cos(y)) / y**3


def test_zero_neutrino_limit_matches_analytic_radiation_potential():
    psi0 = 1e-5
    state = nh.initial_state(0.0, 0.005, 40, primordial_psi=psi0)
    solution = nh.integrate(0.0, 40, state, 0.005, 15.0)
    for x in (.5, 3., 8., 15.):
        assert solution.sol(x)[-1] == pytest.approx(analytic_potential(x, psi0), rel=1e-6)
    # no neutrino shear source: phi=psi, and the photon/neutrino densities agree early
    assert state[0] == pytest.approx(state[2])


@pytest.mark.parametrize("fraction", [0.0, 0.2, 0.4052, 0.68])
def test_initial_00_residual_scales_as_x0_to_the_fourth(fraction):
    residual = {}
    for x0 in (.01, .005):
        state = nh.initial_state(fraction, x0, 12, primordial_psi=1e-3)
        residual[x0] = abs(nh.equations(fraction, 12, x0, state)[1])
    assert residual[.01] < 1e-7 * 1e-3
    assert 12 < residual[.01] / residual[.005] < 20


def test_wrong_initial_density_is_detected_by_independent_constraint():
    state = nh.initial_state(.4, .005, 12, primordial_psi=1e-3)
    bad = state.copy()
    bad[0] += 1e-3
    bad[2] += 1e-3
    assert abs(nh.equations(.4, 12, .005, bad)[1]) > 1e-3
    assert abs(nh.equations(.4, 12, .005, state)[1]) < 1e-9


@pytest.mark.parametrize("fraction", [0.0, 0.4052, 0.68])
def test_potentials_and_traceless_equation(fraction):
    x0 = .005
    state = nh.initial_state(fraction, x0, 12, primordial_psi=1e-3)
    phi, f2 = state[-1], state[4]
    psi = phi - 3 * fraction * f2 / x0**2
    assert psi == pytest.approx(1e-3, rel=2e-5)
    assert phi / psi == pytest.approx(1 + 2 * fraction / 5, rel=2e-5)


def test_validate_gate_and_integrated_constraint_with_neutrinos():
    result = nh.validate(.4052, 40, .005, 15.)
    assert result["numerical_gate_passed"]
    assert result["max_truncation_shift_over_psi"] < 1e-6
    assert result["max_scaled_00_residual"] < 1e-6 * 1e-5
    assert result["lmax"] == 40
    assert result["primordial_initialization_established"] is False
    assert result["full_stability_established"] is False
    assert result["scientific_baseline_ready"] is False
    assert result["missing"]


def test_truncation_matters_without_enough_multipoles():
    fraction = .4052
    short = nh.integrate(fraction, 8, nh.initial_state(fraction, .005, 8), .005, 4.)
    long = nh.integrate(fraction, 80, nh.initial_state(fraction, .005, 80), .005, 4.)
    long_value = long.sol(4.)[-1]
    short_value = short.sol(4.)[-1]
    assert abs(short_value - long_value) / abs(long_value) < 1e-3
    assert abs(nh.integrate(fraction, 16, nh.initial_state(fraction, .005, 16), .005, 4.)
               .sol(4.)[-1] - long_value) < abs(short_value - long_value) + 1e-15


def test_start_epoch_independence():
    fraction = .4052
    values = []
    for x0 in (.002, .01):
        state = nh.initial_state(fraction, x0, 30, primordial_psi=1e-5)
        values.append(nh.integrate(fraction, 30, state, x0, 6.).sol(6.)[:5])
    assert np.max(np.abs(values[0] - values[1])) / 1e-5 < 1e-5


def test_neutrino_shear_changes_the_trajectory():
    base = nh.integrate(0., 30, nh.initial_state(0., .005, 30), .005, 10.).sol(10.)[-1]
    shear = nh.integrate(.68, 30, nh.initial_state(.68, .005, 30), .005, 10.).sol(10.)[-1]
    assert abs(shear - base) / abs(base) > .05


def test_equations_match_numerical_derivative_of_solution():
    fraction, lmax = .4052, 20
    solution = nh.integrate(fraction, lmax, nh.initial_state(fraction, .005, lmax), .005, 8.)
    h = 1e-4
    for x in (.3, 2., 6.):
        numeric = (solution.sol(x - 2 * h) - 8 * solution.sol(x - h)
                   + 8 * solution.sol(x + h) - solution.sol(x + 2 * h)) / (12 * h)
        analytic = nh.equations(fraction, lmax, x, solution.sol(x))[0]
        scale = np.maximum(1e-5, np.abs(analytic))
        assert np.max(np.abs(numeric - analytic) / scale) < 1e-5


@pytest.mark.parametrize("call", [
    lambda: nh.initial_state(1.0, .005, 12),
    lambda: nh.initial_state(-.1, .005, 12),
    lambda: nh.initial_state(float("nan"), .005, 12),
    lambda: nh.initial_state(True, .005, 12),
    lambda: nh.initial_state(.4, .02, 12),
    lambda: nh.initial_state(.4, 0., 12),
    lambda: nh.initial_state(.4, .005, 3),
    lambda: nh.initial_state(.4, .005, 12.0),
    lambda: nh.initial_state(.4, .005, 500),
    lambda: nh.initial_state(.4, .005, 12, primordial_psi=0.),
    lambda: nh.integrate(.4, 12, nh.initial_state(.4, .005, 12), .005, 7.),
    lambda: nh.integrate(.4, 12, nh.initial_state(.4, .005, 12), .005, .004),
    lambda: nh.integrate(.4, 12, nh.initial_state(.4, .005, 12), .005, 3., method="LSODA"),
    lambda: nh.equations(.4, 12, .005, np.zeros(5)),
    lambda: nh.equations(.4, 12, -1., nh.initial_state(.4, .005, 12)),
    lambda: nh.equations(.4, 12, .005, np.full(16, np.nan)),
])
def test_unsupported_inputs_are_rejected(call):
    with pytest.raises(ValueError):
        call()
