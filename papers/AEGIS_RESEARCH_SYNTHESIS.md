# AEGIS: theory, observational pipelines, and scientific-readiness synthesis

**Document type:** working research paper and cross-agent handoff, not a peer-reviewed
result or a completed theory-validation paper.

**Status captured:** 5 November 2026, 01:31 UTC (4 November, 19:31 Central time).
All live counts and process states below are timestamped snapshots, not promises
of current activity. Refresh them before taking action.

**Repository:** `dannyeldridge54/AEGIS`.
**Working checkout:** `C:\Users\Danny\.copilot\repos\AEGIS`, user-owned `master`.
The checkout already contains substantial modified/untracked work. Nothing in
this document authorizes reverting it, committing, pushing, or publishing.

## Abstract

AEGIS investigates scalar-field cosmologies motivated by Barbero-Immirzi (BI)
and torsion-related constructions while building separate observational and
software-validation pipelines. Its local evidence includes a complete,
parallax-selected Gaia DR3 tile archive; a separate ongoing DR3 resweep;
historical cosmology fits; staged CMB, supernova, distance, and growth data;
and newly prepared independent-expansion reference inputs. These channels
do not presently provide a single validated test of the microscopic torsion
mechanism. The corrected three-model cosmology benchmark has no completed,
independently reviewed matched comparison. Gaia flags are screening heuristics,
not detections or a cosmology likelihood. This paper assembles the current
scientific questions, provenance, implemented tools, negative results, missing
inputs, operational checks, and next-stage gates in one portable reference.

## 1. Scope and scientific distinctions

**Scope correction, 5 November 2026, 03:48 UTC:** retain the frozen comparison
as effective-model research. The n=3 potential is an assumed ansatz, not a
derived microscopic torsion prediction. The stated constant-superpotential
sector is axion-independent and cannot generate that potential. No full
coupled-field stability or independent observational confirmation is established.
Any eventual reviewed fit improvement supports only the specified effective
model on the stated likelihoods; it does not close those gates. Do not change
the running benchmark to repair this interpretation, and do not rewrite old
results. The corrected derivation and open-gate ledger are in
[`../theory/DERIVATION_CHAIN.md`](../theory/DERIVATION_CHAIN.md) and
[`../theory/README.md`](../theory/README.md). These are interpretation limits,
not a substitute for a microscopic calculation or perturbation analysis.

Four activities must remain distinct:

1. Derivations and conditional predictions from explicitly stated field-theory inputs.
2. Effective cosmological models evaluated against cosmological likelihoods.
3. Observational catalogue screening and follow-up, especially Gaia Star Mapper.
4. Software, numerical, provenance, and operational tests.

A software regression pass is not a physical detection. A null-equivalence test
is not independent agreement with observations. An in-sample fit improvement
does not establish a microscopic mechanism. Missing data are unavailable, not
zero candidates. Historical outcomes, failures, and withdrawn claims must remain
visible rather than being replaced with the latest favorable result.

The repository also contains a TypeScript agent framework (`src`, `agent`,
`dist`, `package.json`). That software is not an astronomical dataset and its
tests do not validate the physical theory.

## 2. Theory branches and what is actually derived

The canonical BI/supergravity calculations and their assumptions are recorded
in [the derivation chain](../theory/DERIVATION_CHAIN.md) and
[the theory-tool guide](../theory/README.md). The kinetic geometry follows from
the quoted Kahler input and chosen field orientation. The constant-superpotential
calculation does **not** derive the stable positive periodic potential assumed
in the phenomenological Twist fits.

The QCD-anomaly branch uses an effective leading-cosine potential. Its
homogeneous evolution and rapid-oscillation/CDM approximation are a separate
calculation, not the equality-locked, cubic-cosine EDE potential and not late-time
quintessence. A requested equality-era density normalization is not an inferred
parameter or a prediction. Effective-limit consistency checks do not replace
an independently implemented scalar perturbation hierarchy.

The early-dark-energy workflow uses a torsion-motivated effective scalar model
and comparisons with standard cosmology. Equality locking, width/divisor choices,
and fingerprint-potential assumptions must be identified as assumptions where
they are not derived.

The current corrected benchmark concerns **effective one-field Late Twist**,
standard LCDM, and flexible w0-wa. It is not a completed fit of the full two-field
Spiral Twist or an interchangeable result for every AEGIS branch.

The local weak-field branch has conditional coupling/Cassini calculations but
no validated star-sourced field profile, effective-mass/screening solution, or
Galactic orbital residual prediction. Reading B's zero direct matter coupling
is an assumption. Its unchanged Gaia overlay is consequently a pipeline/null
check, not observational support for torsion.

