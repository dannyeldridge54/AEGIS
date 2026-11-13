DEVELOPMENTS 72–75: the four weak spots (13 Nov 2026). AI-assisted. Insert into the matter doc after D71.
Scripts: theory/inflation/s_stability.py; numbers in field_tests/results/s_stability.txt and weak_spots_D72.txt.

## Development 72 — the helper field S is unstable as written; a standard term fixes it

What we checked. W = √3 m S F(T) uses a second field S that must sit at S = 0 during inflation. We computed the
full two-field supergravity potential numerically and the mass of S (both directions) along the plateau.

Result. With K = −3 ln(T + T̄ − SS̄) exactly as written, S is tachyonic: m_S²/H² ≈ −1.9 to −2.0 at the CMB point
(x = 10⁻⁴ to 10⁻³) and −1.4 at x = 3×10⁻³. S would roll away and inflation would not follow our single-field
path. This is the known problem of the simplest no-scale Cecotti/Starobinsky models (Kallosh–Linde, Ellis–Nanopoulos–
Olive): it needs a stabilising term.

Fix (taken). Add the standard quartic term inside the log: K = −3 ln(T + T̄ − SS̄ + ζ(SS̄)²). At S = 0 it changes
nothing (K, K_SS̄ and V are unchanged there, so every inflation number stands). It makes S heavy:
ζ = 10³: −1.2 at x = 10⁻⁴ (still unstable at the CMB point); ζ = 10⁴: m_S²/H² = +6 to +240; ζ = 10⁵: +78 and up.
So ζ ≳ 10⁴ (Λ ≲ 10⁻² M_P, a mass scale for the physics that generates it) makes S heavy (m_S ≫ H) all through the
plateau. Label: chosen (a standard ingredient, value not derived).

Other options recorded. (b) S outside the log, K = −3 ln(T + T̄) + |S|² − ζ|S|⁴: also standard, but changes the
plateau's prefactor, so the inflation numbers would need redoing. (c) Nilpotent S (S² = 0, from a D3-brane):
removes S's scalar altogether; clean, ties to string constructions. We keep (a) because it leaves every computed
number unchanged.

Check with 40-digit arithmetic (s_stability_mp.py, analytic Kähler derivatives) confirms the plateau numbers and
gives a simple rule: on the plateau m_S²/H² ≈ −2 + 8ζx. So S is stable at the CMB point (x* ≈ 1.1×10⁻⁴) for
ζ > ~2300 and heavy (m_S > 3H) for ζ ≳ 1.4×10⁴; earlier in inflation (smaller x) needs proportionally larger ζ.
Cliff and tail: S is stable there even with ζ = 0 (m_S²/H² = +4 at x = 0.01, +430 at 0.1, +4000 at 1, +75 at
30), and ζ only adds 8ζx. So the stabilising term is needed only on the plateau, and the tail is safe.
Is ζ ≈ 10⁴ natural? ζ = 1/Λ² with Λ ≈ 10⁻² M_P ≈ 2×10¹⁶ GeV, the grand-unification scale: it is what heavy
fields of GUT mass leave behind when integrated out (Kallosh–Linde 2013), so no special tuning. Label: chosen, natural.
(A first attempt with smaller finite-difference steps in double precision gave noisy numbers; discarded.)

## Development 73 — fifth force on ordinary matter: the Standard Model must not feel Re T

What we checked. The tail field today is very light (mass ~ H₀), so if ordinary matter's mass depends on x it
makes a long-range fifth force. Cassini allows a universal coupling |β_m| < 3.4×10⁻³.

Result. If ordinary matter sat in the bulk with natural modular weights, β_m = 0.41 (weight 1) or 1.22 (e^{K/2}):
excluded by ×120–360. So the Standard Model must be sequestered: on D3 branes, whose gauge couplings do not depend
on T. Then the proton mass (≈99% from QCD) is T-independent. What remains: the Higgs-generated ~1% (quark and
electron masses) could still depend on x through the Higgs's Kähler weight. With weight 1 that gives β_m ≈ 4×10⁻³,
just above Cassini (×1.2), and composition-dependent forces (equivalence principle) far above MICROSCOPE.

Route (taken). Sequestered Standard Model with a T-independent Higgs sector (sequestering, as in KKLT-type D3
setups, is the usual assumption). Label: assumption. This is the same requirement every runaway-modulus quintessence
model faces; it is not solved here, only stated sharply. Falsifier unchanged: any confirmed fifth force or EP signal.

## Development 74 — the dark-energy size is chosen, not predicted

