"""Audit test A (7 Nov 2026; AI-assisted, not pre-registered): what can fix the dilaton, and what F does each choice give?
    python dilaton_pinning.py   -> dilaton_pinning.json

GKY superfield Phi = phi + i a, K = -3 ln(-Omega/3). Axion kinetic term -(3/(4 phi^2)) (d a)^2, so the canonical axion
is a_c = sqrt(3/2) a / |phi|. A period P in a therefore gives a canonical decay constant F = sqrt(3/2) P / (2 pi |phi|):
F depends on where the dilaton sits. The note's F = (4/pi) sqrt(3/2) is the |phi| = 1 value, which implies P = 8.
Candidate pinning points:
  |phi| = 1    Einstein-Cartan matching: GKY kinetic metric 3/(4 phi^2) = 3/4, the Calcagni-Mercuri coefficient used
               by nieh_yan_period.py (the-twist-torsion-cosmology); not an extremum of V
  |phi| = 1/2  Jordan-frame GR point (alpha_DEF = 0, Damour-Nordtvedt attractor)
  |phi| = 2/3  minimum of the W = const potential (a constant uplift does not move it)
For each: F, log10 F (the `_fF` run-name value), the curvature of V there, and alpha_DEF."""
import json
import math

import sympy as sp

phi = sp.symbols("phi", negative=True)
chi = sp.symbols("chi", real=True)
V = sp.Rational(81, 2) * (-phi - 1) * sp.exp(-6 * phi) / phi ** 2          # W = 1; bi_superpotential.py
Vchi = V.subs(phi, -sp.exp(sp.sqrt(sp.Rational(2, 3)) * chi))
d1V, d2V = sp.diff(Vchi, chi), sp.diff(Vchi, chi, 2)

P = 2 * math.pi * (4 / math.pi) * math.sqrt(1.5) / math.sqrt(1.5)          # period in a implied by the note: 8
CASSINI_ALPHA = math.sqrt(2.3e-5 / 2)                                       # |gamma - 1| < 2.3e-5, gamma - 1 = -2 a^2


def point(name, absphi, reason):
    c = math.log(absphi) / math.sqrt(2 / 3)
    F = math.sqrt(1.5) * P / (2 * math.pi * absphi)
    a_def = 2 / math.sqrt(3) * (absphi - 0.5)
    curv = float(d2V.subs(chi, c))
    slope = float(d1V.subs(chi, c))
    ext = abs(slope) < 1e-6 * abs(curv)
    return {"pin": name, "abs_phi": absphi, "chi": round(c, 4), "reason": reason, "F_MPl": round(F, 4),
            "log10_F_run_name": round(math.log10(F), 4), "V_curvature_over_W2": round(curv, 1),
            "is_extremum_of_V": ext, "rests_there_with_constant_uplift": ext and curv > 0, "alpha_DEF": round(a_def, 4),
            "passes_Cassini_if_light": abs(a_def) < CASSINI_ALPHA}


def run():
    pts = [point("Einstein-Cartan matching", 1.0, "GKY kinetic coefficient equals the Einstein-Cartan 3/4 here; not an extremum of V"),
           point("GR point", 0.5, "matter in the supergravity Jordan frame: alpha_DEF = 0"),
           point("W=const minimum", 2 / 3, "local minimum of the simplest potential; constant uplift keeps it")]
    return {
        "period_in_a_implied_by_note": round(P, 6),
        "F_formula": "F = sqrt(3/2) P / (2 pi |phi|) = (4/pi) sqrt(3/2) / |phi|",
        "points": pts,
        "reading": [
            "The GR point is a local MAXIMUM of the W = const potential: a light dilaton cannot rest there with this W.",
            "At the W = const minimum, alpha_DEF = 0.19, about 50x the Cassini limit, so the dilaton there must be heavy "
            "(Yukawa range below the ~0.05 mm torsion-balance scale, mass above ~5 meV).",
            "A pinned dilaton cannot also roll as dark energy. So the Spiral (rolling dilaton) and a fixed F exclude each "
            "other: either the dilaton rolls and F is free, or it is pinned and the late field is the axion alone with "
            "one of the discrete F values above.",
            "F = (4/pi) sqrt(6) = 3.119 at the GR point is the 'sqrt(6)'-type value already listed in MIRROR_MAP row 10.",
        ],
    }


if __name__ == "__main__":
    out = run()
    json.dump(out, open("dilaton_pinning.json", "w"), indent=1)
    print(json.dumps(out, indent=1))
