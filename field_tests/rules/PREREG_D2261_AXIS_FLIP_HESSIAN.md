# PREREG D2261 — Axis-angle flips: what the mirror geometry forces at rho and i (locked 27 Nov 2026)

**Question (Danny, 27 Nov).** Think out the geometry and the reverse-flipping effect at the axis angles.
**Frame.** The half fundamental domain is the (2,3,inf) reflection triangle: mirrors meet at angle pi/2 at i and pi/3 at rho.
Local coordinate u = (tau - tau0)/(tau - conj tau0) (Feruglio 2302.11580). The residual flip acts as u -> -u at i, u -> omega^2 u at rho;
CP (tau -> -conj tau) is a mirror through both points.
**Hypotheses (from symmetry alone, before computing).**
- H1 (forced): at rho, E_xy = 0 and y^2 E_xx = y^2 E_yy = s(s-1) E / 2. (An order-3 rotation leaves only multiples of the identity invariant.)
  Predicts the D2259 isotropy numbers 1 (s=2) and 3/8 (s=3/2) are forced by the geometry, not accidental.
- H2 (forced): at i, grad E = 0 and E_xy = 0; trace y^2(E_xx+E_yy) = s(s-1) E.
- H3 (NOT forced, measured only): at i, the anisotropy A = E_xx/E_yy. u -> -u leaves every quadratic form invariant, so A need not be 1.
  The leading anisotropic term is Re(u^2) at i and Re(u^3) at rho.
**Method.** E(tau,s) via tools/serapis_calc/eisenstein.E_fourier (mpmath, dps 30, nmax 30), derivatives by mp.diff; independent check by
central finite differences on tools/serapis_calc/shapes.E (scipy). s in {2, 3/2}. Run once.
**Pass.** H1 and H2: relative residual < 1e-8 (mpmath) and < 1e-5 (finite-difference check). H3: reported with both methods agreeing to 1e-5.
**Output.** field_tests/results/d2261_axis_flip.json.
