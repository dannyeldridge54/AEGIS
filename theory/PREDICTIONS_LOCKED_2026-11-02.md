# Forward predictions, locked before the data exist (DESI DR3, Euclid, weak lensing, LiteBIRD, LISA/ET)

**Locked:** 2026-11-02 16:19:51
**Frozen numbers:** `forward_predictions.json` (computed 16:09–16:19 from the stored best fits by
`forward_predictions.py`; no data compared). Every rule below is scored mechanically when the named data are public.
**Tier:** these are model predictions. A pass is EVIDENCE for consistency, not proof.

## Frozen numbers (from the stored best fits; full grids in the JSON)

| Model (stored fit) | Rebuild offset | w0 / wa (CPL fit of w(z), 0 ≤ z ≤ 2.5) | min w(z) | σ8 | r_d (Mpc) |
|---|---|---|---|---|---|
| Late Twist, Pantheon+ (`gF0.4m-0.3_nlfix`) | 0.087 (known open item) | −0.988 / −0.016 | −1.000 | 0.811 | 147.54 |
| Late Twist, DES Y5 (`gF0m0.102_desy5_nlfix`) | 0.002 | −0.930 / −0.100 | −0.998 | 0.800 | 147.59 |
| Coupled Twist (`gF0.4m-0.1_nlfix`) | 0.005 | −0.956 / −0.065 | −1.000 | 0.824 | 147.32 |
| ΛCDM (halofit, Pantheon+) | 0.001 | −1 / 0 | −1 | 0.813 | 147.54 |
| w0–wa (Pantheon+), context | 0.019 | −0.862 / −0.513 | −1.247 | 0.813 | 147.33 |

**BAO (D_M/r_d, D_H/r_d) at the DESI DR2 effective redshifts:**

| z | Late Twist P+ | Late Twist DES Y5 | Coupled Twist | ΛCDM | w0–wa |
|---|---|---|---|---|---|
| 0.295 | 8.200 / 25.631 | 8.244 / 25.627 | 8.143 / 25.414 | 8.179 / 25.600 | 8.141 / 25.341 |
| 0.510 | 13.380 / 22.591 | 13.415 / 22.524 | 13.281 / 22.426 | 13.355 / 22.586 | 13.269 / 22.417 |
| 0.706 | 17.556 / 20.075 | 17.577 / 20.004 | 17.431 / 19.967 | 17.531 / 20.078 | 17.424 / 20.018 |
| 0.934 | 21.834 / 17.518 | 21.840 / 17.460 | 21.690 / 17.463 | 21.810 / 17.525 | 21.700 / 17.552 |
| 1.321 | 27.910 / 14.055 | 27.899 / 14.022 | 27.757 / 14.051 | 27.889 / 14.062 | 27.803 / 14.144 |
| 1.484 | 30.104 / 12.880 | 30.088 / 12.854 | 29.950 / 12.887 | 30.084 / 12.886 | 30.011 / 12.971 |
| 2.330 | 39.020 / 8.632 | 38.993 / 8.627 | 38.883 / 8.657 | 39.004 / 8.636 | 38.992 / 8.690 |

## Data-side rules

**D1. DESI DR3 BAO (no refit).**
- χ² of the published DR3 BAO values (with their covariance) against each frozen prediction above, interpolated in z
  from the JSON grid if DR3 uses other redshifts.
- Δ = χ²(model) − χ²(ΛCDM frozen). **PREFERRED** if Δ ≤ −4; **NEUTRAL** if −4 < Δ < +4; **DISFAVOURED** if Δ ≥ +4.
- Also reported: the same against the w0–wa frozen prediction.

**D2. Any w0–wa posterior from a combination with at least two independent supernova calibrations + BAO + CMB**
(e.g. DESI DR3 + Union3.1/DES-Dovekie, Euclid DR1).
- Each model's (w0, wa) point inside the 95% contour: **CONSISTENT**; outside: **EXCLUDED** (that fit).

**D3. True phantom.** Every Twist fit predicts w(z) ≥ −1 at all z (minimum −1.000, null energy condition). If such a
combination reconstructs w(z) < −1 in any redshift bin at more than 3σ **without** a w0–wa parametrisation, the minimal
and Coupled Twist are **EXCLUDED**. (The Spiral Twist is not covered; it can look phantom in w0–wa analyses.)

**D4. Weak-lensing S8** (Euclid DR1, Rubin LSST Y1, or the final KiDS/DES/HSC joint analysis).
- The Late Twist predicts S8 within 0.002 of ΛCDM, so lensing cannot separate them. The Coupled Twist predicts a higher
  S8 (0.828, S8_FIXED_CODE_RESULTS.md).
- If a survey gives S8 more than 3σ below 0.828, the Coupled Twist is **DISFAVOURED**.

**D5. CMB birefringence ratio** (LiteBIRD, Simons Observatory), only if a photon coupling exists (B4-X):
R = 0.997. **CONSISTENT** if |R_obs − 0.997| ≤ 2σ_obs; otherwise **EXCLUDED** for the B4-X coupling.

## Quantum-side rules (QUANTUM_PATH Q6, Q8)

**Q8. Inflation from the BI field's α = 1 geometry** (theory note, doi:10.5281/zenodo.23898709):
r = 12/N² = 0.0033–0.0048 for N = 50–60, with n_s = 1 − 2/N.
- If LiteBIRD (or BICEP/Keck + SO) gives r < 0.002 at 95%, α = 1 inflation from this geometry is **EXCLUDED**.
- If it detects r in 0.002–0.006, it is **CONSISTENT**.
- An n_s measurement that keeps 0.974 ± 0.002 strengthens the existing TENSION. The escape requires N ≥ 62.5, i.e. a
  stiffer-than-radiation reheating history.

**Q6. Parity-violating gravitational waves.** The minimal Twist's Nieh–Yan coupling gives a velocity-birefringence
scale of about 10⁻⁴³–10⁻⁴² GeV (NIEH_YAN_TWIST_DRAFT.md; LIGO–Virgo bound 6.5×10⁻⁴² GeV).
- A detection by LISA, ET or CE implying a scale above 10⁻⁴¹ GeV cannot come from the Twist coupling (**NOT THE TWIST**).
- A null result above 10⁻⁴² GeV is **CONSISTENT**.

## Housekeeping

- The DES Y5 Late Twist fit rests on a calibration-sensitive supernova offset (LOWZ_SPLIT_RESULTS.md). Its predictions
  are locked anyway, so the future data judge it directly.
- The Pantheon+ Late Twist fit carries a known rebuild offset (0.087). Its frozen numbers come from the rebuilt model,
  which is what is scored.
