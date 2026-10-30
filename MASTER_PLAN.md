# AEGIS / the Twist: master plan

Every step below gets its rule written down and hashed **before** it runs (the AEGIS method), and failures are
published beside passes. Steps are in order of impact for the effort. Times assume this PC (16 cores, CPU only).

## Phase 1: Make the existing result referee-proof (weeks 1–3)

| # | Step | Why a referee cares | How | Time | Done when |
|---|------|---------------------|-----|------|-----------|
| 1.1 | **MCMC posteriors** for ΛCDM, Locked Twist (2 settings) and Twist-1H (1 setting) on P-ACT + DESI DR2 + Pantheon+ | Best fits are not error bars; EDE has known prior-volume effects | Cobaya MCMC, 4 chains each, stop at Gelman–Rubin R−1 < 0.02 | 2–4 nights per model | Credible intervals for f_EDE, θ_i, H₀; triangle plots |
| 1.2 | **Profile likelihood in the divisor N** (N = 6 … 12) | Replaces "9 failed, 8 fits" with an honest curve | Minimise at fixed N on P-ACT and Planck | 2 nights | Δχ²(N) plot, with 9 marked |
| 1.3 | **Exact field solution** (AxiCLASS or CLASS scalar field) for the final fits | The fluid approximation is the first thing experts question | Re-run the best fits with the scalar-field code | 1–2 nights | Δχ² agrees with the fluid fits to within 0.5, or the difference is reported |
| 1.4 | **Full weak-lensing likelihood** instead of the S8 penalty (DES Y3 cosmic shear, and KiDS-Legacy) | Decides the tie properly | Cobaya external likelihoods | 2–3 nights | New pre-registered verdict: preferred, tie or noise |

**Decision point A:** if 1.1 and 1.4 together push the evidence below 1.5σ, say so on the front page and pause the
model. If it holds near 2–3σ, go on.

## Phase 2: Turn the fit into a prediction (months 1–3)

| # | Step | How | Done when |
|---|------|-----|-----------|
| 2.1 | **Derive the onset lock** from the field equations (the hold-and-release idea, `hypotheses/HOLD_RELEASE.md`) | Integrate the field with a matter-coupled trigger; check whether release lands at equality and θ_i ≈ 0.88π without tuning | Yes/no result written up either way |
| 2.2 | **Look for the 9**: is there a reason for F = √(3/2) M_Pl / 9 (field-space periodicity, a discrete symmetry, a loop factor)? | Pencil-and-paper plus a symbolic check; ask an expert | Derivation, or a stated "no derivation found" |
| 2.3 | **Publish predictions before the data**: the CMB TT/TE/EE spectra the fixed model predicts at ℓ = 2000–5000, and the matter power spectrum | CAMB/CLASS output at the best fit plus MCMC spread; hash and timestamp (OpenTimestamps) | Prediction files and plots, timestamped |

## Phase 3: Blind tests on new data (as data arrives)

| # | Data | Rule (to be written before) |
|---|------|------------------------------|
| 3.1 | **SPT-3G** public power spectra | Same Twist-1H, no retuning: Δχ² < −2 vs ΛCDM |
| 3.2 | **DESI DR3** BAO when released | Same models, same rules |
| 3.3 | **Simons Observatory** first spectra | The decisive test: at f_EDE ≈ 0.075 a real signal should reach roughly 4σ or more; if not seen, the model is excluded |

## Phase 4: The paper and the community

| # | Step | Done when |
|---|------|-----------|
| 4.1 | Figures: CMB residuals vs ΛCDM, f_EDE–θ_i contours, H₀ comparison, Δχ²(N) | 4–6 figures in the paper |
| 4.2 | Tighten the paper to the core story; move side results to appendices | Under 15 pages |
| 4.3 | Send the outreach email (Smith, Poulin, OU, Yunes): one at a time, a week apart | One expert reply |
| 4.4 | **arXiv endorsement** in astro-ph.CO, then submit | arXiv ID |
| 4.5 | New Zenodo version after each phase (the DOI family stays the same) | Versioned record |
| 4.6 | Journal submission (Physical Review D or JCAP) after arXiv feedback | Submitted |

## Phase 5: Hold the line on method
- Every new test: pre-registration file, hash, timestamp, then run.
- `CHECK_MY_WORK` updated to cover every new number.
- The claim wall keeps failures beside passes.

## Where things are tracked
- This file (public roadmap).
- The claim wall: `ufe-v2/method/claims.json`.
- Pre-registrations: `cmb-fit/PREREG*.md`.

*It is not a race or a game. It is a stage, and the stage is meant to be shared.*
