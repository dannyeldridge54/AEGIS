# Validation data log (append as data arrives)

| Date | Item | What | Source |
|---|---|---|---|
| 2026-11-08 | V1 | DESI DR3 BAO not yet public | web search 8 Nov; theory audit 7 Nov |
| 2026-11-08 | V1/V2 | Euclid DR1: data tranche Nov 2026 (no cosmology), cosmology mid-2027 | telescoper.blog 16 Jun 2026 |
| 2026-11-08 | V2 | ESPRESSO Δα/α = 1.3 ± 1.3(stat) ± 0.4(sys) ppm, z = 1.1508; clocks (1.0 ± 1.1)e-18/yr | arXiv:2112.05819 |
| 2026-11-08 | V3 | Trailing tail enhanced if DM feels extra attraction (Sgr) | arXiv:astro-ph/0608095 |
| 2026-11-08 | V3 | β_KK < 0.2 (force ratio β²) from Sgr stream | arXiv:0807.4363 |
| 2026-11-08 | V4 | eRASS1 S8 = 0.86 ± 0.01, σ8 = 0.88 ± 0.02, Ω_m = 0.29 | arXiv:2402.08458 |
| 2026-11-08 | V4 | DES Y6 shear S8: NLA 0.798 (+0.014/−0.015), TATT 0.783 (+0.019/−0.015) | arXiv:2602.10065 |
| 2026-11-08 | V5 | Nieh–Yan instantons: −2K e^(−S) cos η | arXiv:1411.4793 |
| 2026-11-08 | V1 | Spiral (P+) forward numbers computed (test) | theory/fpc_ax_spa_spiraltwist_nlfix.json |
| 2026-11-08 | V1/V2/V4 | Frozen forward predictions for ΛCDM, Spiral, S8-J, S8-L (3 SN sets each) | theory/PREDICTIONS_FROZEN_8NOV.md |
| 2026-11-09 | V2 | Spiral dark-matter mass change since z=1100: -0.82 / -0.95 / -0.89 % (code says shrinks; 7 Nov audit said grows: open); S8-L step k_half ≈ 0.57 h/Mpc | theory/v2_frozen_numbers.json |

## 9 Nov 2026, 03:15 UTC: V3 check-in and KiDS rows
- theory/DM_COUPLING_PICTURE.md: the action couples only the BI angle (0.816); "all dark matter at β = 0.816 f" is the
  background stand-in (same expansion, different forces). At S8-L's fitted mass the angle is smooth on galaxy scales,
  so the action predicts β_KK ≈ 0 in streams; the locked V3 numbers (0.053–0.075) are the fits' picture A. Locked
  rule unchanged. Mass-change sign settled for the fitted models: shrinks (angle particles −14 to −16% under B).
- field_tests/rules/DRAFT_V3B_STREAM_TEST.md (draft): predictions per picture, published limits (best β_KK ≈ 0.2–0.3),
  test design. Not locked.
- KiDS-Legacy: S8-J Union3 Δ_KiDS −0.47 (S8-J passes 3 of 3); plain Spiral Pantheon+ +0.46 (passes).
- 9 Nov 2026 ~04:50 UTC: KiDS-Legacy full-shear test (PREREG_KIDS_LEGACY_SHEAR.md) complete, all 9 pairs. S8-J −0.41 / −0.26 / −0.47 PASSES; Spiral +0.46 / +0.57 / +1.15 PASSES; S8-L +6.80 / +7.98 / +7.81 OVER (no feedback on either side). Files in field_tests/S8_WL/results/kids/.
- 9 Nov 2026 07:30 UTC: SIMPLIFY-L scored (fits finished on the PC 8 Nov 22:37 CT): WINNER K2 κ = 1, margin 5.60; free-κ fits flagged not fully converged (P+, Dovekie). field_tests/results/simplify_late_score.json. Bracket round 3 (reported only): θ 2.777 F9 deep P-ACT χ² 2232.088 (locked 2231.776), S8-A 2432.117 (locked 2432.109), S8-B 2429.077.
- 9 Nov 2026 11:23 UTC (05:23 CT): PC started FLAG-1 (3 flagship fits, κ = 1 + DES Y6 S8) and V6 chains (Pantheon+: Spiral, S8-L, ΛCDM × 4 independent chains; Dovekie and Union3 queued after). Rules locked 07:38 UTC. GH2 (#9) stays a draft until the DESI DR1 full-shape table is copied. Log: cmb-fit/results/flagship_v6_log.txt on the PC.
