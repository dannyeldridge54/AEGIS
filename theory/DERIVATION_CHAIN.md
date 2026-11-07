# BI field and scalar-field derivation chain

This note separates algebraic consequences of the stated supergravity/QCD inputs
from assumptions used by AEGIS phenomenology. It is a derivation of the current
implemented equations, not a derivation of the proposed torsion-born $n=3$
Twist potential from a microscopic quantum-gravity action.

## 1. Kähler geometry and the canonical kinetic coupling

Take the quoted BI chiral-superfield Kähler potential

$$
\Omega=e^{\Phi+\bar\Phi}(\Phi+\bar\Phi),\qquad
K=-3\ln(-\Omega/3),
$$

and define $S=\Phi+\bar\Phi$, with $S<0$. Then

$$
K=-3\left(S+\ln(-S/3)\right),\qquad
K_\Phi=-3(1+S^{-1}),\qquad
K_{\Phi\bar\Phi}=\frac{3}{S^2}.
$$

On the real-dilaton slice $\Phi=\phi+ia$, $S=2\phi$, so

$$
\mathcal L_{\rm kin}
=-K_{\Phi\bar\Phi}\,\partial\Phi\,\partial\bar\Phi
=-\frac{3}{4\phi^2}\left[(\partial\phi)^2+(\partial a)^2\right].
$$

For $\phi<0$, define the canonically normalized dilaton by

$$
\chi=\sqrt{\frac32}\,M_{\rm Pl}\ln|\phi|,
\qquad
\frac{d\chi}{d\phi}=\sqrt{\frac32}\frac{M_{\rm Pl}}{\phi}.
$$

Rescale the axion coordinate as $\tilde a=\sqrt{3/2}\,M_{\rm Pl}a$.
Substitution gives

$$
\mathcal L_{\rm kin}
=-\frac12(\partial\chi)^2
-\frac12 e^{\lambda\chi/M_{\rm Pl}}(\partial\tilde a)^2,
\qquad
\lambda=-2\sqrt{\frac23}.
$$

Thus the metric and kinetic-coupling slope follow from the quoted $K$, field
normalization, and sign convention. Reversing the orientation of $\chi$
reverses the reported slope. The separate AEGIS map
$\phi_{\rm abs}=\sqrt{3/2}M_{\rm Pl}\operatorname{arsinh}(1/\gamma)$
is a chosen BI-coordinate convention; it is not derived by this Kähler-metric
calculation alone.

## 2. What the constant-superpotential calculation actually gives

For constant $W$, $D_\Phi W=K_\Phi W$, and the $N=1$ F-term potential is

$$
V=e^K\left(K^{\Phi\bar\Phi}|K_\Phi W|^2-3|W|^2\right).
$$

Since $K^{\Phi\bar\Phi}=S^2/3$, the bracket is

$$
|W|^2\left[\frac{S^2}{3}\,9(1+S^{-1})^2-3\right]
=3|W|^2S(S+2).
$$

Using $e^K=e^{-3S}(-S/3)^{-3}$ and $S=2\phi$ yields

$$
V(\phi)=\frac{81}{2}|W|^2
\frac{(-\phi-1)e^{-6\phi}}{\phi^2}.
$$

This expression has a zero at $\phi=-1$, stationary points at
$\phi=-1/2$ and $-2/3$, and $V(-1/2)<0$. The $-2/3$ point is a local
minimum, not a global vacuum, because $V\to-\infty$ as $\phi\to0^-$.
Consequently this specified superpotential does **not** supply the positive,
stable periodic potential assumed in the Twist fits.

There is a stronger sector-specific obstruction: substitute
$\Phi=\phi+ia$, $\bar\Phi=\phi-ia$ before restricting the potential.
Both $K$ and the constant-$W$ F-term potential depend only on $2\phi$.
Thus $\partial V/\partial a=\partial^2V/\partial a^2=0$ exactly.
This sector cannot produce any axion cosine, let alone n=3.
The symbolic regression checks this directly. It does not exclude potentials
from additional symmetry-breaking sectors that are absent here.

