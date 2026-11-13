LOCKED 2026-11-13 (time = lock commit) by the development driver under STANDING_LOCK_AUTHORITY.md

# PREREG_NS_SPA — how much does the CMB-SPA data dislike the Twist's n_s?

## Question
With ACT DR6 + SPT-3G + Planck low-l (the "SPA" CMB) + DESI DR2 + Pantheon+ + DES Y6 S8, the stored best fits prefer
n_s = 0.9732 (LCDM) and 0.9735 (FLAG-1). The Twist's inflation predicts 0.963-0.965 (PREREG_TWIST_INFLATION). Measure
the cost directly: refit with n_s fixed at 0.964 and compare with n_s free.

## Likelihood
early_late_spa.make(<base>) default SPA likelihood set (planck_2018_lowl.TT/EE, act_dr6_cmbonly.PlanckActCut,
act_dr6_cmbonly.ACTDR6CMBonly, act_dr6_lenslike.ACTDR6LensLike, spt3g_d1_tne_lite, DESI DR2 BAO, Pantheon+) plus
s8_joint_fit.add_s8 (DES Y6 S8) — the same set as the stored cmp_ax_spa_*_s8y6 fits.

## Fits (Cobaya minimize, best_of 4, starts at the stored SPA minimum)
- PURE free:  base ax_spa_spiraltwist_kappa0.8165_beta0_nlfix, n_s free.
- PURE fixed: same, n_s = 0.964.
- LCDM fixed: ax_spa_lcdm_halofit, n_s = 0.964.
- LCDM free: the stored cmp_ax_spa_lcdm_halofit_s8y6.json (chi2 2404.10, n_s 0.9732) — gate: recomputed chi2 at its
  minimum within 0.5 of the stored value.

## Readings (decided on PURE; LCDM reported beside it)
Cost C = chi2(PURE fixed) - chi2(PURE free).
- **CONSISTENT** if C <= 4 (within ~2 sigma).
- **TENSION** if 4 < C <= 9.
- **INCONSISTENT** if C > 9 (beyond ~3 sigma): the Twist's inflation and the SPA data disagree for the Twist's own
  late universe.
Also reported: n_s of PURE free; chi2(PURE free) - chi2(LCDM free).

## Failure handling
No reruns to chase results; corrections only in PREREG_NS_SPA_DEVIATIONS.md, written before any rerun.
