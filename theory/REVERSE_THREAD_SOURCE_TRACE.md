# Reverse-thread source trace and conditional stability

This note traces the exact-shape reverse thread and separates it from the
bounded reverse-exponential solver in `canonical_solver.py`. The source
revision below is AEGIS commit `e1dfd3769d86852ea9938ce573265dc734eb435c`;
it is newer than the base of this branch. Paths refer to that revision unless
otherwise noted. Historical results are not validation of a combined model.

## Exact shape and normalization

`field_tests\rules\PREREG_D1638_G2_THREAD_SHAPE.md` postulates a second copy
of the v3 shape at the independently chosen dark-energy scale. The
implementation is `tools\serapis_calc\p3s.py:23-27,33-55,63-76`. With
`y = exp(sqrt(2) phi)`, `Re(tau) = 1/2` and `C = 8e-7`, it is

```text
V / V_L = [(2/3) y d_y ln E(tau, 3/2)]^2 [1 + C(E(tau, 3/2) - E(rho, 3/2))]
rho = 1/2 + i sqrt(3)/2
```

Here E is the full lattice sum, not the normalized Fourier convention:
`E_full = 2 zeta(3) E_normalized`. At rho, the values are approximately
8.89274510039729 and 3.69897010575073, respectively. If the normalized E
is used in the tilt, its coefficient must be `C * 2 zeta(3)`; the logarithmic
derivative itself is unaffected. The numerical source implementation truncates
the Fourier series, so its outputs do not by themselves establish an error
bound over all positive y.

For the exact lattice series, E is positive, and `C * E(rho) < 1` for the
stated positive C, so the potential is nonnegative. D1641
(`field_tests\rules\PREREG_D1641_G1B_RHO_CURVATURE.md`) derives
`V''(phi_rho) / V_L = 1/4` for D=10, where
`phi_rho = ln(sqrt(3)/2)/sqrt(2)`. The saved lattice isotropy cross-check is
only accurate at roughly the percent level, as corrected in
`theory\pending_docs\D72_D75_weak_spots.md:16422-16425`.

The original exponential `V_L * (1 - A * exp(-beta * phi))` is not this
exact potential: for positive parameters it has no finite stationary point
and becomes negative at sufficiently small phi. A negative potential alone
does not prove an instability.

## Existing checks and their limits

- D1638's locked comparison found the exact and asymptotic shapes different
  under its stated thresholds. The separate scale and initial condition are
  not derived by that comparison.
- D1642 and D1643 report that the start is not set by the model, with a
  small window estimated under a specified area measure. This is not a
  measure-independent probability.
- D1644 is a historical homogeneous one-field evolution. Its failed first
  grid and subsequent extension are retained in
  `field_tests\rules\PREREG_D1644_G9_THREAD_FUTURE_DEVIATIONS.md`. Below rho
  the one-dimensional line leaves the fundamental domain.
- D1653 tests four initial axion offsets in an assumed two-dimensional
  gradient completion; D1655 and D1658 examine additional starts. These
  finite tests do not establish general basin, quantum or joint-field stability.
- `papers\addenda\24380387_REFEREE.md:4-18` records that later likelihood
  comparisons supersede the earlier Gaussian score, that the proposed
  dark-matter coupling was not detected in the stated full-Planck comparison,
  and that the endpoint depends on the axion and dataset.

The transformation `tau -> tau/(tau+1)` maps rho to
`1/2 + i sqrt(3)/6` and i to `(1+i)/2`. Thus the extra rho zero on the
restricted line is a modular image when the full model actually identifies
these points. A one-dimensional slice, or a proposed interaction between
independently defined fields, does not by itself establish that identification.

## Perturbative curve is not the full curve

D1696's `field_tests\rules\PREREG_REALDATA_EXACT.md` calls its curve exact
for its *perturbative* approximation, explicitly omitting the exponential
Fourier terms. With `c = 2 zeta(2)/zeta(3)` it uses

```text
g(y) = [(1 - c/(3y^2)) / (1 + c/y^2)]^2.
```

Its zero is `y = sqrt(c/3) = 0.9551379578`, rather than the full-series rho
value `0.8660254038`. Direct differentiation with `y = exp(sqrt(2) phi)`
gives `g'' = 1` at that perturbative zero, not the full-shape value `1/4`.
The historical perturbative comparison remains a comparison of its stated
model; it is not a full-series joint fit or a source for the full-shape mass.

## Conditional joint-field example

One hypothetical local construction uses independent SERAPIS, Weave and
thread fields, a positive product metric and nonnegative distance-squared
couplings. If the moduli are at rho, the thread has the exact-shape minimum,
and the assumed potential has an isolated positive-Hessian minimum, all
homogeneous scalar masses there can be positive. These choices do not derive
the common action, coupling or modular identification.

For a flat expanding homogeneous FRW solution with this assumed local
minimum at zero potential, uncoupled nonnegative dust and radiation, define
`E = (1/2) G_ab qdot^a qdot^b + V + rho_m + rho_r = 3 H^2`. The equations give
`E_dot = -3 H (G_ab qdot^a qdot^b + rho_m + 4 rho_r/3)`. If a sufficiently
small connected energy sublevel is compact and contains no other stationary
point, the minimum is locally attractive by LaSalle's invariance principle.
This conditional homogeneous result does not establish inhomogeneous,
metric/matter, vector, tensor, nonlinear field-theory or quantum stability.
The source of the joint action and the field/observer map remain open.
