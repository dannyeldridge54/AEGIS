# PREREG R2b2 — continuity of the total χ⁰χ⁰ σv across the χ⁺χ⁻ threshold — locked 2026-11-17 (before any run)
Context: D1158 found |s_{00,00}|² jumps from 0.0023 (just below, wino_s) to 2.86 (just above, two_channel_open). That compares different objects, so it is not the physical test.
Physical quantity: σv(χ⁰χ⁰ in) ∝ s Γ s†, with Γ = [[2, √2], [√2, 3]] in the (00, +−) basis (A1, πα₂²/2M² dropped since it cancels in the ratio).
- Closed side (E < 2δm): s = sommerfeld_nlo.wino_s_nlo(M, v, nlo=False) (real 2-vector).
- Open side (E > 2δm): s = row 0 of sommerfeld.two_channel_open(M, v, Vfun, DM, tails=(0, ALPHA)).
  Vfun is built from the SAME constants as wino_s_nlo (ALPHA2, ALPHA, CW2, MW, MZ, DM from sommerfeld_nlo), so both sides share one potential.
- M = 2000 GeV. E/2δm ∈ {0.95, 0.99, 1.01, 1.05, 1.2, 1.5}, with v = 2√(E/M).
Score:
- jump = |S(1.01)/S(0.99) − 1|. PASS iff jump ≤ 0.20 (a threshold cusp is allowed; an order-of-magnitude jump is not).
- Also reported, not scored: S at all six points, plus |s_00|², |s_0+|².
Fail path: diagnose only. No tuning. Any fix goes in DEVIATIONS_R2b2 written before a rerun.
