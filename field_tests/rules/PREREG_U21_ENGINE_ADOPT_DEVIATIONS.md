# DEVIATIONS to PREREG_U21_ENGINE_ADOPT (engine/kit adoption) — written BEFORE each change
Repo at ab0c2991 (21 Nov 2026, 17:12 UTC) when D1–D9 were written. CubeMind engineering agent (notes: theory/pending_docs/CUBEMIND_ENGINEERING_NOTES.md, E1+).
Rule kept: one entry per item; before/after values recorded; no tolerance loosened. A self-test assertion that pinned an OLD default is
re-pinned to the old value as an EXPLICIT argument (so the published reference number is still reproduced), and a new assertion checks the new default.

## D1 — α⁻¹ = 28.0 at M₁₂ = 1.06e16 GeV (D1800, D1804)
- weave_magd7 default alpha_inv 24.3 → 28.0. Before (default): Re T 16.51, x 0.3208, T_R 4.30e8 GeV. After: Re T 20.21, x 0.2784, T_R 3.73e8 GeV.
- New tool weave_point carries alpha_inv_M12 = 28.0, M12_GeV = 1.06e16 (two-loop, gluino 5.6 TeV gives 27.93 at 1.073e16: same point).
- Self-test: magd7 assertion uses alpha_inv = 40 explicitly; unchanged.

## D2 — N = 6, χ ≈ 90, 𝒱 = 7.5e4, W₀ = 1.0e-8 (D1811)
- weave_W0 defaults volume 1e5 → 7.5e4, m32_GeV 5e5 → 2.6e5 (m₃/₂ from D1808/D1811). Before W0 = 2.70e-8; after W0 = 1.05e-8 (matches D1811's 1.03e-8 at A = 1 to 2 %).
- weave_point carries N = 6, chi ≈ 90 (88–91), volume 7.5e4, W0 1.0e-8, m32 2.6e5; label "consistency selection, not prediction" (D1811).

## D3 — T_R = 3.7e8 GeV, x = 0.279 (D1801)
- weave_wino default T_R 2.61e8 → 3.7e8. Before passing [0.66, 1.0]; after passing [0.66] (f(0.66) = 0.154 ≤ 0.16; f(1.0) = 0.282 > 0.24), the D1801 window 0.66–0.69 TeV.
- weave_genesis default T_R 2.61e8 → 3.7e8. Before eps 6.2e-6, window [6.3e10, 2.5e12]; after eps 4.4e-6, window [4.4e10, 2.5e12], viable.
- weave_rinv default x 0.32 → 0.279. Before r 5.72e-4 (D = 21.5); after recorded in E1.
- Engine: bbn link label L4 "T_R ≈ 1.34e9" → states the inflaton value 1.34e9 AND the visible T_R = x·1.34e9 = 3.7e8 (labels only, no number computed from it).
- Self-test: wino/genesis/rinv assertions use explicit T_R/x; unchanged.

## D4 — gluino 5.6 TeV (D1808)
- weave_rg and weave_rg2 default m_gluino 7000 → 5600. Before rg2 α_s(unif) 0.11584, M₁₂ 1.072e16; after 0.11474, 1.073e16 (D1808: 0.1147).
- Self-test: the weave_rg assertion (M₁₂ 7.2–7.7e15, α⁻¹ 28.77, Δ₃ −0.90) is the published one-loop B11 reference at the OLD 7 TeV gluino; it is
  re-pinned with m_gluino = 7000 passed explicitly (physical reason: the reference number belongs to that input). New assertion: weave_rg2 default α_s(unif) = 0.1147 ± 0.0005.

## D5 — α_D = 0.021–0.022, CONDITIONAL (D1795, D1807 #4, D1812)
- weave_sidm default alpha_D 4.7e-4 → 0.021; label gains "α_D conditional (dark cycle = photon-axion cycle or rank rule N_d = 2N)". Before σ/m 9.33e-7; after 1.86e-3 cm²/g (0.022 gives 2.04e-3; D1795 quotes 2.1e-3).
- Self-test: the C3 reference assertion (9.33e-7) re-pinned with alpha_D = 4.7e-4 explicit; new assertion default σ/m = 1.86e-3 ± 2 %.

## D6 — axion f = √(3/2)/(2πσ) M_P (D1807 #1)
- New query weave_basic q = 'axion_f' {sigma}: value = f/M_P, f_GeV = value·2.435e18. At σ = 38.6: 0.00505 M_P = 1.23e16 GeV. No existing number changes.
  weave_axion_relic (QCD misalignment scaling) is NOT changed: it is a QCD-axion tool, not the dark-cycle axion.

## D7 — proton branch G τ_p ≈ 1.6e35 yr (D1807 #2)
- weave_point carries tau_p_branchG_yr = 1.6e35 (recorded value from D1807, label "recorded, not computed by the kit"; mostly beyond Hyper-K).

## D8 — Λ is an input (D1795)
- weave_point carries Lambda = 'input (U19 withdrawn)'; engine late level gains the label "Λ is a constant input (D1795)". No number changes.

## D9 — (outside the U21 list; referee D1807 #8) weave_nuclear b₀ = 9 (n_f = 3)
- weave_nuclear gains b0 (default 9, was the hard-coded 23/3). Before alpha_s_precision_needed 4.25e-4, δα_s = 0.0033 → δm_q/Λ 0.194;
  after 5.0e-4 and 0.165. Self-test: the 4.25e-4 assertion re-pinned with b0 = 23/3 explicit; new assertion default 5.0e-4 ± 1e-5 (D1807: "≲ 5e-4").
