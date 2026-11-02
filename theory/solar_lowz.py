"""SSG part of PREREGISTRATION_SOLAR_LOWZ.md (locked 2026-11-02 15:17:31): solar-system gate for the BI dilaton.
    python solar_lowz.py   -> solar_gate.json
Reading A: matter on the supergravity Jordan frame, A^2 = -3/Omega, Omega = e^(2 phi) * 2 phi, phi = -exp(sqrt(2/3) chi).
alpha = sqrt2 * dlnA/dchi (Damour-Esposito-Farese); gamma - 1 = -2 alpha^2 / (1 + alpha^2); Cassini |gamma - 1| < 2.3e-5."""
import json
import sympy as sp

chi = sp.symbols("chi", real=True)
phi = -sp.exp(sp.sqrt(sp.Rational(2, 3)) * chi)
Omega = sp.exp(2 * phi) * 2 * phi
lnA = sp.Rational(1, 2) * sp.log(-3 / Omega)
alpha = sp.simplify(sp.sqrt(2) * sp.diff(lnA, chi))
d2 = sp.simplify(sp.diff(lnA, chi, 2))

gr_points = sp.solve(sp.Eq(alpha, 0), chi)
CASSINI = 2.3e-5
amax = (CASSINI / (2 - CASSINI)) ** 0.5            # |gamma-1| = 2a^2/(1+a^2) < C  ->  a^2 < C/(2-C)
rows = []
for c0 in gr_points:
    c0f = float(c0)
    curv = float(d2.subs(chi, c0))
    slope = float(sp.diff(alpha, chi).subs(chi, c0))   # alpha ~ slope * dchi near the GR point
    band = amax / abs(slope)
    # check the band numerically on the exact alpha
    a_lo, a_hi = float(alpha.subs(chi, c0f - band)), float(alpha.subs(chi, c0f + band))
    rows.append({"chi_GR": c0f, "phi_GR": float(phi.subs(chi, c0)), "d2lnA": curv, "dalpha_dchi": slope,
                 "allowed_band_dchi": band, "alpha_at_band_edges": [a_lo, a_hi]})

if not gr_points:
    verdict = "EXCLUDED"
else:
    r = rows[0]
    if r["d2lnA"] > 0:
        verdict = "ATTRACTOR-PROTECTED"
    elif r["allowed_band_dchi"] < 0.01:
        verdict = "FINE-TUNED"
    else:
        verdict = "UNCLASSIFIED (band >= 0.01 and not an attractor; rule has no category)"

out = {"alpha(chi)": str(alpha), "d2lnA(chi)": str(d2), "cassini_alpha_max": amax, "gr_points": rows,
       "far_from_GR_example": {"chi=0": float(alpha.subs(chi, 0)), "chi=-2": float(alpha.subs(chi, -2))},
       "verdict_reading_A": verdict,
       "reading_B": "matter on the Einstein frame: alpha = 0 by construction (extra assumption, not a pass)"}
json.dump(out, open("solar_gate.json", "w"), indent=1)
print(json.dumps(out, indent=1))
