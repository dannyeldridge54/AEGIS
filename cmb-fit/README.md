# AEGIS CMB fit — the decisive test of the torsion-born EDE model

**Question:** does the torsion field still raise H0 once the *full* Planck CMB spectrum is included,
not just the acoustic angle? Background-only fits (AEGIS v2) cannot answer this, because the CMB peak
heights are what pin down the dark-matter density ω_c.

**How:** the torsion field's Lagrangian (canonical Barbero–Immirzi pseudoscalar,
V = Λ⁴[1 − cos(φ/F)]ⁿ) is identical to CAMB's built-in `EarlyQuintessence` model,
V = m²f²[1 − cos(φ/f)]ⁿ. So the test uses CAMB, the Boltzmann code used by the Planck collaboration,
and Cobaya, the standard sampler, with no custom physics code.

| Setting | Value |
|---|---|
| Model | EarlyQuintessence, n = 3; free: f_EDE(z_c), log10 z_c ∈ [3, 4.3], θ_i ∈ [0.1, 3.1] |
| Cosmology | ω_b, ω_c, 100θ\* (exact `thetastar`, not the cosmomc approximation), ln10¹⁰A_s, n_s, τ; Σm_ν = 0.06 eV |
| CMB | Planck 2018: low-ℓ TT, low-ℓ EE, high-ℓ TTTEEE (plik-lite), lensing |
| BAO | DESI DR2, all tracers (`bao.desi_dr2.desi_bao_all`) |
| SNe | Pantheon+ (`sn.pantheonplus`); with SH0ES: `sn.pantheonplusshoes` |
| Runs | ΛCDM and torsion EDE, each without and with SH0ES |

## Steps (Windows)

1. `SETUP_CMB_FIT.bat` — makes a private Python environment in this folder, installs CAMB + Cobaya,
   **validates CAMB against its own documented example (H0 = 73.2113)**, downloads the likelihood
   data, and times one full evaluation.
2. `RUN_CMB_FIT.bat` — the four best fits (hours; low priority, 2 threads). Resumable.
3. Results: `results/REPORT.md` (Δχ² and ΔAIC of torsion EDE vs ΛCDM, H0, f_EDE) and `results/*.json`.

Optional afterwards: `venv\Scripts\python cmbfit.py mcmc` for full posterior chains (one to several days).

## How to read the outcome (decided in advance)

* The torsion field earns a claim only if, **without SH0ES**, ΔAIC (EDE − ΛCDM) < 0, i.e. it improves the
  fit by more than its 3 extra parameters cost, and the best-fit H0 moves toward 73.
* If ΔAIC ≥ 0 without SH0ES, the honest statement is: the model is allowed by the data but not preferred.
* With SH0ES, any improvement mostly reflects absorbing the SH0ES prior; report it, but don't lead with it.
* Published comparison: Poulin, Smith, Calderón & Simon 2025 (arXiv:2505.08051) find f_EDE ≈ 0.09 and
  H0 ≈ 72 with Planck + ACT DR6 + DESI DR2 (profile likelihood, no SH0ES).

## AxiCLASS local scale profiles

`axiclass/run_local_scale_profiles.sh` adds a separate Planck 2018 high-ℓ + lensing profile suite to the existing
ACT/SPT suite. The two CMB likelihood sets are run separately to avoid double-counting overlapping measurements.
Each Planck suite uses the existing 24-point Late Twist \((F,m)\) grid, DESI DR2 BAO, and one local supernova sample
at a time: Pantheon+, Pantheon, JLA, DES Y5, DES-Dovekie, Union3, or Pantheon+ with SH0ES. The runner first fits a
matched AxiCLASS \(\Lambda\)CDM reference for each sample, then runs the grid; it writes distinct result names and
does not modify the historical queue or status files.

Run inside the WSL `aegis` environment with `bash cmb-fit/axiclass/run_local_scale_profiles.sh`. Existing local data
are used only; this does not add Gaia/Star Mapper observations or galaxy-scale, weak-lensing, or cluster likelihoods,
which are not staged as AxiCLASS-compatible likelihoods in this checkout. Failed profile cells remain explicit in
their per-run logs rather than being treated as completed fits. For Late Twist, a non-finite-likelihood penalty is
only an optimizer safeguard: each converged restart is re-evaluated, and non-reproducible minima are excluded before
Cobaya selects a result. If no restart has a reproducible minimum, the cell fails and does not produce a result JSON.
New AxiCLASS result summaries compute `minimum.Omega_m` from the fitted baryon and CDM densities, the fixed
0.06 eV neutrino mass, and H0; the solver's raw derived value is retained as `Omega_m_class_reported`. Historical
JSON summaries are unchanged until explicitly regenerated from their saved `.minimum.txt` chain files.

