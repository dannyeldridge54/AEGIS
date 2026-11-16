# PREREG D722: φ → N2N2 width at τ = ρ (massless doublet state), T_R and N*
Locked 2026-11-16 before computing. Script: theory/modular/phi_n2n2_d722.py. Output: field_tests/results/phi_n2n2_d722.txt.
## Checks first (decide NULL)
1. Basis: |B22| = |(Uᴴ ∂_yA U*)₂₂| must be unchanged (to 1e-10) under U₂ → e^{iα}U₂ for α ∈ {0.3, 1.1, 2.0}, and must equal lim M2(ρ + iδ)/δ (δ = 1e-3, 1e-4, 1e-5) to 1%. If either fails: NULL, loop stops.
## Computation
2. g22 = M1·(|B22|/0.2241)·y√(2/3)/M_P (y = √3/2; K = −3 ln 2y canonical normalisation; overall O(1) Kähler/normalisation prefactor of the N kinetic term not modelled — stated as an estimate). Γ = g22² m/(16π) (identical massless Majorana pair), m = 2.2e13 GeV, M1/m ∈ {0.1, 0.2, 0.33, 0.45, 1, 10}. T_R = (90/(π²·106.75))^{1/4}√(ΓM_P), capped at instant reheating (ρ_th ≤ ρ_end).
3. N* (D719 code, C = 1.15e-6) at T_R for M1/m = 0.1 and 10.
## Decision rule
- CONSISTENT with D692 if the band (M1/m 0.1–10) overlaps 1e6–1e8 GeV; else correction note (no retuning of frozen bands), report N* and n_s and whether n_s stays in 0.970–0.975.
- Fixes only via D722_DEVIATIONS.md written before any rerun.
