# PREREG NA15 — node audit close-out: eps_tilt, covariant, matter_parity, sterile_i, plateau_origin, logderiv_plateau, wino_window
Locked before computing. These nodes carry no new numerical chain to recompute beyond what NA8/NA12 did; checks:
1. matter_parity (D663): Σk(LLH_uH_u) = 2k_L + 2k_Hu ≡ 2 (mod 4) for all k_L odd, k_Hu even (enumerate k ∈ [−7, 7]). PASS if true for all.
2. covariant (D649/D655): the τ = i and ρ bounds agree at the shared y points (23, 26, 28, 30) within 5 % (D655 says "the same"). PASS/FAIL per point.
3. eps_tilt: update node value with NA12 (τ = i window ε ≈ 1.39–1.44e-4 under audited reheating); status stays estimate (fitted).
4. sterile_i: covered by NA8 (D727 coupling λ = √2 κ, n = 1, consistent; mass corrected) — record.
5. plateau_origin (assumed) and logderiv_plateau (killed, D822): status review only (no arithmetic headline); record unchanged.
6. wino_window: BLOCKED (g*(T) EOS table, member.ipmu.jp refused by egress proxy; awaiting Danny's manual save).
Results: field_tests/results/na15_structural.txt.
