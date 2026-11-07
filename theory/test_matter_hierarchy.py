import math

import numpy as np
import pytest

from theory import matter_hierarchy as mh
from theory import neutrino_hierarchy as nh


def kodama_sasaki_ratio(y):
    return (16 * math.sqrt(1 + y) + 9 * y**3 + 2 * y**2 - 8 * y - 16) / (10 * y**3)


def run_superhorizon(fraction, x_final, kt1=1e-3, x0=1e-6, lmax=8):
    state = mh.initial_state(fraction, kt1, x0, lmax, primordial_psi=1e-5)
    return state, mh.integrate(fraction, lmax, kt1, state, x0, x_final, rtol=1e-12, atol=1e-22)


def test_zero_neutrino_superhorizon_potential_matches_kodama_sasaki():
    _, solution = run_superhorizon(0.0, .005)
    for x in (4e-4, 1e-3, 3e-3, 5e-3):
        s = x / 1e-3
        y = s * s + 2 * s
        assert solution.sol(x)[-1] / 1e-5 == pytest.approx(kodama_sasaki_ratio(y), rel=3e-5)


@pytest.mark.parametrize("fraction", [0.0, 0.4052, 0.68])
def test_curvature_perturbation_conserved_through_equality(fraction):
    state, solution = run_superhorizon(fraction, .02)
    zeta0 = mh.curvature_perturbation(fraction, 8, 1e-3, 1e-6, state)
    if fraction == 0:
        assert zeta0 == pytest.approx(-1.5e-5, rel=1e-5)
    for x in (1e-4, 1e-3, .02):
        zeta = mh.curvature_perturbation(fraction, 8, 1e-3, x, solution.sol(x))
        assert zeta / zeta0 == pytest.approx(1, abs=5e-5)


def test_zero_neutrino_matter_era_potential_is_nine_tenths_of_radiation_value():
    _, solution = run_superhorizon(0.0, .02)
    assert solution.sol(.02)[-1] / 1e-5 == pytest.approx(0.9, abs=1e-3)


@pytest.mark.parametrize("fraction", [0.0, 0.4052, 0.68])
@pytest.mark.parametrize("kt1", [3., 100., 1000.])
def test_initial_00_residual_scales_as_x0_to_the_fourth(fraction, kt1):
    residual = {}
    for x0 in (.01, .005):
        state = mh.initial_state(fraction, kt1, x0, 12, primordial_psi=1e-3)
        residual[x0] = abs(mh.equations(fraction, 12, kt1, x0, state)[1])
    assert residual[.01] < 1e-9 * 1e-3 * 1e3
    assert 14 < residual[.01] / residual[.005] < 18


def test_radiation_limit_reduces_to_neutrino_hierarchy():
    fraction, lmax = .4052, 20
    start = mh.initial_state(fraction, 1e9, .005, lmax, primordial_psi=1e-5)
    reference = nh.initial_state(fraction, .005, lmax, primordial_psi=1e-5)
    assert np.max(np.abs(start[:4 + lmax - 1] - reference[:4 + lmax - 1])) < 1e-12 * 1e-5 * 1e3
    assert start[-1] == pytest.approx(reference[-1], rel=1e-10)
    matter = mh.integrate(fraction, lmax, 1e9, start, .005, 6.)
    radiation = nh.integrate(fraction, lmax, nh.initial_state(fraction, .005, lmax,
                                                              primordial_psi=1e-5), .005, 6.)
    for x in (1., 3., 6.):
        assert matter.sol(x)[-1] == pytest.approx(radiation.sol(x)[-1], rel=1e-6)


def test_wrong_series_is_detected_by_independent_constraint():
    kt1 = 3.
    state = mh.initial_state(.4, kt1, .005, 12, primordial_psi=1e-3)
    good = abs(mh.equations(.4, 12, kt1, .005, state)[1])
    no_matter_correction = mh.initial_state(.4, 1e9, .005, 12, primordial_psi=1e-3)
    assert abs(mh.equations(.4, 12, kt1, .005, no_matter_correction)[1]) > 1e3 * good
    bad = state.copy()
    bad[12 + 3] += 1e-3  # delta_c
    assert abs(mh.equations(.4, 12, kt1, .005, bad)[1]) > 1e6 * good


def test_spatial_trace_einstein_equation_is_an_independent_check():
    fraction, lmax, kt1, x0 = .4052, 24, 2., .01
    start = mh.initial_state(fraction, kt1, x0, lmax, primordial_psi=1e-5)
    solution = mh.integrate(fraction, lmax, kt1, start, x0, 6., rtol=1e-12, atol=1e-20)
    h = 1e-4

    def psi(x):
        return mh.potentials(fraction, lmax, kt1, x, solution.sol(x))[0]

    def dphi(x):
        return mh.equations(fraction, lmax, kt1, x, solution.sol(x))[0][lmax + 5]

    for x in (.5, 2., 6.):
        hub = mh.background(kt1, x)[0]
        hub_prime = (mh.background(kt1, x + h)[0] - mh.background(kt1, x - h)[0]) / (2 * h)
        state = solution.sol(x)
        psi_value, phi_value = mh.potentials(fraction, lmax, kt1, x, state)
        lhs = ((dphi(x + h) - dphi(x - h)) / (2 * h)
               + hub * ((psi(x + h) - psi(x - h)) / (2 * h) + 2 * dphi(x))
               + (2 * hub_prime + hub**2) * psi_value + (phi_value - psi_value) / 3)
        pressure = mh.background(kt1, x)[1] * ((1 - fraction) * state[0] + fraction * state[2]) / 3
        assert lhs == pytest.approx(pressure / 2, rel=1e-5)


