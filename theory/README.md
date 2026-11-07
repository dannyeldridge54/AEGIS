# theory/: scripts and outputs for the BI-supergravity theory note

Theory note: doi:[10.5281/zenodo.23898708](https://doi.org/10.5281/zenodo.23898708) (all versions) · source in
[../papers/theory_note/](../papers/theory_note/).

Step-by-step derivation and assumption ledger: [`DERIVATION_CHAIN.md`](DERIVATION_CHAIN.md).

## Repeatable ten-area numerical review

`effective_modes.py` adds time-dependent canonical scalar modes on the
separate n=3 background, including both independent lower-order corrections
in the analytic potential curvature. It evolves
`deltaq''+(3-epsilon)*deltaq'+[(k/Href)^2 exp(-2N)+Vqq]/H2*deltaq=0`
with explicit real-mode initial values and RK45/DOP853 convergence checks.
Here k/Href is dimensionless and comoving with a_today=1, not k in inverse Mpc.
The test suite compares curvature to gradient differences and evolution to
exact massless de Sitter decay and constant negative-mass hilltop growth.

**Fixed-metric approximation only:** perturbations of the metric, matter,
radiation and neutrinos are omitted. It is not the coupled Einstein-Boltzmann
system, has no primordial spectrum, and supplies no CMB/structure likelihood.
Growing test modes do not by themselves exclude a cosmology. Numerical
agreement does not set `full_stability_established` or
`scientific_baseline_ready` to true. No fit or archive is changed.

### Twenty-five development and validation paths for the canonical n=3 model

First coupled stage: `coupled_perturbations.py` defines Newtonian-gauge
scalar/dust/perfect-radiation evolution with equal metric potentials (zero
anisotropic stress). State order is `deltaq, deltaq_prime, delta_m,
theta_m/(aH), delta_r, theta_r/(aH), Phi`; k/Href is strictly positive.
The metric derivative follows the 0i momentum constraint; the independent
00 density constraint is returned for checking, not projected away. Regressions
test its directional derivative along the background and perturbation flow
at three epochs/wavenumbers, zero-state invariance and the resting-scalar
limit. This stage supplies equations, not an integrated cosmological transfer
pipeline or general primordial initialization. It does not include neutrino/photon
hierarchies, anisotropic stress, recombination or likelihood predictions.
Constraint-preservation regressions are not independent Boltzmann validation.
`integrate` now evolves explicit seven-component initial states, rejecting
initial 00-constraint residual above `1e-10` rather than projecting them.
`validate` compares RK45 and refined DOP853 on uniform/accepted-step samples
and checks both trajectories' absolute dimensionless constraint residual below
`1e-8`, state disagreement below `1e-7`, and initial-state error below `1e-10`.
These are local regression thresholds, not observational accuracy budgets.
Integration is not automatic adiabatic initialization or a transfer function;
the full-stability and scientific-readiness flags remain false.
Fixed-metric mode output must contain exactly two state components at each
accepted epoch, with finite, strictly increasing epochs spanning the requested
interval. Empty, malformed or truncated success-flagged output is rejected
explicitly before dense-output validation.
The same dimensional contract applies to background output (two components)
and coupled output (seven components). Coupled epoch arrays must be
one-dimensional; malformed arrays cannot escape as incidental indexing errors.
Both integration methods are independently checked against the exact
Einstein-de Sitter growing mode: constant Newtonian potential and the analytic
dust density/velocity evolution, including the finite-k density term.
The radiation-only acoustic solution also checks both methods against the
analytic evolving Newtonian potential and radiation density/velocity through
sound-horizon entry. This validates the perfect-fluid limit, not photon
scattering, free-streaming neutrinos or anisotropic stress.
Background solutions retain their immutable configuration. Coupled evaluation
rejects a different supplied configuration rather than mixing one trajectory
with another potential or density prescription.
Exactly absent matter/radiation components remain zero without evaluating
their exponential scaling factors. The background and coupled equations thus
retain the finite de Sitter limit at early epochs where those unused factors
would overflow; this does not extend the supported nonzero-density domain.
Coupled validation also compares interior five-point dense-output derivatives
with all seven evolution equations for both solvers, requiring scaled residual
below `1e-5`. This rejects identical stalled scalar trajectories that satisfy
the constraint and initial state but violate finite-k evolution. The check is
sampled numerical evidence, not a rigorous error bound or full stability proof.

`radiation_adiabatic_initial_state(config, k_over_Href, primordial_phi=1e-5)`
now seeds a restricted regular growing mode for **pure radiation**, zero
vacuum energy and a canonical scalar resting at field=0. It rejects mixed
matter/radiation, rolling or displaced scalars, unresolved wavelengths and
starts outside `0 < x=k*exp(initial_N)/sqrt(radiation_today) <= 0.01`.
The nonzero signed Newtonian-potential amplitude must have magnitude at most
`1e-3` (a conservative API linearity bound, not a measured primordial amplitude).
An early-time series through x^6 avoids cancellation; radiation density and
velocity satisfy both Einstein constraints for that truncated metric series.
Absent-background dust variables use the regular passive-fluid series:
their relative entropy and velocity slip vanish at leading superhorizon order,
not exactly at finite k. The scalar mode is zero, excluding scalar isocurvature.
The derivation and truncation boundary are in `DERIVATION_CHAIN.md`.
Pass the returned seven-component state to `integrate` or `validate`.
Regressions cover both amplitude signs, constraints, entropy/velocity scaling,
analytic radiation evolution through horizon entry, and two initial epochs.
This closes only a perfect-radiation limiting-case initialization check.
It supplies no primordial spectrum, mixed-fluid/rolling-field initialization,
neutrino hierarchy, independent Boltzmann comparison or likelihood validation;
all general readiness flags remain false.

`mixed_adiabatic_initial_state` extends this to gravitating dust plus perfect
radiation with the same zero-vacuum/resting-scalar restrictions. Both
`y=matter_today*exp(initial_N)/radiation_today` and the radiation-defined x
must be at most `0.01` (x strictly positive). This is an early radiation-era
**start** restriction, not a restriction on later integration through equality
or horizon entry. An eighth-order scale-factor series derives all fluid and
metric coefficients together; its first-order constraint excludes a spurious
constraint-violating evolution mode. It does not repair an arbitrary seed by
projecting its density. The pure-radiation initializer remains available as
a separate analytic reference.
Mixed-mode regressions check the Einstein constraint, entropy limits, all
evolution equations, pure-radiation agreement, superhorizon evolution across
equality against an independent background quadrature, and start-epoch
independence through equality and horizon entry with both integrators.
These checks do not establish full-strength rolling-field initialization,
full species physics, primordial spectra or independent Boltzmann agreement.
`subdominant_field_adiabatic_initial_state` adds only a first-order-in-f
(scalar budget <= 1e-6) displaced/rolling-field and nonzero-vacuum mode in the
radiation era; see DERIVATION_CHAIN.md section 12.

`neutrino_contract.py` states only the leading superhorizon radiation-era
free-streaming-neutrino initial contract (`phi=(1+2Rnu/5)psi`, shear, velocity;
DERIVATION_CHAIN.md section 13). It is not an evolution or hierarchy and is not
wired into the coupled equations (`phi=psi` there). Tests:
`python -m pytest theory/test_neutrino_contract.py -q`.

`neutrino_hierarchy.py` evolves a radiation-only toy stage: photon perfect
fluid plus the free-streaming massless-neutrino hierarchy (truncated at lmax)
with `phi != psi`, from an O(x^2) regular initial mode (DERIVATION_CHAIN.md
section 14). Not a photon/baryon Boltzmann hierarchy, not coupled to dust or
the scalar, no spectrum or observables; readiness flags stay false. Tests:
`python -m pytest theory/test_neutrino_hierarchy.py -q`.

`matter_hierarchy.py` adds pressureless CDM to that stage on the exact
radiation+dust background `a/a_eq=s^2+2s`, `s=tau/tau_1` (parameter
`kt1=k*tau_1`), with an adiabatic series (delta/phi through x^3, theta x^4,
F_2 x^5) solved against the evolved equations plus the 0i and 00 constraints
(DERIVATION_CHAIN.md section 15). Checks: Kodama-Sasaki transition, zeta
conservation, the independent spatial-trace Einstein equation, and the
`kt1->inf` limit. An optional `baryon_fraction` adds baryons only in the
infinite-opacity tight-coupling limit (section 16; no opacity/recombination
history). No photon hierarchy, scalar/vacuum, spectrum or
observables; readiness flags stay false. Tests:
`python -m pytest theory/test_matter_hierarchy.py -q`.

`primordial_conventions.py` fixes bookkeeping conventions only:
`Delta2_zeta=A*(k/k_pivot)^(n-1)` with `Delta2=k^3 P/(2 pi^2)`, comoving
`k/H_ref=k[1/Mpc]*c/H_ref[km/s/Mpc]` (a_today=1), and the adiabatic radiation-era
map `Phi0=-2*zeta/3` (so `Delta2_Phi0=4/9*Delta2_zeta`). Amplitude, pivot, tilt
and H_ref are required caller inputs; no measured value, running, tensor,
isocurvature or correlation data is built in, and no observational evidence
follows. Tests: `python -m pytest theory/test_primordial_conventions.py -q`.

These are actionable paths, not twenty-five confirmed bugs. Do not promote an
open path to completed based only on neighboring regression tests. Existing
fixed-metric modes are a separate approximation and must not be silently
substituted for the coupled system.

| Path | Work and acceptance evidence | Present boundary |
|---|---|---|
| 1. Canonical curvature | Differentiate all permitted corrections; compare with independent gradient differences | Implemented; regression required |
| 2. Fixed-metric time evolution | Compare zero-k decay and hilltop growth with exact constant-background solutions | Implemented; regression required |
| 3. Finite-k propagation | Compare a massless de Sitter wave with its analytic solution | Two k values and both methods covered; not full k-domain validation |
| 4. Mode convergence | Refine methods, tolerances and steps across k and initial states | Selected-mode check only |
| 5. Mode equation residual | Independently differentiate dense output for both mode equations | Interior five-point derivative gate, scaled threshold 1e-5; not interval proof |
| 6. Mode initial-state fidelity | Check both methods reproduce supplied amplitude and velocity | Both methods checked at scaled threshold 1e-10 |
| 7. Fast-mode step resolution | Demonstrate accuracy with steps resolving the shortest oscillation time | Fixed step cap only |
| 8. Epoch independence | Transform the same physical initial condition between start epochs | Pure-radiation and radiation/dust regular-mode regressions; rolling-field backgrounds open |
| 9. Homogeneous superhorizon limit | Compare mode evolution with tangent evolution of neighboring backgrounds where applicable | Fixed-metric limit alone insufficient |
| 10. Gauge definition | Specify variables and gauge before adding gravitational sources | Newtonian gauge, equal potentials, no anisotropic stress |
| 11. Metric source terms | Derive sourced Klein-Gordon equation from the stated perturbed metric | Sourced equation implemented; independent derivation/code validation remains |
| 12. Einstein constraints | Check constraint preservation independently of evolution equations | 0i evolution and independent 00 residual; directional preservation regressions |
| 13. Matter perturbations | Add conserved pressureless density and velocity modes with metric sources | Coupled trajectories and radiation-era dust adiabatic seeds; general scalar initialization and transfer normalization open |
| 14. Radiation perturbations | Add consistent density, velocity and anisotropic stress treatment | Perfect-fluid equations only; hierarchy and anisotropic stress open |
| 15. Neutrino hierarchy | Specify species, masses, hierarchy truncation and convergence | Open |
| 16. Adiabatic initial conditions | Derive early-time series satisfying constraints and relative entropy limits | Pure radiation and radiation/dust with resting scalar; rolling-field and general-background modes open |
| 17. Isocurvature initial conditions | Specify independent modes and normalization, not arbitrary relabeling | No primordial spectra |
| 18. Primordial normalization | Define amplitude, pivot, tilt and correlations with dimensions | Open |
| 19. Resonance evolution | Resolve oscillatory intervals, growth and linear-validity limits | No resonance exclusion established |
| 20. Independent Boltzmann comparison | Match action, inputs, initial modes and outputs to an independent implementation | No real cross-code agreement |
| 21. Observable transfer functions | Produce gauge-consistent CMB, matter and lensing outputs with units | Mock export contracts only |
| 22. Observable error budget | Bound solver errors against release-specific likelihood sensitivity | Background thresholds are not survey error budgets |
| 23. Synthetic parameter recovery | Inject known parameters and recover them with declared nuisance/prior choices | No fit launch authorized here |
| 24. Posterior and predictive checks | Demonstrate chain convergence, prior robustness and predeclared predictive validation | Optimizer tests are not posterior evidence |
| 25. EFT/microscopic matching | Specify cutoff, corrections, symmetry protection and matching derivation | Blocked: stated constant-W sector is axion-independent; no specified additional sector generates n=3 |

Order of implementation matters: paths 10-12 precede claiming coupled modes;
paths 13-18 precede primordial observable predictions; paths 20-22 precede
scientific likelihood validation; paths 23-24 require a separately authorized
inference run. Path 25 cannot be replaced by numerical agreement. None of these
paths authorizes restarting the stopped comparison or modifying historical
evidence.

### Scientific capability ledger (reviewed 2026-11-04)

These are methodological expectations, not a universal certification standard.
Regression availability does not establish a successful fit or physical truth.

| Expectation | Current capability | Remaining boundary |
|---|---|---|
| Explicit action, units and assumptions | Derivation ledger and separate canonical EFT | Microscopic torsion-to-n=3 matching unresolved |
| Correct background equations and conservation | Friedmann, scalar continuity and independent interior Raychaudhuri residual gate | Background only |
| Analytic limiting cases | Evolved Lambda limit and exact potential identities | No complete perturbation-limit suite |
| Numerical convergence | RK45/DOP853, tighter tolerances, step caps, state and expansion comparisons | Fixed background thresholds, not survey-calibrated precision |
| Independent implementation agreement | Symbolic/numerical Hessian and exporter-expression regressions | No real CLASS/CAMB agreement established for this baseline |
| Perturbations and initial conditions | Staged coupled perfect-fluid evolution and radiation/dust adiabatic initial series with resting scalar | General initial modes, primordial spectrum, species hierarchies and observable growth unresolved |
| Likelihood fidelity | Covariance, dataset overlap and likelihood-parity regressions | Synthetic contract tests are not a data likelihood result |
| Optimization reproducibility | Restart and saved-objective safeguards | Stopped comparison has no reviewed scores |
| Posterior and model comparison | Paired chi-square/AIC eligibility and fingerprint gates | No posterior convergence, Bayesian evidence or predictive validation claimed |
| Reproducible evidence and scope | Input/evidence hashing and fail-closed review scripts | Passing scripts are not independent scientific confirmation |

The new Raychaudhuri gate checks `abs(d ln(H2)/dN + 2*epsilon) < 1e-5`
at the same interior samples as continuity, using central differences of the
evolved expansion rather than simply repeating the algebraic formula.
Thresholds are local background regression choices, not universal cosmology
accuracy requirements. A wrong expansion derivative must fail even when two
solvers agree and a resting scalar trivially satisfies continuity.

The field-equation gate independently differentiates dense-output field and
velocity samples and checks both `dq/dN=qprime` and the scalar acceleration.
Each residual is scaled by `max(1, abs(expected derivative))` and must be below
`1e-5`. A field incorrectly frozen away from a potential extremum can satisfy
continuity, Raychaudhuri and agreement between two equally wrong solvers;
the nonzero-force regression now explicitly rejects that false pass. These
are sampled finite-difference checks, not rigorous interval error bounds.
Both dense-output solutions must also reproduce the configured initial field
and velocity with scaled error below `1e-10`. A shared wrong initial condition
can otherwise pass convergence and every evolution identity; it now fails the
numerical gate even when it is an exact solution of a different initial-value
problem. This does not establish independence from the chosen initial epoch.
Integration success alone is insufficient: accepted epochs must be finite,
strictly increasing and span exactly the requested start and end. Truncated
or malformed solutions are rejected before dense-output validation can
extrapolate beyond the actually integrated interval.

Further scientific review requirements include initial-epoch independence,
parameter-domain and stiff-regime convergence, approximation matching,
gauge/constraint consistency, adiabatic/isocurvature initialization, evolving
instability growth, observable-level error budgets, nonlinear validity,
parameter identifiability, prior sensitivity, posterior convergence, predictive
validation, systematic robustness and EFT cutoff/radiative stability.
Additional boundaries are consistent neutrino/recombination conventions,
observable units and normalization, nuisance-parameter treatment, model-domain
and boundary optima, synthetic-data recovery, coverage calibration, provenance
of independent validations, and propagation of theory uncertainty. This is an
open methodological checklist, not a claim that every item has been implemented
or that an exhaustive search can certify no remaining issues.

Methodological references:
[Cobaya MCMC documentation](https://cobaya.readthedocs.io/en/latest/sampler_mcmc.html)
explains independent chains and convergence assessment;
[DESI DR2 BAO and cosmological constraints](https://arxiv.org/abs/2503.14738)
provides release-specific observational context. Neither reference validates
AEGIS or supplies its missing perturbation/microscopic derivation.

From the repository root on Windows, run:

```powershell
.\cmb-fit\venv312\Scripts\python.exe .\theory\review_numerical.py
```

The script uses its own interpreter to run existing bounded regressions once,
then prints ten review areas with test, failure and skip counts. It does not
invent ten defects or modify source files automatically. Exit `0` means all
areas have complete passing regression evidence; `1` means test failure; `2`
means blocked or incomplete evidence (including skipped tests, collection
errors, missing reports or the default 120-second timeout). Failed-test output
identifies the assertions to investigate and fix. Temporary pytest evidence
is cleaned up after printing; existing reports and archives are not rewritten.
No fit, service restart or catalog acquisition is launched. This is a software
regression gate, not full perturbation validation or microscopic confirmation.
The runner itself is covered by `theory\test_review_numerical.py`.

For the separate numerical/derivation/comparison contract review, run:

```powershell
.\cmb-fit\venv312\Scripts\python.exe .\theory\review_derivation_comparisons.py
```

This uses the same fail-closed runner with ten focused areas, including
analytic limits, symbolic/numerical projections, CAMB density-expression
consistency, reproducible minimizer results, paired score eligibility,
fingerprint drift and likelihood covariance/overlap controls. Comparison tests
also reject empty or nonpositive chronometer measurements and nonfinite
chi-square results from overflow.
Chronometer covariance construction also rejects overflow before loading or
extension preparation can succeed with nonfinite evidence.
The loader also requires positive-definite covariance via Cholesky
factorization, rejecting singular matrices caused by underflow before use.
Observable background interpolation requires at least two finite, distinct
epochs, even for an empty requested output grid.
Observable exports require finite derived parameters, one result per configured
likelihood, and ordered integer CMB multipoles through ell=2500. Mock-solver
regressions cover these contracts without computing a fit or physical spectra.
Spectrum arrays must be one-dimensional, and conversion from log likelihood
to chi-square contributions must remain finite even for finite input values.
Paired-score sums and derived differences (including per-likelihood, AIC and
shared-parameter differences) are checked after arithmetic as well as before
it, so finite input values cannot produce nonfinite exported comparisons.
Saved observational contribution names must match each model's configured
likelihoods, not merely agree between models. Identically mislabeled evidence
now blocks scoring rather than passing the matched-comparison gate.
Present physical matter components must be nonnegative; their sum, normalized
matter density and S8 must remain finite. S8 takes the square root before
normalizing to avoid unnecessary overflow in the intermediate density ratio.
These guards prevent missing evidence from looking like a perfect fit.
Comparison tests
use synthetic temporary evidence; they do not score the user-stopped fit,
execute a replacement fit or establish real CLASS/CAMB numerical agreement.
Run, investigate and fix actual failures, then rerun until no failures or
blocked areas remain; repeating unchanged passing tests is not a new review.

| Script | What it computes | Output |
|---|---|---|
| `bi_kahler_lambda.py` | Kähler metric of the Gates–Ketov–Yunes BI superfield; λ = −2√(2/3) (sympy) | `bi_kahler_lambda.json` |
| `stellar_weak_field.py` | Conditional Jordan-frame weak-field scalar coupling, Cassini envelope, and unscreened Yukawa response; not a stellar prediction | printed JSON |
| `bi_qcd_axion.py` | QCD-anomaly BI-axion potential scale and equality-era consistency estimate (Mercuri–Taveras normalization) | printed JSON |
| `bi_qcd_dynamics.py` | Homogeneous n=1 QCD-axion evolution, with self-consistent background friction and WKB continuation | `bi_qcd_dynamics.json` |
| `solar_lowz.py` | Solar-system gate (Cassini) for the BI dilaton | `solar_gate.json` |
| `bi_superpotential.py` | Supergravity potential for constant W | `bi_superpotential.json` |
| `twist_potential_audit.py` | Exact n=3 harmonic, vacuum and lower-harmonic sensitivity audit of an assumed canonical one-field EFT; not a BI derivation | printed JSON |
| `coupled_stability.py` | Covariant Hessian, transverse projection and scalar-sector entropy mass for the assumed n=1 two-field action; no trajectory verdict | printed JSON |
| `scaling_audit.py` | Dimensionless cosine-shape scaling against an ordinary monomial control; no fractal or microscopic inference | printed JSON |
| `ufe_checks.py` | Inflation from α = 1; dilaton as early field; LQG value | `ufe_er.json`, `ufe_in.json` |
| `spiral_w.py` | Two-field Spiral Twist solver; validation; Ramos-Hamud mirror; scans; matter-like angle | `spiral_*.json` |
| `spiral_class_mirror.py` | AxiCLASS effective spiral against the solver | `spiral_class_mirror.json` |
| `forward_predictions.py` | Frozen predictions from the stored best fits | `forward_predictions.json` |
| `lowz_split.py` | DES Y5 supernova χ² split at z = 0.1 | `lowz_split.json` |
| `f_dilaton_degeneracy.py` | Audit 7 Nov: is the Spiral's F a constraint, or absorbed by the dilaton? | `f_dilaton_degeneracy.json` |
| `dilaton_pinning.py` | Audit test A: what fixes the dilaton, and the F each choice gives | `dilaton_pinning.json` |
| `alpha1_inflation_squeeze.py` | Audit 7 Nov: ACT n_s versus the locked α = 1 tensor ratio | `alpha1_inflation_squeeze.json` |

**Rules written before computing:** `PREREGISTRATION_UFE_CHECKS.md`, `PREREGISTRATION_SOLAR_LOWZ.md`.
**Predictions locked before the data:** `PREDICTIONS_LOCKED_2026-11-02.md`, with its SHA-256 in the `.sha256` file.

The constant-superpotential calculation is only an algebraic consistency check: its positive branch has a negative
signed logarithmic slope in the stated canonical-field orientation, its local minimum is not global, and it does
not derive the exponential or cosine terms assumed in the Spiral Twist model. Run the focused analytic regressions
with `python -m pytest theory/test_bi_supergravity.py`; the background solver's bounded consistency checks are
`python theory/spiral_w.py validate` (do not use `scan` as a validation substitute).

`twist_potential_audit.py` investigates an explicitly separate effective model:
positive amplitude times `(1-cos(q/F))**3`, plus a nonnegative constant,
with an assumed canonical kinetic term and positive `F`. It is periodic and
bounded below, with sixth-order minima, zero quadratic mass, and unstable
hilltops. Its exact n=3 shape requires specific cancellations between three
Fourier harmonics. A permitted leading-cosine correction gives a nonzero mass
and, for negative coefficient, destabilizes the original minimum. Periodicity
alone does not protect those cancellations. Setting amplitude to zero recovers
a cosmological constant only when the scalar is at rest; its kinetic energy
does not disappear automatically.

This establishes a mathematically consistent **assumed one-field EFT**, not a
microscopic torsion construction, full two-field perturbative stability,
quantum stability, or a new fit. No justified microscopic fix is established.
The active frozen comparison and archived potentials remain unchanged.
The audit also checks the canonical continuity/equation-of-motion identity.
With zero potential amplitude, residual scalar kinetic density redshifts as
`a**(-6)` rather than vanishing. Near the n=3 minimum, rapid small-amplitude
oscillations in the sixth-order potential have mean excitation `w=1/2` and
density scaling `a**(-9/2)`, not pressureless CDM. This virial limit excludes
the constant vacuum offset and does not apply during onset or slow roll.
These statements do not validate an effective fluid perturbation closure.
The full-period curvature audit identifies negative curvature where
`cos(q/F) < -2/3`, not only at the hilltop. Actual perturbation growth depends
on expansion and gravitational coupling. For the assumed canonical one-field
action, the time and spatial principal kinetic coefficients are positive and
the short-wavelength sound speed squared is one. This is **not** the averaged
oscillating-fluid sound speed and cannot be replaced by its mean `w=1/2`.
It does not assess the coupled BI fields, gravitational constraint modes,
quantum corrections, or a background-dependent fluid closure.
Published context: [Smith, Poulin and Amin, arXiv:1908.06995](https://arxiv.org/abs/1908.06995)
discusses scalar perturbations, initial conditions, isocurvature and anharmonic
self-resonance. These motivate additional gates, not an assertion of instability
in this model: their highlighted resonance example concerns n near two.
Our n=3 audit does not compute resonance growth, primordial isocurvature,
or perturbative validity along a fitted trajectory.
Separately, the audit derives Ricci curvature `-lambda**2/2` for the
two-field metric `diag(1, exp(lambda*chi))`, giving `-4/3` at the stated BI
slope in reduced Planck units. Positive metric coefficients exclude a
kinetic-sign ghost at finite fields, but negative curvature can contribute
to the entropic mass. A covariant Hessian and trajectory turn rate are still
needed. [Renaux-Petel and Turzynski, arXiv:1510.01281](https://arxiv.org/abs/1510.01281)
establishes this concern for multifield inflation, not an instability verdict
for our late-time solution.
Run `python theory/twist_potential_audit.py` (prints only), and
`python -m pytest theory/test_twist_potential_audit.py` for exact regressions.

`stellar_weak_field.py` derives the Reading-A conformal coupling and the conditional linearized Yukawa-force ratio,
then applies the existing massless Cassini gate. It does not derive the local scalar profile, effective mass,
screening, or Galactic orbit residual needed for a predictive Gaia comparison. Its regression checks are
`python -m pytest theory/test_stellar_weak_field.py theory/test_bi_supergravity.py -q`; passing these algebraic checks
does not validate the missing stellar-scale assumptions.

`bi_qcd_axion.py` independently evaluates the leading QCD-anomaly potential
$V=\chi_{\rm QCD}[1-\cos(\varphi/F_\varphi)]$, derives its curvature mass, and propagates the explicit susceptibility,
decay-constant, expansion, entropy, equality, and target-fraction inputs. Its equality-era angle estimate is relative
to the total density (matter plus radiation) and is valid only in the subdominant, small-angle approximation.
The zero-temperature susceptibility and fixed-degree-of-freedom assumptions are not a thermal QCD likelihood; the
resulting $n=1$ field oscillates as matter long before equality and is neither the AEGIS $n=3$ equality-locked EDE
potential nor late-time quintessence. The full derivation and limitations are in
[`../papers/theory_note/spiral_twist_note.tex`](../papers/theory_note/spiral_twist_note.tex); input-scaling regressions are covered by
`python -m pytest theory/test_bi_qcd_axion.py`.

`bi_qcd_dynamics.py` numerically evolves the homogeneous angle from the approximate onset `H = m/3` through the
rapid-oscillation regime, then continues its averaged density as matter. It includes the scalar contribution in the
Friedmann constraint and Hubble friction during direct integration. The default initial angle is solved to make this
field 5% of the total background density at equality; this is a requested normalization, not a fit or prediction.
The output compares adding this component with replacing an equal amount of CDM, and intentionally reports no
`delta_chi2` in this background report. At equality the module checks \(m/H\) and the effective sound speed at
the configured maximum wavenumber. When those checks pass, the matched likelihood uses CAMB's existing
pressureless-CDM perturbation equations for the scalar density and subtracts that density from ordinary CDM,
preserving total matter. This is the rapidly oscillating, small-\(k/(am)\) effective limit, not a separately
implemented scalar-fluid perturbation hierarchy. The supplied QCD susceptibility is an effective low-energy input,
not a first-principles quantum calculation; the dilaton is frozen and the result does not derive or validate the
separate `n=3` Twist potential.
Run `python -m theory.bi_qcd_dynamics` to rebuild `theory/bi_qcd_dynamics.json`, and
`python -m pytest theory/test_bi_qcd_dynamics.py` for the ODE and WKB-handoff regressions.

The CDM-replacement split preserves total matter: at equality, where radiation
equals that total matter, a requested scalar fraction `f` requires
`omega_scalar = 2*f*(omega_b + omega_cdm_total)`. The additive-scalar denominator
is not appropriate to this replacement.
The CAMB result exporter uses this same replacement normalization; a regression
checks its actual expression without executing a fit. Stored older exported
CDM-share metadata is historical and is not rewritten.
QCD scale inputs must be finite and
positive; requested fractions must lie strictly between zero and one. The
homogeneous solver additionally rejects targets outside its supported initial
angle bracket of 0 to 0.1 radians rather than extending its approximation.

The solar calculation now labels a **coupling minimum**, not demonstrated
attractor protection. It provides both the linearized displacement estimate and
the exact interval satisfying the stated massless Cassini relation; neither
establishes that an actual local solution occupies that interval. Historical
JSON outputs retain their original labels/numbers and are not automatically
rewritten by these corrections. Run calculation functions/tests to inspect
current behavior without regenerating archived JSON.

`python theory/spiral_w.py validate` now exits nonzero if validation fails.
CLI regression checks are in `theory/test_spiral_validation_cli.py`. These
changes concern separate theory utilities, not the running frozen Late Twist
comparison, whose solver, adapter, likelihood inputs and one-attempt policy
remain unchanged.

The exploratory `spiral_w.py` now rejects invalid/nonfinite Friedmann states
instead of freezing derivatives, refuses failed integrations as closure
residuals, and rejects dense-output extrapolation. Its existing `validate`
checks the null energy condition, not a numerical energy-conservation residual;
the separate potential audit verifies an algebraic conservation identity only.
`test_spiral_numerics.py` checks normalized numerical scalar-continuity residuals
below `1e-5` and expansion changes below `1e-7` after tighter tolerances on one
bounded coupled trajectory. This is a representative regression, not validation
of every fitted point. Effective-dilaton reports now take their potential
explicitly instead of sharing a mutable global cache, reject singular ratios,
and evaluate the entry labeled redshift one at exactly one (previously a nearby
grid point). Historical scan files are not regenerated.
Unresolved gates are fitted-trajectory conservation/convergence, coupled-field
perturbative stability, resonance/isocurvature and microscopic harmonic
protection. None is marked passed by the background checks.

### Local and literature review concern ledger

### Remaining scientific concerns and implementation boundaries

**Separate starting baseline:** `effective_baseline.py` defines a canonical
one-field action with excitation `A*(y**3 + c2*y**2 + c1*y)`, `y=1-cos(q/F)`,
and independent vacuum offset. All scales, both correction coefficients,
matter/radiation densities and initial field/velocity/epochs are explicit.
Defaults are illustrative, not inferred, fitted or microscopic predictions.
Negative corrections are permitted, but nonpositive expansion is an error.
The background includes scalar energy in Friedmann and Raychaudhuri equations.
`validate(Baseline(...))` reports tighter-tolerance expansion differences and
sampled continuity residuals with fixed thresholds `1e-7` and `1e-5`.
No present-day closure tuning is implied: `H_ref` is a fixed reference unit.
The numerical gate compares RK45 against tighter DOP853 integration, including
field and velocity differences scaled by `max(1, abs(refined_component))` below
`1e-7`; expansion agreement alone is insufficient. Nonfinite states, potential
gradients and continuity residuals fail explicitly. These are sampled background
checks, not proof of accuracy for arbitrary stiff/rapidly oscillating inputs.
Integration now caps steps at interval/200 for RK45 and interval/400 for
refined DOP853. Validation combines the uniform grid with both solvers'
accepted step points and reports its maximum epoch gap. This reduces
fixed-grid blind spots but does not prove that arbitrarily fast oscillations
or every inter-step feature are resolved; frequency-specific tests remain
necessary before fitting such regimes.
Validation rejects nonfinite comparison errors before maximum tracking and
reports the actual continuity-sample count. A run with no resolvable interior
continuity samples fails rather than reporting a zero residual as a pass.
Central-difference continuity checks exclude integration endpoints explicitly.
An evolved constant-field regression compares both RK45 and DOP853 against
analytic matter/radiation/Lambda expansion and its Raychaudhuri derivative at
101 epochs across the full configured interval, not just at today. This tests
the Lambda limit independently of agreement between numerical methods.
The exploratory two-field solver and matter-angle density calculations use
`2*sin(angle/2)**2` instead of `1-cos(angle)` to avoid cancellation near a
cosine minimum. A tiny-angle regression checks nonzero energy and agreement
with the force. This is algebraically equivalent, not a changed potential.
Background evaluation also rejects a coupling or potential different from
the solved action. Closure tuning rechecks its final integration and requires
`abs(H2_today - 1) <= 1e-8` rather than trusting only the root-finding calls.
Closure rejects configurations that omit dense output or stop before today,
and accepts an explicit `dense=True` without passing duplicate solver keywords.
The perturbation and microscopic gates stay unresolved; the report cannot
declare a scientifically validated baseline. Tests vary lower harmonics
independently rather than selecting them to improve an observational fit.
Run `python -m pytest theory/test_effective_baseline.py`.
This baseline does not replace the running n=3 fit or any archived inputs.

`scaling_audit.py` checks the proposed cross-scale pattern without inserting
pi/Fibonacci scaling coefficients. Normalizing field by `F` and excitation
potential by its amplitude collapses the assumed cosine shape by definition.
Its local small-angle power law is an ordinary Taylor limit: n=1 gives a
quadratic and n=3 a sixth-order potential. The finite-angle effective exponent
varies, and the fixed doubling test departs from the exact monomial control.
Neither this collapse nor periodicity proves fractality or quantum-to-cosmic
matching. Such claims require a specified dimensionless observable, matching
calculation, independent uncertainties and non-fractal/held-out tests.
Run `python theory/scaling_audit.py` and
`python -m pytest theory/test_scaling_audit.py`.
The local exponent uses its small-angle series below `1e-4` to avoid division
by an underflowed half-angle, including the smallest positive floating-point
coordinate. This preserves the analytic exponent even when the potential
value itself is too small to represent; it does not establish scale invariance.

`coupled_stability.trajectory_diagnostic` now evaluates the Hessian, geometric
and turning mass terms on a supplied `spiral_w` solution. The normal direction
comes from its metric-normalized velocity; the turning contribution comes from
the transverse potential gradient divided by field speed. Zero-speed states
are explicitly rejected because that basis is undefined. A bounded n=1
trajectory is tested at three epochs. Neither a positive nor a negative
instantaneous mass settles full mode growth, isocurvature, or n=3 stability.
Supply parameters from the same solved action; this is not a fitted-point
validation or an authorization to retune results.
Solutions now retain their action parameters and potential identity; entropy
diagnostics reject mismatched inputs rather than combining different actions.
`coupled_stability.sample_trajectory` accepts strictly increasing nonnegative
redshifts and reports all samples, the minimum mass, negative-mass sample count
and maximum redshift gap. A 41-point illustrative interval is tested.
Sampling is not continuous stability validation; narrow growth windows can be
missed, and no perturbation modes are integrated.
The numerical transverse Hessian projection is also checked against the
independently differentiated symbolic expression at three epochs, with zero,
negative BI and positive kinetic-coupling slopes. This checks signs and metric
factors, not the completeness of the entropy-mode approximation.

| Concern | Implemented mitigation | Still required |
|---|---|---|
| Missing microscopic n=3 sector | Exact constant-W axion-independence test and corrected derivation ledger | Specify an action, symmetry-breaking sector and scales; no justified replacement supplied |
| Unprotected harmonic cancellations | Fixed positive/negative lower-harmonic shape sensitivity, exact shifted minima and crossover | Quantum correction/protection derivation and separate background sensitivity study |
| Coupled-field perturbative stability | Connection, curvature and exact conservation checks | Covariant perturbation equations evaluated on matched trajectories |
| Primordial isocurvature | Explicit unresolved gate | Inflationary history, initial perturbation spectrum and transfer evolution |
| Self-resonance/nonlinear growth | Negative-curvature diagnostic with limited scope | Time-dependent mode evolution and linear-validity assessment |
| One-field reduction | Distinct n=1/n=3 assumptions and propagation limits documented | Same-action two-field comparison and justified heavy-field hierarchy |
| Fitted-point numerical validation | Representative conservation/convergence tests and explicit failure guards | Completed fit points and solver-specific uncached checks; no retuning |
| Local matter-coupling applicability | Reading-A and Reading-B assumptions separated | Local profile, screening and observational selection/covariance |

`twist_potential_audit.py` prints a fixed illustrative harmonic-sensitivity
study for correction coefficients `-1e-4`, zero and `1e-4`. At angle 0.1,
the nonzero correction is more than four times the original n=3 excitation
potential despite its small coefficient. Negative correction moves the
minimum away from zero; its negative excitation value is not a verdict on
total vacuum energy because the independent constant offset matters.
This is shape sensitivity only, not a background fit, radiative calculation,
or demonstration of robustness. Scientific unknowns are not software defects
that can be removed by changing formulas until a test passes.

| Concern | Resolution / remaining gate |
|---|---|
| Invalid Friedmann states froze derivatives | Explicit error; guarded RHS and dense evaluation |
| Failed integrations became closure residuals | Explicit integration failure |
| Dense solutions allowed extrapolation | Interval and success checks |
| Shared potential cache could mix solutions | Removed; potential passed explicitly |
| Redshift-one label used a nearby sample | Exact redshift evaluation |
| Effective equation-of-state ratio could be singular | Explicit finite/nonzero denominator check |
| Unsuccessful CPL optimizer could produce fit-shaped output | Explicit optimizer failure |
| Matter-angle scan changed matter density after solving | Re-solve final density; reject normalization residual above `1e-5` |
| Coupled exponential helper lacked physical/failure guards | Finite input, density, redshift, integration and Friedmann checks |
| CLASS mirror computed and discarded 64 slope-search solves | Removed dead search; same-parameter comparison unchanged |
| Zero scalar density or invalid expansion entered reports | Explicit equation-of-state and CPL-input guards |
| Ramos mirror used failed independent endpoints / successful FAIL exit | Check integration success and finite endpoint; propagate failed mirror as nonzero CLI exit |
| Invalid Hubble input could launch CLASS shooting guess | Reject nonfinite/nonpositive `h` before numerical work |
| CLASS interpolation silently clamped missing redshift coverage | Validate column shapes, uniqueness, finiteness, physical signs and coverage |
| CLASS normalization assumed first sample was today | Interpolate normalization and radiation density at exactly zero redshift |
| CLASS mirror reported FAIL with successful CLI exit | Preserve report and exit nonzero |
| Solved trajectories were evaluated with mutable global densities | Capture matter/radiation on the solution; reuse in background and CPL evaluation |
| Finite CLASS arrays could overflow normalized ratios | Explicit arithmetic and normalized-finiteness checks |

`mirror_background.py` tests background preparation with synthetic arrays,
without CLASS, fits or archive writes. A full solver mirror rerun remains
separate; these guards do not establish agreement of the physical models.

The CLASS mirror dead-code removal is checked structurally without importing
CLASS or running a solver build. It is not a new numerical mirror validation.
Matter-angle reports now retain their final normalization residual for review.
| Validation description overstated conservation | Corrected; separate numerical continuity regression |
| n=3 cancellations and lower harmonics | Sensitivity documented; microscopic protection unresolved |
| Flat minima versus matter-like QCD oscillations | Distinct limits tested; no fluid substitution |
| Negative potential curvature / self-resonance | Curvature checked; actual mode growth unresolved |
| Curved two-field metric / entropic stability | Ricci curvature derived; full perturbations unresolved |
| Primordial isocurvature | Requires initial-condition and perturbation analysis |
| Effective potential versus microscopic derivation | Explicitly separated; no justified microscopic repair |

**Paths:** scripts that rebuild fits read `TWIST_AXI` (default: this repository's `cmb-fit/axiclass` inside WSL) and
`TWIST_RESULTS`. The pure-Python ones (`bi_kahler_lambda.py`, `solar_lowz.py`, `bi_superpotential.py`,
`ufe_checks.py`, `spiral_w.py`) need only numpy, scipy and sympy.

**Audit, 7 Nov 2026 (AI-assisted, not pre-registered):** `THEORY_AUDIT_2026-11-07.md`. **Coupling decision (7 Nov):** `COUPLING_CHOICE_NIEH_YAN.md`.
