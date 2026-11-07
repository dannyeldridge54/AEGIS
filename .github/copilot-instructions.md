# Repository context

AEGIS contains distinct projects: the TypeScript `aegis-agent` optimizer, Python
cosmology/theory research, and a local Gaia Star Mapper. Keep their results and
validation separate: optimizer tests and catalogue checks do not validate a
cosmological model.

Read `README.md` and `AEGIS_METHOD.md` first. For scientific work, also consult
`MODEL_v2.md`, `papers\AEGIS_RESEARCH_SYNTHESIS.md`, `theory\README.md`, and
`theory\DERIVATION_CHAIN.md`. Local checkouts may contain `AGENT_HANDOFF.md`,
`HANDOFF_LOG.md`, and `NOTE_FOR_COPILOT.md`; use them for continuity, but check
dated statements against current source and stored evidence. Historical fit
tables and old engineering briefs are not current benchmark results or an
instruction to implement their unfinished plans.

## Build and validation commands

Run TypeScript commands from the repository root:

```powershell
npm ci
npm run build
npm test -- --runInBand
npm test -- --runInBand --runTestsByPath tests\aegis.test.ts
npm test -- --runInBand --runTestsByPath tests\aegis.test.ts -t "agent respects maxEvals"
npm start
npm run demo
```

`npm run build` compiles strict ES2020/CommonJS TypeScript from `src` to `dist`,
including declarations and source maps. Jest uses `ts-jest`, Node, and
`tests\**\*.test.ts`; tests and examples are excluded from the TypeScript build.

Use a Python environment with NumPy, SciPy, and pytest for the reference engine
and its offline tests. Python 3.12 is the documented Windows scientific
environment; do not bypass Windows application-control policies to load
blocked extensions.

From the repository root:

```powershell
python -m pytest ufe-v2\tests theory -q
python -m pytest ufe-v2\tests\test_v2.py::test_flatness_exact -q
python -m pytest theory\test_effective_baseline.py -q
node --test ufe-v2\tests\test_candidate_filters.cjs
```

From `ufe-v2`:

```powershell
python -m aegis.method check
python -m aegis.guardrails
python -m aegis.anomaly_report --max-rows 1000
```

The method and guardrail CLIs print JSON: inspect `ok`, `failed`, and `waiting`,
not just the process exit code. The anomaly-report CLI writes a new immutable
report without starting scanners, contacting the network, or running fits.

For bounded numerical and comparison-contract reviews, from the root:

```powershell
.\cmb-fit\venv312\Scripts\python.exe .\theory\review_numerical.py
.\cmb-fit\venv312\Scripts\python.exe .\theory\review_derivation_comparisons.py
```

These use their own interpreter and existing regressions: exit 0 is complete
passing evidence, 1 is failure, and 2 is blocked/incomplete evidence.
`python .\theory\spiral_w.py validate` checks the separate Spiral solver; its
`scan` command is not a validation substitute.

Full AxiCLASS fitting requires Linux/WSL, compiled builds, Cobaya, and likelihood
data. In a Linux/WSL shell, `bash cmb-fit/environment/setup_twist_env.sh` rebuilds
the pinned environment and downloads likelihood packages. After selecting that
environment, `$TWIST_PY cmb-fit/axiclass/early_late_spa.py smoke ax_spa_lcdm_halofit`
evaluates one reference point; inspect its printed `finite` result. A named fit
uses `$TWIST_PY cmb-fit/axiclass/early_late_spa.py <run-name>`.
Do not launch a long fit or restart a stopped benchmark merely to validate an edit.

## Architecture

- **Optimizer:** `src\index.ts` is the public export surface; `interfaces.ts`
  defines tasks, parameter spaces, configuration, state, and discriminated
  events. `AegisAgent` in `agent.ts` runs evaluation, best-result tracking,
  discoveries, phase changes, and persistence. `strategies.ts` generates bounded
  parameter proposals and uses a UCB1 meta-learner to reward strategies.
  Daemon and swarm layers orchestrate these agents; the daemon integrates memory,
  checkpoints, scheduling, and the HTTP dashboard. Parallel and multi-objective
  optimization are separate entry points, not modes of the core run loop.
- **Reference cosmology:** `ufe-v2\aegis\cosmo_v2.py` supplies backgrounds,
  distances, and sound horizons. `data_v2.py` supplies survey inputs and
  `likelihood_v2.py` combines their likelihood terms; `run_v2.py` fits models and
  writes reference results. This acoustic-angle/background engine is distinct
  from the full CMB AxiCLASS/Cobaya pipeline in `cmb-fit\axiclass`.
