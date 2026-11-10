# Two-field Twist: early n = 3 field + the flagship's late dilaton in one model (TWOFIELD)

**Status: LOCKED** on Danny's word ("Get it goin", 9 Nov 2026, 23:29 CT). Drafted as `DRAFT_TWOFIELD.md`; the only edit at
lock is this status line and the smoke numbers below corrected to the stored file. AI-assisted. No two-field fit exists at
lock; the JOINT-SHEAR calibration (gate G-JS, second round) is running and its result is not known.

**Not blind, stated plainly.** Known at writing: the Locked Twist (early field alone, CAMB, Planck-lite data) gives
H0 ≈ 70.5; the flagship (FLAG-1) beats ΛCDM+S8 by 4.71 / 6.01 / 7.69 on the newer CMB set (Planck low-ℓ + ACT DR6 +
SPT-3G) but sits at H0 ≈ 67; S8-A missed both full-shear tests (LATE-BASE: flagship stays the base). A smoke run (no
refit) of both fields at the FLAG-1 point gave H0 71.5, σ8 0.785 (`tf_smoke_both.json`): that says only that the engine runs.

## Question
With the early field added to the flagship, does H0 rise while the fit to CMB + BAO + SN + S8 stays at least as good as
the flagship's, and does it pay for its three extra parameters?

## Model and engine (fixed)
- **FLAG-1 exactly** (`PREREG_FLAGSHIP.md`: S8-J setup, κ = 1, β_eff free, DES Y6 S8 term, CMB + DESI DR2 + one SN set,
  same priors, best of 4), on `AxiCLASS_twofield` with the dilaton carried by the second field "dil" (same equations).
- **Plus the early field** on AxiCLASS's own scalar field (n = 3, full Klein–Gordon, AxiCLASS's fluid switch after many
  oscillations): fraction_axion_ac ∈ [0.001, 0.3], log10_axion_ac ∈ [−4.3, −3.0], θ_i ∈ [0.1, 3.1] (the Locked Twist's
  ranges). z_c free (not tied to z_eq), as the stored Locked Twist.
- Starts: the FLAG-1 best fit for shared parameters; early field at f 0.08, log10 a_c −3.55, θ_i 2.8 (ref widths as above).
- Runs `TF`, `TF_dovekie`, `TF_union3` (3 fits, PC). Code `cmb-fit/axiclass/twofield/twofield_fit.py`.

## Gates
- Engine (done, cloud, `TWOFIELD_ENGINE_STATUS.md`): G-2F0 pass, G-2F3 pass (early field vs CAMB 0.23% / 0.19% rms),
  G-2F4 pass; G-2F2 failed as written on H0/σ8 by ~1e-3, traced to the flagship build's own closure (its reported H0 is
  0.108% above its actual H(z=0)); C_l agree to 6e-6.
- **G-TF-PC (before any fit):** early field off, at each FLAG-1 best fit, total χ² = stored FLAG-1 χ² within **0.15**.
  Stated in advance: the S8 term alone is expected to move by ≈ +0.08 because the new closure reports the true H0
  (cloud check: 3.823 vs 3.747 at the Pantheon+ point); everything else should agree to ≪ 0.05. Fail: no fits.

## Readings (per SN set; 2 of 3 decides)
- **vs FLAG-1:** Δ_F = χ²(TF) − χ²(FLAG-1, recomputed on this engine at its stored point, i.e. the G-TF-PC value).
  **EARLY FIELD EARNS ITS PLACE** if Δ_F ≤ −6 (2 per added parameter); **NOT WORTH IT** if Δ_F > −2;
  else **WEAK**.
- **vs ΛCDM+S8** (stored `ax_spa_lcdm_halofit{...}_s8y6`, lower restart, as FLAG-1): Δ ≤ −4 **SURVIVES**, else as FLAG-1.
- **H0 (reported against stated numbers, not a verdict):** H0 at each best fit next to FLAG-1's (≈ 67.1) and the
  Locked Twist's (70.5); "H0 RISES" is stated only if it is ≥ 1.0 km/s/Mpc above FLAG-1 on 2 of 3.
- Reported, not verdicts: exact f_EDE and z_c, θ_i, β_eff, S8; then (separate, cloud) the locked DES Y3 and KiDS-Legacy
  full-shear tests rerun at the TF best fits against the same ΛCDM partners (LATE-BASE method), so the lensing cost of
  the early field is known.

## What may not happen
No change of priors, data or parameter ranges after any result; failed fits are NO VERDICT for that set; no rerun to
chase a reading. Counted +1 in V7.

## PC time
Estimate: each step ~35 s (both fields, C_l to ℓ 9000 may be slower); 3 fits × best of 4 ≈ 1–3 days, as the S8-A fits.
