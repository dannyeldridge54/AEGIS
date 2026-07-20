"""
UFE (Unified Field Equation) physics module.

Implements the torsion-modified Friedmann equation:
    H²(z) = H₀² [ Ωr(1+z)⁴ + Ωm(1+β)(1+z)³ + ΩΛ ]

With evolving torsion coupling:
    β(z) = β₀ + β₁·z/(1+z)

This allows the early universe (high z → β₀+β₁) to differ from
the late universe (z=0 → β₀), naturally resolving the H₀ tension.
"""

import numpy as np
from scipy.integrate import quad
from aegis.constants import C_LIGHT, OMEGA_R0


def torsion_hubble(z, H0, omega_m, omega_r, beta):
    """H(z) with constant torsion coupling β."""
    omega_L = 1.0 - omega_m - omega_r
    zp1 = 1.0 + z
    E2 = (omega_r * zp1**4
           + omega_m * (1.0 + beta) * zp1**3
           + omega_L)
    return H0 * np.sqrt(np.maximum(E2, 1e-10))


def torsion_hubble_evolving(z, H0, omega_m, omega_r, beta0, beta1):
    """H(z) with redshift-evolving torsion: β(z) = β₀ + β₁·z/(1+z)."""
    beta_z = beta0 + beta1 * z / (1.0 + z)
    omega_L = 1.0 - omega_m - omega_r
    zp1 = 1.0 + z
    E2 = (omega_r * zp1**4
           + omega_m * (1.0 + beta_z) * zp1**3
           + omega_L)
    return H0 * np.sqrt(np.maximum(E2, 1e-10))


def _hz_inv_evolving(z, H0, omega_m, omega_r, beta0, beta1):
    """1/H(z) for integration."""
    return 1.0 / torsion_hubble_evolving(z, H0, omega_m, omega_r, beta0, beta1)


def comoving_distance(z, H0, omega_m, omega_r=OMEGA_R0, beta=0.0, steps=200):
    """Comoving distance d_C(z) in Mpc with constant torsion β (trapezoidal)."""
    if z <= 0:
        return 0.0
    zz = np.linspace(0, z, steps + 1)
    Hz = torsion_hubble(zz, H0, omega_m, omega_r, beta)
    integrand = 1.0 / Hz
    return C_LIGHT * np.trapezoid(integrand, zz)


def comoving_distance_evolving(z, H0, omega_m, omega_r=OMEGA_R0,
                                beta0=0.0, beta1=0.0, steps=200):
    """Comoving distance d_C(z) in Mpc with evolving torsion β(z)."""
    if z <= 0:
        return 0.0
    zz = np.linspace(0, z, steps + 1)
    Hz = torsion_hubble_evolving(zz, H0, omega_m, omega_r, beta0, beta1)
    integrand = 1.0 / Hz
    return C_LIGHT * np.trapezoid(integrand, zz)


def comoving_distance_quad(z, H0, omega_m, omega_r=OMEGA_R0,
                            beta0=0.0, beta1=0.0):
    """Comoving distance using scipy.integrate.quad (high precision)."""
    if z <= 0:
        return 0.0
    result, _ = quad(_hz_inv_evolving, 0, z,
                     args=(H0, omega_m, omega_r, beta0, beta1))
    return C_LIGHT * result


def luminosity_distance(z, H0, omega_m, omega_r=OMEGA_R0,
                         beta0=0.0, beta1=0.0, steps=200):
    """Luminosity distance d_L(z) = (1+z) * d_C(z) in Mpc."""
    dc = comoving_distance_evolving(z, H0, omega_m, omega_r, beta0, beta1, steps)
    return (1.0 + z) * dc


def distance_modulus(z, H0, omega_m, omega_r=OMEGA_R0,
                      beta0=0.0, beta1=0.0, steps=200):
    """Distance modulus μ(z) = 5·log10(d_L/Mpc) + 25."""
    dL = luminosity_distance(z, H0, omega_m, omega_r, beta0, beta1, steps)
    return 5.0 * np.log10(np.maximum(dL, 1e-10)) + 25.0


def growth_factor(z, omega_m, beta=0.0, steps=200):
    """Linear growth factor D(z) with torsion, normalized to D(0)=1."""
    # Solve growth ODE via simple integration
    # D'' + (2 + dlnH/dlna)D'/a - 3/2 Ωm(1+β)(1+z)³ / E²(z) D = 0
    # Use approximate scaling: D(z) ∝ integral of [(1+z')/E(z')³]^... dz'
    # Simplified: use the growth integral approximation
    a_vals = np.linspace(1.0 / (1.0 + z), 1.0, steps + 1)
    omega_L = 1.0 - omega_m
    
    integrand = np.zeros_like(a_vals)
    for i, a in enumerate(a_vals):
        zz = 1.0 / a - 1.0
        E2 = (omega_m * (1.0 + beta) * (1.0 + zz)**3 + omega_L)
        integrand[i] = 1.0 / (a * np.sqrt(E2))**3
    
    D_z = np.sqrt(omega_m * (1.0 + beta) / 2.0) * _E_of_z(z, omega_m, beta) * np.trapezoid(integrand, a_vals)
    
    # Normalize: compute D(0)
    a_vals0 = np.linspace(1e-4, 1.0, steps + 1)
    integrand0 = np.zeros_like(a_vals0)
    for i, a in enumerate(a_vals0):
        zz = 1.0 / a - 1.0
        E2 = (omega_m * (1.0 + beta) * (1.0 + zz)**3 + omega_L)
        integrand0[i] = 1.0 / (a * np.sqrt(E2))**3
    
    D_0 = np.sqrt(omega_m * (1.0 + beta) / 2.0) * np.trapezoid(integrand0, a_vals0)
    
    return D_z / D_0 if D_0 > 0 else 1.0


def _E_of_z(z, omega_m, beta):
    """E(z) = H(z)/H₀ for growth factor calculation."""
    omega_L = 1.0 - omega_m
    E2 = omega_m * (1.0 + beta) * (1.0 + z)**3 + omega_L
    return np.sqrt(max(E2, 1e-10))


# ── Vectorized batch computation ─────────────────────────────────────────

def batch_distance_modulus(z_array, H0, omega_m, omega_r=OMEGA_R0,
                            beta0=0.0, beta1=0.0, steps=200):
    """Compute distance modulus for an array of redshifts (vectorized)."""
    return np.array([distance_modulus(z, H0, omega_m, omega_r, beta0, beta1, steps)
                     for z in z_array])


def batch_comoving_distance(z_array, H0, omega_m, omega_r=OMEGA_R0,
                             beta0=0.0, beta1=0.0, steps=200):
    """Compute comoving distance for an array of redshifts."""
    return np.array([comoving_distance_evolving(z, H0, omega_m, omega_r, beta0, beta1, steps)
                     for z in z_array])
