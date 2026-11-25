# UFE final derivation audit — Copilot, 25 November 2026

**This is the completed derivation audit of the accessible source record, not
a claim that a physical unified field equation has been derived.** The source
record does not contain a common compactification, spectrum, or shared action
for SERAPIS-E and the Weave. No tests, fits, scans, or scientific code were run.

The initial snapshot is
[`UFE_latest_copilot_2026-11-25.md`](UFE_latest_copilot_2026-11-25.md).
This final report closes each requested derivation item where possible and
states why the remaining physical joins are not derivable from the supplied
sources. The controlling baseline is AEGIS `e1dfd3769d86852ea9938ce573265dc734eb435c`;
follow-on notes and exact source pins are listed below.

## 1. What is and is not one equation

There is **no single sourced UFE action** combining the sectors below. These
are separate source theories or explicitly conditional mathematical models.
Putting their terms together would be an assumption, not a derivation.

### Weave v4 proposal

The pinned Weave proposal writes
$$
\mathcal L/\sqrt{-g}=\tfrac12M_P^2R-K_{i\bar j}\partial\Phi^i
\partial\bar\Phi^{\bar j}-V-\tfrac14\sum_a\operatorname{Re}f_a F_a^2
+\tfrac14\sum_a\operatorname{Im}f_a F_a\widetilde F_a
+\mathcal L_{\rm matter},
$$
$$
K=-\ln[-i(S-\bar S)]-2\ln\mathcal V(T_{\rm vis},T_{\rm dark},\ldots)
-\ln[-i(U_3-\bar U_3)]+\sum_\alpha K_\alpha|\Phi_\alpha|^2,
$$
$$
S=C_0+i/g_s,\quad
f_{\rm vis}=T_{\rm vis}+9S,\quad f_{\rm dark}=T_{\rm dark},
$$
$$
W=W_0+A e^{-2\pi T_{\rm vis}/6}+W_{\rm dark}
+Y_qQHq^c+Y_\ell LHe^c+Y_\nu LHN+\tfrac12M_NNN,
$$
$$
V(S)=V_\infty G^{S\bar S}|\partial_S\ln E_{3/2}(S)|^2
+V_{\rm thread}(\phi_{\rm thread})+V_{\rm soft}.
$$
This proposal names a $Z_6$-II orientifold, freezes $U_1,U_2$ at $\rho$,
and treats $U_3$ as the free complex structure. It gives
$N=6$, $x=2\pi\sigma_{\rm vis}/N=21.10$,
$\sigma_{\rm vis}=20.15$, $A=0.54$, $|W_0|\simeq5.6\times10^{-9}$,
$\mathcal V=4.0\times10^4$, $\sigma_{\rm dark}=40.3$, and
$m_{3/2}=2.58\times10^5$ GeV as source-model values. They are not
parameters derived for a common UFE.

The v3 record explicitly includes a $4/9$ factor and tilt; v4 displays a
complex-gradient normalization without that explicit tilt. Under the stated
Wirtinger and kinetic conventions, literal v4's untilted cusp is $9/4$
its coefficient, and matching YFORK2's untilted base takes
$V_{\rm YF}=(9/4)V_{\rm v4}$. Source-owner intent remains unknown. The
reported $0.5625\times2$ at $\rho$ means two degenerate eigenvalues
$9/16$, not one $9/8$ eigenvalue.

The gauge notation is internally inconsistent: with $S=C_0+i/g_s$,
$\operatorname{Re}\rho=1/2$ and $\operatorname{Im}\rho=\sqrt3/2$, yet
the source uses $9\operatorname{Re}S=7.79$ at $\rho$. The number is
$9\operatorname{Im}\rho$. A proposed reading uses $\operatorname{Im}S$
as the physical coefficient, but the full transformed $K,W,f$, duality,
and theta-term conventions are not supplied. This audit does not silently
repair the source.

### Locked YFORK2 scalar sector