The nonlinear scalar-field fix in `axiclass/nlfix/patch_nlfix.py` also corrects Halofit's present-day neutrino
fraction: its denominator must exclude the dark-energy field, just like the time-dependent matter density.
Rebuild an independent AxiCLASS copy after applying the patch; editing summary `Omega_m` values does not repair
spectra or existing fits. Keep the old build and outputs, validate the frozen-field limit and linear/nonlinear
matter and CMB spectra, and use the same verified build and accuracy settings for all matched controls. Select an
independent build root with `TWIST_BUILDS`; this patch does not automatically replace an installed solver.
For likelihood-only optimization (`ignore_prior=True`), save with `save(..., ignore_prior=True)` to read Cobaya's
`.bestfit.txt` rather than posterior `.minimum.txt`. Such runs omit soft priors; enforce any required hard external
domain constraints in the likelihood, since box bounds alone do not retain external priors.
Restart reproduction uses an absolute log-objective tolerance of 0.01 (0.02 in chi-square), with no relative
tolerance: otherwise large total objectives can admit a mismatch exceeding the stated limit. Passing the
frozen-field mirror does not establish numerical accuracy at a fitted non-null point; check that point under
denser settings and repeat matched optimization if the accuracy or restart-spread checks remain unresolved.
When an external likelihood consumes `w0_fld`/`wa_fld`, explicitly include those parameters in the theory's
`input_params` as well. Verify their actual values reach CLASS and that changing each changes physical predictions;
counting sampled parameters or successfully constructing the model is not a routing check. A dense rerun must be
checked against still denser settings, not against the same settings it was fitted with.

## Caveats

* CAMB's own docs note EarlyQuintessence is "not as well tested as most of the rest of CAMB"; the
  validation step checks it reproduces the documented result.
* Plik-lite marginalizes Planck foregrounds assuming ΛCDM-like spectra; this is standard for quick EDE
  tests, but a final paper should repeat the fit with the full plik or NPIPE CamSpec likelihoods.
* Best fits in EDE are known to be harder to find than in ΛCDM (`best_of: 2` restarts are used).

## Expanded observational coverage (separate from the frozen benchmark)

### Current comparison plan

This is the active sequence for the corrected AxiCLASS comparison, not a replacement for the historical
CAMB/EDE workflow above. Compare LCDM, w0-wa and effective one-field Late Twist; keep other theory branches
and historical fits out of this baseline.

| Stage | Current setup | Completion requirement |
|---|---|---|
| 1. Baseline and independent review | `results/restarts/clean_benchmark_reviewed_routing_20261104` | Matched fits, reproducible minima, restart spread, provenance and dense-accuracy gates all pass |
| 2. Common fitted predictions | Exporter installed; reference-point preflights passed, fitted exports pending | Export reviewed best points on identical grids/units; do not label them posterior intervals |
| 3. Publication-reference CMB robustness | Identified, not configured or launched | Validate PR4/NPIPE high-l and official combined Planck-ACT DR6 lensing for every control; preserve its corrections, nuisance treatment and accuracy |
| 4. Separate galaxy-growth comparison | SDSS DR12 joint BAO+RSD preflight passed; fits not launched | Matched fits using its full covariance, replacing rather than stacking overlapping DESI BAO |
| 5. Full DES Y3 shear | Public data staged; likelihood integration blocked | Reproduce official likelihood, nuisance constraints and AxiCLASS parity before fitting |

Gaia collection runs independently and supplies candidate diagnostics, not a cosmology likelihood.
Full-shape clustering, clusters, sirens, local gravity and conditional quantum/parity branches are a deferred
backlog, not active scheduled experiments. The local hourly cross-check is read-only monitoring, not an
implementation worker or fit launcher; only one combined monitor is enabled.

### Daily gated comparison setup (5 November 2026 UTC)

The local `AEGIS gated theory comparison` automation is enabled for 22:00
machine-local time (Central at setup), ID
`6909b65b-0735-4d73-95d4-c8af44b20ea4`. The app reported its first due time as
5 November 04:01:09 UTC (4 November 22:01:09 Central). This is a saved schedule,
not evidence that the new fit has started. The machine/app must remain available.

