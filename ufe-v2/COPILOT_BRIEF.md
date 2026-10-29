---
title: "AEGIS UFE v2 — Engineering Brief for GitHub Copilot"
subtitle: "Replace the v1 torsion model with the Torsion-Born EDE field, fix the physics bugs, update the survey data"
author: "Prepared for Danny Eldridge · October 26, 2026"
geometry: margin=0.9in
fontsize: 10pt
---

# 0. How to use this brief

You are working in the repository `dannyeldridge54/AEGIS`, branch
**`dannyeldridge54-ufe-model-comparison-engine`** (the cosmology engine; `master` is the
general-purpose optimizer and has no cosmology model). Work on a new branch
`ufe-v2-torsion-field`.

A **working, tested Python reference implementation** of everything below ships with this
brief in the folder `aegis_v2/`. Treat it as the source of truth. Your job is to
(1) add it to `python/aegis/`, (2) port the same physics to the JavaScript/TypeScript task
files, (3) delete or quarantine the broken v1 code paths, and (4) make every acceptance
test in Section 7 pass. **Do not change any number in the reference implementation**:
its outputs were checked against an independent solver and against exact computer algebra.

# 1. What AEGIS does today (v1)

The cosmology engine fits a "UFE" torsion model to survey data with the AEGIS optimizer
(CMA-ES, MCMC). The v1 model is, in `ufe-tasks.js:25-43` and `python/aegis/physics.py:19-37`:

$$H^2(z)=H_0^2\left[\Omega_r(1+z)^4+\Omega_m(1+\beta(z))(1+z)^3+\Omega_\Lambda\right],\quad
\beta(z)=\beta_0+\beta_1\frac{z}{1+z},\quad \Omega_\Lambda=1-\Omega_m-\Omega_r .$$

Tasks (registry in `ufe-tasks.js`): `cc-hubble-fit`, `desi-bao-fit`, `sne-pantheon-fit`,
`h0-tension`, `rsd-growth`, `energy-conditions`, `s8-tension`, `dark-energy-eos`,
`combined-multisurvey`, `model-selection-bic`, `ufe-emergence`. The same physics is
duplicated in `python/aegis/tasks/definitions.py`, `mcmc-sampler.js`,
`lcdm-recovery-test.js`, `gpu-*.js/py`.

# 2. Bugs found (fix all of these)

| # | Where | Bug | Impact (measured) |
|---|---|---|---|
| B1 | `ufe-tasks.js:26,38`; `physics.py:21,31`; every `omega_L = 1 - omega_m ...` | Flatness ignores the torsion term. | $E(0)\neq1$: with $\beta=0.3$, input $H_0=67.4$ gives $H(z{=}0)=70.5$. The fitted "H0" is not the Hubble constant. |
| B2 | the v1 model itself | $\Omega_m(1+\beta)$ is a relabelled matter density. | Constant $\beta$ is **exactly** ΛCDM with $\omega_m\to\omega_m(1+\beta)$ (test `test_legacy_constant_beta_is_matter_rescaling`). It is not torsion physics. |
| B3 | `ufe-tasks.js:240`; `definitions.py:184` | $\theta_*$ uses fixed `RS_PLANCK = 147.09`. | 147.09 Mpc is $r_d$ (drag), not $r_s^*$ (144.4). The sound horizon is never computed from the model, so no early-universe physics can change it. |
| B4 | `ufe-tasks.js:46-79`, `definitions.py:402`, `gpu-*` | Trapezoid rule, uniform in $z$, 200–1000 steps to $z=1089$. | $D_C(z_*)$ error **1.6%** (1000 steps) and **40%** (200 steps), i.e. 54× and 1300× Planck's 0.03% error on $\theta_*$. |
| B5 | `ufe-tasks.js:243` | $\theta_*$ tolerance 0.3%. | Planck's error is 0.029%; v1 is 10× too loose. |
| B6 | `ufe-tasks.js:247,273` | SH0ES $H_0$ is inside the "resolution" fit, with ad-hoc weights `0.5*cc + 0.3*bao`. | The fit is pulled to 73 by construction. It cannot show the tension is resolved. |
| B7 | `ufe-tasks.js:279` | $\omega_r$ is a free parameter. | Radiation is fixed by $T_{\rm CMB}=2.7255$ K and $N_{\rm eff}$. |
| B8 | `ufe-tasks.js:136-170,262-266`; `definitions.py:664` | DESI **DR1** BAO, diagonal errors, free `rs` parameter, BOSS $D_V$ in Mpc. | Out of date (DR2, 2025), ignores $D_M$–$D_H$ correlations ($r\approx-0.4$), and decouples $r_d$ from the model. |
| B9 | `ufe-tasks.js:208,227`; `lcdm-recovery-test.js` | SN absolute magnitude `M_B` is a bounded fit parameter. | Must be marginalised analytically (exact, faster, removes a degeneracy). |
| B10 | `ufe-tasks.js:719`; `definitions.py:450` | `rs_predicted = RS_PLANCK*sqrt(1/(1+beta/2))`. | Ad hoc formula with no derivation. Delete. |
| B11 | `ufe-tasks.js:86,304,377,472,685` | Growth uses `1 - omega_m` for $\Omega_\Lambda$ and an approximate growth factor. | Inconsistent with B1 fix. Replace with the ODE solve (Section 5). |
| B12 | `src/torsion.ts:592-911` (`ufeTorsionFunctional`, `crossDomainUFE`, `torsionWaveResidual`) | Residuals in "natural units, all O(1)" with hand-chosen terms. | Not fits to data. Keep as **exploratory** demos only; label them so in code and README; never report them as evidence. |

