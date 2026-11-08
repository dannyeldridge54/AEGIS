# Ready board (8 Nov 2026, 15:20 CT)

One line per item: what it waits on. "Ready" means code tested and predictions frozen; nothing is fitted or tuned
when the data arrive. Ledger rebuilt 8 Nov: 51 locked files, 0 hash problems; 73 verdicts (17 failures on record).

## Running now
| Item | Where | Waits on |
|---|---|---|
| S8-LNL: S8-L lensing with axionHMcode (locked 8 Nov, D1–D4 logged) | cloud | run finishing (~1–2 h) |
| Bracket round 2 (9 fits) | PC | Danny double-clicks `cmb-fit/START_BRACKET_R2.bat` |
| Gaia stream download for V3 | PC collector | ESA rate limits (HTTP 429); retries daily on its own |
| Release watch (DESI DR3, Euclid DR1, Gaia DR4, SO) | PC collector, daily | new papers (Gaia DR4 hits so far are pre-release papers) |

## Ready, waiting for new data
| Step | Data | When expected | Ready? |
|---|---|---|---|
| V1 DESI DR3 BAO | DESI DR3 | not public as of 8 Nov | predictions frozen: `theory/PREDICTIONS_FROZEN_8NOV.md` (all 4 models × 3 SN sets). Scoring rule: **needs a lock** |
| V2 Euclid / Rubin, lab nulls | Euclid DR1 cosmology | mid-2027 | S8, fσ8, w(z) frozen; nulls list in V2 (lock on Danny's word) |
| V4 growth, clusters | DESI / Euclid fσ8 | 2027 | fσ8(z) frozen |
| V4 #5 r, n_s | Simons Observatory / LiteBIRD | 2027+ | locked 2 Nov (kill line r < 0.002) |

## Can run on data we have now, but needs a rule locked first
| Step | Why it waits |
|---|---|
| V3 dark matter vs stars (Sgr, GD-1) | stream download incomplete + membership/scoring rule not locked |
| V6 posteriors and Bayesian evidence | thresholds rule not locked; PC chains (days) |
| V7 look-elsewhere for the Spiral family | counting rule not locked (cheap, cloud) |
| POWER_N n = 1 on AxiCLASS | engine check + lock (DRAFT_POWER_N1_AXICLASS.md) |

## Known caveats carried forward
- S8-L σ8 / S8 / fσ8 omit the ultralight field (S8-LNL D2); BAO, H0, r_d, w(z) unaffected.
- Spiral family vs ΛCDM BAO differences are ≤ 0.7%; DR3 must be combined across bins and with SNe to separate them.
