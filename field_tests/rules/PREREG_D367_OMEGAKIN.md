# PREREG D367: x's kinetic share during and after matter genesis (Danny "Schedule all needed compute", 08:06 CT). Locked before running.

Purpose: replace D362's background-only estimate (Ω_kin,x ≈ 0.13–0.17 at T = 2×10¹³ GeV, ≈ 0.02 after σ entropy) with the v5 matter run's own
numbers. This is a consistency number for TWIST-I's capture condition (D361–D366), not a prediction.
Run theory/review/omegakin_d367.py: the matter_refit_check settings (m_σ = 5.8×10¹⁰ GeV, decay coupling 0.1, heat 0.8%, exp cliff 4/π, μ = 1,
n = 125), extended to Nafter = 16 e-folds. Every 0.5 e-fold, print T, Ω_kin,x = (dp² + g dy²)/6, Ω_V = V/(3H²), Ω_σ, x, and the running n_B/s.
Validation: the n_B/s printed at the original Nafter = 11 must equal 1.090×10⁻¹⁰ within 1% (D277); otherwise the run is void.
Reading: D362's estimate is CONFIRMED if Ω_kin,x at T ≈ 2×10¹³ GeV lies within ×3 of 0.02–0.17, and FAILED otherwise (D362 is then corrected
with the computed value). It also reports whether x is still rolling (dp > 10⁻³) at the end, which TWIST-I needs for a late capture.
Runs after the D360 T1 runs finish (cloud cores). No reruns.
