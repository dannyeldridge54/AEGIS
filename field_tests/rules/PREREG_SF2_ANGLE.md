# SF2: does the Barbero–Immirzi angle matter in the Spiral Twist? (pre-registration)

**Locked:** 2026-11-07, at the time recorded in `PREREG_SF2_ANGLE.md.sha256` (UTC). Written by Claude at Danny's request
("set everything up"), **before any β = 0 Spiral fit exists** (no `cmp_ax_spa_spiraltwist_beta0*` file in any repository
or on the PC at lock time). AI-assisted.

## Why
SF (locked 2 Nov) scored **BEATS LCDM** and **COMPETITIVE** with w0–wa. The Spiral has two dark-energy settings: the
dilaton slope κ and the matter-like BI angle β_eff = 0.816 f. With β_eff = 0 the model is plain exponential
quintessence, which is not specific to the Twist. SF2 asks whether the BI-specific part, the angle, is what the data use.
Free fits gave β_eff = 0.042–0.049 (f = 5.2–5.9%), inside the Babu–Amendola bound and near their ±0.05 modes.

## Runs (same code, data, priors, halofit, best of 4 as SF; only β_eff fixed at 0, κ free)
| Sample | β = 0 run (new) | β free (stored, SF) |
|---|---|---|
| Union3 (run first) | `ax_spa_spiraltwist_beta0_union3_nlfix` | `ax_spa_spiraltwist_union3_nlfix` |
| Pantheon+ | `ax_spa_spiraltwist_beta0_nlfix` | `ax_spa_spiraltwist_nlfix` |
| DES-Dovekie | `ax_spa_spiraltwist_beta0_dovekie_nlfix` | `ax_spa_spiraltwist_dovekie_nlfix` |

DES Y5 is excluded, as in SF. The SF gate (κ = 0.05, β = 0 reproduces ΛCDM within 0.08) already covers β = 0.

## Measure and rule
D_s = χ²(β = 0) − χ²(β free) on sample s (one extra setting).
- **ANGLE NEEDED** if D_s ≥ 4 on at least 2 of 3 samples.
- **ANGLE NOT NEEDED** if D_s < 1 on at least 2 of 3 samples: the Spiral's gain is plain exponential quintessence.
- **WEAK** otherwise.
- Reported beside it (not the verdict): χ²(β = 0) − χ²(ΛCDM) and − χ²(w0–wa) per sample; the stored no-BAO and cold-restart
  (`_r4`) Spiral runs.
- A failed or non-finite run is NO VERDICT for that sample; any setting change is logged first. Look-elsewhere: one test.

## Expectation (not a rule)
Not predicted. The stored no-BAO runs (β drops to 0.017–0.045) suggest part of the gain is the DESI-driven late-time
preference that w0–wa also captures.
