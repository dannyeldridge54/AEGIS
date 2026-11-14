# Deviations for PREREG_D355_MNU_FREE (written before any run)

D1 (07:20 CT, before running): the lock named the baseline files and run names wrongly. The χ² values it quotes (2404.1015, 2405.554) are
the right baselines, but they live in cmp_ax_spa_lcdm_halofit_s8y6.json (ΛCDM, n_s free) and cmp_ns_spa_pure_free.json (PURE, n_s free). The
NS-SPA set includes the DES Y6 S8 joint likelihood, added by ns_spa_fit.setup(). The wrapper therefore reuses ns_spa_fit.setup(model, fixed=False)
(identical likelihoods, priors, builds; best_of 4 as NS-SPA) and only frees m_ncdm. Run names: d355_pure_mnufree, d355_lcdm_mnufree.
Statistic, reading and void rule are unchanged.

D2 (07:58 CT, crash fix; no result had been produced): the PURE fit died at 07:52, ~10 min after start and with no Python traceback, while the
LCDM fit kept running in parallel. That is consistent with the process being killed (most likely memory: two coupled-build AxiCLASS fits at
OMP 4 each; the NS-SPA fits ran one at a time). Fix: rerun PURE alone, unchanged (same script, same settings), after the LCDM fit has
written cmp_d355_lcdm_mnufree.json, then score. Launcher Desktop\RUN_D355_PURE.bat → cmb-fit/axiclass/run_mnufree_d355_pure.sh. This is a
crash rerun of a fit that produced no result, not a rerun to change a result.