Dark energy today needs e^{−2n}m²/4 = ρ_DE, i.e. n = 126.8 (e^{−254}). n was set to match; the theory does not
compute it. This is the cosmological-constant problem restated, not solved. Label changed from "sets" to "chosen
(fitted to ρ_DE)" in REVIEW_GUIDE. What the theory does predict is the shape (w₀ ≈ −0.90, w_a ∈ [−0.15, 0]) once
the size is fixed.

## Development 75 — the field travels about 15 Planck lengths

From the CMB point (x ≈ 1.1×10⁻⁴) to today (x ≈ 30–300) the canonical field moves Δφ ≈ 15–18 M_P. The swampland
distance conjecture says towers of states get light as e^{−λΔφ}, λ ~ O(1), which would spoil the effective theory
far before 15 M_P. Every α-attractor + quintessence-from-one-field model (and most large-excursion models) has the
same issue. Label: open, generic. Note that inflation itself only spans ~5 M_P; the rest is the post-inflation
roll to the tail.

## Development 76 — the twist angle y: heavy during inflation, unstable in the middle of the tail

Scripts: theory/inflation/plateau_checks.py, angle_valley.py; results/plateau_checks.txt, angle_valley.txt.

What we checked. With S = 0 the landscape is V(x, y) = m²|F(x + iy)|²/(4x²). We computed the mass of the angle y
(canonical, with the same weight 3/(4x²) as x) along the whole path.

Plateau. m_y² = 4H² from x = 10⁻⁵ to 10⁻², so y is heavy all through inflation: it stays at y = 0, leaves no
isocurvature of its own and does not bend the path. Good.

After the cliff. Along y = 0 the landscape is a ridge, not a valley: m_y²/H² ≈ 2 − 8n x²/(x+1)³ (H² = V/3), i.e.
−3.5 at x = 0.1, −121 at x = 1, −28 at x = 30, crossing zero at x ≈ 500 (= 4n) and +1.7 at x = 3000. The cause is
the factor e^{−nT/(T+1)}: its size falls when T gets an imaginary part. The true valley lies at large y (y ≈ 23 at
x = 0.1, ≈ 120 at x = 30), hundreds of Planck lengths away in canonical distance, so the field cannot reach it;
the question is only whether small y grows.

Why it is probably harmless, and the condition. (1) Between the cliff and today the universe is dominated by
radiation and matter, whose H is far larger than the tail's own √(V/3), so y is frozen by Hubble friction exactly as x
is. (2) Today the tail dominates, so what matters is x today. The tail has the slope √(2/3) that PURE-TWIST assumes
only for x ≳ 3000 (slope 1.08×√(2/3) at 3000, 1.25× at 1000, 8.8× at 30). In that same range y is stable
(m_y² ≈ +1.7H²). So the assumption the late-time fits already make (tail on its √(2/3) slope) also makes y stable.
Condition recorded: x today ≳ 3000 (equivalently: the kination after the cliff carries x that far). Not yet shown
from the dynamics. Open too: the hidden-axion kick gives y a velocity at the cliff, where y is tachyonic; a two-field
run of the cliff with the full V(x, y) should check how far y moves (it would need to move ~20 in T units to fall into
the valley, which looks impossible, but it is not computed).

Correction to D75: with x today ≳ 3000 the field distance from the CMB point is about 21 M_P (not 15–18).

## Development 77 — loop corrections from the reheating field: χ must be supersymmetric

What we checked. χ couples as g²(φ − φ₀)²χ²/2 with g ≈ 0.1. On the plateau the CMB point is 5.1 M_P from the end of
inflation, so χ is very heavy there (M = g|φ − φ₀| ≈ 0.5 M_P) and its quantum (Coleman–Weinberg) energy is huge.

Result. Without supersymmetry: ΔV/V ≈ 2×10⁷ — the plateau is destroyed; keeping the n_s shift below 0.001 would need
g < 2×10⁻⁴, far too small for preheating. With χ in a chiral multiplet the boson and fermion pieces cancel and only
the Hubble-size mass splitting is left: ΔV/V ≈ 1%, Δη ≈ +0.001, so n_s moves up by about +0.002 (order-of-magnitude:
the coefficient depends on how χ couples in supergravity). Route (taken): χ is a chiral superfield coupled through the
superpotential, as standard in supergravity preheating. Consequence: n_s ≈ 0.964 may sit nearer 0.966 — still far
from 0.974. Label: estimate; a full one-loop supergravity calculation is open.

