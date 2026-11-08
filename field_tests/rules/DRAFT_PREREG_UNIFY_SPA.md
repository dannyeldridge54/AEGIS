# DRAFT pre-registration UB-2s: the joined field on the combined CMB (ACT DR6 + SPT-3G), declared follow-up

**Status: DRAFT, not locked.** Declared in `PREREG_UNIFY_DATA.md` as the first follow-up. Written 7 Nov 2026 with AI
assistance, before any UB-2 result. Lock it (SHA-256 + timestamp, as `PREREG_UNIFY_SPA.md`) before it runs; the driver
`cmb-fit/ub2_spa_fit.py` refuses to run until then.

## Same as UB-2 except the CMB data
- Model, variant B, priors, engine (two-field CAMB module), thresholds: exactly `PREREG_UNIFY_DATA.md`.
- CMB: the `spa_` set of `cmbfit_compare.py` — Planck PR3 high-ℓ cut at the ACT overlap + ACT DR6 CMB-only + ACT DR6 ×
  Planck PR4 lensing + Planck low-ℓ + SPT-3G D1 TT/TE/EE lite (with ACT and SPT calibrations and priors as there).
  + DESI DR2 + one SN set (Pantheon+, DES-Dovekie, Union3).
- New references on the same data and engine: `lcdm_spa[_dovekie|_union3]`, `w0wa_spa[...]`; Locked Twist: `spa_edelock`
  (Pantheon+; the other two sets are run too, as `edelock` references, before the verdict is read).

## When it runs
Only if UB-2's verdict is MIXED, TIE or worse against ΛCDM, or DOES NOT UNIFY — or if Danny asks for it as a
confirmation of a pass. Either way it is reported beside UB-2, never instead of it.

## Open before locking
1. Run it whatever UB-2 shows (stronger), or only after a UB-2 shortfall (cheaper)? Recommended: whatever UB-2 shows.