For $\tau=x+iy$, $y>0$, the separate scalar-only source model is
$$
\mathcal L=\tfrac12R-\frac{\dot x^2+\dot y^2}{4y^2}-V,\quad
V=V_0[1+C(E_{3/2}(\tau)-E_{3/2}(\rho))],
$$
$$
V_0=\tfrac49y^2|\nabla\ln E_{3/2}|^2,\quad C=8\times10^{-7},\quad
G_{ab}=\delta_{ab}/(2y^2),\quad \rho=e^{i\pi/3}.
$$
Its homogeneous equations are
$$
\ddot x-\frac2y\dot x\dot y+3H\dot x+2y^2V_x=0,\qquad
\ddot y+\frac{\dot x^2-\dot y^2}{y}+3H\dot y+2y^2V_y=0,
$$
$$
H^2=\{(\dot x^2+\dot y^2)/(4y^2)+V\}/3.
$$
Here $E_{3/2}$ has Laplace eigenvalue $3/4$. This is not the full Weave
action or a joint five-field model.

### SERAPIS-E source sector

SERAPIS-E uses $E_2(U)$, Laplace eigenvalue $2$, in the stated
$T^6/(\mathbb Z_2\times\mathbb Z_2)$ orientifold. Its shape is
$$
z=E_2(U)-E_2(\rho),\qquad
V_{\rm SE}(U)=V_0\,\frac{z(1+Cz)}{1+z}.
$$
The uplift plateau $V_0$ is chosen, not derived from this compactification.
The source does not identify this $U$ with any Weave modulus.

## 2. Conditional bridges — separate models, not the UFE

### Loop-metric candidate

For independent $U=x+iy$, $S=c+is$, fixed other moduli, and
$\gamma\ge0$, the chosen truncation is
$$
K=-\ln(2y)-\ln(2s)+\gamma E_2(U)/s,\qquad
F=1+2\gamma E_2/s.
$$
Using $y^2(E_{xx}+E_{yy})=2E$ and
$|\nabla t|=2t/y$ for each positive lattice summand $t$,
$$
K_{U\bar U}=F/(4y^2),\quad K_{S\bar S}=F/(4s^2),\quad
K_{U\bar S}=-\gamma(E_y+iE_x)/(4s^2),
$$
$$
\det K_{I\bar J}
=\frac{F^2-\gamma^2y^2|\nabla E_2|^2/s^2}{16y^2s^2}
\ge\frac{1+4\gamma E_2/s}{16y^2s^2}>0.
$$
Thus the metric is positive throughout this chosen two-field truncation.
For $\gamma>0$, it does not have independent full $S$-modular symmetry.
This proof does not cover omitted fields, loop corrections, matter constraints,
or a common compactification.

A separate potential on that metric is
$$
\begin{aligned}
V={}&V_0\frac{z[1+(\gamma/s)z]}{1+z}
+V_w\frac49s^2|\nabla\ln E_{3/2}(S)|^2
[1+C_w(E_{3/2}(S)-E_{3/2}(\rho))]\\
&+\eta J_2(U)J_{3/2}(S),\quad
z=E_2(U)-E_2(\rho),\quad
J_p(T)=E_p(T)/E_p(\rho)-1.
\end{aligned}
$$
$C_w,\eta\ge0$, $V_0,V_w>0$, and the combined action are assumptions.
Although the explicit $\eta$ link begins quartically at $(\rho,\rho)$,
the full covariant potential has a mixed cubic. It cannot inherit a
cubic-free stability theorem. The candidate's own 2:1 mass tuning is
$V_w=32V_0E_2(\rho)$.

### Modular-invariant and product-link alternatives

