# Conditional common-action consistency check

This is a post-hoc algebraic check, not a preregistered prediction, fit, or
observational evidence. Source paths below refer to AEGIS commit
`e1dfd3769d86852ea9938ce573265dc734eb435c`.
The candidate does not derive a common compactification.

## What is combined, and what is not

SERAPIS-E uses an E(U,2) one-loop correction in a specific IIB
T6/(Z2 x Z2) orientifold; the plateau is placed in the uplift sector by
choice, and brane-position stability needs a separate mechanism
(`papers\v3\serapis_v3.3_draft.tex:224-238`). The Weave equation instead
proposes a Z6-II orientifold with U1/U2 frozen at rho and U3 free
(`tools\project_docs\WEAVE_UNIFIED_EQUATION.md:26-43`). The late scalar is
a postulated second copy at an independent scale, not a derived field
identity (`field_tests\rules\PREREG_D1638_G2_THREAD_SHAPE.md`). Neither
source supplies their shared light spectrum, full K, W and uplift, or a
derivation of cross-couplings. Additional loop channels are omitted here.

## A conditional loop metric

Assume two independent complex fields U=x+iy and S=c+is, y,s>0, fixed
other moduli, and the *chosen* truncated Kähler potential, in Planck units:

```text
K = -ln(2y) - ln(2s) + gamma E2(U)/s,  gamma >= 0
E2(U) = sum' y^2 / |m+nU|^4,          F = 1 + 2 gamma E2/s.
```

The loop term is sourced by the orientifold above; applying it together
with these tree terms and a dynamical S is an additional model choice.
Using y^2(E_xx+E_yy)=2E gives

```text
K_UbarU = F/(4y^2),       K_SbarS = F/(4s^2)
K_UbarS = -gamma(E_y+i E_x)/(4s^2).
```

For each positive lattice summand t, |grad t|=2t/y, so the triangle
inequality gives |grad E2| <= 2E2/y. Consequently

```text
det(K_IbarJ)
  = [F^2 - gamma^2 y^2 |grad E2|^2/s^2]/(16 y^2 s^2)
  >= [1 + 4 gamma E2/s]/(16 y^2 s^2) > 0.
```

Both diagonals are positive, so this truncated two-complex-field metric
is positive everywhere in the upper half-planes for gamma >= 0. At rho,
grad E2=0 and the kinetic metric is F times the tree metric. This does
not cover omitted fields, higher corrections, fluids, reduced
metric/matter constraints, or quantum stability.

The truncated K is invariant under U modular transformations up to a
Kähler transformation, but it does not have an independent full S
modular symmetry when gamma>0. For S -> -1/(S-1), which fixes rho, the
loop term changes by

```text
gamma E2(U) [((c-1)^2+s^2-1)/s].
```

Its mixed S derivative is 3 gamma E2/16 at c=1,s=2; thus it is not a
Kähler transformation. Omitted UV terms could change this conclusion.
The source record also says D7/O7 break full S duality
(`theory\pending_docs\D72_D75_weak_spots.md:18820-18828`).

## Vacuum curvature and symmetry-compatible alternative

In tree hyperbolic canonical tangent coordinates q, at
rho=1/2+i sqrt(3)/2, the SERAPIS-E potential has m_U^2=2 V0 E2(rho)
for each real U component. YFORK2's separately specified
`(4/9)y^2 |grad ln E(S,3/2)|^2` has m_S^2=V_inf/4 for each real S
component, from its stated normalization and the E3/2 Laplace equation.
The D=10 late-thread slice has m_phi^2=V_L/4 (D1641). Positive
heights make these positive. The late thread is a one-dimensional
postulate, not a unique two-dimensional modular completion.

The hypothesized eta d(U,S)^2/2 adds the matrix
`[[eta,-eta],[-eta,eta]]` in each pair of tree-canonical tangents.
It is positive semidefinite for eta>=0, but violates an independent
rho order-3 rotation of U alone. Such a coupling needs an identified
diagonal symmetry or explicit/spontaneous breaking. It is not a general
no-go if those symmetries do not survive the actual compactification.

A different, *postulated* smooth potential uses
`J(T)=[E2(T)-E2(rho)]/E2(rho)`:

```text
V_link = eta J(U)J(S)/2
       + kappa (phi-phi_ref)^2 [J(U)+J(S)]/2.
```

J is nonnegative, modular invariant, and locally J=|q|^2+O(|q|^3).
For eta,kappa>=0 the first term is quartic at rho; the second adds
`z=kappa (phi_rho-phi_ref)^2` to each modulus mass-squared.
This potential is separately modular invariant if phi is a singlet;
the kinetic truncation above still breaks independent S duality. If
both modulus kinetic blocks receive the loop factor F at rho, their
tree-coordinate Hessian eigenvalues divide by F. A positive vacuum
Hessian does not show that the same point is stationary with coupled
dust: the phi equation adds the force b rho_c.

The gauge conventions also need resolution: the Weave defines
S=C0+i/g_s and uses Re f_vis with f_vis=T_vis+9S, while
`field_tests\rules\PREREG_D2051_tether_dark_visible.md` substitutes
Re S=sqrt(3)/2 at rho. Literal Re rho=1/2. A possible redefinition
S_std=-iS requires transforming all K, W, f, dualities and theta-term
conventions consistently; it must not be silently applied. The cloud
coordinator's C2 bridge reply identifies 1/g_s=Im S as the intended
physical coefficient and calls for dated correction D2257. The full
transformed holomorphic functions and theta convention still need to
be supplied before the action is consistent.

## Reproduce the algebra

With the project's `requirements-tools.txt` installed, run:

```powershell
python theory\check_loop_kinetics.py
```

This uses SymPy to verify the metric derivatives, the summand gradient
identity, the determinant bound's numerator, the S-duality counterexample,
and the local block Hessian. The lattice triangle inequality, source
assumptions, positive-height conditions and physical interpretations
remain explicit mathematical arguments, not numerical fit results.
The decisive next step is a single specified compactification and its
complete light fields, symmetry action, K, W, uplift, gauge functions,
and late-sector couplings; then compute the covariant Hessian and full
reduced perturbation matrices on an on-shell background.
