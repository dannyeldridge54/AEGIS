# PREREG_WEAVE_INDEX — does N_eff = s = 3/2 come out of E(τ, 3/2) on the Z₃ orbit at ρ? (locked D1604, 2026-11-19 12:42 CT)
Orbit: γ(τ) = (τ − 1)/τ (order 3, fixes ρ = e^{iπ/3}); points τ₀, γτ₀, γ²τ₀.
Constructions (fixed list): K1 v_k = y_k^{3/2} (tree strand); K2 v_k = y_k^{−1/2} (one-loop strand); K3 v_k = 2ζ(3)y_k^{3/2}/E(τ_k) (tree share of E); K4 v_k = y_k ∂_y ln E(τ_k) (gradient strand, the Zhinü object); K5 v_k = (⅔ y_k ∂_y ln E)² (the Zhinü plateau factor V₀/V∞ itself).
Effective generation number N_eff = (Σ|v|)²/Σv² (Koide Q = 1/N_eff).
Evaluate at: τ₀ = ρ + ε e^{iφ} for ε ∈ {0.05, 0.1, 0.2, 0.3} and φ ∈ {0, π/2, π, 3π/2}; at τ₀ = i; at τ₀ = 2i, 5i (approaching the cusp).
Pass rule: a construction PASSES if N_eff = 1.5 ± 0.0015 either (a) for all ε, φ, or (b) at τ₀ = i, or (c) in the cusp limit (5i, with 2i trending to it). Otherwise FAIL. No constructions or points added after seeing results.
Script: field_tests/scripts/weave_index/run.py
