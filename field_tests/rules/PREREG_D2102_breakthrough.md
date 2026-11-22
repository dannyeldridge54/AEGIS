# PREREG D2102: the breakthrough chart in one pass (B1, B4, B2, B3); formulas and goalposts as in tools/bloom/BREAKTHROUGH_CHART_2026-11-22.md. Locked before computing.

- **B1:**
  - For k = 1..6, compute B = W₀_target/e^{−2πk·(√3/2)}, for the KKLT target 2.70–2.86e-9 and for the KL (7, 8) target 2.0e-9 (with A = 1).
  - **PASS** if some integer k gives B ∈ [0.1, 10]. The window is the same as D2046's, **not widened**.
  - **Look-elsewhere:** the fraction of log-uniform targets in [1e-10, 1e-8] that also pass (p).
- **B4:**
  - μ_W = 0.25 × 0.551 × 159 TeV.
  - For M = M_s = 1e16 GeV and M = M_P = 2.435e18 GeV, find the integer k giving C ∈ [0.1, 10].
  - **PASS** or FAIL, with p computed the same way (targets log-uniform over 1–100 TeV).
- **B2 (ESTIMATE):**
  - D3 cost = N_vis·3 + 1 for N_vis ∈ {2, 3, 5} (families 3·1·1), against the give-back range 17–34 and the budget 4–6.
  - Report "within budget" or "over".
- **B3:**
  - Seed at L = 3, χ_i ∈ {1/3, 1/2, 2/3, 1, 3/2, 2, 3} (343 points), 30 s per χ.
  - PS three families, then tadpole + K completion, then the D2097 confinement rule for every exotic ring.
  - Then the one-loop α_s fit (D2083 predict), against the goalposts α_s within 2σ and M_s ≥ 4e15.
  - **PASS** if ≥ 1 exotic-safe model hits; report counts and look-elsewhere (hits / near / 0.09).
