# PREREG JMF11 — compiled Janus-MF (numba) vs spectra_mf
Locked 2026-11-17 18:35 CT before the equivalence run (probes on Q3 only while writing: rtol 1e-10 → Δn_s 1e-7, 0.23 s; rtol 1e-11 → 0.44 s;
tighter rtol converges to 0.94547695, i.e. spectra_mf itself carries ~2e-8).
Code: tools/janus_calc/mf_jit.py (same equations as spectra_mf/spectra_mf_fast; whole integration compiled; Dormand–Prince 5(4); potential from sympy).
Setting fixed: rtol 1e-11, bd 1000 ("jit"); reported only: bd 300 ("jit quick").
Models: the five JMF6/JMF10 models (Q1, Q3, Q9, N2p, N1), N* = 55, 9 k on ±0.4. Reference: spectra_mf (bd 1000).
Claim J1: |Δn_s| ≤ 1e-6 and |Δr/r| ≤ 1e-5 on all five, AND median speed-up ≥ 20× over spectra_mf (compile time excluded; reported separately).
Pass → mf_jit becomes the PC default for multi-field runs (labelled "jit"); fail → not adopted; no reruns to chase.
