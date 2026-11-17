# PREREG J10 — Janus vs exact Mukhanov–Sasaki over the J7b model set at NEW pivots N* = 45, 55, 65 (PC job)
Locked 2026-11-17 before any J10 number. Models: the 16 J7b models (indices 1–17 except 9, built by j7b_wide.build). Exact reference exactly as J7b
(ms.spectra_fast, dlnk 9 points on [−1, 1], bd = 1000 — the R0-checked configuration). Janus: core.spectra3. 48 points.
Absolute-accuracy claims (no ASPIC; Janus vs exact only): C1 median |Δn_s| ≤ 1e-5 and max ≤ 1e-4; C2 median |Δr/r| ≤ 1e-3; C3 median |Δα_s| ≤ 1e-5.
All three → JANUS ACCURACY HOLDS AT NEW PIVOTS; else report which failed. Runs on Danny's PC via the AEGIS PC runner; code copied unchanged from this
commit. Results: field_tests/results/janus_j10_nstar.txt (+ part file), copied back to the repo.
