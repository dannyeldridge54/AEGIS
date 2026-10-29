# AEGIS UFE v2 — Torsion-Born EDE engine (reference implementation)

Drop-in replacement for the v1 "UFE" cosmology physics on branch
`dannyeldridge54-ufe-model-comparison-engine`. Read `AEGIS_UFE_v2_Copilot_Brief.pdf` first.

| File | Purpose |
| --- | --- |
| `aegis/cosmo_v2.py` | Models (ΛCDM, legacy β with flatness fixed, full Barbero–Immirzi torsion field), sound horizon, distances |
| `aegis/data_v2.py` | DESI DR2 BAO, Planck θ*, ω_b prior, SH0ES and Local Distance Network H0 |
| `aegis/likelihood_v2.py` | CMB θ* + DESI DR2 BAO (correlated) + Pantheon+ (full cov, analytic M) + optional local H0 |
| `run_v2.py` | Fits all three models with and without the SH0ES prior; writes `results_v2.json` |
| `tests/test_v2.py` | 8 acceptance tests |
| `data/pantheon/pantheon_binned_fullcov.json` | Pantheon+ 40-bin full-covariance data (copied from the repo) |

```
pip install numpy scipy
python tests/test_v2.py       # 8 PASS lines
python run_v2.py              # ~1 hour on a laptop; prints and saves the results
```