On a tree product metric, another proposed potential is
$$
J(T)=\frac{E_2(T)-E_2(\rho)}{E_2(\rho)},\qquad
V_{\rm link}=\frac{\eta}{2}J(U)J(S)
+\frac{\kappa}{2}(\phi-\phi_{\rm ref})^2[J(U)+J(S)].
$$
For $\eta,\kappa\ge0$, $J\ge0$, $J(\rho)=0$, the first term begins
quartically and the second adds
$\kappa(\phi_\rho-\phi_{\rm ref})^2$ to each modulus mass-squared in the
stated tree-metric convention. These couplings and the physical identity of
$\phi$ are assumed.

A separate independent-modular candidate uses
$$
K=-\ln(2\operatorname{Im}U)-\ln(2\operatorname{Im}S),\qquad
V_{\rm link}=\Lambda I_{3/2}(S)I_2(U),\quad\Lambda\ge0.
$$
The $I_p$ definitions and UV origin are not complete in the available
source record. A proposed mediator
$$
\Delta V=-\frac{(aJ_2(U)+bJ_{3/2}(S))^2}{2M_\chi^2},\qquad
\chi_*=-\frac{aJ_2(U)+bJ_{3/2}(S)}{M_\chi^2}
$$
also generates both negative self terms; it does not derive an isolated
positive cross term. Its mediator, couplings, and UV completion are assumed.

### Flux bridge

For $W=A(U)-SB(U)$, suppose $W=D_UW=D_SW=0$, the Kähler metric is
positive diagonal, there is no omitted sector or uplift, and an unbroken
$U$-only order-three symmetry acts at $U=\rho,S=S_0$. Then
$$
A(\rho)=B(\rho)=0,\quad A'(\rho)=S_0B'(\rho),\quad
a=A''-S_0B'',\quad b=B',
$$
$$
W_2=\tfrac12a(\delta U)^2-b\delta U\delta S,\qquad
V_2=e^K\{K^{U\bar U}|a\delta U-b\delta S|^2
+K^{S\bar S}|b\delta U|^2\}.
$$
The symmetry selection rule is $a\bar b=0$. For $b\ne0$, $a=0$
and four real masses equal
$e^K K^{U\bar U}K^{S\bar S}|b|^2$; for $b=0$, the $S$ multiplet is
massless in this truncation. Matching this quadratic term to the loop
candidate requires $V_w=8V_0E_2(\rho)$, inconsistent with that model's
separate $32V_0E_2(\rho)$ tuning. This is a toy F-term result, not a
flux-realization theorem or a joint action.

The mathematical example
$W=c(S-S_0)E_4(U)/\eta_{\rm Ded}(U)^{10}$ has the relevant local weight character,
but exponential cusp growth and no supplied flux periods or tadpole
realization. D1504 freezes complex structure and effective periods;
SPTILT_TF's no-scale slice has $W\ne0$. Neither supplies the bridge's
assumptions.

## 3. Derivations completed conditionally

### Separate local masses

At $\rho$, in the stated tree-canonical conventions, the source potentials
give $m_U^2=2V_0E_2(\rho)$ for each SERAPIS-E component,
$m_S^2=V_\infty/4$ for each YFORK2 component, and $m_\phi^2=V_L/4$
for the postulated late exact-shape scalar. These are separate models.
Weave's $0.5625\times2$ means two degenerate eigenvalues $9/16$, not one
mass $9/8$. A 2:1 tuning is not a derived resonance or field identity.

### Moving extremum with coupled dust (T1)

Given
$$
\rho_c=\rho_{c*}(a_*/a)^3e^{b(\phi-\phi_*)},\qquad
V_\phi+b\rho_c=0,
$$
differentiate with respect to $N=\ln a$. Since
$\rho_{c,N}=(-3+b\phi_N)\rho_c$, the chain rule gives
$$
(V_{\phi\phi}+b^2\rho_c)\frac{d\phi_{\min}}{d\ln a}
-3b\rho_c=0,\qquad
\frac{d\phi_{\min}}{d\ln a}
=\frac{3b\rho_c}{V_{\phi\phi}+b^2\rho_c},
$$
when the denominator is nonzero. This is the instantaneous-extremum slope;
it does not imply the field equation tracks that extremum. The requested
comparison to the D1716 CLASS trajectory at $z=0,1,3$ cannot be performed
from the accessible record: the saved background is absent and no code was
run. No tracking tolerance is claimed.

