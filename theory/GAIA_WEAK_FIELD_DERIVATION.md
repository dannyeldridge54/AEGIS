# Conditional weak-field scalar coupling for a Gaia comparison

## Result and scope

The Jordan-frame BI conformal map gives a definite *conditional* weak-field
scalar coupling. Under a linear, unscreened point-source approximation, that
coupling gives a Yukawa fifth-force response. The repository does **not** yet
derive a local scalar profile, a stellar/Galactic effective mass, screening, or
a Gaia-observable orbit residual. This is therefore a theory-side derivation
and bound, not a completed Star Mapper theory overlay or a test of AEGIS.

## Conformal factor and coupling

Use the reduced-Planck-normalized canonical field from
`DERIVATION_CHAIN.md`,

\[
\phi/M_{\rm Pl}=-\exp\!\left(\sqrt{2/3}\,\chi/M_{\rm Pl}\right),
\qquad \Omega=2(\phi/M_{\rm Pl})e^{2\phi/M_{\rm Pl}}.
\]

With the registered Reading-A matter metric
\(g_J=A(\chi)^2g_E\), \(A^2=-3/\Omega\). Let
\(x=\sqrt{2/3}\,\chi/M_{\rm Pl}\). Then

\[
\ln A=\tfrac12\ln(3/2)+e^x-\tfrac{x}{2},
\qquad
\alpha_{\rm DEF}\equiv\sqrt{2}\,M_{\rm Pl}\frac{d\ln A}{d\chi}
=\frac{2e^x-1}{\sqrt3}.
\]

The general-relativistic point is
\(x_{\rm GR}=-\ln2\), or
\(\chi_{\rm GR}/M_{\rm Pl}=-\sqrt{3/2}\ln2=-0.84892845\). At that point,
\(d^2\ln A/d(\chi/M_{\rm Pl})^2=1/3>0\) and
\(d\alpha_{\rm DEF}/d(\chi/M_{\rm Pl})=\sqrt2/3=0.47140452\), agreeing with
the existing `solar_lowz.py` calculation.

## Conditional local force

For a canonical scalar with conformal matter coupling, linearized about a
constant local background and sourced by an unscreened point mass, the static
field has a Yukawa profile. The ratio of scalar to tensor acceleration is

\[
\frac{|a_\chi(r)|}{|a_T(r)|}
=\alpha_{\rm DEF,0}^2(1+m_{\rm eff}r)e^{-m_{\rm eff}r}.
\]

Here \(m_{\rm eff}\) is the local effective scalar mass and \(r\) is physical
distance. The massless/long-range limit is \(\alpha_{\rm DEF,0}^2\). This
formula assumes universal unscreened coupling at source and test body; it does
not calculate \(m_{\rm eff}\) or establish that a star or the Galaxy meets
those assumptions.

The preregistered massless PPN relation is
\(|\gamma-1|=2\alpha^2/(1+\alpha^2)\). With the Cassini limit
\(2.3\times10^{-5}\), it implies
\(\alpha_{\rm DEF}<0.0033912\) and hence a conditional long-range force
fraction below \(1.15\times10^{-5}\). Linearizing the existing coupling around
the GR point gives \(|\Delta\chi|/M_{\rm Pl}<0.00719\), consistent with the
saved solar-system gate. For a finite range, the Yukawa factor suppresses this
force further.

## Consequences for Star Mapper

- **Reading B:** direct matter coupling and direct scalar-force correction are
  zero by assumption. An identical Gaia/overlay result is a null/pipeline
  check, not independent predictive agreement.
- **Reading A:** the weak-field coupling is nonzero away from the GR point, but
  the Cassini gate confines the long-range local coupling near that point.
  The current cosmological background fits do not provide the local Galactic
  boundary-value solution or effective mass needed to predict a source-by-
  source correction.
- Current Star Mapper records retain Gaia positions, proper motions and some
  radial velocities, but not the full astrometric covariance needed for an
  orbit-residual likelihood. Many records also lack radial velocity. A
  defensible comparison additionally needs a specified Galactic potential,
  selection/control model, covariance propagation, and an independently
  validated local-field solution.

Accordingly, do not modify Gaia measurements, reclassify anomaly flags, or
attribute them to torsion using this result. A future theory-enabled mapper
can display the conditional coupling envelope separately, but a predictive
stellar overlay must wait for the missing local solution and data model.

## Reproducibility

Run `python -m pytest theory/test_stellar_weak_field.py
theory/test_bi_supergravity.py -q` from the repository root. The symbolic
coupling, GR point, Cassini inversion, linearized band, and Yukawa limiting
behavior are covered. These internal checks do not validate the astrophysical
assumptions or a stellar-scale AEGIS prediction.
