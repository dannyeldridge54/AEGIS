# AEGIS inventory (Job 1 of the AEGIS Tools Work Order)

Written 15 Nov 2026 from a full pass over branch `unify-bg` and the two companion public repositories
(CosmoExplorer, torsion-lambda-toolkit). "Runs today" means I ran it in a clean cloud container this session,
unless marked *not run*. Pre-SERAPIS material was moved to `archive/` the same day (see archive/README.md).

## AEGIS repository, folder by folder

| Folder | What it is | Runs today? | Depends on | Known problems |
|---|---|---|---|---|
| `papers/v3/` | SERAPIS paper (13 pp, LaTeX, 6 figures), prediction sheet, submission package, Zenodo files, outreach drafts | Yes: builds with pdflatex + bibtex, 0 overfull boxes | TeX Live | v3.1 not yet on Zenodo (needs "Publish"); emails unsent (need "Send") |
| `theory/modular/` | 85 SERAPIS scripts (D637–D713): exact Mukhanov–Sasaki solver, Janus relations, Epstein/BHK plateaus, multi-scale tests | Yes (spot-checked D692, D700, D702, D710, D711, D713) | numpy, scipy, mpmath, CAMB 2.0.5 | Scripts are one-off; shared code is copied (e.g. the D632 MS block) rather than imported |
| `theory/` (other subfolders) | Twist-era derivations (twist2, twistg/l/p, inflation, kahler_cliff, string_home, …) | *Not run* | numpy, scipy, sympy | Locked by SHA-256 paths, so kept in place; superseded science |
| `theory/pending_docs/D72_D75_weak_spots.md` | The research log: every D-note D72–D713 | — | — | ~6,800 lines; two parallel sessions collided on numbers today (D707, D712) → Job 2 |
| `field_tests/rules/` | 590 files: PREREG locks, .sha256 hashes, DEVIATIONS | Yes: 294 hashes checked, 289 match | — | 5 mismatches: 4 locked scripts edited after locking (D325, D367, D383, D437) and D633 (addendum appended, with its own addendum hash) |
| `field_tests/results/` | 382 result files | — | — | AION audit: 184 OK, 0 late, 66 D-numbered without a lock (early exploratory), 133 without a D-number |
| `field_tests/` (rest) | Twist test harness: scorers, ledger builder, DES Y3 shear wrapper (S8_WL), DESI mocks, gates, schedules | Ledger builder runs; reports 3 missing Twist rule files | CosmoSIS, CAMB, AxiCLASS (PC) | Paths specific to Danny's PC; Twist-era |
| `cmb-fit/` | CAMB/AxiCLASS fit pipeline, two-field CAMB module (ub2_camb), coupled/ULA AxiCLASS builds | *Not run* (needs the PC environment) | AxiCLASS, candl, CAMB | Run logs moved to archive; still referenced by field_tests/run_pc.sh, so kept in place |
| `ufe-v2/` | Star Mapper: resumable Gaia DR3 sweeps, anomaly scanner, HEALPix-lite, validation collector | Unit tests: 117 pass, 2 fail | Python, Gaia TAP (network) | Failing: a rule-copy hash test that predates the D633 addendum, and a scanner-readiness text check; runs daily on Danny's PC |
| `apps/cosmos_atlas/` | Static sky viewer (index.html, sky_pointer.html) plus SIMBAD/VizieR fetchers and "hunts" | *Not run* (static HTML; fetchers need network) | Browser; astroquery-style HTTP | Nine near-duplicate fetch scripts (fetch_more, fetch_more2, …) |
| `method/` | AEGIS Method kit (rule/deviation templates, lock_rule.py) | Yes | stdlib | `verify` mis-resolved paths (reported 202 bad of 294); **fixed today**, now 289/294 |
| `tools/aion/` | AION 0.1.0 pre-registration kit (new/lock/deviate/check) | Yes: 3 tests pass; audit in docs/AION_AUDIT.md | stdlib, git | Licence pending |
| `ops/` | PC job runners (pcjobs), ladder/deep state files | *Not run* | PC | Writes to `results/` (kept as an empty folder) |
| Root | README (rewritten for SERAPIS), TOOLS.md, AEGIS_METHOD.md, CITATION.cff, LICENSE (HL3-MIL-SV), check_my_work scripts, run_derivations.py | — | — | CITATION.cff still cites the Twist EDE paper (v2), not SERAPIS |

## Companion repositories

| Repo | What it is | Runs today? | Notes |
|---|---|---|---|
| CosmoExplorer (public, v2.0.0, TypeScript) | Background-cosmology model explorer: 11 models, 73 data points from 6 surveys, adaptive scan, daemon | Yes: 20/20 Jest tests pass | `node_modules` (90 MB) is committed to the repo; README's comparison table oversells it against Cobaya/CosmoMC |
| torsion-lambda-toolkit (public, v0.2.0, TypeScript + Python bridges, LGPL-3.0) | TorsionΛ: Einstein–Cartan torsion screening toolkit with background, CMB shift/acoustic scale, σ₈/S₈, Fisher, likelihoods, CAMB/Cobaya bridges | *Not run* this session (49 test files) | 33 top-level status/report .md files; earlier audit: CMB shift parameter outside Planck at β = 0.192 → Job 7. σ₈/S₈ is now implemented (`src/physics/matter-power-spectrum.ts`), so that item from October is closed |
| aegis-Kronos-syndyr (private) | PC-side mirror | Not inspected | Don't touch its git (standing rule) |

## Strongest pieces (ranked)
1. **The pre-registration record itself**: 294 hashed locks, 289 still exact, every SERAPIS result (D637 onward) locked before it ran. AION can now audit it in one command. This is rare in any field.
2. **The SERAPIS computation stack** (`theory/modular/`): an exact Mukhanov–Sasaki solver validated against slow roll to ≤ 0.001 in n_s, and modular-form series checked against lattice sums to 7–8 digits.
3. **The multi-scale test scripts** (D710, D711, D713): CMB-by-release scoring, CAMB Lyman-α and S8, neutrinos, DM, colliders. They are nearly a public tool (Job 3).
4. **The Janus closed forms** (D640, D669, D671): small, analytic, checkable by anyone (Job 4).
5. **CosmoExplorer**: clean, tested, installs.

## Weakest pieces (ranked)
1. **The research log**: one 6,800-line file with no index, and number collisions between parallel sessions (Job 2).
2. **Script duplication**: SERAPIS scripts copy shared code instead of importing it, so a fix in one doesn't reach the others.
3. **TorsionΛ status**: physics problems from October (shift parameter) are not reflected in its README; 33 report files make it hard to see what is current (Job 7).
4. **PC-only paths**: cmb-fit, field_tests runners and ops assume Danny's PC, so nobody else can rerun them.
5. **Two stale tests** in ufe-v2, and a CITATION.cff that points to the superseded Twist paper.
