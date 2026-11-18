<!-- AEGIS-FP BSQ5AGS2BX6UJJEB · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# SERAPIS v3 — reproducibility

Every number in the paper comes from a script in `theory/modular/`. Each script was locked by a PREREG file (with a sha256 hash and a git commit) before it was run. See `papers/v3/MANIFEST.md`.

## Environment
Python 3.13; package versions are in `requirements.txt`. No GPU is needed. Each script runs in seconds to a few minutes on a laptop.

## One command per result
| Paper result | Command (from repo root) | Expected output |
|---|---|---|
| τ = i derivation checks (Sec. 2–3) | `python3 theory/modular/tau_i_d574.py` | field_tests/results/tau_i_d574.txt |
| Two-term model (Sec. 3) | `python3 theory/modular/two_term_d575.py` | two_term_d575_rerun.txt |
| Species mass term (Sec. 7) | `python3 theory/modular/species_mass_d577.py` | species_mass_d577_rerun.txt |
| N* history (Sec. 6) | `python3 theory/modular/osc_nstar_d578.py` | osc_nstar_d578.txt |
| Exact Mukhanov–Sasaki n_s, r (Sec. 4) | `python3 theory/modular/exact_ns_d588.py` | exact_ns_d588.txt |
| ε window at low T_R (Sec. 4) | `python3 theory/modular/eps_window_lowtr_d602.py` | eps_window_lowtr_d602.txt |
| Running α_s (Sec. 4) | `python3 theory/modular/running_d632.py` | running_d632.txt |
| Janus relation (Sec. 5) | `python3 theory/modular/janus_analytic_d635.py` | janus_analytic_d635.txt |
| Axion two-field δN (Sec. 7) | `python3 theory/modular/two_field_dn_d587.py` | two_field_dn_d587.txt |
| Dilaton suppression (Sec. 7) | `python3 theory/modular/adiabatic_y_d592.py` / `_d594.py` | adiabatic_y_d592.txt / _d594.txt |
| Stiff-phase growth (Sec. 6) | `python3 theory/modular/stiff_growth_d595.py` | stiff_growth_d595.txt |
| SERAPIS-ρ (Sec. 9) | `python3 theory/modular/serapis_rho_d610.py`, `rho_nstar_d613.py`, `rho_running_d634.py` | matching results files |
| Proton parity at i / ρ (Sec. 7) | `python3 theory/modular/vacuum_i_selection_d551.py`, `vacuum_rho_selection_d612.py` | matching results files |
| SERAPIS-E frozen band (Sec. SERAPIS-E) | `python3 theory/modular/serapis_e_exact_d692.py` | serapis_e_exact_d692.txt |
| τ = i corrected reheating band (D815) | `python3 theory/modular/chronos_ms_d815.py` | chronos_ms_d815.txt |
| ρ Affleck–Dine window (v3.2, D895) | `python3 theory/modular/ad_rho_d895.py` | ad_rho_d895.txt |
| ρ lepton-sector lift ε (v3.2, D896) | `python3 theory/modular/rho_osc_d896.py` | rho_osc_d896.txt |
| τ = i Affleck–Dine window at corrected T_R (v3.2, D900) | `python3 theory/modular/ad_tau_i_d900.py` | ad_tau_i_d900.txt |

## Reproduction check (2026-11-15)
Three key scripts were re-run from a clean state. Their outputs were byte-identical to the stored results (blank lines ignored):
exact_ns_d588 (5.0 s), eps_window_lowtr_d602 (0.9 s), janus_analytic_d635 (9.2 s). The fresh outputs are in `out/`.

## Integrity
- Locks: `field_tests/rules/PREREG_*.md` + `.sha256`, committed before each run.
- Fixes: `*_DEVIATIONS.md`, each written before its rerun. Superseded outputs are kept, not deleted.
- AI assistance: the code and drafts were written with Claude (Anthropic). The author directed the work and checked the results.

## Reproduction check of the published v3.2 archive (2026-11-16, D913)
The Zenodo v3.2 reproducibility zip (md5 6a57f8c68ca101aa76354a1146dd6d3c) was unpacked into a clean directory and all 22 scripts above were run there (python3, same versions). 21 outputs are byte-identical to the stored results (blank lines ignored). The 22nd, chronos_ms_d815, is identical in every physics line; the stored file also carries four timing lines from the original run's wrapper (`real/user/sys`, `EXIT 0`). Summary: `out/RP_v3.2_SUMMARY.txt`; fresh outputs of the v3.2 rows: `out/*_rp.txt`. Total run time about 3 minutes.
