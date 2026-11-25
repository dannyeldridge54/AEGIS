# Where the string-fit engines are (for the local agents) — 25 Nov 2026

Danny asked the cloud coordinator to tell you where the engines are that were built for the string fits. All paths are in the
AEGIS repo, branch `unify-bg` (this list was written at commit 1fa03d92). Read the code at a pinned commit and cite it; these
are tools with their own validation notes, not established physics. Each tool's docstring names the D-notes that validated it.

## 1. The reference: `tools/serapis_calc/` (SERAPIS calculator)
The base toolkit and the one everything else is checked against. Run `python -m tools.serapis_calc.selftest` from the repo root
before using it; it exits 0 only if every cross-check passes.
| File | What it does |
|---|---|
| `eisenstein.py` | Non-holomorphic Eisenstein series E(tau,s), two independent evaluations (Fourier series and direct lattice sum) |
| `shapes.py` | Shape functions of a torus modulus U, E(U,s) in the GRV eq. 1.5 normalisation (full lattice), to ~1e-12 |
| `modular.py`, `jseries.py` | Klein j from E4, E6; exact integer q-expansion of j |
| `strings.py` | Level S: string one-loop on tori, built in stages (Jacobi theta functions first), each checked by an independent route |
| `potentials.py`, `p3s.py` | SERAPIS plateau potentials; the species-plateau inflation equation (SERAPIS_FINAL_EQUATION.md v3) |
| `landscape.py` | The potential on the whole upper half-plane: vacuum finder and masses (canonical Hessian) |
| `ms.py`, `ms_jit.py`, `multifield.py` | Exact single-field Mukhanov-Sasaki spectra (plain and compiled); multi-field background |
| `nstar.py` | N* from the matching equation (Planck 2018 X eq. 47 form) |
| `meter.py` | Inverse string meter: a measured n_s -> C and Im S x Im rho for SERAPIS-E |
| `emulator.py` | Fast SERAPIS-E emulator (quadratic surrogate fit to 5 exact points; an interpolation tool, labelled as such) |
| `relation.py` | Consistency relation: alpha_s and beta_s from (n_s, r) |
| `pipeline.py` | All levels linked: model -> potential -> vacuum -> spectra -> N* -> observables -> distance to data |
| `data.py` | The data values used in the D-notes |
Also read `README.md`, `STRINGS_PLAN.md`, `P3S_NOTES.md` in that folder.

## 2. The fast solver: `tools/janus_calc/` (Janus String Calculator)
A fast, model-aware solver for SERAPIS observables. It never imports the reference solver, so the two are independent.
| File | What it does |
|---|---|
| `core.py`, `core_jit.py` | One background integration, Hubble-flow parameters, spectra (plain and compiled) |
| `mfms.py`, `mf_jit.py` | Exact multi-field Mukhanov-Sasaki (MultiModeCode equations, arXiv 1410.0685) |
| `mfms_nc.py`, `mfms_nc_jit.py` | The same on a curved field space (Kaiser et al., arXiv 1511.09148) |
| `twofield.py` | Multi-field delta-N (validated in D999, D1000) |
| `anyV.py` | Any potential given as a formula string or a callable |
| `models.py` | The SERAPIS branch potentials, built from serapis_calc's modular functions |
| `observe.py` | One call: reheating temperature -> N* (self-consistent) -> observables with error bars |
| `settings.py` | Model library and the CMB constraints it scores against |
Public copy: https://github.com/dannyeldridge54/janus-string-calculator (may lag this branch).

## 3. String thresholds: `tools/strings/`
`gh_thresholds.py`, `gh_thresholds_v2.py` — Gmeiner-Honecker (arXiv 0910.0843) N=2 lattice sums and the Z6' Standard Model
SU(3), SU(2) thresholds. v2 has coefficients read from the source PDF; calibrated in D2232/D2233. Use v2.

## 4. Compactification and lattice tools
| Path | What it does | Caveat |
|---|---|---|
| `tools/kaluza/` | Kaluza-Klein masses and stability for 1D warped (Dudas-Mourad-type) compactifications | Its own docstring says the scalar-operator solver is NOT yet validated against the published numbers |
| `tools/lattice/lattice_lab.py` | The lattice web tool (results validated in D1276-D1291) | |

## 5. Fitters and the Loom
| Path | What it does |
|---|---|
| `tools/fastcmb/loom_fast.py` | Fast CMB fitter: same theory, likelihoods and verdict rule as the reference fit, search organised for speed (D2173 Addendum 1) |
| `tools/loom/` | The Loom: `compass.py` (direction and pull of each measurement), `field_map.py` (historical knob moves and what they pulled), planner spec and locks |
| `tools/weave_cm_v5c/`, `tools/weave_cm_v5/`, `tools/weave_cm/` | The Weave CubeMind lenses and patches |
| `tools/cubemind_ufe/` | CubeMind's UFE lens (`ufe_lens.py`), Loom core (`loomcore.py`), mission and knob protocol |
| `tools/calcq/` | The calculation queue that ran sweeps on the PC |

## 6. The newest engine: `tools/field_engine/`
`engine.py` (planner, lenser, lock, derivers, fitter, tester, referee, corrector, librarian; v2 adds independent samples,
confidence selection and serial batches), `testwire.py`, `FIELD_MACHINE_PLAN.md`. Tested with mock models only.

## 7. Indexes
`tools/TOOL_REGISTRY.md` (every tool), `tools/TOOLKIT_STATS.md`, `tools/TOOLKIT_MAP_CERN1_HYPERION.md`.
The scripts behind individual string results are under `theory/modular/`, `theory/flux/`, `theory/deep/`, each named by its D-note.

## Two things to keep straight when you use them
1. `eisenstein.py` and `shapes.py` use different normalisations of E (coprime-pair sum with a factor 1/2, and full lattice).
   Your handoff already noted that SERAPIS-E uses the full-lattice E(tau,2); check which one a formula assumes before comparing numbers.
2. A tool reproducing a number is a check of the tool, not a derivation of the common action. The Weave (Z6-II) and SERAPIS-E
   (T6/(Z2xZ2)) are still separate constructions; these engines do not close that gap.

— cloud coordinator (Claude)
