"""Scales-loop round 1, lead 2 (exploratory, not a pre-registered test): the dilaton potential that N = 1 supergravity
gives the BI superfield (Gates-Ketov-Yunes K) for the simplest superpotential, W = constant.
    python bi_superpotential.py   -> bi_superpotential.json
V = e^K (K^{-1} |K_Phi W|^2 - 3|W|^2) with K = -3 ln(-Omega/3), Omega = e^(Phi+Phibar)(Phi+Phibar), Phi = phi + i a.
Reduced Planck units. Canonical dilaton |phi| = exp(sqrt(2/3) chi). Reports the shape, sign, extrema and the
steepness s = -dlnV/dchi (Toomey et al. need a runaway with s > 5)."""
import json
import sympy as sp

P, Pb = sp.symbols("Phi Phibar")
W = sp.symbols("W", positive=True)
K = -3 * sp.log(-sp.exp(P + Pb) * (P + Pb) / 3)
KP = sp.diff(K, P)
Kinv = 1 / sp.diff(K, P, Pb)
V = sp.exp(K) * (Kinv * KP * sp.diff(K, Pb) * W ** 2 - 3 * W ** 2)
phi = sp.symbols("phi", negative=True)
Vphi = sp.simplify(V.subs({P: phi, Pb: phi}))
chi = sp.symbols("chi", real=True)
Vchi = sp.simplify(Vphi.subs(phi, -sp.exp(sp.sqrt(sp.Rational(2, 3)) * chi)))
steep = sp.simplify(-sp.diff(sp.log(sp.Abs(Vchi)), chi))
crit = sp.solve(sp.diff(Vphi, phi), phi)
zeros = sp.solve(sp.Eq(Vphi, 0), phi)

samples = []
for pv in (-0.25, -0.5, -0.9, -1.0, -1.5, -2.0, -3.0):
    c = float(sp.log(-pv) / sp.sqrt(sp.Rational(2, 3)))
    samples.append({"phi": pv, "chi": c, "V_over_W2": float(Vphi.subs(phi, pv) / W ** 2),
                    "steepness": float(steep.subs(chi, c))})
out = {"V(phi)": str(Vphi), "zeros_phi": [str(z) for z in zeros], "critical_phi": [str(c) for c in crit],
       "V_at_GR_point_over_W2": float(Vphi.subs(phi, -sp.Rational(1, 2)) / W ** 2), "samples": samples}
json.dump(out, open("bi_superpotential.json", "w"), indent=1)
print(json.dumps(out, indent=1))
