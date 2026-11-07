"""Is the Spiral Twist's decay constant F a real constraint? (audit check, 7 Nov 2026; AI-assisted, not pre-registered)
    python f_dilaton_degeneracy.py   -> f_dilaton_degeneracy.json

Claim tested: in L = -1/2 (d chi)^2 - 1/2 e^(lam chi) (d theta)^2 - V0 e^(-kap chi) - m^2 F^2 (1 - cos(theta/F)),
with matter blind to the dilaton, shifting the dilaton by c is an exact symmetry once the other inputs are rescaled:
    chi0 -> chi0 + c,  F -> F e^(-lam c/2),  theta0 -> theta0 e^(-lam c/2),  m -> m e^(lam c/2),  V0 -> V0 e^(kap c).
If so, fixing F (e.g. from the Nieh-Yan period) says nothing until something physical fixes the dilaton's value.
PASS (degenerate) if H^2 and w agree to < 1e-6 at z = 0..3 for every case. Uses spiral_w.py unchanged."""
import json
import math

import spiral_w as s

TOL = 1e-6
ZS = (0.0, 0.5, 1.0, 2.0, 3.0)
CASES = [  # (kap, m, theta0, shift c); c = -0.8489 puts the start at the Jordan-frame GR point |phi| = 1/2
    (1.2, 3.0, 1.0, -0.8489), (1.2, 3.0, 1.0, 0.5), (0.5, 3.0, 0.5, -0.8489), (0.5, 3.0, 0.5, 1.0),
]


def run():
    lam, F = s.LAM, s.FDEC
    rows = []
    for kap, m, th0, c in CASES:
        V0, solA, VA = s.closed(kap, m, th0)               # reference: chi0 = 0, F = (4/pi) sqrt(3/2)
        k = math.exp(-lam * c / 2)
        solB, VB = s.solve(V0 * math.exp(kap * c), kap, m / k, th0 * k, F=F * k, chi0=c)
        dmax = 0.0
        for z in ZS:
            N = -math.log(1 + z)
            hA, rA, pA = s.H2_of(solA, VA, N)
            hB, rB, pB = s.H2_of(solB, VB, N)
            dmax = max(dmax, abs(hA - hB), abs(pA / rA - pB / rB))
        rows.append({"kap": kap, "m": m, "theta0": th0, "chi_shift": c, "F_equivalent": F * k, "max_diff": float(dmax),
                     "same_cosmology": bool(dmax < TOL)})
    ok = all(r["same_cosmology"] for r in rows)
    return {
        "check": "F vs dilaton starting value in the Spiral Twist",
        "F_paper": F,
        "paper_model_equals": "dilaton starting at the GR point |phi| = 1/2 with F = %.4f" % (F * math.exp(-lam * -0.8489 / 2)),
        "if_dilaton_pinned_at_GR_point_and_F_is_the_Nieh_Yan_value": "paper-convention F = %.4f, not %.4f"
            % (F * math.exp(lam * -0.8489 / 2), F),
        "tolerance": TOL,
        "cases": rows,
        "verdict": "DEGENERATE: F is not a constraint unless the dilaton's value is fixed" if ok else "NOT degenerate",
        "note": "lambda itself is not affected; only F is absorbed. Matter blind to the dilaton is the assumption.",
    }


if __name__ == "__main__":
    out = run()
    json.dump(out, open("f_dilaton_degeneracy.json", "w"), indent=1)
    print(json.dumps(out, indent=1))