### Eta-kappa Hessian boundary (T3)

For the local five-field ansatz
$$
V_5=V_{\rm base}+\eta|e-w|^2
+\kappa(\phi-\phi_{\rm ref})^2(|e|^2+|w|^2),
$$
take paired real canonical components, baseline
$\tfrac12\mu_e^2e^2+\tfrac12\mu_w^2w^2$, and
$\Delta=\phi_0-\phi_{\rm ref}$. The modulus block is
$$
H_{\rm mod}=
\begin{pmatrix}
\mu_e^2+2\eta+2\kappa\Delta^2&-2\eta\\
-2\eta&\mu_w^2+2\eta+2\kappa\Delta^2
\end{pmatrix}.
$$
The local strict-minimum conditions are
$H_{11}>0$, $\det H_{\rm mod}>0$, and positive thread curvature.
This is the boundary for the explicitly stated normalization; it is not a
source-specific physical boundary because $\mu_e^2,\mu_w^2$ and the shared
action are not supplied.

A different conditional reverse-thread model has
$$
\begin{aligned}
V_{\rm joint}={}&V_{\rm SE}(U)+V_{\rm W,completion}(S)
+V_R(\phi)+R e^{b(\phi-\phi_{\rm ref})}
+\tfrac{\eta}{2}d_G(U,S)^2\\
&+\tfrac{\kappa}{2}(\phi-\phi_{\rm ref})^2
[d_G(U,\rho_{\rm lift})^2+d_G(S,\rho_{\rm lift})^2],\\
V_R={}&V_L(1-Ae^{-\beta\phi}),\quad
A=16\zeta(2)/(3\zeta(3)),\quad\beta=2\sqrt2.
\end{aligned}
$$
At $U=S=\rho=\rho_{\rm lift}$, its canonical modulus block is
$$
\begin{pmatrix}k_E+\eta+\kappa\Delta^2&-\eta\\
-\eta&k_W+\eta+\kappa\Delta^2\end{pmatrix}.
$$
For $k_E,k_W>0,\eta,\kappa\ge0$, this block is positive. At the frozen
dust balance, the thread curvature is
$$
\beta A V_Le^{-\beta\phi}+b\rho_c=0,\qquad
(V_R+R e^{b(\phi-\phi_{\rm ref})})_{\phi\phi}
=b(b+\beta)\rho_c.
$$
Thus $b=-0.074$, with $-\beta<b<0$, gives a saddle regardless of
positive $\eta,\kappa$; $b<-\beta$ can give positive frozen curvature,
but is not an adopted source parameter. At $b=-\beta$ there is no
isolated extremum. These frozen local results do not prove an evolving
attractor. This reverse-thread construction and the preceding local ansatz
are not the same model.

### Perturbation specification (T2)

