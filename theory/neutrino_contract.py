"""Leading-order superhorizon radiation-era contract with free-streaming neutrinos.

Conformal Newtonian gauge, ds^2=a^2[-(1+2psi)dtau^2+(1-2phi)dx^2], reduced
Planck units (8 pi G=1), pure radiation (photons + massless neutrinos) with
Rnu=rho_nu/(rho_gamma+rho_nu) and calH=1/tau. Shear convention:
(rho+P)sigma = -(k_i k_j - delta_ij k^2/3) Sigma^ij_j with the traceless
Einstein equation k^2(phi-psi)=(3/2)a^2 sum(rho+P)sigma.

This only states the gauge/source/initial-condition contract; it is not a
Boltzmann hierarchy, not an evolution and not a primordial spectrum. See
DERIVATION_CHAIN.md section 13 for the derivation and domain.
"""
import math


def neutrino_radiation_adiabatic_contract(neutrino_fraction, k_tau, *, primordial_psi=1e-5):
    """Leading (x^0 for potentials/densities, x^1/x^2 for velocity/shear) mode.

    k_tau=k/calH=k*tau must satisfy 0 < k_tau <= .01. primordial_psi is the
    time-time potential; neutrino_fraction must lie in [0, 1).
    Returns dimensionless quantities with velocities as theta/calH.
    Terms of relative order k_tau^2 are neglected.
    """
    for value in (neutrino_fraction, k_tau, primordial_psi):
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError("Neutrino contract inputs must be finite numbers")
    if not 0 <= neutrino_fraction < 1:
        raise ValueError("Neutrino fraction must lie in [0, 1)")
    if not 0 < k_tau <= .01:
        raise ValueError("Neutrino contract requires superhorizon 0 < k*tau <= .01")
    if not 0 < abs(primordial_psi) <= 1e-3:
        raise ValueError("Neutrino contract potential must be nonzero and within 1e-3")
    psi = float(primordial_psi)
    rnu = float(neutrino_fraction)
    k2 = k_tau * k_tau
    radiation_density = -2 * psi
    return {
        "psi": psi,
        "phi": (1 + 2 * rnu / 5) * psi,
        "delta_gamma": radiation_density,
        "delta_nu": radiation_density,
        "delta_matter": 0.75 * radiation_density,
        "theta_over_calH": k2 * psi / 2,
        "sigma_nu": k2 * psi / 15,
        "neutrino_fraction": rnu,
        "k_tau": float(k_tau),
        "scope": "leading-order radiation era; photon/neutrino hierarchy not evolved",
    }
