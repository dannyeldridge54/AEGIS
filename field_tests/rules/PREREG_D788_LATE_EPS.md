# PREREG D788: can the late N → udd decays give ε ≥ ε_req? (Nanopoulos–Weinberg check)
Locked 2026-11-16 before computing. Script: theory/modular/late_eps_d788.py. Output: field_tests/results/late_eps_d788.txt.
Literature: for a particle that is stable without the B-violating interaction, the CP asymmetry is at least second order in the B-violating coupling (Nanopoulos–Weinberg; quoted in 1310.0840).
(a) Dim-6 only: ε_max ≈ (1/8π)·(M/Λ)² (one extra insertion of c/Λ² relative to the tree, |c| ≤ 1, maximal phase) [estimate]. Evaluate it for M ∈ {4.3e11, 1e12}, at the D783 Λ_max (T₂ ≥ 1e5) and the D783 Λ (T₂ ≥ 3e6). Compare with ε_req (D783, B-violating: 2e-5 – 1.2e-3).
(b) If (a) fails: postulate P5, a Z₃-charged colour-triplet diquark scalar X with renormalisable couplings y₁ N u X* and y₂ X d d, mass M_X > M. Then Λ_eff² = M_X²/(y₁y₂) and ε ≈ (1/8π)·Im(y₁y₂…)/|y|²·y² ≈ y²/(8π) [estimate]. Report the y needed for ε_req, and M_X for Λ_eff in the D783 window.
Decision: WALL if ε_max(a) < ε_req,min for all cases. P5 VIABLE-ARITHMETIC if y ≤ 1 suffices.