### Open theory questions

The potential's microscopic origin; equality-era onset; initial conditions;
field width and divisor; two-field versus effective one-field validity; local
screening and lens dynamics; gravitational-wave versus electromagnetic distance
propagation; and non-null nonlinear matter-spectrum validity remain open.
Gaia anomalies or a changed inferred Hubble constant cannot fill these gaps.

## 3. Local observations and provenance

The inventory was based on file metadata, manifests, bounded schema inspections,
saved checks, and tool/source review. It was **not** a new read of every source
row or a complete integrity hash of every multi-gigabyte archive.

| Channel | Locally present evidence | Qualification and remaining gaps |
|---|---|---|
| Legacy Gaia systematic sweep | 12,288 level-5 tiles; state records 192,208,838 selected rows; about 17.47 GB compressed tiles | Complete for the declared selection, not all Gaia sources or an unbiased Milky Way census; saved all-tile local/ESA count audits match |
| Active Gaia resweep | Run `gaia-full-20261104T025414Z`; 529/12,288 completed tiles, 25,291,715 rows at capture; 24/24 retained ESA count checks match | Separate archive, non-random completion order, mixed tile schemas; do not combine with the legacy count |
| Legacy Gaia random-patch exports | `cosmos_map_stars.csv`, `cosmos_map_flags.csv`, patch history and summary | Distinct scanner/denominator; overlapping encounters, truncated patches, and stale summary risks |
| Impact structures | 45 records plus stored result | Best scanned period 27.65 Myr, scan-corrected p=0.3325: no significant rhythm in this test; age uncertainties are not propagated |
| Exoplanet period ratios | Preregistration and analysis code | `exo_rows.json` and `exo_result.json` absent from the working research directory; historical dashboard/ledger pass is not locally reproduced |
| Cosmology package/data tree | Planck, ACT, BAO/RSD, supernova, SPT and DES Y3 reference inputs | Roughly 5.67 GB in `cmb-fit` includes software/results/duplicates, not 5.67 GB of independent observations; each actual likelihood needs qualification |
| Cosmic chronometers | BC03/MM20 inputs and author covariance recipe, separate adapter | Finite reference-point preflight exists, no matched fit |
| Standard sirens | GW170817 posterior/prior manifest; external software/reference source | No complete selection/injection and host/catalog-completeness setup or validated AEGIS propagation adapter |
| Strong-lens time delays | Pinned TDCOSMO 2025 source, processed inputs, 28 released chains | Released chains are not a reproduced fit; portable reference parity, distances, and lens-dynamics mapping remain blocked |
| Theory arrays and summaries | About 107 MB in `theory`, including generated spectra/dynamics arrays | Predictions/calculations, not additional observational measurements |
| Backups and bundles | `handoff_backup`, `v2-update`, paper release trees | Historical transport/publication artifacts; do not count duplicated contents as independent evidence |

### Gaia selection and uncertainty boundary

The scanner uses Gaia DR3 source-ID HEALPix ranges with
`parallax_over_error > 5`, an ordered paginated query, and a left join by
`source_id` to `external.gaiaedr3_distance`. The completed legacy archive is
complete only for this selection. Selection, crowding, extinction, sky coverage,
and missing radial velocities affect what can be inferred.

Gaia DR3 astrometry is shared with EDR3. Bailer-Jones geometric distances use
Gaia astrometry and a Galactic prior; they are not an independent distance
experiment. The 16th/84th-percentile interval is not automatically a Gaussian
standard error. The scanner's mismatch-width cut is not a calibrated
three-sigma test.

The legacy schema lacks retained uncertainties. Newer tiles in the active run
retain parallax error, proper-motion errors/their correlation, and Bailer-Jones
bounds. Neither existing schema has all zero-point and covariance inputs.
This corrects the earlier overbroad statement that every active tile lacks
uncertainty fields.

ESA count checks validate counts for the query selection, not row-by-row source
values, calibrated anomaly labels, independent distances, or a torsion model.
Catalogue release, measurement epoch, download time, filesystem modification,
and report generation are different timestamps.

## 4. Implemented diagnostics and changes in this pass

Star Mapper provides the dashboard, livestream, status/checks, tile downloads,
and immutable timestamped anomaly JSON/Markdown reports. The observational
report excludes cosmology/theory claims and labels missing candidate exports
explicitly. The current sweep has no run-level candidate CSV export; its row
evidence exists in tiles, not a claimed populated candidate report.

