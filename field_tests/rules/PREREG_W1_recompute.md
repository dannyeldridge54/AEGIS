# PREREG W1 — first real-recompute wave on the AEGIS web: SERAPIS-E sensitivities (measured edge strengths)
Locked 2026-11-17 20:20 CT before running. Context: the heuristic wave from serapis_e (docs/web/waves.json) answered most strongly at nstar_e (+0.555), then S_6d,
bhk_tilt (+0.258), band_e (+0.155). W1 replaces guesses with measured sensitivities using the existing exact pipeline (tools/serapis_calc/pipeline.predict, unchanged).
Baseline: SERAPIS-E, C = 1.15e-6, T_R = 1e7 GeV (self-consistent N*). Waves (each + and its exact inverse):
 w_N: N* → N* ± 1 at fixed potential (spectra at fixed N); w_C: C → C × (1 ± 0.1) (BHK tilt), self-consistent N*; w_T: T_R → T_R × 10^(±1), self-consistent N*.
Report for each: Δn_s, Δr/r, Δα_s (+ and −), the asymmetry |Δ+ + Δ−| (nonlinearity), and the distance of n_s to CMB-SPA (0.9684 ± 0.0030) and SPA+DESI (0.9728 ± 0.0027).
Reading rule (fixed now): an edge's measured strength = |Δn_s|/σ_SPA for its wave; the heuristic ordering (nstar_e > bhk_tilt) is CONFIRMED if |Δn_s(w_N)| > |Δn_s(w_C)|,
otherwise REVERSED. Asymmetry > 20 % of |Δ| marks a nonlinear link (flagged on the web). Labels: computed; no physics claim beyond these sensitivities.
