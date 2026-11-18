# PREREG U2 — upgrade loop, counterpart 2: the SERAPIS pipeline (pipeline.predict) — fast path
Locked before building/running. Motivation: W1 (PREREG_W1_recompute) died on the cloud 30-min wall because pipeline.predict iterates the slow ms.spectra (~5 min per call) for the self-consistent N*.
Build: tools/serapis_calc/pipeline.predict_fast(model, C, TR, lam) — self-consistent N* with Janus core spectra3 r and the exact-end V*/V_end (same nstar.py, the NA2/TK1-D1 method), then ONE compiled ripple-free exact MS (U1b: build_spline, bd 4000, 9-pt ±0.1) at that N*. Returns the same keys as predict. predict is unchanged.
Tests:
 T1 equivalence vs TK1's recorded end-to-end rows (D1254/D1256, same method with the reference MS): T_R 6.6e8 C 1.0e-6 (N* 50.133, n_s 0.97172, r 4.5210e-4); T_R 2.0e10 C 1.15e-6 (N* 51.272, n_s 0.974380, r 4.56395e-4): |ΔN*| ≤ 0.002, |Δn_s| ≤ 1e-5, |Δr/r| ≤ 2e-4.
 T2 speed: ≤ 40 s per call including the potential build (old predict: ≥ 15 min).
 T3 α_s: |α_s(fast) − α_s(TK1 D3, U1b)| ≤ 5e-6 at the T_R 2.0e10 row.
Adopt (W1 rerun via DEV D1 uses it) only if T1–T2 PASS. Results: field_tests/results/u2_pipeline_fast.txt.
