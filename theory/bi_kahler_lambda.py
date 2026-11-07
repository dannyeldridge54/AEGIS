"""Derive the BI-superfield Kähler metric and axion kinetic coupling.

    python bi_kahler_lambda.py -> bi_kahler_lambda.json

The Kähler potential is quoted from Gates, Ketov & Yunes (2009), eqs. 5.36–5.37.
This derives the field-space geometry, not the Spiral Twist potential.
"""
import json
from pathlib import Path

import sympy as sp


def calculate():
    P, Pb = sp.symbols("Phi Phibar")
    Omega = sp.exp(P + Pb) * (P + Pb)
    K = -3 * sp.log(-Omega / 3)
    metric = sp.simplify(sp.diff(K, P, Pb))

    phi = sp.symbols("phi", negative=True)
    metric_phi = sp.simplify(metric.subs({P: phi, Pb: phi}))
    lam = -2 * sp.sqrt(sp.Rational(2, 3))
    chi = sp.symbols("chi", real=True)
    metric_chi = sp.simplify(
        metric.subs({
            P: -sp.exp(sp.sqrt(sp.Rational(2, 3)) * chi),
            Pb: -sp.exp(sp.sqrt(sp.Rational(2, 3)) * chi),
        })
    )
    residual = sp.simplify(
        metric_chi - sp.Rational(3, 4) * sp.exp(lam * chi)
    )

    return {
        "kahler_metric": str(metric),
        "metric_at_Phi=phi": str(metric_phi),
        "canonical_dilaton": "chi = sqrt(3/2) ln|phi|",
        "axion_factor": "f(chi) = exp(lambda chi), after rescaling a_canonical = sqrt(3/2) a",
        "lambda": float(lam),
        "lambda_exact": "-2 sqrt(2/3)",
        "residual_check(should be 0)": str(residual),
        "toomey_2511.23463_posterior_planck_desi": "lambda = -1.3 (+1.3 / -1.5), prior (-3, 0)",
        "field_space_curvature": "metric (3/2)(dphi^2 + da^2)/phi^2: Gaussian curvature -2/3 (hyperbolic; alpha-attractor alpha = 1)",
    }


def main():
    output = calculate()
    path = Path(__file__).with_name("bi_kahler_lambda.json")
    path.write_text(json.dumps(output, indent=1) + "\n", encoding="utf-8")
    for key, value in output.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
