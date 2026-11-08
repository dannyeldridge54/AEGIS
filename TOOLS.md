# Reusable tools from the AEGIS / Twist project

Each is usable outside the Twist. Status says how ready it is for someone else.

| Tool | What it does | For whom | Where | Status |
|---|---|---|---|---|
| AEGIS Method kit | Rule template, deviation template, SHA-256 lock + ledger verifier (stdlib) | Any researcher | `method/` | Ready |
| Pre-registration ledger builder | Re-verifies every locked rule and tabulates every verdict | Any project using the kit | `field_tests/ledger/build_ledger.py` | Ready (paths specific; generalise next) |
| Two-field dark-energy module for CAMB 2.0.5 | Evolves two coupled scalar fields' perturbations (synchronous gauge) from a tabulated background; λ = 0 limit matches EarlyQuintessence to 2×10⁻⁵ | Cosmologists testing multi-field dark energy | `cmb-fit/ub2_camb/` | Working; needs a README and a public patch |
| Coupled + ultralight-axion AxiCLASS build | Coupled dilaton–dark-matter quintessence plus an ultralight axion fraction (pheno_axion n = 1); two documented patches | Cosmologists | `cmb-fit/axiclass/coupled/`, `nlfix/`, `ula/` | Working; code-identity checked to 2×10⁻⁸ |
| DES Y3 cosmic-shear wrapper for arbitrary P(k) | Runs the full DES Y3 shear likelihood (CosmoSIS) on any model's matter power, with equal-effort nuisance minimisation | Anyone checking a model against weak lensing | `field_tests/S8_WL/part2/` | Working |
| Forward-prediction freezer | Turns stored best fits into locked BAO, w(z), fσ8, S8 predictions | Anyone pre-registering for DESI/Euclid | `theory/forward_predictions_cloud.py` | Working |
| Star mapper (AEGIS v2 monitor) | Resumable Gaia DR3 sweeps, anomaly scanning, live web view | Citizen science, astronomy education | `ufe-v2/` | Running daily |
| Validation collector | Gaia tidal-stream samples with row-cap splitting; daily arXiv release watch | Anyone tracking data releases | `ufe-v2/aegis/validation_collect.py` | Running |

Next for each "working" tool: a short README, a minimal example, and a licence line, so another person can use it
without asking us.
