# PREREG D355: does the Twist background tighten the neutrino-mass limit? (locked before running; Danny chose "Free-neutrino fit (PC)", 07:08 CT)

Locked 14 Nov 2026, ~07:15 CT. AI-assisted. Uses already-scored data (the NS-SPA set), so it is a SENSITIVITY, never counted as evidence.

Runs (PC, WSL, AxiCLASS + cobaya minimiser, same likelihoods, priors, builds and best_of as the stored fits):
- `ax_spa_lcdm_halofit_mnufree` and `ax_spa_spiraltwist_kappa0.8165_beta0_nlfix_mnufree`, made by the wrapper
  cmb-fit/axiclass/mnufree_d355.py, which calls early_late_spa.make(<base name>) unchanged and only replaces the fixed
  m_ncdm = 0.06 eV (one massive state) with a free parameter m_ncdm ∈ [0.001, 0.6] eV (ref 0.06 ± 0.02). Everything else is identical.
- The baselines are the stored minima with n_s free and m_ncdm = 0.06: cmp_ax_spa_lcdm_halofit.json and
  cmp_ax_spa_spiraltwist_kappa0.8165_beta0_nlfix.json (values in ns_spa.json: χ² 2404.1015 and 2405.554).

Statistic: P_X = χ²(X, m = 0.06) − χ²(X, m free) for each model, and D = P_PURE − P_LCDM.
Reading: TIGHTER if D > 1 (the Twist background penalises Σm_ν = 0.06 more than ΛCDM); SAME if |D| ≤ 1; LOOSER if D < −1. The best-fit m_ncdm
of each is also reported. A negative P (the free fit worse than the fixed one) means the minimiser failed; the run is then void and reported
as such (no rerun to chase).
No reruns; fixes go in PREREG_D355_MNU_FREE_DEVIATIONS.md, written before any rerun.
