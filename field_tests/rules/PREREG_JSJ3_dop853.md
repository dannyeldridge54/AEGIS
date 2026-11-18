# PREREG JSJ3 — janus-jit with a compiled DOP853 background (coefficients from scipy), per-model speed vs ASPIC
Locked 2026-11-17 20:05 CT before the run. Probes while writing (3 models): DOP853 needs ~700 steps vs ~2500 for DP5(4) at the same rtol 1e-12; build ~0.4 ms,
point ~0.09 ms (min of 30); n_s differs from DP5(4) janus-jit by ≤ 3e-10. Single-sample timings on this shared machine are noisy, so timing is now median of 10 repeats.
Code: tools/janus_calc/core_jit.build8 (DOP853 tableau and error norm as scipy's DOP853, coefficients imported from scipy.integrate._ivp.dop853_coefficients; rtol 1e-12, atol 1e-14).
Points and comparisons as JSJ1/JSJ2 (16 J7m points; core.spectra3 reference; exact = ms-jit). ASPIC timing: j7m_aspic, (best of 5 wall − best of 5 process start)/24 per point.
Claims: JS1 as before (≤ 1e-7 n_s/α_s, ≤ 1e-6 r/r vs core; median vs exact unchanged within 1e-7);
JS3 per point (median of 10) janus-jit8 ≤ ASPIC per point; JS4 per model (build + 2 points, medians of 10) janus-jit8 ≤ ASPIC per model (2 points).
Verdict: JS1 → build8 becomes the janus-jit default; JS3/JS4 reported as FASTER / NOT faster than ASPIC, per point and per model.
