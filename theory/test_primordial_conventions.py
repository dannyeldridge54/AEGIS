import math

import numpy as np
import pytest
from scipy.integrate import quad

from theory.effective_baseline import Baseline
from theory.primordial_conventions import (
    C_LIGHT_KM_S, PowerLawSpectrum, comoving_k_over_Href, mixed_initial_state_for_zeta,
    phi0_from_zeta, zeta_from_phi0,
)

# Synthetic bookkeeping values only; they are not measured inputs.
SPECTRUM = PowerLawSpectrum(amplitude=4e-9, pivot_k_over_Href=50., tilt=.95)


def test_power_law_is_exactly_pivot_normalized_with_tilt_scaling():
    assert SPECTRUM.curvature_power(50.) == pytest.approx(4e-9, rel=1e-15)
    assert SPECTRUM.curvature_power(500.) == pytest.approx(4e-9 * 10**-.05, rel=1e-13)
    assert SPECTRUM.curvature_power(5.) == pytest.approx(4e-9 * 10**.05, rel=1e-13)
    flat = PowerLawSpectrum(4e-9, 50., 1.)
    assert flat.curvature_power(1e-3) == flat.curvature_power(1e6) == 4e-9


def test_radiation_era_potential_is_four_ninths_of_curvature_power():
    for k in (1., 50., 1e4):
        assert SPECTRUM.potential_power(k) == pytest.approx(4 / 9 * SPECTRUM.curvature_power(k), rel=1e-14)
        assert SPECTRUM.potential_rms(k)**2 == pytest.approx(SPECTRUM.potential_power(k), rel=1e-14)


def test_phi_zeta_relation_round_trips_and_is_anticorrelated():
    for zeta in (-3e-5, 1e-5, 2.5e-6):
        assert phi0_from_zeta(zeta) == pytest.approx(-2 * zeta / 3, rel=1e-15)
        assert zeta_from_phi0(phi0_from_zeta(zeta)) == pytest.approx(zeta, rel=1e-14)


def test_unit_conversion_matches_independent_arithmetic():
    assert C_LIGHT_KM_S == 299792.458
    assert comoving_k_over_Href(.05, 100.) == pytest.approx(149.896229, rel=1e-12)
    assert comoving_k_over_Href(1., C_LIGHT_KM_S) == pytest.approx(1., rel=1e-15)
    # Doubling H_ref halves the dimensionless k at fixed physical k.
    assert comoving_k_over_Href(.1, 140.) == pytest.approx(comoving_k_over_Href(.1, 70.) / 2, rel=1e-14)


@pytest.mark.parametrize("tilt", [.9, .9999999, 1., 1.0000001, 1.1])
def test_variance_matches_numerical_quadrature_and_is_continuous_at_unit_tilt(tilt):
    spectrum = PowerLawSpectrum(3e-9, 20., tilt)
    low, high = 2., 2e3
    numeric, _ = quad(lambda lnk: spectrum.curvature_power(math.exp(lnk)),
                      math.log(low), math.log(high), epsabs=0, epsrel=1e-13)
    assert spectrum.zeta_variance(low, high) == pytest.approx(numeric, rel=1e-11)
    assert PowerLawSpectrum(3e-9, 20., 1.).zeta_variance(low, high) == pytest.approx(
        3e-9 * math.log(high / low), rel=1e-15)


@pytest.mark.parametrize("args", [
    (0., 1., 1.), (-1e-9, 1., 1.), (math.nan, 1., 1.), (1e-9, 0., 1.),
    (1e-9, math.inf, 1.), (1e-9, 1., math.nan), (1e-9, 1., math.inf), (True, 1., 1.),
])
def test_spectrum_rejects_invalid_inputs(args):
    with pytest.raises(ValueError):
        PowerLawSpectrum(*args)


@pytest.mark.parametrize("k", [0., -1., math.nan, math.inf])
def test_spectrum_and_units_reject_invalid_wavenumbers(k):
    with pytest.raises(ValueError):
        SPECTRUM.curvature_power(k)
    with pytest.raises(ValueError):
        comoving_k_over_Href(k, 70.)
    with pytest.raises(ValueError):
        comoving_k_over_Href(.1, k)


def test_variance_rejects_bad_ranges_and_overflow():
    with pytest.raises(ValueError):
        SPECTRUM.zeta_variance(10., 10.)
    with pytest.raises(ValueError):
        SPECTRUM.zeta_variance(10., 1.)
    steep = PowerLawSpectrum(1., 1., 1e6)
    with pytest.raises(ValueError):
        steep.curvature_power(1e300)
    with pytest.raises(ValueError):
        steep.zeta_variance(1., 1e300)
    with pytest.raises(ValueError):
        phi0_from_zeta(math.nan)
    with pytest.raises(ValueError):
        zeta_from_phi0(math.inf)


@pytest.mark.parametrize("y,x", [(0., .005), (.002, .005), (.0099, .0099)])
def test_initial_state_has_requested_conserved_curvature_perturbation(y, x):
    zeta = -4e-5
    config = Baseline(initial_N=math.log(max(y, 1e-3)) if y else -7., initial_field=0., vacuum=0.,
                      matter_today=.9 if y else 0., radiation_today=.9)
    scale = math.exp(config.initial_N)
    k = x * math.sqrt(.9) / scale
    state = mixed_initial_state_for_zeta(config, k, zeta)
    # Independent definition: zeta=-Phi+delta_r/4 -> -3*Phi0/2 up to O(x^2).
    measured = -state[6] + state[4] / 4
    assert abs(measured / zeta - 1) < 3 * x**2
    assert state[6] == pytest.approx(-2 * zeta / 3, rel=1e-3)


def test_initial_state_rejects_zero_or_nonfinite_zeta():
    config = Baseline(initial_N=-7., initial_field=0., vacuum=0., matter_today=0., radiation_today=.9)
    for zeta in (0., math.nan):
        with pytest.raises(ValueError):
            mixed_initial_state_for_zeta(config, 1., zeta)
    with pytest.raises(ValueError):
        mixed_initial_state_for_zeta(config, 1., 1.)
