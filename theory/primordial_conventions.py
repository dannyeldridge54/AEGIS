"""Explicit primordial amplitude, pivot, tilt and unit conventions (no data).

Supplies dimensionless bookkeeping for the supported radiation/dust adiabatic
initializers in ``coupled_perturbations``. Amplitude, pivot, tilt and the
reference Hubble rate are caller inputs; no measured value is built in and no
observational result is implied. See DERIVATION_CHAIN.md section 11.
"""
from dataclasses import dataclass
import math

from theory.coupled_perturbations import mixed_adiabatic_initial_state

C_LIGHT_KM_S = 299792.458  # exact by SI definition

# Phi0 = -2*zeta/3, with zeta = -Phi + delta_r/4 -> -3*Phi0/2 (section 9).
PHI0_OVER_ZETA = -2.0 / 3.0


def _finite_positive(name, value):
    if not isinstance(value, (int, float)) or isinstance(value, bool) \
            or not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return float(value)


def comoving_k_over_Href(k_per_Mpc, hubble_ref_km_s_Mpc):
    """Dimensionless comoving k/H_ref for a_today=1: k[1/Mpc]*c/H_ref."""
    k = _finite_positive("Comoving wavenumber k [1/Mpc]", k_per_Mpc)
    h_ref = _finite_positive("Reference Hubble rate [km/s/Mpc]", hubble_ref_km_s_Mpc)
    value = k * C_LIGHT_KM_S / h_ref
    if not math.isfinite(value) or value <= 0:
        raise ValueError("Dimensionless wavenumber is not numerically resolved")
    return value


def phi0_from_zeta(zeta):
    """Signed asymptotic radiation-era potential for a signed conserved zeta."""
    if not isinstance(zeta, (int, float)) or isinstance(zeta, bool) or not math.isfinite(zeta):
        raise ValueError("zeta must be finite")
    return PHI0_OVER_ZETA * float(zeta)


def zeta_from_phi0(phi0):
    """Inverse of phi0_from_zeta."""
    if not isinstance(phi0, (int, float)) or isinstance(phi0, bool) or not math.isfinite(phi0):
        raise ValueError("Phi0 must be finite")
    return float(phi0) / PHI0_OVER_ZETA


@dataclass(frozen=True)
class PowerLawSpectrum:
    """Delta2_zeta(k)=amplitude*(k/pivot)^(tilt-1), pivot in comoving k/H_ref.

    Delta2 = k^3 P/(2 pi^2) with <zeta_k zeta*_k'> = (2 pi)^3 delta^3(k-k') P.
    Adiabatic only: scalar isocurvature is zero by construction, so there is
    no adiabatic/isocurvature cross-correlation, and Phi0 is perfectly
    (anti)correlated with zeta. Running and tensors are not represented.
    """
    amplitude: float
    pivot_k_over_Href: float
    tilt: float

    def __post_init__(self):
        _finite_positive("Amplitude", self.amplitude)
        _finite_positive("Pivot k/H_ref", self.pivot_k_over_Href)
        if not isinstance(self.tilt, (int, float)) or isinstance(self.tilt, bool) \
                or not math.isfinite(self.tilt):
            raise ValueError("Tilt must be finite")

    def _log_ratio(self, k_over_Href):
        k = _finite_positive("k/H_ref", k_over_Href)
        return math.log(k / self.pivot_k_over_Href)

    def curvature_power(self, k_over_Href):
        """Dimensionless Delta2_zeta(k)."""
        try:
            value = self.amplitude * math.exp((self.tilt - 1) * self._log_ratio(k_over_Href))
        except OverflowError as error:
            raise ValueError("Primordial power overflowed") from error
        if not math.isfinite(value):
            raise ValueError("Primordial power is not finite")
        return value

    def potential_power(self, k_over_Href):
        """Delta2 of the asymptotic radiation-era potential: (4/9)*Delta2_zeta."""
        return PHI0_OVER_ZETA**2 * self.curvature_power(k_over_Href)

    def potential_rms(self, k_over_Href):
        """Root-mean-square Phi0 per logarithmic interval in k."""
        return math.sqrt(self.potential_power(k_over_Href))

    def zeta_variance(self, k_low, k_high):
        """Integral of Delta2_zeta d ln k over [k_low, k_high] (k/H_ref)."""
        low, high = (_finite_positive("k_low", k_low), _finite_positive("k_high", k_high))
        if high <= low:
            raise ValueError("k_high must exceed k_low")
        span = math.log(high / low)
        epsilon = self.tilt - 1
        try:
            if epsilon == 0:
                value = self.amplitude * span
            else:
                value = (self.amplitude * math.exp(epsilon * self._log_ratio(low))
                         * math.expm1(epsilon * span) / epsilon)
        except OverflowError as error:
            raise ValueError("Primordial variance overflowed") from error
        if not math.isfinite(value):
            raise ValueError("Primordial variance is not finite")
        return value


def mixed_initial_state_for_zeta(config, k_over_Href, zeta):
    """Mixed radiation/dust adiabatic state for one signed conserved zeta."""
    return mixed_adiabatic_initial_state(
        config, k_over_Href, primordial_phi=phi0_from_zeta(zeta))
