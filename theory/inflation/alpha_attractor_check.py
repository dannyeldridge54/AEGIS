"""T2: is the Twist's field space an alpha-attractor, and what inflation does that imply? AI-assisted.
Metric ds^2 = d sigma^2 + e^{lam sigma} d chi^2 (units M_P) has Gaussian curvature K = -lam^2/4.
alpha-attractors (Kallosh-Linde): K = -2/(3 alpha). The Twist fixes lam = -2 sqrt(2/3) (not fitted)."""
import math
lam = -2 * math.sqrt(2 / 3)
K = -lam ** 2 / 4
alpha = -2 / (3 * K)
print(f"lam = {lam:.4f}; Gaussian curvature K = {K:.4f}; alpha = {alpha:.4f}  (alpha = 1: the Starobinsky class)")
# Leading-order attractor predictions; N set by reheating. Twist leptogenesis needs T_RH >~ 2e13 GeV (near-instant
# reheating), which puts N near its maximum for this class, ~55-57.
for N in (50, 55, 57):
    ns, r = 1 - 2 / N, 12 * alpha / N ** 2
    print(f"N = {N}: n_s = {ns:.4f}, r = {r:.4f}")
data = {"Planck 2018 (+lensing)": (0.9649, 0.0042), "Planck+ACT+SPT (CMB-SPA)": (0.9684, 0.0030),
        "Planck+ACT+DESI (P-ACT-LB)": (0.9743, 0.0034)}
ns = 1 - 2 / 56
for k, (m, s) in data.items():
    print(f"{k}: {m} +/- {s}: Twist (N=56, n_s={ns:.4f}) is {(ns - m) / s:+.1f} sigma")
print("r: BICEP/Keck 2018 r < 0.036 (95%): Twist r ~ 0.004, allowed; LiteBIRD / CMB-S4 aim at sigma(r) ~ 0.001")
