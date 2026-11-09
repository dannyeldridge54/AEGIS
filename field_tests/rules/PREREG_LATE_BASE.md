# Which late model is the base? S8-A full-shear tests and the base choice (LATE-BASE)

**Locked:** 9 Nov 2026, time in `PREREG_LATE_BASE.md.sha256` (UTC), on Danny's word ("Set this up", 15:36 CT, after the
plan: finish S8-A properly, then combine). AI-assisted. No S8-A full-shear number exists at lock.

**Known at lock, stated.** S8-A beats ΛCDM by 10.4 / 13.9 / 15.1 and passes the compressed DES Y6 S8 test 3 of 3
(PREREG_S8A_ANGLE.md). S8-L passed that compressed test too and then failed both full-shear tests (S8-LNL DES Y3:
+2.65 / +3.21 / +2.57; KiDS-Legacy: +6.80 / +7.98 / +7.81). The flagship (FLAG-1) passes ΛCDM+S8 3 of 3; its own
full-shear reruns are not run.

## Part 1: S8-A full-shear tests (methods fixed by earlier locked rules, unchanged)
- **DES Y3 shear:** exactly as PREREG_S8L_NONLINEAR.md (axionHMcode basic + HMcode-2020 BAO damping on both sides,
  same flags, z grid, equal-effort minimisation over the shear nuisances, gate G2 ≤ 0.5%), pairs
  `S8A{,_dovekie,_union3}_axhm` vs the stored ΛCDM `ax_spa_lcdm_halofit{...}_axhm`. Δ_WL ≤ +2 passes.
- **KiDS-Legacy COSEBIs:** exactly as PREREG_KIDS_LEGACY_SHEAR.md and its S8-L treatment (same axionHMcode P(k) files,
  same settings), pairs `S8A{...}` vs the same ΛCDM partners. Δ_KiDS ≤ +2 passes.
- The only code change: the S8-A P(k) comes from the angle-coupled build (`fld_coupling_beta = √(2/3)`,
  `fld_in_delta_m = 1`, so CLASS's linear matter power already counts the angle; the component split for
  axionHMcode uses total matter as the reference). Gate G2 applies unchanged.
- Readings per survey: PASSES if ≤ +2 on at least 2 of 3; OVER otherwise. NO VERDICT for a set whose gate fails.

## Part 2: the base for the two-field model
- **S8-A becomes the late base** if it PASSES on at least one survey and is not OVER on both.
- **Otherwise the flagship (FLAG-1) stays the base.**
- The two-field model (early n = 3 field + the chosen late base, one engine) is then specified in its own rule,
  written and locked before any two-field fit. Nothing in this rule fixes its verdicts.
- Counted in V7: +1 (S8-A full shear); the base choice itself is a selection and is reported as such.
