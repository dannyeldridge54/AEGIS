# V1: scoring the frozen forecasts against DESI DR3 BAO

**Status: LOCKED** on Danny's word (8 Nov 2026, "Get everything going by yourself"). Fingerprint and UTC time in
`PREREG_V1_DESI_DR3.md.sha256`. DESI DR3 BAO was not public at the lock (web search and release watch, 8 Nov).

## What is scored
The frozen forecasts in `theory/PREDICTIONS_FROZEN_8NOV.md` (files `theory/fpc_*.json`, SHA-256 listed there): ΛCDM,
Spiral, S8-J and S8-L, each at its three stored best fits (Pantheon+, DES-Dovekie, Union3). **No refit.** The numbers
are used exactly as frozen. If a DR3 redshift is not on the frozen grid, the forecast is recomputed at that redshift
from the same stored best fit with the same script (no parameter changes); this is logged.

## Data
DESI DR3 BAO as published (the collaboration's D_M/r_d, D_H/r_d, D_V/r_d and their full covariance), all tracers.
If DESI publishes several BAO-only data vectors, the one the DESI cosmology paper uses as its baseline is used.

## Statistic
For each model and SN set: χ²_DR3 = (d − t)ᵀ C⁻¹ (d − t), with t the frozen forecast.
Δ = χ²_DR3(model) − χ²_DR3(ΛCDM, same SN set).

## Readings (per model)
- **FAVOURED by DR3** if Δ ≤ −4 on at least 2 of 3 SN sets.
- **DISFAVOURED by DR3** if Δ ≥ +4 on at least 2 of 3 SN sets.
- **NO PREFERENCE** otherwise.
Also reported, not a verdict: χ²_DR3 per data point for every model (goodness of fit), and the DR3 w0–wa contour (if
DESI publishes one) against each model's frozen CPL (w0, wa).

## Code gate
Before scoring: the same code must reproduce DESI DR2 BAO χ² for the stored ΛCDM Pantheon+ fit within 0.5 of a
direct calculation with the published DR2 data vector and covariance.

## What may not happen
No refit, no change to the forecasts, no choice of SN set after seeing DR3, no change of thresholds. Refits on DR3 are a
separate test with their own rule. Failures are reported at full size.
