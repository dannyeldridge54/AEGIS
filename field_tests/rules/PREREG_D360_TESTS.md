# PREREG D360: two more tests (Danny "More test", 07:49 CT 14 Nov). Locked before running. AI-assisted.

## T1. Isocurvature at the alternative reading's own fit point (closes D320's stated limitation)
Run theory/review/alt_isocurv_d360.py: the D268 one-pass script at m_σ = 3.0×10¹⁰ GeV (the alternative reading's 1× fit point, D297), other
settings as D320. Two runs in parallel: baseline s0 = 0.1 and s0 = 0.105.
Report: Y_alt(base) (expected ≈ 1× observed, ±30%, as the fit point was set by the m_σ^−0.89 scaling) and S_alt = ln(Y_alt(1.05)/Y_alt(base))/ln 1.05.
Rule: |S_alt| ≤ 5 → PASS; margin 5.1/S_alt at f = 0.1 M_P (≥ 1 passes). If Y_alt(base) is outside 0.5–2× observed, report "fit point off"; the S
result still stands. No reruns.

## T2. Numerical check of D359's dilution estimate (an estimate check, not a prediction)
Script theory/review/modulus_dilution_d360.py: a homogeneous modulus φ with V = m²φ²/2, decay rate Γ = m³/8πM_P², radiation with g* = 106.75,
started at H = 10 m with φ₀ = A M_P at rest, integrated through decay. Dilution Δ = S_final/S_without-modulus. Cases: m = 10⁹ GeV (A = 1, 10⁻³) and
m = 10¹³ GeV (A = 1, 10⁻³). Pass: each numerical Δ is within a factor 10 of D359's estimate (1.5×10⁹, 1.5×10³, 1.5×10³, ~1). Otherwise D359 is
corrected. (The 10⁵ GeV case is skipped as too stiff; it follows from the same scaling.)
