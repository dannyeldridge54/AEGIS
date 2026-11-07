"""Conditional weak-field scalar-force derivation for the BI Jordan-frame branch.

This derives the conformal coupling and a standard linearized Yukawa-force
response. It does not solve the AEGIS scalar profile around a star or make
Gaia-specific predictions.
"""
import math

import sympy as sp


GAMMA_BOUND = 2.3e-5
SQRT23 = math.sqrt(2 / 3)


def symbolic_derivation():
    x = sp.symbols("x", real=True)
    chi_over_mpl = sp.symbols("chi_over_Mpl", real=True)
    slope = sp.sqrt(sp.Rational(2, 3))

    # phi/M_Pl = -exp(sqrt(2/3) chi/M_Pl), Omega = 2 phi exp(2 phi/M_Pl).
    phi_over_mpl = -sp.exp(slope * x)
    omega = 2 * phi_over_mpl * sp.exp(2 * phi_over_mpl)
    ln_a = sp.simplify(sp.log(-3 / omega) / 2)
    alpha_def = sp.simplify(sp.sqrt(2) * sp.diff(ln_a, x))
    gr_point = sp.solve(sp.Eq(alpha_def, 0), x)[0]
    d_alpha = sp.simplify(sp.diff(alpha_def, x))
    d2_ln_a = sp.simplify(sp.diff(ln_a, x, 2))
    return {
        "ln_A": sp.simplify(ln_a),
        "alpha_DEF": alpha_def,
        "gr_point_chi_over_Mpl": gr_point,
        "dalpha_dchi_at_GR": sp.simplify(d_alpha.subs(x, gr_point)),
        "d2lnA_at_GR": sp.simplify(d2_ln_a.subs(x, gr_point)),
        "chi_GR_over_Mpl": sp.simplify(gr_point),
    }


def cassini_alpha_max(gamma_bound=GAMMA_BOUND):
    """Invert |gamma - 1| = 2 alpha^2 / (1 + alpha^2)."""
    if not math.isfinite(gamma_bound) or not 0 < gamma_bound < 2:
        raise ValueError("gamma_bound must be finite and between 0 and 2")
    return math.sqrt(gamma_bound / (2 - gamma_bound))


def alpha_def(chi_over_mpl):
    """DEF-normalized conformal coupling for the stated Jordan-frame map."""
    if not math.isfinite(chi_over_mpl):
        raise ValueError("chi_over_mpl must be finite")
    return (2 * math.exp(SQRT23 * chi_over_mpl) - 1) / math.sqrt(3)


def yukawa_force_ratio(alpha, mass_times_radius):
    """Return |a_scalar|/|a_tensor| for an unscreened linear scalar point-source limit.

    The formula assumes the same local coupling at source and test body. The
    effective scalar mass/range is not derived by this module.
    """
    if not math.isfinite(alpha) or not math.isfinite(mass_times_radius):
        raise ValueError("alpha and mass_times_radius must be finite")
    if mass_times_radius < 0:
        raise ValueError("mass_times_radius must be non-negative")
    return alpha * alpha * (1 + mass_times_radius) * math.exp(-mass_times_radius)


def derive():
    result = symbolic_derivation()
    alpha_max = cassini_alpha_max()
    slope = float(result["dalpha_dchi_at_GR"])
    chi_gr = float(result["chi_GR_over_Mpl"])
    return {
        "status": "conditional weak-field result; not a stellar-scale AEGIS prediction",
        "assumptions": [
            "Einstein-frame canonical scalar with conformal matter metric g_J = A(chi)^2 g_E.",
            "Reading A universal Jordan-frame matter coupling.",
            "Linearized, unscreened point-source approximation for the Yukawa force ratio.",
            "The Cassini inversion uses the preregistered massless/long-range PPN relation.",
        ],
        "symbolic": {key: str(value) for key, value in result.items()},
        "cassini": {
            "abs_gamma_minus_one_max": GAMMA_BOUND,
            "alpha_DEF_max": alpha_max,
            "chi_GR_over_Mpl": chi_gr,
            "dalpha_dchi_over_Mpl_at_GR": slope,
            "linearized_allowed_abs_delta_chi_over_Mpl": alpha_max / slope,
            "max_long_range_scalar_to_tensor_acceleration_ratio": alpha_max**2,
        },
        "yukawa_response": {
            "formula": "alpha_DEF^2 * (1 + m_eff*r) * exp(-m_eff*r)",
            "at_zero_range_parameter": yukawa_force_ratio(1.0, 0.0),
            "at_m_eff_r_1": yukawa_force_ratio(1.0, 1.0),
            "range_parameter": "m_eff*r; m_eff is not determined here",
        },
        "reading_b": {
            "direct_matter_coupling": 0.0,
            "direct_scalar_force_ratio": 0.0,
            "meaning": "zero by assumption, not a measured null result",
        },
        "not_derived": [
            "A local scalar profile and effective mass around a star or the Galaxy.",
            "Screening, boundary conditions, or environmental dependence.",
            "A six-dimensional stellar orbit, Galactic potential, or Gaia residual likelihood.",
        ],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(derive(), indent=2))
