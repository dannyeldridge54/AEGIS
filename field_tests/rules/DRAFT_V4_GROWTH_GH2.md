# V4 #9: GH-2, no-refit growth and expansion check of the current fits (DRAFT, not locked)

**Status: DRAFT** (9 Nov 2026, V4 check-in). Nothing computed against data. Same statistic and verdict words as the
locked GH rule (`PREREGISTRATION_GROWTH_HZ.md`, 2 Nov, NEUTRAL for the older fits); only the models and one dataset
are new.

## Data
1. **H(z):** the 15 Moresco cosmic-chronometer points with the full covariance, exactly the frozen file of the GH rule
   (`growth_hz_data.json`, fetched 2 Nov). Independent of everything in our fits.
2. **fσ8, SDSS:** the six eBOSS/SDSS RSD-only values (Alam et al. 2021, Table III), diagonal, as GH.
3. **fσ8, DESI DR1 full shape (new):** DESI 2024 V (arXiv:2411.12021), §7.1 compressed values, tracers BGS 0.295,
   LRG1 0.510, LRG2 0.706, LRG3 0.919, ELG2 1.317, QSO 1.491 (ELG1 excluded by DESI). **Before lock:** copy the
   table (values, errors, and whether it quotes fσ8 or fσ_s8) into a frozen data file with its SHA-256. Caveat stated:
   same galaxies as the DESI DR2 BAO in our fits; the correlation is ignored. DESI DR2 full shape is not public.

## Models (stored best fits, no refit) and ΛCDM references
| Label | Fit | ΛCDM reference |
|---|---|---|
| Spiral | `ax_spa_spiraltwist{,_dovekie,_union3}_nlfix` | `ax_spa_lcdm_halofit{,_dovekie,_union3}` |
| S8-J | `ax_spa_spiraltwist{...}_nlfix_s8y6` | `ax_spa_lcdm_halofit{...}_s8y6` (best of the `_more` tries) |
| S8-L | `spiralL{,_dovekie,_union3}` | `ax_spa_lcdm_halofit{...}` |

Each model is rebuilt exactly as `theory/forward_predictions_cloud.py` builds it. Mirror gate: σ8 of the rebuild equals
the stored σ8 within 1e-3, or no verdict for that fit. S8-L's fσ8 omits the ultralight share (caveat S8-LNL D2); its fσ8
rows are reported with that caveat and its H(z) rows are unaffected.

## Statistic and verdict (as GH)
χ²_H = rᵀC⁻¹r with each model's own H0; χ²_f = Σ(Δfσ8/σ)² per fσ8 dataset. Δ = χ²(model) − χ²(ΛCDM ref).
Per model and dataset: **SUPPORTS** Δ ≤ −2; **NEUTRAL** −2 < Δ < +2; **DISFAVOURS** Δ ≥ +2. A model's verdict for a
dataset holds if 2 of 3 SN sets agree; otherwise MIXED. Δ_H + Δ_f is reported beside. Adds 3 models × 3 datasets to
the V7 look-elsewhere count.

## Blindness, stated
The chronometer and SDSS data were used in GH on older fits, not on these; the DESI DR1 values are public. No one has
computed these numbers for these fits. Not blind to the data's existence.

## Cost
Cloud only, about 10 minutes (9 rebuilds). **PC time: none.**
