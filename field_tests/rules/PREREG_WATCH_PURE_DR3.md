# WATCH-PURE-DR3: the PURE-TWIST prediction for DESI DR3 (and the next independent BAO survey)

**Status: DRAFT**, written 12 Nov 2026 (~21:05 CT) during the theory work Danny asked for ("Keep developing it").
LOCKED only on Danny's word. AI-assisted.

**Why.** PURE-TWIST (κ = √(2/3), β = 0, no parameter beyond ΛCDM) was PREFERRED on 12 Nov 2026 (DESI DR2, SDSS,
Pantheon+, CMB distance priors). Its frozen predictions are in `field_tests/results/pure_twist_predictions.json`:
w0 = −0.900, wa = −0.143 (CPL fit to w(z) for z < 2); expansion 0.45–0.66% faster than ΛCDM at z = 0.5–1.3
(D_H/r_d), D_M/r_d +0.86% at z = 0.3. This rule fixes how new BAO data will be scored **before** they exist.

## Frozen now
Both models at their FULL best fits of 12 Nov 2026, **no refit**: PURE-TWIST (h 0.66922, ω_b 0.02250, ω_c 0.11622) and
ΛCDM (TOURNAMENT LCDM_FULL). Same code path as `tournament.py` (`bao_pred`).

## Readings (the first DESI release after DR2, with its published covariance; then the same for Euclid BAO)
- **D-PRED (decides):** Δχ² = χ²(PURE-TWIST) − χ²(ΛCDM) on the new BAO data alone.
  **SUPPORTED** if Δχ² ≤ −2; **DISFAVOURED** if Δχ² ≥ +2; **UNDECIDED** otherwise.
- **D-SIGN (reported):** at each z in 0.5–1.3, is the measured D_H/r_d below the ΛCDM prediction (the sign PURE-TWIST predicts)?
- **D-W (reported):** the release's own w0wa result vs (−0.900, −0.143).

## What may not happen
No refit of either model before scoring, no change of data cuts or bands after the data are public. Counted +1.

## Code
`field_tests/missing_piece/watch_pure_dr3.py` (after the lock and the data release).
