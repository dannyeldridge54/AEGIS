# Where the string-fit engines are (for the local agents) — 25 Nov 2026

Danny asked the cloud coordinator to tell you where the engines are that were built for the string fits. All paths are in the
AEGIS repo, branch `unify-bg` (this list was written at commit 1fa03d92). Read the code at a pinned commit and cite it; these
are tools with their own validation notes, not established physics. Each tool's docstring names the D-notes that validated it.

## 0. START HERE: the multi-knob resonating / pulsing engines (the ones you were looking for)
Your sessions reported that the "pulsing displays" you inspected could not be verified as the Claude engines and that you
needed an original filename. These are the original files. They are all in `tools/loom/` unless a path is given.
| File | What it is |
|---|---|
| `pulse.py` | The pulsing Loom: mark every tension point, triangulate them all at once, test, re-read the compass, repeat. Coupled knobs ln m3/2 (K_T) and ln T_R |
| `resonance.py` | Layered resonance: the equation built from the centre outward through 9 layers (torus, pyramid, turnover, cube, fold, dilaton, forces, cosmology, late universe) (D1972) |
| `resonance10.py`, `resonance_d2156.py` | The same with a 10th rung: outer data shell, negative-space shell, spine (D2136, D2156) |
| `loom_rt.py` ... `loom_rt5.py` | Real-time layered pulsing engines v1-v5 (D1983, D1986, D1987, D1989, D1993). v5 is the current one; `test_rt_equivalence.py` shows it reproduces v4 bit for bit |
| `weave_core.py` | One engine = margins + Jacobian fingerprint + compass + lenses + per-node optimisation (D2168) |
| `loomcore.py` (also `tools/cubemind_ufe/loomcore.py`) | Loom core: a fractal of knob agents with a balancing centre; each agent owns <= 9 knobs and tunes them octave-then-fifth |
| `loomd.py`, `planner.py`, `centre_brief.py` | The Loom as a daemon; the planner; the brief for the centre referee |
| `lens_core.py`, `lensing.py` | Layer lensing: lenses = right-singular directions of each layer's margin Jacobian in knob space (D1981, D1982) |
| `still_point.py`, `method_tests.py`, `method_tests_3axis.py` | The still point of the three tandem axes S, T, U; the tests OF the method (injection-recovery etc.) |
| `compass.py`, `field_map.py`, `review.py`, `triangulate.py` | Direction and pull of each measurement; historical knob moves; pattern review; bracketing |
| `check.py`, `online_fdr.py`, `pass_label_check.py`, `test_loom_battery.py` | The Loom's own checks, false-alarm control and battery. Run these before trusting any verdict |
| `negspace_ladder.py`, `negspace_outward.py`, `node_equations.py`, `open_node_equations.py`, `wall_pull.py` | The negative-space ladder and its node equations (D2137-D2145). The first two are labelled MAP, not derivation |
| `tools/weave_knobs.py` | Central-equation engine: three knob equations K_S (g_s), K_T (sigma_vis, Vol, A), K_U (\|u\|) feeding one central map (UFE v4 section 8) |
| `tools/weave_control/engine.py`, `server.py` | Weave Control: ONE parameter set drives every toolkit, level by level; local control panel on port 8790 |

**String-geometry / SUSY engines: `tools/seed/`** (105 files; read `SEED.md` and `SEED_SHORTCUTS.md` first)
| File | What it is |
|---|---|
| `z6p.py` | IIA T6/Z6' fractional D6-brane builder (= the Weave's Z6-II twist (1,2,-3)/6), from Gmeiner-Honecker 0708.2285 (D2146) |
| `seed_v3.py` | Seed engine v3: exact consistency landscape on T6/(Z2xZ2), exact integer-chi SUSY conditions, 3-family visible pair (D2082) |
| `tsusy.py`, `joint4.py`, `kl_gaugino.py`, `z2z6p_k7_robust.py` | SUSY threshold -> two-loop alpha_s; four-goalpost joint test (alpha_s, wino, gluino, m_h); gaugino mass scan; robustness (D2085-D2123) |
Note the two orbifolds both appear here: `z6p.py` is Z6', `seed_v3.py` is Z2xZ2. That is the same split as the open
compactification gap; having a builder for each does not join them.

Status words in those docstrings are the authors' own (MAP, PREREG, D-number). Quote them as written.

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
