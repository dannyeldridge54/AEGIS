# KiDS-Legacy test: gate result and implementation notes (logged before any model-pair chi2)

## Gate (rule: reproduce KiDS-Legacy's own LCDM best-fit chi2 within 0.5), 8 Nov 2026 ~23:30 UTC
Data: KiDS_Legacy_cosmic_shear_data_release.tar.gz from kids.strw.leidenuniv.nl, SHA-256
7fdf214cbb54e51d5ca385d79a4590750d3c5dc9fe6803460bab8ed841c57f77. Their COSEBIs pipeline as released, except
the CosmoPower emulator replaced by CAMB with HMcode-2020 + baryon feedback (the model the emulator was trained on),
at the maximum-likelihood point of their public Nautilus chain: chi2 = 124.266 vs the chain's 124.291 (|diff| 0.025).
**G PASS.** Dependencies: 2pt_stats dcb101d, kcap 36b40c5, CosmoPipe efcce93, CSL as in the Part 2 runs.

## D1 (implementation, before any model pair): how the baseline nonlinear model is applied to our P(k)
- Our models' linear P(k) come from the stored CLASS files (same as Part 2). KiDS's baseline nonlinear model
  (HMcode-2020 with feedback, free logT_AGN) is applied as a boost: P_nl = P_lin(model) x [P_nl/P_lin] from CAMB at the
  model's omega_b, today's omega_cdm, h, n_s, sigma8 (A_s rescaled) and CPL (w0, wa) (LCDM: -1, 0). For LCDM this
  equals CAMB's own HMcode to 0.2% at z = 0 (1% at z = 1, the CLASS/CAMB linear difference, the same on both sides).
- The pyhmx (HMx library) route was tried first and rejected: its HMcode-2020 feedback mode differed from CAMB's by
  5-12% at k = 3-10 h/Mpc.
- Speed: the boost is computed on a logT_AGN grid 7.3-8.3, step 0.05, and ln P interpolated linearly in between.
- S8-L pair: both sides use the stored axionHMcode (basic + BAO damping) nonlinear power, which has no baryon
  feedback; logT_AGN is fixed at 8.0 on both sides (the limitation the rule anticipates).
- Equal effort exactly as Part 2: Nelder-Mead (tol 1e-3, maxiter 6000) from KiDS's starting values, then up to 3
  rounds of restarts from each side's own best and from the partner's best, stopping when neither improves by > 0.05.
