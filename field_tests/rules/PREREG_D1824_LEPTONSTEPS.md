# PREREG D1824 — charged leptons on the ρ theta-step ladder (locked 21 Nov 2026 before computing; repo at 6981ebac)
Steps (derived as D1822): for (M_L, M_R, M_H) = (9, 9, 18) on T²/Z₃ at τ = ρ, K = 1458, characteristic a = (n + s)/162 with integer n and SS shift s = 1/6 (all three phases 1/6 ⇒ one common shift, stated assumption); coupling steps e^{−c(n+s)²}, c = π Im ρ · K/162² = 0.1511. Allowed family ratios: R = e^{−c[(n₁+s)² − (n₂+s)²]}, n₁ > n₂ ≥ 0, n ≤ 12.
Targets: m_μ/m_τ = 0.0595, m_e/m_μ = 4.84e-3 (both must be hit by a CONSISTENT triple n_τ < n_μ < n_e). Hit: within 10 % for each.
Coverage guard: fraction of log-uniform random ratios in [1e-4, 1] within 10 % of some allowed R = f; and the chance that a random PAIR is hit by a consistent triple = f₂ (Monte Carlo, 20000 pairs).
Verdict: SIGNAL only if a consistent triple exists AND f₂ < 0.01; HIT-BUT-VACUOUS if a triple exists but f₂ ≥ 0.01; MISS if none.
