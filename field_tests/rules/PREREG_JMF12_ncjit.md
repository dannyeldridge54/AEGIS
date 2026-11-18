# PREREG JMF12 — compiled Janus-MF-NC (curved field space, numba) vs spectra_nc
Locked 2026-11-17 18:45 CT before the equivalence run (one probe on DoubleQuadNC while writing: n_s 0.925024083, 0.69 s after compile).
Code: tools/janus_calc/mfms_nc_jit.py (same equations as tools/janus_calc/mfms_nc.py; compiled DP5(4), rtol 1e-11, bd 1000).
Cases: (a) DoubleQuadNC exactly as JMF9 (p = (0.002M², 0.004M², 1), M = 5e-7, G = diag(1, sin²φ1), start (0.4, 26), PyTransport slow-roll velocity);
(b) flat metric DQuad Q3 (m² = 1e-11, 9e-11, start (12, 12), slow-roll velocity −∇V/V as JMF9's self-check); (c) a second sphere radius: G = diag(R², R² sin²φ1) with R = 2,
same potential and start as (a).
Reference: tools/janus_calc/mfms_nc.spectra_nc on the same inputs. N* = 55, 9 k on ±0.4.
Claim K1: |Δn_s| ≤ 1e-6 on all three cases AND median speed-up ≥ 20× (compile excluded). Pass → adopted as the curved-space PC default ("nc-jit"); fail → not adopted.
