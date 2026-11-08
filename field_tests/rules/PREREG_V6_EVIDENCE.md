# V6: posteriors and Bayesian evidence, Spiral vs ΛCDM 

**Status: LOCKED** on Danny's word (8 Nov 2026: "we don't need the data in order to lock it and do it", after "Get everything going by yourself"). No chain had been run. Runs on the PC after bracket round 2 finishes, so the 9 fits are not slowed.

## Question
With full posteriors instead of best fits, how strongly do the data prefer the Spiral (and S8-L) over ΛCDM once the
volume of the extra parameters is paid for?

## Method (fixed when locked)
- Cobaya `mcmc`, same likelihoods, priors and builds as the stored fits (`ax_spa_spiraltwist_nlfix`, `spiralL`,
  `ax_spa_lcdm_halofit`), Pantheon+ first, then DES-Dovekie and Union3 if time allows.
- Convergence: Gelman–Rubin R − 1 < 0.02 on all parameters, 4 chains each. Chains that do not converge are reported as
  such, not read.
- Evidence: MCEvidence (Heavens et al. 2017) on the converged chains; cross-check with the Laplace approximation at
  the stored best fit. If the two differ by more than 1 in ln B, both are reported and no verdict is drawn.

## Readings (Jeffreys-type, on ln B = ln Z(model) − ln Z(ΛCDM))
|ln B| < 1 **INCONCLUSIVE**; 1–2.5 **WEAK**; 2.5–5 **MODERATE**; > 5 **STRONG**, in the direction of the sign.
Also reported: 1D posteriors of β, κ, ω_fld, and whether ΛCDM's values sit inside the 95% region.

## What may not happen
No prior widened or narrowed after seeing chains; priors are the ones in the stored fits.
