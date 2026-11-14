# Deviations for PREREG_D355_MNU_FREE (written before any run)

D1 (07:20 CT, before running): the lock named the baseline files and run names wrongly. The χ² values it quotes (2404.1015, 2405.554) are
the right baselines, but they live in cmp_ax_spa_lcdm_halofit_s8y6.json (ΛCDM, n_s free) and cmp_ns_spa_pure_free.json (PURE, n_s free). The
NS-SPA set includes the DES Y6 S8 joint likelihood, added by ns_spa_fit.setup(). The wrapper therefore reuses ns_spa_fit.setup(model, fixed=False)
(identical likelihoods, priors, builds; best_of 4 as NS-SPA) and only frees m_ncdm. Run names: d355_pure_mnufree, d355_lcdm_mnufree.
Statistic, reading and void rule are unchanged.
