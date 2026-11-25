# R1-R4 source review (Copilot)

This is a source review and bounded diagnostic, not completion of the R1-R4
calculations or a unified-field derivation. Historical AEGIS citations below
refer to commit `e1dfd3769d86852ea9938ce573265dc734eb435c`.
The late exact-shape field as a second copy is a **postulate**
(`field_tests/rules/PREREG_D1638_G2_THREAD_SHAPE.md`), not a derived field
identity or a common microscopic action.

## Assessment

- **R1:** A local Hessian calculation can delimit parameter choices for the
  stated hypothetical model. A finite grid does not establish a global
  stability region, coupled spacetime dynamics, or quantum stability.
- **R2:** `joint_field_points.frozen_extremum` at CubeMind commit
  `0da7d6cad78cf8158fa31c438cbc985c6d72e3df` implements the released
  reverse-exponential branch, not the D1638 full exact shape; it also requires
  strictly negative b. Its b-to-zero limit cannot return the rho minimum and
  curvature V_L/4: the exponential has no finite stationary minimum at b=0.
  An exact-shape root requires a separately specified potential and input,
  not relabelling that function.
- **R2/R3 dynamics:** The source coupling satisfies
  `rho_c = rho_c* (a*/a)^3 exp[b(phi-phi*)]` and
  `phi_ddot + 3H phi_dot + V_phi = -b rho_c`
  (`PREREG_COUPLED_THREAD.md` and `PREREG_NEGSPACE_DERIVE.md`). A frozen
  extremum is not generally an on-shell evolving solution. When
  `V_phi + b rho_c = 0`, differentiation gives
  `d phi_min/d ln a = 3 b rho_c/(V_phiphi + b^2 rho_c)` if the denominator
  is nonzero. An exactly tracked moving extremum must also satisfy the field
  equation. The rho/quarter limit applies to the *uncoupled exact shape*,
  not to the unrelated exponential helper.
- **R3 perturbations:** `Omega^2 = k^2/a^2 + m^2 + rho_r/4` belongs to the
  specified stationary, uncoupled, zero-vacuum test background. It cannot
  simply be used for a rolling coupled scalar with dust and metric
  perturbations. A conserved Wronskian checks normalization, not physical
  stability, interacting quantum theory, or renormalized backreaction.
- **Gauge conventions remain open:** `WEAVE_UNIFIED_EQUATION.md:38,48,58`
  defines `S=C0+i/g_s` and uses `Re(T+9S)` for the gauge kinetic coefficient.
  `PREREG_D2051_tether_dark_visible.md:3` instead evaluates `Re S` as
  `sqrt(3)/2` at rho. The literal first convention has `Re S=1/2`.
  An explicit change of variables, including gauge and theta-term conventions,
  is needed before combining these expressions or propagating their numbers.

## Density anchors and sign

The sign of the physical mass change is determined by
`b (phi_today - phi_reference)`, not by b alone. D1716's locked input uses
`amp=1.83`, `b=-0.074`, a CMB anchor at `z*=1090`, and its specified CLASS
background; its saved residual remains historical and its shape-match rule
failed. The saved `field_tests/results/coupled_thread.json` is a distinct
fit output: its parameter order is verified in
`field_tests/scripts/realdata/coupled.py:38-40`, with
`amp=0.8999990721775433` and `b=-0.06242464324193747`. Do not substitute one
for the other.

The pre-output D2134 addendum's sign claim was later corrected, not erased:
`theory/pending_docs/D72_D75_weak_spots.md:21597-21601` reports
`Delta phi=+0.62` for `b=-0.05` and `Delta phi=-0.84` for `b=+0.05`, so both
examples have `b Delta phi < 0` and losing mass. This is not a universal
statement for arbitrary trajectories. D1716's negative b with increasing phi
is consistent with mass loss. D2134 also distinguishes present-day and
recombination anchors; those produce different effective-density residuals.
The historical D1725 and D2134 non-adoption verdicts remain unchanged.

## R4: i-class point

The point `tau=(1+i)/2` and its i-class endpoint were already documented in
`theory/pending_docs/D72_D75_weak_spots.md:16440-16444` and
`field_tests/rules/PREREG_D1653_G9B_TAU_PLANE.md`. The modular map
`tau -> tau/(tau+1)` takes i to `(1+i)/2`; physical identification requires
the full model to impose the relevant SL(2,Z) quotient.

For the full lattice E, `x=1/2`, `y=exp(sqrt(2) phi)`, `C=8e-7` and
`f=V/V_L`, at `y=1/2` one has `f=f'=0`. A **post-hoc diagnostic**, using
analytic Bessel derivatives at 24 and 40 Fourier terms, gives
`f'' = 0.0857411841375`. The two truncations agree at the displayed precision;
this is not an interval-certified error bound, a preregistered result, or a
test of the complete two-dimensional, joint, or quantum dynamics.
