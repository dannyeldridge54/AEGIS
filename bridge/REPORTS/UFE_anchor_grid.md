# UFE anchor grid

**Cycle 2: one symmetry anchor; one data anchor; zero bound anchors.**
Recommend first selecting the separate SERAPIS-E and YFORK2 local scalar
cells at rho: their existing conditional mass formulas give a clear baseline
for a later, separately planned check. They are **not** a joint theory or a
full-stability verdict. No switch has been run for this grid; all unselected
cells remain **not yet computed**. Danny selects cells before a test plan is
locked and run.

## What is anchored

The modular fundamental-domain pictures provide a repeatable coordinate map,
not evidence of a physical fractal or a unified field. In the upper half-plane,
rho = exp(i pi/3) and i are fixed by respective nontrivial elliptic modular
transformations; the cusp i-infinity is a boundary class, not an ordinary
finite point. A differentiable scalar potential invariant under the relevant
modular transformation has a stationary point at the corresponding elliptic
fixed point. Stationarity alone does not establish a minimum.

Images of one fixed point under the modular group represent the same
symmetry orbit, not independent observations. A local stability statement
transfers between images only when the **full model**, field-space metric,
background and relevant boundary conditions transform consistently under
that symmetry. Model-specific symmetry breaking, truncated sectors, matter,
and bounds can invalidate the transfer. No common compactification or field
identification between SERAPIS-E and YFORK2 is assumed.

In the Loom, a "node" is an optimizer or bookkeeping unit, with nested knob
agents and separate tune/held inputs; a negative-space node records a proposed
bound or headroom. That computational nesting is a map, not a derivation of
physical fractal structure or evidence that a bound is satisfied.

## Anchor ledger (append-only)

