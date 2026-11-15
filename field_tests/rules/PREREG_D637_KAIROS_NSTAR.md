# PREREG D637: Kairos at the paper's reheating N* (referee R8 major issue 3)
Locked before computation, 2026-11-15. Script: theory/modular/kairos_nstar_d637.py (functions copied verbatim from exact_ns_d588.py by reading lines 1–42 of that file; no edits). Output: field_tests/results/kairos_nstar_d637.txt.
- Model: ε = 0 (HS-Kairos plateau, p = 2), exact Mukhanov–Sasaki as D588 (n_s from k·e^{±0.05}).
- N* values: 46.08, 47.60, 49.21 — the D602 bracket endpoints and middle for the nearest computed tilt (ε = 1e-4); the ε-dependence of N* in D602 is < 0.05 e-folds, so this is the Sec. 6 history. Labelled as such.
- Report n_s, r, y*, and distances to CMB-SPA (0.9684 ± 0.0030) and SPA+DESI (0.9728 ± 0.0027), plus to the paper's CMB value 0.9682 ± 0.0032 and CMB+DESI 0.9728 ± 0.0029 (arXiv:2512.10613).
- Use: these replace the Kairos numbers in the paper (abstract, Sec. 4, Fig. 2 caption if affected). Kairos is a reference face, not a frozen prediction, so no lock is changed. No reruns; fixes via PREREG_D637_DEVIATIONS.md written first.
