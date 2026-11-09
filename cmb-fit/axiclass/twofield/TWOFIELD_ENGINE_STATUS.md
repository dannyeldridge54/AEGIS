# Two-field Twist (early boost + flagship late dilaton in one model): engine status 9 Nov 2026

Goal: one model with the Locked Twist's early field (n = 3, f_EDE, z_c tied to z_eq, θ_i free) AND the flagship's late
dilaton (κ = 1, dark-matter coupling β_eff, DES Y6 S8 term), to see whether H0 rises without losing the lensing fit.
No rule drafted or locked; no data touched.

## Route tried first (cheap): early field as AxiCLASS's pheno_axion fluid, dilaton as the scalar field
Runs in one CLASS call (the dilaton takes the closure, the fluid takes fraction_fld_ac). **Cross-engine gate G-2F1
FAILS** (`twofield_g2f1_cloud.json`): at the stored Locked Twist best fit (ΛCDM part identical, no dilaton), the fluid
version vs CAMB's full EarlyQuintessence field differs by 4.5% rms in C_l^TT and 8.7% rms in C_l^EE (ℓ 30–2500);
the same comparison for plain ΛCDM agrees to 0.2% rms, so the engines agree and the fluid approximation is what fails.
Cause (known in the EDE literature): the fluid description is poor for a field started near the top of its potential
(θ_i ≈ 2.77, strongly anharmonic). So this route is not usable for fits.

## Routes that would work
1. **Second scalar field in AxiCLASS** (the coupled-dilaton build plus a full n = 3 axion field): new background and
   perturbation equations, initial conditions and shooting for two fields. Gates: (i) with the early field off it
   reproduces the flagship χ² within 0.1; (ii) with the dilaton frozen it reproduces CAMB's Locked Twist C_l within
   0.3% rms. Cost: engine work in the cloud (the largest single engine job so far), then 3 PC fits.
2. **CAMB two-field module** (`cmb-fit/ub2_camb`, already validated for UB-2): runs both fields fully, but CAMB has no
   dark-matter coupling, so the flagship's β would have to be dropped. Cheaper, but it would test "EDE + exponential
   quintessence", not the Twist's coupled model. Not recommended as the main test.

Recommendation: route 1, after the V6 evidence and S8-A results are in (so one engine job at a time).
