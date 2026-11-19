# PREREG_FLAV_RHO — flavour at the inflation endpoint ρ (locked D1595, 2026-11-19 12:15 CT)
Question: does the residual Z₃ at τ = ρ, with the minimal A4 (Γ₃) weight-2 modular triplet Y(τ) (Feruglio 1706.08749), give Koide's Q = 2/3?
Validation (must pass first): Y(ω)/Y₁ = (1, ω, −ω²/2) to |Δ| < 1e-10; else the run is INVALID.
Constructions (fixed list, no additions after seeing results): C1 √m_i ∝ |Y_i|; C2 m_i ∝ |Y_i|; C3 √M = circ(Y₁,Y₂,Y₃) eigenvalue moduli; C4 √M = circ(Y₁,Y₃,Y₂). Evaluated at ρ (= ω + 1), ω, and i (comparison).
Pass rule: |Q − 2/3| < 1e-3 at ρ for a construction ⇒ that construction "reproduces Koide at ρ"; otherwise FAIL for that construction.
Also reported (descriptive, no pass rule): Koide amplitude and phase δ from current lepton masses (Belle II 2023 m_τ; PDG m_τ recalled), vs 2/9.
One run. Script: field_tests/scripts/flav_rho/run.py.
