# LATE-BASE (S8-A full shear): implementation notes, written before any S8-A shear number

1. S8-A P(k): `part2/axiclass_pk.py` builds S8-A runs with `angle_fit.make` (angle-coupled build, CDM uncoupled,
   fld_in_delta_m = 1). Check: σ8 of the rebuild 0.80917 vs stored 0.80917 (Pantheon+).
2. axionHMcode component split (`nonlinear/axhm_pk.py`): for S8-A, CLASS's linear P(k) already counts the angle, so the
   reference transfer is total matter, weighted by the ACTUAL background densities at each z (the angle's mass runs,
   so ω_fld × a⁻³ is wrong for it). First try with ω weights: gate G2 = 2.5% (FAIL); with actual densities:
   G2 = 0.17% (PASS, limit 0.5%). The gate itself is unchanged.
3. Axion fraction given to axionHMcode for S8-A: the angle's share of the dark matter TODAY from CLASS's background
   (4.56% at the Pantheon+ point) instead of the early input share (5.43%), because the angle is ~16% lighter today.
   S8-L is unaffected (uncoupled: the two are equal).