For the conditional five-real-field model
$x^I=(x_E,y_E,x_W,y_W,\phi)$, use the tree product metric
$$
G_{IJ}=\operatorname{diag}(1/(2y_E^2),1/(2y_E^2),
1/(2y_W^2),1/(2y_W^2),1),
$$
Einstein gravity, Newtonian gauge $\Phi=\Psi$, zero anisotropic stress,
pressureless dust with $m/m_i=e^{b(\phi-\phi_i)}$, and uncoupled perfect
radiation. Put $N=\ln a,\ p=x_N,\ q^I=\delta x^I,\ B=\Phi_N$,
$F^I=G^{IJ}V_{,J}$. Then
$$
\rho_c=\rho_{c,i}e^{-3N+b(\phi-\phi_i)},\quad\rho_r=\rho_{r,i}e^{-4N},
\quad H^2=\frac{\rho_c+\rho_r+V}{3-G_{IJ}p^Ip^J/2},
$$
$$
\epsilon=\frac{\rho_c+4\rho_r/3+H^2G_{IJ}p^Ip^J}{2H^2},\quad
p_N=-(3-\epsilon)p-\Gamma(p,p)-F/H^2-b\rho_c e_\phi/H^2.
$$
For nonzero comoving $k$, the conditional linear system is
$$
\begin{aligned}
q^I_{NN}={}&-(3-\epsilon)q_N^I-2\Gamma(p,q_N)^I
-(\partial_K\Gamma^I{}_{JL})q^Kp^Jp^L
-\frac{k^2}{(aH)^2}q^I-\frac{(\partial_JF^I)q^J}{H^2}\\
&+4p^I B-\frac{2F^I\Phi}{H^2}
-\frac{b\rho_c(\delta_c+2\Phi)}{H^2}e_\phi^I,\\
\delta_{c,N}={}&-\frac{k^2v_c}{aH}+3B+bq_{\phi,N},\quad
v_{c,N}=-(1+bp_\phi)v_c+\frac{\Phi+bq_\phi}{aH},\\
\delta_{r,N}={}&-\frac43\frac{k^2v_r}{aH}+4B,\quad
v_{r,N}=\frac{\delta_r/4+\Phi}{aH}.
\end{aligned}
$$
Impose
$$
B=-\Phi+\tfrac12G_{IJ}p^Iq^J
+\frac{a[\rho_cv_c+(4/3)\rho_rv_r]}{2H},
$$
and check
$$
k^2\Phi+3(aH)^2(B+\Phi)+a^2\delta\rho/2=0,\quad
\Phi_{NN}+(4-\epsilon)B+(3-2\epsilon)\Phi-\delta p/(2H^2)=0,
$$
with
$$
\delta\rho=\rho_c\delta_c+\rho_r\delta_r+K+V_{,I}q^I,\quad
\delta p=\rho_r\delta_r/3+K-V_{,I}q^I,
$$
$$
K=H^2[G_{IJ}p^Iq_N^J+\tfrac12(\partial_KG_{IJ})q^Kp^Ip^J
-G_{IJ}p^Ip^J\Phi].
$$
Here $\delta_c$ is the physical dust energy-density perturbation. This
completes the requested **conditional specification only**. It is not
derived from a shared UFE action and does not provide a reduced
scalar-fluid-metric no-ghost/gradient proof, full species hierarchy, vector
or tensor perturbations, quantum state, or backreaction.

## 4. Status of each field and parameter

- **CONDITIONAL** — Weave $S=C_0+i/g_s$, $\rho=e^{i\pi/3}$,
  $g_s=2/\sqrt3$; the latter is outside perturbative control.
- **CONDITIONAL** — Weave $T_{\rm vis}$, $f_{\rm vis}=T_{\rm vis}+9S$,
  $N=6,\sigma_{\rm vis}=20.15,x=21.10,A=0.54,|W_0|\simeq5.6e-9$,
  $\mathcal V=4.0e4,m_{3/2}=2.58e5$ GeV, within its KKLT proposal.
- **CONDITIONAL** — Weave $T_{\rm dark},f_{\rm dark}=T_{\rm dark}$,
  $\sigma_{\rm dark}=40.3$, and dark gauge sector; the dark-cycle size is
  conjectural in that source.
- **CONDITIONAL** — Weave $U_3=i$, a choice, not a field identification.
- **OPEN** — Weave $\phi_{\rm thread}$ and $V_{\rm thread}$; its
  geometric origin and potential are not supplied.
- **CONDITIONAL** — Weave matter multiplets and $Y_q,Y_\ell,Y_\nu,M_N$;
  the quark spurion, Koide inputs, and neutrino fluxes $(4,4,8)$ are
  phenomenological/chosen inputs, not a derived shared action.