`axiclass/scheduled_comparison.py` runs on the existing WSL interpreter.
Current low-credit monitoring configuration (user approved 4 November 2026):
`AEGIS lightweight cross-checks` replaces the hourly audit on the same automation
ID `10762a61-8378-47ba-b9a9-1a81158f91a8`. It is enabled at
`29 */6 * * *` (00:29, 06:29, 12:29, 18:29 machine-local time), using
Auto efficiency. It reads local endpoints and bounded recorded attempt summaries,
writes a small audit in its own session files, and does not recompute scorecards,
run tests or launch fits. Older hourly audit descriptions below are historical.
The approved 22:00 daily comparison is unchanged. Both schedules require the
computer and Copilot app to be available; no immediate run was requested.

The included `axiclass/tests/test_dashboard.py` also runs the Node dashboard
regressions before fitting. On WSL it can use the existing Windows `node.exe`
with a converted test-file path. Missing Node or a failed dashboard regression
blocks the gate; it never installs a runtime or bypasses a failed test.
Without `--run` it checks provenance only. With `--run`, it verifies frozen
source/data/solver fingerprints and prerequisite gates, runs the axiclass
regressions plus four Gaia/UFE test files, and permits one new matched
LCDM/w0-wa/effective Late Twist attempt. A Linux advisory lock and scoped
process check reject overlap; a persistent attempt marker prevents automatic
retries after interruption or failure. It never resumes or overwrites an
existing output archive, changes fit domains, or invokes automatic dense refits.
The lock covers this wrapper; other manually launched tools must respect it
or avoid starting concurrent comparisons.

The scheduled output is `results/restarts/scheduled_baseline_20261105`.
The old `clean_benchmark_reviewed_routing_20261104` archive remains untouched
as provenance/reference evidence. The exact frozen driver and reviewer are
in the originating session's `files\clean_reviewed_routing_20261104_scripts`.
Those local files, WSL solver and likelihood packages are required dependencies;
their absence is a blocker, not permission to reinstall or substitute data.
The automation pins the wrapper and scorecard hashes; later source changes
require review before unattended execution.

The wrapper runs the frozen reviewer's audit in a separate process for minimum
reproduction, restart spread and dense fitted-point accuracy. Only a
`reviewed_in_sample` fingerprinted scorecard can complete the attempt.
An unresolved gate requires a new user decision, not repeated fitting to find
a favorable result. Logs/tests/scorecards live in the initiating automation
session's durable files, identified by the attempt marker beside the archive.
Later daily runs inspect or score this same attempt. The hourly read-only job
has subsequently been extended with user approval to inspect the scheduled
archive and missing research-channel inputs, while retaining its original
cadence/read-only limits and labeling the original interrupted archive separately.

Setup validation: **97 tests passed in 64.92 seconds on the actual WSL
interpreter**, including execution-lock and no-retry guards. The real
provenance-only check matched **274 files**. No new fit was launched during
setup; these checks do not establish a model preference.