The [Gates--Ketov--Yunes construction](https://arxiv.org/abs/0906.4978v3)
provides a dilaton-axion superfield and kinetic geometry; this fact alone
does not fix a superpotential or the proposed late/early-time potential.

## 3. Effective QCD-anomaly axion input

Let $\theta=\varphi/F_\varphi$ be a dimensionless angular field. The low-energy
QCD vacuum energy is periodic in $\theta$; retaining its leading cosine
harmonic is an effective approximation:

$$
V_{\rm QCD}(\varphi)
=\chi_{\rm QCD}(0)\,[1-\cos(\varphi/F_\varphi)].
$$

Expanding about a minimum,

$$
V_{\rm QCD}
=\frac12\frac{\chi_{\rm QCD}(0)}{F_\varphi^2}\varphi^2
+O(\varphi^4/F_\varphi^4),\qquad
m_\varphi^2=V_{\rm QCD}''(0)=\frac{\chi_{\rm QCD}(0)}{F_\varphi^2}.
$$

With the inputs used by `bi_qcd_axion.py`,
$\chi_{\rm QCD}^{1/4}=75.6\,\mathrm{MeV}$ and
$F_\varphi=2.0\times10^{18}\,\mathrm{GeV}$, this gives
$\chi_{\rm QCD}=3.27\times10^{-5}\,\mathrm{GeV}^4$ and
$m_\varphi=2.86\times10^{-12}\,\mathrm{eV}$. The susceptibility is an
external low-energy input here; this is not a first-principles instanton,
thermal-QCD, or quantum-loop calculation. The cosine is not an exact result
for the full QCD free energy at all temperatures.

## 4. Onset and equality-era scaling

In radiation domination, the Friedmann equation and thermal radiation density
give

$$
H(T)=\sqrt{\frac{\pi^2g_*}{90}}\frac{T^2}{M_{\rm Pl}},
$$

where $M_{\rm Pl}$ is the reduced Planck mass. Defining the approximate
oscillation onset by $3H(T_{\rm osc})=m_\varphi$,

$$
T_{\rm osc}
=\left(\frac{m_\varphi M_{\rm Pl}}
{3\sqrt{\pi^2g_*/90}}\right)^{1/2}.
$$

Entropy conservation, $g_{*s}T^3a^3=\mathrm{constant}$, then implies

$$
\frac{a_{\rm eq}}{a_{\rm osc}}
=\frac{T_{\rm osc}}{T_{\rm eq}}
\left(\frac{g_{*s,\rm osc}}{g_{*s,\rm eq}}\right)^{1/3}.
$$

For small initial angle $\theta_i$, the onset energy is approximately
$\rho_{\varphi,\rm osc}\simeq\chi_{\rm QCD}\theta_i^2/2$. Once $m\gg H$,
the harmonic oscillations average to pressureless matter, so
$\rho_\varphi\propto a^{-3}$. If the onset is radiation dominated, a useful
small-angle estimate for the scalar fraction of total density at equality is

$$
f_{\varphi,\rm eq}
\simeq \frac12
\frac{\chi_{\rm QCD}}{\rho_{\rm bg,osc}}
\frac{\theta_i^2}{2}\frac{a_{\rm eq}}{a_{\rm osc}}.
$$

The leading factor $1/2$ converts the scalar-to-radiation ratio at equality
to a fraction of total density when matter and radiation are equal. This
estimate assumes the field is subdominant at onset, the background is
radiation-dominated then, and oscillations are harmonic by equality; it is not
a likelihood result. The ODE in `bi_qcd_dynamics.py` improves on this
small-angle estimate by including scalar energy in the homogeneous Friedmann
constraint and Hubble friction until the configured rapid-oscillation/WKB
handoff.

## 5. Homogeneous field equations used by the numerical solver

For a canonical homogeneous scalar with the cosine potential in a
Friedmann--Lemaître--Robertson--Walker background,

$$
\ddot\varphi+3H\dot\varphi
+\frac{\chi_{\rm QCD}}{F_\varphi}\sin(\varphi/F_\varphi)=0,
$$
$$
\rho_\varphi=\frac12\dot\varphi^2+V,\qquad
p_\varphi=\frac12\dot\varphi^2-V.
$$

Writing $\theta=\varphi/F_\varphi$, $N=\ln(a/a_{\rm osc})$, and a prime
for $d/dN$, the equation becomes

$$
\theta''+\left(3+\frac{d\ln H}{dN}\right)\theta'
+\frac{m_\varphi^2}{H^2}\sin\theta=0.
$$

`bi_qcd_dynamics.py` normalizes $H$ by $H_{\rm osc}=m_\varphi/3$, and
densities by $3M_{\rm Pl}^2H_{\rm osc}^2$. Let $h=H/H_{\rm osc}$,
$f_\varphi=F_\varphi/M_{\rm Pl}$, and let $R(N)$, $M(N)$ be the separately
normalized radiation and matter backgrounds. Then

$$
h^2
=\frac{R+M+3f_\varphi^2(1-\cos\theta)}
{1-f_\varphi^2\theta'^2/6},
\qquad
\frac{d\ln h}{dN}
=\frac{-4R-3M-f_\varphi^2h^2\theta'^2}{2h^2},
$$
$$
\theta''+\left(3+\frac{d\ln h}{dN}\right)\theta'
+\frac{9}{h^2}\sin\theta=0.
$$

These are homogeneous background equations. The post-handoff averaged
$a^{-3}$ continuation is justified only after the field is oscillating
rapidly with small amplitude. It does not evolve perturbations.

## 6. The un-derived AEGIS Twist hypothesis

The fitted ansatz

$$
V_{\rm Twist}(\phi)
=\Lambda^4[1-\cos((\phi-\phi_0)/F)]^3
$$

does not follow from the Kähler metric, the constant-$W$ calculation, or the
leading QCD-anomaly cosine above. Its nonnegative normalization, power $n=3$, period
$F$, field map, initial conditions, and equality-era release prescription
remain additional hypotheses. In particular, replacing the QCD $n=1$
potential with the fitted $n=3$ form requires a specified microscopic
symmetry-breaking or non-perturbative sector and a derivation of its
temperature dependence and normalization. No such derivation is claimed here.

The cube is nonnegative for positive $\Lambda^4$ without an extra constant
uplift. An independently added cosmological constant is a separate input, not
a consequence of this expression. Exact harmonic expansion gives

$$
(1-\cos x)^3=\frac52-\frac{15}{4}\cos x
 +\frac32\cos(2x)-\frac14\cos(3x).
$$

At a minimum the leading term is $x^6/8$, so the quadratic mass vanishes.
The rapid small-amplitude excitation has mean $w=1/2$ by the virial relation,
not the $w=0$ of the separate leading QCD cosine. A lower harmonic allowed by
periodicity spoils the cancellations; symmetry protection is not established.

## 7. Derived two-field equations, not a derived potential

Assume the Einstein-frame action in reduced Planck units, metric signature
$(-,+,+,+)$, minimally coupled matter/radiation (Reading B), and

$$
\mathcal L_{\rm fields}=-\frac12(\partial\chi)^2
 -\frac12 f(\chi)(\partial\theta)^2-V(\chi,\theta),
\qquad f=e^{\lambda\chi}.
$$

Here $\theta$ is the dimensional field coordinate used by `spiral_w.py`,
not the dimensionless QCD angle in section 5. Its potential uses
`cos(theta/F)`. The field-space connection is

$$
\Gamma^\chi_{\theta\theta}=-\frac{\lambda f}{2},\qquad
\Gamma^\theta_{\chi\theta}=\Gamma^\theta_{\theta\chi}=\frac{\lambda}{2}.
$$

Varying this action on homogeneous FLRW gives

$$
\ddot\chi+3H\dot\chi-\frac{\lambda f}{2}\dot\theta^2+V_{,\chi}=0,
\qquad
\ddot\theta+(3H+\lambda\dot\chi)\dot\theta+\frac{V_{,\theta}}f=0.
$$

With primes denoting $d/d\ln a$, define
$K_N=(\chi'^2+f\theta'^2)/2$ and $\epsilon=-\dot H/H^2$. Then

$$
H^2=\frac{\rho_m+\rho_r+V}{3-K_N},\qquad
\epsilon=\frac{\rho_m+\tfrac43\rho_r+H^2(\chi'^2+f\theta'^2)}{2H^2},
$$
$$
\chi''=-(3-\epsilon)\chi'+\frac{\lambda f}{2}\theta'^2-\frac{V_{,\chi}}{H^2},
\qquad
\theta''=-(3-\epsilon)\theta'-\lambda\chi'\theta'-\frac{V_{,\theta}}{fH^2}.
$$

These match the exploratory solver signs. Physical expanding solutions require
finite positive $H^2$; the solver's constraint branch additionally requires
$K_N<3$. A boundary violation is an error, not frozen evolution.
For $\rho_s=H^2K_N+V$ and $p_s=H^2K_N-V$,
$\dot\rho_s+3H(\rho_s+p_s)=0$ follows exactly from the two field equations.
`twist_potential_audit.py` checks this identity symbolically; a bounded numerical
regression checks it along one trajectory. Neither establishes all fitted
trajectories or perturbative stability.

The field-space Ricci scalar is $-\lambda^2/2$, not a kinetic ghost verdict.
The covariant potential Hessian, trajectory turning and gravitational
constraints must be included in a full stability calculation. These equations
derive dynamics **given** $V$; they do not derive the n=3 potential, its
microscopic sector, or its initial conditions. The two-field solver's n=1
cosine and the fitted effective n=3 branch remain distinct models.

## 8. Microscopic repair requirements and current result

### Separate scalar-sector perturbation diagnostic

`coupled_stability.py` derives the covariant Hessian
$V_{;IJ}=V_{,IJ}-\Gamma^K_{IJ}V_{,K}$ for the stated exponential-plus-n=1-cosine
action. In particular $V_{;\theta\theta}=V_{,\theta\theta}
+(\lambda f/2)V_{,\chi}$: the ordinary potential curvature alone is insufficient.
It constructs a metric-unit normal to an assumed moving trajectory and derives
$V_{;ss}$. The standard two-field scalar-sector entropy mass is
$m_s^2=V_{;ss}+3\omega^2+\dot\sigma^2R_{\rm fs}/2$; here the geometric term is
$-\lambda^2\dot\sigma^2/4$. Turning contributes positively to this expression.

The direction/turn rate must come from a trajectory with nonzero field speed,
not be chosen to manufacture a favorable result. At rest this basis is undefined.
Matter/radiation perturbations and gravitational constraints are not evolved.
A negative mass term can indicate growth risk, not a kinetic ghost, a full
mode-growth calculation or an exclusion. This diagnostic is not transferred
to the separate fitted n=3 model. Run
`python -m pytest theory/test_coupled_stability.py` for the exact identities.

No microscopic repair is justified by the specified inputs. A nonconstant
holomorphic superpotential, additional multiplets, or an anomalous/gauge
sector would change the theory and must be specified before calculating.
Choosing Fourier coefficients to reproduce n=3 is reconstruction of a desired
effective shape, not its prediction.

A defensible extension must supply the symmetry and charges, holomorphic
superpotential and Kähler terms, origin of harmonic amplitudes and signs,
stabilization of the dilaton and extra fields, and the scale/temperature
dependence. Integrating out heavy fields also requires a hierarchy and
control of induced kinetic and potential corrections. Only then can one test
whether the low-energy potential approximates n=3, whether the cancellations
survive corrections, and whether its cosmological initial conditions are
justified. The current QCD n=1 input is not such an extension for n=3.
The implemented effective model remains usable as phenomenology with these
limitations; the frozen likelihood comparison is not changed by this audit.

## 9. Restricted adiabatic initialization of the coupled perfect-fluid stage

This is a limiting-case derivation for `coupled_perturbations.py`, not a
primordial prescription for the fitted Twist or Spiral models. Use the same
Newtonian gauge, equal metric potentials and reduced Planck units as that
module. A prime below means d/dN; `t_m,r = theta_m,r/(aH)`.
Set matter and vacuum density to zero, radiation density strictly positive,
and the canonical scalar displacement and velocity to zero. At this extremum
the scalar force and its perturbation sources vanish; choosing
`deltaq=deltaq_prime=0` excludes scalar isocurvature. It does not establish
stability of arbitrary potential corrections.

Radiation gives `H2 = radiation_today * exp(-4N)/3` and epsilon=2.
Define `x = k*eta/sqrt(3) = k*exp(N)/sqrt(radiation_today)`,
so `x'=x` and `W=(k/(aH))^2=3*x^2`. Eliminating the density and velocity from
the two Einstein constraints and radiation conservation gives

```text
Phi'' + 3*Phi' + x^2*Phi = 0
Phi(x) = 3*Phi0*(sin(x)-x*cos(x))/x^3
Phi/Phi0 = 1 - x^2/10 + x^4/280 - x^6/15120 + O(x^8)
Phi'/Phi0 = -x^2/5 + x^4/70 - x^6/2520 + O(x^8)
```

Regularity as x tends to zero selects this solution over the singular
decaying branch; `Phi0` is the signed asymptotic Newtonian potential.
The initializer evaluates the polynomial instead of subtracting nearly equal
trigonometric terms, and obtains radiation variables from the constraints:

```text
M = Phi + Phi'
delta_r = -2*M - 2*W*Phi/3
t_r = W*M/2
```

With radiation/H2=3 these impose the independent 00 constraint and 0i metric
derivative without solving for an arbitrary density correction. The truncated
metric has evolution error beginning at O(Phi0*x^8); the constraints hold
algebraically up to floating-point rounding.

Absent-background dust variables are passive test-fluid limits, not a second
gravitating species. Integrate `t_m'=W*Phi` with no independent constant
velocity mode, and `delta_m'=-t_m+3*Phi'` with
`delta_m(0)=-3*Phi0/2`:

```text
t_m/Phi0 = 3*x^2/2 - 3*x^4/40 + x^6/560 + O(x^8)
delta_m/Phi0 = -3/2 - 21*x^2/20 + 33*x^4/1120 - x^6/2016 + O(x^8)
delta_m - 3*delta_r/4 = -3*Phi0*x^4/32 + O(Phi0*x^6)
t_m - t_r = 3*Phi0*x^4/8 + O(Phi0*x^6)
zeta = -Phi + delta_r/4 -> -3*Phi0/2
```

Thus adiabaticity means vanishing leading superhorizon relative entropy,
not forcing identical finite-k velocities or density ratios. For independent
finite-x checks the exact passive velocity is `9*Phi0*(1-sin(x)/x)` and its
integrated density is
`-3*Phi0/2 + 3*(Phi-Phi0) - 9*Phi0*I(x)`, where
`I(x)=ln(x)+EulerGamma-Ci(x)+sin(x)/x-1` and `I(0)=0`.

The API requires resolved `0 < x <= 0.01` and finite nonzero
`abs(Phi0) <= 1e-3`. The latter is a conservative implementation bound for a
linear test mode, not a cosmological spectrum measurement or full linearity
criterion for subsequent evolution. Mixed-fluid, displaced/rolling-scalar,
nonzero-vacuum and subhorizon starts are explicitly unsupported, not silently
approximated by radiation domination.

Regressions check signed amplitudes, both constraints, entropy/velocity
scaling, all seven equations, exact radiation and passive-dust evolution
through horizon entry with both integrators, and agreement from two early
start epochs. They do not validate nonzero-matter backreaction, rolling
scalar adiabatic modes, photons/neutrinos, anisotropic stress or primordial
power-spectrum amplitude/tilt/correlations. General initialization,
full-stability and scientific-baseline readiness remain unestablished.

## 10. Radiation/dust adiabatic series with a resting scalar

`mixed_adiabatic_initial_state` retains a zero-vacuum scalar at field=0 but
allows nonzero dust density and backreaction. Define
`y=matter_today*a/radiation_today`, `x=k*a/sqrt(radiation_today)`,
`W=3*x^2/(1+y)` and `epsilon=(4+3*y)/(2*(1+y))`.
The x here is a radiation-normalized wavelength parameter; it is **not**
`k*eta/sqrt(3)` in the mixed background.
Set `u_m=t_m/W`, `u_r=t_r/W` so the regular velocities have finite limits.
Since `W'/W=2*epsilon-2`, the five fluid/metric equations become

```text
P = (3*y*u_m + 4*u_r)/(2*(1+y)) - Phi
delta_m' = -W*u_m + 3*P
u_m' = -epsilon*u_m + Phi
delta_r' = -4*W*u_r/3 + 4*P
u_r' = (1-epsilon)*u_r + delta_r/4 + Phi
Phi' = P
```

Let `s=a/a_initial`, `y=y_initial*s`, `x=x_initial*s`, and
`Z=(delta_m,u_m,delta_r,u_r,Phi)`. Expand `s*dZ/ds=A(s)*Z` using
`1/(1+y_initial*s)=sum_n (-y_initial)^n*s^n`. For the regular adiabatic
mode, `Z_0=Phi0*(-3/2,1/2,-2,1/2,1)`; the scalar perturbation is zero.
This fixes the leading entropy mode and radiation-era normalization, not
a stochastic primordial spectrum. The recurrence is

```text
(n*I-A_0)*Z_n = sum_{j=1..n} A_j*Z_(n-j)
```

The evolution matrix has a positive-power constraint-violating mode:
`I-A_0` has rank four, so regularity alone does not determine `Z_1`.
Use the independent 00 constraint, multiplied by (1+y), to fix it:

```text
3*x_initial^2*s^2*Phi
  + (9/2)*y_initial*s*u_m + 6*u_r
  + (3/2)*y_initial*s*delta_m + (3/2)*delta_r = 0
```

At order one, replace the dependent radiation-continuity row of the
recurrence by this constraint coefficient. Orders two through eight use
the nonsingular evolution recurrence. Evaluate the polynomial at s=1 and
restore `t_m,r=W*u_m,r`. This derives the mode coefficients; no later
density projection or silently added isocurvature is used. Truncation begins
at ninth order in the initial scale-factor expansion, not ninth order in
arbitrary late-time x or y. The implementation requires resolved
`0 <= y_initial <= 0.01`, `0 < x_initial <= 0.01` and the same finite
signed amplitude bound as section 9. These are conservative local series
domain choices, not a rigorous interval error bound. Subsequent integration
may cross equality and horizon entry.

An independent long-wavelength check uses conserved
`zeta=-3*Phi0/2` and the background expansion alone. Neglecting finite-k
corrections, the regular growing potential obeys

```text
Phi(a) = (3*Phi0/2) * [1 - H(a)/a * integral_0^a da_tilde/H(a_tilde)]
       = (3*Phi0/2) * [1 - sqrt(1+y) * integral_0^1 t^2/sqrt(1+y*t) dt]
delta_m = 3*(Phi - 3*Phi0/2)
delta_r = 4*(Phi - 3*Phi0/2)
u_m = u_r = 3*Phi0/2 - Phi
Phi/Phi0 = 1 - y/16 + 7*y^2/160 + O(y^3)
```

The quadrature approaches Phi/Phi0=1 in radiation domination and 9/10
in matter domination. Both integrators are compared with this independent
superhorizon solution from y=0.005 through y=100 at finite, very small k.
Further tests compare all seven initial-series derivatives with the original
equations, check the independent density constraint and entropy/velocity
limits, recover the separate pure-radiation series, and evolve two distinct
early starts through equality and horizon entry.
These are perfect-fluid/resting-scalar checks, not rolling-field adiabatic
initialization, a photon/neutrino hierarchy, an observable transfer pipeline,
or independent Boltzmann validation. General readiness flags stay false.

## 11. Primordial amplitude, pivot, tilt and unit conventions

`primordial_conventions.py` is bookkeeping for section 9/10 modes, not a
measured spectrum. For a statistically homogeneous adiabatic scalar field,
`<zeta_k zeta*_k'> = (2 pi)^3 delta^3(k-k') P(k)` and
`Delta2(k)=k^3 P(k)/(2 pi^2)`, so `<zeta^2>=integral Delta2 d ln k`.
A power law is `Delta2_zeta=A*(k/k_pivot)^(n-1)`; A is dimensionless and
the pivot is a comoving k in the same unit as k. The reduced-unit module
measures comoving k (a_today=1) in H_ref, hence
`k/H_ref = k[1/Mpc]*c/H_ref[km/s/Mpc]` with exact `c=299792.458 km/s`.
H_ref is whatever reference rate defines the `M_Pl^2 H_ref^2` densities of the
baseline; it is a required input.

Sections 9-10 give `zeta=-Phi+delta_r/4 -> -3*Phi0/2` for the regular mode,
so `Phi0=-2*zeta/3` and `Delta2_Phi0=(4/9)*Delta2_zeta`; the sign flips under the
opposite zeta convention but powers do not. The variance of the power law over
`[k1,k2]` is `A (k1/k_p)^e expm1(e ln(k2/k1))/e` with `e=n-1`, and
`A ln(k2/k1)` at `e=0`. Scalar isocurvature is zero by construction
(deltaq=0), so adiabatic/isocurvature cross-correlation is absent, and
`Phi0` and `zeta` are perfectly anticorrelated. Running, tensors, non-Gaussianity,
the transfer from primordial to later epochs, and any amplitude, pivot or tilt
value are **not** supplied. Tests use synthetic values, compare the variance
with independent quadrature, check pivot/tilt scaling, unit arithmetic, input
rejection, and that the mixed initializer reproduces the requested conserved
zeta to O(x^2). No observational evidence or readiness flag follows.

## 12. Displaced/rolling subdominant canonical scalar (first order in f)

`subdominant_field_adiabatic_initial_state` supports a displaced or rolling
field, and nonzero `vacuum`, only when the scalar budget
`f=(V+H2*field_prime^2/2)/(3*H2)` at the initial epoch is `<=1e-6` (caller
may tighten it). The fluid variables are the section 10 resting-scalar
series, with errors O(f) in the delta amplitudes. At k->0 the 0i equation
gives `Phi'+Phi=-eps*s` and, with `s=delta_r/4`, `delta_m=3s`,
`u_m=u_r=-s` (theta/(aH)=wave2*u), `deltaq=-field_prime*s`, the 00 equation
reduces identically (using `eps=(m+4r/3+field_prime^2)/2` and the field
equation) for any s. An earlier residual `3*f*Phi0` was an implementation
defect: the series velocities carry `1/H` built with the fluid-only `H2`, so
they are now rescaled by `H2_true/H2_fluid`, and `Phi'` includes the scalar
momentum `field_prime*deltaq/2`. The 00 residual is now O(f*x^2*Phi0)
(measured ~2e-6 f*Phi0 at x~1e-3), *verified* (not projected away) by
`integrate`'s 1e-10 gate; Phi0=1e-3 now passes at f=1.7e-7. The amplitude s
(regular-versus-decaying-mode choice) still comes from the fluid series, so an
O(f) decaying-mode admixture is not excluded; excluding it needs the pre-onset
field history (Weinberg's integral), which is not derived. The scalar follows the common adiabatic time shift
`dN=-delta_r/4` (same as `delta_m=3*delta_r/4`): `deltaq=field_prime*dN`,
`deltaq'=field_prime'*dN+field_prime*dN'` with
`field_prime'=-(3-epsilon)field_prime-V'/H2` and
`dN'=-delta_r'/4` from the radiation equation. For field=0, no kinetic
energy and zero vacuum it equals the mixed series exactly. Tests check that
limit, the O(f) constraint scaling, x^2-scaled entropy leakage
`deltaq+field_prime*delta_r/4` after evolution (and that a wrong `deltaq'`
leaks far more), the numerical gate, rejection of f above bound, and start-epoch
independence: re-initializing from the evolved background at N=-15 instead of
-16 changes the trajectory by <1e-4 (relative to each component's maximum),
with the error growing as x^2 (k=300 versus 100 gives a ratio 5-15). This is a
consistency check of the O(x^2) series truncation, not proof the decaying mode
is absent.
Not covered: scalar-dominated or non-radiation epochs, the O(f) regular-mode
selection of Phi0, and any microscopic origin of the potential; general readiness flags
remain false.

## 13. Gauge/source/initial-condition contract with free-streaming neutrinos

`neutrino_contract.py` records only the leading superhorizon radiation-era
mode (calH=1/tau, `Rnu=rho_nu/(rho_gamma+rho_nu)` in `[0,1)`, `k*tau<=.01`)
in conformal Newtonian gauge with potentials `psi` (time-time) and `phi`
(spatial), and shear convention `(rho+P)sigma` as in the module docstring.
The traceless equation `k^2(phi-psi)=(3/2)a^2 sum(rho+P)sigma` with
`a^2 rho_nu=3 Rnu/tau^2` makes `phi != psi`. At leading order
`delta_gamma=delta_nu=-2 psi`, `delta_m=3 delta_r/4`, `theta=k^2 tau psi/2`
(the 0i equation; `theta_nu-theta_gamma` is O(k^4 tau^3)), and
`sigma_nu=k^2 tau^2 psi/15` from `sigma'=(4/15) theta_nu`. Substituting into
the traceless equation gives `phi=(1+2 Rnu/5) psi`, i.e. the standard
`psi=20C/(15+4Rnu)` normalisation. Tests check the traceless, 0i and
`theta'`, `sigma'`, dust-velocity equations, the O(k^2 tau^2) scaling of the
00 residual, the `Rnu=0` limit against the perfect-radiation initializer and
input rejection. It is not wired into `coupled_perturbations.py` (whose
equations assume `phi=psi`), evolves nothing, supplies no hierarchy
truncation, matter-era/photon-baryon coupling or spectrum, and no readiness
flag changes. A consistent hierarchy stage is still unfinished.

## 14. Radiation-era photon-fluid + free-streaming neutrino evolution

`neutrino_hierarchy.py` (k=1, `x=k tau`, `calH=1/x`, `a^2 rho_r=3/x^2`) evolves
`delta_gamma, theta_gamma, delta_nu, theta_nu, F_2..F_lmax, phi` with
`psi=phi-3 Rnu F_2/x^2` (traceless equation, `F_2=2 sigma`):
`phi'=2 Theta/x^2-psi/x` (0i, `Theta=(1-Rnu)theta_g+Rnu theta_nu`),
`delta'=-4theta/3+4phi'`, `theta_g'=delta_g/4+psi`,
`theta_nu'=delta_nu/4-F_2/2+psi`, `F_2'=8theta_nu/15-3F_3/5`,
`F_l'=[l F_{l-1}-(l+1)F_{l+1}]/(2l+1)` and the Ma-Bertschinger closure
`F_lmax'=F_{lmax-1}-(lmax+1)F_lmax/x`. Photons have no shear and no baryons
(an idealisation); there is no dust, scalar or vacuum. The 00 equation
`x^2 phi+6 Theta/x+1.5 delta_bar=0` is not used in the evolution and is the
independent residual. The regular series was solved with sympy (overdetermined
system, consistent) through `delta, phi` at x^2, `theta` at x^3, `F_2` at x^4:
with `D=2R+25`, `delta=-2+g2 x^2`, `g2=-(112R^2+1370R+3675)/(315 D)`,
`theta_g=x/2+a3 x^3`, `a3=-5(2R+7)/(28 D)`, `theta_nu=x/2+b3 x^3`,
`b3=-(506R+2275)/(1260 D)`, `F_2=2x^2/15+c4 x^4`, `c4=-(56R+295)/(945 D)`,
`phi=(1+2R/5)+p2 x^2`, `p2=-(56R^2+580R+525)/(630 D)` (units of psi(0)).
At R=0 these equal the expansion of `3(sin y-y cos y)/y^3`, `y=x/sqrt3`, and
the evolved potential matches it to 1e-6. The leading contract of section 13
left an O(x0^2) 00 residual that grew like x and gave a ~1% potential error at
x=15; the O(x^2) series reduces the initial residual to O(x0^4) (tests check
the x0^4 scaling). Supported: `0<x0<=.01`, `Rnu in [0,1)`, `4<=lmax<=200`,
`x_final<=lmax/2` (truncation reflection), validated by lmax -> 2 lmax,
RK45 vs DOP853, start-epoch independence and derivative checks. Missing:
photon-baryon coupling/polarization, matter and scalar coupling, primordial
spectrum, transfer functions, observables and independent Boltzmann
comparison (no local compatible solver was run). Readiness flags remain false.

## 15. Radiation+CDM extension of the hierarchy stage

`matter_hierarchy.py` (k=1, `x=k tau`) adds cold dark matter. Background:
`a=A(s^2+2s)`, `s=tau/tau_1`, `A=a_eq` exactly solves `a'^2=(rho_r0+rho_m0 a)/3`
(8 pi G=1) with `rho_r0=rho_m0 A`, `4A^2/tau_1^2=rho_m0 A/3`, giving
`calH=2(1+s)/(x(2+s))`, `a^2 rho_r=12/(x^2(2+s)^2)`, `a^2 rho_m=12 e/(x(2+s))`,
`e=1/kt1`, `s=e x` (tests check Friedmann and `calH'=-a^2(rho+3P)/6`).
Added equations: `delta_c'=-theta_c+3 phi'`, `theta_c'=-calH theta_c+psi`;
`phi'=Theta_tot/2-calH psi` (0i, `Theta_tot=(4/3)a^2[(1-R)rho_r theta_g+R rho_r
theta_nu]+a^2 rho_m theta_c`), `psi=phi-R a^2 rho_r F_2` (traceless). The
independent residual is `x^2[phi+3calH(phi'+calH psi)+a^2 delta_rho/2]`.
Initial mode: power series in `x` for every variable with the exact
`a(x)`, solved with sympy (overdetermined: all evolved equations through the
order each retained coefficient fixes, 0i and 00) plus adiabatic conditions
`delta_g=delta_nu=(4/3)delta_c` at x^0 and `psi(0)=1`. It yields
`phi=(1+2R/5)+p1 x+p2 x^2+p3 x^3` with `p1=-e(16R+15)/(8(2R+15))`, etc.
(all coefficients in the module); the `e=0` terms equal section 14 and the
leading terms equal section 13. Supported: `0<x0<=.01`, `x0/kt1<=.01`, `R in
[0,1)`, `4<=lmax<=200`, `x_final<=lmax/2`. The 00 residual of the start state
scales as x0^4 for several `kt1` and R. Independent checks: for R=0, k->0 the
numerical potential matches the Kodama-Sasaki
`Phi/Phi_0=[16 sqrt(1+y)+9y^3+2y^2-8y-16]/(10y^3)`, `y=a/a_eq` (so
`Phi->0.9 Phi_0`); `zeta=-phi+delta_rho/(3(rho+P))` is conserved through
equality to O(x^2) for R>0; the spatial-trace equation
`phi''+calH(psi'+2phi')+(2calH'+calH^2)psi+(phi-psi)/3=a^2 delta P/2` holds to
1e-5; lmax, tolerance and start-epoch refinement. Not included here (see
section 16 for the baryon extension): photon hierarchy/polarization, scalar or
vacuum coupling to the hierarchy, primordial spectrum, transfer functions,
observables, independent Boltzmann comparison. Readiness flags remain false.

## 16. Baryons in the tight-coupling limit

Adds `baryon_fraction=f_b=rho_b/rho_m` (default 0, bitwise unchanged) to
`matter_hierarchy.py`. Since baryons and CDM are both `a^-3`, the section-15
background is exact for any `f_b`. Thomson scattering is taken at infinite
opacity (leading order in `k/kappa'`): `theta_b=theta_gamma`, `delta_b=(3/4)
delta_gamma` (preserved by the continuity equations), photon shear dropped, and
with `Rb=3rho_b/(4rho_gamma)=b e x(2+e x)`, `b=3f_b/(4(1-R_nu))`, `e=1/kt1`:
`(1+Rb)theta'=-Rb calH theta+delta_gamma/4+(1+Rb)psi`, with baryon momentum in
the 0i source and `(3/4)f_b delta_gamma` in the 00 source. A sympy series solve
of all evolved equations plus the 0i and 00 constraints, order by order, shows
baryons change only `theta_gamma,4 += e b (4R+15)/180` through the retained
orders; every other coefficient is `f_b`-independent. Supported domain:
`f_b in [0,1)` and the section-15 limits. This is not a statement about
validity at finite opacity: no opacity, ionization or recombination history is
included, so the evolved range is not physically bounded by `k/kappa'` here
and results must not be read as photon-baryon acoustic physics. Checks: the 00
residual still scales as x0^4; deliberately dropping the new term degrades
start-epoch agreement >5x; the independent spatial-trace equation and
`zeta` conservation hold with `f_b>0`. Still missing: finite-opacity coupling,
ionization history, photon hierarchy/polarization, scalar/vacuum coupling,
spectra, transfer functions, observables, independent Boltzmann comparison
(none matched locally). Readiness flags remain false.

## Reproducibility

- Symbolic Kähler metric and kinetic-coupling check:
  `python -m pytest theory/test_bi_supergravity.py -q`
- Constant-superpotential extrema and sign checks: the same test module.
- QCD scale and homogeneous-field equations:
  `python -m pytest theory/test_bi_qcd_axion.py theory/test_bi_qcd_dynamics.py -q`
- Machine-readable background output: `theory/bi_qcd_dynamics.json`.
- Exact one/two-field identities and numerical regressions:
  `python -m pytest theory/test_twist_potential_audit.py theory/test_spiral_numerics.py -q`.
- Coupled perfect-fluid equations and restricted adiabatic initial modes:
  `python -m pytest theory/test_coupled_perturbations.py -q`.