The screening flags are high tangential velocity, excess RUWE, and parallax/
geometric-distance mismatch. They identify follow-up candidates only.
Potential binaries require NSS/literature checks; high-velocity interpretations
require uncertainty propagation, radial velocity and an orbit model. Known
Gaia data issues must be consulted before treating an NSS entry as confirmation.

### Installed, but not hot-loaded into the scanner

The acquisition code now retains raw unrounded parallax, reference epoch,
astrometric solution type, effective colour/pseudocolour/ecliptic latitude,
positional errors, all ten correlations of the five astrometric parameters,
and radial-velocity error. It records each newly written tile's column list
and acquisition query. The sixth pseudocolour dimension is not fully retained.
No zero-point correction, uncertainty propagation, or significance calculation
has thereby been implemented.

All 17 additional non-parallax field names were found in the official DR3
datamodel (HTTP 200). A direct live TAP-schema request returned HTTP 503.
Documentation/schema checks and offline tests do **not** establish a successful
full sweep-range acquisition query; that preflight remains required. A later
single-source live test succeeded, as recorded in the operational update below.

The running Python process is not hot-reloaded. Its loaded query and new tiles
still use the prior uncertainty-enabled schema. A homogeneous schema-complete
baseline therefore needs a separately named, validated run or a separately
versioned enrichment product. Completed tiles have not been rewritten.

Resume now refuses malformed/incompatible state and missing completed-tile
evidence rather than silently dropping records or restarting acquisition.

### Matched-control hold

By explicit user decision, matched-control analysis remains on hold until
schema-complete inputs are available. The provisional tool now checks all
headers before expensive archive reads/hashes, rejects missing schema fields,
malformed rows, count mismatches and changing tile fingerprints. It rejects
partial sweeps by default. Its synthetic tests now pass, but no real-archive
control report has been generated.

Even its permitted output would be **descriptive stratum counts only**:
same-tile/photometry/SNR strata and flag-specific distance strata, clean-row
controls, no calibrated p-values or corrected anomaly rates. Solution type
is retained but not yet used in matching; matching counts are not selected
source pairs, independent replicates, or theory scores. Header presence does
not prove every row contains usable values.

### Historical display correction

`science.json` and the livestream now explicitly label cosmology/result cards
as historical, not live fit status. The exoplanet pass is marked unreproducible
locally. The claim ledger retains historical outcomes; its structural wall/hash
checks must not be mistaken for reproduction of a missing dataset.

## 5. Corrected cosmology comparison

The designated archive is:

`cmb-fit\results\restarts\clean_benchmark_reviewed_routing_20261104`.

Its declared common suite is Planck 2018 low-l, high-l lite and lensing, DESI
DR2 BAO and Pantheon+. The design uses a separate corrected AxiCLASS build,
four restarts per model, explicit parameter routing, matched nuisance settings,
and likelihood-minimum objectives within stated domains.

The archive's comparison JSON explicitly says **"Unfitted null-test seed only."**
Saved null, spectra, and routing gates do not supply matched minima.
No matching fit/reviewer process was present in the scoped process check.
Do not infer global process absence from that check, or relaunch a historical
job merely because a PID or old log exists.

Necessary final gates include uncached minimum reproduction, restart spread,
fitted-point dense numerical accuracy, matching likelihood settings/provenance,
and exact independent review coverage. Earlier work found that excellent
differential null agreement can coexist with a material absolute dense
likelihood shift; fitted-point accuracy checks remain essential.

`comparison_scorecard.py` fingerprints declared inputs/solver/adapter/evidence,
detects changes during capture, and refuses scores until its evidence contract
is satisfied. Passing summary booleans alone cannot unlock comparisons.
No reviewed three-model scores are presently established here.

Report paired likelihood/AIC differences and per-likelihood gains **and losses**
only within a matched suite. Do not compare absolute totals from different
dataset combinations. AIC is not a detection probability; BIC, Bayes factors,
posterior intervals, profile intervals, and genuinely held-out scores require
their own justified inputs/analyses. There is no universal combined theory score.

Historical early-EDE CAMB/AxiCLASS figures in earlier papers and dashboards are
not new scores for the corrected Late Twist suite. Do not silently rewrite
published/historical numerical claims using an incomplete new benchmark.

## 6. Independent and robustness pipelines

