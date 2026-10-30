"""Independent re-check of the UFE / Locked Twist numbers (no AEGIS code used)."""
import math
from scipy.stats import chi2, norm
from scipy.integrate import solve_ivp
import numpy as np

ok = lambda c: "PASS" if c else "FAIL"
rows = []
def chk(name, got, want, tol):
    rows.append((ok(abs(got - want) <= tol), name, got, want))

# 1. Field origin: phi0 = sqrt(3/2) arsinh(1/gamma). Which gamma gives the quoted rest point 2.6265 M_Pl?
s = math.sqrt(1.5)
g_from_phi = 1 / math.sinh(2.6265 / s)
g_meissner = 0.237532957965                     # Barbero-Immirzi value from black-hole entropy (Meissner 2004)
chk("gamma implied by phi0 = 2.6265", g_from_phi, g_meissner, 2e-4)
chk("phi0 from Meissner gamma (M_Pl)", s * math.asinh(1 / g_meissner), 2.6265, 1e-3)
rows.append(("INFO", "phi0 from the other LQG value gamma = 0.2740 (should NOT match)", s * math.asinh(1 / 0.27398563), "2.4569, not 2.6265: the rest point picks out 0.2375"))

# 2. Width module
chk("F = sqrt(3/2)/9 (M_Pl)", s / 9, 0.1361, 5e-5)

# 3. Fluid exponent and <w> for n = 3
n = 3
w = (n - 1) / (n + 1)
chk("<w> = (n-1)/(n+1)", w, 0.5, 1e-12)
chk("exponent 3(1+w)", 3 * (1 + w), 4.5, 1e-12)
# numerically: oscillation in V = (1-cos x)^3 with small amplitude, time-average of w = (K-V)/(K+V)
def rhs(t, y): return [y[1], -3 * (1 - math.cos(y[0])) ** 2 * math.sin(y[0])]
sol = solve_ivp(rhs, (0, 4000), [0.3, 0.0], max_step=0.05, rtol=1e-10, atol=1e-12)
x, v = sol.y; K = 0.5 * v ** 2; V = (1 - np.cos(x)) ** 3
wt = np.trapezoid((K - V), sol.t) / np.trapezoid((K + V), sol.t)
chk("<w> by direct integration (small oscillations)", wt, 0.5, 0.01)

# 4. The lock: a_c = omega_r / omega_m
wr = 2.4728e-5 * (1 + 0.22711 * 3.044)
chk("omega_r (N_eff = 3.044)", wr, 4.1823e-5, 2e-8)
wm_needed = wr * (1 + 3560)                     # omega_m implied by the quoted z_c = 3560
rows.append(("INFO", "omega_m implied by z_c = 3560", wm_needed, "Planck LCDM 0.1430 gives z_eq 3418; EDE fits raise omega_c"))
chk("z_eq for Planck LCDM omega_m = 0.1430", 0.1430 / wr - 1, 3418, 25)

# 5. Information criteria and significance
for lab, d, k, aic in (("Planck 2-setting", -4.70, 2, -0.70), ("P-ACT 2-setting", -7.23, 2, -3.23),
                       ("Planck 1-setting", -4.46, 1, -2.46), ("P-ACT 1-setting", -6.14, 1, -4.14)):
    chk(f"dAIC {lab}", d + 2 * k, aic, 1e-9)
p1 = chi2.sf(6.14, 1); chk("p (dchi2 6.14, 1 dof)", p1, 0.013, 0.0006)
rows.append(("INFO", "sigma for p(6.14, 1 dof)", norm.isf(p1 / 2), "~2.5 sigma"))
p2 = chi2.sf(7.23, 2); rows.append(("INFO", "p / sigma (7.23, 2 dof)", f"{p2:.4f} / {norm.isf(p2 / 2):.2f}", "~2.2 sigma"))

# 6. Acoustic scale
th = 1.0408e-2
chk("l_A = pi / theta*", math.pi / th, 301.8, 0.1)
peaks = [220, 536, 813, 1127, 1421, 1727, 2011]
chk("mean peak spacing", (peaks[-1] - peaks[0]) / 6, 298.5, 0.01)
chk("sound horizon change %", (140.7 / 144.9 - 1) * 100, -2.9, 0.01)

# 7. Hilltop starts as fractions of pi
chk("theta_i Planck / pi", 2.77 / math.pi, 0.88, 0.005)
rows.append(("INFO", "theta_i P-ACT / pi", 2.71 / math.pi, "hold-release prediction 0.88"))

w0 = max(len(r[1]) for r in rows)
for r in rows:
    got = f"{r[2]:.6g}" if isinstance(r[2], float) else r[2]
    print(f"{r[0]:5} {r[1]:<{w0}}  got {got}   expect {r[3]}")
print(f"\n{sum(r[0] == 'PASS' for r in rows)} pass, {sum(r[0] == 'FAIL' for r in rows)} fail, {sum(r[0] == 'INFO' for r in rows)} info")
