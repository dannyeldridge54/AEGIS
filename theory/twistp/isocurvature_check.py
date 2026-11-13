"""D134: isocurvature from light spectators during inflation (both models). AI-assisted, order of magnitude.
(a) TWIST-P light-angle range: the angle's quantum kick at the CMB point, delta y = (H/2pi) / sqrt(2 K_TTbar),
    K_TTbar = 3/(4x^2) + beta/(4x^3); the matter yield's sensitivity is ~1 per unit y at most (period 8), so S_B ~ delta y.
(b) Both models: the hidden axion sigma (m_sigma ~6e10 GeV << H) is light: delta sigma/sigma0 = (H/2pi)/(f_dec M_P);
    S_B = k * delta sigma/sigma0 with k = dlnY/dln sigma0 ~ (s0/f) cot(s0/f) = cot(1) ~ 0.64 for the kick force sin(A y - s/f).
Planck: uncorrelated CDM-equivalent isocurvature P_S/P_zeta < ~0.04 -> S_c < 0.2 * 4.6e-5; S_B = S_c * Omega_c/Omega_b."""
import math, twistp_inflation as TP
H = 1.5e13 / 2.435e18; Pz = 4.6e-5; SB_max = 0.2 * Pz * (0.265 / 0.049)
print(f"bound: S_B < {SB_max:.1e}")
for beta in (0.0, 2.2e-3, 1e-2, 2.2e-2):
    x = TP.obs(beta, 1.2)["xstar"]; K = 3 / (4 * x * x) + beta / (4 * x ** 3)
    dy = (H / (2 * math.pi)) / math.sqrt(2 * K)
    print(f"(a) beta {beta:.1e}: x* {x:.1e}, delta y {dy:.1e} -> S_B <~ {dy:.0e} ({'ok' if dy < SB_max else 'FAIL'})")
for f in (0.05, 0.1, 0.3):
    ds = (H / (2 * math.pi)) / f; SB = (1 / math.tan(1)) * ds
    print(f"(b) f_dec {f}: delta sigma/sigma0 {ds:.1e}, S_B ~ {SB:.1e} ({'ok' if SB < SB_max else 'FAIL'}; margin x{SB_max/SB:.0f})")
