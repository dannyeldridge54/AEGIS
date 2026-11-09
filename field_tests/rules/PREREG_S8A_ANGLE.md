# Pre-registration S8-A: the light angle carries the coupling, as the action says (picture B)

**Locked:** 9 Nov 2026, time in `PREREG_S8A_ANGLE.md.sha256` (UTC), on Danny's word ("Take best route ... just start
all process testing", 10:30 CT, after the engine report). AI-assisted. No S8-A fit exists at lock.

**Not blind, stated plainly.** Known at lock: S8-L (coupling on the cold dark matter) beats ΛCDM but its lensing is
NOT FIXED (S8-LNL, DES Y3) and OVER on KiDS-Legacy; the engine report (cloud, no data) shows that at S8-L's stored
point, moving the coupling onto the angle lowers σ8 by about 0.5% (0.8038 → 0.7996, angle counted) and H0 by 0.4.

## Question
The action (theory/DM_COUPLING_PICTURE.md) says only the BI angle's mass runs with the dilaton, at strength √(2/3), and
the rest of the dark matter is blind to it. S8-L coded the reverse. With the coupling where the action puts it, does
the Spiral still beat ΛCDM, and does its lensing improve?

## Model (fixed)
- S8-L exactly (PREREG_SPIRAL_L.md: same data, priors, settings, κ free, log10 a_c ∈ [−6, −3.5], Θ_i = 0.1, n = 1,
  best of 4), with one change: the cold dark matter is uncoupled; the angle share f = β_eff/√(2/3) carries the coupling
  with strength **√(2/3) fixed** (mass ∝ e^(√(2/3)φ); energy exchange √(2/3)(1 − w)ρ φ', exact for a field whose mass
  runs that way). β_eff keeps the prior [0, 0.12]. Same parameter count as S8-L.
- σ8, S8 and fσ8 count the angle (`fld_in_delta_m = 1`), so the S8-L caveat D2 does not apply.
- Engine: `cmb-fit/axiclass/angle/` (patch_angle.py on a copy of the S8-L build; cloud gates G-A0, G-A1, G-A3
  passed 9 Nov, `angle_gates.json`, including one gate redefined after its first result, stated in
  ANGLE_ENGINE_STATUS.md). Fitter `angle_fit.py`; runs `S8A`, `S8A_dovekie`, `S8A_union3` (PC).

## Gate (before any fit)
G-A-PC: on the PC build, with the angle coupling off, the fitter reproduces each stored S8-L χ² within 0.1
(`python angle_fit.py gate_pc` → results/s8a_gate_pc.json). If it fails: no fits, no verdict.

## Verdicts (per SN set)
- **Against ΛCDM** (stored `ax_spa_lcdm_halofit*`): BEATS if Δχ² ≤ −4 on at least 2 of 3; TIE if none ≤ −4 and none ≥ +2;
  otherwise MIXED.
- **Lensing:** DES Y6 S8 penalty vs ΛCDM at the best fit, as S8-WL Part 1 (P ≤ 2 passes). LENSING FIXED if P ≤ 2 on
  2 of 3 and BEATS; TRADE-OFF if P ≤ 2 on 2 of 3 but not BEATS; NOT FIXED otherwise.
- **Reported, not verdicts:** χ²(S8-A) − χ²(S8-L) (same parameter count); f, mass in eV, S8, H0; φ(today) shift and the
  angle's mass change since z = 1100. Full-shear reruns (DES Y3, KiDS-Legacy) at the best fits are a separate step.
- **Stream prediction (V3):** under this model the angle is smooth on galaxy scales at the fitted mass, so the
  predicted dark-matter-only force in streams is β_KK ≈ 0 (recorded, scored only by a future rule).
- A failed or non-finite fit is NO VERDICT for that set; any settings change is logged first. +1 in V7.