| ID | Point | Kind | Sector / node | Value and error | Source | Status |
|---|---|---|---|---|---|---|
| A01 | rho = 1/2 + i sqrt(3)/2 | symmetry | SERAPIS-E, modulus / torus node | Exact coordinate; no observational error. For full-lattice E2, z=E2(U)-E2(rho), V=V0 z(1+C z)/(1+z), V0 > 0, finite C, MPl=1 and canonical metric G=I/(2 y²), each of the two scalar masses squared is 2 V0 E2(rho) > 0. Historical D2259 reports E2(rho) = 5.783359299678672 and N8 finite-difference discrepancies 6.79e-6 and 5.46e-6 relative to its analytic target; these are numerical check differences, not statistical uncertainties. | [Audit](https://github.com/dannyeldridge54/AEGIS/blob/e155cdbd05fa47241abeb6f29774d5d47454bd06/bridge/REPORTS/UFE_final_copilot_2026-11-25.md), [D2259 result](https://github.com/dannyeldridge54/AEGIS/blob/e155cdbd05fa47241abeb6f29774d5d47454bd06/field_tests/results/d2259_ufe_stages.json) | **stable locally**, only for that scalar truncation and assumptions; full coupled stability and observational bounds **not yet computed**. Historical check, not a new test. |
| A02 | scalar spectral index at pivot k*=0.05 Mpc⁻¹ | data | Inflation / primordial-spectrum node, sectors separate | n_s = 0.9728 ± 0.0029, 68% marginalized interval, dimensionless; SPA + BICEP/Keck + DESI DR2. The same analysis gives r < 0.035 at 95%, an upper limit, not a second independent anchor. | [Balkenhol et al., §2–3, eq. (2)](https://arxiv.org/html/2512.10613v2) | **not yet computed** for either sector. This is not a field location or a stability test. |

## Adjustable switch grid

Each cell states the planned question and its current status, not an
authorization to calculate. `L` and `D` below identify candidate engines,
not verified runtime environments; a selected cell needs its own fixed
model, inputs, thresholds and C7 plan.

| Anchor | Sector E2 / E3/2 | Point rho / i | Bridge none / loop / J-link / flux | Dust b and sign | v3 / v4 normalization | Gauge reading | Bounds on / off |
|---|---|---|---|---|---|---|---|
| A01 rho | E2: **stable locally** as in ledger; E3/2 switch and both full models **not yet computed** in this grid. Check separate canonical Hessians with `L` / `D`. | rho as ledger; i **not yet computed in this grid**. Compare stationary-point Hessian signatures separately with `L`. | **not yet computed** for full linked theories. Specify each bridge action and its domain before Hessian/constraints with `D` or a separately reviewed solver. | **not yet computed** for a physical common model. For the conditional reverse-thread frozen dust balance, the audit derives curvature b(b+beta) rho_c, beta=2 sqrt(2); distinguish sign intervals and existence before a local Hessian with `D`. | **not yet computed** as a full model. Audit reports literal untilted v4 is 9/4 the v3 coefficient under stated conventions; check explicit actions and remaining terms with `D`, not a sector identity. | **not yet computed** for a complete transformed action. Source-owner notation correction is recorded separately; require K, W, f and theta dictionary before a gauge comparison. No suitable complete engine established. | **not yet computed**. Specify each bound and its dataset/likelihood separately; a switch does not remove a physical constraint. `tools/loom/negspace_ladder.py` is a historical MAP only, not a likelihood or stability proof. |
| A02 n_s | **not yet computed**: E2 candidate `tools/janus_calc/models.py` + `observe.py`; E3/2 requires a validated two-field adapter, with `tools/janus_calc/mfms_nc.py` only a candidate. | **not yet computed**: horizon exit is a trajectory point, not rho/i; neither candidate engine provides the missing mapping by itself. | **not yet computed**: no sourced bridge or suitable joint-action engine established. | **not yet computed**: dust-to-primordial transfer not established; no validated adapter named. | **not yet computed**: specify sector action and use a validated spectrum engine; the 1D `p3s.py` slice is not full YFORK2. | **not yet computed**: no validated complete gauge dictionary or comparison engine. | **not yet computed**: use the paper's stated posterior only under matching assumptions. Bound-off is sensitivity only, never observational acceptance; no joint likelihood has been pinned. |

`L` = `tools/serapis_calc/landscape.py` and `D` =
`tools/field_engine/ufe_stages.py`, as read at AEGIS commit
`e155cdbd05fa47241abeb6f29774d5d47454bd06`. `L` imports NumPy/SciPy and
uses `E_paper` normalization, which must be reconciled with the audit's
full-lattice normalization before comparing masses. `D`'s script entry point
writes `field_tests/results/d2259_ufe_stages.json`; it must not be rerun
against that historical path. Import/runtime dependency closure and safe
isolated output paths are not established. Neither engine was imported or
executed for this grid.

The historical CMB-SPA inputs in `tools/serapis_calc/data.py` are marginal
n_s summaries; the two datasets overlap, and that file supplies no joint
covariance or running likelihood. A tilted reference in
`tools/janus_calc/settings.py` was chosen to target n_s. Do not score it as a
blind prediction, sum overlapping pulls, or equate the one-dimensional
`p3s.py` slice with a full YFORK2 perturbation model.

## Source and execution boundary

The scope and requested sequence are [C8](https://github.com/dannyeldridge54/AEGIS/blob/8830b27251545838141001bbaf5d80685dadb1bd/bridge/REPORTS/C8_cloud_research_loop_anchor_points_2026-11-25.md)
and [C7](https://github.com/dannyeldridge54/AEGIS/blob/09a9c6147863f5aca96f72302a9f3bc090506c40/bridge/REPORTS/C7_cloud_GO_derive_and_test_2026-11-25.md).
The older results are explicitly historical; no model flip, fit, scan,
process self-check, native solver or new scientific test was executed for
cycle 1. Before an authorized selected-cell run, publish and verify its
specific model/source/data/null/threshold plan and SHA-256 sidecar; preserve
failure and record any deviation before a rerun.

### Cycle 1 normalization clarification

Source review establishes that `eisenstein.E_paper` equals
`2 zeta(2s) * E_fourier`, the full-lattice normalization. Thus `L` at
`lam=1`, multiplied by explicit `V0`, matches the A01 potential above;
do not silently substitute primitive `E_fourier` or another `lam`. This
resolves the normalization cross-check mentioned above, not the untested
runtime or full-physics gates. Source:
[`eisenstein.py`](https://github.com/dannyeldridge54/AEGIS/blob/8830b27251545838141001bbaf5d80685dadb1bd/tools/serapis_calc/eisenstein.py),
[`landscape.py`](https://github.com/dannyeldridge54/AEGIS/blob/8830b27251545838141001bbaf5d80685dadb1bd/tools/serapis_calc/landscape.py).

### Cycle 2: data-anchor qualifications

Balkenhol et al. use a Lambda-CDM plus varying-r analysis with a
single-field slow-roll tensor consistency relation and optical-depth prior
tau = 0.051 ± 0.006; transferring the scalar posterior to another model
requires checking those assumptions. SPA+BK and SPA+BK+DESI overlap; do
not add their pulls or interpret the marginal summaries as a joint
n_s/r/running likelihood. The paper's 0.0029 width is distinct from
the 0.0027 value in a historical repository summary and must not be
silently substituted. The paper provides joint contours and products, but
they have not been acquired, pinned or validated for this grid. Model
parameters tuned to n_s are not blind predictions.

The candidate engines above are source paths at AEGIS commit
`09a9c6147863f5aca96f72302a9f3bc090506c40`; `observe.py` is a
single-canonical-field route, `mfms_nc.py` needs an independently validated
YFORK2 adapter and returns n_s, scalar power and elapsed e-folds rather
than r or running. Engine source inspection is not validation, and no
engine, comparison or switch has run.