def test_validate_gate_and_integrated_constraint_with_matter():
    result = mh.validate(.4052, 40, 2., .005, 15.)
    assert result["numerical_gate_passed"]
    assert result["max_truncation_shift_over_psi"] < 1e-6
    assert result["max_start_epoch_shift_over_psi"] < 1e-5
    assert result["max_scaled_00_residual"] < 1e-5 * 1e-5
    assert result["primordial_initialization_established"] is False
    assert result["full_stability_established"] is False
    assert result["scientific_baseline_ready"] is False
    assert result["missing"]


def test_equations_match_numerical_derivative_of_solution():
    fraction, lmax, kt1 = .4052, 20, 2.
    solution = mh.integrate(fraction, lmax, kt1, mh.initial_state(fraction, kt1, .005, lmax),
                            .005, 8.)
    h = 1e-4
    for x in (.3, 2., 6.):
        numeric = (solution.sol(x - 2 * h) - 8 * solution.sol(x - h)
                   + 8 * solution.sol(x + h) - solution.sol(x + 2 * h)) / (12 * h)
        analytic = mh.equations(fraction, lmax, kt1, x, solution.sol(x))[0]
        scale = np.maximum(1e-5, np.abs(analytic))
        assert np.max(np.abs(numeric - analytic) / scale) < 1e-5


def test_background_satisfies_friedmann_and_acceleration_equations():
    kt1 = 2.
    for x in (.01, .5, 3.):
        hub, rho_r, rho_m = mh.background(kt1, x)
        assert hub**2 == pytest.approx((rho_r + rho_m) / 3, rel=1e-12)
        h = 1e-4 * x
        hub_prime = (mh.background(kt1, x + h)[0] - mh.background(kt1, x - h)[0]) / (2 * h)
        # calH' = -(a^2/6)(rho+3P)
        assert hub_prime == pytest.approx(-(2 * rho_r + rho_m) / 6, rel=1e-6)


@pytest.mark.parametrize("call", [
    lambda: mh.initial_state(1.0, 3., .005, 12),
    lambda: mh.initial_state(.4, 0., .005, 12),
    lambda: mh.initial_state(.4, -1., .005, 12),
    lambda: mh.initial_state(.4, float("inf"), .005, 12),
    lambda: mh.initial_state(.4, True, .005, 12),
    lambda: mh.initial_state(.4, .1, .005, 12),
    lambda: mh.initial_state(.4, 3., .02, 12),
    lambda: mh.initial_state(.4, 3., .005, 3),
    lambda: mh.initial_state(.4, 3., .005, 12, primordial_psi=0.),
    lambda: mh.integrate(.4, 12, 3., mh.initial_state(.4, 3., .005, 12), .005, 7.),
    lambda: mh.integrate(.4, 12, 3., mh.initial_state(.4, 3., .005, 12), .005, 3.,
                         method="LSODA"),
    lambda: mh.equations(.4, 12, 3., .005, np.zeros(5)),
    lambda: mh.equations(.4, 12, 3., -1., mh.initial_state(.4, 3., .005, 12)),
    lambda: mh.equations(.4, 12, 3., .005, np.full(18, np.nan)),
])
def test_unsupported_inputs_are_rejected(call):
    with pytest.raises(ValueError):
        call()


FB = 0.157


def test_zero_baryon_fraction_is_bitwise_default():
    for kt1 in (3., 100.):
        base = mh.initial_state(.4052, kt1, .005, 12)
        assert np.array_equal(base, mh.initial_state(.4052, kt1, .005, 12, baryon_fraction=0.))
        assert np.array_equal(
            mh.equations(.4052, 12, kt1, .3, base)[0],
            mh.equations(.4052, 12, kt1, .3, base, baryon_fraction=0.)[0])


@pytest.mark.parametrize("fraction", [0.0, 0.4052])
def test_baryon_loading_changes_only_the_photon_baryon_velocity_at_x4(fraction):
    kt1, x0, psi0 = 3., .005, 1e-3
    base = mh.initial_state(fraction, kt1, x0, 12, primordial_psi=psi0)
    loaded = mh.initial_state(fraction, kt1, x0, 12, primordial_psi=psi0, baryon_fraction=FB)
    diff = loaded - base
    expected = (psi0 * (1 / kt1) * (3 * FB / (4 * (1 - fraction))) * (4 * fraction + 15) / 180
                * x0**4)
    assert diff[1] == pytest.approx(expected, rel=1e-12)
    assert np.count_nonzero(np.delete(diff, 1)) == 0


