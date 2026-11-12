# E_G forecast for FLAG-1: frozen predictions for future lensing × galaxy-velocity measurements

**Status: LOCKED** on Danny's word ("Do that.", 12 Nov 2026, 13:02 CT, replying to "freeze FLAG-1's E_G predictions
now, as a dated, locked forecast"). AI-assisted. Time and fingerprint in the .sha256 file.

**Why.** FLAG-1's dark-matter fifth force raises E_G (lensing compared with galaxy motion) by about 3–5% above its
ΛCDM partner at 0.3 < z < 1.5 (MISSING-PIECE M2). Today's measurements (±17%) cannot tell them apart. Forecasts for
DESI × Simons Observatory reach about 2%. These numbers are frozen now so that the comparison cannot be tuned afterwards.

**Not blind.** Known at writing: ACT DR6 × BOSS E_G (Wenzl et al. 2024): CMASS z = 0.555, 0.31 (+0.06/−0.05); LOWZ
z = 0.316, 0.49 (+0.14/−0.11). M2 on those points: NO DISCRIMINATION (Δχ² +0.81). Weak-lensing surveys have tended to
find slightly less clumping than ΛCDM, which would go against FLAG-1; this was stated to Danny before the lock.

## Frozen numbers (no refit, ever, under this rule)
Method: E_G = Ω_m,eff(z)/f(z), with Ω_m,eff = (ρ_b + ρ_cdm)(z)·a³/ρ_crit,0 and f from the linear cb power at k = 0.02 Mpc⁻¹;
galaxies are taken to move with the dark matter. Fits: the same stored fits and ΛCDM partners as
`PREREG_LENSING_FORECASTS_FLAG1.md`. Full table with fingerprints: `field_tests/missing_piece/eg_frozen.json`
(code `freeze_eg.py`).

Pantheon+ (primary):

| z | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0 | 1.2 | 1.5 |
|---|---|---|---|---|---|---|---|---|---|---|
| FLAG-1 | 0.4688 | 0.4422 | 0.4209 | 0.4036 | 0.3895 | 0.3780 | 0.3684 | 0.3605 | 0.3482 | 0.3360 |
| ΛCDM | 0.4479 | 0.4219 | 0.4015 | 0.3854 | 0.3725 | 0.3620 | 0.3535 | 0.3465 | 0.3358 | 0.3252 |
| FLAG-1/ΛCDM − 1 | +4.7% | +4.8% | +4.8% | +4.7% | +4.6% | +4.4% | +4.2% | +4.0% | +3.7% | +3.3% |

The Dovekie and Union3 pairs give +2.7% to +5.2% (in the JSON). Values between the listed z are interpolated linearly.

## Scoring a future measurement
For a published E_G measurement (any lensing × velocity method) at redshift z with error σ (statistical and
systematic in quadrature, as the paper gives them; asymmetric errors used as in M2):
Δχ²_EG = χ²(FLAG-1) − χ²(ΛCDM), summed over its independent points, Pantheon+ numbers.
- **FLAG-1 SUPPORTED:** Δχ²_EG ≤ −4.
- **FLAG-1 RULED OUT AT THIS STRENGTH:** Δχ²_EG ≥ +4.
- **INCONCLUSIVE:** otherwise.
- If the measured value is below both models by more than 2σ, that is also reported: both miss, and FLAG-1 misses
  further.
- If the measurement's E_G definition (scale, estimator) differs enough that the method above does not apply, the score
  is NO VERDICT, with the reason, rather than an adapted prediction.
- Data already public at this lock (ACT DR6 × BOSS) are scored in M2 and are not forecasts.

## What may not happen
No refit and no change of numbers, method or bands after any measurement appears. Every qualifying measurement is
scored once and reported whatever it shows. Counted +1 in V7 per measurement scored.
