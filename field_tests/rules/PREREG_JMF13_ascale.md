# PREREG JMF13 — scale-factor normalisation fix for all Janus-MF codes (item 25 root cause)
Locked 2026-11-17 19:15 CT before running the fixed code.
Finding (diagnostic, I25 + debug, before this lock): PyTransport NC gives physical n_s at R = 1.5 (0.933687) and R = 2 (0.936712) where our NC codes gave −0.83 / 3.49,
so the fault was ours. Root cause found in the debug: modes are normalised with a = e^N; for long runs (N_* ≈ 114–121 at R ≥ 1.5) the mode amplitudes Q ~ u/a ~ 1e-50
fall far below the ODE absolute tolerance atol = 1e-30, so error control switches off and the modes are garbage (P_R ~ 1e53 scattered). R = 1 and the flat models
(N_* ≈ 25–30) were safe by luck. Same a = e^N appears in mfms.py, mf_jit.py, mfms_nc.py, mfms_nc_jit.py.
Fix (physics unchanged; comoving rescaling): a = e^(N − N_p) with k measured in the same units (k_p = H(N_p)), as the single-field reference ms.spectra_fast already does.
Claims:
 A1 (no change where it worked): Q3 flat model — spectra_mf, spectra_mf_fast, spectra_jit — each within 1e-7 of its own pre-fix value (JMF10/JMF11: 0.94547697,
    0.94547694, 0.94547694 rounded to 8 d.p.); NC R=1 (DoubleQuadNC start (0.4, 26)) python and nc-jit within 1e-7 of 0.92502415 / 0.92502408.
 A2 (fixed): NC python and nc-jit at R = 1.5 and R = 2 within 2e-4 of PyTransport (0.933687, 0.936712; field_tests/results/i25_pyt_radius.txt).
Both → the a-normalisation fix is adopted in all four codes; JMF9's VALIDATED scope extends to R = 1.5, 2; nc-jit adopted (curved-space PC default).
Note recorded: PyTransport's own n_s at R=1 moved 4e-5 between time grids (0.925023 vs 0.924982), so PyTransport comparisons stay at the 2e-4 level.
