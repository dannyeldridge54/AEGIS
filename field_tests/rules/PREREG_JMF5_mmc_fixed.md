# PREREG JMF5 — Janus-MF non-separable vs a derivative-consistent MultiModeCode build
Locked 2026-11-17 before any JMF5 number from the patched build. Patch: theory/janus/mmc_jmf5_fix.patch (sha256 prefix bbe24da49898a98f) on MMC @641153c,
built at /home/claude/ext/mmc_fix. Changes (only these): case 11 — dV of the lightest field gains (1/12)φ_L Σ_{i≠L} λ_iφ_i²; d²V_{Li} = d²V_{iL}
= (1/6)λ_iφ_Lφ_i; d²V_{LL} gains (1/12)Σ_{i≠L} λ_iφ_i². Case 12 — V gets ½ on off-diagonal terms, V = ½φᵀMφ (the code comment's
"mass matrix", so its dV and d²V were already right). Mode solver untouched.
Models: N1 as JMF4 (Janus functions unchanged, already known: n_s 0.954824, r 0.19566 — the unknown is the patched MMC).
N2' = ½m₁²φ₁² + ½m₂²φ₂² + εφ₁φ₂, m² = (1e-11, 9e-11), ε = 1e-12, φ_init (12, 12) — Janus gets these exact V, ∇V, Hessian.
MMC run settings as JMF4 (running-of-running and δN-SR side outputs off). Claims: C1 |Δn_s| ≤ 2e-4, C2 |Δr/r| ≤ 2e-3, each model.
All pass → JANUS-MF NON-SEPARABLE AGREES WITH A CONSISTENT REFERENCE. Honest scope label in any case: the reference is MMC's mode solver with
my patch, not a fully independent code. Results: field_tests/results/janus_jmf5.txt (+ stamp).
