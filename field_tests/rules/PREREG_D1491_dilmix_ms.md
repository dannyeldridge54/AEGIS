# PREREG D1491 — exact Mukhanov–Sasaki spot check of the DILMIX best strip point (help plan set 9)

Locked 2026-11-19 ~12:33 UTC before computing. Our own file and D-number; the point (α 0.375, C 1.5e-6) is NOT in the P3 chat's locked DILMIX grid
(α ∈ {0.25, 0.5, 0.75} × C ∈ {1.25e-6, 2.5e-6}), so this does not run its locked scan.
Method: the shared pipeline (tools/serapis_calc pipeline.predict, exact MS spectra, self-consistent N*, T_R 8.94e8) with the same DILMIX overrides
as its run.py (E_paper → E(τ,3/2); grid mapping P = α x/(1+x) + (1−α)[1 − 1/(1+x)²], e = P/(1−P); DILATON32 D1 start rule) — copied into our script.
Prediction under test (D1485 SR forecast): n_s 0.97126, r 5.288e-4, in band. AGREE if |Δn_s| ≤ 5e-4 and |Δr/r| ≤ 2 %; IN BAND if n_s ∈ [0.969, 0.975] and r ∈ [4.55, 5.7]e-4.
Fixes only via PREREG_D1491_DEVIATIONS.md first. No reruns to chase.