| Pipeline | Current verified/prepared stage | Next scientific gate |
|---|---|---|
| Common observables | Shared-grid reference exports; exporter installed | Export reviewed fitted points; state units, conventions and absence of posterior intervals |
| SDSS DR12 joint BAO/RSD | Nine-measurement/full-covariance reference preflight | Separate matched fits replacing overlapping BAO; validate compressed-growth applicability |
| Publication-reference CMB | Identified PR4/NPIPE high-l plus Planck-ACT lensing route | Reproduce official corrections, nuisance handling and numerics, then matched controls; avoid overlapping-data double counting |
| DES Y3 shear | Public inputs staged | Official likelihood/cuts/covariance/TATT/redshift/calibration parity and AxiCLASS all-model validation |
| Chronometers | Separate Cobaya adapter and three-model reference preflight | Matched suite and systematic sensitivity; no inference from reference-point ordering |
| Sirens | Pinned posterior/prior fixture and isolated CLI/package checks recorded | Selection/injections, independent host redshifts/completeness, posterior-prior handling and AEGIS distance/propagation interface |
| Time delays | Pinned source/inputs/released-chain structure checks | Portable reference likelihood parity; mass-sheet/external-convergence/kinematics and AEGIS mapping |
| Local gravity and parity | Conditional calculations/backlog | Explicit coupling/propagation prediction and applicable likelihood before testing |

The recorded chronometer reference chi-square contributions are 6.2423,
6.6044, and 6.7412 for LCDM, w0-wa, and Late Twist. These are **unoptimized
reference points**, not best-fit rankings. Its author-recipe systematic
interpolation holds the endpoint beyond z=1.475; the z=1.965 sensitivity test
is recorded, not a refit.

The siren fixture has 8,078 posterior samples and an explicit PE-prior manifest.
Catalogue redshifts derived under a fiducial cosmology are not independent host
redshifts. Do not replace siren or lens analyses with independent one-number
Hubble-constant penalties. TDCOSMO's reference chain includes Pantheon+, so
additional use must account for overlap.

## 7. Operational status and scheduling

At capture the monitor was `scanning`, with two workers and no application
error. Dashboard, `/live`, anomaly JSON, and anomaly Markdown returned HTTP 200.
It advanced from 526 to 529 completed tiles during this pass. The existing
scanner process (PID 1030 in the scoped WSL check) was neither stopped nor
restarted. The historical-display changes were observable through `/api/science`;
clients must reload the page to pick up edited HTML.

**Low-credit revision, approved 4 November 2026 at about 20:06 Central:**
The same audit ID is now enabled as **AEGIS lightweight cross-checks**, cron
`29 */6 * * *`, Auto efficiency. It makes four short read-only checks per day,
rather than 24 hourly checks, and reads bounded recorded attempt summaries
instead of rehashing inputs/recomputing scorecards or revisiting the full
scientific backlog. This is 83% fewer audit invocations, not a guaranteed credit
saving percentage. The 22:00 daily one-attempt comparison remains unchanged.
No duplicate job, immediate run, restart, cleanup or additional fit was created.
The app and machine must be available. Earlier hourly-audit descriptions below
record the previous configuration and are superseded by this revision.

Previously, the local **AEGIS hourly cross-checks** automation was enabled:
ID `10762a61-8378-47ba-b9a9-1a81158f91a8`, cron `29 * * * *`.
The 01:29 UTC run was reported running; next scheduled time was 02:29 UTC.
It performs bounded read-only audits and lightweight scorecard generation,
not expensive fits, integrations, downloads, restarts or data acquisition.
It needs the local machine/app and permitted source/artifact access.

Subsequent user-approved update: the same hourly job now separately checks
the new `scheduled_baseline_20261105` attempt when it exists and reports
research-channel input gaps. Its cadence and read-only/no-fit boundaries are
unchanged. It never substitutes the old archive for missing new results.

The retired Gaia-only automation
`095c09ef-2f43-4d0c-bd32-a5506c36035b` remains disabled. No automation was changed
or manually launched in this pass. A schedule or a completed automation task
does not establish a completed scientific fit.

### Subsequent user-approved scheduling update

After the snapshot above, the user approved a local daily 22:00
test-first comparison job. `AEGIS gated theory comparison`, ID
`6909b65b-0735-4d73-95d4-c8af44b20ea4`, was saved and read back enabled.
Its first app-reported due time is 5 November 04:01:09 UTC. The original
hourly audit and retired Gaia-only job were not changed.

The installed `cmb-fit\axiclass\scheduled_comparison.py` verifies frozen
provenance and prerequisite gates, runs regression tests, and permits one
new matched LCDM/w0-wa/effective Late Twist attempt in
`cmb-fit\results\restarts\scheduled_baseline_20261105`. A lock/process guard
and persistent attempt marker prevent overlap and automatic refitting.
It uses the frozen reviewer's audit in a separate process, then the
fingerprinted scorecard; failed accuracy/restarts do not trigger automatic
dense refits. See `cmb-fit\README.md` for execution limits and local dependencies.