The tracked independent-expansion backlog also includes cosmic chronometers
([covariance primer](https://gitlab.com/mmoresco/CCcovariance)), standard sirens
([gwcosmo data requirements](https://lscsoft.docs.ligo.org/gwcosmo/data.html)), and strong-lens
time delays ([TDCOSMO 2025 public analysis](https://github.com/TDCOSMO/TDCOSMO2025_public)).
These are cataloged validation routes, not installed likelihoods or scheduled fits. Before integration,
reproduce the standard-control analysis and fingerprint measurements, full covariance, selection,
calibration and nuisance assumptions. Chronometers need stellar-population systematic covariance;
sirens need posterior-prior/selection and host/catalog-completeness treatment; time delays need
mass-sheet, external-convergence and kinematics modeling. A local-gravity modification needs its
own lens-dynamics mapping. Do not replace these analyses with independent one-number H0 penalties.

The BC03/MM20 chronometer route now has a separate Cobaya likelihood in
`axiclass/chronometers.py` and focused tests. It uses the author's reference recipe: diagonal
measurement errors plus fully correlated IMF and `mod_ooo` covariance terms; the original
notebook's `numpy.interp` endpoint hold beyond the systematic table is retained and explicitly
flagged as a high-redshift systematic limitation. Inputs are fingerprinted in session artifacts,
not the repository data tree. The all-model reference-point preflight
`preflight_chronometers_20261105.py` passed on all three comparison branches. At those
unoptimized reference points, the chronometer chi-square contribution is 6.2423 (LCDM), 6.6044
(w0-wa), and 6.7412 (Late Twist); dropping the sole z=1.965 measurement changes each by only
0.0493–0.0995. These
are diagnostic likelihood contributions, not fitted scores or evidence for a model.

For standard sirens, official `gwcosmo` 3.1.0 and LIGO dependencies are isolated from the AEGIS
environment; an official GW170817 posterior/prior fixture is staged and structurally checked.
The bright-siren CLI `--help` smoke check passes, but Astropy warns that its optional IERS
update cannot reach the network. This is package/CLI validation only, not an inference preflight.
The current GWTC-3 v3 parameter-estimation release is also cataloged at
https://zenodo.org/records/22685054 (14.1 GB total; not downloaded wholesale). Matching
detection injections and host/line-of-sight redshift information are still missing. More
importantly, `gwcosmo`'s standard cosmology assumes a flat w0-wa background and
`dGW/dL = 1` by default. AEGIS has no validated adapter for its expansion history or a
theory-derived GW-versus-EM propagation ratio, so this is not yet a qualified AEGIS likelihood.

For strong lenses, the TDCOSMO 2025 source is pinned in session artifacts with its processed
inputs and 28 released posterior chains; isolated `hierarc`/lens-model dependencies and the
sampler import are checked. Published posterior chains are not a reproduced likelihood fit.
The reference runner uses a hard-coded author-cluster data path and standard cosmology families.
Portable likelihood parity, an AEGIS distance adapter, and a justified lens-dynamics mapping
remain blockers. The hourly cross-check automation remains audit/scorecard-only; no new
likelihood fits are scheduled or launched.

### Decision gates, not a search for a winning fit

`axiclass/comparison_scorecard.py --archive <benchmark-directory> --output <new-json-path>` starts
a read-only scorecard immediately, even while fits are pending. Output must be a new file outside the
benchmark archive. It SHA256-catalogs declared likelihood inputs, solver binary, adapter/patch and
JSON evidence; input drift blocks scoring. Only after all three minima and independent review gates
pass does it emit the three paired comparisons: chi-square, AIC, per-likelihood contributions and
shared bestpoint differences, alongside restart/dense diagnostics. Negative differences favor the
candidate named in each pair. It checks likelihood contributions reproduce the total; a zero hard-domain
constraint is not an extra observational dataset. This uses the declared benchmark/reviewer contracts,
not a new likelihood evaluation or proof of global optimality.
Cataloged files are rehashed after reading to detect changes during capture. Pending or blocked
reports list no available scores; they retain explicit pending requirements instead.
Summary pass flags alone do not unlock scoring: four restart records must reproduce the saved
minimum and spread, dense totals must reproduce their shifts, and the independent review must
cover exactly the declared models with consistent numerical evidence. JSON is validated before
creating a new output file so nonfinite content cannot leave a partially serialized scorecard.
Archived observational likelihood settings must match across models, not merely their column names.
Changes to the archive's JSON file set during capture also block scoring, including newly created
failure markers. These checks detect concurrent changes; they do not replace immutable run archives.

BIC, Bayes factors, posterior intervals, detection significance and held-out scores are explicitly
unavailable until their necessary inputs and validated analyses exist. There is no universal composite
"theory score." AIC is an in-sample complexity diagnostic under the declared likelihood objective, not
a detection probability. Keep the fingerprint catalog, sampled/derived labels and score availability
with every displayed comparison. This utility does not launch later fits or change current data.

Finish the running baseline before launching another expensive matched optimization. Lightweight DES Y3
pipeline design can proceed independently, but installs, reference evaluations and fits need their own
validated setup; the monitor does not perform them. If numerical or restart gates fail, correct the cause
in a separately labeled archive rather than relaxing thresholds or changing the active snapshot.

For each completed suite, report paired chi-square differences against both controls, per-likelihood
contributions, numerical/restart uncertainty and parameter-count penalties under the declared objective.
Do not compare absolute totals from different dataset suites as model improvements. Growth is a separate
robustness comparison, not automatically held-out evidence: the surveys overlap and its BAO/RSD measurements
are correlated. Best-point exports remain predictions, not measurement errors or posterior intervals.

Before interpreting a preference as a robust constraint, obtain matched profile-likelihood intervals or
converged posterior chains with explicitly stated priors/objective and equivalent nuisance treatment.
Before a predictive test, freeze the corrected-build model/parameters, observation selection, statistic,
covariance, nuisance handling and decision rule in a new preregistration. Select genuinely unused data or
account for training/test correlations, then evaluate without retuning on the test result. Preserve old
locked predictions rather than silently replacing them. Neither an in-sample improvement nor a successful
held-out test alone identifies the microscopic torsion mechanism.

The active run's launch manifest and frozen driver/reviewer snapshots in the originating session files are
authoritative for its identity and settings. Do not edit them midrun. The older
`clean_benchmark_verified_fnu_20261104` attempt was interrupted for invalid w0/wa routing and is not valid
comparison evidence. Other archived fits and locked predictions remain historical; do not delete them, use
them as active status, or mix them into the corrected comparison. An unchanged log or an existing PID alone
does not establish progress. Failed or unavailable checks remain explicit.

The [DESI DR2 public reference documentation](https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/README.html)
uses PR4/NPIPE high-l CamSpec plus combined Planck-ACT DR6 lensing in its default CMB combination.
Our PR3-lite first pass is a valid labeled comparison design, not identical to that reference.
Its public optimization products are posterior maxima; do not compare them directly with our
likelihood-only totals. The [ACT likelihood instructions](https://github.com/ACTCollaboration/act_dr6_lenslike)
specify primary-CMB corrections, convergence-spectrum conventions and accuracy requirements.
Maximum multipole alone does not establish accuracy, and the diagnostic export through ell=2500 is
not a replacement for an ACT likelihood adapter. Preserve matched neutrino species/mass/radiation
conventions and validate nonlinear-model assumptions away from the null before precision lensing claims.

`axiclass/observational_coverage.py` prepares a matched local growth variant for any baseline configuration:
`with_galaxy_growth(info, output)` replaces BAO likelihoods with `bao.sdss_dr12_consensus_final`. This uses the
published SDSS DR12 compressed joint distance/expansion/growth measurements at z = 0.38, 0.51 and 0.61, including
the full 9-by-9 covariance. It is not a raw full-shape analysis. `validate_growth_data(packages_path)` checks the
measurement order and positive-definite covariance before use. Do not stack this with overlapping DESI/SDSS BAO
data without a justified cross-covariance; keep the original DESI benchmark and the replacement growth suite
separate. Finite reference evaluations are preflight checks, not completed growth fits.
The growth and chronometer covariance checks require symmetry to relative
tolerance `1e-12` with no absolute tolerance floor, so changing covariance units
cannot allow a materially asymmetric matrix through to Cholesky evaluation.

`axiclass/observable_outputs.py` provides `evaluate_observables(info, point)` for a supplied parameter point,
using a copied configuration without launching a minimizer or writing to its output archive. All models share
11 redshifts from 0 to 2.5, 100 wavenumbers from 0.001 to 1 per Mpc, and CMB multipoles 2 through 2500.
The returned predictions include per-likelihood chi-square, H0, age, drag sound horizon, sigma8, physical
background matter fraction and S8, distances and BAO ratios, effective fsigma8, linear/nonlinear matter power,
and lensed TT/TE/EE/BB/pp spectra. The raw CLASS matter summary is retained separately; scalar-field diagnostics
are explicitly branch-specific. Background extrapolation, nonfinite arrays and missing required spectra fail
explicitly. Power is in Mpc cubed with k in inverse Mpc, not h-scaled units; CMB spectra are unweighted C_ell.
Exports at reference points are not fitted constraints or observations, and contain no posterior intervals.
The effective growth approximation needs separate validation for scale-dependent/coupled branches. This
exporter does not integrate DES Y3 or establish a Galactic torsion field; full shear still requires the
pipeline checks below.

The approved public DES Y3 release was staged under `packages/data/des_y3_release_f461f7181f8a`, pinned to the
CosmoSIS Standard Library commit recorded in its `release_manifest.json`. The FITS release includes shear
correlations, galaxy correlations, redshift distributions and covariance, plus the reference configuration,
priors and scale cuts. Data staging and covariance validation do not establish a working AxiCLASS/Cobaya
likelihood. The installed environment has no DES Y3 likelihood, CosmoSIS, FAST-PT or CCL implementation.
Do not relabel DES Y1 as Y3, use an unverified testing fork, or substitute a compressed S8 penalty for full shear.
Full Y3 integration must reproduce the public reference with matching scale cuts, source-redshift and shear
calibration treatment, TATT intrinsic alignments, nonlinear power, units and covariance selection. Preserve
instrument/calibration constraints even in likelihood-only runs; silently dropping nuisance priors is not an
equivalent survey analysis. Compare all cosmological models with the same validated observational pipeline.

Observational gaps still include raw galaxy full-shape modeling, full galaxy weak lensing, clusters, standard
sirens, and a calibrated Gaia orbit-residual likelihood. Tensor modes, curvature and variable neutrino sectors
are optional model extensions, not measurements already present in the current flat, fixed-neutrino benchmark.
The conditional photon-birefringence, gravitational-wave parity and BI-inflation predictions in
`theory/PREDICTIONS_LOCKED_2026-11-02.md` belong to distinct theory branches; they are not outputs of the one-field
Late Twist fit. Preserve the locked historical predictions and label corrected-build predictions as a new series.
