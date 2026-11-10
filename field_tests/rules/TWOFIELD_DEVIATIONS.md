# PREREG_TWOFIELD.md — deviation log

Logged before any rerun. The locked rule itself is not edited. AI-assisted.

## D1 (10 Nov 2026, ~00:30 CT) — engine bug in HALOFIT; gate G-TF-PC rerun once after the fix

**What happened.** G-TF-PC failed on the PC (`cmb-fit/results/tf_gate_pc_try1.json`). With the early field off, total
χ² came out 0.909 / 0.845 / 0.838 *below* the stored FLAG-1 values (tolerance 0.15). Per the rule, no fits ran.

**Diagnosis** (`tf_gate_diag.json`, no fit):
- The flagship's own build reproduces the stored χ² at the stored points (|Δ| ≤ 0.013 per set).
- The two-field build matches it on Planck low-ℓ, BAO and SN. S8 shifts by +0.06 to +0.11, as the rule stated in advance.
- The miss is in the small-scale CMB terms: ACT DR6 CMB-only about −0.71, SPT-3G about −0.18, ACT lensing and
  PlanckActCut a few hundredths.

**Cause.** The flagship build (`AxiCLASS_coupled_nlfix`) has an "nl-scf-fix" in `external/Halofit/halofit.c`. It makes
HALOFIT treat the scalar-field dilaton as dark energy rather than as ρ − 3p matter, in Ω_m, Ω_v, w and f_ν. In the
two-field build the dilaton lives in the new field "dil". That field is added to Ω_m as ρ − 3p, the same as scf, but
HALOFIT was never told about it. So HALOFIT counted the dilaton as matter.

The effect in the cloud, at the FLAG-1 Pantheon+ point, two-field vs flagship:
- nonlinear P(k, z = 0) off by up to 79%;
- lensed C_l (ℓ 30–9000) off by 8% / 7% / 10% rms (TT / EE / φφ).

The engine gate G-2F2 missed this because its C_l check (6e-6 rms) did not run through the nonlinear correction.

**Fix** (`patch_twofield.py`, function `halofit()`): "dil" gets the same HALOFIT treatment as the flagship's scf. That
means it is subtracted from Ω_m (also at z = 0 for f_ν), added to Ω_v, and added to the effective w (fields + Λ). The
change is gated on `has_dil`, so with `dilaton = no` the code is unchanged.

Cloud check after the fix, at the same point:
- lensed C_l agree with the flagship to 4.1e-5 / 6.4e-6 / 8.7e-6 rms (TT / EE / φφ);
- nonlinear P(k) agrees to 2e-5;
- σ8 and h are unchanged by the fix (linear quantities).

**What changes.**
- The engine is brought to the locked spec: "FLAG-1 exactly … dilaton carried by the second field 'dil' (same equations)".
- G-TF-PC is rerun once, with the same tolerance (0.15), the same stored references and the same expected S8 shift.
- If it passes, the 3 fits run as locked. If it fails again: no fits, NO VERDICT, and no further engine changes under
  this rule.
- Nothing else changes: model, priors, ranges, data, thresholds and readings are all as locked.

Danny asked for the fix ("Fix", 9 Nov 2026, 23:48 CT) after the failed gate was reported to him; the cause was found after that.

**D1 addendum (10 Nov 2026, 00:20 CT): build-script fix only.** The first PC rebuild stopped before changing any file.
The PC's flagship build follows the git patch `0001-nl-scf-fix`, so its HALOFIT computes f_ν with the plain `Omega0_m`.
The cloud build is the later `patch_nlfix.py`, which also takes the field out of f_ν. To match the PC flagship exactly,
the f_ν line is now left as it is in such a build; the dark-energy changes to Ω_m, Ω_v and w are applied as before.
Tested on a copy of that HALOFIT version: it patches and compiles. No gate had been rerun at this point.