@pytest.mark.parametrize("fraction", [0.0, 0.4052])
@pytest.mark.parametrize("kt1", [3., 100., 1000.])
def test_baryon_initial_00_residual_scales_as_x0_to_the_fourth(fraction, kt1):
    residual = {}
    for x0 in (.01, .005):
        state = mh.initial_state(fraction, kt1, x0, 12, primordial_psi=1e-3, baryon_fraction=FB)
        residual[x0] = abs(mh.equations(fraction, 12, kt1, x0, state, baryon_fraction=FB)[1])
    assert residual[.01] < 1e-9
    assert 14 < residual[.01] / residual[.005] < 18


def test_omitting_the_baryon_velocity_term_worsens_start_epoch_agreement():
    fraction, lmax, kt1, fb = .4052, 12, 3., .5
    x0, x_final, psi0 = .01, .3, 1e-3

    def shift(drop):
        outputs = []
        for start_x in (x0, x0 / 2):
            state = mh.initial_state(fraction, kt1, start_x, lmax, primordial_psi=psi0,
                                     baryon_fraction=fb)
            if drop:
                state[1] -= (psi0 / kt1 * 3 * fb / (4 * (1 - fraction)) * (4 * fraction + 15)
                             / 180 * start_x**4)
            sol = mh.integrate(fraction, lmax, kt1, state, start_x, x_final, rtol=1e-12,
                               atol=1e-22, baryon_fraction=fb)
            outputs.append(sol.sol(x_final)[1])
        return abs(outputs[0] - outputs[1])

    assert shift(True) > 5 * shift(False)


def test_baryon_spatial_trace_einstein_equation_is_an_independent_check():
    fraction, lmax, kt1, x0 = .4052, 24, 2., .01
    start = mh.initial_state(fraction, kt1, x0, lmax, primordial_psi=1e-5, baryon_fraction=FB)
    solution = mh.integrate(fraction, lmax, kt1, start, x0, 6., rtol=1e-12, atol=1e-20,
                            baryon_fraction=FB)
    h = 1e-4

    def psi(x):
        return mh.potentials(fraction, lmax, kt1, x, solution.sol(x))[0]

    def dphi(x):
        return mh.equations(fraction, lmax, kt1, x, solution.sol(x),
                            baryon_fraction=FB)[0][lmax + 5]

    for x in (.5, 2., 6.):
        hub = mh.background(kt1, x)[0]
        hub_prime = (mh.background(kt1, x + h)[0] - mh.background(kt1, x - h)[0]) / (2 * h)
        state = solution.sol(x)
        psi_value, phi_value = mh.potentials(fraction, lmax, kt1, x, state)
        lhs = ((dphi(x + h) - dphi(x - h)) / (2 * h)
               + hub * ((psi(x + h) - psi(x - h)) / (2 * h) + 2 * dphi(x))
               + (2 * hub_prime + hub**2) * psi_value + (phi_value - psi_value) / 3)
        pressure = mh.background(kt1, x)[1] * ((1 - fraction) * state[0] + fraction * state[2]) / 3
        assert lhs == pytest.approx(pressure / 2, rel=1e-5)


def test_baryon_curvature_conserved_and_00_constraint_holds_through_equality():
    fraction, lmax, kt1, x0 = .4052, 8, 1e-3, 1e-6
    start = mh.initial_state(fraction, kt1, x0, lmax, primordial_psi=1e-5, baryon_fraction=FB)
    solution = mh.integrate(fraction, lmax, kt1, start, x0, .02, rtol=1e-12, atol=1e-22,
                            baryon_fraction=FB)
    zeta0 = mh.curvature_perturbation(fraction, lmax, kt1, x0, start, baryon_fraction=FB)
    for x in (1e-4, 1e-3, .02):
        state = solution.sol(x)
        zeta = mh.curvature_perturbation(fraction, lmax, kt1, x, state, baryon_fraction=FB)
        assert zeta / zeta0 == pytest.approx(1, abs=5e-5)
        assert abs(mh.equations(fraction, lmax, kt1, x, state, baryon_fraction=FB)[1]) < 1e-9


def test_baryon_validate_gate_and_scope_flags():
    result = mh.validate(.4052, 40, 2., .005, 15., baryon_fraction=FB)
    assert result["numerical_gate_passed"]
    assert result["baryon_fraction"] == FB
    assert result["scientific_baseline_ready"] is False
    assert result["primordial_initialization_established"] is False
    assert any("finite-opacity" in item for item in result["missing"])


@pytest.mark.parametrize("bad", [-.1, 1., 1.5, float("nan"), float("inf"), True])
def test_invalid_baryon_fraction_is_rejected(bad):
    state = mh.initial_state(.4, 3., .005, 12)
    with pytest.raises(ValueError):
        mh.initial_state(.4, 3., .005, 12, baryon_fraction=bad)
    with pytest.raises(ValueError):
        mh.equations(.4, 12, 3., .1, state, baryon_fraction=bad)
    with pytest.raises(ValueError):
        mh.integrate(.4, 12, 3., state, .005, 1., baryon_fraction=bad)