The real WSL regression command covered `cmb-fit\axiclass\tests` and the four
Gaia/UFE test files listed below: **97 passed in 64.92 seconds**. A separate
provenance-only run verified **274 files** without launching a fit.
The expanded Gaia query was retried once and still returned ESA HTTP 503.
The running scan was left intact; at the later check it was scanning,
538/12,288 tiles and 25,545,227 selected rows, with no reported application error.
No new fit has run merely because this schedule was saved.

### Subsequent ESA 503 diagnosis

The same expanded single-source query subsequently returned one public Gaia
row through WSL POST in 7.52 seconds and through native Windows GET with
HTTP 200. Both returned the requested raw astrometry/covariance-input columns
and the joined Bailer-Jones median/lower/upper distances. This demonstrates
that the expanded columns and join can be served; it does not establish
that the earlier 503 is permanent, nor identify its precise cause.

The exact installed source-range query, tested on that one source with its
SNR filter and ordering, timed out through both WSL POST and native GET.
Thus range-query completion, sustained throughput and a homogeneous expanded
run remain unvalidated. No scanner restart, endpoint replacement or fallback
was installed. Small explicit source-ID enrichment is a verified access route;
bulk asynchronous TAP or the documented ARI service requires its own
schema/selection/provenance preflight before replacing acquisition.

## 8. Reproduction and handoff map

Read this paper first, then the named primary source and manifest for the task.
Use live evidence rather than historical process IDs or this paper's counts.

| Task | Primary repository location |
|---|---|
| Gaia collection/query and row schema | `ufe-v2\aegis\star_scanner.py`, `ufe-v2\aegis\sweep.py` |
| Offline reports and HTTP presentation | `ufe-v2\aegis\anomaly_report.py`, `ufe-v2\monitor_server.py`, `ufe-v2\monitor.html`, `ufe-v2\live.html` |
| Provisional controls and hold checks | `ufe-v2\aegis\matched_control.py`, `ufe-v2\tests\test_matched_control.py` |
| Legacy/full Gaia evidence | `ufe-v2\cosmos_map\tiles\L5`, `sweep_state.json`, `verify_all.json`, `verify_local.json` |
| Current independent Gaia archive | `ufe-v2\cosmos_map\runs\gaia-full-20261104T025414Z` |
| Theory/assumption ledger | `theory\DERIVATION_CHAIN.md`, `theory\README.md`, `papers\theory_note\spiral_twist_note.tex` |
| Cosmology design and coverage | `cmb-fit\README.md`, `cmb-fit\axiclass\early_late_spa.py`, `observational_coverage.py` |
| Score/provenance and common predictions | `cmb-fit\axiclass\comparison_scorecard.py`, `observable_outputs.py` |
| Chronometer likelihood | `cmb-fit\axiclass\chronometers.py` and its focused tests |
| Separate terrestrial/planet analyses | `research\impacts`, `research\exoplanet_locks` |

Additional pinned data, launch manifests, frozen scripts and reference
preflights live outside Git under:

`C:\Users\Danny\.copilot\session-state\140cec95-10b4-4eb8-af24-c664085ac6b3\files`.

Important artifacts include `clean_reviewed_routing_20261104_launch.json`,
`clean_reviewed_routing_20261104_scripts`, `first_pass_evidence_log.md`,
`observational_coverage_inventory_20261104.json`,
`scientific_comparison_standards_20261104.md`,
`additional_validation_opportunities_20261104.md`,
`star_mapper_frozen_baseline_20261105.json`, and
`independent_validation_20261104`.

The frozen Star Mapper snapshot records 520 tiles, not the current count.
The independent-validation folder contains source/data hashes and reference
metadata, including `staged_reference_data_20261105T005614Z.json` and
`chronometer_reference_preflight_20261105T005438Z.json`.
Other agents/clones may not have access to these paths. Report that blocker;
use supported artifact transfer rather than inventing input files or silently
substituting a different release. This paper does not embed the full datasets.

### Validation performed for this pass

From the repository root, using the existing Windows Python 3.12 environment:

```powershell
$env:PYTHONPATH = Join-Path (Get-Location) 'ufe-v2'
& '.\cmb-fit\venv312\Scripts\python.exe' -m pytest -q `
  ufe-v2\tests\test_anomaly_report.py `
  ufe-v2\tests\test_scanner_readiness.py `
  ufe-v2\tests\test_matched_control.py `
  ufe-v2\tests\test_v2.py `
  --basetemp 'C:\Users\Danny\.copilot\session-state\140cec95-10b4-4eb8-af24-c664085ac6b3\files\pytest-readiness-20261105-0130'
