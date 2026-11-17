# PREREG A1 — wino CMB annihilation (dark-matter triangle, Djl A) — locked 2026-11-17
Code: theory/wiring/a1_wino_cmb.py (written after this lock; uses tools/janus_astro/sommerfeld.wino_s, unchanged).
Inputs (all sourced, PREP_A_dm_triangle.md):
- Γ = (π α₂²/2M²)[[2,√2],[√2,3]] (1712.07142 Eq. 3.4); σv_tot = 2 sΓsᵀ (s real from wino_s); α₂ = sommerfeld.ALPHA_W.
- GeV⁻² → cm³/s: (ħc)² c = 0.389379e-27 cm² × 2.99792458e10 cm/s (PDG constants).
- Planck 2018: p_ann < 3.2e-28 cm³ s⁻¹ GeV⁻¹ (2109.02696 citing Planck 2018 VI). p_ann = f_eff σv/M.
- f_eff ∈ [0.14, 0.41] (DERIVED bracket from 1506.03811, see PREP_A).
- Anchor: 1504.05554 — thermal wino present-day σv(WW) "10⁻²⁴–10⁻²⁵ cm³/s".
Tests:
- T1 (convention): s=(1,0) gives σv = 2πα₂²/M² to rel 1e-12. PASS/FAIL.
- T2 (anchor): σv_tot(M=2.9 TeV, v=1e-3) in [5e-26, 2e-24] cm³/s (anchor band with ×2 margin; order-of-magnitude check, labelled). PASS/FAIL.
- T3 (saturation): |σv(v=1e-7)/σv(v=1e-6) − 1| < 0.1 for every grid mass except within ±0.1 TeV of a resonance peak (reported, not scored).
- RESULT (prediction, not pass/fail): on M = 0.5…3.5 TeV (step 0.1, plus 2.3–2.5 step 0.02) at v=1e-7, p_ann(M) for f_eff=0.14 and 0.41; excluded mass ranges for f_wino=1; max allowed DM fraction f_max = sqrt(3.2e-28/p_ann) (f² scaling).
A1 VALIDATED iff T1 and T2 pass. Fixes only via DEVIATIONS written before any rerun.