- **ASSUMED** — Weave $V_\infty^{1/4}=4.9\times10^{15}$ GeV,
  $\delta_{\rm Koide}=2/9,c_e$, $|u|\simeq0.0266$, fluxes $(4,4,8)$,
  $v/m_{\rm SUSY}\simeq2.7\times10^{-7}$, and $\sigma_{\rm dark}=40.3$;
  these are TRUST/phenomenological/chosen/tuned inputs in that proposal.
- **CONDITIONAL** — Weave dark baryon $X$, dark photon $A'$, and split
  superpartners/$V_{\rm soft}$, only in that proposal; its quoted
  $m_{3/2}=2.58\times10^5$ GeV is not a shared-action prediction.
- **CONDITIONAL** — YFORK2 $\tau=x+iy$, $G_{ab}=\delta_{ab}/(2y^2)$,
  $C=8e-7$, $V_\infty$, and $\rho$, only in its scalar model.
- **CONDITIONAL** — SERAPIS-E $U$, $E_2(U)$, $V_0$, and coefficient
  $C$, only in its $T^6/(\mathbb Z_2\times\mathbb Z_2)$ source.
- **ASSUMED** — Loop truncation $\gamma$, product-link $\Lambda,I_p$,
  mediator $a,b,M_\chi$, modular-link $\eta,\kappa,\phi_{\rm ref}$, and
  each proposed UV completion.
- **CONDITIONAL** — Flux-bridge $A(U),B(U),S_0$ and masses, only under its
  SUSY-Minkowski, symmetry, diagonal-metric, and no-omitted-sector assumptions.
- **ASSUMED** — Five-field local $e,w,\phi$, its baseline Hessian, and
  link normalization.
- **ASSUMED** — Dust coupling $b$, $\rho_{c*}$, $R$, and reverse-thread
  distance links and $\rho_{\rm lift}$ in the separate conditional
  late-sector construction.
- **OPEN** — Source-owner gauge-field dictionary and transformed theta term
  for the Weave $f_{\rm vis}$.
- **DERIVED** — The modular eigenvalues $2$ and $3/4$ differ; a simple
  isometric identification of $E_2$ and $E_{3/2}$ does not follow.
- **OPEN** — Shared light-field spectrum, common $K,W,V$, uplift, field
  dictionary, and all physical cross-couplings.
- **OPEN** — Physical photon/observer map, matter transfer, full perturbation
  action, nonlinear stability, and quantum state/backreaction.

## 5. Explicit non-derivability and blockers

- **OPEN — Compactification / field map.** SERAPIS-E's $E_2(U)$ comes from
  $T^6/(\mathbb Z_2\times\mathbb Z_2)$; the Weave names $Z_6$-II.
  Neither source supplies a common light spectrum, brane/duality action, or
  field map. Therefore the sources do not determine a shared action. The
  $E_2$ and $E_{3/2}$ eigenvalues differ (2 versus $3/4$); equal
  $\rho$ coordinates and matched local masses do not remove the mismatch.
- **BLOCKED — Gauge convention.** The source's real-part coefficient and
  its numerical value disagree. A consistent field redefinition requires
  transformed holomorphic functions, dualities, and theta convention not
  present in the record. Source-owner intent is needed; no silent swap is
  justified.
- **BLOCKED — T1 application.** The D1716 saved CLASS background needed for
  the requested values at $z=0,1,3$ is inaccessible here. The exact
  moving-extremum relation is derived, but evaluating tracking or choosing
  a tolerance without the specified trajectory would invent data.
- **OPEN — Source-specific T3 boundary.** The algebraic Hessian conditions
  are derived for each stated hypothetical normalization, but a common
  baseline Hessian and action are absent. They cannot establish physical
  stability of the unprovided theory.
