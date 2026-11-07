"""Compute the pre-registered Cassini gate for the BI dilaton matter coupling.

    python solar_lowz.py -> solar_gate.json

Reading A couples matter to the supergravity Jordan frame. Reading B sets the
coupling to zero by assumption; it is not an observational pass.
"""
import json
from pathlib import Path

import sympy as sp


def calculate():
    chi = sp.symbols("chi", real=True)
    phi = -sp.exp(sp.sqrt(sp.Rational(2, 3)) * chi)
    Omega = sp.exp(2 * phi) * 2 * phi
    ln_a = sp.Rational(1, 2) * sp.log(-3 / Omega)
    alpha = sp.simplify(sp.sqrt(2) * sp.diff(ln_a, chi))
    d2_ln_a = sp.simplify(sp.diff(ln_a, chi, 2))

    gr_points = sp.solve(sp.Eq(alpha, 0), chi)
    cassini = 2.3e-5
    alpha_max = (cassini / (2 - cassini)) ** 0.5
    rows = []
    for point in gr_points:
        point_float = float(point)
        curvature = float(d2_ln_a.subs(chi, point))
        slope = float(sp.diff(alpha, chi).subs(chi, point))
        band = alpha_max / abs(slope)
        alpha_edges = [
            float(alpha.subs(chi, point_float - band)),
            float(alpha.subs(chi, point_float + band)),
        ]
        rows.append({
            "chi_GR": point_float,
            "phi_GR": float(phi.subs(chi, point)),
            "d2lnA": curvature,
            "dalpha_dchi": slope,
            "allowed_band_dchi": band,
            "alpha_at_band_edges": alpha_edges,
            "band_scope": "Linearized estimate only; not an exact Cassini acceptance interval.",
            "exact_cassini_interval_chi": [
                float(sp.sqrt(sp.Rational(3, 2)) * sp.log((1 - sp.sqrt(3) * alpha_max) / 2)),
                float(sp.sqrt(sp.Rational(3, 2)) * sp.log((1 + sp.sqrt(3) * alpha_max) / 2)),
            ],
        })

    if not gr_points:
        verdict = "EXCLUDED"
    else:
        row = rows[0]
        if row["d2lnA"] > 0:
            verdict = "COUPLING-MINIMUM (dynamical attraction and local Cassini compliance not established)"
        elif row["allowed_band_dchi"] < 0.01:
            verdict = "FINE-TUNED"
        else:
            verdict = "UNCLASSIFIED (band >= 0.01 and not an attractor; rule has no category)"

    return {
        "alpha(chi)": str(alpha),
        "d2lnA(chi)": str(d2_ln_a),
        "cassini_alpha_max": alpha_max,
        "gr_points": rows,
        "far_from_GR_example": {
            "chi=0": float(alpha.subs(chi, 0)),
            "chi=-2": float(alpha.subs(chi, -2)),
        },
        "verdict_reading_A": verdict,
        "reading_B": "matter on the Einstein frame: alpha = 0 by construction (extra assumption, not a pass)",
    }


def main():
    output = calculate()
    path = Path(__file__).with_name("solar_gate.json")
    path.write_text(json.dumps(output, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=1))


if __name__ == "__main__":
    main()
