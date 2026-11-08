# S8-L lensing re-check with an ultralight-field nonlinear model (S8-LNL)

**Status: LOCKED** on Danny's word (8 Nov 2026: "Yes, lock it and run"); fingerprint and UTC time in
`PREREG_S8L_NONLINEAR.md.sha256`. Written at his request ("Fix lessening issues"). No DES Y3 shear number was computed
with the new model before the lock. G2 runs after the lock, before any shear χ².

## Why
S8-L Part 2 (8 Nov, reported) came out Δ_WL = +15.74 / +15.45 / +14.47, OVER. That run turned the linear power into the
nonlinear power with halofit, which is not calibrated for an ultralight-field (ULA) share. Measured symptom
(`field_tests/S8_WL/results/s8l_nonlinear_check.txt`): at k = 0.05–0.2 h/Mpc the S8-L and Spiral linear power agree to
within 2.4%, but halofit gives S8-L 6–21% more nonlinear power. The recorded OVER is **not** changed or replaced by this
test; both are reported side by side.

## Question
Does S8-L pass the locked Part 2 lensing rule (`PREREG_S8_WL.md` Part 2: Δ_WL ≤ +2 PASSES, else OVER) when the
nonlinear power of **both** models comes from a halo model built for mixed ultralight + cold dark matter?

## Method (fixed when locked)
- **Nonlinear model:** axionHMcode (Vogt et al. 2022; Dome et al. 2024 calibration, `version = 'dome'`, `alpha = True`,
  `concentration_param = True`, as its README recommends), with `eta_given = True`, `one_halo_damping = True`,
  `two_halo_damping = True`, `full_2h = False` (the HMcode-2020 set) on **both** sides, commit a85ba2679cba5abe68b4cfd1e49b7a52bdcda424, plus one patch
  (`field_tests/S8_WL/nonlinear/axionHMcode_bao_damping.patch`): the two-halo linear power is BAO-damped as in HMcode-2020
  (Mead et al. 2020 eqs. 14–16; `dewiggle.py`), the one piece of HMcode-2020 axionHMcode leaves out.
- **Both sides the same code:** S8-L at its stored best fits (cmp_spiralL*.json: ax fraction = omega_fld / (omega_fld +
  omega_cdm), mass from the stored log10_a_c as in spiral_l_score.py); ΛCDM at its stored best fits with ax fraction 0
  (the model then reduces to HMcode-2020). No cosmology is refitted; only the DES Y3 nuisance parameters are minimised,
  exactly as `run_part2.py` (same pairs, same equal effort, best of the same tries).
- **Linear input:** per-component linear power (CDM, baryons, ULA, total) from AxiCLASS at the stored points, same
  builds as the stored fits; σ8 must equal the stored value to 1e-5.
- **Redshifts:** the model is evaluated on a z grid of 0–3 (at least 30 points) and interpolated in z to the
  pipeline's grid. Outside its calibrated range (z < 1) it is used as is; this is stated as a limitation, not adjusted.

## Code gates (must pass before any shear χ² is computed)
- **G1:** ΛCDM (ax fraction 0) axionHMcode vs CAMB HMcode-2020 at the stored ΛCDM Pantheon+ point: |ratio − 1| ≤ 2%
  for 0.01 ≤ k ≤ 10 h/Mpc at z = 0, 0.5, 1.
- **G2:** S8-L linear total power from the component sum equals the stored pk_spiralL.npz linear power to 0.5%.
- A failed gate stops the test; the failure is reported, and fixing it is a logged deviation.

## Readings
Per SN set: Δ_WL = χ²_WL(S8-L) − χ²_WL(ΛCDM), PASSES if ≤ +2, else OVER. Overall: **LENSING FIXED (full shear)** if
PASSES on at least 2 of 3; **NOT FIXED** otherwise. The halofit result (+14 to +16) is quoted beside it.

## What this test cannot do
- It does not refit the cosmology with the new nonlinear model (the stored fits used halofit in CMB lensing; the
  effect there is small but not zero).
- It is one extra attempt at the lensing problem; that is counted in the ledger.

## Pre-lock gate log (code checks only, no survey data)
- 8 Nov, G1 try 1 (eta_given, two_halo_damping off): max deviation from CAMB HMcode-2020 21–24%. Those two switches are
  part of HMcode-2020, so the flag set above was changed to include them. Changed before the lock, logged here.
- 8 Nov, G1 try 2 (flag set above): max deviation 2.05% (z = 0), 1.59% (z = 0.5), 1.17% (z = 1), worst at
  k = 0.17 h/Mpc (the BAO-wiggle region). **Fails the 2% line by 0.05% at z = 0.** Not changed; Danny decides before the
  lock whether to keep 2% (then the cause is investigated first) or set another line. The same code is used on both
  sides, so a shared offset of this size largely cancels in Δ_WL; that is a reason, not a proof.
- Execution-only fix: numpy 2 renamed np.trapz; the gate script maps it to np.trapezoid (same function).
- 8 Nov, cause found (Danny chose "find the cause first"): with the trend removed, the smooth part of the ratio agrees to
  0.13%; the whole miss is BAO wiggles (±1.9%), because axionHMcode's two-halo term uses the undamped linear power while
  HMcode-2020 damps the wiggles. Fix: the patch above.
- 8 Nov, G1 try 3 (patch on): max deviation **0.12%** (z = 0), 0.08% (0.5), 0.06% (1). **G1 PASS** at the unchanged 2% line.
