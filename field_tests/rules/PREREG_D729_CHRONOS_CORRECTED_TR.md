# PREREG D729: two-term SERAPIS at τ = i (Chronos) at the corrected T_R
Locked 2026-11-16 before computing. Script: theory/modular/chronos_tr_d729.py (= eps_window_lowtr_d602.py with only the ε and T_R loops changed). Output: field_tests/results/chronos_tr_d729.txt.
## Inputs (fixed now)
ε ∈ {1.3e-4, 1.6e-4} (the frozen window); T_R ∈ {1e6, 3e6} GeV (D727: 1.0–3.0e6); w ∈ {3/5, 0} bracket; all other machinery as D602 (MS-shifted y*, D588 offset).
## Decision rule (written before running)
- Report N*, y*, n_s, r for each of the 8 rows.
- State for each row whether it lies inside the frozen τ = i band (n_s 0.970–0.975, r 4.8–5.7e-4) and inside y* ≤ 25.
- Frozen bands are NOT retuned. If any row leaves the band or y* > 25: record which part of the window the corrected history excludes (e.g. ε = 1.6e-4 out) as a correction, scored on future data as locked.
- Fixes only via D729_DEVIATIONS.md.