```

Result: **45 passed in 1.56 seconds**. The ordinary Windows pytest temp root
was inaccessible; a new isolated session-artifact directory resolved setup.
Two defects in the previously untested draft test fixtures were corrected.
Use a new empty `--basetemp` path for subsequent runs; do not clear historical
test outputs or broad session directories.

These tests cover offline report behavior, schema retention, resume guards,
tile provenance, historical labels, control hold/input checks and existing
UFE regressions. They do not reproduce a cosmology fit, calibrate Gaia
significance, validate the expanded live query, or validate all external packages.

A read-only preflight of both real archives also refused analysis as intended:
the full legacy archive lacks required uncertainty columns, and the active
archive was incomplete at 531/12,288 tiles. No control report was produced.
Changed tracked files passed the scoped whitespace check. The whole-checkout
check still flags pre-existing whitespace in unrelated theory JSON files;
those existing changes were preserved.

## 9. What should happen next

The system is starting correctly **as a resumable, partial DR3 catalogue
collection**, not as a schema-complete scientific baseline or theory test.
Leave it running unless a specific operational intervention is approved.

First validate the expanded Gaia query against the available archive service.
Then decide explicitly between a separately named homogeneous run and a
versioned targeted enrichment product; preserve both existing archives.
Do not run the held matched-control analysis on mixed or incomplete inputs.

For cosmology, resolve the interrupted/incomplete corrected benchmark and
independent-review prerequisites before scoring or launching another expensive
suite. Freeze any genuinely predictive test's model/parameters, observation
selection, covariance, nuisance treatment and decision rule before evaluation.
Retuning on the purported holdout invalidates the predictive interpretation.

Preserve all measurements, archive versions, failed/interrupted attempts and
unfavorable comparisons. Exclude inputs only for documented quality,
applicability or overlap reasons established independently of whether they
favor AEGIS. An unusable input remains in the provenance record with its
exclusion reason; it is not silently deleted or counted as supporting evidence.

Restore the actual exoplanet source/result provenance if available; otherwise
keep its local outcome unavailable. Improve crater dating/source provenance and
age-uncertainty treatment before interpreting a periodicity scan.

### Future online comparison dashboard (user-requested backlog)

TODO: add read-only scorecard/comparison views to the online setup after the
local comparison contract is validated. This is a future integration idea,
not an authorized upload, deployment, or replacement for the missing Zenodo
record.

Serve immutable scorecards tied to an explicitly selected archive, never an
unqualified "latest winning fit." Show pending, blocked, interrupted and
reviewed states; distinguish report generation time from input timestamps;
display archive identity, source fingerprints, independent-review status and
staleness. Missing evidence must render unavailable, not zero or a pass.

For reviewed matched suites, show all three candidate-minus-control comparisons,
chi-square/AIC differences, parameter counts, per-likelihood gains and losses,
restart spread and dense-accuracy shifts. Keep different dataset combinations,
historical fits, effective-model comparisons and Gaia screening separate.
Do not display AIC as a detection probability or imply microscopic torsion
confirmation. Link each presentation to its downloadable JSON and evidence
catalogue; preserve prior versions.

Acceptance: API and dashboard fixtures cover pending, failed, stale, drifted
and reviewed archives; no score is exposed before the validated scorecard
gate permits it. Public deployment requires a separate decision about host,
access and which local artifacts may be shared.

### Astronomy-driven filtering and research channels

The user chose **KAIROS** for this observation/follow-up workspace, alongside
their JANUS/CHRONOS naming theme. AEGIS remains the umbrella; this name changes
presentation, not the physical theory, solver, dataset identity or evidence
contract. No roles for separate JANUS/CHRONOS systems are established here.

Published workflows, rather than an informal poll of astronomers, motivate
the additions. [GaiaUnlimited](https://gaiaunlimited.readthedocs.io/en/latest/)
provides survey/subsample selection functions; its
[binary-detectability example](https://gaiaunlimited.readthedocs.io/en/latest/notebooks/dr3-unresolved-binaries.html)
describes sky/crowding-dependent RUWE thresholds and warns that the feature is
under development. [TOPCAT](https://www.star.bristol.ac.uk/~mbt/topcat/)
illustrates practical needs for table metadata, subsets, crossmatching,
linked plots and export. These are methodological sources, not endorsements
of AEGIS or proof of a universal quality cut.

Implemented now: non-destructive radial-velocity availability and usable
partial-uncertainty view filters, preserving valid zero and exposing incomplete
inputs; filtered JSON with source/report provenance and bounded-parent scope;
prospective raw astrometry retained in candidate JSON. The views cover only
the first 40 displayed candidates from the bounded export, not the full sweep.
The active sweep lacks a candidate CSV, so this does not invent source rows
from aggregate counts.

The report/dashboard also include eight reference-only research routes:
Galactic assembly/dynamics, unresolved binaries, asteroids/comets, meteors,
interstellar small bodies, exoplanets, pulsars/neutron stars, and black holes.
Each states its question, authoritative sources, required observations and
unsupported inference. No new detection or object-type classifier is installed.

Solar System work must use time-tagged moving-object astrometry and validated
orbits, not the star catalogue. Sources include
[ESA's separate Gaia SSO catalogue](https://www.cosmos.esa.int/web/gaia/dr3-solar-system-objects),
[MPC confirmation candidates](https://www.minorplanetcenter.net/iau/NEO/toconfirm_tabular.html),
[JPL close approaches](https://ssd-api.jpl.nasa.gov/doc/cad.html) and
[fireballs](https://ssd-api.jpl.nasa.gov/doc/fireball.html), and the
[Global Meteor Network](https://globalmeteornetwork.org/).
Close approach is not impact probability. Fast motion or nominal eccentricity
above one alone does not classify an interstellar object; missing fireball
velocities and uncertainties remain missing.

For [exoplanets](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html),
preserve per-reference system consistency and candidate dispositions: PS
contains multiple rows per planet/reference, while PSCompPars can mix parameter
sources. New candidates need light curves/RV and blend/activity validation.
[ATNF](https://www.atnf.csiro.au/research/pulsar/psrcat/) supplies pulsar
parameters/timing references; optical matches alone cannot detect a pulsar.
[HEASARC](https://heasarc.gsfc.nasa.gov/W3Browse/) and SIMBAD support
multiwavelength/literature follow-up, but emission or excess RUWE alone cannot
establish a black hole or dynamical mass.

Keep expensive science gated by input readiness, not simply a wall-clock
schedule. Existing one-minute view saves, ten-minute reports/ESA count checks,
hourly health/provenance audits and one fixed daily comparison attempt are
operational cadences, not automatic full-data inference. Per-source covariance
validation, selection correction, epoch-aware/ambiguity-aware crossmatches,
time-series/orbit analysis and false-positive calibration remain missing.

### KAIROS test-environment and scorecard result

The configured WSL test scope was rerun after these additions, using the
existing `/home/syndyr/micromamba/envs/aegis/bin/python`, `pytest -q -p
no:cacheprovider`, `cmb-fit\axiclass\tests` and the four Gaia/UFE files:
`test_anomaly_report.py`, `test_scanner_readiness.py`,
`test_matched_control.py`, `test_v2.py`. Result: **99 passed in 56.60 seconds**.
The dashboard command `node --test ufe-v2\tests\test_candidate_filters.cjs`
passed **5 tests**, covering finite/missing/zero inputs, filter composition,
invalid uncertainty ranges, provenance-preserving export and script/control
checks. These are software checks, not discovery or theory scores.

The installed scientific scorecard was executed against the original
`clean_benchmark_reviewed_routing_20261104` archive. Its preserved output is
`files\kairos-review-scorecard-20261105-0220.json` in the originating session.
Result: **pending**, with no reported fingerprint errors. All three model
results and `post_run_review` are missing; numeric comparisons are unavailable.
Evidence catalogue SHA256:
`32f1f9656e35a2932a797e20a099106ce937cd4648f229cf937fc51615f8a48c`.
The new scheduled archive did not yet exist; it was not replaced by old scores.

A new immutable reporter-3.4 report pair was generated in the active run:
`anomaly_report_20261105T015711142270Z_3418005a.json` and `.md`.
The HTTP endpoint served version 3.4 and all eight research reference routes;
the file-backed main dashboard served KAIROS and the new filter/export controls.
The active run still has no candidate CSV, so no row-level candidates were
invented. The old running report worker may later publish a 3.3 report until
its process is restarted; this new report stays preserved, and older-report
compatibility remains. The expanded acquisition code is still not loaded.

At 5 November 01:57:45 UTC, collection was scanning at 564/12,288 completed
tiles and 26,342,890 selected rows, with 25/25 retained ESA count checks matching
and no reported application error. No scanner restart, catalogue rewrite,
new fit, download, commit or public deployment was performed in this update.

## 10. Online checks and references

### Subsequent bounded bug/readiness review

Found and fixed: the main dashboard loaded a saved report only once; failed
requests could leave stale candidate exports available; repeated rendering
could duplicate flag options; switching to an older report could retain
research-channel labels from a newer report. It now polls reports every
60 seconds, reports the actual fetch/render error, disables stale exports,
preserves only applicable flag selections and clears absent research metadata.
The expanded dashboard regression suite passed **8 tests**. Reload the main
dashboard to load these JavaScript changes; no scanner restart is required.

Additional fixes: rejected malformed/non-ASCII Gaia IDs in candidate exports,
preserved numeric zero and escaped Markdown table cells, and excluded invalid
distance intervals from matched-control strata. A Python test in the existing
scheduled test directory now runs the Node dashboard suite, using the existing
Windows Node executable through WSL when needed. Missing Node or dashboard test
failure blocks the test gate before any fit attempt. No wrapper hash, schedule
or one-attempt policy was changed.
After these fixes, the entire existing scheduled validation scope passed
**112 tests in 65.30 seconds**, including the eight Node dashboard regressions.
The primary dashboard and saved JSON endpoint returned HTTP 200 and the served
HTML included the one-minute report timer. Reporter and matched-control changes
are installed for new processes; the existing scanner was not restarted.

Additional gaps remain explicit:
no tested backup/restore mechanism was established in this review; no
completed scheduled scientific attempt exists yet. The periodic report worker
and expanded acquisition are not hot-reloaded. Full-catalog candidate
extraction, uncertainty/selection calibration and object-specific measurements
remain scientific prerequisites. This bounded review does not certify the
whole dirty checkout or all dependency/software versions as bug-free.
Storage headroom was about 594.1 GiB on C: at 01:59 UTC, so capacity was not
an immediate blocker; free space is not a backup.

Accessed 4 November 2026 Central time / 5 November UTC:

1. [Official Gaia DR3 source datamodel](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html):
   parameter definitions, covariance fields, quality indicators and units.
2. [ESA EDR3/DR3 analysis code](https://www.cosmos.esa.int/web/gaia/edr3-code) and
   [the linked zero-point implementation](https://gitlab.com/icc-ub/public/gaiadr3_zeropoint):
   magnitude/colour/position and five-/six-parameter-dependent correction.
   Subtract the returned zero point from archive parallax. Do **not** reapply
   the EDR3 six-parameter G correction to Gaia DR3; ESA says it is already applied.
3. [Gaia DR3 known issues](https://www.cosmos.esa.int/web/gaia/dr3-known-issues):
   published IPD-statistic defects and specific false-positive NSS orbits.
4. [ESA Gaia science performance](https://www.cosmos.esa.int/web/gaia/science-performance):
   crowded-field completeness and measurement limitations.
5. [Gaia DR4 overview](https://www.cosmos.esa.int/web/gaia/dr4) and
   [release events](https://www.cosmos.esa.int/web/gaia/dr4-events):
   2 December 2026 release planning; DR4 source consolidation/data structure
   changes require a distinct release-aware pipeline, not a renamed DR3 run.
6. [DESI DR2 reference products](https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/README.html),
   [ACT lensing instructions](https://github.com/ACTCollaboration/act_dr6_lenslike),
   and [Cobaya documentation](https://cobaya.readthedocs.io/):
   earlier source-verified comparison requirements are preserved in the
   scientific-standards artifact and `cmb-fit\README.md`.
7. [Chronometer covariance reference](https://gitlab.com/mmoresco/CCcovariance),
   [gwcosmo data requirements](https://lscsoft.docs.ligo.org/gwcosmo/data.html),
   and [TDCOSMO 2025 reference release](https://github.com/TDCOSMO/TDCOSMO2025_public):
   source-pinned local preparation, not new likelihood fits.

The open [Zenodo record 23934537](https://zenodo.org/records/23934537)
returned **HTTP 410 Gone** in this pass. It is not a usable publication reference.
Do not assume another DOI is the same paper/version, or upload/replace a release
without explicit publication approval. Existing theory-note references require
their own version/content verification.

## Conclusion

AEGIS has useful observational archives, implemented numerical tools, explicit
null/regression tests and several prepared validation routes. The strongest
currently established Gaia result is reproducible selected-row accounting;
the strongest new changes are input retention, failure visibility and scientific
status separation. Neither establishes a torsion detection. Completion requires
schema-appropriate observations, defensible controls/systematics, matched
reviewed cosmological fits and explicit theory-to-observable mappings.
