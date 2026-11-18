# PREREG JMF10 — faster Janus-MF: vectorised k-modes (and a quick mode), equivalence vs spectra_mf
Locked 2026-11-17 18:15 CT before the equivalence run (a single timing probe on Q3 was done while writing the code: 15.5 s → 3.8 s, Δn_s 2e-8;
bd scan on Q3 only: bd 300 → 1.25 s).
New: tools/janus_calc/mfms.spectra_mf_fast — same equations as spectra_mf; all k-modes in one ODE, common start where the lowest k has k/aH = bd.
Models: the five JMF6 models (Q1, Q3, Q9, N2p, N1 — potentials, parameters and starts exactly as theory/janus/jmf6_pytransport.py), N* = 55, 9 k on ±0.4.
Claims (each on all 5 models):
 F1 (same accuracy): spectra_mf_fast(bd=1000) vs spectra_mf(bd=1000): |Δn_s| ≤ 1e-6 and |Δr/r| ≤ 1e-5; median speed-up ≥ 3×.
 F2 (quick mode): spectra_mf_fast(bd=300) vs spectra_mf(bd=1000): |Δn_s| ≤ 1e-6 and |Δr/r| ≤ 1e-5; median speed-up ≥ 8×.
Verdicts: F1 pass → fast becomes the default MF route for new locks; F2 pass → bd=300 allowed as "quick mode" in new locks (labelled). Fail → not adopted; no reruns to chase.