- **Full fits and theory:** `early_late_spa.py` maps run names to model/data
  choices, selects solver builds, runs Cobaya, and saves `cmp_<name>.json`.
  `theory` contains separate derivations, effective backgrounds, and fixed-metric
  and coupled perturbation stages. Their readiness gates must not be conflated.
- **Star Mapper:** `ufe-v2\monitor_server.py` serves file-backed HTML and APIs,
  runs either `aegis.sweep.SkySweep` or the legacy random `StarScanner`, and
  periodically writes reports through `aegis.anomaly_report`.
  `aegis.method` maintains the claim wall and ledger; `aegis.guardrails`
  recomputes scientific/provenance checks for the monitor.
- **Local AI tooling:** `agent` is a separate, Git-ignored Python/Ollama workspace,
  with helm/check-in controls, approval-gated actions, a builder, and council.
  It is not the TypeScript optimizer or the cosmology likelihood engine.

## Code and scientific conventions

- Keep exported optimizer APIs consistent with `src\index.ts` and shared
  contracts in `interfaces.ts`. Tasks accept named numeric parameters and may
  evaluate synchronously or asynchronously. Minimization is the default;
  best-result comparisons and strategy rewards must also respect maximize goals.
  Agent events use the existing event union; localized message templates live in
  `language.ts`, with runtime language switching.
- Scientific numbers come from stored results/checkpoints, not hand-entered
  replacements in pages or `science.json`. Distinguish likelihood-only chi-square
  from effective objectives including priors. Compare models with matched data,
  solver builds, nuisance treatment, and restart policies; charge extra settings
  through AIC and apply the predeclared multiple-testing rules.
- Preserve SHA-256-locked preregistrations, predictions, historical failures,
  withdrawals, and old reports. Ideas discovered in the tested data are not blind.
  The claim wall separates evidence, hypothesis, and meaning; no regression pass
  promotes a hypothesis to physical evidence.
- In the Twist reference engine, the field coordinate is displacement
  `d = phi_abs - phi_0`, with the cosine minimum at `d = 0`.
  Distinguish physical densities `omega` from fractional densities `Omega`,
  `h` from `H0`, and drag horizon `r_d` from recombination horizon `r_s`.
  Maintain exact present-day flatness and model-computed sound horizons.
  DESI DR2 uses correlated BAO terms; the reference SN likelihood analytically
  marginalizes absolute magnitude. The local SH0ES prior is explicitly optional.
- The n=3 Twist potential remains an assumed effective ansatz, not a derived
  microscopic torsion prediction. QCD n=1 dynamics, early EDE, effective Late
  Twist, and two-field Spiral Twist are distinct branches. Numerical agreement
  alone must not set full-stability or scientific-readiness flags to true.

## Data, runtime, and publication boundaries

- Starting `monitor_server.py` starts network scanners. Preserve the existing
  scanner lock and archive; use `AEGIS_RUN_ID` for an intentionally isolated
  resweep under `ufe-v2\cosmos_map\runs\<id>`. Reusing the same ID resumes that
  run. `AEGIS_OUT_DIR`, `AEGIS_MODE`, and `AEGIS_MONITOR_PORT` control the existing
  monitor configuration; use the offline report CLI for report-only work.
- Never combine systematic-sweep counters, legacy random-patch encounters, or
  separate run archives into one denominator. Catalogue flags are heuristics,
  not detections; Gaia and Bailer-Jones distances share astrometry. Preserve
  source IDs exactly as strings in browser/JSON work. Missing inputs are
  unavailable, not zero; preserve valid zero and disclose bounded/truncated reads.
  Keep `astrometric_quality_pass` and its legacy `confirmed` alias compatible
  without implying independent confirmation.
- Fit scripts resolve paths relative to their source. Use `TWIST_RESULTS`,
  `TWIST_BUILDS`, `TWIST_PY`, and `COBAYA_PACKAGES_PATH` for relocated environments
  rather than embedding machine-specific paths.
- Follow `.gitignore`: local catalogue dumps, environments, likelihood downloads,
  backups, `node_modules`, `dist`, and internal agent notes stay out of commits.
  Retain existing authorship/license headers and provenance hashes.
- Public posting, publishing, messages, accounts, credentials, spending, and
  deletion require explicit owner approval. Public explanations use plain
  English, keep personal/private information out, and report losses as clearly
  as wins. Consult `LICENSE` rather than historical README pricing statements.
