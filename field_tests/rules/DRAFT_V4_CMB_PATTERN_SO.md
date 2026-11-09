# V4 #7: the Locked Twist's EE/TE pattern vs ΛCDM for Simons Observatory (DRAFT, not locked; pattern frozen)

**Status: DRAFT** (9 Nov 2026). The pattern is computed and frozen now; the scoring rule is not locked.

## Frozen prediction (computed 9 Nov, cloud)
- Spectra: CAMB (EarlyQuintessence n = 3 for the Locked Twist), lensed D_ℓ to ℓ = 4000, at the stored best fits
  `edelockP{,_dovekie,_union3}` and the same-data ΛCDM `lcdmP{,_dovekie,_union3}`. Gate: σ8 of each rebuild equals the
  stored value within 1e-4 (all 6 pass).
- Files: `theory/v4_cmb_spectra_frozen.json.gz` (uncompressed SHA-256 8fc87a9e5bdb7bfc616c20cc9c8696eeb8a859c9f56adbf3022c6ef1e4308f61),
  summary `theory/v4_cmb_pattern_frozen.json`; code `theory/v4_cmb_pattern.py`, `theory/v4_cmb_residuals.py`.
- Pattern (Twist − ΛCDM, mean fractional, ℓ bins 30–300 / 300–800 / 800–1500 / 1500–2500 / 2500–4000):

| SN set | EE | TE (where |TE| is not near zero) |
|---|---|---|
| Pantheon+ | −0.5 / −0.2 / −0.0 / +0.2 / +0.1 % | −0.5 / 0.0 / +0.2 / +0.1 / −0.4 % |
| DES-Dovekie | −0.3 / +0.0 / +0.2 / +0.4 / +0.1 % | −0.3 / +0.3 / +0.6 / +0.5 / −0.1 % |
| Union3 | −0.3 / −0.1 / +0.0 / +0.2 / −0.0 % | −0.3 / +0.1 / +0.5 / +0.2 / −0.4 % |

  Shape common to all three: a deficit at ℓ < 300 and a small excess at ℓ 800–2500, at the 0.2–0.6% level.
- **Rough SO reach** (white noise 6.2 μK-arcmin, 1.4′ beam, f_sky 0.4, Gaussian, no foregrounds, parameters fixed):
  EE 2.0–3.1σ, TE 2.2–2.5σ (TT 4.9–6.7σ). After marginalising parameters and foregrounds the real reach is lower.
  **Expected outcome on SO EE/TE alone: probably CANNOT TELL.** Stated now so a null is not a surprise.

## Rule (to lock)
When SO publishes an EE+TE likelihood: evaluate both stored fits on SO EE+TE only, cosmology fixed at each stored
minimum, SO nuisance parameters minimised for each side with equal effort. Δ = χ²(Twist) − χ²(ΛCDM).
**SUPPORTS** Δ ≤ −4; **DISFAVOURS** Δ ≥ +4; else **CANNOT TELL**; 2 of 3 SN sets, else MIXED. +1 in V7.

## PC time
None for the no-refit evaluation if the SO likelihood runs in Python (cloud, minutes). A full refit version would be a
separate rule.
