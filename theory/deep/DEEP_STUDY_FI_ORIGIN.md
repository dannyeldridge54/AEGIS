# Deep study D436 — a D-term origin for the Twist's capture coupling (14 Nov 2026, 19:00 CT). AI-assisted.

**Question.** Twist-2 needs states χ that become light exactly when the rolling modulus crosses x_E (capture, D396) and a potential that
holds it there (pinning, D407/D422). D388 showed a superpotential coupling λ(T − T_E)χχ̄ cannot come from IIB (shift symmetry allows T in W
only as e^(−aT)) and only globally from IIA fluxes. Is there another origin?

## 1. The mechanism (literature + symbolic check)

On magnetised D7-branes the Fayet–Iliopoulos parameter of the brane U(1) is linear in the 2-cycle volumes,
ξ_a = (1/𝒱) Σ_i M_{a,i} t^i, with M_{a,i} = ∫ c₁(L_a) ∧ [D_a] ∧ ω_i integers set by the worldvolume flux (Cicoli/Blumenhagen-type IIB
orientifolds; arXiv:0711.3389 eqs. 3.3, 3.14). The D-term potential is V_D = (g²/2)(Σ Q|φ|² − ξ)². Two facts matter:
- ξ is a function of Re T (volumes), not of W, so the axionic shift symmetry that killed the superpotential route (D388) is not an obstacle.
- Charged fields have m_φ² = −g² Q ξ at φ = 0: they are massless exactly where ξ = 0, a hyperplane of Kähler moduli space set by flux integers.

Symbolic check (theory/deep/fi_origin_check.py; K = −ln(T₁+T̄₁) − 2 ln(T₂+T̄₂), GS shifts δ₁, δ₂ on Im T₁, Im T₂):
ξ = δ₁/(2x₁) + δ₂/x₂, zero at **x_E = −(δ₁/2δ₂) x₂** (δ₁, δ₂ of opposite sign), and near it m_φ² ≈ −g²Q (dξ/dx₁)(x₁ − x_E) with
dξ/dx₁|_E = −2δ₂²/(δ₁x₂²): **linear in (x₁ − x_E)** — the D-term analogue of λ(T − T_E). So the capture point is a ratio of flux charges
times a second (fixed) modulus: quantised, like the IIA flux idea of D388, but now local to the brane sector.

## 2. How it would work in the Twist (estimates, δ₂ = 0.01, x₂ = 30, so δ₁ = −0.0197 for x_E = 29.6; computed)
- Far from x_E (ξ ≠ 0), the field of the right charge condenses, |φ|² = ξ/Q, so V_D = 0: the Twist rolls freely along a D-flat valley.
- At x_E all charged states and the U(1) gauge boson become light: exactly the enhanced-symmetry point the thermal trap (D396) needs.
- Past x_E, if no field of the opposite charge exists, V_D = g²ξ²/2 is a steep wall: the Twist cannot overshoot.
- SUSY-breaking soft masses add V ≈ m_soft²|φ|² = m_soft² ξ/Q, a gentle slope toward ξ = 0. Wall + slope pin x at x_E without a separate
  condensate scale. The energy released between the pin and the free-roll limit (29.6 → 29.83) is ~10⁻⁷–10⁻⁵ of the radiation at capture
  (m_soft = 10⁴–10⁵ GeV): no moduli problem, no dilution.
- The anomalous U(1) gauge boson eats the axion (Stückelberg) and is heavy (~M_s) away from x_E; that gauge strength is what makes the
  decay of x fast (D407).

## 3. The obstacle (serious, and it is the same place the earlier control flag pointed to)
ξ ∝ δ₁/(2x₁) grows as x₁ → 0. At the CMB point (x ≈ 1.3×10⁻⁴) ξ ≈ −76 M_P², and even at the end of inflation (x ≈ 9×10⁻³) ξ ≈ −1.1 M_P².
If unscreened, V_D ≈ 10³ M_P⁴, thirteen orders above the inflationary energy (~10⁻¹⁰ M_P⁴). Screening needs a condensate |φ|² ~ 10² M_P²,
i.e. trans-Planckian field values, outside the effective theory. So the D-term origin works near capture (x ~ 30) but is incompatible with
the Twist's inflation at x ≪ 1 unless the magnetised brane sector does not exist there (e.g. the brane is only BPS / only wrapped in part of
moduli space, or the x ≪ 1 region has a different description altogether). This matches D408/D409/D423: the small-x region is outside
geometric control in any case.

## 4. Verdict
A concrete, literature-grounded candidate for the origin of (T − T_E): a moduli-dependent Fayet–Iliopoulos term from worldvolume flux on a
magnetised D7-brane. It explains why the capture point exists and is quantised, why states are light there, why the field is pinned (soft
terms + D-term wall), and why the decay is at gauge strength. It does NOT yet fit the inflationary phase: the same FI term is enormous at
small volume. Status: OPEN → "candidate origin found, conditional on the small-x region being described differently". Next step (needs a
lock): a two-modulus toy model with the D7 sector present only for x ≳ 1, checking the roll from the end of inflation to capture.

## 5. Step 2 result (D437, locked toy)
Starting from the real Twist trajectory, the FI mechanism alone captures the field: it hits the D-term wall at x_E at T ≈ 1.5×10¹¹ GeV,
bounces back by Δx ≈ 0.1–0.2, and the soft-mass slope returns it to the wall by T ≈ 2×10¹⁰–6×10¹⁰ GeV, where it settles. No separate condensate
scale or thermal trap is needed. The open problem is now isolated to the small-x region (inflation and the first ~2.5 e-folds after it).

## 6. Step 3 result (D438, locked toy): the small-volume obstacle disappears in the stringy treatment
The supergravity FI formula ξ ∝ (1/𝒱)∫J∧F is only the large-volume limit of the grade difference of the brane bound state's constituents
(Π-stability; Douglas–Fiol–Römelsberger, hep-th/0002037). Grades are phases, so the FI term stays bounded. In a T²×T² toy with fluxes
(10, 400) and a capture root at x_E = 29.6, |ζ| ≤ 0.37 M_s² for every x below x_E (−0.373 at the CMB point), against −76 M_P² from the naive
extrapolation; screening needs only a sub-string-scale condensate, nearly constant during inflation. The mechanism therefore survives from
inflation to capture at toy level. Remaining: α′/instanton corrections at x ≲ 1, the brane gauge coupling at small volume, and a real
Calabi–Yau embedding.
