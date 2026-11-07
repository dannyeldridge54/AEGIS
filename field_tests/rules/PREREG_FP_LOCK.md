# FP-L: the Fingerprint test in the UFE (Locked Twist) form (pre-registration)

**Locked:** 2026-11-07, at the time recorded in `PREREG_FP_LOCK.md.sha256` (UTC), at Danny's request ("update them with
it"), **before any locked-onset Fingerprint or cosine fit exists** (no `cmp_fp_*_lock` file anywhere at lock time).
Companion to FP (`cmb-fit/axiclass/torsion_shape/PREREGISTRATION_SINH.md`, locked 26 Oct), which stays as written.

## What changes from FP
Only the onset: z_c is **locked to matter–radiation equality**, a_c = ω_r/(ω_b + ω_c), exactly as in the UFE v2 paper
(Zenodo doi:10.5281/zenodo.23847152) and every Locked Twist fit (`early_late_spa.py` LOCK). Free settings: f_EDE, θ_i.
Same code (Fingerprint build, gate `fp_regress.json` passed), same data (Planck 2018 low-ℓ TT, EE, plik-lite TTTEEE,
lensing + DESI DR2 BAO + Pantheon+, no SH0ES), same priors, best of 4, x₀ = 2.1445 fixed.

## Runs
`fp_cosine_lock` (plain cosine = Nieh–Yan) and `fp_sinh_lock` (Fingerprint = Holst).

## Rule (the FP thresholds, unchanged)
Δ = χ²_eff(sinh) − χ²_eff(cosine), χ²_eff = χ² + ((A_planck − 1)/0.0025)².
- Δ < −2: the data prefer the torsion (sinh) shape: favours Holst.
- −2 ≤ Δ ≤ +2: the data cannot tell the shapes apart yet.
- Δ > +2: the data disfavour the periodic-in-γ shape: favours Nieh–Yan.
A failed or non-finite run is NO VERDICT. Look-elsewhere: FP and FP-L together are two readings of one question.
