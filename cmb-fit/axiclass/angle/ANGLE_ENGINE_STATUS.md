# S8-A engine (coupling on the ultralight angle, picture B): status 9 Nov 2026

Code: `patch_angle.py` (5 edits to a copy of AxiCLASS_coupled_nlfix_ula), `build_angle.sh`, gates `angle_gates.py`.
Equations: see the patch docstring (B = √(2/3)(1 − w), exact for a field whose mass runs as e^(√(2/3)φ)).
No rule drafted or locked yet; no data touched.

| Gate | Test | Result |
|---|---|---|
| G-A0 | coupling 0 reproduces the S8-L build at the stored S8-L point | **PASS** (all differences exactly 0) |
| background | heavy angle (99% of dark matter) coupled at β vs cold dark matter coupled at β: ΔH0 and Δφ(today) | **agree to 1e-4** (β = 0.05 and 0.1) |
| G-A1 | same, growth: σ8 shift from the coupling | **FAIL**: the fluid gets 87% (β = 0.05) and 82% (β = 0.1) of the cold-dark-matter σ8 shift |
| side finding | uncoupled heavy pheno_axion fluid vs cold dark matter | σ8 differs by 2.5% even with no coupling (AxiCLASS fluid property; touches S8-L only at the ~0.1% level, its share is 6%) |

Not trusted until G-A1 passes (report only): at the stored S8-L point, moving the coupling onto the angle gives
σ8 0.8039 → 0.7976 and H0 67.90 → 67.47 (CLASS's Ω_m label in the coupled builds is known to be wrong; S8 from it is not used).

Next (engine, cloud): find the 2.5% fluid-vs-CDM baseline gap first (initial conditions of the fluid perturbations,
the non-adiabatic c_s² − c_a² term), then re-test G-A1. Only then a rule (DRAFT) and PC fits.
