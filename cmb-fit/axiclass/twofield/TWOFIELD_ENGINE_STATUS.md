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

## Route 1 built (9–10 Nov): `AxiCLASS_twofield` (`patch_twofield.py`, `build_twofield.sh`)
Design choice: the **early n = 3 field uses AxiCLASS's own scalar field** (scf: full Klein–Gordon, its fluid switch
after many oscillations, its shooting), because that machinery is the tested part; the **late dilaton is the new second
field "dil"** (`dilaton = yes`, `dil_kappa`, `dil_beta`, `dil_phi_ini`), with the flagship's exact equations
(V = μ⁴e^(−κφ), CDM mass ∝ e^(β(φ−φ_ini)), Klein–Gordon background and synchronous-gauge perturbations, fifth force on
CDM). Closure: input leaves Λ as the closure; the background hands Λ's budget to dil and iterates μ⁴ until
ρ_tot(today) = H0² (rel. 1e-9). Late base = FLAG-1 (LATE-BASE result, 9 Nov). Synchronous gauge only.

Gates (cloud, no data; set by me when writing the scripts, not by a locked rule):
| Gate | What | Result |
|---|---|---|
| G-2F0 | dilaton off = AxiCLASS_coupled_nlfix at the FLAG-1 best fit (σ8, H0, C_l TT/EE/pp) | **PASS** (bit-identical) |
| G-2F2 | flagship dilaton moved from scf to dil (no early field): σ8, H0 ≤ 1e-4; C_l ≤ 1e-4 rms | **FAIL as written**: C_l agree to 6e-6 rms, but H0 differs by 1.08e-3 and σ8 by 7.5e-4 |
| G-2F3 | native scf n = 3 field (dil off) vs CAMB EarlyQuintessence at edelockP, exact f_EDE and z_c matched: ≤ 0.3% rms | **PASS**: TT 0.23%, EE 0.19% rms (ΛCDM engine agreement 0.22% / 0.17%; the fluid route gave 4.5% / 8.7%) |
| G-2F4 | both fields present (dil frozen, κ = 1e-6) = Λ closure at the same point: ≤ 1e-5 rms | **PASS** (5e-6) |
| smoke | both fields live (edelockP early field + FLAG-1 dilaton, no refit) | runs, finite, 34 s per C_l |

**G-2F2 diagnosis (checked, threshold not changed):** the flagship's own scf closure (CLASS shooting) leaves its actual
expansion today 0.108% below its H0 parameter (H(z=0)/H0 = 0.99892; Ω_scf 0.687453 vs wished 0.685972). The dil
closure is exact, and its H0 (67.086) equals the flagship's actual H(z=0) (67.159 × 0.99892 = 67.086). So the new
field reproduces the flagship's physics (C_l to 6e-6) and the difference is in how the flagship *reports* H0.
Consequence worth knowing: **stored FLAG-1 (and other scf-closure) H0 values are ~0.1% high** (≈ 0.07 km/s/Mpc);
χ² are unaffected (all observables use the integrated background). Reported, not corrected anywhere.

Parametrisation for fits: the early field's exact f_EDE and z_c are matched by an outer secant on AxiCLASS's shooting
targets (`tf_gates_ede.match`, ~4 background runs). A two-field fit wrapper and the rule (data, priors, verdicts,
equal-effort ΛCDM/flagship/Locked Twist references) come next; **no two-field fit runs before that rule is locked.**
Notes: AxiCLASS's `Omega_m()` is wrong in these builds (known quirk; S8 must be computed from ω's, as elsewhere).

**Correction (10 Nov 2026, TWOFIELD_DEVIATIONS.md D1):** G-2F2's C_l agreement (6e-6) was without the nonlinear
(HALOFIT) correction. With HALOFIT, the pre-fix build counted "dil" as matter in HALOFIT: nonlinear P(k) off by up to 79%,
lensed C_l off by ~8% rms. Fixed in `patch_twofield.py` (`halofit()`); after the fix, lensed C_l to l = 9000 agree with
the flagship to 4e-5 (TT) / 6e-6 (EE) / 9e-6 (phi-phi) rms, nonlinear P(k) to 2e-5.