## Development 78 — correction: the slope the field sees today is steeper than √(2/3) at the derived heat share

Script: theory/darkenergy/tail_slope_full.py; results/tail_slope_full.txt.

What we found. Backlog L (tail_freeze.py) located where the field freezes after the cliff, x_f, but took today's slope
as c·x/(x + μ), keeping only the μ factor. The full tail also keeps a leftover of the cliff,
−d ln V/dφ = c·x·[2n·m2/(x + m2)² + 1/(x + μ)], and that leftover is not small unless x_f ≫ 2n ≈ 250.
Results (μ = 1, n = 125, m2 = 1; thawing field, exponential approximation, CPL fit):
  - heat share 0.04%: x_f ≈ 1160, slope 1.21 × √(2/3) = 0.99; w₀ ≈ −0.85, w_a ≈ −0.22; angle stable (+1.1 H²)
  - heat share 0.13% (the computed central value): x_f ≈ 360, slope 1.69 × √(2/3) = 1.38; w₀ ≈ −0.69, w_a ≈ −0.42;
    angle slightly unstable (−0.8 H²)
  - heat share 0.4%: x_f ≈ 120, slope 2.5: too steep to be today's dark energy.
Reference, slope √(2/3) exactly (PURE-TWIST): w₀ −0.90, w_a −0.15.

What it means.
  1. PURE-TWIST (κ = √(2/3)) is the limit x_f ≫ 250, which needs a heat share ≲ 0.01%. At the computed heat share the
     full model is steeper. The locked PURE-TWIST results stand as tests of that tail; but calling PURE-TWIST "the
     theory's own prediction" now needs this condition. REVIEW_GUIDE updated.
  2. The tail's slope is tied to reheating: more heat → the field stops earlier → steeper slope today. This links the
     matter and dark-energy sectors through one number; it is a prediction once f is pinned down.
  3. At the central heat share the predicted w_a ≈ −0.42 sits just past the locked ceiling (w_a ≥ −0.40,
     PREREG_WA_CEILING) — not a new test (the ceiling was locked for the √(2/3) tail), but noted.
  4. The exponential approximation overstates steepness slightly (the slope falls as the field moves on); a
     full-potential late-time run is the next check.
  5. Observation, not a claim: at f ≈ 0.04% the slope is ≈ 1, the value FLAG-1 uses. FLAG-1 was fitted, so this is a
     coincidence until tested on new data.

Options to recover √(2/3) without a tiny heat share (each a new model version; would need its own locked tests):
  (a) a cliff factor that saturates faster, e.g. exp(−n T²/(T² + m2²)) or exp(−n(1 − e^{−T/m2})): leftover slope falls
      like 1/x² or e^{−x} instead of 1/x;
  (b) lower heat share (smaller g): moves the matter yield too;
  (c) accept the steeper tail and test it — the honest default.
We take (c) for now: no model change, the condition is recorded, and the late-time fits are not rerun.

Correction to D76: at the central heat share x today ≈ 360, so the angle is mildly unstable today (m_y² ≈ −0.8H²,
|m_y| < H: slow growth from a tiny start; probably harmless, not computed). Correction to D75: field distance ≈ 19 M_P.

## Development 78b — the full tail shape softens it: one curve of (w₀, w_a) set by the heat share

Script: theory/darkenergy/tail_full_thaw.py; results/tail_full_thaw.txt. Same as D78 but the field thaws on the
full tail shape (its slope eases as it moves), not a fixed exponential.

  heat share 0.01%: w₀ −0.89, w_a −0.16 (≈ PURE-TWIST)
  heat share 0.04%: w₀ −0.86, w_a −0.20
  heat share 0.08%: w₀ −0.81, w_a −0.27
  heat share 0.13% (computed): w₀ −0.74, w_a −0.34; field today at x ≈ 520, where the angle is just stable (D76)
  heat share 0.20%: w₀ −0.64, w_a −0.44
  heat share 0.40%: w₀ −0.40 — far too stiff.

So the full model predicts a one-parameter curve in (w₀, w_a), with the heat share — the same number that sets the
matter yield — choosing the point. At the computed heat share it sits at w₀ ≈ −0.74, w_a ≈ −0.34: inside the locked
ceiling, and closer to the DESI DR2 direction (w₀ ≈ −0.75 to −0.80) than PURE-TWIST, though DESI's w_a (≈ −0.7) is
still deeper. This replaces the exponential numbers in D78. Not yet tested against data: a locked test (heat share
fixed from D42's computed range, not fitted) is the natural next step.
