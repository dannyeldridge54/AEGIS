# V4 #10: cluster counts as compressed S8 checks

**Status: LOCKED** on Danny's word (9 Nov 2026, 01:33 CT, "Start them"); time and fingerprint in the .sha256 file. Drafted 9 Nov (V4 check-in) and locked unchanged except this line. Nothing scored.

## Which data, and why compressed (searched 9 Nov)
| Survey | Paper | Result used | Public likelihood? |
|---|---|---|---|
| eROSITA eRASS1 (western hemisphere) | Ghirardini et al. 2024, arXiv:2402.08458 | S8 = 0.86 ± 0.01 (Ω_m 0.29 +0.01/−0.02, σ8 0.88 ± 0.02) | none found |
| SPT clusters + DES/HST weak-lensing masses | Bocquet et al. 2024, arXiv:2401.02075 | S8 = 0.795 ± 0.029 (Ω_m 0.286 ± 0.032, σ8 0.817 ± 0.026), clusters alone | not confirmed |

So both are used as Gaussian S8 compressions, like S8-WL Part 1, and **stated as compressions**: both are ΛCDM
inferences, and cluster counts depend on σ8(z) and Ω_m separately, so the compression is an approximation for models
whose growth history differs (most of all S8-L and the coupled fits). The two surveys disagree with each other by about
2σ; they are scored separately and never combined.

## Models (stored best fits, no refit)
Spiral, S8-J, S8-L (as DRAFT_V4_GROWTH_GH2), and the Locked Twist (`edelockP*`, reference `lcdmP*`). S8 in the
s8wl_score convention from the frozen `fpc_*.json` files; S8-L omits the ultralight share (D2).

## Statistic and verdict
Per survey: Δ = (S8_model − S8_obs)²/σ² − (S8_ΛCDM − S8_obs)²/σ². **SUPPORTS** Δ ≤ −2; **NEUTRAL** −2 < Δ < +2;
**DISFAVOURS** Δ ≥ +2; 2 of 3 SN sets, else MIXED. Adds 4 models × 2 surveys to V7.

## Blindness, stated plainly
Not blind: every input number is already public and the model S8 values are already frozen, so the outcome can be
read off before scoring. This is a consistency check, not a prediction, and is labelled so in the ledger.

## Upgrade path
If eRASS1 or SPT releases a likelihood, a new rule evaluates the stored fits in it (cloud, no refit) before any fit.

## Cost
Arithmetic on frozen numbers. **PC time: none.**
