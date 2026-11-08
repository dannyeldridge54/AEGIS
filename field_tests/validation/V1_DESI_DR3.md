# V1 — DESI DR3 forward predictions (items #11, #2, #25, #17). Scheduled: 8 Nov 16:47 CT

**Goal:** lock the current model's numbers before DESI DR3 BAO is public.
**Status (8 Nov 09:45 CT):** prep done. DR3 BAO not published (search 8 Nov; theory audit 7 Nov: arXiv:2610.37664 is a
methods paper, not DR3). Code ready and tested: `theory/forward_predictions_cloud.py` (cloud, CLASS direct).
Test run `ax_spa_spiraltwist_nlfix`: H0 67.78, r_d 147.32, CPL w0 −0.917 / wa −0.132, min w −1.000, σ8 0.8193
(stored 0.8193, match), S8 0.8326, D_M/r_d(0.51) 13.302, D_H/r_d(0.51) 22.383.

## To do at 16:47
1. Re-check DR3 is still unpublished.
2. Run `forward_predictions_cloud.py` on: the 3 Spiral fits, the 3 S8-J joint fits (Spiral + ΛCDM, `_s8y6`, taking the
   better ΛCDM of `_s8y6`/`_s8y6_more`), the 3 ΛCDM halofit references, and S8-L if scored. One run per process.
3. Locked Twist (CAMB, `edelockP*`): BAO + r_d via `field_tests/S8_WL/part2/aegis_camb.py` settings (EarlyQuintessence).
4. Dark-matter coupling sign: theory audit F says the mass **grows** (dilaton rolls to larger χ); record β per fit.
5. Draft `rules/DRAFT_PREREG_PRED_DESI_DR3.md` with rules like PREDICTIONS_LOCKED_2026-11-02 D1–D3, plus:
   - #2 coupling: if DR3 + SN analyses fit a DM–DE interaction, Twist predicts β ≈ 0.04–0.05 with DM mass growing.
   - #17 neutrino mass: state the Twist's direction only if it can be computed (else record as a qualitative claim).
6. Ask Danny to lock.

## Data collected
- DESI DR2 BAO effective redshifts: 0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33 (in the script).
- Euclid DR1: first data tranche Nov 2026 (no cosmology); cosmology products mid-2027 (telescoper.blog, 16 Jun 2026).
