# PREREG JSJ1 — compiled single-field Janus ("janus-jit") vs core.spectra3, and timing vs ASPIC
Locked 2026-11-17 19:35 CT before the equivalence run (probes on one TI model while writing: Δn_s 2e-10; build 4–5 ms, 0.08 ms per point after compile).
Code: tools/janus_calc/core_jit.py — same equations and pivot convention as core.Model/spectra3; background by compiled DP5(4) (rtol 1e-12, atol 1e-14);
ε-flow from the same 41-point uniform grid with not-a-knot cubic-spline slopes solved in compiled code (replaces scipy CubicSpline; same spline definition).
Points: the 16 scored J7m comparisons (TI ×6, SFI p=3 ×2, N* = 50, 60), models and starts from j7m_grid.build. Exact reference: ms-jit (D1225) with J7b settings.
Claims:
 JS1 (same answers): |Δn_s|, |Δα_s| ≤ 1e-7 and |Δr/r| ≤ 1e-6 vs core.spectra3 on all 16; and accuracy vs exact unchanged (median |Δn_s| within 1e-7 of core's).
 JS2 (speed vs core): median (build + 2 points) time ratio core/jit ≥ 20× (compile excluded).
 JS3 (speed vs ASPIC, reported with the claim): median per-point time of janus-jit ≤ ASPIC's per-point time on the same 12 parameter points
     (ASPIC: j7m_aspic wall time minus process start, divided by 24; best of 5).
Verdict: JS1 & JS2 → janus-jit adopted as the single-field default; JS3 reported as stated (faster or not than ASPIC per point; per-model including the build also reported).
