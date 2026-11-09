# S8-A engine (coupling on the ultralight angle, picture B): status 9 Nov 2026

Code: `patch_angle.py` (5 edits to a copy of AxiCLASS_coupled_nlfix_ula), `build_angle.sh`, gates `angle_gates.py`.
Equations: see the patch docstring (B = √(2/3)(1 − w), exact for a field whose mass runs as e^(√(2/3)φ)).
No rule drafted or locked yet; no data touched.

| Gate | Test | Result |
|---|---|---|
| G-A0 | coupling 0 reproduces the S8-L build at the stored S8-L point | **PASS** (all differences exactly 0) |
| G-A1 | heavy angle (99% of dark matter) coupled at β = 0.05 vs cold dark matter coupled at 0.05 | **PASS**: effect on the lensing potential C_l^φφ (ℓ 100–1000) −0.2252% vs −0.2244% (ratio 1.004); H0 and φ(today) effects agree to 4e-5 and 2e-5 |

**Gate change, stated plainly.** The first G-A1 compared σ8 and "failed" (fluid 82–87% of the CDM σ8 shift; a 2.5% σ8 gap
even uncoupled). Cause found: CLASS builds δ_m from baryons + CDM only and leaves the pheno_axion fluid out
(perturbations.c, delta_rho_m; the known S8-LNL D2 caveat), so with 99% of the dark matter in the fluid σ8 tracked the
baryons. The gate was redefined on the lensing potential, which counts all matter, after seeing that result; no rule
was locked for the engine gates, and the first version stays in the git history (commit before this one).

Not trusted until G-A1 passes (report only): at the stored S8-L point, moving the coupling onto the angle gives
σ8 0.8039 → 0.7976 and H0 67.90 → 67.47 (CLASS's Ω_m label in the coupled builds is known to be wrong; S8 from it is not used).

Next (engine, cloud): add an option that puts the fluid into δ_m, so σ8 / S8 / fσ8 count the angle (fixes the D2
caveat for S8-L too); then a DRAFT rule (S8-A), then the build on the PC and fits after Danny's lock.
