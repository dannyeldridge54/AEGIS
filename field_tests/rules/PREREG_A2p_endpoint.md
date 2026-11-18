# PREREG A2p: wino line+endpoint photon ratio (ESTIMATE, no pass bar)
- Formula: 2507.15937 Eqs. 2.6, 2.7, 2.9, 2.11, 2.12, 2.13 (alttext copy, D1335/D1336), n = 1.
  Photons in the window: line = 2(F0+F1)·S (δ term doubled, per paper), endpoint = ∫_{1−Δ}^{1} of the non-δ terms of Eq. 2.9 (common σ0·e^{−(4α/π)Lχ²} divided out).
- R(Δ) = 1 + endpoint/line. Inputs: (s00, s01) from tools/janus_astro/sommerfeld.py wino_s(M, v=1e-3); α_W = 0.0335 (module value; LL, no running); m_W = 80.4.
- Grid: M = 1.0, 1.25, 1.5, 2.9 TeV; Δ = 0.05, 0.10 (H.E.S.S.-like), 0.15.
- Sanity checks (must hold, else DEVIATIONS before any rerun): with α_W = 0 the solver gives s = (1, 0); R ≥ 1 everywhere; R rises with Δ.
- Label: ESTIMATE (LL only; NLL scale band ≈5% per 1808.08956; s_{0m} normalisation assumed equal to the paper's, both use the 1307.4082 potential). No pass bar: the result says how conservative the D1324 f_max (line-only) is.
- Script: field_tests/scripts/a2p_endpoint.py. Output: field_tests/results/a2p_endpoint.txt.
