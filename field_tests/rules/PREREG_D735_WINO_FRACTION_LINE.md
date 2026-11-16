# PREREG D735: does SERAPIS-E's wino sub-fraction survive the H.E.S.S. line limit? (rescale estimate)
Locked 2026-11-16 before computing. Script: theory/modular/wino_fraction_d735.py. Output: field_tests/results/wino_fraction_d735.txt.
## Inputs (literature, fixed now)
- H.E.S.S. 2018 line limit (arXiv:1805.05741): ⟨σv⟩_γγ < 4e-28 cm³/s at 1 TeV, Einasto (stated in abstract). Mass dependence assumed L(M) = 4e-28 (M/1 TeV)² (fixed photon-count scaling; read-off uncertainty × 2 stated). Cored (kpc) profiles weaken it by 1e2–1e3 (paper's footnote).
- Wino line rate (arXiv:1307.4400, Eqs. 5–6, heavy-wino values): σ_γγ ≈ 1.6e-27, σ_Zγ ≈ 1.1e-26 cm³/s; effective line σ_line = σ_γγ + ½σ_Zγ = 7.1e-27, taken mass-independent across 0.66–1.85 TeV (Sommerfeld structure ignored; stated).
- SERAPIS-E fractions (D732, T_R = 3.2e8): f = 0.14 / 0.26 / 0.67 at M2 = 0.66 / 1.0 / 1.85 TeV.
## Decision rule
- f_max = √(L/σ_line). PASS (Einasto) if f ≤ f_max; report the M2 range that passes for Einasto, for Einasto with × 2 uncertainty, and for a kpc core.
- This is an order-of-magnitude rescale, labelled estimate. A dedicated line-shape analysis would supersede it.
