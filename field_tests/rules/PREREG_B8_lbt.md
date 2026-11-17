# PREREG B8 — τ=i dark-radiation cases scored against the LBT 2026 Y_p and D/H with theory errors — locked 2026-11-17, before the run
Inputs as in B7: bbn_net.abundances(OMBH2, dNeff_init, 1.0), OMBH2 = serapis_inputs.OMBH2 = 0.02242. The B7 init values are reused, not re-solved:
- base: 0;
- U(1): 0.2069;
- SU(2): 0.6169;
- SU(2)+gaugino: 1.1533.
Check: ΔN_final must reproduce B7's 0.054 / 0.161 / 0.301 within 0.003.
Data (arXiv:2601.22239, D1191):
- Y_p = 0.2458 ± 0.0013 (Eq. 2), theory ± 0.0002 (Eq. 19);
- 10⁵ D/H = 2.513 ± 0.028 (Eq. 1), theory ± 0.083 (Eq. 20).
Errors combined in quadrature.
Verdict per case, taking the larger of |pull_Yp| and |pull_DH|:
- OK if < 2;
- TENSION if 2–3;
- EXCLUDED if > 3.
Also reported, not scored: the Y_p pull vs EMPRESS XV 0.2402 ± 0.0040.
