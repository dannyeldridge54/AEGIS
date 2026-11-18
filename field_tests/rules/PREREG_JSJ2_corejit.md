# PREREG JSJ2 — janus-jit with the build fix (follows D1226)
Locked 2026-11-17 19:50 CT before the run. Change since JSJ1 (found by a timing probe, answers unchanged at rtol 1e-12): the background build allocated and
zeroed 200 000-row arrays each call (~2–3 ms fixed cost); now np.empty with doubling from 4 096 rows. Integration tolerances unchanged (rtol 1e-12, atol 1e-14).
Same points, claims and script logic as PREREG_JSJ1_corejit.md (JS1 same answers; JS2 median ×20 vs core; JS3 per point vs ASPIC), plus
JS4 (reported with its claim): per model (build + 2 points) janus-jit median vs ASPIC 2 points — FASTER or NOT.
Verdict: JS1 & JS2 → janus-jit adopted as the single-field default.
