# PREREG JMF3 — JANUS-MF beyond quadratic: exact multi-field MS vs MultiModeCode on two non-quadratic 2-field potentials
Locked 2026-11-17 before any JMF3 number (Janus-MF or MMC). Code under test: tools/janus_calc/mfms.py (unchanged since D1162, JMF2).
Reference: MultiModeCode (laynep/MultiModeCode @641153c, /home/claude/ext/mmc), its exact n_s and r = (r/n_t)·n_t, same parsing as JMF1/JMF2.
Potentials [MMC modpk_potential.f90, cases fetched from source]:
 M1 N-quartic (case 3): V = Σ ¼ λ_i φ_i⁴, λ = (1e-13, 9e-13) [vparams(1,:) = -13, -13+log10 9], φ_init (20, 20).
 M2 N-flation axions (case 2): V = Σ Λ_i⁴(1 + cos(φ_i/f_i)), log10 Λ = (-2.6, -2.6), log10 f = (1.0, 1.2), φ_init (8, 12).
Janus-MF gets V, grad and the exact Hessian of the same potentials; same φ_init; pivot exits 55 e-folds before ε = 1 (as JMF2).
Claims (same tolerances as JMF2): C1 |n_s^J − n_s^MMC| ≤ 2e-4; C2 |r/r_MMC − 1| ≤ 2e-3, for each model.
All four → JANUS-MF VALIDATED BEYOND QUADRATIC; any fail → NOT (report which). A model where MMC or Janus gives no result is LISTED, not scored,
and the verdict is then PARTIAL. Wall limit 40 min for the whole job. Results: field_tests/results/janus_jmf3.txt (+ provenance stamp).
