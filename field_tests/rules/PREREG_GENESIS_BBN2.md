# PREREG_GENESIS_BBN2 — "stabilise helium": upgraded BBN module (locked D1633, 2026-11-19 15:45 CT)
Context: the toy BBN of PREREG_GENESIS_MATTER FAILED (Y_p = 0.202; D1632). That result stands. This is a NEW lock with a standard (textbook) method, chosen before running and not tuned to the answer.
Method (tools/genesis/bbn2.py):
1. Background: photons + e± with full Fermi–Dirac ρ, P, s integrals; T(a) from entropy conservation of γ+e± (this captures the e± heating); neutrinos T_ν ∝ 1/a, N_eff = 3 + ΔN_eff; H² = 8πρ/(3M_P²).
2. Weak rates: Born approximation, full phase-space integrals over electron energy with separate T and T_ν (Bernstein–Brown–Feinberg / Weinberg form), normalised so the T→0 n→p rate is 1/τ_n (τ_n = 878.4 s). No Coulomb, radiative or finite-mass corrections (these are worth ≈ +0.002–0.005 in Y_p, so a small low bias is expected).
3. Network in time: n, p, D, ⁴He. Capture n + p → D + γ with ⟨σv⟩ = 4.55 × 10⁻²⁰ cm³ s⁻¹ (Dodelson); photodissociation from detailed balance; D + D → (³He, t) → ⁴He lumped as 2D → ⁴He with N_A⟨σv⟩ = 1 × 10⁸ cm³ mol⁻¹ s⁻¹ (order of magnitude). Stiff solver (BDF), T from 10 MeV to 0.01 MeV. η = 6.127 × 10⁻¹⁰ (Ω_b h² = 0.02237).
Pass rules (same window as before, plus two new ones):
P1 Y_p ∈ [0.235, 0.260] (observed 0.245 ± 0.003).
P2 Systematic: rerun with the D + D rate ×10 and ÷10 (pre-declared, part of this lock); report the spread. PASS if spread ≤ 0.01.
P3 dY_p/dΔN_eff from ΔN_eff = 0 and 0.3 ∈ [0.008, 0.018] (literature ≈ 0.013).
If P1 fails, the module stays flagged; no tuning of rates afterwards.
Script: field_tests/scripts/genesis_matter/bbn2_run.py
