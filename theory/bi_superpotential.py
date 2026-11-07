"""Exploratory N=1 supergravity potential for the BI superfield with constant W.

    python bi_superpotential.py   -> bi_superpotential.json

V = exp(K) (K^PhiPhibar |D_Phi W|^2 - 3 |W|^2) for
K = -3 ln(-Omega/3), Omega = exp(Phi + Phibar) (Phi + Phibar), and constant W.
Reduced Planck units. The signed logarithmic slope s = -d ln(V)/d chi is
reported only for V > 0. With the stated canonical-field orientation it is
negative on that branch. This algebraic calculation is neither a loop
calculation nor a derivation of the Spiral Twist potential.
"""
import json
from pathlib import Path

import sympy as sp


def calculate():
    P, Pb = sp.symbols("Phi Phibar")
    W = sp.symbols("W", positive=True)
    K = -3 * sp.log(-sp.exp(P + Pb) * (P + Pb) / 3)
    KP = sp.diff(K, P)
    Kinv = 1 / sp.diff(K, P, Pb)
    # For constant W, D_Phi W = K_Phi W.
    V = sp.exp(K) * (Kinv * KP * sp.diff(K, Pb) * W**2 - 3 * W**2)
    phi = sp.symbols("phi", negative=True)
    axion = sp.symbols("axion", real=True)
    complex_slice = sp.simplify(V.subs({P: phi + sp.I * axion, Pb: phi - sp.I * axion}))
    Vphi = sp.factor(sp.simplify(V.subs({P: phi, Pb: phi})))
    chi = sp.symbols("chi", real=True)
    Vchi = sp.simplify(Vphi.subs(phi, -sp.exp(sp.sqrt(sp.Rational(2, 3)) * chi)))
    signed_log_slope = sp.simplify(-sp.diff(sp.log(Vchi), chi))
    crit = sp.solve(sp.diff(Vphi, phi), phi)
    zeros = sp.solve(sp.Eq(Vphi, 0), phi)
    second_derivative = sp.diff(Vchi, chi, 2)

    critical_points = []
    for point in crit:
        canonical = sp.log(-point) / sp.sqrt(sp.Rational(2, 3))
        value = sp.simplify(Vphi.subs(phi, point) / W**2)
        curvature = sp.simplify(second_derivative.subs(chi, canonical) / W**2)
        critical_points.append({
            "phi": str(point),
            "type": "local minimum" if curvature.is_positive else "local maximum",
            "V_over_W2": float(value),
            "d2V_dchi2_over_W2": float(curvature),
        })

    samples = []
    for pv in (-0.25, -0.5, -0.9, -1.0, -1.5, -2.0, -3.0):
        canonical = sp.log(-sp.Rational(str(pv))) / sp.sqrt(sp.Rational(2, 3))
        value = sp.simplify(Vphi.subs(phi, sp.Rational(str(pv))) / W**2)
        value_float = float(value)
        sample = {
            "phi": pv,
            "chi": float(canonical),
            "V_over_W2": value_float,
            "potential_sign": "positive" if value_float > 0 else ("negative" if value_float < 0 else "zero"),
            "signed_log_slope_s": (
                float(signed_log_slope.subs(chi, canonical))
                if value_float > 0 else None
            ),
        }
        samples.append(sample)

    return {
        "V(phi)": str(Vphi),
        "constant_W_axion_force": str(sp.simplify(sp.diff(complex_slice, axion))),
        "constant_W_axion_mass_squared": str(sp.simplify(sp.diff(complex_slice, axion, 2))),
        "axion_shift_scope": "Stated K and constant W F-term sector only; no anomaly, extra multiplet, or nonperturbative sector included",
        "zeros_phi": [str(z) for z in zeros],
        "critical_phi": [str(c) for c in crit],
        "critical_points": critical_points,
        "V_at_GR_point_over_W2": float(Vphi.subs(phi, -sp.Rational(1, 2)) / W**2),
        "potential_sign_domain": "positive for phi < -1; zero at phi = -1; negative for -1 < phi < 0",
        "global_stability": "unbounded below as phi approaches 0 from below; no stable global vacuum",
        "signed_log_slope_definition": "s = -d ln(V) / d chi; reported only for V > 0",
        "slope_orientation": "s is negative on phi < -1 for chi = sqrt(3/2) ln|phi|; its magnitude alone is not a positive-s runaway criterion",
        "spiral_twist_potential_derived": False,
        "samples": samples,
    }


def main():
    output = calculate()
    path = Path(__file__).with_name("bi_superpotential.json")
    path.write_text(json.dumps(output, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=1))


if __name__ == "__main__":
    main()
