# Watch list for the next data: the DESI–SDSS split (addendum to PREREG_PRED_DESI_DR3.md)

**Status: LOCKED** on Danny's word ("Can you add that to something that we're looking for in our next sets of data",
12 Nov 2026, 13:11 CT). AI-assisted. Adds watch items to the locked DESI DR3 predictions; changes nothing in that rule.
DESI DR3 cosmology results are not public at lock.

**What was seen (12 Nov 2026, informal look against the ΛCDM partner fit, before MISSING-PIECE M3).**
Percent offsets from the ΛCDM partner `cmp_ax_spa_lcdm_halofit_s8y6` (sha256 808f54eb49c9b1f3):
- Sideways distances D_M at z ≈ 0.7–1.3: DESI DR2 −0.9 to −1.0% (short); SDSS DR16 LRG z = 0.698 +2.9 ± 1.9% (long).
  The z ≈ 0.70 gap is 3.8% (about 1.8σ).
- Depth D_H at z ≈ 0.5–0.7 (faster expansion when short): DESI DR2 −3.1% at both 0.51 and 0.706; SDSS DR16 LRG −4.2%.
  Here the surveys agree.
- DESI DR2's z = 0.51 D_M runs long (+1.9 ± 1.3%), against the trend of the other DESI bins.

**FLAG-1 (primary fit, frozen in PREREG_PRED_DESI_DR3.md) relative to the same ΛCDM partner:** D_M −0.44% (0.706),
−0.55% (0.934), −0.57% (1.321); D_H −1.16% (0.51), −1.10% (0.706).

## Watch items (scored once each when DESI DR3 BAO is public; each reported whatever it shows)
For each item: the DR3 points in the stated redshift range, their offsets from the ΛCDM partner computed at DR3's own
z_eff, and the generalised-least-squares mean offset m ± σ_m using DR3's covariance. FLAG-1's predicted mean f is
computed the same way from the frozen primary fit at the same z_eff.

- **W1, sideways distances short (0.6 ≤ z_eff ≤ 1.4, D_M only).**
- **W2, faster expansion (0.4 ≤ z_eff ≤ 0.8, D_H only).**

Readings for W1 and W2:
- **FLAG-1 DIRECTION CONFIRMED:** m < 0 by at least 2σ_m, and |m − f| ≤ 2σ_m.
- **OVERSHOOTS:** m < 0 by at least 2σ_m, but m is more than 2σ_m below f (the data go further than FLAG-1).
- **FADES TO ΛCDM:** |m| ≤ σ_m and |m − f| > 2σ_m.
- **UNCLEAR:** otherwise.

Reported only (no reading):
- **W3:** DR3's D_M at z ≈ 0.51, beside DR2's +1.9%.
- **W4:** D_M at z ≈ 0.7 from the next survey independent of DESI (Euclid BAO, or another), beside DESI's −0.9% and
  SDSS's +2.9%.
- The DR3 − DR2 shift of each W1/W2 point.

**Stated now:** DR3 contains the DR2 data, so persistence is partly expected; the shift (and W4) carries the new
information. Counted +2 in V7 (W1, W2).

## What may not happen
No change of the reference, the ranges, the method or the bands after any DR3 number is seen. No refit of FLAG-1.
