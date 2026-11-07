# AEGIS UFE v2 — Torsion-Born EDE engine (reference implementation)

Drop-in replacement for the v1 "UFE" cosmology physics on branch
`dannyeldridge54-ufe-model-comparison-engine`. Read `AEGIS_UFE_v2_Copilot_Brief.pdf` first.

| File | Purpose |
| --- | --- |
| `aegis/cosmo_v2.py` | Models (ΛCDM, legacy β with flatness fixed, full Barbero–Immirzi torsion field), sound horizon, distances |
| `aegis/data_v2.py` | DESI DR2 BAO, Planck θ*, ω_b prior, SH0ES and Local Distance Network H0 |
| `aegis/likelihood_v2.py` | CMB θ* + DESI DR2 BAO (correlated) + Pantheon+ (full cov, analytic M) + optional local H0 |
| `run_v2.py` | Fits all three models with and without the SH0ES prior; writes `results_v2.json` |
| `tests/test_v2.py` | 8 acceptance tests |
| `data/pantheon/pantheon_binned_fullcov.json` | Pantheon+ 40-bin full-covariance data (copied from the repo) |

```
pip install numpy scipy
python tests/test_v2.py       # 8 PASS lines
python run_v2.py              # ~1 hour on a laptop; prints and saves the results
```

The reference supernova loader requires matching finite bin vectors, positive
ordered redshifts, and a finite symmetric positive-definite covariance.
Absolute-magnitude elimination projects centered residuals instead of
subtracting two large quadratic forms, preserving common-offset invariance.
Nonfinite likelihood outputs are rejected explicitly; the optimizer wrapper
logs numerical rejection and retains its existing `1e12` penalty. Unexpected
programming errors are no longer silently converted into that penalty.
These checks do not replace the full AxiCLASS/Cobaya cosmology pipeline.

### Offline Star Mapper anomaly reports

**KAIROS** is the observation/research-follow-up workspace within AEGIS, named
for the opportune moment. This is a presentation name, not a new solver or
detection engine; existing Gaia Star Mapper commands, report schemas and
archive identities remain unchanged. It can sit alongside the user's
JANUS/CHRONOS naming family without assigning or changing those systems' roles.