- **OPEN — Physical perturbations and observables.** The T2 equations are
  conditional on a chosen action and fluid closure. Without the action and
  constraint-reduced kinetic/principal-gradient matrices, full perturbative
  stability, photon mapping, lensing, and quantum conclusions are not
  derivable.
- **OPEN — Flux realization.** D1504 freezes complex structure and effective
  periods; SPTILT_TF is no-scale with nonzero $W$. The toy bridge and
  mathematical modular-SUGRA example do not provide joint quantized flux
  periods, tadpoles, or a controlled UV completion.
- Historical chronometer source-capture agreement is a post-hoc 14-row
  in-grid reproducibility comparison with no author $H_0>50$ prior; it is
  not a calibrated UFE fit or physical evidence.

## 6. Round-three disposition and completion

- **T1:** derivative relation **DERIVED**; requested CLASS-background
  comparison **BLOCKED** for absent input data.
- **T2:** required fields, gauge, equations, fluid closure, and constraint
  checks **CONDITIONAL** on the stated product-metric action; derivation from
  the physical UFE **OPEN** because no shared action exists.
- **T3:** generic and reverse-thread local Hessian boundaries
  **CONDITIONAL / DERIVED** above; physical applicability **OPEN**.
- **Compactification gap:** **OPEN**, not resolved.

The derivation audit is complete to the evidence available: every proposed
bridge is either derived under stated assumptions or explicitly marked
non-derivable from missing source inputs. **The UFE itself is not complete**;
no unified physical action or resolved compactification is claimed.

## 7. Branch and source provenance

Remote tips checked during this audit, plus explicitly identified local-only
snapshots:

| Repository | Branch | Commit | Status |
|---|---|---|---|
| AEGIS | `unify-bg` | `523fc6db1b0a004f129dd88709a5e85f57fd1c2e` | Tip before this final report commit |
| AEGIS | `dannyeldridge54-jubilant-doodle` | `523fc6db1b0a004f129dd88709a5e85f57fd1c2e` | Local worktree tip before this final report commit |
| AEGIS | `master` | `f8df6cc` | Remote baseline tip checked |
| AEGIS | `dannyeldridge54-fluffy-invention` | `d9b679f169e572a2395a97c3c4fd0fb8d78f1b2b` | Remote tip checked |
| AEGIS | `dannyeldridge54-ufe-physical-derivation` | `a3fad45a802f378426c6a3352a6d13bf85e250b1` | Remote tip checked |
| CubeMind | `dannyeldridge54-data-lense-derivation-engine` | `c345aaaef329175a27b8acabb24bea29cd9337ba` | Remote tip checked |
| CubeMind | `dannyeldridge54-scalar-quantum-connection` | `a420798964484e7ca0211fb2ab99e019ec703381` | Remote tip checked |
| CubeMind | `dannyeldridge54-crispy-eureka` | `3339a0af6676b0753b350218216a015f83add177` | Coordinator-provided local HEAD; remote unverified |
| CubeMind | `master` | `bbccd0be24753d0f6e7fd8b9a0eb0c92aec50f83` | Coordinator-provided local HEAD; remote unverified |

Coordinator-provided uncommitted artifacts in other sessions were not
assumed to be included in these commits. Pinned AEGIS records include
`tools/project_docs/WEAVE_UNIFIED_EQUATION.md`,
`field_tests/rules/PREREG_YFORK2.md`,
`papers/v3/serapis_v3.3_draft.tex`,
`theory/COMMON_ACTION_CHECK.md`,
`field_tests/rules/PREREG_D1504_flux_tilt.md`,
`field_tests/rules/PREREG_SPTILT_TF.md`, and
`field_tests/rules/PREREG_D2051_tether_dark_visible.md`.
Weave v3 and v4 pins reported by the coordinator are respectively
`a4823abd6640008413bdcc71fa3f20bfbbc66e74` and
`9b77c9ae2d27e2b37d0c4ebe9be04889add9f7dc`.
