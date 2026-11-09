# V4 — Growth (#9), clusters (#10), long-horizon numbers (#5, #7, #8). Scheduled: 11 Nov 09:43 CT

## #9 growth
- Existing: GH test (`P/PREREGISTRATION_GROWTH_HZ.md`, NEUTRAL for older fits) with data `cubemind/data/growth_hz_data.json`.
- Plan: rerun GH unchanged for the Spiral, S8-J, S8-L fits (fσ8(z) already produced by `forward_predictions_cloud.py`).
  Cheap, cloud. Add DESI DR1 full-shape fσ8 if a compressed table is public (DR2 full-shape not yet out; DR2 Lyα
  full-shape validation paper arXiv:2607.27411 exists).

## #10 clusters
- eRASS1 (Ghirardini et al. 2024, arXiv:2402.08458): Ω_m = 0.29 (+0.01/−0.02), σ8 = 0.88 ± 0.02, **S8 = 0.86 ± 0.01**.
  No public likelihood found yet → use as a compressed S8 Gaussian (like S8-WL Part 1), stated as a compression.
- Also eRASS1 structure growth from counts: arXiv:2410.09499.
- Twist values: Spiral S8 0.833–0.840 (SF), 0.826–0.827 (S8-J); ΛCDM ≈ 0.814–0.816.

## #5 r, n_s — locked 2 Nov (Q8): r = 0.0033–0.0048 (N = 50–60); kill line r < 0.002.
## #7 Locked Twist CMB pattern — compute EE/TE residuals vs ΛCDM from the stored spectra for Simons Observatory.
## #8 H0 — Locked Twist H0 from the stored fits (AxiCLASS SPA point: 70.39 in the 8 Nov smoke test).

## Status 9 Nov 04:40 UTC (V4 check-in): all five drafted, none locked
- #9 `rules/DRAFT_V4_GROWTH_GH2.md` (adds DESI DR1 full-shape fσ8; copy its table before lock). Cloud, ~10 min.
- #10 `rules/DRAFT_V4_CLUSTERS.md`: no public eRASS1 likelihood found; eRASS1 S8 0.86 ± 0.01 and SPT S8 0.795 ± 0.029
  as compressions, scored separately; not blind (labelled a consistency check).
- #5 `rules/DRAFT_V4_RNS.md`: adds r = 3(1 − n_s)² and an n_s kill line; notes the Locked Twist's own n_s 0.981 is
  already above Q8's 0.960–0.967.
- #7 `rules/DRAFT_V4_CMB_PATTERN_SO.md`: pattern frozen (`theory/v4_cmb_*`); EE/TE residuals 0.2–0.6%; rough SO reach
  2–3σ before marginalising → probably CANNOT TELL.
- #8 `rules/DRAFT_V4_H0.md`: Locked Twist 70.53–70.55 vs ΛCDM 68.24–68.32; scored per ladder family.
- PC time now: none. Later: #5 primary n_s needs 3 + 3 refits on SO data (~5 h each, parallel).
