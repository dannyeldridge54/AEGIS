# NS-PURE: does the Twist's own dark energy bring the CMB+DESI spectral index back to its inflation prediction?

**Status: DRAFT**, written 12 Nov 2026 (~21:50 CT) as step 1 of the plan Danny asked for ("Plan out all our next steps",
"Keep working on it"). LOCKED only on Danny's word. AI-assisted. PC (full CMB likelihoods), after V6 finishes.

**Why.** Twist inflation (α = 1) predicts n_s = 0.963–0.965. CMB alone agrees (Planck 0.9638 ± 0.0040), but adding DESI
BAO under ΛCDM pushes n_s up (Planck + DESI 0.9690 ± 0.0035; CMB-SPA + DESI 0.9737 ± 0.0025), and arXiv:2512.05108
attributes that shift to the BAO–CMB tension under ΛCDM. PURE-TWIST (κ = √(2/3), β = 0) changes the late universe, so it
may ease that tension and lower the inferred n_s. If it does not, the inflation prediction is in real trouble.

**Not blind.** Known at writing: the numbers above; PURE-TWIST PREFERRED on the compressed likelihood; the TWIST-INFLATION
prediction. Not known: any n_s from a PURE-TWIST full-CMB fit.

## Fits (frozen now)
The V6 setup exactly (`field_tests/selfcheck/v6_pr4_fit.py`: Planck PR4 CamSpec high-ℓ TTTEEE + Planck 2018 low-ℓ TT, EE
+ lensing + DESI DR2 BAO + Pantheon+ + DES Y6 S8), Cobaya minimizer, best_of 4, n_s free with the pipeline's own prior.
- ΛCDM (the V6 LCDM fit, reused if V6 has finished; else run identically).
- PURE-TWIST: engine `ax_spa_spiraltwist_kappa0.8165_beta0_nlfix` (κ = 0.8165 and β = 0 fixed, no extra parameter).

## Readings
- **Gate:** both setups evaluate to finite χ² at their starting points; the ΛCDM n_s lies within 0.005 of 0.969.
- **N1 (decides):** Δn_s = n_s(PURE-TWIST) − n_s(ΛCDM).
  **SUPPORTED** if Δn_s ≤ −0.003 and n_s(PURE-TWIST) ≤ 0.9705 (within 2σ, σ = 0.0035, of the 0.9635 prediction);
  **NOT SUPPORTED** if Δn_s > −0.001; **PARTIAL** otherwise.
- **N2 (reported):** Δχ² (PURE-TWIST − ΛCDM) on the same data, and its parts (CMB, BAO, SN).

## What may not happen
No change of data, priors, engines or bands after any number is computed. Counted +1.

## Code
`field_tests/selfcheck/ns_pure_fit.py` → `field_tests/results/ns_pure.json`; PC runner script `run_ns_pure_pc.sh`.
