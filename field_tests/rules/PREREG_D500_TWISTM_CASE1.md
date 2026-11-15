# PREREG D500 — Twist-M case (i): full run with a two-sided FI trap at the self-dual point (Danny 20:37 CT "Start"), locked before computing.
Script theory/deep/twistm_case1_d500.py. Field φ (x = e^{cφ}, c = √(2/3)) + radiation, N = ln a from the end of inflation, M_P = 1.
V = V_M(x) + V_FI(x). V_M: D490 Twist-M lnV with n = 234.054, ε = 1.614e-7, normalised by V_* = 4.95e63 GeV⁴ at x* = 6.58e-5 (D494).
V_FI = m_s² M_s² |ζ_M(x)|, ζ_M(x) = (2/π) atan(x) − 1/2 (chosen form: bounded, zero at x = 1, odd under x → 1/x as the duality requires; stated assumption).
M_s from 𝒱(1) = (2a)^{3/2}, a = 7599, g_s = 0.5: M_s = g_s^{1/4}√(π/𝒱) M_P. m_s ∈ {1e-9, 1e4} GeV.
Start: end of inflation (D490 code), φ′² = 2(1 − Ω_r0), Ω_r0 = 0.0075 (as D492). Run to N = 42 (T ~ MeV) or until settled (|ln x| < 1e-6 with |φ′| < 1e-9).
Outputs: number of crossings of x = 1, first crossing N, max excursions, settling N, |ln x| and Ω_x at N = 42 (BBN: Ω_x ≤ 0.05), and the remnant summed over crossings
(D444 method: R = g² ζ_M′(1) M_s² ẋ, g = 0.7, m*² = (R/2)^{2/3}, V_res = m_s² m*²/g², capped by the available V_FI energy at that crossing; Σ V_res/s(T)) vs DM 4.3e-10 GeV.
Verdicts: "CAPTURED AT x = 1" (settled before N = 42 and BBN ok); remnant reported. Crossings capped at 20000 (state if hit). No reruns; fixes via _DEVIATIONS first.
