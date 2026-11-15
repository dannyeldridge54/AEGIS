# PREREG D605: frozen forward predictions for two-term SERAPIS (scored ONLY on data published after 2026-11-15)

Model: plateau I²/(I² + 1) + ε·I₁ (p = 2, α = 1/3), vacuum at τ = i.
- ε ∈ [1.3e-4, 1.6e-4], from the D602 window (post-hoc: ε was chosen after seeing current data).
- Reheating by symmetry-suppressed off-diagonal decays, T_R = 1e3–1e5 GeV (D601).
- Baryogenesis via Affleck–Dine along LH_u (D599–D604).

Bands (from results/eps_window_lowtr_d602.txt; D588 offsets included):
- P1 n_s = 0.9698–0.9754.
- P2 r = 4.8–5.7e-4.
- P3 n_t = −r/8 (single-field consistency); α_s ≈ −(1 − n_s)²/2 ≈ −3e-4 to −5e-4 (estimate).
- P4 Σm_ν = 0.0588–0.0600 eV with NORMAL ordering (m_ν1 ≲ 1e-8 eV).
- P5 no superpartners below ~1e8 GeV: soft masses ~1e9 GeV (no-scale, D585); m₃/₂ ≈ 1.0–1.2e11 GeV.
- P6 negligible isocurvature (≲ 1e-10 of ζ) and f_NL^local ≈ (5/12)(1 − n_s) ≈ 0.01.

Scoring rules:
- DISFAVOURED (≥ 3σ):
  - a future n_s measurement more than 3σ outside P1;
  - r detected more than 3σ outside [2.4e-4, 1.1e-3] (that is, 0.5× to 2× the band);
  - r < 2.4e-4 at 95% CL;
  - Σm_ν detected > 0.07 eV at 3σ;
  - inverted ordering established at > 3σ by oscillation experiments;
  - |f_NL^local| > 5 at 3σ.
- SUPPORTED: r detected inside P2 at ≥ 3σ, with n_s inside P1.
- Each test is scored separately. No re-tuning of ε after future data; any revision is a new model with a new lock.
