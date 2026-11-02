"""BI field as a dilaton-axion pair (Gates, Ketov & Yunes 2009, arXiv:0906.4978): what kinetic mixing does it imply?
    python bi_kahler_lambda.py   -> bi_kahler_lambda.json
Input (quoted from the paper, eqs 5.36-5.37): Omega = e^(P+Pb) (P+Pb),  K = -3 ln(-Omega/3).
Output: the Kahler metric, the canonical dilaton chi, and lambda in f(chi) = e^(lambda chi) multiplying the axion's
kinetic term, the form of Toomey et al. (arXiv:2511.23463). Units: reduced Planck mass = 1. Tier: HYPOTHESIS (algebra
on a quoted Kahler potential; the supergravity embedding of the Twist is an assumption)."""
import json
import sympy as sp

P, Pb = sp.symbols("Phi Phibar")
Omega = sp.exp(P + Pb) * (P + Pb)
K = -3 * sp.log(-Omega / 3)
g = sp.simplify(sp.diff(K, P, Pb))                      # Kahler metric K_{Phi Phibar}

phi = sp.symbols("phi", negative=True)                   # Phi = phi + i a; -Omega/3 > 0 needs phi < 0
g_phi = sp.simplify(g.subs({P: phi, Pb: phi}))          # depends on phi only (shift symmetry in a)
# L_kin = -g (d phi^2 + d a^2). Canonical dilaton: (1/2) dchi^2 = g dphi^2 -> dchi = sqrt(2g) dphi
dchi_dphi = sp.sqrt(2 * g_phi)
# with g = 3/(4 phi^2): chi = sqrt(3/2) ln|phi|, so g = (3/4) e^(-2 sqrt(2/3) chi)
lam = -2 * sp.sqrt(sp.Rational(2, 3))
chi = sp.symbols("chi", real=True)
g_chi = sp.simplify(g.subs({P: -sp.exp(sp.sqrt(sp.Rational(2, 3)) * chi), Pb: -sp.exp(sp.sqrt(sp.Rational(2, 3)) * chi)}))
check = sp.simplify(g_chi - sp.Rational(3, 4) * sp.exp(lam * chi))

out = {
    "kahler_metric": str(g),
    "metric_at_Phi=phi": str(g_phi),
    "canonical_dilaton": "chi = sqrt(3/2) ln|phi|",
    "axion_factor": "f(chi) = exp(lambda chi), after rescaling a_canonical = sqrt(3/2) a",
    "lambda": float(lam),
    "lambda_exact": "-2 sqrt(2/3)",
    "residual_check(should be 0)": str(check),
    "toomey_2511.23463_posterior_planck_desi": "lambda = -1.3 (+1.3 / -1.5), prior (-3, 0)",
    "field_space_curvature": "metric (3/2)(dphi^2 + da^2)/phi^2: Gaussian curvature -2/3 (hyperbolic; alpha-attractor alpha = 1)",
}
json.dump(out, open("bi_kahler_lambda.json", "w"), indent=1)
for k, v in out.items():
    print(f"{k}: {v}")