From `ufe-v2`, run `python -m aegis.anomaly_report`. This **does not start the
monitor or scanners, access the network, or run fits**. It creates a new timestamped
JSON/Markdown pair in `cosmos_map\anomaly_reports\` on every run, without modifying
any previous evidence or report. That directory is ignored by Git; keep the local
files if you need the history. `--max-rows 1000` reduces the default bounded read
of 20,000 flag rows (maximum 20,000).

For an isolated full Gaia resweep that preserves the default archive, start the
monitor with a new safe run ID, for example
`$env:AEGIS_RUN_ID='gaia-full-20261104'; python monitor_server.py`. Its tiles,
state, verification telemetry, and reports are written under
`cosmos_map\runs\<id>\`; the existing `cosmos_map` data is not cleared or reused.
Restarting with the **same** run ID resumes its completed tiles; use a different
ID only when you intentionally want a separate archive. The monitor creates an
immutable report at startup and refreshes it every ten minutes. `/api/status`
includes the report timestamp and any refresh error. To create a one-off report
manually, use `python -m aegis.anomaly_report --outdir cosmos_map\runs\<id>`.
New sweep runs retain all ESA count spot checks in `sweep_state.json`;
`/api/checks` exposes the saved telemetry while the dashboard reports its match
totals.
Joined Gaia/Bailer-Jones range queries use 8,000-row pages (with 4,000/2,000-row
fallback sizes) to reduce per-job workload after large ESA jobs were
aborted. Pagination remains ordered by exact source ID with the same selection;
smaller pages do not impose a per-tile catalogue cap. Async jobs retain their
query-hashed identity and are never silently resubmitted. A definitively
`ABORTED`/`ERROR` async job triggers the next smaller page size for the same
unfinished source-ID interval, without moving the pagination cursor. Its old
record remains untouched. Each page has at most three distinct query sizes;
exhaustion blocks that tile instead of repeatedly polling the dead job.
Ambiguous submissions and unknown phases also block rather than creating a
replacement job. Other tiles continue. `/api/status` exposes `blocked_tiles`
and degraded/blocked collection state, displayed on the dashboard. Blocked
tiles are excluded for the lifetime of that monitor process; restarting
rechecks their saved jobs without clearing evidence or automatically
resubmitting the same query. Exhausted jobs need explicit operator recovery.

The default monitor combines a sky-coverage map and a rotatable 3D Galactic-
coordinate view with a catalog-only evidence review. The sky map shows
completed-tile centers and active tile-query centers; its separate 20,000-row
reservoir sample plots individual stars. Click stars, tile centers, and tracked
extremes to inspect their available measurements and location. In 3D, drag to
orbit, use the X/Y/Z sliders for explicit axis rotation, use the wheel to zoom,
and Shift/middle/right-drag to pan; Reset restores the initial view. The 3D
sample uses the scanner's Sun-centered Galactic X/Y/Z positions and is not a
modeled or complete map of the Milky Way. Existing chart samples may not retain
Gaia source IDs, which the detail panel reports as unavailable. `/api/status`
reports the active scanner mode and
its `scan.stars` value: for `sweep`, this is the sum of
rows in completed, non-overlapping Gaia source-ID HEALPix tiles; for the legacy
random scanner, it is the count of unique IDs in its in-memory catalog, excluding
overlapping patch encounters. The report reads `cosmos_map\sweep_state.json` and
reports its per-tile counters separately from the legacy
`cosmos_map\star_scan_summary.json`. Those files describe different scanner
modes and snapshots; their totals are never combined. The legacy summary is
written every 10 patches and can lag its catalog CSV. Its `rechecked` count
means IDs sent for another distance query, not additional stars. The dashboard
surfaces current and persisted systematic-sweep flag counts plus active
tile-query progress; flag categories can overlap, and row-level candidates
remain unavailable when the candidate export is missing.

The report checks that tile files exist for completed state entries but does
not reread the entire tile archive (currently many gigabytes); sweep totals
are persisted per-tile row counters, not a row-by-row re-audit. The legacy
flag/candidate view reads `cosmos_map\cosmos_map_flags.csv`; only the first 40
flagged rows from the bounded prefix are displayed, in file order. Truncation
and inspected-row denominator are explicit. Missing input is unavailable, not
zero. The report also shows whether the legacy catalog CSV is newer than its
summary.

The report contains astronomical catalog evidence only. Local cosmology/theory
records, speculative interpretations and causal claims are intentionally
excluded. Flag labels are scanner heuristics, not scientific discoveries or
calibrated significance tests.

New scanner rows also retain Gaia parallax error, pmRA/pmDec errors and their
pairwise correlation, plus Bailer-Jones 16-84% distance bounds. These inputs are
shown with candidate rows and map details when present. Older rows remain
unchanged and show missing values; running scans do not acquire the new fields
until a scanner process using the updated code is started. The mapper does not
propagate these inputs into a calibrated velocity interval, significance or
anomaly probability, and it does not retain the full five-parameter Gaia
astrometric covariance.

Other local astronomy inputs are reported in a separate section, never merged
with Gaia star classifications. The local impact-structure analysis is included
when its source and result files are present. The exoplanet period-ratio analysis
is marked unavailable until its `research\exoplanet_locks\exo_rows.json` source
rows are present. The crater-age result is not plotted on the Gaia sky map because
it has no sky coordinates.

Each report records its schema/reporter versions, UTC generation time, source
paths, file modification times and SHA-256 for the sweep state and other small
source records. Large tile archives and flag CSVs are not hashed in full; only
a bounded candidate prefix is read from the flag CSV. The latest recorded tile
or patch timestamp is distinguished from filesystem timestamps and catalog
releases; generating a report never makes old observations fresh.
Gaia and Bailer-Jones distances share astrometry; agreement is a consistency
check, not two independent observations. No significance, control-sample test,
new anomaly classification, or causal interpretation is computed.
The per-star export now exposes this heuristic as `astrometric_quality_pass`.
The older `confirmed` column/property remains as a compatibility alias for
existing catalogues and clients; it does not mean an independently confirmed
star or discovery.
When all three Bailer-Jones distance quantiles are available, the scanner
requires positive lower bounds, nonzero interval width, and a median within
the interval. Invalid intervals raise an explicit source-ID-bearing error
instead of supplying chart distances, velocities or quality-pass labels.
Missing quantiles retain the existing inverse-parallax fallback; historical
rows and reports are not rewritten.

The default dashboard links to `/api/anomaly-report.md` and
`/api/anomaly-report.json` (latest saved report; 404 if absent). These endpoints
only read reports. Candidate rows can be searched and filtered locally in the
browser. Radial-velocity availability and partial-uncertainty usability filters
are non-destructive views of the first 40 displayed candidates, not full-catalog
selection or new classification. Partial usability checks finite nonnegative
parallax/PM errors, PM correlation in [-1,1], and positive ordered BJ bounds;
it does not validate full covariance or propagate errors. The filtered JSON
download preserves exact source IDs, report time/run, source fingerprints,
filter values and bounded-parent scope. Missing/invalid values are distinct
from valid zero. No statistically complete sample is produced.

Reporter 3.4 retains the prospective raw astrometry fields in candidate JSON
when present. Old reports/rows remain usable; unavailable fields stay missing.
The running reporter may keep its previously imported code until restart:
use the offline CLI for a new immutable 3.4 report without restarting collection.
The file-backed dashboard only needs a browser reload.

The research-channel table adds authoritative reference routes for Galactic
dynamics, binaries, asteroids/comets, meteors/fireballs, interstellar small
bodies, exoplanets, pulsars and black holes. It states required observations
and what cannot be inferred. These are **reference-only routes**: no new
catalogue ingestion, crossmatches, moving-object detection, transit/timing
analysis, orbit fitting or compact-object classification has been installed.
GaiaUnlimited selection/sky-dependent binary models are linked, not applied.
Actual moving-object detection requires time-tagged observations rather than
the Gaia star export. The dashboard links to the official Gaia Archive and visualisation
documentation, TOPCAT, and Astropy for independent inspection and analysis.
These external tools are links only; the dashboard does not contact them.
**Starting `monitor_server.py` still starts its existing network scanners**;
use the CLI alone for an offline report.

Focused offline checks: `python -m pytest tests\test_anomaly_report.py`.
Dashboard filter/export checks: `node --test tests\test_candidate_filters.cjs`.
The dashboard polls saved reports every 60 seconds in addition to its live
status polling. Report-fetch/render failures show the actual error and disable
candidate export; previously displayed snapshot metrics are explicitly not
current. Refreshes preserve valid flag selections without duplicating options.
Reports without research-channel metadata clear that view rather than retaining
labels from a newer report. Reload the browser to load these JavaScript changes.
Candidate report input rejects malformed Gaia source IDs. Markdown exports
preserve numeric zero and escape table separators. Matched-control distance
strata require positive, ordered bounds enclosing the reported median; invalid
intervals are excluded, not repaired or treated as usable uncertainties.
The AI monitoring audit now runs every six hours at minute 29, using Auto
efficiency and bounded read-only checks, replacing the earlier hourly audit.
It does not rerun scorecards/tests; the daily 22:00 comparison owns those gates.
Collection/report/browser timers do not invoke an AI model or consume AI credits.
Local automation requires the computer and Copilot app to remain available.
On 4 November 2026 at about 20:08 Central, the existing WSL monitor was
restarted on the same `gaia-full-20261104T025414Z` archive. Reporter 3.4 and the
expanded acquisition query were verified live. All 586 completed tiles and
27,152,418 selected rows were retained. Initial expanded requests timed out at
50,000 and 20,000 rows and entered the existing 8,000-row retry tier; successful
post-restart collection was not yet verified. Do not equate a healthy HTTP
endpoint with working ESA acquisition. Older tile schemas remain unchanged.
Small state/view files were copied and hash-checked through a separate restore
directory in session artifacts; this is not a full catalog or off-device backup.

### ESA timeout workaround (verified later the same evening)

The bounded native synchronous GET probe also timed out, but ESA's public
asynchronous TAP returned 1,000 rows with all expanded columns. The collector
now supports durable async range jobs in `aegis/tap_async.py`. A synchronous
timeout or HTTP 502/503/504 switches subsequent range queries to async;
`AEGIS_TAP_ASYNC=1` selects async immediately and is enabled on the running
WSL collector. This does not change the source tables, range selection, ordering,
distance join, fields or scientific gates.

Jobs and fingerprinted CSV pages are retained under the active run's `tap_jobs`.
Polls have bounded request/wait times. Transient retry preserves the same query/job;
ambiguous submissions without a returned job URL require manual investigation
and are never silently resubmitted. Failed, expired or malformed responses are
errors, not empty catalogues. Public ESA jobs have finite server retention.
Local page caches are evidence, not a storage-cleanup target.

### Local backups

`aegis/local_backup.py` backs up completed files in `ufe-v2/cosmos_map` and
`cmb-fit/results` to the approved `C:\Users\Danny\AEGIS-Backups` destination.
It uses SHA-256-addressed objects and unique snapshot manifests, retaining old
versions and unfavorable results without automatic pruning. Changing files
are retried with bounded attempts; corrupt backup objects and insufficient
capacity are explicit failures. Temporary/in-progress files and locks are
excluded. Each saved sweep state must have its completed tile files in the
manifest. File snapshots of active fit outputs are not a transactional fit
checkpoint. The repository, dependencies and other session artifacts are not
included in this data-backup scope.

The approved **AEGIS verified local backup** automation is enabled daily at
21:00 machine-local time using Auto efficiency. It invokes the existing Windows
Python runtime and performs a selected-file restore check after backing up.
The script itself makes no model calls; the app-triggered run uses AI credits.
The machine/app must remain available. No automatic restart or deletion occurs.

Manual invocation from the primary checkout in PowerShell:

```powershell
$env:PYTHONPATH = "$PWD\ufe-v2"
$env:PYTHONDONTWRITEBYTECODE = "1"
.\cmb-fit\venv312\Scripts\python.exe -m aegis.local_backup --repo "$PWD" --destination "C:\Users\Danny\AEGIS-Backups" --restore-check
```

Manifests are in `snapshots`, content in `objects`, and non-destructive restores
in unique `restore-checks` directories. `restore(destination, manifest)` restores
and verifies a full manifest into a new directory; CLI `--restore-check` verifies
a bounded selection of state, tile and result files instead of duplicating
the entire catalog a second time. Never manually replace live data from a
backup while collection is running. A same-C-drive copy cannot protect against
disk failure, theft or damage to the machine; off-device backup remains absent.

The two initially stalled tiles completed: 11833 had 18,876 rows and 7413 had
25,998 rows. Their saved gzip CSV counts match sweep state and include expanded
astrometry fields. The fully tested collector resumed 597 completed tiles and
27,368,495 rows at about 20:23 Central. Earlier schemas are not backfilled.
ESA spot-count checks still use fresh synchronous requests, not cached jobs;
their timeout can therefore remain a separate verification limitation.

The dashboard disables export when candidate-row evidence is missing. The
livestream clears stale telemetry on status failure and withholds damaged
historical result/status text without changing `science.json` or guessing symbols.
RUWE/tangential-speed labels describe follow-up heuristics rather than companion
or origin classifications.

Live-status fetch failures clear old counts and show the request error.
Missing live star counts are unavailable, not zero; candidate cells retain
numeric zero in derived values as well as raw catalog fields.

### Collection and review cadence

The scanner saves views every 60 seconds, completes immutable tiles as pages
finish, and schedules an ESA count check every 600 seconds plus request time.
The monitor generates immutable reports every 600 seconds plus generation time.
These intervals are not real-time alerts, row-by-row audits or statistical
analysis. The hourly local audit checks progress/freshness and comparison
evidence; the user-approved daily 22:00 local job permits one fixed matched fit
attempt, then monitors/scores it on later runs. The machine/app must stay on.
Full-catalog controls remain held until complete schema-ready inputs exist;
new survey ingestion or expensive analysis needs its own validated pipeline.

### Scientific-readiness changes (5 November 2026 UTC)

Future processes also query and retain unrounded Gaia parallax, reference epoch,
astrometric solution type, the colour/ecliptic-latitude inputs to the official
EDR3/DR3 zero-point recipe, positional errors, all ten correlations of the five
astrometric parameters, and radial-velocity error. Completed tiles written by
this version record their column list and acquisition query in their state entry.
These are retained measurements, not applied corrections or propagated errors.
The extra pseudocolour dimension of six-parameter solutions is not fully retained.
The current process does not hot-reload Python code; these acquisition changes
are **installed for a future launch, not active in the running scanner**.

Historical tiles are not rewritten or backfilled. The existing DR3 resweep
contains both legacy and uncertainty-enabled schemas. For a homogeneous new
baseline, use a separately named archive after validating the expanded query
against the live service; do not treat a same-ID resume as a schema upgrade of
completed tiles. Resume now refuses corrupt/incompatible state or missing
completed-tile evidence instead of silently starting over.

Matched controls remain **on hold** by decision. `aegis.matched_control` rejects
incomplete sweeps by default, preflights every completed tile header before
reading/hashing full archives, rejects absent schema inputs and malformed/count-
mismatched rows, and verifies tile fingerprints after capture. Synthetic tests
do not qualify real data. Even schema-complete descriptive output would not
establish calibrated significance, selection correction, or a predictive AEGIS
test; its solution-type field is retained but not used in the matching strata.

`science.json` and the livestream now identify their cosmology/results cards as
historical, not current fit status. The old exoplanet pass is explicitly
unreproducible locally until its source rows and results are restored.
The complete project handoff is
[`papers/AEGIS_RESEARCH_SYNTHESIS.md`](../papers/AEGIS_RESEARCH_SYNTHESIS.md).
## Anomaly scanner (gravity, quantum, space telemetry)

`monitor_server.py` also runs `aegis/anomaly_scanner.py` (disable with `AEGIS_ANOMALIES=0`). It watches GWOSC gravitational-wave events,
the NIST quantum beacon, NOAA SWPC, NASA DONKI/GCN/Exoplanet Archive and JPL feeds, flags candidates the same way the star scanner does
(flag + how to confirm), and compares every category's new data with its earlier data (KS and Wasserstein distance, with an old-vs-old control).
Swept Gaia tiles are compared with earlier tiles, and `cosmos_map/incoming/NAME.csv` files are compared with that name's history.

- `/api/anomalies.json?wavelength=&object=&flag=&source=` filtered results with counts; `.ecsv` and `.vot` give Astropy, TOPCAT and Aladin files
- `/api/compare` old-vs-new distances; `/api/licenses` licence and credit for each source
- Flags are candidates, not discoveries. Tests: `python -m pytest tests/test_anomaly.py`