# 3. The new physics (v2): Torsion-Born Early Dark Energy

**Field.** Promoting the Barbero–Immirzi parameter $\gamma$ of the Holst action to a field
and eliminating torsion gives a canonical, ghost-free pseudoscalar (Taveras & Yunes 2008):
$$\phi=\sqrt{3/2}\,M_{\rm Pl}\,\mathrm{arsinh}(1/\gamma),\qquad
V(\phi)=\Lambda^4\left[1-\cos(\phi/F)\right]^n .$$
Torsion is non-zero only while $\phi$ rolls. That gives built-in screening.

**Background** (units: $\phi$ in $M_{\rm Pl}$, densities in $3M_{\rm Pl}^2(100\,{\rm km\,s^{-1}Mpc^{-1}})^2$,
$N=\ln a$, $\mathcal E=H/100$):
$$\mathcal E^2=\frac{\omega_m a^{-3}+\omega_r a^{-4}+\omega_\Lambda+v(\phi)}{1-\phi'^2/6},\qquad
\phi''+\Big(3+\frac{\mathcal E'}{\mathcal E}\Big)\phi'+\frac{3v_{,\phi}}{\mathcal E^2}=0,$$
$$\frac{\mathcal E'}{\mathcal E}=-\frac32\frac{\omega_m a^{-3}+\frac43\omega_r a^{-4}}{\mathcal E^2}-\frac{\phi'^2}{2}.$$
Initial conditions: $\phi=\theta_iF$, $\phi'=0$ at $a=10^{-8}$; integrate to $a=1$.
**Exact flatness:** $\omega_\Lambda=h^2-\omega_m-\omega_r-\rho_\phi(a{=}1)$, so $E(1)=1$ always.

**Sound horizon, computed from the model (fixes B3):**
$$r_s(z)=\frac{c}{100h}\int_0^{a(z)}\frac{c_s\,da}{a^2E(a)},\quad
c_s=\frac{1}{\sqrt{3(1+\frac{3\omega_b}{4\omega_\gamma}a)}},\quad
\theta_*=\frac{r_s(z_*)}{D_C(z_*)} .$$
$z_*$: Hu–Sugiyama (1996). $z_d$: Eisenstein–Hu (1998), scaled by 1.03848 to Planck's 1059.94.
Integrate in $\ln a$ (Simpson, 20,001 points), and $D_C$ in $\ln(1+z)$. Accuracy:
$<10^{-5}$ vs adaptive quadrature (B4 fixed).

**Parameters:** $h,\ \omega_c,\ \log_{10}v_0\ (\Lambda^4),\ F$; fixed $\theta_i=2.8$, $n=3$,
$\omega_b=0.02237$ (prior), $\omega_\gamma=2.473\times10^{-5}$, $N_{\rm eff}=3.046$.
**Derived:** peak field fraction $f$, its redshift $z_c$, late-time $w\approx(n-1)/(n+1)$.

# 4. Survey data (replace the v1 tables)

**DESI DR2 BAO** (arXiv:2503.14738, Table IV), full $D_M$–$D_H$ correlation:

| Tracer | $z$ | $D_V/r_d$ | $D_M/r_d$ | $D_H/r_d$ | $r_{MH}$ |
|---|---|---|---|---|---|
| BGS | 0.295 | 7.942 ± 0.075 | | | |
| LRG1 | 0.510 | | 13.588 ± 0.167 | 21.863 ± 0.425 | −0.459 |
| LRG2 | 0.706 | | 17.351 ± 0.177 | 19.455 ± 0.330 | −0.404 |
| LRG3+ELG1 | 0.934 | | 21.576 ± 0.152 | 17.641 ± 0.193 | −0.416 |
| ELG2 | 1.321 | | 27.601 ± 0.318 | 14.176 ± 0.221 | −0.434 |
| QSO | 1.484 | | 30.512 ± 0.760 | 12.817 ± 0.516 | −0.500 |
| Ly$\alpha$ | 2.330 | | 38.988 ± 0.531 | 8.632 ± 0.101 | −0.431 |

**CMB:** Planck 2018 $100\theta_*=1.04109\pm0.00030$; $\omega_b=0.02237\pm0.00015$.
Compare $\theta_*$ as a ratio to the engine's own Planck-ΛCDM value ($h=0.6736$,
$\omega_c=0.1200$) so the 0.26% fitting-formula offset cancels.
**SNe:** Pantheon+ 1701 SNe, existing 40-bin full STAT+SYS covariance
(`data/pantheon/pantheon_binned_fullcov.json`), $M$ marginalised analytically:
$\chi^2=A-B^2/C$ with $A=\Delta^TC^{-1}\Delta$, $B=\Delta^TC^{-1}\mathbf 1$, $C=\mathbf 1^TC^{-1}\mathbf 1$.
**Local $H_0$** (separate, optional term, never mixed silently): SH0ES $73.04\pm1.04$;
Local Distance Network (2026) $73.50\pm0.81$.

# 5. Code changes, file by file

1. **Add** `aegis_v2/aegis/{cosmo_v2,data_v2,likelihood_v2}.py` to `python/aegis/`
   and `aegis_v2/run_v2.py` to `python/`. Add `aegis_v2/tests/test_v2.py` to `python/tests/`.
2. **Port to JS** as `src/cosmo-v2.ts` (exported, typed) with the same functions:
   `zStar`, `zDrag`, `soundHorizon`, `Distances{DC,DH,DV}`, `TorsionField` (use an RK45/DOP853
   integrator, `rtol=1e-8`, 8001 output points), `Likelihood{cmb,bao,sn,h0}`.
   Numbers must match Python to 1e-4 relative (add a Jest test that loads the Python outputs
   in `results_v2.json`).
3. **Rewrite tasks** in `ufe-tasks.js` and `definitions.py` to call the v2 engine:
   `h0-tension` → CMB+BAO+SNe likelihood; report results with and without the local $H_0$
   term (B6). `desi-bao-fit` → DR2 table, $r_d$ computed (B8). `sne-pantheon-fit` →
   analytic $M$ (B9). `combined-multisurvey` and `model-selection-bic` → compare ΛCDM,
   legacy-β (flatness fixed), and TorsionField with ΔAIC and ΔBIC using the true parameter counts.
4. **Delete** `RS_PLANCK` from every θ* and BAO computation, the ad-hoc `rs_predicted`
   (B10), `omega_r` as a fit parameter (B7), and the uniform-$z$ trapezoids (B4).
   Keep `RS_PLANCK` only as a documented reference constant.
5. **Growth** (`rsd-growth`, `s8-tension`): solve
   $D''+(2+\frac{d\ln E}{d\ln a})D'-\frac32\frac{\omega_m a^{-3}}{h^2E^2}D=0$ in $N=\ln a$,
   with $D\propto a$ deep in matter domination and $f=d\ln D/d\ln a$. The torsion field does not cluster
   (sound speed 1), so it enters only through $E$.
6. **Label** the exploratory functionals in `src/torsion.ts` (B12) with a header comment and
   remove them from any "discoveries" or evidence output.
7. **README and papers:** replace v1 claims of an H0 resolution with the v2 results table
   in Section 6, and cite the DESI DR2, Pantheon+, Planck, and SH0ES sources above.

# 6. Results of the v2 engine (run October 26, 2026)

RESULTS_TABLE_PLACEHOLDER

# 7. Acceptance tests (all must pass)

| Test | Requirement |
|---|---|
| `test_flatness_exact` | $E(a{=}1)=1$ to $10^{-12}$ for every model |
| `test_planck_baseline` | ΛCDM at Planck values: $r_s^*=144.27$, $r_d=147.10$, $D_C(z_*)=13894.4$ Mpc |
| `test_distance_accuracy_vs_quad` | $D_C(z_*)$ within $10^{-5}$ of adaptive quadrature |
| `test_field_reproduces_paper` | $n=3$ paper point: $f=0.183$, $z_c\approx3540$, $r_s^*=133.48$, $w\to0.5$ |
| `test_field_screened_at_bbn` | field fraction $<10^{-20}$ at $T=1$ MeV |
| `test_lcdm_limit` | $v_0\to0$ recovers ΛCDM to $10^{-8}$ |
| `test_late_release_stays_flat` | late-release field: $E(1)=1$, finite distances |
| `test_legacy_constant_beta_is_matter_rescaling` | documents B2 |
| Jest parity (new) | JS engine matches Python to $10^{-4}$ on all quantities above |

# 8. Guardrails (do not violate)

* Never put the local $H_0$ prior inside a fit and then call the result a resolution of the
  tension. Always report both runs.
* Report $\Delta\chi^2$ together with the number of extra parameters and $\Delta$AIC/$\Delta$BIC.
* CMB information here is the acoustic angle only. A claim about the full CMB fit needs CLASS or CAMB.
* Keep the paper's derived/assumed/open split: the potential $V(\phi)$ is assumed.
