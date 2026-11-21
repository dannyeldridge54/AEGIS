"""weave_reverse — reverse-thread (dark-energy) helpers for the Weave side loop (D1850+). AI-assisted.
Units: M_P = 1 (reduced Planck mass) unless a name says GeV. Kähler moduli T = τ + iθ, K_TT̄ = K_ττ/4,
canonical saxion dφ = √(K_ττ/2) dτ.
"""
import math

ALPHA_EM = 1 / 137.036
MP_GEV = 2.435e18
H0_GEV = 1.44e-42
B_EM_MSSM = 12.0          # b_2 + (5/3) b_1 (GUT-normalised), MSSM
B_EM_SM = 11.0 / 3.0      # same combination, SM
C_EM_MSSM = 16.0          # c_a = Σ T(r) − T(G) combined the same way (5 + (5/3)(33/5))


# ---------- Kähler geometry ----------
def swiss_K(tb, tv, td):
    return -2 * math.log(tb**1.5 - tv**1.5 - td**1.5)


def tau_b_from_vol(V, tv, td):
    return (V + tv**1.5 + td**1.5) ** (2 / 3)


def dK_dphi_move_one(V, tv, td, h=1e-4):
    """δK/δφ when only τ_d moves (τ_b, τ_v held): K_d / √(K_dd/2), by central differences."""
    tb = tau_b_from_vol(V, tv, td)
    f = lambda t: swiss_K(tb, tv, t)
    Kd = (f(td + h) - f(td - h)) / (2 * h)
    Kdd = (f(td + h) - 2 * f(td) + f(td - h)) / h**2
    return Kd / math.sqrt(Kdd / 2), Kd, Kdd


def dK_dphi_single(k):
    """K = −k ln(T+T̄), one modulus moving: |δK/δφ| = √(2k)."""
    return math.sqrt(2 * k)


def G_matrix(V, tv, td, h=1e-4):
    """Field-space metric G_ij = K_ij/4 in (τ_v, τ_d) at fixed τ_b (for the kinetic-mixing estimate)."""
    tb = tau_b_from_vol(V, tv, td)
    f = lambda a, b: swiss_K(tb, a, b)
    Kvv = (f(tv + h, td) - 2 * f(tv, td) + f(tv - h, td)) / h**2
    Kdd = (f(tv, td + h) - 2 * f(tv, td) + f(tv, td - h)) / h**2
    Kvd = (f(tv + h, td + h) - f(tv + h, td - h) - f(tv - h, td + h) + f(tv - h, td - h)) / (4 * h * h)
    return Kvv / 4, Kdd / 4, Kvd / 4


# ---------- gauge-coupling leak per unit δK ----------
def dlnalpha_dK_KLZ():
    """KL + local matter metrics: d(α⁻¹)/dK = b_em/(12π) (= D400 coefficient / 3)."""
    return ALPHA_EM * B_EM_MSSM / (12 * math.pi)


def dlnalpha_dK_range():
    """Variants: KL+Z; KL+Z+soft thresholds; KL (no Z) + soft. Returns dict of |d ln α/dK|."""
    kl_z = B_EM_MSSM / (12 * math.pi)
    soft = -(B_EM_MSSM - B_EM_SM) / (4 * math.pi)
    kl_noz = C_EM_MSSM / (4 * math.pi)
    return {"KL+Z": ALPHA_EM * abs(kl_z),
            "KL+Z+soft": ALPHA_EM * abs(kl_z + soft),
            "KL(noZ)+soft": ALPHA_EM * abs(kl_noz + soft)}


def vol_needed(td, zeta_bound, coeff):
    """Swiss small cycle: |δK/δφ| ≈ √(12 τ^{3/2}/𝒱) ⇒ 𝒱 for ζ = coeff·|δK/δφ| < bound."""
    return 12 * td**1.5 * (coeff / zeta_bound) ** 2


# ---------- saxion mass for V = c σ e^{−aσ} at height ρ ----------
def saxion_mass_over_H0(a, sigma, Omega_L=0.685, geometry="single", k=3, V=None, tv=None):
    """m/H0 for V(σ) = c σ e^{−aσ} normalised to ρ = 3 H0² Ω_L at σ (M_P = 1).
    m² = (dτ/dφ)² V_ττ + (d²τ/dφ²) V_τ. geometry 'single' (K = −k ln) or 'swiss' (needs V, tv)."""
    Vt = 3 * Omega_L  # in units of H0²
    Vtau = Vt * (1 / sigma - a)
    Vtautau = Vt * (a * a - 2 * a / sigma)
    if geometry == "single":
        g = math.sqrt(k / 2) / sigma           # dφ/dτ
        dg = -math.sqrt(k / 2) / sigma**2
    else:
        h = 1e-3
        gf = lambda t: math.sqrt(abs(dK_dphi_move_one(V, tv, t)[2]) / 2)
        g = gf(sigma)
        dg = (gf(sigma + h) - gf(sigma - h)) / (2 * h)
    dtau = 1 / g
    d2tau = -dg / g**3                           # d²τ/dφ² = −g'/g³
    m2 = dtau**2 * Vtautau + d2tau * Vtau
    return math.sqrt(m2)


# ---------- plateau exponents ----------
def beta_single(n, k):
    """K = −k ln(T+T̄), correction 1/τ^n ⇒ e^{−βφ}, β = n√(2/k)."""
    return n * math.sqrt(2 / k)


def beta_fibre(m):
    """Fibre modulus at fixed 𝒱 (𝒱 = √τ1 τ2): τ1 = e^{2φ/√3}, correction τ1^{−m} ⇒ β = 2m/√3."""
    return 2 * m / math.sqrt(3)


if __name__ == "__main__":
    # self-test against closed forms
    assert abs(dK_dphi_single(3) - math.sqrt(6)) < 1e-12
    r, Kd, Kdd = dK_dphi_move_one(1e5, 20.15, 38.6)
    approx = math.sqrt(12 * 38.6**1.5 / 1e5)
    assert abs(r / approx - 1) < 0.02, (r, approx)
    # D400: d ln α/d ln x = 6.97e-3 for K = −3 ln ⇒ per unit K: /3
    assert abs(dlnalpha_dK_KLZ() * 3 - 6.97e-3) < 2e-5, dlnalpha_dK_KLZ() * 3
    # single-modulus saxion mass closed form m²/H0² = 2Ω[(aσ)² − 3aσ + 1]
    a, s, Om = 2 * math.pi, 38.6, 0.685
    closed = math.sqrt(2 * Om * ((a * s) ** 2 - 3 * a * s + 1))
    assert abs(saxion_mass_over_H0(a, s, Om) / closed - 1) < 1e-9
    assert abs(beta_single(1, 3) - math.sqrt(2 / 3)) < 1e-12 and abs(beta_fibre(0.5) - 1 / math.sqrt(3)) < 1e-12
    print("weave_reverse self-test OK")
