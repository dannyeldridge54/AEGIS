# PREREG D781: SERAPIS-E observables if the Z₃-charged heavy ν reheat the universe late (D780)
Locked 2026-11-16 before computing. Script: theory/modular/late_reheat_d781.py (the D725 N* code with ρ_th evaluated at T₂; nothing else changed). Output: field_tests/results/late_reheat_d781.txt.
History: inflaton oscillation (quadratic, w = 0) → decay at T_R1 into non-relativistic heavy N (w = 0) → N decay at T₂ → radiation. Since both phases are matter-like, the matching uses ρ_th = (π²/30)g*T₂⁴ in the D725 formula.
Runs: C ∈ {1.0, 1.15, 1.3}e-6 × T₂ ∈ {3.175e8 (K4), 3e6, 3e4, 3e2} GeV.
K4: C = 1.15e-6, T₂ = 3.175e8 reproduces D725 (N* = 49.72, n_s = 0.9732, r = 4.697e-4).
Decision per T₂:
- INSIDE if some C ∈ [1.0, 1.3]e-6 gives n_s ∈ [0.970, 0.975] and r ∈ [4.55, 5.12]e-4 (the frozen D693 bands);
- else OUTSIDE ⇒ CORRECTION (no retuning; the frozen bands stay as frozen).
