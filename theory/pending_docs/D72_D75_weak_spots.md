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
(fitted to ρ_DE)" in REVIEW_GUIDE. Update (D79/D84): the tail energy is m²e^{−2n}μ/(4x_f) with the field frozen at
x_f ≈ 350–450, so the matching value is n ≈ 123.8 (126.8 ignored the 1/x_f factor); the runs use n = 125, close enough for
shapes. Either way chosen. What the theory does predict is the shape (w₀ ≈ −0.90, w_a ∈ [−0.15, 0]) once
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

## TAIL-F result (locked PREREG_TAIL_F, 13 Nov 2026 09:09; scored the same morning)

FIXED (heat share 0.13%, w₀ −0.74, w_a −0.34, no free extra parameter): Δχ² = +29.2 vs ΛCDM → **FULL TAIL
DISFAVOURED**. RANGE (heat share free 0.01–0.25%): best at the lower edge, 0.01% (w₀ −0.89, w_a −0.16, i.e. the
PURE-TWIST limit), Δχ² = −2.79 vs ΛCDM, +3.4 behind free w₀w_a → **DATA WANT LESS HEAT THAN COMPUTED**.

What this means. The model as written, with the reheating we computed, makes today's dark energy too stiff, and the
data reject it strongly. The data are happy only in the limit where the cliff's leftover slope has died away — which
is PURE-TWIST. So PURE-TWIST is not automatic: the theory must do one of
  (a) make far less heat (≲ 0.01%: g ≈ 0.1 → smaller, which also moves the matter yield), or
  (b) change the cliff factor so its leftover slope dies off fast (e.g. exp(−nT²/(T² + m2²))) — a new model version
      that keeps the computed reheating and returns the √(2/3) tail;
  (c) let the field keep travelling further after the cliff by some other route (not identified).
None is taken yet; this is Danny's call. Until then the honest summary is: PURE-TWIST fits; the full model with its
computed reheating does not.

## Development 79 — a reshaped cliff: exp(−n(1 − e^{−πT/4})) keeps inflation and gives the √(2/3) tail at any heat

Script: theory/inflation/cliff_v2.py; results/cliff_v2.txt. Done after TAIL-F failed (so: a model change made after
seeing data — labelled as such).

The problem (TAIL-F). The old cliff factor exp(−nT/(T + m2)) leaves a slope that dies only like 1/x, so at the
computed heat share the tail is too steep (Δχ² +29).

Tried.
  (i) exp(−nT²/(T² + m2²)) (leftover dies like 1/x²): tail becomes exactly PURE-TWIST, but the cliff's quadratic term
      takes over the plateau and r drops to 0.0010–0.0017, breaking the locked r = 0.0034–0.0040. Rejected.
  (ii) exp(−n(1 − e^{−T/m2})) (leftover dies like e^{−x/m2}): at small x it is −nT/m2, the same linear term as the old
      cliff, so the plateau is unchanged; at large x the leftover vanishes exponentially. Taken.

Results for (ii), μ = 1, n = 125:
  - Inflation unchanged: N* 55.7, n_s 0.9642, r 0.0038 (old: identical), for m2 = 0.5, 1 and 4/π.
  - Tail: slope (0.99–1.00) × √(2/3) and w₀ −0.90, w_a −0.145 at heat share 0.04%, 0.13% and 0.4% alike — the tail no
    longer depends on reheating. The field freezes at x ≈ 350–450 at 0.13%.
  - Angle y: heavy on the plateau (+4H²); unstable only while crossing the cliff (x ≈ 0.3–10, passed in kination);
    stable on the tail from x ≈ 30 (+2H²; old cliff only from x ≈ 500).
  - Helper field S: same plateau rule (−2 + 8ζx); with this cliff S is slightly unstable far down the tail if ζ = 0
    (−1.0H² at x = 100), so the ζ ≳ 10⁴ term of D72 is now needed on the tail too; with it S is heavy everywhere.

Choice of m2: m2 = 4/π. Then e^{−T/m2} = e^{−2πT/8}, the exponent of an SU(8) gaugino condensate — the same hidden
SU(8) and the same A = π/4 as the matter kick — and the cliff factor becomes periodic in the angle y with period 8,
the twist angle's own period. (The old cliff broke that periodicity.) This is a motivated form, not a derivation:
why the condensate appears inside an exponential (a "double exponential") is not explained. Label: chosen.

Consequence for the tests. The new version's tail is PURE-TWIST, so PURE-TWIST's locked results now apply to the
full model at its computed heat share; but this was arranged after TAIL-F, so new data (DESI DR3, Euclid) are the real
test. Inflation's locked predictions (n_s, r) are untouched. Matter: the end of inflation is unchanged for m2 = 1 and
rescaled in x for m2 = 4/π (x_end 8.8×10⁻³ vs 7.0×10⁻³); the kick and yield are expected to be unchanged — to be rechecked.

## Development 80 — quantum stability of the tail and supersymmetry breaking today (open, severe, generic)

Script: theory/darkenergy/tail_quantum.py; results/tail_quantum.txt.

Tree level is safe. Adding a constant W₀ (the source of today's gravitino mass, m₃/₂ = |W₀|/(2x)^{3/2}) leaves the
potential unchanged at S = 0: the no-scale structure cancels K^{TT̄}|D_TW|² against −3|W|² exactly, so the tail keeps
its shape whatever W₀ is. (The S field's own F-term breaks supersymmetry only at the meV scale, √ρ_DE.)

Loops are not. Any particle whose mass depends on x adds ~m⁴/(64π²) to the vacuum energy with an x-dependence, which
would swamp the tail: an electron 10³¹ × ρ_DE, a TeV superpartner 10⁵⁶ ×. Only particles lighter than ~6 meV may have
x-dependent masses. So the theory needs (a) the Standard Model sequestered from T (as D73 already requires) and (b)
superpartner masses that do not depend on x — e.g. supersymmetry breaking in a sequestered sector with no-scale
cancellation surviving at one loop. Neither is shown. This is the Kolda–Lyth problem shared by every quintessence
model with a rolling modulus, and the cosmological-constant problem behind it is not solved here either.
Label: open, generic, severe. Stated in REVIEW_GUIDE assumptions.

## Development 81 — how early S is stable, the size of ζ, and where inflation starts

Script: inline (cliff_v2 + the D72 rule m_S²/H² = −2 + 8ζx); results/s_early_efolds.txt. Reshaped cliff, m2 = 4/π:
CMB point x* = 1.34×10⁻⁴ (N* 55.7).
  ζ = 10⁴: S stable for 248 e-folds before the CMB point, but only heavy (m_S > 3H) from 1.3 e-folds after it.
  ζ = 3×10⁴: stable 856 e-folds before, heavy from 109 e-folds before the CMB point.
  ζ = 10⁵: heavy from 496 e-folds before.
So the working value is raised to ζ ≳ 3×10⁴ (Λ = 1/√ζ ≈ 6×10⁻³ M_P ≈ 1.4×10¹⁶ GeV — still the GUT scale). D72's
"ζ ≳ 10⁴" is superseded for the reshaped cliff.

Initial conditions. The plateau runs on to x → 0, so inflation can start anywhere earlier on it; with ζ ≳ 3×10⁴ there
are hundreds of e-folds of plateau on which S is heavy before the CMB scales leave. What is not addressed is the general
plateau-inflation question of why a patch starts smooth and potential-dominated (Ijjas–Steinhardt–Loeb); the Twist
says nothing new about it. Label: open, generic.

## Development 82 — birefringence: the Twist's zero is robust (two independent reasons)

The measured rotation 0.28 ± 0.06° (4.9σ, calibration-dependent) is in tension with our locked β = 0. Why we predict 0:
  1. The photon's coupling to the angle would come from a T-dependent gauge kinetic function. The Standard Model is
     sequestered on D3 branes (D73, needed against fifth forces), so there is no y F F̃ term.
  2. Even with such a term the rotation is (k/2)(y_today − y_last-scattering). The angle sits at its minimum on the tail
     (stable, D79), unmoved since long before last scattering, so the difference is zero.
Both would have to fail for the Twist to give a rotation. So if a calibration-independent birefringence is confirmed at
≥ 5σ, the Twist is falsified on this point — no adjustment available. (Already a stated falsifier.)

## Development 83 — the link to loop quantum gravity: what is derived, what is assumed, and a mismatch today

What is from the literature. Promoting the Barbero–Immirzi parameter to a field (Taveras–Yunes 2008; Calcagni–Mercuri
2009) and embedding it in N = 1 supergravity with K = −3 ln(T + T̄) (Gates–Ketov–Yunes 2009, arXiv:0906.4978) are
published constructions. The Twist starts from them, so the α = 1 field space and the slope √(2/3) are inherited.

What the Twist assumes. (1) That this field is the no-scale modulus T of the whole model (inflaton, dark energy). (2) The
superpotential W = √3 m S F(T) and the shape of F — chosen, not derived from LQG. (3) The Nieh–Yan coupling c_A = √(3/8)
(D-level choice, COUPLING_CHOICE_NIEH_YAN.md). Nothing in the Twist uses LQG's quantum geometry itself (spin networks,
area spectrum); the "loop quantum gravity" content is the name and origin of the field.

A mismatch. In LQG the parameter has a value fixed by black-hole entropy, γ ≈ 0.24–0.27. With the mapping used
earlier (UFE check LQ: real part of the field multiplies R, imaginary part multiplies the Holst term, so 1/γ = y/x),
the Twist today has y = 0 (the angle sits at its minimum, D79/D82), so 1/γ = 0: the Holst term is switched off today,
not set to 0.24. With x today ≈ 450 no simple alternative mapping gives 0.24 either (1/x ≈ 0.002). So the Twist does
not reproduce the LQG value of γ today. Either the mapping is different (open), or γ's black-hole value is not the
present value of this field (then the link to LQG's entropy counting is lost). Label: open; a reviewer from LQG will
ask this first. (The older UFE-LQ "match" of 0.259 was for a different, superseded model in which the angle carried
the late-time field.)

## Development 84 — kination after the cliff adds about 2 e-folds: n_s moves up to ≈ 0.9654

Script: theory/inflation/kination_Nstar.py; results/kination_Nstar.txt (reshaped cliff, m2 = 4/π).
The locked n_s (0.963–0.965) used N* for instant reheating. In the Twist the inflaton's motion dominates after the cliff
(kination, w = 1) until the reheating radiation takes over. A stiff phase adds e-folds: ΔN = ¼ ln(ρ_end/ρ) − ΔN_a, computed
on the actual background: +2.23 / +1.94 / +1.66 at heat share 0.04% / 0.13% / 0.4%. At 0.13%: N* 57.6, n_s 0.9654,
r 0.0035 (instant reheating: 55.7, 0.9642, 0.0038).
Together with the loop estimate of D77 (+0.002, order of magnitude) the Twist's best number is n_s ≈ 0.965–0.968,
r ≈ 0.0035. This is an upward systematic on the locked prediction, found after locking; the locked rule is scored as
written (its range 0.963–0.965 sits at the edge). It eases the ACT/SPT tension (0.974) by about a third, not more.

## Development 85 — kination also changes the dark-matter mass (estimate)

Script: theory/matter/dm_kination.py; results/dm_kination.txt.
The gravity-only dark-matter estimate (D38, D58: 3.5×10⁶–1.9×10⁷ GeV) assumed radiation domination from T_RH down. In
the Twist the bath forms during kination (D84), when the universe expands faster than radiation alone would make it,
so less dark matter is made from the bath. With the radiation share at bath formation taken from D84's kination e-folds
(f_eff ≈ 4×10⁻⁴ at the computed heat share), the yield falls by ×19–58 and the dark-matter mass needed rises to
≈ 1×10⁸–6×10⁸ GeV (range 6×10⁷–1×10⁹ over heat shares 0.4–0.04%). Still far below T_RH, so the light branch holds.
Label: estimate (no full Boltzmann run). Gravitational production directly from the inflaton is small here: the usual
channel needs an oscillating inflaton condensate, and in kination the field does not oscillate; the fermion is conformal
when light, so the change of expansion at the cliff makes almost none. Residual open item: a full Boltzmann run.

## Development 86 — kination tilts the primordial gravitational waves blue (estimate)

Script: theory/inflation/gw_kination.py; results/gw_kination.txt. Inflation's waves (r ≈ 0.0035) give a flat
Ω_GW h² ≈ 3.5×10⁻¹⁸ at low frequency. Modes that re-entered during kination are boosted ∝ frequency, up to ×50–90 at
≈ 10⁷ Hz (Ω_GW h² ≈ 2–3×10⁻¹⁶). A real feature of the Twist (a stiff phase after inflation), but far below the N_eff
bound and below any planned detector. Not a near-term test; recorded as a prediction of shape.

## Development 87 — a candidate origin for the reshaped cliff (speculative)

Script: inline; results/n_instanton.txt.
Write the cliff factor as a condensate of the inflation sector itself: exp(−n(1 − e^{−πT/4})) = exp(−b·f(T)) with a gauge
kinetic function f(T) = (n/b)(1 − e^{−πT/4}). Near the plateau f ≈ (n/b)(π/4)T — the standard linear f = kT; once the
hidden SU(8) condensate (∝ e^{−πT/4}) has switched off, f saturates at n/b. So the reshaped cliff is what a T-dependent
gauge coupling would give if the hidden SU(8) condensate enters the inflation sector's coupling as a threshold
correction. This also turns n into a coupling: one instanton, n = 8π²/g², gives α = g²/4π ≈ 1/20 for n ≈ 124 — near,
but not at, the unification value (~1/25); an SU(8) condensate (n = 8π²/(8g²)) would need α ≈ 1/158.
Status: a story, not a construction. Nothing here derives the threshold correction's size or sign, and "α ≈ 1/20" is a
numerical observation with obvious look-elsewhere risk (several conventions tried). Recorded as a lead to check against
string constructions (e.g. moduli-dependent threshold corrections, Dixon–Kaplunovsky–Louis), not as support.

## Development 88 — gravitinos are safe from the heat, but their mass moves with x (estimate)

Script: theory/matter/gravitino_check.py; results/gravitino_check.txt.
At T_RH ≈ 3×10¹⁴ GeV the plasma makes gravitinos with Y ~ 3×10⁻⁸. For m₃/₂ = 10¹¹–10¹³ GeV they decay at T ≈ 10⁶–10⁹ GeV,
holding only 0.03–0.3% of the energy then — never dominant, long before nucleosynthesis. (Their decay products need the
R-parity violation already assumed.) The D26 gravitino worry is therefore not a problem at these masses.
But with a constant W₀ the gravitino mass is m₃/₂ = |W₀|(2x)^{−3/2}: it falls by ~10⁴–10⁷ between reheating (x ≈ 0.01–1)
and today (x ≈ 450). Superpartner masses set by gravity mediation would move with x the same way — exactly the x-dependent
masses that D80 shows would swamp the tail through loops. So the Twist needs supersymmetry breaking whose visible-sector
effects do not follow x (sequestered, e.g. anomaly- or gauge-mediated with a T-independent messenger sector). This sharpens
D80; it does not solve it.

## Development 89 — correction to D73: if T were a string volume modulus, branes would not shield matter

Script: inline; results/volume_modulus_fifth_force.txt.
D73 said: put the Standard Model on D3 branes, whose gauge coupling does not depend on T, and the proton mass stops
depending on x. That holds in string units, not in Planck units. If T were the overall volume modulus (K = −3 ln(T + T̄)
is exactly its Kähler form), the string scale in Planck units goes as M_s/M_P ∝ V^{−1/2} ∝ x^{−3/4}, and every brane
mass (Λ_QCD, so the proton) follows it: β_m = (3/4)√(2/3) ≈ 0.61, excluded by Cassini ×180. This is the known reason a
light volume modulus cannot be quintessence.
What it means for the Twist. T must not be the string volume modulus. In the Twist T is the Barbero–Immirzi field, which
shares the volume modulus's Kähler form but whose value need not set the string scale — so the conflict is avoided only
if that identification holds and the Planck-to-string ratio is fixed by something else. The brane language used in D70
(hidden SU(8) on a separate cycle) and D73 (Standard Model on D3 branes) is therefore an analogy borrowed from string
constructions, not a construction of the Twist. Label: correction (D73's justification was incomplete); open: an
explicit setting in which a field with K = −3 ln(T + T̄) is light today without setting the string scale.

**D89 addendum — the 4D supergravity reading (a way through).** If the Twist is read as a 4D supergravity with no string
scale behind it (T is the Barbero–Immirzi field, nothing more), the question is only how matter's masses depend on T in
Planck units. Put matter in the sequestered no-scale form K = −3 ln(T + T̄ − Σ|Q|²/3) (matter metric K_Q = 1/(T + T̄)).
Then a physical Yukawa coupling is e^{K/2}·Y/√(K_Q K_Q' K_H) = (2x)^{−3/2}·Y·(2x)^{3/2} = Y: independent of T. The QCD
scale is fixed if f_QCD does not depend on T. Tree-level scalar masses vanish (no-scale). What still depends on T is any
dimensionful superpotential term: a μ-term gives physical μ = e^{K/2}μ/K_H ∝ x^{−1/2}, so the Higgs vev, and with it the
electron and quark masses, would follow x unless μ is generated in a T-independent way (e.g. from the same sequestered
SUSY-breaking sector, D88). So in the 4D reading the fifth-force problem reduces to D73's residual Higgs-sector question,
and the string-volume objection of D89 does not apply. Label: derivation of a known property (conformal sequestering);
the μ-term origin stays open.

**D89 addendum, caveat (written after checking the scaling more carefully).** In the sequestered no-scale form the matter
sector is conformally coupled: canonically normalised, dimensionless couplings are T-independent, but every dimensionful
parameter in it scales as x^{−1/2} in the Einstein frame (μ, any supersymmetry-breaking F-term, hence soft masses). Whether a
dynamically generated scale such as Λ_QCD (so the proton mass) also scales as x^{−1/2} depends on how the trace anomaly
couples to the supergravity compensator; I have not settled this. If it does, the proton mass moves with x, β_m = ½√(2/3)
≈ 0.41 (excluded ×120), and the fifth-force problem returns in full — the same as D73's "weight 1" case. So the honest
status of D73/D89 is: the fifth-force problem is not solved in either reading; it reduces to whether all Standard-Model
scales can be made T-independent, which needs a mechanism not in the Twist. Label: open, severe (alongside D80).

## Development 90 — the QCD scale does move with x: the fifth-force problem is real (settles the D89 caveat)

Script: theory/darkenergy/fifth_force_KL.py; results/fifth_force_KL.txt.
The physical gauge coupling in supergravity depends on K and on the matter metrics through the anomaly (Kaplunovsky–Louis):
1/g² = Re f + (b/16π²) ln(M_P²/μ²) + (c/16π²)K − Σ T(r)/(8π²) ln det Z_r. For QCD in the MSSM (c = 3, b = 3), with
K = −3 ln(2x) and matter metric Z = (2x)^{−n}, Λ_QCD ∝ x^{3/2 − 2n}:
  - n = 1 (sequestered / D3 form): Λ_QCD ∝ x^{−1/2}, Yukawas fixed → proton mass moves, β ≈ 0.41 (Cassini ×120).
  - n = 0 or 3/2: Λ_QCD ∝ x^{±3/2} → β ≈ 1.2.
  - n = 3/4 (the one weight that fixes Λ_QCD): Yukawas then go as x^{−3/8}; the ~5% of the nucleon mass from quark masses
    gives β ~ 0.015 (×4.5 Cassini), and electrons and nuclei with different quark content fall differently (equivalence
    principle, far above MICROSCOPE). And 3/4 is not a natural weight.
Conclusion. No modular-weight choice shields ordinary matter from a light T. The fifth-force problem is a real, unsolved
problem of the one-field Twist: if T is today's dark energy, matter feels it at the 1–100% level. Options (Danny's call):
(1) find a shielding mechanism (none known); (2) let a separate, shielded field carry dark energy, keeping T for inflation,
reheating and the kick; (3) state it as the theory's main open problem. Status recorded: (3), with (2) as the clean fallback.

## Development 91 — screening does not rescue it (option 1 checked)

Script: theory/darkenergy/screening_check.py; results/screening_check.txt.
Known ways a light coupled field hides from solar-system tests, checked against the Twist's tail:
  - Chameleon (Khoury–Weltman): with the Twist's exponential tail and β ≈ 0.41, the field's Compton wavelength inside the
    Sun is 1.8 AU and inside the Earth 0.9 AU — far larger than the bodies (needs ≪ radius). No thin shell: NOT screened.
    (Chameleons need inverse-power potentials that steepen toward small field; an exponential does not.)
  - Damour–Polyakov least coupling: needs the matter coupling A(φ) to have a minimum the field is drawn to; here masses
    are power laws in x (D90), monotonic — no minimum.
  - Symmetron: needs a Z₂ symmetry and a symmetry-breaking potential; the tail has neither.
  - Vainshtein/derivative screening: needs higher-derivative interactions absent from two-derivative supergravity.
Conclusion: none of the standard mechanisms applies. Option 1 is closed within known physics; the remaining choices are
(2) a separate, shielded dark-energy field, or (3) the stated open problem.

## Development 92 — a lead: the twist ANGLE as dark energy, with the size half stabilised

Script: theory/darkenergy/angle_dark_energy.py; results/angle_dark_energy.txt.
Idea. Both severe problems (D80 loops, D90 fifth force) come from the SIZE half x being light today. The ANGLE half y is
different: matter couples to it only through its rate of change (Nieh–Yan, shift symmetry), so a slowly rolling angle gives
no fifth force, and its potential is protected from loop corrections by that symmetry (the original motivation of
pseudo-Nambu–Goldstone quintessence, Frieman–Hill–Stebbins–Waga 1995). So: let x settle in a minimum after the cliff
(heavy, short range) and let the angle carry dark energy. One field T still does everything — size for inflation, angle for
the matter kick and for dark energy.
Numbers (angle potential L⁴(1 + cos(φ_y/f)), f = 1.56 M_P, thawing from rest at angle θ_i from the top, Ω_DE 0.69):
  θ_i 0.1–0.6 → w₀ ≈ −1.00 to −0.99 (ΛCDM-like); 1.0 → −0.98, w_a −0.03; 1.5 → −0.94, −0.09; 2.0 → w₀ −0.80, w_a −0.30;
  beyond ~2.2 no dark-energy solution. So the angle gives a one-parameter family from ΛCDM to (−0.80, −0.30), along the
  direction DESI points. θ_i would be where the angle came to rest after the kick — set by the matter-making dynamics, so in
  principle computable rather than free.
What it needs (not done): (a) a minimum for x after the cliff (moduli stabilisation; a model change, and the PURE-TWIST tail
predictions would be replaced); (b) the angle's potential height ≈ ρ_DE (the cliff factor already makes the potential
periodic in y with period 8, D79, with a height suppressed like e^{−πx/4} — whether it lands at ρ_DE depends on where x
settles); (c) f from the kinetic weight at the settled x (1.56 M_P was computed elsewhere on the path); (d) θ_i from the kick.
Label: lead, exploratory. If it works it removes both severe problems while keeping the one-field claim. Danny's call
whether to develop it (it changes the late-time model).

## Development 93 — working on D92: where the angle's dark-energy height comes from, and what still blocks it

Results: field_tests/results/angle_de_scale.txt.
(1) The height. After σ decays, the SU(8) linking term leaves the angle a potential Λ⁴e^{−(π/4)x}[1 − cos(πy/4)] — periodic
with the angle's own period 8. With the height the matter kick needs at the cliff (Λ⁴ ≈ 10⁻¹⁸–10⁻¹⁷ M_P⁴, D68/D70), this
equals today's dark energy (7.3×10⁻¹²¹ M_P⁴) when x ≈ 299–302. The reshaped cliff's kination run leaves the field at
x ≈ 446 / 145 for heat share 0.13% / 0.4% — x ≈ 300 corresponds to a heat share of about 0.2%, inside the computed range.
So the same term that makes matter would, at the size where kination leaves the field, have the height of dark energy:
the dark-energy scale would follow from the matter sector instead of being chosen (n would no longer set it; the size
half's own leftover e^{−2n} must then be smaller, n ≳ 124). Caution: one coincidence, found by looking; not support yet.
(2) The block. For no fifth force the size half must be heavy (range < ~50 μm, m_x ≳ 4×10⁻³ eV) with its minimum at
x ≈ 300 and its own energy there ≈ 0. A light, merely frozen x still gives the β ≈ 0.4 force (D90). So the route needs a
stabilising potential for x whose minimum sits at the kination freeze point — a coincidence of two scales unless one
mechanism sets both — and whose zero is tuned (the cosmological-constant problem moves there). If the minimum is not where
the field arrives, x oscillates with Planckian amplitude and becomes a moduli problem (dilutes the matter made at the kick).
(3) Where it stands. Better than D80/D90 (no fifth force from the angle, loop-protected potential, dark-energy scale tied
to matter), but it trades them for a stabilisation problem for x. Next concrete steps, if pursued: a superpotential term
that gives x a minimum near 300 without touching the plateau; the angle's resting value θ_i after the kick (decides w₀,
w_a); f at x ≈ 300. Label: lead, exploratory.

**D93 step: a first stabiliser for x at ≈300 (crude estimate).** Script: inline; results/kklt_try.txt. Add a KKLT-type piece
W₂ = W₀ − A e^{−aT} (a second condensate, a = 2π/N). Asking for its minimum at x ≈ 300 and a mass m_x ≥ 4×10⁻³ eV (no
fifth force beyond ~50 μm) gives: a = 0.05 → A ≈ 10⁻¹⁹ M_P³; a = 0.1 → A ≈ 10⁻¹³; a = 0.2 → A ≈ 0.2 (spoils the plateau,
where the term is ≈ A); a = 0.3 → 10¹². So a slowly varying condensate (a ≈ 0.05–0.1, N ≈ 60–125) can hold x at 300 while
staying invisible on the plateau (its energy there ~10⁻²⁷ vs the plateau's 10⁻¹⁰).
Costs, stated: (i) KKLT minima are anti-de Sitter, depth ~ m₃/₂² M_P² ≫ ρ_DE, so an uplift must cancel it to 1 part in
~10⁶⁰ — the cosmological-constant problem, moved here; (ii) the gravitino today would be ~meV (m₃/₂ ~ |W₂|e^{K/2}), so
supersymmetry breaking for the Standard Model must come from elsewhere (gauge-mediation-like; a meV gravitino is
cosmologically allowed); (iii) the minimum must sit where kination leaves the field (≈300 at ~0.2% heat) or x oscillates
(moduli problem); (iv) the mass estimate is order-of-magnitude (m_x ~ a²x|W₂|e^{K/2}). Status: not ruled out; worth a
proper two-field calculation if Danny wants this route.

## Development 94 — the stabilised-size route meets the cosmological moduli problem

Script: theory/darkenergy/modulus_problem.py; results/modulus_problem.txt.
If x is held in a valley at x_s today, it was not there all along: kination leaves it frozen at x_f, and it starts to
oscillate about x_s when H falls to m_x. Its oscillation then behaves like matter and grows relative to radiation:
  - m_x = 4×10⁻³ eV (just enough against fifth forces): starts at T ~ 750 GeV; with an amplitude of 1 M_P the relic is
    ~10¹¹ × the critical density; it must start within 1.3×10⁻⁶ M_P of the valley (x_s = x_f to 1 part in 10⁶).
  - heavier, non-decaying moduli are worse (1 eV: 3×10⁻⁷; 1 MeV: 10⁻⁸).
  - very heavy moduli (≳10⁵ GeV) decay before nucleosynthesis, but their decay releases entropy that dilutes the matter
    asymmetry made at the kick — the matter match (D62) would be lost by a large factor.
Also: if x_s lies below x_f, the field passes the valley during kination with far more kinetic energy than the valley's
depth (~m₃/₂²) and overshoots (Brustein–Steinhardt).
Way out, untested: adiabatic tracking (Linde 1996) — if x carried a Hubble-induced mass well above H all the way from the
cliff, it would follow its valley and oscillations would be exponentially small; that contradicts the free kination
roll the reheating and matter results rely on.
Conclusion for the D92/D93 route: it trades the fifth force for a moduli problem that needs x_s = x_f to ~10⁻⁶ (or a
tracking mechanism that changes reheating). Ranking of the three options after D90–D94:
  (2a) separate shielded dark-energy field: clean, gives up "one field does everything" for dark energy;
  (2b) angle as dark energy with stabilised size (D92–94): elegant, keeps one field, but needs a 10⁻⁶ coincidence or new
       tracking physics;
  (3) one-field tail as is: fits data (PURE-TWIST) but has the unsolved fifth-force and loop problems.
Danny's call. Status recorded: (3), with (2a) and (2b) written up.

**Matter recheck, first result (old cliff reproduced, 10:00).** Same nominal settings as the 09:00 check (μ = 1, f = 0.0013,
m_σ = 6×10⁹ GeV, y = 0.1, cliff-switchable copy of hidden_kick_decay.py): n_B/s 8.96×10⁻¹¹ (1.03×), dilution 4.48 —
vs 0.87× and dilution 5.32 in confirm_f0013_m6e9.txt. The two runs differ by 18%; the 09:00 command line was not saved, so
some setting (probably s0, the hidden field's start) must have differed. Both are within ~15% of 1×, so m_σ ≈ 5–6×10⁹ GeV
stands; the old-vs-new-cliff comparison below uses one script and one set of settings, so it is like for like.

## Development 95 — the structural choice behind D90–D94

Putting D90–D94 together:
  - A size half x that is light today gives a fifth force (D90), with no screening (D91) and no loop protection (D80).
  - Any fix makes x heavy today. If x reaches its valley late (after kination), its oscillation overcloses the universe or
    dilutes the matter unless it lands within ~10⁻⁶ of the floor (D94). That holds for option (2a) too: a separate
    dark-energy field does not remove the need to park x.
  - The one moduli-safe way to park x is a valley right after the cliff, with a mass near the inflaton's (~10¹³ GeV): then
    x simply oscillates and decays as the inflaton does in standard models — reheating by inflaton decay, no kination.
So the real fork is:
  (A) Keep the light tail (one field does everything, PURE-TWIST predictions w₀ ≈ −0.90, w_a ≈ −0.15) and carry the fifth-force
      and loop problems as the theory's main open problems (the status today).
  (B) End inflation in a valley (cliff → minimum). Inflation's n_s, r stay (plateau unchanged); reheating, N*, the kick, the
      dark-matter mass and n_s's kination shift must all be redone; dark energy must then come from somewhere else — a
      constant, the angle (needs a height source other than the SU(8) term, which is far too large at x ~ 1), or a separate
      shielded field. PURE-TWIST's late-time predictions would be dropped; the late universe would be ΛCDM-like unless a new
      dark-energy piece is added.
(A) is a bold, testable theory with a known hole; (B) is safer but gives up the late-time half of the "one field" claim.
Danny's call; nothing is changed until he chooses.

**Decision (Danny, 10:03): route A.** Keep the light tail; one field does everything; the fifth force (D90–D91) and the
tail's quantum stability (D80) are stated as the theory's main open problems. Routes B and the angle-dark-energy lead
(D92–D94) stay written up as alternatives.

## Development 96 — no choice of modular weights shields all of the Standard Model (strengthens D90)

Script: theory/darkenergy/weights_shield.py; results/weights_shield.txt.
D90 used one weight for all matter. Allowing every MSSM multiplet its own weight (Q, U, D, L, E, H_u, H_d; generation-
universal), we asked for all seven conditions at once: the three gauge couplings fixed (Kaplunovsky–Louis), the up, down and
lepton Yukawas fixed, and the μ-term fixed. The equations have rank 5 and are inconsistent: no exact solution exists.
Relaxing any one of SU(3), the up or down Yukawa, or μ still leaves no solution; relaxing one of SU(2), U(1) or the lepton
Yukawa allows one, but what is left over is far outside the bounds:
  - SU(2) or U(1) left free: d ln α/dφ ≈ 0.01–0.04, against atomic-clock and quasar limits of ~10⁻⁶;
  - lepton Yukawa left free: m_e ∝ x^{3/2}, an equivalence-principle violation η ~ 6×10⁻⁹ against MICROSCOPE's 10⁻¹⁵.
So the obstruction is structural (it comes from the Standard Model's own anomaly coefficients), not a matter of choosing
weights. This confirms D90: with the light tail (route A) the fifth force cannot be removed inside this framework at one loop.

## Development 97 — what the fifth force means for the data tests (consistency note)

Every late-time fit (PURE-TWIST, K816, FLAG-1, TAIL-F) let the tail field couple to nothing (PURE) or to dark matter only.
If ordinary matter is not shielded (D90, D96), the theory as written also couples the field to baryons, with β_b ≈ 0.4.
Such a coupling would change the cosmology too (baryon clustering and the baryon acoustic scale), not only solar-system
tests, and would very likely be excluded by the CMB and BAO on its own — not computed here (the coupled AxiCLASS build
couples the field to dark matter only). So the data results describe the Twist *with* a working shield. Stated plainly:
PURE-TWIST's fits test the tail's shape; they do not test the unshielded theory, which is excluded by Cassini already.
Label: consistency note; it belongs beside the main open problem in REVIEW_GUIDE.

## Development 98 — the remaining observables, and a coverage table

Scripts: theory/inflation/extra_observables.py; results/extra_observables.txt, hidden_glueballs.txt; table: theory/COVERAGE.md.
Inflation at the Twist's own N* = 57.6: n_s 0.9654, running α_s = −6.0×10⁻⁴, r 0.0035, tensor tilt n_t = −4.4×10⁻⁴ (the
single-field consistency relation n_t = −r/8 — a test for a future B-mode experiment), squeezed non-Gaussianity
f_NL ≈ 0.014 (unobservably small, as for any single-field slow roll), inflation scale V^{1/4} ≈ 7.9×10¹⁵ GeV, H* ≈ 1.5×10¹³ GeV.
Hidden SU(8): confines near 10¹⁴ GeV (from the kick height); its glueballs decay through Planck-suppressed operators in
~10⁻³ s, before nucleosynthesis — no relic, no extra radiation. Nucleosynthesis: the field is frozen from kination until it
thaws in the last few billion years, so constants at BBN equal today's (given a shield). Hubble constant: PURE-TWIST gives
H₀ ≈ 66.8, so the Twist does not ease the SH0ES tension. Areas the Twist does not address: black holes, the Big Bang
singularity, and LQG's quantum geometry itself. The full area-by-area table is theory/COVERAGE.md.

## Development 99 — black holes

Results: field_tests/results/bh_singularity_lqg.txt.
  - No hair: a static black hole cannot carry a charge of a minimally coupled light scalar (Bekenstein), so black holes
    in the Twist look exactly like general relativity's; the slow cosmological roll gives only negligible "hair".
  - Mergers: no scalar radiation from black-hole pairs, and c_gw = c (locked null). Neutron stars are different: if matter
    is unshielded they carry the field's charge (β ≈ 0.4), and binary pulsars would radiate dipole waves — excluded, a
    second face of the main open problem (D90).
  - Superradiance: the tail field's mass is ~H₀ ~10⁻³³ eV, far below the 10⁻²⁰–10⁻¹⁰ eV window where black holes grow
    scalar clouds — no signal.
  - Black-hole entropy: LQG's S = A/4 fixes γ ≈ 0.24–0.27 at the horizon. In the Twist γ is a field; its value at a
    horizon would be today's cosmic value, which (D83) is not 0.24 under the mapping used. So the Twist does not reproduce
    LQG's entropy counting as it stands — the same open mismatch, seen from black holes.

## Development 100 — the Big Bang singularity

In loop quantum cosmology the singularity is replaced by a bounce at ρ_c = √3/(32π²γ³) ρ_Pl ≈ 0.41 ρ_Pl for γ = 0.2375
(0.27 ρ_Pl for 0.274). For plateau (Starobinsky-type) potentials a slow-roll phase after the bounce is "almost inevitable"
(Bonga & Gupt, arXiv:1510.00680), and the Twist's plateau has the same α = 1 shape, so a bounce-then-inflation history is
plausible. Two catches, stated: (i) with γ a field, ρ_c would depend on its value at the bounce, and under the mapping used
(1/γ = y/x, y = 0) γ is not ~0.24 there either; (ii) the helper field S and the hidden sector were never followed through a
bounce. Label: not derived; a consistent-looking outline that inherits the γ-mapping problem.

## Development 101 — loop quantum gravity's quantum geometry

LQG's area spectrum has a smallest area 4√3πγ ℓ_P² (≈ 5.2 ℓ_P² for γ = 0.2375). If γ is a field, the size of the area
quanta would change with it — over cosmic history and from place to place. No experiment can see Planck-scale areas, so
this gives no test, and the Twist uses none of LQG's quantum geometry in its calculations. Stated plainly: the Twist is a
supergravity model motivated by LQG; it does not derive anything from LQG's quantum geometry, and its γ field does not sit
at the value LQG needs (D83). Making that link real (a mapping under which today's field gives γ ≈ 0.24, or a reason γ's
black-hole value is not the cosmic field value) is the open foundational task.

## Development 102 — a possible fix for the γ mismatch (hypothesis, check queued)

Results so far: field_tests/results/gamma_mapping.txt. Check: field_tests/missing_piece/angle_end_check.py (queued).
The reshaped cliff (D79) makes the landscape periodic in the angle with period 8, and its deepest line is y = 4 (mod 8): at
x = 0.01–1 the energy at y = 4 is 10⁻⁹⁹–10⁻²¹¹ of that at y = 0 (the cliff has "already happened" there). Inflation runs
along y = 0, protected by a barrier near |y| ≈ 0.1 (from the Gaussian factor e^{−n(π/4)²y²} against the growth of |T|²),
which in canonical units is ~10³ M_P away on the plateau but only ~0.1–1 M_P at the cliff (x ~ 0.1–1). The hidden-axion
kick spins the angle exactly there. If it carries y past the barrier, the angle falls into the y = 4 valley and stays near
4 (mod 8) on the tail (far down the tail the two lines merge and y is held only weakly).
Consequence: with the most direct mapping, 1/γ = Im T (the Barbero–Immirzi pseudoscalar is T's imaginary part in the
Gates–Ketov–Yunes superfield), y = 4 gives **γ = 0.25** today — inside LQG's black-hole range 0.2375–0.274. That would close
D83/D99/D100's mismatch.
Cautions, stated before the check: (i) look-elsewhere — earlier (D83) we tried 1/γ = y/x and 1/x; this is the third
mapping; (ii) it rests on the kick moving y by ≳ 0.1 at the cliff, not yet computed; (iii) the period 8 itself was chosen to
match the Nieh–Yan instanton counting, so 1/γ = 4 = half a period is a structural number, not a fit — but "half a period"
is still a choice. Prediction written before the run: if y_end mod 8 ≈ 4 the hypothesis survives; if ≈ 0 it fails.

**D102 barrier, computed.** The angle barrier sits at |y| ≈ 0.11 on the plateau (height ×5×10⁵ at the CMB point, ~1400 M_P
away), shrinks through the end of inflation (×48 and 14 M_P at x = 0.01; ×1.05 and 0.8 M_P at x = 0.1) and is gone by
x ≈ 0.3: past there y = 0 is a ridge. But by then the potential has fallen by ~10⁻⁸⁰ and kination dominates, so the ridge
exerts almost no force: whether y reaches 4 is decided by how far the kick's velocity carries it while coasting. That is
exactly what the queued run measures (y_end).

## Development 103 — where the fifth force really comes from, and the one avenue left

Results: field_tests/results/fifth_force_frames.txt.
(1) Origin. In the Gates–Ketov–Yunes superfield the real part of T multiplies the curvature R — it is a conformal (Weyl)
factor. Put the Standard Model inside the same no-scale supergravity and it is conformally coupled: every mass scales as
x^{−1/2}. That, plus the Kaplunovsky–Louis anomaly terms, is D90's fifth force. It is a feature of the embedding, not of the
Barbero–Immirzi idea: in Einstein–Cartan–Holst gravity alone the field meets matter only through torsion (the Nieh–Yan
coupling to the axial current, a derivative coupling) — the Twist's original claim of "no fifth force".
(2) The fix at tree level. Let the Standard Model couple minimally to the Einstein-frame metric (outside the no-scale log),
meeting the twist field only through gravity and the Nieh–Yan term. Then β = 0 at tree level, and late-time loops cannot
regenerate it much: the canonical field has a nearly exact shift symmetry today (its potential is ~10⁻¹²⁰ M_P⁴), so induced
couplings are suppressed by V''.
(3) What breaks it again: supersymmetry thresholds. Below the superpartner mass m_soft the strong coupling runs with the
Standard Model coefficient (7) instead of the MSSM one (3), so Λ_QCD ∝ m_soft^{4/7}. If m_soft depends on x, the proton mass does:
  - gravity mediation, m_soft ~ m₃/₂ ∝ x^{−3/2}: β ≈ 0.70 (excluded);
  - F-term gauge mediation, F/M ∝ x^{−1/2}: β ≈ 0.23 (excluded);
  - a soft scale independent of T: β ≈ 0 (allowed).
Every F-term carries e^{K/2}, so F-term breaking always feels x. D-term breaking does not: the D-term potential carries no
e^K, so a Fayet–Iliopoulos term in a T-blind U(1) gives a supersymmetry-breaking scale independent of x.
(4) Status. The main open problem narrows to one concrete requirement: the Standard Model couples minimally in the Einstein
frame, and supersymmetry is broken by a T-independent D-term (with mediation that does not bring back an x-dependent F-term;
gravitino-mediated contributions, ∝ m₃/₂(x), must stay subdominant). Not built; known D-term-breaking models exist, but whether
one fits here is open. Label: narrows D90/D96 to a specific, checkable route; open.
Caveat on (3): a constant Fayet–Iliopoulos term in supergravity is constrained (Komargodski–Seiberg: it needs a gauged
R-symmetry); newer constructions allow constant FI terms without one (Cribiori, Farakos, Tournoy & Van Proeyen, 2017). Which
applies here, and whether the gravitino-mediated pieces stay small enough (they scale as m₃/₂(x)), are the first checks.
D103 follow-up (literature, 10:35). In no-scale models with the "new" Fayet–Iliopoulos terms the D-term potential is not
T-blind: e.g. for K = −2 ln(T + T̄) and constant f, V_D = 2g²/(f₀(T + T̄)²) (as quoted in Aldabergenov, arXiv:1903.11829),
and the Kähler-invariant new FI terms carry factors of e^{K} in general. For the Twist's K = −3 ln(T + T̄) such a term
scales like the other dimensionful scales (∝ x^{−1/2} for the soft scale), giving β ≈ 0.23 again. So the new FI terms do not
open the avenue. What remains is the old-style constant FI term with a gauged R-symmetry (V_D = g²ξ²/(2 Re f), T-blind if f
is), which brings its own constraints (the superpotential must carry R-charge, anomaly cancellation). Status: D103's route
narrows further to "a gauged-R, T-blind D-term"; still open, and harder than it first looked.
A point in its favour: the Twist's superpotential W = √3 m S F(T) already has an R-symmetry (S carries R-charge 2, T none —
the standard stabiliser-field structure), and the added W₀ − A e^{−aT} pieces would break it; so a gauged U(1)_R with a
constant FI term is structurally available for the inflation sector as written. Whether it survives anomaly cancellation and
coexists with the SU(8) and supersymmetry-breaking sectors is the concrete next check.

**Matter recheck, second result (10:37).** Reshaped cliff, m2 = 1 (same settings, same script): n_B/s 7.71×10⁻¹¹ (0.887×),
dilution 5.08, hidden share at end 4×10⁻¹⁹ — vs 1.030× with the old cliff. The reshaped cliff changes the matter yield by
−14%; m_σ ≈ 5–6×10⁹ GeV still gives the observed amount. (m2 = 4/π case running.)

## Development 104 — the Standard Model outside the supersymmetric sector: the fifth force largely goes away (estimate)

Script: theory/darkenergy/sm_outside_sugra.py; results/sm_outside_sugra.txt.
Proposal. The supersymmetric sector is the gravity/inflaton sector (T, S, χ, the hidden SU(8)); the Standard Model is NOT
supersymmetric and couples minimally to the Einstein-frame metric. It meets the twist field only through (a) gravity, (b) the
Nieh–Yan torsion term (a derivative coupling to the axial current — no force, but it drives matter-making), and (c) the
reheating field χ, through which it was heated.
What this removes. No conformal coupling (D89/D103), so no tree-level fifth force. No Standard-Model superpartners, so no
supersymmetry thresholds (D103) and no R-parity assumption. Supersymmetry breaking in the supersymmetric sector today is only
F_S ~ √ρ_DE ~ meV (W = 0 at S = 0, so m₃/₂ ≈ 0), so nothing x-dependent at a high scale reaches the Standard Model — D80's
loop problem is not triggered by Standard-Model masses.
What survives (one loop through χ, whose mass g|φ − φ₀| grows along the tail): d ln m_f/dφ ~ h²/(8π²·19). Then
  - h = 0.03: β_N ~ 2×10⁻⁷, η ~ 3×10⁻¹⁶ — passes Cassini and MICROSCOPE;
  - h = 0.1: β_N ~ 2×10⁻⁶ (Cassini fine), η ~ 3×10⁻¹⁴ (MICROSCOPE 10⁻¹⁵: fails by ~30);
  - h = 1: fails MICROSCOPE by ~10⁵.
So the χ–Standard-Model Yukawa must be h ≲ 0.05 (order of magnitude; the η estimate is crude).
A second constraint (the price of a non-supersymmetric SM): SM loops give χ a mass correction that breaks χ's supersymmetric
cancellation on the plateau (D77). With an ultraviolet cutoff at M_P this destroys the plateau for any h ≳ 10⁻³; with a cutoff
near the GUT scale (4×10⁻³ M_P) it is ΔV/V ~ 10⁻³ (h = 0.03) to 2×10⁻² (h = 0.1); with 4×10⁻⁴ M_P it is ≤ 2×10⁻⁴. So the
Standard Model's cutoff for its coupling to χ must sit well below M_P (≲ GUT scale) — a naturalness assumption, stated.
Knock-on: smaller h makes χ live longer, so more heat is released (heat share ∝ 1/h: ~0.8% at h = 0.05, T_RH ≈ 4×10¹⁴ GeV).
With the reshaped cliff the dark-energy tail does not care (D79); the matter yield at ~0.8% heat needs a recheck (it rises
toward f ~ 1%, D62 correction), which would move m_σ up.
Status: the main open problem (D90) has a concrete resolution at the order-of-magnitude level: Standard Model non-supersymmetric
and minimally coupled; χ–SM Yukawa h ≲ 0.05; SM–χ cutoff ≲ GUT scale. Label: estimate + assumptions; it returns the Twist to
its original "no fifth force" picture. To do: a matter-yield run at h ≈ 0.03–0.05; a careful MICROSCOPE estimate.
D104 refinement (Ti vs Pt, MICROSCOPE's test masses): Δβ from the electron-fraction difference (3×10⁻⁵ of the mass) and
nuclear σ-term/binding differences (~10⁻⁴), η ≈ 2Δβ·β_Earth: h = 0.05 → η ~ 9×10⁻¹⁷ (passes), h = 0.1 → ~1.4×10⁻¹⁵ (borderline).
Constraint: h ≲ 0.08 (still order-of-magnitude). Caveat: today χ's mass g|φ − φ₀| ~ 2 M_P is above the Planck scale, so the
χ-loop estimate sits at the edge of the effective theory; χ should be treated as integrated out, which only weakens its
effects — the bound is conservative in that sense.

## Development 105 — tail stability after D104: the supersymmetric sector is fine; the Standard Model's vacuum energy is not

Script: theory/darkenergy/tail_stability_d105.py; results/tail_stability_d105.txt.
(a) Supersymmetric-sector loops today are harmless: the χ multiplet, split only by Hubble-sized masses (~H₀²), shifts the tail
energy by ~0.8% and its slope by ~0.1%; the helper field S contributes ~10⁻¹⁰⁸ of ρ_DE. So D80's problem no longer comes from
particle masses (D104 removed the SM's x-dependent masses).
(b) What remains is the Standard Model's vacuum energy reaching x through χ. With χ integrated out (its mass g|φ − φ₀| is
near M_P), the x-dependent part is ~h²Λ⁶/(m_χ²(16π²)²) for a renormalisable coupling: with h = 0.05 that is ~10²⁰ ρ_DE even
for a TeV cutoff (10⁹⁸ for a GUT cutoff). If χ reaches the SM only through gravity it is ~10⁻⁸ ρ_DE for a TeV cutoff (fine) but
~10⁴⁸ for 10¹⁰ GeV and ~10⁹⁶ for the GUT scale. So the tail is stable only if the Standard Model's large vacuum energy does not
couple to x at all — i.e. whatever cancels the cosmological constant must also cancel its field-dependent parts. That is the
cosmological-constant problem in field-dependent form, shared by every quintessence model; it is not solved here.
(c) A useful by-product: χ can reach the SM only gravitationally and still reheat. Its gravitational decay rate ~m_χ³/(8πM_P²)
is fast because χ is heavy: it decays after Δφ ≈ 0.52 M_P (m_χ ≈ 0.05 M_P, below M_P — so the trans-Planckian-χ worry of the
gap list does not arise: χ is gone long before its mass would pass M_P), giving a heat share ≈ 0.8% (T_RH ≈ 4×10¹⁴ GeV). Then
there is no renormalisable χ–SM coupling, the D104 fifth-force residue becomes Planck-suppressed (the h ≲ 0.08 bound is
no longer needed), and (b) improves to the gravity-only line.
Status: D80 is reduced to the field-dependent cosmological-constant problem (generic, open). Route taken for χ: gravitational
decay (option recorded; the matter-yield check at 0.8% heat — queued — covers it too).
D105 (c) refined. A minimally coupled scalar decays through gravity mainly into non-conformal scalars — here the Higgs
(4 real degrees of freedom); decays into fermions are suppressed by (m_f/m_χ)² and into gauge bosons by the trace anomaly.
With Γ = 4m_χ³/(32πM_P²) (Higgs): χ decays after Δφ ≈ 0.52 M_P, heat share ≈ 0.8% (0.8–1.1% over the decay-rate conventions), still
T_RH ≈ 4×10¹⁴ GeV. Decays into the gravity-only dark-matter fermion are suppressed by (m_DM/m_χ)² ~ 10⁻¹⁸ — no direct
overproduction. Open detail: χ's fermion partner also has to decay (e.g. to a Higgs and a light fermion, or a gravitino);
not worked out.

## Development 106 — a new gap: χ's fermion partner must decay, and that threatens the dark-matter count

Results: field_tests/results/chi_fermion.txt.
χ must be supersymmetric (D77), so it has a fermion partner χ̃ with the same growing mass g|φ − φ₀|. Instant preheating makes
fermions too (non-adiabatic production at the crossing is comparable to bosons). Gravity alone cannot make χ̃ decay (minimal
gravity conserves fermion number mod 2 per species, and with Hubble-induced splitting χ̃ is the lighter member), so without a
decay χ̃ — heavier and heavier along the roll — would come to dominate the universe. It therefore needs a Planck-suppressed
coupling to the Standard Model (e.g. χ̃ψH/M_P), which is fine for decay (rate ~m³/M_P²). But the same class of operators lets
χ̃ make gravity-only dark-matter pairs (three-body, branching ~(m_χ/M_P)²/64π² ~ 4×10⁻⁶), giving n_DM/s ~ 10⁻⁸ × (fermion share).
For 1×10⁸ GeV dark matter that overproduces by ~3×10⁷–3×10⁹ (fermion share 0.01–1).
Options: (i) a symmetry that forbids χ̃ → dark matter far below gravitational strength (needs a gauged symmetry, since gravity
breaks global ones); (ii) dark matter made this way instead of by freeze-in — the observed amount then needs m_DM ≈ 0.03–3 GeV
(fermion share 1–0.01), produced very relativistic but cold enough today (velocity ~10⁻¹⁰ c); this would replace the 10⁸ GeV
prediction; (iii) fermionic preheating strongly suppressed (not expected). None checked in detail.
Status: open, new. It touches the dark-matter prediction (D58/D85) and must be settled before that number is quoted firmly.

## Development 107 — related new work (Aug 2026) and the Twist's gravitational-wave propagation prediction

Gao, Wang, Garcia de Andrade et al., arXiv:2608.09487 (18 Aug 2026), promote the Barbero–Immirzi parameter to a dynamical
field in Einstein–Cartan–Holst gravity, couple it to a separate Ratra–Peebles quintessence field, and bound the resulting
gravitational-wave friction with dark sirens (GWTC-3: |ξ_BI| ≲ 0.7, |ξ_coup| ≲ 0.13; ET+CE forecast σ ~ 10⁻²). They use two
fields and do not discuss fifth forces; the Twist uses one field for both jobs, so this is related, not overlapping (to cite).
The Twist's own statement: in the Einstein frame the tail field does not multiply R, and the angle — the only part with a
Nieh–Yan coupling — is static today (D82), so the Twist predicts no extra gravitational-wave friction and no parity-violating
(birefringent) gravitational-wave propagation today: ξ = 0 in their language. Testable by ET+CE dark sirens at the ~10⁻² level.

**D106 developed — the graviton channel cannot be switched off.** Once χ̃ has any decay to Standard-Model fermions
(χ̃ → ψ + X), the same decay with a virtual graviton emitting a dark-matter pair (χ̃ → ψ + X + DM DM̄) is allowed whatever
symmetry the dark matter carries: the pair is neutral under any charge, and gravity couples to everything. Its branching ratio is
set by gravity alone, ~(m_χ/M_P)²/(several hundred) ≈ 10⁻⁶–10⁻⁵ at m_χ ≈ 0.05 M_P. So option (i) (a protecting symmetry) fails.
What remains: (ii) the dark matter is this decay product — a gravity-only fermion of roughly 10 MeV–10 GeV (the range covers the
fermion share and the branching-ratio uncertainty), born with energy ~m_χ/3 but redshifted to v ~10⁻⁹ c today, so cold; freeze-
in from the bath is then negligible (Ω ∝ m). Or (iii) fermionic preheating far below the bosonic one, which instant preheating
does not suggest. Leaning: (ii). Consequence if confirmed: the Twist's dark-matter prediction moves from ~10⁸ GeV (freeze-in) to
a light, gravity-only fermion of MeV–GeV mass, made non-thermally at reheating — still invisible to direct detection, but a
different number. Not adopted until the fermion share and branching ratio are computed; the reviewer guide flags the mass as
unsettled.
**D106 numbers (script theory/matter/dm_from_chi_fermion.py; results/dm_from_chi_fermion.txt).** Instant preheating makes χ's
scalar and fermion in equal numbers (same occupation, same mass). With χ → Higgs making the bath and χ̃'s own decay doubling it,
n_χ̃/s ≈ (3/8)T_RH/m_χ ≈ 1.2×10⁻³. The graviton-mediated branching to a dark-matter pair, (m_χ/M_P)²/(16π²C) with phase-space
factor C = 3–30, is 6×10⁻⁷–6×10⁻⁶. The observed dark matter then needs **m_DM ≈ 0.07–0.65 GeV** (70–650 MeV). This is the
Twist's dark-matter mass if D106 (ii) holds — about 10⁹ times lighter than the freeze-in estimate. Order of magnitude; the
gravitational four-body rate deserves a proper calculation before this becomes a stated prediction.

**Matter recheck, complete (11:03; results/kick_cliff_v2.txt).** Same script and settings (μ = 1, heat 0.13%, m_σ = 6×10⁹ GeV,
y = 0.1): old cliff 1.03×; reshaped cliff with m2 = 1: 0.887×; reshaped cliff with m2 = 4/π (the SU(8) value, D79): **2.29×**
(dilution 5.6). The m2 = 4/π version moves the cliff to slightly larger x (x_end 8.8×10⁻³ vs 7.0×10⁻³), where the kick term
e^{−(π/4)x} is the same but the inflaton is faster, and the yield rises by 2.6×. With yield ∝ m_σ^−0.89, exactly 1× needs
**m_σ ≈ 1.5×10¹⁰ GeV** for the adopted cliff (was ≈ 5–6×10⁹). Matter-making survives the reshaped cliff; only the hidden
mass shifts, by a factor ~2.5.
**D106 correction (11:08).** The branching ratio above was too big. The literature form for dark-matter pairs emitted by a
virtual graviton in a two-body decay (Zheng, arXiv:2208.05859, eq. 2.11 with M ≃ M_P) is BR = c̃(1/4π²)²(m_χ/4M_P)⁴ with
c̃ = O(1) — fourth power, not second. At m_χ ≈ 0.05 M_P: BR ≈ 1.8×10⁻¹¹ c̃, so n_DM/s ≈ 2×10⁻¹⁴ c̃ and the observed dark
matter needs **m_DM ≈ 2×10⁴ GeV / c̃ (2–200 TeV for c̃ = 10–0.1)**, replacing the 70–650 MeV of the first estimate. Freeze-in
then adds only ~10⁻⁴ of the abundance; the particles are born with E ~ m_χ/4 but are cold today (v ~ 10⁻¹⁶ c). So in this
route the Twist's dark matter is a gravity-only fermion of tens of TeV. Still an estimate (c̃ for this decay not computed).

## Development 108 — can n_s reach 0.974? Not with K = −3 ln(T + T̄): the measurement tests the "3" itself

Results: field_tests/results/ns_routes_d108.txt.
For any plateau reached exponentially — which is what the no-scale Kähler potential's order-2 pole gives — n_s ≈ 1 − 2/N
(here 0.9653 at the Twist's N* = 57.6; reshaping the potential, D66's α-deformation and kination change this only slightly).
Reaching 0.974 that way needs N ≈ 77 e-folds, which no reheating history allows. Polynomial α-attractors, whose plateau is
approached as a power (Kallosh & Linde, arXiv:2202.06492), give n_s = 1 − (2/N)(k + 1)/(k + 2): for k = 2, 1 − 3/(2N) = 0.974 at
N = 57.6 — exactly the ACT/SPT value. But those need a kinetic pole of a different order (q ≠ 2), i.e. a Kähler potential that is
not −3 ln(T + T̄), and that form is the base of the Twist (the Gates–Ketov–Yunes superfield and the slope √(2/3)).
Conclusion: there is no honest route inside the Twist to n_s = 0.974. If Simons Observatory confirms ~0.974, it would be
measuring a different pole order — the Twist's founding Kähler potential would be wrong, not just a parameter. This sharpens the
locked falsifier: n_s ≈ 0.973 (confirmed) rules out the no-scale base of the theory. Label: derived (standard results).
**D106 coefficient (11:25).** Zheng (arXiv:2208.05859, eqs. 3.2 and 3.4) gives the gravitational bremsstrahlung width as
Γ = C λ² m⁵/M_P⁴ with C ≈ 4.1–4.3×10⁻⁹ for fermion dark matter (from scalar or fermion plasma particles). Relative to the
two-body width λ²m/(8π) (or /16π) that is BR ≈ 1.1–2.1×10⁻⁷ (m_χ/M_P)⁴ ≈ 0.8–1.5×10⁻¹² at m_χ ≈ 0.052 M_P — i.e. c̃ ≈ 0.04–0.08
in the earlier form. Then **m_DM ≈ 2.5–5×10⁵ GeV (250–500 TeV)** in the χ̃-decay route. Remaining uncertainties: the fermion
share and m_χ at decay (BR ∝ m_χ⁴), each worth a factor of a few. Coverage and paper updated to "hundreds of TeV".

## Development 109 — the n ≈ 124 leads checked: no consistent identification

Results: field_tests/results/n_leads_check.txt. If the cliff depth were an instanton action, n = 2π/α would need α ≈ 1/19.7;
the MSSM unified value (~1/24.3) gives n ≈ 153, which misses today's dark energy by e^{−58}. Tying n to the hidden SU(8)'s
own cycle (D70, τ ≈ 27–37) gives n ≈ 170–232 for one instanton, or needs τ ≈ 158 for an SU(8) condensate — neither matches
the τ ≈ 30 the kick needs. Conclusion: D87's "α ≈ 1/20" and the SU(8) links do not survive a consistency check; n stays
**chosen**. Dropped as leads (kept on record).

## Development 110 — two refinements to the χ picture

(1) What "χ decays through gravity" means precisely. Pure graviton exchange cannot make a single χ decay: gravity couples to
the stress tensor, which is quadratic in χ around ⟨χ⟩ = 0, and the preheating coupling g²φ²χ² has a χ → −χ symmetry. So χ
(and χ̃) decay only through operators linear in χ, e.g. χ(∂H)²/M_P or χ̃ψH/M_P. Effective-theory reasoning expects such
Planck-suppressed operators (gravity is not expected to respect global symmetries), and with coefficients of order one they
give Γ ~ m_χ³/(8–32π M_P²), as used in D105. Stated as an assumption: the χ → −χ symmetry is broken at the Planck scale and no
gauge symmetry protects it. (If it were exact, χ would be stable and would come to dominate — excluded.)
(2) Fermion share confirmed. For a Yukawa-type mass m = g|φ − φ₀|, fermions crossing m = 0 get the same occupation as bosons,
n_k = e^{−πk²/(g|φ̇|)} (Greene & Kofman; Peloso & Sorbo), so a complex scalar (2 dof) and its Weyl partner (2 dof) are made in equal
numbers: the fermion share used in D106 (equal numbers) stands. With the decay coefficient range in (1), m_χ at decay is
0.052–0.074 M_P; BR ∝ m_χ⁴ then spans ×4, so the χ̃-route dark-matter mass is ≈ 100–500 TeV.

**D102 result (11:38): the hypothesis FAILS as stated.** The pre-registered check (angle_end_check.py; prediction written in
D102 before the run) gives, 11 e-folds after the end of inflation: x_end ≈ 145, **y_end = 15.40**, y mod 8 = 7.40. The stated
rule was "y mod 8 ≈ 4 survives, ≈ 0 fails"; 7.40 is 0.6 from 8 ≡ 0 and 3.4 from 4, so the reading is FAILS. What happened: the
kick did carry the angle past the barrier, but it kept turning — about two full periods — and stopped near a multiple of 8, not in
the y = 4 valley (the valley's pull has faded by the time the angle slows: the potential has dropped ~10⁻⁸⁰ through the cliff).
Under the direct mapping 1/γ = y this gives γ ≈ 0.065, not 0.25. (On the far tail the angle's restoring force is not periodic,
so y = 15.4 is not equivalent to 0; either way it is not 4.) Matter yield in the same run: 2.29× (as in the matter recheck).
Status: the γ = 0.25 route is closed; the LQG mismatch (D83) stands as an open problem.

## Development 111 — a new gap: slow gravitinos at the cliff

Literature: Kolb, Long & McDonough (arXiv:2102.10113) found "catastrophic" production of the helicity-½ gravitino when its sound
speed c_s vanishes; later work (e.g. arXiv:2104.03749, "Slow and safe gravitinos") shows unconstrained superfields are protected by
goldstino–inflatino mixing, and that the danger is confined to doubly constrained (orthogonal) set-ups; a model with an unconstrained
stabiliser S and a quartic Kähler term was found safe (its F-term is not suppressed).
The Twist: S is unconstrained with the quartic term (D72) — the protected class. But two features are specific: W = 0 along S = 0, so
m₃/₂ = 0 throughout; and the inflaton's own F-term vanishes (F_T = 0), so φ̇·F* = 0 holds identically and c_s² reduces to (p/ρ)²,
which passes through zero once, where kinetic and potential energy are equal — at the cliff, as w goes from −1 to +1. One crossing
(not repeated oscillations) limits the effect, and the mixing argument should apply, but neither has been checked for this
superpotential. If longitudinal modes were made efficiently they would be light fermions (m₃/₂ ≈ 0) — extra radiation (N_eff) — or
contribute to the dark-matter question (D106).
Status: open, new; a dedicated calculation (the helicity-½ mode equation through the cliff) is the check.
**D111 worked out (11:45; results/gravitino_cliff.txt).** With m₃/₂ = 0 and F_T = 0, the Kolb–Long–McDonough sound speed is
c_s² = 1 − 4|φ̇|²|F|²/ρ² = (p/ρ)², zero once at the cliff. For unconstrained superfields (the Twist's case) Dudas et al.
(arXiv:2104.03749) show that when c_s → 0 the longitudinal gravitino becomes mostly inflatino and the physical eigenmodes do not
slow down: production is that of ordinary fermions at gravitational strength, not UV-catastrophic. Here the fermions are the T̃–S̃
pair, which get a Dirac mass from W_TS = √3 m F′(T) (inflaton-scale on the plateau, ~e^{−n}m — negligible — on the tail). Made once
at the crossing with H ≈ 1.5×10¹³ GeV, their energy share is ~(H/M_P)² ≈ 4×10⁻¹¹, i.e. ~5×10⁻⁹ of the radiation: ΔN_eff ~ 3×10⁻⁸
(bound ~0.3). Resolved (estimate, by the published result for this model class); no dark-matter or N_eff consequence.

## Developments 112–117 — the remaining gaps, one by one (11:45–12:05; results/gaps_d112.txt, cc_field_dependent_d116.txt)

**D112 — dark-matter mass settled (conditional).** Freeze-in from the bath and bremsstrahlung in χ̃ decays make the *same*
gravity-only particle, and neither yield depends on its mass (m_DM ≪ T_RH, m_χ), so the yields add: 1/m = 1/m_freeze-in + 1/m_brems.
At 0.8% heat (freeze-in alone ≈ 0.5–2.6×10⁸ GeV, scaled from dm_kination.txt), bremsstrahlung supplies ≥ 99% of the dark matter and
**m_DM ≈ 100–500 TeV**. The 10⁸ GeV value is only the fallback if χ̃ has no decay to Standard-Model fermions (D106 (ii) fails) —
which D110's Planck-scale breaking of χ → −χ makes unlikely. Status: unsettled → derived-conditional (fermion DM; estimate).

**D113 — field distance, with a timeline.** Reshaped cliff, heat 0.8%: CMB point → end of inflation 5.1 M_P; end → frozen
11.0 M_P (x frozen ≈ 73); total ≈ **16 M_P** (replaces the ~19–21 M_P of D75, which used the old cliff). Most of it is crossed in
the first ~5 e-folds after inflation, while the bath is hot (T ≈ 10¹²–10¹⁴ GeV). Distance-conjecture test: a tower with mass
M_P e^{−λΔφ} (taking it at M_P at the CMB point) stays above the bath temperature for λ = 1/√2 (the sharpened bound) and
λ = √(2/3) (natural for this Kähler potential; margin ~5× at N ≈ 3), but falls below it for λ = 1 at N ≈ 3 (1.0×10¹³ vs
2×10¹³ GeV). If the tower starts below M_P (e.g. string scale ~10¹⁷ GeV), λ = √(2/3) also crosses. Status: open, now
quantitative — survives for λ ≤ √(2/3) with a tower near M_P; fails otherwise.

**D114 — initial conditions.** Starts on the plateau with any kinetic share: from rest anywhere up to p₀ = −13 (2 M_P above
the CMB point) gives ≥ 300 e-folds and the CMB point is crossed on the attractor (v/v_sr = 0.994). A kinetic-dominated start
(ρ/V = 100–10⁴, moving toward the cliff) overshoots if it starts within ~3–4 M_P of the CMB point (p₀ = −13: only 11–44
e-folds, off attractor ×50–110), but works from p₀ ≤ −16 (≥ 107 e-folds, on attractor). Moving up the plateau is always fine.
Kination overshoot distance ≈ ln(ρ₀/V)/√6, so a Planck-density kinetic start needs p₀ ≲ p* − 10 ≈ −21: the plateau is
unbounded, so this is generic. Not addressed: inhomogeneous starts (a patch ≳ H⁻¹ must be smooth — the standard plateau critique).
Status: homogeneous initial conditions generic (derived numerically); inhomogeneity open (generic to plateau models).

**D115 — c̃ (bremsstrahlung coefficient) already pinned.** The 11:25 Zheng value (C ≈ 4.1–4.3×10⁻⁹, i.e. c̃ ≈ 0.04–0.08)
stands. What remains is a factor-2 width normalisation (8π vs 16π) and the m_χ⁴ spread (×4), both inside the 100–500 TeV range.
No further work possible without the full χ̃ → ψH + graviton matrix element.

**D116 — the field-dependent vacuum-energy problem, quantified (rough).** χ's mass depends on the inflaton; χ and χ̃ cancel
in loops except for their splitting, and the Planck-suppressed links to the non-SUSY Standard Model that D110 needs split them by
δm² ~ Λ⁴/(16π² M_P²). Then δV(φ) ~ m_χ(φ)² δm²/(16π²) ≈ 10⁵ GeV⁴ (SM loops only to 1 TeV) up to 10⁶¹ GeV⁴ (to 0.05 M_P):
**10⁵²–10¹⁰⁸ × ρ_DE.** Possible protection checked: if χ's inflaton dependence ran through the SU(8) factor e^{−πT/4}, it would
switch off on the tail, but that needs x ≳ 150–320 and the field freezes at x ≈ 73 — **fails**. Status: open, and now the
sharpest weak point: the χ sector must decouple from the tail by ~10⁻⁵² or better (e.g. preheating via a different field, or
χ's mass not depending on the tail direction). Same problem every quintessence model with couplings has (Kolda & Lyth 1999).

**D117 — γ mismatch and the SU(8) construction: what would be needed.**
(a) γ: D102 closed the y = 4 route. Three routes left, none tested: (i) the Twist's γ is a running/field value and the
black-hole-entropy γ (0.2375 or 0.274 by counting scheme) is a separate, Planck-scale quantity — consistent but drops the link;
(ii) the self-dual choice γ = ±i with analytic continuation (Frodden, Geiller, Noui & Perez 2012) reproduces Bekenstein–Hawking
without fixing a real γ, which removes the entropy constraint; (iii) a different map from y to γ. Status: open, choice not data.
(b) SU(8): the 4/π in the cliff equals 2π/8, which is what an SU(8) gaugino condensate with gauge function f = T gives
(W ∝ e^{−2πT/8}). But the Twist uses that factor *inside* an exponent, exp(−n(1 − e^{−πT/4})), which a single condensate does
not give. A construction needs: an SU(8) sector with f = T; a second sector whose gauge function contains the SU(8) condensate
(f₂ ∝ n(1 − e^{−πT/4})) so that its condensate supplies the outer exponential; n ≈ 125 still chosen (D109). Status: requirements
written; not constructed.

## Developments 118–120 — working the open items (12:00–12:15)

**D118 — a fix for D116: χ's mass saturates (results/chi_saturating_d118.txt).** Replace the linear preheating mass
m_χ = g|φ − φ₀| by a holomorphic, saturating one: W ⊃ (h/2)(1 − e^{−2π(T−T₀)}) χ². Since χ = 0 during inflation this term does
not touch V(T). m_χ vanishes at x₀ (instant preheating as before), grows almost linearly just after, and tends to h on the tail,
where its leftover dependence on the tail field is ∝ e^{−2πx}. Matching D105's slope g = 0.1 at the crossing (x₀ = 0.02–0.1 gives
h = 0.2–1.0 M_P), χ reaches its decay mass 0.052 M_P after Δφ = 0.44–0.49 M_P (D105: 0.52) — heat share ~0.65–0.75% instead of
0.77%, within the matter check's range. During inflation |m_χ| ≤ 0.13–0.17 M_P ≫ H, so χ stays put. On the tail (x ≈ 73):
**field-dependent vacuum energy 10⁻¹⁴⁵ (SM loops to TeV) to 10⁻⁸⁸ (to 0.05 M_P) × ρ_DE** — D116's 10⁵²–10¹⁰⁸ removed. The
constant part (~h²δm²/16π²) joins the ordinary cosmological-constant problem (tuned, as in every model).
Costs: (i) a new assumption — a single-instanton factor e^{−2πT} of the same T (action 2π Re T; the cliff's SU(8) factor is
e^{−2πT/8}); (ii) e^{−2πT} has Im T period 1, so m_χ at the crossing is 2h|sin πy|: preheating needs y close to an integer when the
field crosses x₀ (y ≈ 0 at the end of inflation; to be checked against the two-field run); (iii) the faster-than-linear growth
shifts χ's decay slightly earlier (above). Status: D116 → candidate fix (estimate), with one new assumption.

**D119 — a construction route for the cliff's double exponential.** A second hidden gauge group G₂ (rank N₂) whose gauge
function picks up the SU(8) condensate through the Planck-suppressed mixed operator ∫d²θ (c/M_P³) Tr W₈² Tr W₂²: when SU(8)
condenses, ⟨Tr W₈²⟩ ∝ M_P³ e^{−2πT/8}, so f₂ = f₀ − κ e^{−πT/4} with κ = c × O(1). G₂'s condensate is then
Λ₂³ ∝ e^{−2πf₂/N₂} = e^{−2πf₀/N₂} · exp(n e^{−πT/4}) with **n = 2πκ/N₂**. The constant e^{−2πf₀/N₂} only rescales m, so the cliff
depth is n — no tuning of f₀ against κ is needed (only f₀ > κ for weak coupling). n ≈ 125 needs κ ≈ 20 N₂ (c ~ 40–160 for N₂ =
2–8): a large coefficient, so n is still chosen — now as c. Not yet shown: how Λ₂³ enters W multiplied by S·T/√(1+T/μ) (needs G₂
matter whose masses involve S and T), and the SU(8) sector being strongly coupled near x → 0 (the plateau) is outside control.
Status: route written; partly constructed; n relocated, not explained.

**D120 — the γ mismatch: route chosen.** Of D117's three routes, (ii) is the only one that removes the conflict rather than
renaming it: with the self-dual value γ = ±i and analytic continuation, black-hole entropy comes out as Bekenstein–Hawking for any
area (Frodden, Geiller, Noui & Perez, arXiv:1212.4060), so the entropy calculation no longer fixes a real γ, and the Twist's field
value (whatever y settles at) is not contradicted. Cost: the Twist's γ is then a cosmological field unrelated to the LQG area
spectrum, and the "LQG link" becomes motivation only (as COVERAGE already lists for quantum geometry). Status: open mismatch →
resolved by choice (labelled as such), not by derivation.

**D121 — D118's condition checked: PASSES (results/crossing_angle_d118.txt; theory/matter/crossing_angle_d118.py).** Two-field run
with the matter-check settings (exp cliff 4/π, heat 0.8%), traced for 2 e-folds after inflation: the field passes x = 0.02–0.1
between 0.4 and 1.2 e-folds after the end, and the angle is still |y| < 5×10⁻⁵ there (the kick that later carries it to y ≈ 15
comes afterwards). So the saturating mass's minimum at the crossing is 2h|sin πy| ≤ 3×10⁻⁴ h ≤ 3×10⁻⁴ M_P, below the
non-adiabatic window √(g φ̇) ≈ 5×10⁻⁴ M_P: instant preheating proceeds as with the linear mass. (Upper bound from the printed
precision; the true |y| is smaller.) D118 stands as a candidate fix with one new assumption.

**D122 — inhomogeneous starts: placed in the literature (not simulated).** Numerical-relativity studies of inflation from lumpy
initial data (Clough et al., arXiv:1608.04408; Aurrekoetxea, Clough, Flauger & Lim, arXiv:1910.12547) find convex potentials
robust and concave (plateau) potentials robust when the potential varies on super-Planckian scales, much less so on sub-Planckian
ones. The Twist's plateau departs from flat as x = e^{√(2/3)φ}, i.e. on the scale √(3/2) M_P ≈ 1.22 M_P — the same scale as
Starobinsky's, the super-Planckian case — and is unbounded upward (D114), so a lumpy patch can start far from the CMB point.
By analogy with those results the Twist sits in the more robust plateau class; the cliff is ~5 M_P below the CMB point, so it
plays no role at the start. Status: open, generic → "robust by analogy with published simulations (not run for the Twist)".

**D123 — which λ for the field distance (results/tower_volume_d123.txt).** If T behaves like a volume-type modulus (the
K = −3 ln(T + T̄) form), the tower is Kaluza–Klein modes, m ~ M_P/x for x > 1 (λ = √(2/3)), and, by T-duality, winding modes
m ~ M_P x for x < 1 (assumption; O(1) factors dropped). Along the Twist trajectory: tower/H = 20 at the CMB point, 1400 at the end
of inflation; after inflation the smallest tower/T is 76 (right at the end), then 10³–10⁶; today (x ≈ 73) the tower is
~3×10¹⁶ GeV. **Passes everywhere on the observed history.** But it puts a floor on the plateau: the tower drops to H at
x ≈ H/M_P ≈ 6×10⁻⁶ (p ≈ −14.7), so the far plateau is outside the EFT. That clashes with D114: kinetic-dominated starts needed
p₀ ≲ −16. Under this assumption only near-rest starts in p₀ ≈ −14.7 … −11 are inside the theory (≥ 300 e-folds from rest there);
fast starts are not. Status: field distance — passes (with the volume-modulus assumption); initial conditions — narrowed.

**D124 — the 0.8%-heat matter check: prediction MISSED (results/matter_h005_check.txt).** Pre-registered prediction 2–3× at
m_σ = 6×10⁹ GeV; result **7.53×** (entropy dilution ×1.84 instead of ×5.6 at 0.13%: more heat, less dilution by the hidden field's
decay). The angle ends at y = 1.21 (vs 15.4 at 0.13% heat). Refit with yield ∝ m_σ^−0.89 → **m_σ ≈ 5.8×10¹⁰ GeV**, a ~10× extrapolation
of the scaling law, so a confirmation run at 5.8×10¹⁰ GeV was locked (matter_refit_check.py, prediction 0.6–1.6×) before running.
Note: with D118's saturating χ mass the heat share is ~0.65–0.75%, slightly lower.

**D125 — the tail at the D105 heat share (results/tail_at_08_d125.txt).** Reshaped cliff, heat 0.01 / 0.13 / 0.65 / 0.8%: the field
freezes at x ≈ 5800 / 446 / 89 / 73 and today sits at x ≈ 7100 / 547 / 110 / 89, but the late-time curve barely moves:
**w0 = −0.899 … −0.902, wa = −0.146 … −0.142.** The dark-energy prediction is insensitive to the heat share (the leftover slope
dies like e^{−πx/4}, so where the field freezes hardly matters once the tail thaws). Today's x ≈ 89 (not 73) used in D116/D118
changes nothing: the e^{−πx/4} switch-off still fails (needs ≳ 150), the saturating mass gains margin.

**D126 — D119 completed: how the condensate enters W as S·T·(…) (results/racetrack_d126.txt).** Take two copies of G₂ (rank N₂)
exchanged by a Z₂ under which S → −S, with gauge functions f_± = f₀ − κ e^{−πT/4} ∓ a S T (holomorphic; the e^{−πT/4} piece from
the SU(8) condensate as in D119). Their condensates form a racetrack:
W = A[e^{−b f₊} − e^{−b f₋}] = 2A sinh(b a S T) e^{−b f₀ + n e^{−πT/4}} ≈ 2A a b e^{n − b f₀} · S · T · exp(−n(1 − e^{−πT/4})),
b = 2π/N₂, n = bκ. So: (i) W is odd in S and vanishes at S = 0 — the property the Twist assumed (m₃/₂ = 0, D111) is now protected by
the Z₂; (ii) the S³ terms vanish with their first two derivatives at S = 0, so they change neither V nor m_S²; (iii) the factor S·T
comes out of the expansion of sinh; (iv) the inflaton mass is a gauge-coupling hierarchy: √3 m = 2Aab e^{−b(f₀ − κ)}, and
m = 2.1×10⁻⁵ M_P needs b(f₀ − κ) ≈ 9–13 (for Aab = 0.1–10), i.e. 1/g₂² ≈ 3–17 at T → 0 (α₂ ≈ 0.005–0.03, weakly coupled) — the
plateau scale is explained by a perturbative coupling, not put in by hand. Left over: the 1/√(1 + T/μ) factor (must come from the
prefactor A(T) — e.g. a one-loop threshold — not derived), κ ≈ 20 N₂ (n still chosen, D119), and the SU(8) sector is strongly
coupled near x → 0. Status: SU(8)/cliff construction → mostly constructed (two pieces open).

**D127 — the 1/√(1 + T/μ) factor moved into the Kähler potential (results/kahler_sqrt_d127.txt).** Instead of the superpotential
(where it would need a negative-power threshold), put it in S's kinetic term:
K = −3 ln(T + T̄ − SS̄(1 + (T + T̄)/(2μ)) + ζ(SS̄)²) ≈ −3 ln(T + T̄) + 3SS̄[1/(T + T̄) + 1/(2μ)] + … —
i.e. S's metric is the no-scale piece plus an ordinary constant (canonical) piece. At S = 0, K^{SS̄} gains 1/(1 + x/μ), so with
W = √3 m S T cliff(T) (exactly D126's racetrack form, no prefactor function needed):
V = m²|T cliff(T)|²/(4x²(1 + x/μ)) — **identical to the old potential for real T**, so inflation (n_s, r, N*), the cliff, the tail
(w0, wa) and every fit are unchanged. Only the angle direction differs: m_y²/H² is the same to 4 digits through inflation
(+8.000 at the CMB point) and at the cliff (−274 vs −273 at x = 1), and today (x ≈ 89) is +8.0 instead of +4.1 — the angle stays
heavy either way. Open check: the S mass on the tail with the new metric (rough estimate: ζ-term still dominates, S stays heavy).
Status: the 1/√ factor → derived from a natural Kähler term; D126 + D127 give the whole W = √3 m S F(T) from a Z₂ racetrack except n.
**D127 check — S stays heavy (results/s_mass_d127.txt; full two-field F-term potential, ζ = 3×10⁴).** m_S²/H², old vs new metric:
CMB point 29.2 / 29.2 (matches −2 + 8ζx); x = 0.01: 2402 / 2355; x = 1: 2.5×10⁵ / 6.8×10⁴; today (x = 89): 2.1×10⁷ / 2.6×10³. The new
constant term weakens S's mass on the tail by ~10⁴ but S remains ≫ H everywhere, so it stays at S = 0. (Today m_S ~ 50 H₀ is
cosmologically light, as before; S = 0 is protected by D126's Z₂, so S has no linear coupling to anything — no fifth force.) Passes.

**D128 — can D118's new factor come from a gauge theory? (results/chi_su2_d128.txt).** D118 used a single-instanton factor
e^{−2π(T−T₀)}. A gaugino condensate of SU(N) with f = T gives e^{−2πT/N}. Checked at x = 73 (field leaves its frozen value during
the late thaw) and 89 (today), worst case SM loops to 0.05 M_P: single instanton ≤ 10⁻⁸⁹ ρ_DE (passes); **SU(2), e^{−πT}: up to
~10¹¹ ρ_DE at x = 73 — passes only if SM loops are cut off below ~10¹⁶ GeV** (at x = 89 it passes fully); SU(3): 10⁴⁴ (fails).
So the fix needs either a stringy (single) instanton, or an SU(2) condensate plus an SM cutoff under ~10¹⁶ GeV. Status: D118's
assumption narrowed to two options; preheating/decay numbers unchanged (Δφ 0.44–0.49 M_P).

## Developments 130–131 — the two data gaps (12:20)

**D130 — the reshaped cliff already has a locked out-of-sample test.** Its late-time curve (w0 −0.902, wa −0.142 at 0.8% heat;
−0.899…−0.902 over all heat shares, D125) coincides with PURE-TWIST's (w0 −0.900, wa −0.143), which WATCH-PURE-DR3 locked on
12 Nov 20:59 before any post-DR2 data. So DESI DR3 (and the next independent BAO survey) tests the reshaped model fairly, even
though the reshape itself was post hoc. No new lock needed; stated in the model card.

**D131 — n_s against the CMB-SPA data: the locked test is running; what is known so far.** Published: P-ACT-LB n_s = 0.9752 ±
0.0030, CMB-SPA + DESI 0.9728 ± 0.0027, CMB-SPA alone 0.9684 ± 0.0030 (arXiv:2510.18656, ΛCDM). The Twist gives 0.964–0.968
(instant reheating to kination with loops). Naively that is ~1σ from CMB-SPA alone but ~2–3σ once DESI BAO is added. One hope
was that the Twist's own dark energy (w0 ≈ −0.90) would remove the BAO-driven shift, since those published numbers assume ΛCDM.
The finished leg of the locked NS-SPA test (PURE background, n_s free; PC, 11:08) says it does **not**: its minimiser runs land at
n_s ≈ 0.973–0.976. The locked reading (fixed n_s = 0.964 vs free) is still running (PURE_FIXED, run 3/4); a rough expectation from
the widths is a cost of ~9–12 in χ² at 0.964 (the TENSION/INCONSISTENT border) and ~4 at 0.968 — expectation only, the locked
number decides. If INCONSISTENT: the D108 falsifier is effectively met by current data, and the only escapes on file are a
polynomial attractor (contradicts K = −3 ln, D108) or a larger N* (more kination than D84 allows).
D131 add: with this plateau (n_s ≈ 1 − 2/N*) reaching 0.973 needs N* ≈ 74 (0.968 → 63; 0.975 → 80), i.e. 15–20 more e-folds than
D84's kination gives (+1.9); a stiff phase cannot supply that (the usual upper bound is N* ≈ 60–63). That escape is closed.

**D132 — can the n_s problem be fixed inside the model? Checked; no.** (i) Any plateau that approaches flat as 1 − A e^{√(2/3)φ}
gives n_s ≈ 1 − 2/N* whatever A is: μ, the cliff's own x and x² terms (already in the numbers) and α in K = −3α ln all leave it.
(ii) Kination: at the 0.8% heat share it adds ΔN ≈ (1/12)·3 ln(1/f) ≈ 1.2 (not D84's 1.9), so n_s is ~0.965, slightly lower.
(iii) Heavy fields (S at 30 H², the angle at 8 H²) change n_s negligibly; loops +0.002 are already in the 0.965–0.968 range.
(iv) Only a different approach to the plateau (polynomial, D108) raises n_s, and that means a different Kähler potential — a new
model. Changing the model now, against the very data that shows the problem, would be fitting to the result; if pursued, it must
be written and locked as a new model and tested on data it has not seen. Context (not a fix): the high n_s comes mostly from
adding DESI BAO to the CMB; CMB-SPA alone gives 0.9684 ± 0.0030, ~1σ from the Twist, and the authors of arXiv:2510.18656 note
the shift may reflect a BAO/CMB tension. Status: wait for the locked NS-SPA reading; report it at full size.

## Development 133 — a new model, TWIST-P (locked 12:23, PREREG_TWISTP.md, sha256 c7fcb64f…)
Built on Danny's word after D131/D132 (so its agreement with current data is not evidence). Extra Kähler term β/(T + T̄) — a
pole of order 3 that dominates only deep on the plateau (polynomial attractor there) — with S's metric scaled by e^{β/u} so the
potential along real T is exactly the Twist's (checked in full SUGRA). Results (theory/twistp/, results/twistp_*.txt): n_s rises
with β but saturates at 0.9713 (β ≈ 0.02–0.05) because the cliff's steep linear term (~nπ/2 · x) ends the plateau first; it never
reaches 0.974. Self-consistency limits: the angle's mass falls as m_y² = 8H²/(1 + β/3x*), heavy (> 9/4 H²) only for β ≤ 2.2×10⁻³;
S fails for β ≳ 0.04. Locked segment: n_s 0.965–0.969 (+ loops ≤ 0.972) with r 0.0036–0.0052, rising together — a joint n_s–r
test for SO/LiteBIRD/CMB-S4. Honest size of the gain: at most ~+0.004 on n_s inside the allowed range; vs today's P-ACT-LB
0.9752 ± 0.0030 that is ~2σ instead of ~3σ — a partial relief, not a fix.

**D134 — isocurvature from light spectators (both models; results/isocurvature_check.txt; estimate).** Bound used: uncorrelated
CDM-equivalent isocurvature P_S/P_ζ < ~0.04 → baryon S_B < 5×10⁻⁵. (a) The angle: its quantum kick at the CMB point is δy ≈
(H/2π)/√(2K_TT̄) ≈ 1–2×10⁻¹⁰ for β = 0 … 0.022 (the large kinetic metric at small x makes it tiny), so even TWIST-P's light-angle
range gives S_B ≲ 2×10⁻¹⁰ — safe by 10⁵. (b) A gap in BOTH models, now checked: the hidden axion σ (m_σ ≈ 6×10¹⁰ GeV ≪ H) is
light during inflation; δσ/σ₀ = (H/2π)/(f M_P) ≈ 10⁻⁵ for f = 0.1, and with dlnY/dlnσ₀ ≈ cot(1) ≈ 0.64 for the kick force,
S_B ≈ 6×10⁻⁶ — safe by ×8 (×4 at f = 0.05, ×24 at f = 0.3). Order of magnitude; the yield's true sensitivity to σ₀ was not run.
A prediction follows: baryon isocurvature at the 10⁻⁶–10⁻⁵ level, below current reach.

## Developments 135–137 — corrections after the independent referee review (13:05; full report in the session)

**D135 — the fifth force is reopened as the main open problem.** The referee is right that D104 and D110 are inconsistent.
D110 argues that gravity generically produces Planck-suppressed operators linear in χ (so χ can decay). The same reasoning
produces operators linear in the tail field, (φ/M_P)·O_SM, with O(1) coefficients — a coupling β = O(1), against Cassini's
β² < ~10⁻⁵. "SM outside SUGRA, minimally coupled" (D104) does not forbid them; it simply sets them to zero. So either (i) an
unexplained symmetry forbids every φ–SM coupling while allowing χ–SM ones (none is known: Re T has no shift symmetry), or (ii) the
fifth force is real. Status: main open problem (as before D104); assumption 1 is relabelled "unexplained symmetry required".

**D136 — labels corrected.** (a) 4/π: "assumed (SU(8) form)", not "derived" — with f = T the SU(8) coupling g² = 1/x is 10²–10⁴
through the whole inflationary region, so the condensate formula is outside control there. (b) The inflaton mass: "related to a
gauge coupling", not "explained" — b·f₀ ≈ 134 must sit ≈ 9 above b·κ = 125 (a ~7% cancellation). (c) n: a tuning of ρ_DE
(n = 124.6 reproduces ρ_DE at x = 89; Δn ≈ 0.35 per factor 2). Single value used everywhere: n ≈ 125. (d) Isocurvature (D134):
"unverified" until D137. (e) Initial conditions (D114): fast starts are excluded — they begin at x ≈ 2×10⁻⁶, where S is tachyonic
(m_S²/H² = −2 + 8ζx < 0 for x < 8.3×10⁻⁶) and below the tower floor (D123). Only near-rest starts in x ≈ 10⁻⁵–10⁻⁴ remain.
(f) Matter (m_σ) and dark matter (100–500 TeV) are removed from the predictions table until they stop moving. (g) Kination ΔN at
0.8% heat is 1.2 (D132), not 1.9; consistency_v5's quoted "+1.9" is superseded. (h) The late-time test is generic thawing
quintessence with λ = √(2/3); the supergravity structure plays no role in it — stated plainly. (i) DR3 is cumulative with DR2, so
WATCH-PURE-DR3 is not fully out of sample; its reading is weaker than a fresh survey's.

**D137 — the yield's sensitivity, locked before running (field_tests/missing_piece/yield_sensitivity.py).** Prediction
written first: |dlnY/dlnσ₀| ≤ 5 and |dlnY/dy₀| ≤ 10⁴. (The isocurvature bound S_B < 5×10⁻⁵ allows |dlnY/dlnσ₀| up to 5 for
δσ/σ₀ ≈ 10⁻⁵, and |dlnY/dy₀| up to 2.5×10⁵ for δy ≈ 2×10⁻¹⁰; the y prediction is set stricter, at 10⁴.) If a bound is exceeded, D134 fails for that source.

## Development 138 — geometry already inside the Twist (Danny's question, 13:14: "find geometric shapes that fit our numbers")
Checked which geometric structures are genuinely present, as opposed to number coincidences.
**Genuine (follow from the model's equations):**
(1) The inflaton's field space is a hyperbolic disk (Poincaré disk, SU(1,1)/U(1)): K = −3 ln(T + T̄) gives constant negative
curvature R = −2/(3α) with 3α = 3. The plateau, n_s ≈ 1 − 2/N and r ≈ 12α/N² all come from the disk's boundary.
(2) That disk is one rung of the "seven-disk" ladder from maximal (N = 8) supergravity / M-theory (Ferrara, Kallosh & Linde,
arXiv:1610.04163; Kallosh, Linde, Wrase, Yamada, arXiv:1704.04829): seven complex scalars whose geometry, built on the
seven imaginary octonions (the Fano plane's 7 points and 7 lines), allows only 3α = 1, 2, …, 7. The Twist sits at 3α = 3.
Its r = 0.0036 at N* ≈ 56 matches that rung (12α/N² ≈ 0.0039). So the Twist's Kähler potential is one of seven discrete,
geometrically allowed shapes — not a free choice. (Whether 3α = 3 means "three disks merged along a Fano line" is suggestive
but not checked here.)
(3) The hidden SU(8) that gives the cliff's 4/π = 2π/8 is the same group as the maximal compact subgroup in N = 8
supergravity's scalar manifold E7(7)/SU(8) (70 scalars). The Twist's two pieces — the disk and SU(8) — both point at the same
parent geometry. Suggestive, not derived.
(4) The cliff makes Im T periodic with period 8 (an 8-fold rotation, Z₈); the D126 racetrack adds a mirror Z₂ (S → −S).
**Consequence for TWIST-P:** its extra term β/(T + T̄) adds a pole of order 3, so its field space is no longer a hyperbolic disk —
it leaves the seven-disk ladder. The geometric picture favours the original Twist over TWIST-P.
**Not found / not claimed:** no geometric meaning for n ≈ 125, m_σ, y_end, or 0.8%; bound states of particles "joining into
shapes" are not something these equations compute.
**Testable:** the seven rungs predict r ≈ 0.0011·3α at N ≈ 57 — LiteBIRD/CMB-S4 can tell rung 3 (the Twist) from its
neighbours 2 and 4 only marginally (Δr ≈ 0.0012 against σ(r) ~ 0.001).

**D139 — the Twist's history as a disk, a cusp and a 2-torus (Danny's picture: "Metatron's cube … pressure out of the centre …
toroid … tesseract"; theory/geometry/q_disk.py, results/q_disk.txt, q_disk.png).** Calculated, not imagined:
(1) In the cliff's own variable q = e^{−πT/4} the period-8 angle closes, so the field space is exactly the unit disk once round:
rim |q| → 1 = the inflation plateau (CMB scales at |q| = 0.9999, end of inflation 0.990), centre q → 0 = the dark-energy tail
(|q| ≈ 10⁻²⁵ frozen, 5×10⁻³¹ today). The whole history is one inward spiral, rim → centre, turning by arg q = −πy/4 (about −54°
for y ≈ 1.2 at 0.8% heat). The potential falls by e^{2n} ≈ 10¹⁰⁹ from rim to centre; the centre holds today's dark energy, a
NEGATIVE pressure (p = −0.90ρ) — the "pressure at the centre" in the picture, though it pulls the expansion outward rather than
radiating out.
(2) The kinetic metric in q, ds² = 3|dq|²/(|q| ln|q|²)², is a hyperbolic disk with a cusp at the centre (pseudosphere/horn
geometry): both the rim and the centre are infinitely far away — the history runs between two boundaries at infinity.
(3) With S, the field space has 4 real dimensions and two angles (arg q, arg S): a 2-torus over a 2-d base — a genuine toroidal,
four-dimensional structure. It is not a tesseract (a tesseract is a 4-d cube; the 4-torus would need all four directions
periodic; here only two are).
(4) Not found: no 13-circle (Metatron's cube) or 12-around-1 structure appears in any equation; nothing in the model computes
the shape of bound particles. Recorded as interpretation, not prediction.

**D140 — constructed and tested: the "scaling shield" against the fifth force (theory/darkenergy/scaling_shield_d140.py;
results/scaling_shield_d140.txt).** Construction: K = −3 ln(T + T̄) has the no-scale scaling symmetry T → λT; put the SM in
sequestered (Einstein-frame minimal) form so its couplings respect it; χ carries no scaling charge, so its Planck links to the SM
stay allowed (D110) — the χ/φ asymmetry D135 needed now comes from a named symmetry. A φ–SM coupling then needs a source that breaks
the scaling. Tested against Cassini (β < 3.4×10⁻³) and MICROSCOPE (β < ~1.2×10⁻⁶) at x = 73 and today's 89:
(a) instanton breaking ∝ q^k (the cliff's own e^{−πT/4}): β ≈ 3×10⁻²⁹ — passes by 10²³; (b) D118's e^{−2πT}: passes by 10²³⁴;
(d) the superpotential's breaking reaches the SM only via gravity, β ~ 10⁻¹²⁰ — passes; (c) **perturbative breaking ∝ c_p/x^p
decides it**: p = ½ or 1 fails Cassini even for c_p = 1; p = 3/2 (the α′³ form in string theory) passes Cassini but needs
c_p < 8×10⁻⁴ for MICROSCOPE; p = 2 needs c_p < 6×10⁻³; p = 3 passes with c_p < 0.3. Status: fifth force → **conditional**:
safe if the scaling symmetry is broken only non-perturbatively, or perturbatively at order ≥ 1/x³ (or ≥ 1/x^{3/2} with a
coefficient below 10⁻³). The open question is now precise: which perturbative corrections the SM–T sector has.

**D141 — correction to D140, and the literature (13:30).** (1) With the scaling symmetry alone, couplings g(y/x)·O_SM are allowed
(y/x is invariant); today y/x ≈ 0.013 gives β ≈ 0.011 g′ — Cassini needs g′ < 0.3, MICROSCOPE g′ < 10⁻⁴: fails for g′ ~ 1. The
shield needs BOTH isometries of the disk — the scaling T → λT and the axion shift T → T + ic — which together act transitively,
so no invariant function of T exists and every φ–SM coupling must break one of them. The cliff breaks the shift only through
q = e^{−πT/4}, so D140's (a) numbers stand for the combined construction; (c) (perturbative 1/x^p breaking) still decides it.
(2) Literature: the general idea — approximate global symmetries suppressing quintessence couplings to matter — is Carroll's
(1998, "Quintessence and the rest of the world"). Burgess, Quevedo and collaborators (arXiv:2111.07286, 2212.14870) study the
no-scale scaling symmetry in detail and find that in string constructions matter generically couples to the dilaton at LEADING
order (Brans–Dicke-like, too large), because matter masses scale with the extra-dimensional size; they need other mechanisms
("axion homeopathy", screening). So the Twist's shield works only if the SM is genuinely neutral under both isometries — i.e.
sequestered so its masses do not come from the T-sector geometry. That is still an assumption, now with a name and a precise test
(the perturbative order p ≥ 3). Novelty: the specific combination (the cliff's own instanton as the only breaking, with π/4 set by
SU(8)) appears to be new; the mechanism class is not.

**D142 — the isometry shield, constructed explicitly and run against every precision test (shield_tests_d142.py;
results/shield_tests_d142.txt, shield_fingerprint.txt); predictions locked (PREREG_SHIELD.md).** Using the full thawing solution
(x = 72.7 at BBN, 73.1 at z = 3, 75.8 at z = 1, 85.0 at z = 0.14, 88.9 today; d ln x/dt = 2.5×10⁻¹¹ /yr): the instanton part passes
quasars by 10¹⁹, Oklo 10²¹, BBN 10²³, clocks 10²¹. A perturbative leak c_p/x^p is limited most tightly by **atomic clocks** (not
MICROSCOPE as D140 said): p = 1 needs c_p < 3.5×10⁻⁶; p = 2, c_p < 1.6×10⁻⁴; p = 3, c_p < 9×10⁻³; p = 4, c_p < 0.6. Correction to
D140: an O(1) leak needs p ≥ 4. New signature: because the field is frozen until late, any leak has a fixed redshift shape — about
78% of the total change happens at z < 1 and almost nothing above z ≈ 3 — and ties clock drifts to quasar shifts.

## Developments 143–147 — working the afternoon worklist (theory/pending_docs/WORKLIST_2026-11-13_afternoon.md)

**D143 — the shield vs a volume-type T: a sharp geometric condition (shield_vs_volume_d143.py).** D123 assumed T behaves like the
volume of the extra dimensions. Then string α′³ corrections (Becker–Becker–Haack–Louis) give a 1/x^{3/2} leak with size ξ ∝ Euler
number χ of the compact space: ξ = −ζ(3)χ/(2(2π)³). The clock limit for p = 3/2 is c_p < 2.2×10⁻⁵. Unsequestered SM: fails for every
χ ≠ 0. Sequestered SM (one loop): still fails unless |χ| < 1.4 — **the compact space must have Euler number zero** (such spaces exist,
e.g. Schoen's manifold and some toroidal orbifolds), or T must not be the volume (and then D123's tower argument needs redoing).
Status: a concrete, checkable condition on the extra-dimensional geometry; the two Twist assumptions (D123 and the shield) are
compatible only on χ = 0 spaces.

**D144 — what couplings of the angle y to the SM the shift symmetry still allows.** Shift-invariant couplings are derivative
(∂_μ y J^μ, the lepto-axiogenesis coupling c_A, which the model needs) or topological (y·G G̃). Neither gives a monopole (composition-
dependent) force: derivative couplings vanish for a static field and give only spin/velocity-dependent effects; a y·GG̃ coupling would
make the angle QCD-axion-like (a potential ~ m_π² f_π² ~ 10⁻³ GeV⁴, negligible against the angle's +8H² on the plateau; today the angle
already sits at its minimum) and gives a spin-dependent force only with an extra CP-violating scalar coupling, which the shift forbids.
Status: consistent; the shield keeps exactly the coupling baryogenesis needs.

**D145 — the SM's gauge couplings must not come from T.** The hidden SU(8) and G₂ have f = T; the SM's f must come from another
modulus (or be constant). A Planck-suppressed mixed operator c Tr W₈² Tr W_SM²/M_P³ is allowed and gives f_SM ⊃ c q — instanton-
suppressed, i.e. already in D142's part (a): passes by 10¹⁹⁺. Status: consistent, one more assumption made explicit (SM gauge
kinetic functions independent of T).

**D146 — two-step loop leaks T → X → SM.** Through χ: χ's T-dependence is the saturating e^{−2πT} (D118) → leak ∝ e^{−2πx} ≈ 10⁻²⁴³.
Through S: Z₂-odd, at S = 0, couples in pairs only via gravity → ≲ (H₀/M_P)² ~ 10⁻¹²². Through the hidden sectors: via q (as D145).
Through gravitons: ~ V_tail/M_P⁴ ~ 10⁻¹²⁰. All pass. The only dangerous leak is perturbative (D142 (c), D143).

**D147 — the dark-matter route survives the shield.** χ is neutral under both isometries, so the χ̃ψH/M_P operator that lets χ̃ decay
to SM fermions (D106/D112) is allowed; the 100–500 TeV estimate is unchanged by the shield (still conditional and out of the
predictions table until it settles).

**D148 — the SU(8) strong-coupling problem has a simple cure (results/su8_weak_d148.txt).** With f_SU(8) = f₀ + T (f₀ a constant from
another modulus, e.g. a dilaton) the condensate is e^{−2π(f₀+T)/8} = e^{−πf₀/4}·e^{−πT/4}: the cliff's 4/π is unchanged, but the
coupling 1/g² = f₀ + x ≥ f₀ through all of inflation. f₀ = 2: α ≤ 0.04 ('t Hooft λ ≤ 4) — weakly coupled, formula under control;
cost: the D119/D126 mixed-operator coefficient must grow by e^{πf₀/4} ≈ 4.8, to c ~ 190–770. f₀ = 4: α ≤ 0.02, c ~ 1000–4000.
Trade-off: control of SU(8) versus a larger operator coefficient (n is still chosen, now inside c). Status: referee point 3(a) →
fixable at the price of a larger coefficient; 4/π can be called "SU(8) form, weakly coupled for f₀ ≳ 2".

**D149 — can the seven-disk ladder move n_s? No.** On any rung n_s ≈ 1 − 2/N at leading order (α only sets r ≈ 12α/N²); a merger
of disks during inflation changes r, not n_s. The ladder cannot help the n_s tension (consistent with D108/D132).

**D150 — why would the SM be neutral? The volume picture says it cannot be (worklist item 14).** Where the SM's constants come from
matters: on D3-branes its gauge couplings come from the axio-dilaton, not T (good, D145), but its UV cutoff is still the string or
KK scale. If T is the volume (D123), M_s ∝ M_P/√V ∝ x^{−3/4}, and Λ_QCD = M_s e^{−8π²/(b g²(M_s))} inherits that: β = (3/4)√(2/3)
≈ 0.61 — 180× over Cassini, at leading order. This is exactly Burgess and Quevedo's finding (D141). So **the shield requires that T
is NOT the overall volume**: the SM's UV scale must not depend on T (e.g. T a fibre or other non-volume Kähler modulus, with the SM's
cycle and the volume stabilised separately — the "fibre quintessence" direction in the literature). Consequences: (1) D143's α′³
condition (Euler number 0) applied to a volume-type T; for a non-volume T the leading corrections are different and must be
re-derived; (2) D123's tower argument used the volume (KK for x > 1, winding for x < 1); for a non-volume T the distance-conjecture
tower is not known — the field distance (≈ 16 M_P) goes back to "open". Status: a real fork, recorded for Danny: volume-type T
(distance conjecture OK, fifth force fails at O(1)) versus non-volume T (shield possible, distance conjecture open).

**D151 — the volume problem is the known one, and the ladder gives each rung's dark energy (rung_tails_d151.py).** In string
compactifications a single modulus with K = −3 ln(T + T̄) (rung 3α = 3) is the overall volume (or the diagonal of three equal tori),
and a light volume modulus couples to matter at Planck strength — a known exclusion (Tasinato et al., arXiv:1203.6655, which
propose instead a FIBRE modulus whose coupling is suppressed by ε ~ m₃/₂/M_P and whose leading potential does not depend on it).
So the rung-3 Twist has no known string realization that avoids the fifth force; D140–D142's shield is a consistent effective
theory, not a string-derived one. Note: the Twist has m₃/₂ = 0 along S = 0, which in a fibre-type set-up would push ε further down —
a possible advantage, not computed. A fibre-type field would sit on a different rung, which changes the dark-energy prediction.
Thawing from rest, λ = √(2/(3α)): rung 1: w0 −0.68, wa −0.44; rung 2: −0.85, −0.22; **rung 3 (Twist): −0.90, −0.15**; rung 4:
−0.93, −0.11; rung 5: −0.94, −0.09; rung 6: −0.95, −0.07; rung 7: −0.96, −0.06. DESI DR2 alone pulls toward the lower rungs; any
switch would be a new model, built after seeing the data, and must be locked and tested on new data only.
Status: fifth force = main open problem at the string level (EFT shield exists; string realization of a neutral SM with a rung-3
modulus unknown).

**D152 — a candidate string home for OUR rung-3 Twist: heterotic string on the Z₃ orbifold (heterotic_z3_d152.py).** Danny: "can we
just work on ours". The volume problem (D150/D151) is a type IIB statement: there the string scale tracks the Einstein-frame volume.
In the heterotic string, M_s/M_P is set by the 4-d dilaton S, so the overall modulus T can move at fixed S without moving the string
scale. On the Z₃ orbifold: (i) T has K = −3 ln(T + T̄) — rung 3, the Twist's; (ii) T-dependent gauge thresholds come only from N = 2
sectors (Dixon–Kaplunovsky–Louis) and Z₃ has none, so the SM gauge couplings (f = S) do not depend on T at one loop; (iii) untwisted
matter (weight 1 each) has physical Yukawas ∝ x⁰; (iv) twisted Yukawas come from worldsheet instantons ∝ e^{−2πT/3} — instanton-type
breaking, β ≈ 10⁻⁷⁹ (passes by 10⁷³). So matter is neutral at tree level and one loop, and the remaining breaking is
non-perturbative — exactly the shield of D140–D142, now with a known string setting. Open: (a) the dilaton S must be stabilised
separately (standard but not shown here); (b) in heterotic language the hidden condensates depend on T through η(T), and the cliff's
e^{−πT/4} form is not yet reproduced (T-duality relates small and large x — the plateau sits at small x — worth checking);
(c) higher-loop/α′ corrections to the Kähler potential still set the perturbative leak, which must fall as 1/x⁴ or faster (D142).
Status: fifth force → "consistent EFT shield with a candidate heterotic Z₃ realization"; not a derivation.

**D153 — the cliff in heterotic language: the exponent fits, the depth does not (results/heterotic_cliff_d153.txt).** With
T = 8 T_het (the Kähler potential keeps the same rung), the cliff's factor e^{−πT/4} is exactly e^{−2πT_het} = q, the modular nome
that runs every heterotic worldsheet-instanton and threshold effect — so the "SU(8)" exponent has a second, natural origin. The
κq term of D119 then arises from N = 2 threshold corrections, f₂ ⊃ −(b′₂/4π²) ln η(T_het) ⊃ (b′₂/4π²) q, giving n = −b′₂/(2πN₂).
But n = 125 would need |b′₂| ≈ 1600–6300; real beta coefficients are O(1–30), so thresholds give n ≲ 2. Two further problems:
N = 2 sectors are exactly what Z₃ lacks (D152 used that to protect the SM), and the same threshold carries a term linear in T that
reshapes the tail unless cancelled. Status: the exponent π/4 has a natural heterotic meaning (q of the modular group); the cliff
depth n ≈ 125 cannot come from thresholds and stays chosen; a consistent orbifold (N = 2 sector seen by the hidden group only) is
not found. Plateau note: the inflation region x ~ 10⁻⁴ is T_het ~ 10⁻⁵, the T-dual of a very large radius — the plateau may be
better described in the dual frame (not pursued).

**D154 — the string-level frontier, stated precisely.** Three things the Twist needs at once: (A) rung 3, K = −3 ln(T + T̄) for the
moving field; (B) a hidden gauge group whose gauge function is linear in T (f = f₀ + T) — that is what makes the cliff and the
racetrack (D119, D126, D148); (C) Standard-Model constants independent of T (the shield). Known settings give two of the three:
- Type IIB, T the overall volume, hidden branes (D7) on its 4-cycle: A + B, but the string scale tracks T → C fails (D150).
- Weakly coupled heterotic Z₃: A + C (D152), but there all gauge functions are f = k S (dilaton) at tree level; T enters only via
  small thresholds (ln η), which cannot give a linear-T gauge function nor n ≈ 125 (D153) → B fails.
- Heterotic M-theory (Hořava–Witten): f_hidden = S − εT and f_visible = S + εT gives B for the hidden group, but the same threshold
  puts T into the SM's coupling → C fails.
- LVS fibre / blow-up moduli: C can hold (suppressed couplings, Tasinato et al.), but their Kähler potentials are not rung 3 → A fails.
**No known string setting gives A, B and C together.** This is now the Twist's sharpest theoretical open problem (alongside n). A
possible direction (not worked): a type IIB setting with T the overall volume and the SM on D3-branes in a strongly warped throat
whose local scale is fixed by fluxes, with the T-dependence of the warped scale cancelled — would need explicit checking against
D150's β ≈ 0.6.
D154 add: the warped-throat direction checked at leading order — the warped tip scale goes as V^{−1/3} e^{A₀} with V ∝ x^{3/2}, so SM
masses ∝ x^{−1/2}: β ≈ 0.41, still ~120× over Cassini. Warping does not rescue the IIB volume case. The frontier stands.

**D155 — type IIA checked for D154.** In IIA the string scale in Planck units is set by the 4-d dilaton (like heterotic), and three
equal torus Kähler moduli give K = −3 ln(T + T̄): A ✓, C ✓ at leading order. But gauge groups live on D6-branes wrapping 3-cycles,
so their gauge functions depend on the complex-structure moduli U, not on T, and the T-dependence of the superpotential comes from
fluxes (polynomial in T) and worldsheet instantons (powers of q = e^{−2πT}). The cliff needs the condensate inside an exponent,
exp(n q), with n ≈ 125 — not the form either source gives. B ✗. IIA joins heterotic Z₃ as "A + C, not B". Pattern across all five
settings: wherever matter is neutral to T (C), T cannot also carry a hidden gauge coupling linear in T (B). If that pattern is a
theorem, the Twist's cliff must come from somewhere other than a T-dependent gauge coupling — a concrete redirection for the
construction programme (open).

**D156 — the loop shift of n_s redone with the saturating χ mass (referee minor point; results/loop_shift_d156.txt).** D77's +0.002
came from χ's mass growing linearly with the inflaton (curvature 2g² in φ). With D118's saturating mass, χ's mass on the plateau is
≈ 2πh(x₀ − x), almost constant across the CMB window: the curvature drops by x*/x₀ ≈ 1.3×10⁻³–6.5×10⁻³, so the loop shift is
~+3×10⁻⁶–1×10⁻⁵ — negligible. Consequence: the Twist's n_s is ≈ 0.964–0.965 (instant reheating to kination), not 0.965–0.968; the
n_s tension is slightly WORSE than quoted. The locked bands (TWIST-P: "+0.000…+0.003") contain this, so no lock changes; the model
card and full-state numbers are corrected.

## Development 157 — the locked n_s test is scored: INCONSISTENT (PREREG_NS_SPA; results/ns_spa.json; PC run, scored 13:20)
Data: ACT DR6 + SPT-3G + Planck low-ℓ + ACT lensing + DESI DR2 BAO + Pantheon+ + DES Y6 S8, with the PURE-TWIST late universe.
**Cost of fixing n_s at the Twist's value 0.964: Δχ² = 11.73 → INCONSISTENT** (locked thresholds: ≤ 4 consistent, 4–9 tension,
> 9 inconsistent). With n_s free the Twist's late universe prefers n_s = 0.9756 (ΛCDM: 0.9732). Reported beside it: ΛCDM with
n_s fixed at 0.964 costs 8.46 (TENSION) — so this data set disfavours n_s = 0.964 for either late universe, a bit more strongly
with the Twist's. Also: on this data set PURE-TWIST with n_s free fits WORSE than ΛCDM by Δχ² = +1.45 (it was −3.4 on the
compressed DESI+SN+CMB set) — the dark-energy preference does not survive the full SPA likelihood here.
Consequences, stated plainly: (1) the D108 falsifier is met on current data: the Twist's inflation (n_s ≈ 0.964–0.965, D156) is
inconsistent with CMB-SPA + DESI at the locked level. (2) TWIST-P was built for this and can only be scored on future data.
(3) Caveat recorded, not used to soften the reading: the high n_s is driven by combining DESI BAO with the CMB (CMB-SPA alone gives
0.968 ± 0.003 in the literature), which some authors attribute to a BAO–CMB tension.

**D158 — where the dark-energy preference went on the full SPA data (diagnostic only; PC results cmp_ns_spa_pure_free.json vs
cmp_ax_spa_lcdm_halofit_s8y6.json).** PURE-TWIST (n_s free) minus ΛCDM (n_s free), per likelihood: DESI BAO −0.63, Pantheon+ −2.55,
DES Y6 S8 −0.04 (late universe: −3.2, the Twist still wins) — but CMB: Planck low-ℓ TT −0.26, low-ℓ EE +1.03, Planck/ACT cut +1.13,
ACT DR6 +0.66, ACT lensing +0.67, SPT-3G +1.47 (CMB: +4.7, the Twist loses). Net +1.45. So the Twist's late-time dark energy still
fits the late-time data better; the full high-precision CMB pays for it, presumably through the parameter shifts needed to keep the
distance to last scattering fixed. Caveat (not used to change any reading): the four minimiser starts for PURE free landed at
n_s 0.9732–0.9759, so minimiser scatter of order 1 in χ² cannot be excluded; an MCMC would settle it. The locked readings stand.

## Development 159 — the cliff without any hidden gauge sector: TWIST-K (theory/kahler_cliff/; results/kahler_cliff_d159.txt)
(Danny 13:50: "stop old things and develop through new".) Put the cliff in the helper field's Kähler metric instead of W:
K = −3 ln(u − g E(u) SS̄ + ζ E(u)² (SS̄)²), E(u) = exp(2n(1 − e^{−πu/8})), u = T + T̄;  W = √3 m S T (no exponential at all).
Full two-field supergravity check (step sizes scaled to E, 200 digits): **V along real T equals the Twist's to 10 digits at every
x from the CMB point to today**; S stays heavy everywhere (m_S²/H² = 29 at the CMB point, 2355–68,000 through the cliff, 2636 today).
New: the angle stays at +4H² everywhere — the Twist's tachyonic angle region at the cliff (m_y²/H² = −18 to −259 at x = 0.3–3)
disappears, and V no longer has the 8-fold angle symmetry (y enters only through |T|²).
What this buys: (1) no SU(8), no G₂ racetrack, no mixed operator — need B of D154 is gone; (2) E depends on Re T only, so it is
shift-symmetric (the shield's isometry), and its tail dependence e^{−πx/4} = |q| is the form of a worldsheet-instanton correction to
a Kähler metric — present precisely in the heterotic and IIA settings where matter is neutral (A + C, D152, D155). So a string home
with A + C may now be enough. (3) n becomes the coefficient of that instanton correction in ln(K_SS̄): 2n ≈ 250. Worldsheet-instanton
coefficients are integer curve counts (Gromov–Witten invariants), often in the hundreds to thousands — a possible route to DERIVING n
(not done; e.g. the quintic's degree-1 count 2875 = 23 × 125 is noted as a coincidence only, no relation derived).
What it costs / changes: (a) the angle's dynamics change (no cliff tachyon) — the matter yield must be recomputed (D160, locked
before running); (b) the hidden axion's kick needs an instanton term coupling σ to the angle, now taken as a worldsheet instanton
∝ |q| cos(πy/4 − σ/f) instead of SU(8); (c) inflation, the cliff, the tail and every late-time observable are unchanged — so n_s is
still INCONSISTENT (D157); TWIST-K fixes the construction, not the data problem.

**D161 — n as an instanton sum: what it would take (TWIST-K).** In TWIST-K the dark-energy scale is set by
ln E(∞) − ln E(0) = 2n ≈ 250, the total change of ln K_SS̄ between the plateau (x → 0, |q| → 1) and the tail (|q| → 0). With a
worldsheet-instanton series ln K_SS̄ ⊃ −Σ_k c_k |q|^k, that change is Σ_k c_k evaluated at |q| = 1 — the FULL resummed instanton
sum at small volume, not a single curve count. Genus-0 counts N_d grow exponentially with degree (the series converges only away
from the small-volume/conifold region), so this sum is finite only after resummation, where it is governed by the geometry near
small volume. So "n = a count of curves" is too naive; "n = the resummed instanton sum at small volume" is the precise target.
This needs a specific compact geometry and the matter-metric's instanton expansion — a research project, not attempted here. The
single-term form exp(−2n|q|) used in TWIST-K is a model of that resummation, not derived. Status: route to deriving n identified
and stated precisely; n still chosen.

## Development 162 — TWIST-L: raising n_s without leaving rung 3 (locked 13:59, PREREG_TWISTL.md)
Key observation: any plateau that approaches flat as a power of x = e^{cφ} gives n_s ≈ 1 − 2/N (D132), but a LOGARITHM of x is
linear in φ, so a factor 1/ln(1/x) in V gives a polynomial approach (V ≈ 1 − b/(c|φ|), k = 1) while T's own kinetic term — the
rung-3 disk — is untouched. In TWIST-K the cliff already lives in S's Kähler metric, so a log factor there (L = 1 + b/(1 + ln(1+2/u)),
the shape a loop/running correction takes) does this. Results (twistl_scan.txt, b = 0 reproduces TWIST-K's 0.9649/0.0036): b = 1:
n_s 0.9688, r 0.0048; b = 2: 0.9715, 0.0061; b = 3: 0.9735, 0.0073; b = 5: 0.9762, 0.0095; b = 10: 0.9791, 0.0140. S stays heavy
(8–24 H²), the angle +4H², the tail unchanged. Built after seeing the n_s data → locked for future CMB data only. Compared with TWIST-P:
stays on the seven-disk ladder (the geometric picture survives), and predicts a lower r at the same n_s (0.006 vs 0.011 at 0.971) —
future r measurements can tell them apart. Open: b ≈ 2–5 is large for a one-loop log (needs many fields) — naturalness not shown.

**D163 — TWIST-L's log can be natural (results/twistl_naturalness_d163.txt).** An ordinary one-loop log (L = 1 + κ ln(1/x)) has the
wrong form (it tilts the plateau the wrong way). TWIST-L needs an INVERSE log, b/ln(1/x) — which is exactly how a running gauge
coupling depends on scale. If S's metric gets a correction C·g²(μ) from a gauge sector whose relevant scale is set by T (μ = x M, e.g.
winding/KK masses at x < 1), and that coupling is IR-free (like QED: it weakens logarithmically at low scales), then
1/g² = (|b_β|/8π²)(ln(1/x) + ln(Λ_L/M)) and L = 1 + C g² reproduces TWIST-L's form with b = 8π²C/|b_β|. For b = 2–5 and beta
coefficients |b_β| = 1–20: C ≈ 0.03–1.3 — natural sizes for a tree-level coupling of S to that sector. So the naturalness worry of D162
(b "large for a one-loop log") is answered by the inverse-log/running-coupling reading: b is large because 8π²/|b_β| is large, not
because many fields run in a loop. The Landau scale must sit near M (ln(Λ_L/M) ≈ 1) — one condition, not derived. Status: plausible
origin, not derived; the TWIST-L lock is unchanged.
D162 add (tail check, results/twistl_tail_check.txt): on the tail L adds ≤ 1% to the slope √(2/3) (0.5–1.2% for b = 1–10), so w0
moves by ~0.002 and wa negligibly — TWIST-L's dark energy is the Twist's within DESI DR3's reach. (The full-state note first said
"unchanged to ~10⁻⁵"; corrected.)

**D164 — the heterotic home is NOT self-consistent as matched (results/heterotic_coupling_d164.txt).** At fixed 4-d coupling the
heterotic 10-d coupling grows as g_s ≈ g_YM R³. With the cliff's exponent matched to the heterotic instanton (T_het = x/8, D153),
weak coupling (g_s < 1) holds only for 6.4 < x < 10.1 (R ≈ 0.9–1.1). Along the history: during inflation the (T-dual) radius is
25–250 and g_s ~ 10⁴–10⁷; today (x ≈ 89) R ≈ 3.3 and g_s ≈ 26. So both inflation and today sit at STRONG heterotic coupling — the
heterotic M-theory (Hořava–Witten) regime, where D154 found the Standard Model's coupling picks up T (f = S + εT) and the shield
fails. D152's weak-coupling properties (no T-thresholds on Z₃) therefore do not apply where they are needed. Escape (not checked):
if the cliff came from an instanton of action 2π·N·T_het (a degree-N curve, or N-fold wrapping), T_het = x/(8N) and today's
point is weakly coupled for N ≳ 9; high-degree curve counts are enormous, which might also bear on n (D161) — a lead, not a result.
Inflation would still sit at strong coupling (dual radius large). Status: the string-home question reopens; D152 downgraded from
"candidate" to "candidate only if the cliff instanton has degree ≳ 9".
D164 add: the degree-N escape has a price. Lower-degree instantons (d < N) would give slower exponentials e^{−πxd/(4N)}; for N = 9 at
x = 89 a degree-1 term is ~4×10⁻⁴ — 10²⁷ times the cliff's leftover — which would reshape the dark-energy tail and break the shield's
margins (D142). So the escape needs the curve counts of degree 1…N−1 to vanish (or be cancelled) in the relevant metric: a strong,
checkable condition on the compact geometry, not a natural default.

## Developments 165–166 — trying to derive n from string geometry (Danny 14:16: "go ahead … map out the universe correctly")

**D165 — curve counts cannot give n (theory/string_home/quintic_n_d165.py; results/quintic_n_d165.txt).** The quintic's genus-0
counts were computed here from its mirror periods (n₁ = 2875, n₂ = 609,250, n₃ = 317,206,375, … n₇ ≈ 2.95×10²⁰ — matching the
literature, a check on the code). Their share of e^{−K} rises from 3×10⁻⁸ (τ = 3) to 2.6×10⁻² at τ = 1.2, the edge of the geometric
phase (conifold at τ ≈ 1.21; the series diverges beyond it, so smaller τ values are not trusted). With the heterotic matter metric
∝ e^{−K_T/3}, the change of ln(matter metric) available is ≲ 0.01 — against 2n ≈ 250 needed: short by ~10⁴. So in TWIST-K the
10¹⁰⁸ hierarchy cannot come from a worldsheet-instanton correction to a metric, at least not on a typical Calabi–Yau. The large
number must come from an EXPONENT (a non-perturbative effect whose action is large), not from a series of curve counts.

**D166 — the natural source of a large exponent: flux integers and warping (lead, not a result).** In type IIB flux compactifications
a warped throat (Klebanov–Strassler) gives a hierarchy e^{4A₀} = e^{−8πK/(3g_sM)} from two flux integers. Matching e^{−2n}:
K/(g_s M) ≈ 30 — e.g. g_s = 0.1, M = 20, K ≈ 60: ordinary flux numbers. Striking structural echo: in KKLT-type models the
nilpotent stabiliser S is the anti-D3 brane at the tip, and its Kähler metric carries the inverse warp factor — exactly where
TWIST-K puts E. Problems (why this is a lead only): (i) direction — warping is strong at SMALL volume and washes out at large volume,
while TWIST-K needs E ≈ 1 on the plateau (small x) and E ≈ e^{2n} on the tail (large x); it fits only if x is the T-dual of the
volume; (ii) shape — warp factors depend on volume as powers, while the Twist's tail needs the leftover to die as e^{−πx/4}; a
power law would change the tail slope and w0 (a different model); (iii) D150: a warped Standard Model gets a fifth force — here only
the S-sector would sit in the throat, which must be checked. Status: n's most promising origin is a flux-integer warping hierarchy
(K/(g_sM) ≈ 30), with three concrete obstacles written down.

**D167 — warping's shape, checked (results/warp_shapes_d167.txt).** For the hierarchy to sit at the cliff, ln E must be ≪ 1 at the CMB
point (x ≈ 10⁻⁴) and 2n ≈ 250 today. A power-law warp factor (T-dual reading of D166) gives ln E ≈ 241 already at the CMB point — no
plateau. A warp factor that switches on linearly in (1 − |q|) gives ln E ≈ 241 at the CMB point too. Only the form where the EXPONENT
switches on, E = exp(2n(1 − |q|)) (TWIST-K), gives ln E = 0.03 at the CMB point, 2.4 at the end of inflation and 250 today. So the
string mechanism must make the hierarchy's exponent itself grow as (1 − e^{−πx/4}) — in warping language, the throat's depth
8πK/(3g_sM) must turn on with T (for example, if the effective g_s or flux charge depends on T through a factor 1 − |q|). With that
form, obstacle (ii) of D166 disappears (the tail's leftover dies as e^{−πx/4}, as required). Status: n's origin narrowed to
"an exponent proportional to (1 − |q|) with coefficient 2n ≈ 250 = 8πK/(3g_sM)"; what makes the exponent switch on is open.

## Development 168 — base physics: the full late-universe prediction set (theory/observables/; locked PREREG_GROWTH)
From the rung-3 tail alone (no string input): w(z) = −0.899 (z = 0), −0.949 (0.5), −0.974 (1), −0.996 (3). At the same Ω_m and H₀ as
ΛCDM: H(z)/H_ΛCDM peaks at +1.9% (z ≈ 0.5); D_M is 1.4–1.5% short at z ≈ 0.7–1; σ8 is 1.5% lower today (the S8 tension goes the
Twist's way, modestly); f σ8 is 3.2% lower at z = 0.3–0.5, fading to 0.4% by z = 3; the growth index stays GR-like (0.557 → 0.548,
within 0.003 of ΛCDM) because the field neither clusters nor couples to matter. These are the numbers DESI DR3 full-shape, Euclid and
Rubin will measure; locked as PREREG_GROWTH (a γ deviation > 0.05 or an f σ8 excess at z = 0.3–0.7 at > 3σ disfavours the Twist).

**D169 — the Twist and the Hubble tension (theory/observables/h0_shift_d169.py; background-only estimate).** Holding the early universe
fixed by the CMB (ω_m = 0.1430 and the distance to last scattering at their ΛCDM values), the Twist's thawing tail needs H₀ = 65.7
km/s/Mpc (ΛCDM 67.4) and Ω_m = 0.331 (ΛCDM 0.315). So the Twist moves H₀ AWAY from local measurements (~73): it makes the Hubble
tension slightly worse, as thawing quintessence generically does. Stated plainly as a cost of the model; the Twist offers no
resolution of the Hubble tension. (Full CMB fits shift parameters together; the NS-SPA PURE fits are the precise version.)

**D170 — what DESI will actually see: CMB-anchored BAO ratios (theory/observables/bao_ratios_d170.py; results/bao_ratios_d170.txt).**
Same early universe as Planck-ΛCDM (ω_m, r_d, θ* fixed; Twist H₀ 65.7): D_M/r_d is larger than ΛCDM's by +1.3% at z = 0.30, +0.8% at
0.51, +0.5% at 0.71, +0.3% at 0.93, +0.1% at 1.3–1.5, ~0 at 2.3; D_H/r_d is smaller by 0.4–0.5% at z = 0.5–1.5 (larger by 0.3% at
z = 0.3). The signal is concentrated at z < 1 and is largest in the transverse distance at low z — where DESI's own w0wa preference
comes from. These are the numbers behind WATCH-PURE-DR3 (already locked; not re-locked here).

**D171 — neutrino mass degeneracy (theory/observables/neutrino_mimic_d171.py; background-only estimate).** At z = 0.51 the Twist's
CMB-anchored distance signal (D_V +0.44% over Planck-ΛCDM) can be mimicked in ΛCDM by adding late-time matter worth +0.044 eV of
neutrino mass (Σm_ν 0.06 → 0.10 eV, H₀ 66.9). But the redshift shapes differ: at z = 0.30 the Twist gives +0.95% vs the mimic's
+0.53%; at z = 0.93, +0.06% vs +0.30%; at z = 1.48, −0.03% vs +0.19%. So the Twist's signal is steeper toward low redshift than a
neutrino-mass shift; DESI DR3's redshift coverage can separate them. Consequence for interpretation: a ΛCDM analysis of a
Twist universe would be pulled toward a somewhat HIGHER neutrino mass at z ≈ 0.5 and lower at z ≈ 0.3–1.5, partially cancelling;
no claim is made here about DESI's own neutrino-mass result (that needs the full likelihood).

## Development 172 — strong CP and the ISW effect (theory/observables/strongcp_isw_d172.py; results/strongcp_isw_d172.txt)
**(a) Can the twist angle be the QCD axion? It could solve strong CP, but as it stands it makes far too much dark matter.** A
shift-symmetric y·GG̃ coupling is allowed (D144). The angle's decay constant on the frozen tail is f ≈ 4–5×10¹⁶ GeV; QCD's potential
then dominates the angle's own (the T-sector shifts the QCD minimum by only ~10⁻⁴³, far below the 10⁻¹⁰ bound), so θ_QCD relaxes to 0
— strong CP solved. But the angle then oscillates as axion dark matter: for an initial angle of order one it gives 3–4×10⁵ times the
observed dark matter, and the Twist's own runs leave it 0.5–0.9 rad from a minimum. It would need θ_i ≈ 2×10⁻³ (or a dilution of
~10⁵ after the QCD transition). Status: the angle is NOT the QCD axion in the Twist as computed; strong CP stays unaddressed. Lead
noted: if the angle's kick could be arranged to stop within ~10⁻³ rad of a minimum, the angle would solve strong CP AND be the dark
matter (replacing the gravity-only fermion) — a different, testable model (axion haloscopes at f ~ 5×10¹⁶ GeV, m_a ~ 10⁻¹⁰ eV, the
ABRACADABRA/DMRadio range). Not pursued without a mechanism.
**(b) ISW.** The late-time integrated Sachs–Wolfe signal (the change of the potentials since z ≈ 3) is 5.0% stronger than ΛCDM's at
the same Ω_m — a small, definite prediction for CMB × galaxy cross-correlations (current precision ~10–20%; future surveys a few %).

**D173 — where neutrino masses could come from (lead; results/neutrino_scale_d173.txt).** The matter mechanism (lepto-axiogenesis)
uses neutrino masses but the Twist does not explain them. With the standard seesaw, m_ν = y²v²/M_R: the heaviest neutrino (~0.05 eV)
needs M_R ≈ 6×10¹⁴ GeV for an order-one Yukawa, 5×10¹³ for y = 0.3, 6×10¹² for y = 0.1. That is the Twist's own range of scales:
the hidden SU(8) confines near 10¹⁴ GeV (D98, hidden-gauge construction), the reheating temperature is ~4×10¹⁴ GeV, and the
inflationary Hubble rate 1.5×10¹³ GeV. A right-handed-neutrino mass set by the hidden confinement scale would land in the right
place with Yukawas 0.3–1 — a natural lead, not built (and absent in TWIST-K, which has no SU(8); there it would need another source).
Caveat: right-handed neutrinos at ~10¹⁴ GeV below T_RH would be produced after inflation and their decays add ordinary leptogenesis
on top of lepto-axiogenesis — a second matter source to be checked if this is pursued.
D172 add (strong-CP lead checked): could the angle relax toward a minimum by itself before the QCD era, giving the small θ_i the lead
needs? No — its mass comes from the T-sector potential (m_y² ≈ 4V_T/3), which during the radiation era is far below H², so the angle
stays frozen at its post-kick value (0.5–0.9 rad) until long after the QCD transition. The lead needs an external mechanism.

## Development 174 — the four Tier-2 checks (theory/twistl/twistl_history_check.py, twistl_reheating_check.py, tier2_estimates.py)
1. **TWIST-L is stable along the whole history** (b = 3 and 10, full two-field SUGRA): m_S²/H² = 22 at x = 10⁻⁴, 2355–68,000 through
   the cliff, 2636 today; the angle +4H² everywhere. Same as TWIST-K.
2. **Reheating carries over.** TWIST-K has the Twist's potential and kinetic term along real T exactly, so its reheating is identical.
   TWIST-L (normalised to the observed A_s) heats a little less: heat share ×0.81–0.83 (b = 3) and ×0.67–0.71 (b = 10) of the Twist's,
   i.e. ~0.65% and ~0.55% instead of 0.8% — inside the range already covered (D118: 0.65–0.75%); the tail is insensitive (D125); the
   matter yield at those heat shares would need its own check if TWIST-L is ever favoured.
3. **The cliff's gravitational-wave burst is invisible**: f ≈ 10¹¹ Hz today with Ω_GW h² ~ 10⁻¹⁴ (BBN bound ~10⁻⁶; ultra-high-frequency
   proposals need ≳ 0.1 at GHz). Small-scale features sit at the end-of-inflation horizon, far below astrophysical scales: no
   primordial black holes of interest.
4. **TWIST-L is quantum-stable**: S and graviton loops shift V by 10⁻¹² to 4×10⁻¹¹ of itself; the two-loop correction to the running
   coupling behind the log factor changes the effective b by ~10%, which moves the prediction along the locked n_s–r curve, not off it.

## Development 175 — rung 3 is the QUATERNION rung (theory/geometry/fano_rung3_d175.py; results/fano_rung3_d175.txt)
Literature check first (correction to D138): the seven-disk papers (arXiv:1610.04163, 1704.04829) identify disks by hand
(T₁ = … = T_k) and do not use the Fano plane; the octonion link is elsewhere — Duff & Ferrara (hep-th/0610314, 0704.0507): N = 8
black-hole entropy is Cartan's E₇ invariant, E₇ ⊃ SL(2)⁷ gives seven qubits, and the seven tripartite (three-qubit, STU-type)
pieces are exactly the seven lines of the Fano plane, which is the octonions' multiplication table.
Computation: of the 35 ways to identify three of seven disks, exactly 7 lie on a Fano line, and those are exactly the triples that
close under octonion multiplication — {1, e_a, e_b, e_c} is then a copy of the quaternions. Doing the same for every rung: closed
choices exist only for 3α = 1 (7 ways: one unit, a copy of the complex numbers), 3α = 3 (7 ways: the quaternions) and 3α = 7 (1 way:
the octonions); rungs 2, 4, 5, 6 have none. So the rungs that respect the algebra are exactly the normed division algebras C, H, O
(imaginary dimensions 1, 3, 7 — Hurwitz's theorem), and **the Twist's rung 3 is the quaternionic one**: the Twist's single field is
the diagonal of an STU triple sitting on one Fano line. Hypothesis (not derived): if consistent truncations must close under the
octonion product, only rungs 1, 3, 7 occur — r ≈ 0.0012, 0.0036, 0.0084 at N ≈ 57 and dark energy w0 ≈ −0.68, −0.90, −0.96.
That is a sharp, falsifiable selection rule; locked as PREREG_DIVISION_RUNGS.

**D176 — novelty check of D175 (Gunaydin, Kallosh, Linde & Yamada, arXiv:2008.01494).** They already tie the seven disks to octonions:
the superpotential is built from the associative triads (= Fano lines = quaternionic subalgebras) via the (7,4) Hamming code, giving
3α = 7 and, through "split" models (6+1, 5+2, 4+3), all seven benchmarks. Consequences: (1) the octonion/Fano connection is theirs;
(2) rungs 2, 5, 6 do arise in octonion-structured constructions, so D175's "only 1, 3, 7" selection rule is NOT implied by them —
recorded as deviation D1 of PREREG_DIVISION_RUNGS (kept as an independent, stricter conjecture); (3) a genuinely new observation
survives: their 4+3 split is built by hand and its rung-3 direction (T², T³, T⁶) is NOT a Fano line. The G2-natural 4+3 split would
take the three moduli of an associative triad (a Fano line, rung 3) and the four of its coassociative complement (rung 4). In that
version the Twist's rung-3 field is literally the quaternionic (associative) part of the octonionic structure. Whether a Hamming-code
superpotential gives that split with two flat directions is a concrete construction problem (open; candidate next step).

**D177 — the G2-natural 4+3 split, built (theory/geometry/g2_split_d177.py; results/g2_split_d177.txt).** Superpotential in the
Kallosh–Linde–Wrase–Yamada style restricted to two blocks, W = M[Σ_{A}(T_i − T_j)² + Σ_{C}(T_i − T_j)²], with A = {1,2,4} a Fano line
(associative triad) and C = {3,5,6,7} its complement (a coassociative quadruple — checked for all 7 lines: no complement contains a
line). Mass matrix eigenvalues (in units of M): 0, 0, 6, 6, 8, 8, 8 — exactly two flat directions, T_A and T_C, with all other moduli
heavy. T_A is three identified disks: K = −3 ln(T + T̄), rung 3 — the Twist. T_C is rung 4. All seven such splits are equivalent under
the Fano plane's symmetry. Contrast: Gunaydin–Kallosh–Linde–Yamada's hand-made 4+3 split puts {2,3,6} — not a Fano line — in the rung-3
block. So the Twist can be read as the associative (quaternionic) flat direction of a G2-structured split, with a rung-4 companion
modulus T_C. Open: whether this split follows from the octonion/Hamming-code superpotential of GKLY rather than being written in block
form; and what the companion T_C does (it would be a second light field — fixed by other effects, or a second, rung-4 dark-energy-like
field with w0 ≈ −0.93, wa ≈ −0.11 if it also thaws).

**D178 — the rung-4 companion must be stabilised, and then the Twist stays one light field (results/companion_d178.txt).** With the G2
split, K gains −4 ln(T_C + T̄_C), so the inflation potential carries e^{K_C} = (2x_C)^{−4} ∝ e^{−2√2 φ_C}: an unstabilised companion
runs away (ε_C = 4) and destroys inflation. So T_C needs its own stabilisation — e.g. a Kallosh–Linde racetrack giving a supersymmetric
Minkowski vacuum (W_C = ∂W_C = 0, so W = 0 at S = 0 and the gravitino stays massless) with m_C ≫ H_inf ≈ 1.5×10¹³ GeV. Then e^{K_C} is a
constant absorbed into m, and every Twist prediction is unchanged. A second thawing (rung-4) dark-energy field is excluded unless its mass
were purely Hubble-induced — not the case for a racetrack. One more ingredient (standard in the literature), no change to observables.

**D179 — the octonionic building blocks DO produce the associative/coassociative split (theory/geometry/g2_split_signs_d179.py;
results/g2_split_search_d179.txt).** Search over every superpotential built only from Gunaydin–Kallosh–Linde–Yamada-type terms — one
product (T_i − T_j)(T_k − T_l) per coassociative quadruple, any of its 3 pairings, either sign (823,543 combinations) — keeping those
whose supersymmetric flat directions are exactly T_A (a Fano line) and T_C (its complement), with every term vanishing there.
Result: 1,824 such superpotentials for each of the 7 lines (equal counts, as the Fano symmetry requires — the check on the code; a
first version that fixed signs by sorting gave unequal counts and was discarded), the smallest using 4 of the 7 quadruples. So the
G2-natural 4+3 split — the Twist's rung 3 as the associative (quaternionic) flat direction — arises from the same octonionic
ingredients GKLY use, not only from the block form of D177. Open: whether the specific signs fixed by the octonion structure constants
(the coassociative 4-form) are among the 1,824 — the last step to "derived from the octonions" rather than "built from their pieces".

**D180 — GKLY's EXACT octonion superpotential does NOT contain the associative split (theory/geometry/gkly_exact_split_d180.py).**
Their W_O (arXiv:2008.01494 eq. 4.7) has one fixed term per Fano line: (T^{r+2} − T^{r+4})(T^{r+5} − T^{r+6}), with pairings and signs set
by the octonion structure; the full W_O leaves one flat direction (all seven equal, rung 7), as they state. Testing every subset of
those exact terms (127 subsets, with unit and with random coefficients): none gives the two flat directions T_A (a Fano line) and T_C
(its complement). So D179's 1,824 split superpotentials all need pairings or signs that differ from the octonion-fixed ones. Reading:
the associative/coassociative split can be built from octonionic PIECES but is not obtained by removing codewords from the octonion
superpotential itself — consistent with GKLY finding their 4+3 split only by hand (and with a non-Fano rung-3 set). This looks like a
structural statement: within the exact octonion superpotential, rung 3 does not come out aligned with a quaternionic subalgebra.
Status: the "Twist = quaternionic rung of the octonions" picture is geometric (D175, D177), but NOT derived from the published
octonion superpotential; it needs a different (still octonion-built) superpotential. Recorded as a precise negative result.

**D181 — why the exact octonion superpotential refuses (results/gkly_compatible_d181.txt).** For a Fano-line split only 3 of GKLY's 7
octonion terms are compatible (one of their pairs lies inside the line or inside its complement); those 3 leave THREE flat directions
that are not clean disk identifications. So within the octonion-fixed pairing (pairs of index difference 2 and 1 in the cyclic
labelling), an associative-aligned split is under-constrained — the obstruction is structural, not numerical.

**D182 — a lead for n from curve counts after all, via the gauge function (results/kappa_counts_d182.txt; order of magnitude).** D153
dismissed threshold corrections because beta coefficients are small. But in heterotic (2,2) models the moduli-dependent thresholds also
involve the Yukawa/prepotential instanton series, whose coefficients are curve counts (thousands). If the gauge-function correction κq
carries κ ~ n₁/(16π²), the requirement n = 2πκ/N₂ = 125 needs n₁ ~ 3,160·N₂: the quintic (2,875) gives N₂ ~ 0.9, P(1,1,1,1,2)[6]
(7,884) N₂ ~ 2.5, P(1,1,1,1,4)[8] (29,504) N₂ ~ 9.3 — the right range for a small hidden group. Normalisation uncertain by O(1)–O(2π);
this is a lead only. But it reconnects the two failed routes (D153 thresholds, D165 metric instantons): the large number could be a
curve count sitting in a gauge coupling's instanton correction, inside an exponent — exactly the form D167 requires.
D182 add (literature normalisation; arXiv:2408.12458, "Non-perturbative resolution of strong coupling singularities in 4d N=1
heterotic/M-theory"): (i) on toroidal orbifolds the holomorphic threshold is f_a ⊃ −(b_a/16π³) ln η(iT)¹² — its q-coefficient is
~12 b_a/16π³ ≈ 0.024 b_a, confirming D153 (too small); (ii) on Calabi–Yaus the large instanton corrections to the gauge coupling come
from M5-brane instantons, Re S → r − (1/32π³) Σ_γ Re[Ω̄_γ …], with Ω̄_γ generalised Donaldson–Thomas (BPS) invariants — counts, but
not genus-0 curve counts. With the 1/(32π³) prefactor, κ ≈ 20 N₂ needs BPS counts ~2×10⁴·N₂ (about 4×10⁴ for N₂ = 2) — plausible
sizes for such invariants, ~5× larger than the 1/16π² guess. Caveat: these corrections live in heterotic M-theory, where D154 found the
Standard Model's coupling picks up T; and they correct Re S (shared by both E₈'s) unless the hidden sector sits on a different wall.
Status: the "big count in an exponent" route has a concrete published mechanism (M5-instanton corrections to the gauge coupling,
weighted by BPS counts), with the right order of magnitude; its compatibility with the shield is the open point.

**D183 — heterotic M-theory with the hidden force on the other wall (results/hw_walls_d183.txt; standard Hořava–Witten relations,
order of magnitude).** The wall couplings are 1/g² = Re S + b_wall Re T, with b_wall set by the wall's bundle and five-brane charges and
anomaly cancellation c₂(V_vis) + c₂(V_hid) + [M5] = c₂(TX). Choosing c₂(V_vis) = c₂(TX)/2 makes b_vis = 0 — the Standard Model's gauge
coupling loses its linear T term — while the hidden wall keeps b_hid = −[M5] ≠ 0, i.e. a hidden coupling linear in T (need B) and an
instanton-corrected hidden sector for n (D182). So the coupling half of C can be engineered. But the UV scale cannot: M_GUT/M_P ∝
(Re S·Re T)^{−1/2}, so at fixed S the QCD scale tracks x^{−1/2} and β ≈ 0.41 — 120× over Cassini, the same scale problem as D150.
Status: in heterotic M-theory A and B hold and the gauge-coupling part of C can be arranged, but the Standard Model's mass scale still
follows T. The frontier is now down to ONE precise obstruction across every setting checked: the matter sector's UV scale tracks the
rung-3 modulus. Anything that fixes M_GUT/M_P independently of T (a different modulus setting it, or T not being the volume-like
direction that also sets the interval) would close the gap.

**D184 — the matter-neutral direction and its rung, setting by setting (theory/darkenergy/scale_preserving_d184.py).** Moving several
moduli together so that the matter sector's UV scale stays fixed defines a path in moduli space; its kinetic term behaves like a single
disk of rung 3α_eff. Results: type IIB → 3α_eff = 12 (tail slope 0.41, beyond the seven-disk ladder); heterotic M-theory → 3α_eff = 4
(slope 0.71: w0 ≈ −0.93, wa ≈ −0.11); weakly coupled heterotic → 3α_eff = 3 exactly, with the gauge coupling (Re S) also fixed. So the
ONLY setting where the matter-neutral direction is the Twist's own rung 3 — with both the scale and the couplings fixed — is weakly
coupled heterotic (consistent with D152). In the others, keeping both fixed needs at least three moduli moving together.
Unified frontier: the Twist's natural string home is weakly coupled heterotic; what breaks it is D164 — today's x ≈ 89 maps to strong
heterotic coupling when the cliff is the basic instanton. Closing the gap = a cliff instanton of action ~9× the basic one (degree ≳ 9,
or 9-fold wrapping) with no lower-degree contributions (D164 add). Side result: a heterotic-M-theory Twist would sit on rung 4 and
predict w0 ≈ −0.93, wa ≈ −0.11 — distinguishable from the rung-3 Twist (−0.90, −0.15) by DESI DR3 + Euclid.

**D185 — the heat-share route to weak heterotic coupling is closed (theory/inflation/heat_window_d185.py).** More reheating freezes the
field earlier: frozen x = 29 (2%), 12 (5%), 8.5 (7%), 6.1 (10%). But (i) the late thaw carries it back to x ≈ 13–36 today, never
below ~13, so g_s today stays ≥ 1.46 (weak coupling needs x < 10); and (ii) once the field freezes near the cliff (x ≲ 12) the
cliff's leftover reshapes the dark energy — w0 −0.81, wa −0.10 at 7% and wa = +0.33 at 10% (the thaw solver fails above that). The
insensitivity of the prediction to the heat share (D125) holds only while the field freezes at x ≳ 15. So the weak-coupling window
cannot be reached by heating; the degree-≳9 cliff instanton (D164/D184) remains the only route found.

**D186 — a subtlety inside the weakly coupled heterotic home: which dilaton is stabilised (results/gs_dilaton_d186.txt).** On Z₃ the
modular anomaly is cancelled by the universal Green–Schwarz term, so the physical coupling is 1/g² = Re Y with
Y = S − (δ_GS/16π²) ln(T + T̄). If moduli stabilisation fixes the holomorphic S, then 1/g² drifts with ln x and the QCD scale picks up
β ~ (8π²/b)(δ_GS/16π²)√(2/3) ≈ 0.4–4 for δ_GS = 3–30 — far over Cassini. The shield therefore needs the stabilisation to fix the
GS-corrected Y (the field the gauge couplings actually see), which is the natural variable for Kähler/racetrack stabilisation in these
models but must be checked in any explicit construction. Added to the weak-heterotic home's list of conditions: (1) cliff instanton of
degree ≳ 9 with no lower-degree terms (D164); (2) Y, not S, stabilised (D186); (3) perturbative leaks falling as 1/x⁴ (D142).

**D187 — the heterotic-M-theory alternative (rung 4) made testable next to the Twist (results/rung4_vs_rung3_d187.txt).** Same late-
universe calculation as D168 with slope 1/√2 instead of √(2/3): w0 −0.925 (vs −0.899), w(z=0.5) −0.963 (vs −0.949); H(z)/H_ΛCDM peaks
at +1.4% (vs +1.9%); D_M short by 1.0–1.1% at z ≈ 0.5–1 (vs 1.3–1.5%); σ8 −1.1% (vs −1.5%); f σ8 −2.4% at z ≈ 0.3 (vs −3.2%); growth
index GR-like in both. The rung-4 signal is about 70–75% of the rung-3 signal throughout — DESI DR3 + Euclid (w0 to ~0.03–0.05) can
separate them only at the ~1σ level; Euclid + Rubin growth adds a second handle. So the data can weakly discriminate which string
setting (weakly coupled heterotic → rung 3; heterotic M-theory → rung 4) the field lives in. Not locked separately: PREREG_GROWTH and
WATCH-PURE-DR3 fix the rung-3 numbers; the rung-4 numbers are recorded here for comparison.

**D188 — how a "degree ≳ 9 only" cliff could arise, and its catch (reasoning note).** On a smooth one-modulus Calabi–Yau, curves of
degree 1 exist (n₁ = 2875 on the quintic), so lower-degree instantons are generic. They can be removed for a SPECIFIC coupling by a
discrete selection rule: if the helper field S carries a Z₉ charge and a degree-d worldsheet instanton carries charge d mod 9 (the
standard way orbifold/discrete symmetries forbid Yukawa couplings), only d ≡ 0 mod 9 contributes to S's metric. That would give
exactly D164's requirement. The catch: curve counts grow ~10³ per degree (the quintic's n₉ is ~10²⁶ by extrapolation of D165's table),
so if those counts appear as coefficients the correction is enormous rather than the ~250 n needs — unless the coefficient is a
different, much smaller invariant (e.g. a BPS index of the specific coupling, or counts suppressed by a high power of the loop factor).
Status: a mechanism for the degree condition exists (discrete selection rule); the size of the resulting coefficient is the open issue.
Two of the frontier conditions (degree ≳ 9; n ≈ 125) are therefore linked — the same instanton sum sets both.

**D189 — the Z₉-selected instanton sum, computed (theory/string_home/z9_selection_d189.py).** Quintic curve counts extended to degree 19
via mirror symmetry: n₉ = 5.04×10²⁶ (confirms D188's estimate), n₁₈ = 2.40×10⁵⁵; growth n_d/n_(d−1) → 1640, so the sum converges only for
τ ≳ 1.18 (conifold estimate 1.21 — consistent). Keeping only degrees ≡ 0 mod 9: at the convergence edge the degree-9 share of e^{−K} is
2×10⁻⁴, so (1/3)ln(1+R) ≈ 2×10⁻⁴ against the 2n ≈ 250 needed. Inside the controlled region it is ≲ 10⁻³; past the edge, degree 18 overtakes
degree 9 (×90 at τ = 1.1, ×2.6×10⁴ at τ = 1) — the sum is uncontrolled, and even its truncation only reaches ~10 by τ = 0.85.
**Verdict:** a Z₉ selection rule can enforce D164's degree condition, but it cannot simultaneously supply n through the matter metric —
the instanton sum changes ln(metric) by O(10⁻⁴–1) where it is under control, ~10³× too little at best. This closes "n from instantons
in the metric" for the selected sum too (extends D165). n stays with an exponent (flux warping, D166–D167) or a non-geometric phase near
the conifold (where τ ≈ 1.2 and the large-volume description itself ends). The degree condition and n are therefore NOT set by the same
sum (corrects the hope at the end of D188): they are two separate requirements.

**D190 — can the flux-warping route for n (D166) live in the heterotic home? (literature check).** D166's exponent 2n = 8πK/(3g_sM) is
Klebanov–Strassler/GKP warping, a type IIB mechanism (RR + NS three-form flux on a deformed conifold). The heterotic analogue is the
resolved conifold with torsion (Carlevaro–Israël, arXiv:0910.3190; local models review arXiv:1109.1534): there the coupling can be kept
small everywhere and a double-scaling limit isolates a throat, but the warp factor is **power-like** in the blow-up parameter a
("acquires a power-like behavior" when a is small compared with the magnetic charges), not exponential in a ratio of flux quanta.
So in heterotic, a hierarchy like e^{−250} must be put into a by hand — it relocates n rather than deriving it.
**Verdict:** the frontier is now sharper. Matter-neutrality (C) and the rung-3 disk (A) point to weakly coupled heterotic; the only
lead found that turns integers into an exponential depth n (flux warping) is type IIB, where C fails (D150–D151). D189 closed instanton
sums in the metric. Remaining honest options for n: (i) a IIB construction that evades D151's matter coupling (e.g. matter on D3-branes
far from the volume modulus, sequestered — a known but model-dependent escape); (ii) heterotic/F-theory duality, where the IIB flux
integers map to heterotic bundle data — whether the exponent survives the map is the precise open question; (iii) accept n as a
chosen number (as now). (ii) is the most promising next lead.

**D191 — heterotic/F-theory duality as a home for warped n (reasoned assessment, not computed).** IIB/F-theory three-form flux maps under
the standard duality chain (Dasgupta–Rajesh–Sethi hep-th/9908088; Becker–Becker–Dasgupta–Green hep-th/0301161) to heterotic compactifications
on non-Kähler manifolds with torsion; the flux integers become torsion/H-flux and bundle data. The heterotic torsional throats that
exist at weak coupling (D190) have power-like warping. An exponentially deep IIB throat therefore maps, as far as the literature shows,
to a heterotic region that is either strongly coupled or outside the perturbative torsional description — the same place D164 already
put the Twist. **Verdict:** no gain at weak heterotic coupling; the exponent does not obviously survive. Status of n: no derivation
route is open in the weakly coupled heterotic home. Ranked remaining: (1) IIB with sequestered D3-brane matter (evades D151 for matter
on distant branes, but must then rebuild the shield for the volume modulus — a concrete next construction); (2) accept n as chosen.

**D192 — IIB with sequestered D3-brane matter (theory/string_home/sequestered_d192.py): fails.** Sequestering makes the SM gauge couplings
dilaton-set and T-independent, but in IIB the only rung-3 direction is the overall volume, and every local scale on a D3-brane is tied to
the string scale, M_s/M_P ~ V^(−1/2) = τ^(−3/4). In canonical units that is a universal matter coupling β = (3/4)/√(3/2) = 0.61 —
181× above the Cassini bound (3.4×10⁻³). Other IIB moduli that matter could be sequestered from (blow-ups, fibres) are not rung 3.
**Verdict:** option (1) of D191 is closed. In IIB, "rung 3" and "matter neutral" are incompatible for a structural reason (the
volume sets M_s/M_P), not a model-building one. Combined with D189–D191: no string setting found derives n while keeping A + C;
n stays chosen. The remaining open string question is the weakly coupled heterotic home with n accepted as an input.

**D193 — stabilising the heterotic dilaton Y (theory/string_home/dilaton_kl_d193.py): works, with a narrow window.** A Kallosh–Linde-type
racetrack of two hidden condensates, W_Y = W0 + A e^{−aY} − B e^{−bY} with SU(8) × SU(9) (a = 2π/8, b = 2π/9), imposing W_Y = W_Y' = 0 at
Re Y₀ = 2 (g² ≈ 1/2): B/A = 0.945, W0 = 0.026 A. Results: (i) Y₀ is fixed by W_Y alone, so gauge couplings do not depend on T (the
shield survives — Z₃ has no T-dependent thresholds, D152); (ii) with W_Y = 0 at the minimum the T-sector potential is exactly the Twist's
(no gravitino mass from this sector, no cross terms); (iii) Y's mass m_Y = e^{K/2}|W''|/K_YȲ scales as x^(−3/2), so it changes ×10³ across
inflation (x 10⁻⁴ → 10⁻²). Requiring m_Y > 10 H_inf at the end of inflation and m_Y < M_s (~0.25 M_P) at its start gives
A ≈ 5×10⁻⁷ – 2×10⁻⁶ — a window of only ~×4 (A = 1 would put m_Y above M_P). Today m_Y ≈ 10⁻¹¹ M_P ~ 10⁷ GeV (no Y fifth force).
**Costs, stated plainly:** one tuning (W_Y = 0 at the minimum — the KL condition), a narrow prefactor window, and supersymmetry breaking
must come from a separate sector whose vacuum energy only shifts the constant (the cosmological-constant problem is not solved by the
Twist, as in any quintessence model). **D186's requirement is met in principle.** The weakly coupled heterotic home now has: A (rung 3),
C (neutral matter, Z₃), Y stabilised (this note), degree-9 cliff via a Z₉ rule (D188); n chosen; cliff form and modular (T-duality)
consistency still to be shown (D-notes ~1177–1332).

**D194 — T-duality vs the rim/centre picture, and a Γ₀(9) cusp escape (theory/string_home/modular_cusps_d194.py).** Problem: if the
heterotic modulus has full SL(2,Z) duality, V(T) = V(−1/T), so the small-x plateau (rim) and the large-x tail (centre) would be the same
physics — the Twist's E (≈1 on the plateau, ≈e^{2n} on the tail) is not duality-invariant. Escape: a duality group Γ₀(N) without the
Fricke involution (typical with Wilson lines / orbifolds with fixed tori) has inequivalent cusps 0 and i∞ — rim and centre become two
genuinely different cusps. N = 9 is a genus-zero level with hauptmodul h = (η(T)/η(9T))³ (24/(N−1) = 3, an integer), and it ties in with
D188's Z₉. Computed: h → 27 e^{−2π/(9 Im T)} at the cusp 0 (checked: 1.869×10⁻¹⁴ both ways at Im T = 0.02) and h ~ e^{2π Im T} at i∞. So
s = 1/(1 + c h) builds a duality-covariant E = exp(2n(1 − s)): E → 1 on the plateau (corrections e^{−2π/(9T)} — far flatter than the
Twist's), E → e^{2n} on the tail with leftover ∝ e^{−2πT_het} = e^{−πx/4} (the Twist's tail exactly).
**Price:** a modular function switches near the self-dual region: with c = 1 the cliff sits at Im T_het = 0.205, x = 1.64, not x ≈ 0.01.
Keeping x ≈ 0.01 needs c ≈ 10²⁴¹ — a second huge number, no better than n. So the duality-consistent version is a DIFFERENT model
(call it TWIST-M: cliff at x ≈ 1.6, plateau exactly flat in E) whose inflation must be recomputed before anything is claimed. Status:
the T-duality obstacle is real for the Twist as written; Γ₀(9) is a concrete way out that changes the cliff's location. Next: compute
TWIST-M's inflation (N*, n_s, r) with the D159 helper, and lock its predictions before any comparison with data.

**D195 — TWIST-M's inflation and tail, computed (theory/string_home/twistm_inflation_d195.py).** Along real T with S = 0 the potential is
exactly V = m²/(4 g(u) E(u)) (u = T + T̄, g = 1 + u/2). Check: the Twist's E reproduces n_s 0.9642/0.9650 and r 0.0037/0.0036 at
N* = 55.7/57 (matches the model card). TWIST-M with the Γ₀(9) hauptmodul and c = 1: inflation ends at u ≈ 1.03 (Twist: 0.018), the CMB
point moves to u* ≈ 0.054, and n_s = 0.9651/0.9658, r = 0.0038/0.0036 — the same predictions (it is the same exponential-plateau
attractor; the plateau slope now comes from g instead of E's linear term). Tail: for c = 1, 1/(c h) = e^{−πu/8}(1 + O(e^{−πu/8})), so
the dark-energy tail is the Twist's to leading order (corrections ~e^{−πx/4} relative, negligible today). **So the duality-consistent
version costs nothing observable at c = 1, and needs no second huge number** — the cliff simply moves to near the self-dual radius.
It does NOT fix n_s (still ~0.965, so D157's INCONSISTENT verdict applies to TWIST-M equally), and n is still chosen. Must be redone
before any claim: heating and matter (they depend on where the cliff sits), N* range, and D164's coupling check at the new cliff.
Status: T-duality obstacle (D194) resolved in principle by Γ₀(9) at no observable cost; post-data construction, no new predictions.

**D196 — TWIST-M9: the degree-9 duality-consistent cliff (theory/string_home/twistm9_d196.py).** Using s = 1/(1 + h⁹) (h the Γ₀(9)
hauptmodul; h⁹ is still Γ₀(9)-invariant): at the large-radius cusp 1/h⁹ = q⁹(1 + 27q + …) — the leftover STARTS at degree 9 with no lower
degrees, which is exactly D164's escape condition, now built in by modular symmetry rather than imposed. Matching the tail gives
Im T_het = x/72; today (x = 89) 1/h⁹ = 4.44×10⁻³¹ vs the Twist's e^{−πx/4} = 4.39×10⁻³¹ (tail kept), and Im T_het = 1.24, R ≈ 1.11,
g_s ≈ 0.96 — weakly coupled, but only just. **Cost:** the cliff moves out to u ≈ 23 (x ≈ 11.5); the stretch between the plateau and
the cliff (where V ∝ 1/(1 + u/2) is a power-law slope with ε ≈ 1/3) adds e-folds, pushing the CMB point and giving n_s = 0.9596/0.9606,
r = 0.0051/0.0048 at N* = 55.7/57 — further from the data than the Twist (0.964–0.965) or TWIST-M (0.965–0.966).
Fix note: the end-of-inflation search in D195 started on the tail; it now scans down the tail, across the cliff, and brackets the
plateau-side edge. D195's numbers are unchanged on rerun (0.9651/0.9658, r 0.0038/0.0036).
**Verdict:** there is a trade-off inside the duality-consistent family: degree 1 (TWIST-M) keeps n_s ≈ 0.965 but sits at strong heterotic
coupling today (g_s ≈ 26, D164); degree 9 (TWIST-M9) is weakly coupled today (g_s ≈ 0.96) but lowers n_s to ≈ 0.960. Neither reaches the
data's n_s ≈ 0.974 (D157). Changing μ (the g-term) could shorten the intermediate stretch — not tried here, because tuning it after
seeing n_s would be post-data fitting; if pursued it must be locked as a separate model first.

**D197 — PREREG_TWISTM9 scan, run as locked (ce4be11; results/twistm9_mu_scan.txt).** All eight μ pass the exclusion tests (inflation ends
at the cliff, u ≈ 23; g_s today 0.96; S heavy, m_S²/H² 930–10⁵). Locked prediction curve (N* = 55.7 / 57):
μ 0.125: n_s 0.9568/0.9579, r 0.0058/0.0055 · μ 1: 0.9596/0.9606, r 0.0051/0.0048 · μ 16: 0.9639/0.9648, r 0.0040/0.0038.
n_s rises only slowly with μ (≈ +0.001 per doubling) and stays below 0.965 across the whole grid: TWIST-M9 cannot reach the data's
n_s ≈ 0.974 at any locked μ. Its curve (n_s 0.957–0.965 with r 0.0038–0.0058, r FALLING as n_s rises) is distinct from TWIST-L and
TWIST-P (where r rises with n_s) — future CMB data can tell the three apart. Plain reading: the weakly coupled, duality-consistent
heterotic version is, on current data, worse than the Twist; it is kept only as a locked, falsifiable alternative.

**D198 — attempting Q4 of the open-problem doc exposes a new leak: Green–Schwarz mixing (theory/string_home/gs_leak_d198.py; estimate).**
Good part first: at the Z₃ ORBIFOLD point the untwisted moduli space is the exact coset (free worldsheet CFT), so the α′³ (χζ(3)) correction
that would give a 1/x³ leak on a smooth Calabi–Yau is absent; one-loop thresholds carry no T (no N = 2 sectors; Mayr–Stieberger hep-th/9303017:
"the moduli dependence … arises only from the orbifold sectors" with N = 2). Problem: the gauge couplings depend on the duality-INVARIANT
string coupling, 1/g_s² = Re Y + (κ/2) ln u_het with κ ∝ δ_GS/8π² (Z₃ generally has δ_GS ≠ 0). D193 fixed the holomorphic Y with
T-independent prefactors, which is not duality-covariant. Making it covariant (each racetrack term carries η(T) powers so all have weight −3)
keeps the two KL conditions consistent but gives Re Y₀(T) = c − 2κ ln|η|, so 1/g_s² = c + (κ/2) ln(u_het|η|⁴) — this grows LINEARLY in
T at large T. Rough size (ΔT_het since z ≈ 1 taken as 0.3 for TWIST-M9 — a guess, to be computed from the tail): |Δα/α| ~ 10⁻⁴ × δ_GS,
against quasar/clock bounds ~10⁻⁶ ⇒ needs |δ_GS| ≲ 0.01. For the degree-1 matching it is ~10× worse.
**Verdict:** a new condition for the heterotic home — the Green–Schwarz coefficient of the overall modulus must vanish (all duality-anomaly
coefficients b′ₐ = 0, hidden groups included), OR the dilaton must be stabilised in its invariant form with no T-dependence (e.g. Kähler
stabilisation — not shown). D193's "works" is downgraded to "works only if δ_GS ≈ 0". This also names a falsifiable signature: if any
leak exists it is a drift of α tracking ln(u|η|⁴), i.e. ∝ T at late times — the same redshift shape PREREG_SHIELD already fixes.

**D199 — a no-go: on a Z₃-type orbifold, δ_GS = 0 forbids every condensing gauge group (theory/string_home/gs_zero_d199.py).** Using
Ibanez–Lüst's duality-anomaly coefficient b′ⁱₐ = −C(Gₐ) + Σ T(R)(1 + 2nⁱ_R) (hep-th/9202046 eq. 3.6; δⁱ_GS = b′ⁱₐ/kₐ for every factor when no
N = 2 sectors) with Z₃ modular weights (untwisted −δᵢⱼ, three copies; twisted −2/3 per plane; oscillator states −5/3 in one plane). The code
reproduces the literature's b′ = −30 for both the hidden E₈ and the (2,2) E₆ (a check). Algebra: b′ = −C + U − Tw/3 − Osc, while the N = 1
beta coefficient is b = −3C + 3U + Tw + Osc. Setting b′ = 0 gives b = 2·Tw + 4·Osc ≥ 0: **no asymptotically free group survives** (brute
scan: 0 counter-cases). So δ_GS = 0 (needed by D198) and gaugino condensation (needed by D193's racetrack, and for any hidden-sector dilaton
stabilisation) cannot coexist on a Z₃-type orbifold.
**Consequences:** (i) the heterotic Z₃ home with condensate-stabilised dilaton predicts an α drift of order 10⁻⁴ × |δ_GS| (D198) — excluded
for any |δ_GS| ≳ 0.01, and every example in the literature has |δ_GS| = 9–30 per plane; (ii) the only escapes are a dilaton stabilised by
something other than condensates (non-perturbative Kähler corrections / the invariant linear-multiplet dilaton fixed T-independently — the
precise open question), or an orbifold where the Twist's modulus is a plane that is NOT completely rotated (then δ_GS need not equal b′/k, but
such planes have N = 2 sectors, which reintroduce T-thresholds for the SM unless the SM avoids them — D152's original worry).
Status: the heterotic Z₃ home is under real pressure; "matter neutral" (C) now requires a dilaton-stabilisation mechanism not yet known.

**D200 — the escape exists in the literature: Binétruy–Gaillard–Wu Kähler stabilisation with a condensate whose beta coefficient equals the
GS coefficient (hep-th/9611149; literature check).** In BGW's modular-invariant linear-multiplet formalism the condensate is
ρ_a² ∝ Π_I [(t^I + t̄^I)|η(t^I)|⁴]^{(b − b_a)/b_a} (their eq. 2.28; b = GS coefficient, b_a = condensing group's), and the moduli-dependent
part of the potential is ∝ d_a = (b − b_a)(1 + 4ζ Re t) (eq. 2.34). When b_a = b — exactly the case of a pure hidden E₈ on Z₃ (b′_E₈ = −C(E₈) =
−30 = δ_GS per plane, D199's check) — "the potential is independent of the moduli, which therefore remain undetermined", while the dilaton
(the duality-INVARIANT ℓ) "is completely determined by string nonperturbative effects" (⟨ℓ⟩ ≈ B/2 for f = A e^{−B/V}). Since V then has
no t-dependence, ℓ cannot depend on t.
**What this fixes:** (i) the α drift of D198 came from fixing the HOLOMORPHIC dilaton with a racetrack; fixing the invariant ℓ with
nonperturbative Kähler corrections leaves physical gauge couplings (k_a/g_s²(ℓ), Z₃ thresholds zero) independent of T — the shield survives
with δ_GS ≠ 0, so D199's no-go is sidestepped, not violated; (ii) T stays flat under the hidden sector (F_T = 0 since d_a = 0), so the Twist's
own potential is the only one T feels at this order — exactly what the model needs; (iii) TWIST-K has no hidden racetrack, so D193's
SU(8)×SU(9) is dropped in favour of a single pure-E₈ condensate.
**Conditions/costs:** no other condensate with b_a ≠ b may be significant (it would pin T at the self-dual point); the cosmological constant
is tuned to zero (as in BGW); supersymmetry is broken by the E₈ condensate at a high scale (no TeV SUSY implied); BGW assume full SL(2,Z)
— the Γ₀(9) version (D194) and the coupling of BGW's sector to the Twist's helper field are not checked. D193 is superseded.

**D201 — coupling the BGW hidden sector to the Twist (reasoned; tree level exact, loops estimated).** Set-up: K = k(ℓ) − 3 ln(u − gE SS̄ +
ζE²(SS̄)²), W = W_hid + √3 m S T, with the BGW condition b_a = b so F^T = 0 and V_hid = 0 (tuned) for every T (D200).
(i) **Tree level, S = 0:** D_T W = D_T W_hid = 0 and D_S W = √3 m T + K_S W_hid = √3 m T (K_S = 0 at S = 0), and the hidden F-terms cancel
against −3|W_hid|² by the tuning. So V(T) is EXACTLY the Twist's (the overall e^{k(ℓ)} is a constant once ℓ is fixed, absorbed in m).
(ii) **Soft mass of the helper S:** K is separable between ℓ and (T, S), so R_{ℓℓ̄SS̄} = 0 and with V₀ = 0, F^T = 0 the canonical soft mass is
m_3/2² — independent of T. (In canonical S the ζ-term's E-dependence also cancels: ζE²|S|⁴/u → ζu|S_c|⁴/(9g²).)
(iii) **One loop:** S's bosons have m² = m_s(u)² + m_3/2², its fermion m_s(u)²; STr M⁴ ⊃ 4 m_s(u)² m_3/2², the only T-dependent piece. Today
m_s ~ 10–300 H₀ (S is heavy only relative to H, D159/D197), so V_1-loop(T) ~ m_s² m_3/2²/(16π²) ≲ V_DE requires m_3/2 ≲ 0.1 M_P — no constraint
in practice. The cosmological constant itself is still tuned (as in any quintessence model).
(iv) **Inflation:** the Twist's energy multiplies e^{k(ℓ)} and pushes on ℓ; stability needs m_ℓ ≫ H_inf ≈ 1.5×10¹³ GeV. In BGW m_ℓ is a
multiple of m_3/2, so m_3/2 must be ≳ 10¹²–10¹³ GeV — high-scale supersymmetry breaking, which a pure-E₈ condensate naturally gives (not
computed here). (v) **Γ₀(9):** BGW's T-independence at b_a = b comes from the anomaly coefficients matching, not from the specific form of η;
the same cancellation should hold with Γ₀(9) forms — argued, not shown.
**Verdict:** the BGW sector and the Twist decouple at tree level and up to harmless loops; the conditions are b_a = b, V₀ tuned, and a high
gravitino mass (≳ 10¹² GeV). The heterotic home now has a complete, consistent effective-theory chain except for n (chosen), n_s (data),
and the Γ₀(9)-BGW check.

**D202 — the E₈ condensate's gravitino mass clears the inflation bound (literature numbers, Gaillard–Wu hep-th/9605170).** BGW give
m_3/2 = (b/4)√⟨ūu⟩ (eq. 3.38), b = C/8π² = 0.380 for E₈, with no T-dependence; their worked example (A_f = 6.92) settles at ⟨ℓ⟩ = 0.45 with
m_3/2 = 7.6×10⁻⁵ M_P = 1.9×10¹⁴ GeV. Against the Twist's H_inf = 6.1×10⁻⁶ M_P (1.5×10¹³ GeV): m_3/2 ≈ 12 H_inf. The dilaton mass in this class
is enhanced over m_3/2 by ~1/b² (≈ 7; an estimate, not from the paper), so m_ℓ ≈ 90 H_inf — the dilaton is stable during inflation (D201 (iv)
satisfied). Condensation scale ~0.09 M_P ≈ 2×10¹⁷ GeV. D201's loop bound (m_3/2 ≲ 0.1 M_P) is met by ~10³. Implications: supersymmetry is
broken at ~10¹⁴ GeV — no superpartners at colliders (a genuine prediction of this home), the Higgs mass hierarchy is not explained by SUSY,
and the gravitino (10¹⁴ GeV) decays long before nucleosynthesis. Caveat: the numbers are BGW's example parameters (A_f chosen by them);
m_3/2 depends exponentially on ⟨ℓ⟩, so it is a plausibility check, not a derivation.

**D203 — TWIST-M9's weak coupling today is NOT automatic: it needs strong reheating (estimate).** D196 took today's x ≈ 89 from the Twist.
But in TWIST-M9 inflation ends at x ≈ 11.5 instead of 0.0088, and the kination run after the cliff is set by the heat share f. Calibrating on
the Twist (0.0088 → freeze at 73 for f = 0.8%) gives Δφ ≈ 2.29 ln(1/f). Then for TWIST-M9: f = 0.8% → freeze at x ~ 10⁵, T_het ~ 1300,
g_s ~ 3×10⁴ (strongly coupled — the M9 advantage is lost); f = 5% → g_s ~ 200; f = 20% → g_s ~ 4; landing at x ≈ 73–89 needs f ≈ 0.33–0.37.
Weak coupling (g_s < 1 ⇔ x ≲ 91 today) therefore requires a third or more of the inflaton energy to become heat at the cliff — ~45× the
Twist's preheating efficiency, and with an upper edge (x ≲ 91) so it is also a tuning. Caveats: the calibration assumes the same kination
physics (Δφ ∝ ln(1/f)) and the same thawing; the actual M9 heating (χ's coupling must be re-placed at the new cliff) is not computed.
**Verdict:** TWIST-M9 trades the strong-coupling problem for a reheating requirement f ≈ 0.35 ± 0.02 — a new, checkable condition and a
fine-tuning. Together with its lower n_s, M9 is a weaker candidate than first appeared; the heterotic-home question remains open at this point.

**D204 — TWIST-M9 freeze/thaw computed (theory/inflation/m9_freeze_d204.py; results/m9_freeze_d204.txt): weak coupling today is out of reach.**
Full D185 machinery with the M9 potential. Heat share → frozen x, today x, g_s today: 0.8% → 1.98×10⁴, 2.43×10⁴, 4.4×10³; 5% → 3147, 3862, 279;
20% → 771, 946, 34; 35% → 432, 530, 14; 50% → 297, 364, 8.1. Today's x falls only ~1/f, so even 100% heat would leave x ≈ 180 and g_s ≈ 3;
weak coupling needs x ≲ 91. The dark energy is unaffected (w0 −0.900, wa −0.145 at every heat share — the leftover is negligible this far out).
This corrects D203 (its calibration ignored the late thaw and the different post-cliff dynamics; it said f ≈ 0.35 suffices — wrong) and
D196 (which assumed today's x = 89). **Verdict:** no version found has weakly coupled heterotic strings today: degree 1 gives g_s ≈ 26
(D164), degree 9 gives g_s ≳ 3 even with total reheating. Today's Twist field sits in the strongly coupled (Hořava–Witten) regime in
every heterotic realisation tried, where the shield's protections (no T in the SM couplings, rung 3) fail (D154, D184). The string home is
therefore OPEN again at the level of "no known setting"; the effective-theory shield (PREREG_SHIELD) stands as an assumption, not a derivation.

**D205 — why weak coupling today is structurally hard, and the pivot to heterotic M-theory (rung 4; locked PREREG_TWIST4).**
Structural reason behind D164/D204: at fixed 4-d gauge coupling g_s ≈ g_YM R³, so weak coupling needs R within ~0.9–1.1 of the self-dual
radius — a window of only Δφ ≈ 0.5 M_P in the canonical field, while the Twist's history spans ~16 M_P and today's point is set by
reheating and thawing, not by the self-dual point. Landing inside that window today would be a coincidence. The natural regime for a
far-travelled modulus is the strongly coupled one: heterotic M-theory, where the 11-d description is valid at large orbifold length. There:
the matter-neutral direction is rung 4 (D184); there is no exact T-duality (D194's issue absent); open-membrane instantons between the walls
give e^{−aT} terms (a natural cliff source); the visible threshold f = S + εT that broke the shield in D154 vanishes when the two walls carry
equal instanton numbers with no five-branes (the symmetric case; literature to be checked). Rung-4 inflation (rung4_inflation_d205.py, E-model
check reproduces Starobinsky): n_s 0.9644–0.9652, r 0.0045–0.0047 after the rung-3 offset; late predictions D187. Locked as PREREG_TWIST4
(future data only, both rung readings reported). Status: the most consistent home found is heterotic M-theory with the Twist on rung 4;
r ≈ 0.0046 instead of 0.0036 and w0 −0.925 instead of −0.899 are the observable differences. n_s and n are unchanged problems.

**D206 — the heterotic-M-theory home has a known matter-neutral class: symmetric vacua (literature check, hep-th/9908100).** Benakli/Donagi–
Lukas–Ovrut–Waldram-type "symmetric vacua" (c₂(V₁) = c₂(V₂) = ½c₂(TX), no five-branes) have, per the abstract, gauge kinetic functions with
"no perturbative threshold corrections", no corrections to the matter Kähler metric, and flat space as the 5-d vacuum; the βᵢTⁱ threshold
(the εT that broke the shield in D154) vanishes exactly. They exist on some complete-intersection Calabi–Yaus (not on elliptically fibred
ones) and can give three generations. So need C (neutral matter) is satisfied at the perturbative level in a concrete, published class of
heterotic-M-theory vacua — at strong coupling, where D204 says the Twist's field actually is. Remaining for this home: (i) the rung of the
direction the Twist moves along must be checked in symmetric vacua specifically (D184 gave 4 for the generic matter-neutral direction; with
β = 0 the matter metric has no T correction, so fewer moduli may need to move — could even restore rung 3); (ii) the cliff from open-membrane
instantons in E(T) form; (iii) dilaton/orbifold-length stabilisation (BGW-type analogue at strong coupling); (iv) n. Status: best home so far.
D206 add — point (i) settled: symmetric vacua do NOT restore rung 3. Witten's tree-level relations G_N = κ²/(16π²Vρ), α_GUT = (4πκ²)^{2/3}/(2V)
give G_N M_GUT² = (2α_GUT)^{3/2}/(64π³ ρM_GUT): at fixed coupling, M_GUT/M_P ∝ (ρM_GUT)^{−1/2}, i.e. ∝ T^{−1/2}. Moving T alone gives every
matter scale a universal coupling β = (1/2)/√(3/2) = 0.41 (Cassini: 3.4×10⁻³) — a tree-level effect that the vanishing thresholds do not
remove. So the matter-neutral direction must move several moduli together, which is D184's rung 4. Symmetric vacua remove the
threshold/matter-metric leaks along that direction; the rung stays 4 and PREREG_TWIST4's numbers stand.

**D207 — the rung-4 home needs a different superpotential: W linear in T is special to rung 3 (algebra).** With K = −3α ln(u − gE SS̄ + …)
and W = c S Tᵖ, at S = 0: W = 0, D_S W = c Tᵖ, K_SS̄ = 3α gE/u, so V = e^K K^{SS̄}|W_S|² = u^{−3α} · u/(3α gE) · c²|T|^{2p} ∝ u^{2p+1−3α}/(gE).
A plateau (V → const on the rim apart from g and E) needs p = (3α − 1)/2: p = 1 for rung 3 — exactly the Twist's √3 m S T — but p = 3/2 for
rung 4. A half-integer power of T is not a natural superpotential (branch cut at T = 0; T^{3/2} cannot arise from integer instanton
expansions). With integer p on rung 4: p = 1 gives V ∝ 1/u (rolls away from the rim — no plateau), p = 2 gives V ∝ u (rolls to the rim).
So PREREG_TWIST4's "same plateau shape on rung 4" assumes a superpotential the rung-4 home does not obviously supply; in heterotic M-theory
the effective field is a combination of S, T and the CY volume, so W along that direction need not be a pure power — this must be built
before the rung-4 inflation numbers are trusted (the late-universe numbers, set by the tail slope 1/√2, do not depend on it). Caveat added
to PREREG_TWIST4 by deviation file, not by editing the lock.
D207 add — a selection rule falls out: an integer-power plateau superpotential needs p = (3α − 1)/2 ∈ ℤ, i.e. 3α odd — rungs 1, 3, 5, 7
(p = 0, 1, 2, 3). Even rungs (2, 4, 6) need half-integer powers. This overlaps with, but is not the same as, the octonion-closure set
{1, 3, 7} of D175 (rung 5 passes here, fails there). Rung 3 is the only rung in both sets with p = 1, the simplest S·T coupling.
A mild structural argument for rung 3; it does not by itself choose the string setting.

**D208 — CORRECTION to D205–D206: the rung-4 path in heterotic M-theory changes the Standard-Model gauge coupling.** D184's own output
says it: the scale-preserving HW path has a_S = −1 per unit ln T (S·T fixed), and "gauge coupling 1/g² = Re S also varies along any path with
a_S ≠ 0". With symmetric vacua f = S exactly, so along the rung-4 direction d ln α/dφ = 1/√2 ≈ 0.71 — a thaw of Δφ ~ 0.1 since z ~ 1 would move
α by ~7%, against quasar/clock bounds ~10⁻⁶. So the rung-4 "home" of D205–D206 is NOT matter-neutral; I missed D184's caveat. Holding BOTH
the scale and the coupling fixed in HW forces Re S fixed AND the orbifold length fixed, leaving only Calabi–Yau SHAPE moduli at fixed volume.
Example (K3/T⁴-fibred volume t₁t₂², path t₁ = e^σ, t₂ = e^{−σ/2}): k_eff = 1 + 2·¼ = 1.5, i.e. "rung 1.5", tail slope λ = √(2/1.5) = 1.155.
Late universe for λ = 1.155 (late_predictions_rung.py, LAM=1.155): w0 −0.79, w(0.5) −0.89, H up to +4.1%, D_M short ~3% at z ≈ 0.5–1,
σ8 −3.2%, f σ8 −7% at z ≈ 0.3–0.5 — signals ~2× the Twist's, likely in tension with DESI DR2 BAO at the ~1% level (not fitted here).
Shape moduli are also not rung 3, so the inflation sector would have to change too (D207: integer-power plateau needs odd rungs).
**Status after the correction:** PREREG_TWIST4 stays locked (locks are not withdrawn) but is marked VOID-AS-HOME by deviation D2: its numbers
describe a direction that is not matter-neutral. Every heterotic home examined fails at least one need today: weak coupling unreachable
(D204); HW rung-4 path moves α (this note); HW shape moduli give a steep tail and are not rung 3. The string home is OPEN; the shield is an
effective-theory assumption (PREREG_SHIELD), which is where it stood before today's string work — now with the obstructions mapped.

**D209 — a general obstruction for question 9 (perturbative strings with matter at the string scale).** For any 10-d string compactification,
M_P² ∝ M_s² V/g_s² (V in string units), so (M_s/M_P)² ∝ g_s²/V. If the Standard Model's scales track M_s (true for heterotic, and for D-brane
matter in IIA/IIB), a direction that grows the overall volume (the rung-3 field, x ∝ V^{1/3}) keeps the SM scale fixed ONLY if g_s² ∝ V,
i.e. g_s ∝ x^{3/2}. Two ways to read it: (a) fix g_s (IIB-like) → the SM scale drifts, β ≈ 0.61 (D150, D192); (b) fix the 4-d dilaton
(heterotic, IIA with D6-branes) → the 10-d coupling grows as x^{3/2}. Case (b) is weakly coupled only where V ≲ 1/g_YM² ~ 2, i.e. at the string
scale. The Twist can sit there today only if the cliff's instanton is calibrated so that today's x maps to V ~ 1: degree d ≈ x_today/10 (D164).
That calibration plus T-duality (which needs the cliff near the self-dual point, D194–D195) plus the computed post-cliff roll (which carries the
field ~10²–10⁴ times further, D204) are mutually incompatible in every version built. IIA with D6-branes has the same structure as heterotic
(gauge couplings set by complex-structure moduli, f independent of Kähler T; Yukawas instanton-suppressed) — it inherits case (b) and the
same strong-coupling problem, going over to M-theory on G₂ manifolds, where the overall-volume direction is a different rung (K = −3 ln V₇
gives 3α = 7 for the overall scaling) — not checked further.
**Verdict:** "rung 3 + neutral matter + weak coupling today" is obstructed generically, not just in the examples: a matter-neutral volume
direction in a perturbative string drives the 10-d coupling up as x^{3/2}. A home needs either matter whose scale does NOT track M_s (non-
perturbative / strongly coupled sectors), or a rung-3 direction that is not the overall volume. Recorded as the precise form of question 9.

**D210 — a lead that evades D209: the IIB overall COMPLEX-STRUCTURE modulus with D3-brane matter (theory/string_home/iib_complex_structure_d210.py).**
D209's obstruction is for a VOLUME direction. On a factorisable T⁶ orientifold the overall complex-structure modulus U (all three tori
stretched alike, volume fixed) has K = −3 ln(U + Ū): rung 3. Tree level, with SM matter on D3-branes:
- D3 gauge coupling f = S: U-independent. M_s/M_P ∝ g_s^{1/4} V^{−1/2}: U-independent. 10-d coupling g_s = 1/Re S: U-independent — so moving U
  never drives the string to strong coupling (the failure of every heterotic version, D204/D209, is absent).
- D3–D3 matter metric Z_i ∝ 1/(t_i u_i) (from hep-th/0404134's D5 metric 1/(s u₁) by T-duality on T²₁; flagged as derived, not quoted) ⇒
  physical Yukawa Y = e^{K/2}W/√(Z₁Z₂Z₃) = W/√s: independent of every u_i AND t_i (sympy check).
- Complex-structure moduli space has no α′ corrections in IIB; its large-complex-structure periods carry exponentials e^{2πiU} (mirror of
  worldsheet instantons) — a natural source of the cliff's e^{−aU} form.
- Geometry at today's value (u ≈ 89): a T² of area 89–300 string units has radii ~89–160 and ~1–1.8 string lengths — KK modes of the long
  direction at ~M_s/100, harmless at the M_s implied by these volumes.
So this is the FIRST setting found with rung 3 + neutral matter + weak coupling holding simultaneously at tree level.
**Open (in order of danger):** (1) string loops: Berg–Haack–Körs-type corrections carry Eisenstein series E₂(U) ≈ 2ζ(4)(Im U)², i.e. a KK
Casimir term GROWING as u²/(s t): rough size δK ~ 10⁻³ at u = 89 (s ~ 10, t ~ 90) — if it enters the D3 matter metric at that size it gives
β ~ 10⁻³, near Cassini and probably over composition-dependent EP/clock bounds; this needs the actual one-loop matter metric. (2) SL(2,Z)_U is
a geometric symmetry of each torus (u ↔ 1/u relabels cycles): plateau (small u) and tail (large u) must be made distinct — D7-branes or flux
on specific cycles break it to Γ₀(N) (D194's mechanism carries over). (3) Fluxes usually fix U: the construction needs U left unfixed by
flux (its potential then comes only from the Twist sector). (4) The helper field and the S·U coupling: GVW flux superpotentials are polynomial
in U (terms linear in U are standard), suggestive but not built. (5) n. Status: a genuine new lead; the shield's string home is no longer
"none known" at tree level — it is "IIB complex structure with D3 matter, pending a one-loop check".

**D211 — the D210 lead fails at one loop (rough estimate, theory/string_home/iib_oneloop_d211.py).** Berg–Haack–Körs (hep-th/0508171 eq. 12)
give K⁽¹⁾ = (1/256π⁶) Σ [E₂^{D3}(A_I, U_I)/((S − S̄)(ρ_I − ρ̄_I)) + E₂^{D7}(0, U_I)/(…)]. The D3 position/matter fields A sit INSIDE the Eisenstein
function, so the one-loop D3 matter metric depends on U. Its leading piece comes from the KK modes of the torus's long direction (radius ∝ √U)
and grows ∝ Im U: δZ/Z ≈ 8πU₂·4π²ζ(2)·c/(256π⁶ Re S) ≈ 6.6×10⁻³ c U₂/Re S. With the Standard Model on the D3-branes its coupling FIXES
Re S = 1/g² ≈ 2, so at today's U₂ ≈ 89: δZ/Z ≈ 0.3 (c = 1) to ~40 (c = 128, BHK's brane-multiplicity coefficient), β ≈ 0.1–16 — 30× to 5000×
over Cassini, and growing with U rather than falling as 1/x⁴. Even Re S = 100 leaves β ≈ 2×10⁻³–0.3. Caveats: order-of-magnitude (the
normalisation of A and the exact E₂(A,U) expansion are not done carefully); but the GROWTH ∝ U is robust — it is the decompactifying
direction's KK tower (the distance-conjecture tower) coupling to brane matter at one loop.
**Verdict:** the IIB complex-structure direction is neutral at tree level but not at one loop; it fails for the same structural reason that
every "move far in moduli space" route fails: something becomes light (KK tower here, strong coupling in heterotic) and couples to matter.
This is a general lesson for question 9: a field that travels ~16 M_P will, in every string setting examined, make some tower light enough
to break matter neutrality by the time it reaches today's value. The string home is open; the shield remains an EFT assumption.

**D212 — the Twist's dark-energy tail sits EXACTLY on the Trans-Planckian Censorship bound (theory/darkenergy/tcc_rungs_d212.py).**
Bedroya–Vafa (arXiv:1909.11063, eq. 19) derive (|V′|/V)_∞ ≥ 2/√((d−1)(d−2)) in the asymptotic region of field space; in 4-d this is
√(2/3) = 0.8165. On rung 3α = k the tail slope is λ = √(2/k): rung 3 gives λ = √(2/3) — equality, to every digit. Rungs 4–7 (λ 0.71–0.53)
VIOLATE the bound; rungs 1–2 satisfy it. Combined with D207 (integer-power plateau superpotential needs an odd rung), the allowed set is
{1, 3}. Rung 1 (λ = √2) gives w0 −0.68, σ8 −5.4%, H +5.8% at z = 0.3, D_M short 3.3% (LAM=1.414 run) — signals ~3× the Twist's, very likely
excluded by DESI DR2 (not fitted). So rung 3 is the SHALLOWEST tail TCC permits and the only TCC-allowed odd rung compatible with the
data's mild w0 ≈ −0.9 — a selection argument for rung 3 independent of the octonion story (D175) and of r.
Consequences: (i) the HW rung-4 alternative (D187, PREREG_TWIST4) violates TCC — a third strike against it; (ii) the Twist makes a sharp
swampland-facing prediction: today's dark energy is an exponential tail with the minimal TCC slope, so any measurement implying a
shallower asymptotic slope (w0 closer to −1 with the same thawing shape, e.g. w0 > −0.93 with |wa| small) would push it into TCC
violation; (iii) caveats: TCC is a conjecture; the bound is asymptotic and the Twist's tail is asymptotic only up to e^{−πx/4} leftovers
(negligible today). This is a genuine structural plus: the "rung 3" that the cosmology picked is exactly where quantum-gravity
consistency (as conjectured) puts its edge. It also matches the observation that no-scale (K = −3 ln) exponentials saturate TCC, which
is known in the swampland literature — so this is a recognition, not a discovery.

**D213 — the same conjecture cuts the other way for inflation (honesty check on D212).** Bedroya–Brandenberger–Loverde–Vafa (1909.11106)
apply TCC to inflation: "the energy scale of inflation has to be lower than 10⁹ GeV" and ε < 10⁻³¹, i.e. negligible r. The Twist's inflation has
V^{1/4} ≈ 7.9×10¹⁵ GeV (r = 0.0036) — 8×10⁶ over that bound — and ε = 2×10⁻⁴. So TCC, taken at face value, EXCLUDES the Twist's inflation
(as it excludes every standard high-scale plateau model, Starobinsky included), while its asymptotic-slope form (D212) singles out the
Twist's dark-energy tail. One cannot use TCC selectively: either (a) TCC holds in its strong form, and the Twist's inflation sector — like
all detectable-r inflation — is ruled out, with r ≈ 0.0036 detection by LiteBIRD/CMB-S4 then falsifying TCC itself; or (b) TCC is too strong
(several papers argue the inflation bound can be relaxed, e.g. 2001.00040), and D212 is only a suggestive coincidence. Recorded framing:
D212 is a consistency observation, NOT support; the r measurement will test the Twist and the strong TCC against each other — a sharp,
two-sided outcome worth stating in the paper.

**D214 — neutrino masses: a Giudice–Masiero-type Majorana mass at the gravitino scale (lead, conditional).** TWIST-K dropped the hidden
SU(8) that D173 used to place the seesaw scale. A standard replacement: a Kähler term (c/2) N N + h.c. for right-handed neutrinos gives a
Majorana mass M_R ≈ c·m_3/2 once supersymmetry is broken (the Giudice–Masiero mechanism applied to N). With the BGW E₈ example's
m_3/2 ≈ 2×10¹⁴ GeV (D202) and Dirac Yukawa y: m_ν = y²v²/M_R = 0.15 y² eV — y ≈ 0.6 gives 0.05 eV (the atmospheric scale), y ≈ 0.1 gives
0.0015 eV; the full seesaw window 6×10¹²–6×10¹⁴ GeV (D173) brackets it. So high-scale supersymmetry breaking, which the dilaton-stability
argument (D201–D202) needed anyway, puts the seesaw scale where the data want it with order-one Yukawas, and the Twist's own matter
mechanism (lepto-axiogenesis via the angle) does not need thermal leptogenesis from N. Caveats: this relies on the BGW sector, whose string
home failed the shield test today (D204–D211); within the effective theory it is a coherent, optional add-on, not a prediction.

**D215 — what "n is chosen" costs statistically: the Twist turns the cosmological-constant problem into a prior on n.** Today's dark energy
scales as ρ_DE ∝ m² e^{−2n}: one unit of n moves ρ_DE by e² ≈ 7.4, one decade is Δn = 1.15. Two readings of "n is an input":
(a) n comes from integers in some sector (flux numbers, instanton degrees — D166, D188): then a flat distribution over those integers is
a LOG-FLAT distribution over ρ_DE. Weinberg's anthropic argument works because a prior flat in ρ (near ρ = 0) favours values near the upper
anthropic bound (~10²–10³ ρ_obs), so the observed value is unsurprising. A log-flat prior gives equal weight per decade all the way down,
so the chance of landing within a decade of the observed value is ~1/(number of allowed decades) — 1/12 to 1/120 for a lower cut-off 10–120
decades below — the anthropic explanation largely fails unless something caps how small ρ_DE can be. (b) n is continuous and only the
combination m² e^{−2n} is scanned (as Λ is in ΛCDM): then the Twist inherits exactly Weinberg's argument and is no worse than ΛCDM.
**Status:** the Twist does not solve the cosmological-constant problem (stated since D129); this note sharpens what it would take to
explain n: either a mechanism fixing n, or a landscape in which the dark-energy SCALE (not n) is uniformly scanned near zero. If the cliff
depth really were a flux integer, the Twist would be in a statistically worse position than a bare Λ — a point a referee would raise.
D215 correction (same session, after running the numbers): the comparison above overstated the case. With a log-flat prior the chance of
landing within a decade of the observed value is 8% (cut-off 10 decades down), 1.6% (60), 0.8% (120); the simple uniform-in-ρ estimate for
Weinberg's case, P(ρ < ρ_obs | ρ < 200 ρ_obs), is ~0.5% (careful galaxy-weighted versions give ~5–10%). So the integer-n reading is NOT clearly
worse than a bare Λ — the two are comparable unless the log-flat range is extremely deep. Revised status: n chosen costs about the same as
Λ chosen; neither is explained; no extra penalty for the Twist from this argument. The "referee point" sentence above is withdrawn.

**D216 — the leak's redshift shape tells WHICH kind of leak it is (theory/darkenergy/leak_shape_growing_d216.py).** PREREG_SHIELD item 2
fixed the fingerprint Δα(z)/Δα(z=1) for leaks that FALL as x^{−p}, p = 3–4 (what atomic clocks allow in an EFT shield). Today's string survey
found the generic leaks GROW with the field (∝ x from a KK tower, D211; ∝ x^{3/2} from strong coupling, D204/D209). Since the field moved only
0.20 M_P since z = 1 (0.24 since z = 3), every leak is close to linear in Δφ and the shape changes only mildly with p:
| p | z = 0.14 | 0.5 | 2 | 3 | 6 |
| 4 | 0.218 | 0.655 | 1.254 | 1.327 | 1.374 |
| 3 | 0.233 | 0.672 | 1.232 | 1.299 | 1.340 |
| 1 | 0.263 | 0.706 | 1.193 | 1.247 | 1.280 |
| −1 (KK tower) | 0.296 | 0.739 | 1.160 | 1.202 | 1.228 |
| −1.5 (strong coupling) | 0.305 | 0.747 | 1.152 | 1.192 | 1.217 |
So a string-type (growing) leak sits OUTSIDE the locked band (0.22–0.23 at z = 0.14; 1.23–1.25 at z = 2) by 0.07–0.10 — distinguishable
with ~3% shape precision, which a future joint clock + quasar data set could reach only if a leak is detected well above threshold.
Both shapes keep "almost nothing new above z ≈ 3" (ratio ≤ 1.38), so the DISFAVOURED-shield clause (z > 3 more than 1.5× the z = 1 value)
is unaffected. Added as a reported (non-verdict) quantity by PREREG_SHIELD deviation D2: if a leak is detected, fit p and report whether
it is falling (EFT shield with perturbative leaks) or growing (tower/strong-coupling leak, the string-generic case).

**D217 — lumpy starts: the Twist-specific risk is the helper's tachyon edge, and it is set by ζ (theory/inflation/lumpy_tachyon_d217.py).**
D122 placed the Twist in the robust plateau class by analogy (super-Planckian plateau scale 1.22 M_P). The model-specific danger is that S is
tachyonic for x < x_b = 1/(4ζ) (m_S²/H² = −2 + 8ζx, D136): an inhomogeneous patch whose field starts deeper than x_b does not inflate along the
Twist's path. With the model's ζ = 3×10⁴: x_b = 8.3×10⁻⁶, leaving 3.4 M_P of stable plateau beyond the CMB point and at most ~900 e-folds from the
edge (check: the code reproduces N* = 55.7 from the CMB point). Plateau-model simulations (D122) need patches that start a few M_P up the
plateau; 3.4 M_P is marginal for large initial gradients. ζ only shapes S's quartic term — with S = 0 along the path it changes none of the
predictions — and the stable range grows as ln ζ: ζ = 3×10⁵ → 6.2 M_P (9×10³ e-folds), 3×10⁶ → 9.1 M_P, 3×10⁸ → 14.7 M_P. So the lumpy-start
risk is removable by a larger ζ at no observational cost; the remaining limit is the distance-conjecture tower floor deep on the plateau
(D123), which a larger stable range runs into first. Status: "robust by analogy, provided ζ ≳ 3×10⁵ (a free, unobservable coefficient)";
noted as a recommended model-card change, not applied (changing a coefficient after the fact would need its own consistency re-run).

**D218 — ζ = 3×10⁵ adopted after a full re-run (theory/kahler_cliff/zeta3e5_check_d218.py; results/zeta3e5_check_d218.txt).** Full two-field
supergravity check of TWIST-K with ζ = 3×10⁵: V along the path equals the Twist's to 10 digits at x = 5×10⁻⁷, 1.3×10⁻⁴, 0.01, 1, 89; the angle stays at
+4H² everywhere; m_S²/H² = 310 (CMB point), 2.4×10⁴ (cliff), 6×10⁵ (x = 1), 2.6×10⁴ (today); and at x = 5×10⁻⁷ m_S²/H² = −0.8, matching the formula
−2 + 8ζx (edge x_b = 8.3×10⁻⁷) — a check of the D217 analysis. No observable changes (S = 0 along the path). Model card updated; the lumpy-start
status becomes "robust by analogy, with 6.2 M_P of stable plateau beyond the CMB point".
D218 correction — the gain is mostly cut off by the tower floor. D123 (volume-modulus assumption, winding modes m ~ M_P x for x < 1) puts the
EFT's edge where the tower reaches H, at x ≈ 6×10⁻⁶ — HIGHER than the new tachyon edge (8.3×10⁻⁷). So the usable plateau beyond the CMB point is
set by the tower, not by ζ: 3.8 M_P (tower = H) or 2.4 M_P (tower = 3H), versus 3.4 M_P with the old ζ. Raising ζ removes the S-tachyon as the
binding limit (worth keeping: the potential and all predictions are unchanged) but gains only ~0.4 M_P; "6.2 M_P" in D218 and the model card
is withdrawn. Lumpy-start status: "robust by analogy, ~2.5–3.8 M_P of plateau beyond the CMB point inside the EFT (tower-limited, under the
volume-modulus assumption)".

**D219 — strong CP next to the Twist: only a post-inflationary QCD axion survives (theory/observables/axion_isocurvature_d219.py; estimate).**
(i) The shield forbids the Twist's own angle from being the QCD axion: a θ-term coupling Im T·GG̃ comes from a gauge kinetic function f_SM ⊃ cT,
whose real part is exactly the Re T–gauge coupling the shield excludes (D140, D198). (ii) Any OTHER axion with its Peccei–Quinn symmetry
broken during inflation gets quantum spread δθ = H/(2πf) with H_inf = 1.5×10¹³ GeV; requiring axion isocurvature below Planck's bound
(S_rms < 9×10⁻⁶) needs θ_i below its own spread for every f from 10¹⁰ to 10¹⁶ GeV — excluded (the standard tension between detectable r and
pre-inflationary axions). (iii) What remains: PQ symmetry restored during or after inflation (f ≲ H_inf), i.e. a post-inflationary,
field-theory QCD axion; if it is the dark matter, lattice results put m_a ≈ 40–180 μeV. Prediction (conditional on the Twist's r and an
axion solution of strong CP): haloscopes should find the axion, if at all, in the ~40–600 μeV range (MADMAX, ALPHA-class), and string-scale
(f ~ 10¹⁶ GeV) axions — including the heterotic model-independent axion — cannot be the solution unless their mass is lifted during
inflation. Generic to any detectable-r inflation, stated here as a Twist corollary.

**D220 — online literature on the n_s problem, and TWIST-G− (locked PREREG_TWISTGN, results/twistgn_scan.txt).** Recent papers (2025–26) show
the α-Starobinsky family reaches the ACT n_s ≈ 0.974 by (a) a multiplicative power tilt V(1 − u)² u^{−δ√α} with δ ≈ 0.017 (arXiv:2606.24131),
(b) an added log term δL(u)^p (same paper), (c) a Coleman–Weinberg factor 1 + δ ln φ (arXiv:2506.12436; small effect at α ≈ 1), or (d) a
plateau truncated to a power-law approach (arXiv:2609.10991, n_s ≈ 1 − 4/(3N)). Our files already held (b)/(c)-type (TWIST-L) and (d)-type
(TWIST-P); (a) was new. In the Twist it is W = √3 m S T^{1+γ}: a small non-integer power, the form of an anomalous dimension.
Run (after locks; the first lock PREREG_TWISTG had the sign wrong — deviation D1 — its γ ≥ 0 branch LOWERS n_s and is recorded as such):
| γ | n_s (N* 55.7/57) | r | asymptotic tail slope |
| 0 | 0.9642/0.9650 | 0.0037/0.0036 | 0.8165 (= TCC) |
| −0.005 | 0.9703/0.9710 | 0.0054/0.0052 | 0.8247 |
| −0.0085 | 0.9740/0.9747 | 0.0069/0.0067 | 0.8304 |
| −0.012 | 0.9772/0.9780 | 0.0087/0.0084 | 0.8361 |
γ ≈ −0.0085 lands on the ACT central value with r ≈ 0.007. Three properties worth recording: (i) |γ| ≈ 1.3/(16π²) — the size of a one-loop
anomalous dimension, so the needed effect is naturally loop-sized; (ii) the sign that raises n_s also makes the dark-energy tail STEEPER
(λ = √(2/3)(1 − 2γ)), so TWIST-G− stays on the allowed side of the TCC bound — unlike a positive tilt; (iii) dark energy barely moves: w0
−0.895 vs −0.899, σ8 −1.53% vs −1.47% (LAM = 0.8304 run). Status: post-data, locked, scored only on future CMB data. It sits close to
TWIST-L's curve (TWIST-L: n_s 0.9735 at r 0.0073; TWIST-G−: 0.974 at r 0.0068), so future data will hardly separate those two, but both
separate from TWIST-P (higher r) and TWIST-M9 (lower n_s). Not done: a full two-field supergravity check of W ∝ T^{1+γ} (branch cut on the
negative real axis, irrelevant for Re T > 0) and a derivation of γ from a specific loop.
**D221 — TWIST-G− passes the full two-field supergravity check (theory/kahler_cliff/twistgn_sugra_d221.py; results/twistgn_sugra_d221.txt).**
γ = −0.0085, ζ = 3×10⁵: V/V_Twist = x^{2γ} exactly as intended (1.164 at the CMB point, 1.081 at the cliff, 1 at x = 1, 0.927 today — the
tilt and nothing else); m_S²/H² unchanged (310, 2.4×10⁴, 6×10⁵, 2.6×10⁴); the angle's mass is +3.966 H² everywhere (vs +4 at γ = 0) — stable.
So TWIST-G− is a consistent supergravity model; what is missing is a derivation of γ ≈ −0.0085 from a specific loop.

**D222 — where a loop-sized γ in TWIST-G− could come from (sketch with literature; not a calculation).** V ∝ e^K K^{SS̄}|W_S|², so W ∝ S T^{1+γ}
is equivalent to the helper's metric carrying an extra factor u^{−2γ} = u^{+0.017}: a small shift of the helper's effective modular weight.
Antoniadis–Gava–Narain–Taylor (hep-th/9212045) show one-loop string corrections to matter Kähler metrics contain an infrared part that
reproduces the field-theory anomalous dimensions plus a moduli-dependent part. In effective-field-theory language: if the scale at which the
helper's wavefunction Z_S is evaluated depends on T as μ ∝ u^a, running gives Z_S ∝ u^{a γ_S}; matching needs a·γ_S ≈ 0.017 — γ_S ≈ 0.017
(a = 1), 0.034 (a = ½), 0.051 (a = ⅓), i.e. 2.7–8/(16π²): one-loop size, e.g. order-one Yukawa couplings of S to a handful of fields.
Catch: with full modular invariance the loop combination is ln[(T + T̄)|η(T)|⁴], not ln(T + T̄); at the plateau (T → 0, the dual cusp) that
gives an exponentially flat factor, NOT a power tilt — so the TWIST-G− mechanism needs the modulus NOT to have exact SL(2,Z) duality (fine in
the effective theory and in settings without exact T-duality; under the Γ₀(9) option of D194 the behaviour at the cusp 0 must be checked).
Status: natural size and a plausible mechanism identified; no explicit model computes γ.

**D223 — the n_s problem is mostly the BAO–CMB tension (literature, arXiv:2512.05108).** Published n_s (ΛCDM, no lensing): CMB alone — Planck
0.9638 ± 0.0040, ACT 0.9666 ± 0.0076, SPT 0.948 ± 0.012, CMB-SPA 0.9693 ± 0.0029; adding DESI BAO shifts each up (+0.004 to +0.010): CMB-SPA + DESI
0.9737 ± 0.0025. The authors attribute the shift to the BAO–CMB tension (n_s is partly degenerate with the BAO-sensitive parameters). The
Twist's 0.9645 sits −1.7σ from CMB-SPA alone, −0.2σ from Planck, +1.4σ from SPT, but −3.7σ from CMB-SPA + DESI; TWIST-G− (0.9743) is the mirror
image (+0.2σ vs CMB-SPA + DESI, +1.7σ vs CMB-SPA alone, +2.6σ vs Planck, +2.2σ vs SPT). So the INCONSISTENT verdict (D157) is a statement about CMB + BAO jointly. Our own
NS-SPA run already tested the natural hope that the Twist's dynamical dark energy would relieve the BAO–CMB tension and found it does not
(free-n_s minima 0.973–0.976 with the PURE background, D157 context). Practical consequence: which branch survives (Twist vs TWIST-G−/L) will be
decided as much by how the BAO–CMB tension resolves (DESI DR3, Simons Observatory) as by n_s itself — worth stating in the paper.

**D224 — swampland-review check of today's string conclusions (literature: "Hitchhiker's Guide to the Swampland", arXiv:2509.02632).**
Consistent with D209–D213: (i) the TCC bound s₁ ≥ 2/√((d − 1)(d − 2)) = 2/√6 in 4-d is quoted (our D212 slope check); (ii) for quintessence
coupled to matter at gravitational strength, fifth-force limits need (|∇V|/V)² ≲ 10⁻⁵ (Chiang–Murayama) — incompatible with any O(1) slope,
which is why the Twist needs an exact shield, not a small coupling; (iii) the review's stated escape — "fifth forces are avoided if the
modulus is localised in the extra dimensions, away from the SM" — is sequestering by locality, which D192 showed fails for the overall volume
and which for a local (blow-up) modulus does not give rung 3. One tension flagged for follow-up: the review cites Tosone et al. finding
∇V/V ≲ 0.31 for thawing exponential quintessence (pre-DESI-DR2 data, as quoted); our own DR2-era fits prefer the Twist's 0.82 slope over ΛCDM
(Δχ² −3.4), so the data preference has moved — but a referee may cite the older bound; the paper should quote the DR2-era result explicitly.
D224 add — resolved with DR2-era literature (arXiv:2504.04226): an exponential-quintessence fit to DESI DR2 with other data gives
λ = 0.698 +0.173/−0.202 (flat; 0.722 with curvature free), a ~3.5σ preference for λ ≠ 0 and a 3.3–3.8σ preference over ΛCDM. The Twist's
λ = √(2/3) = 0.8165 sits +0.7σ from that central value; rung 4 (0.707) would sit at the centre, rung 1 (√2) is 4σ off. The older
"∇V/V ≲ 0.31" bound is superseded by DR2. Note the irony worth stating in the paper: the data's central slope (0.70) is slightly BELOW the
TCC bound (0.8165); the Twist sits exactly on the bound and +0.7σ above the data's central value — data and the conjecture pull in opposite
directions by less than 1σ, and DR3 will sharpen this.

**D225 — how exact the shield must be TODAY, from current clocks (literature + computation).** The best laboratory drift bound is
α̇/α = (1.8 ± 2.5)×10⁻¹⁹ /yr (Yb⁺ E3/E2 ratios, quoted in the ²²⁹Th review arXiv:2606.26600). The Twist's field moves today at dφ/dN = 0.457,
i.e. 3.2×10⁻¹¹ M_P/yr. So any coupling of α to the field must satisfy |d ln α/dφ| < 1.6×10⁻⁸ (2σ) — five orders of magnitude tighter than the
Cassini bound on the matter coupling (3.4×10⁻³). A thorium nuclear clock with enhancement K ~ 10⁴ at 10⁻¹⁸ stability would push this to ~3×10⁻¹²
per M_P. For comparison, every string leak estimated today was O(10⁻⁴–10) per M_P (D198, D208, D211). Reading: the shield must be exact to
~10⁻⁸ in α already; the instanton-only breaking of PREREG_SHIELD item 1 (β ~ 10⁻⁷⁹) passes with enormous margin, while ANY perturbative leak
must be suppressed below 10⁻⁸ today — which is why the perturbative leak was required to fall as 1/x⁴ (D142). Nuclear clocks are the experiment
that will test the shield most directly in the next decade.

**D226 — a risk to the dark-energy evidence: a higher optical depth (literature, Jhaveri–Karwal–Hu arXiv:2504.21813).** The CMB+BAO tension
(BAO prefer low Ω_m, which pushes the inferred neutrino mass below the oscillation floor) can be removed if the reionisation optical depth is
τ ≈ 0.091 ± 0.011 instead of the low-ℓ EE value ~0.054–0.065 (trade-off ΔM_ν ≈ 5Δτ). In that case the CMB+BAO preference for w0–wa dark energy
drops below 95% CL; the supernova preference remains (and remains in tension with BAO). For the Twist: (i) its BAO + SN advantage (−3.2,
D158) is partly the same BAO pull, so a high-τ resolution would weaken the dark-energy case for the Twist as for every thawing model; (ii) the
SN-driven part would survive; (iii) n_s is positively correlated with τ in CMB fits, so a higher τ would, if anything, raise the inferred n_s
further (not quantified in the paper) — bad for the plain Twist, neutral for TWIST-G−/L. A direct τ measurement (LiteBIRD, CLASS, ground
low-ℓ) therefore bears on both of the Twist's main data questions at once. Recorded as a known systematic, not a result.

**D227 — TWIST-C: a constant helper term W = √3 m S (T + c) (locked PREREG_TWISTC 3cfaf39; results/twistc_scan.txt).** Prompted by
Gialamas–Katsoulas–Tamvakis (arXiv:2505.03608), who keep K = −3 ln(T + T̄ − |S|²/3) and fix Starobinsky's n_s with a small integer-power
superpotential correction. In the Twist the most generic such term is a constant linear in S. Scan (a sign bug in the plateau check — the
slope is negative on the plateau — was fixed in code before any result was read; the locked rule is unchanged):
| c | n_s (N* 55.7/57) | r |
| −3×10⁻⁷ | 0.9567/0.9574 | 0.0030/0.0028 |
| 0 | 0.9642/0.9650 | 0.0037/0.0036 |
| +1×10⁻⁷ | 0.9669/0.9677 | 0.0040/0.0039 |
| +3×10⁻⁷ | 0.9724/0.9734 | 0.0047/0.0046 |
| +1×10⁻⁶ | 0.9946/0.9964 | 0.0084 |
c ≈ +3.5×10⁻⁷ reaches n_s ≈ 0.974 with r ≈ 0.005 — LOWER r than TWIST-G− (0.0068) or TWIST-L (0.0073) at the same n_s, so the three are separable
by r at the ~0.002 level (LiteBIRD/CMB-S4 σ(r) ~ 0.001). Costs: (i) c must be ~10⁻³ of the field value at the CMB point (u* ≈ 2.5×10⁻⁴) and
is sharply tuned — n_s moves by ~0.01 for Δc ~ 2×10⁻⁷ — a new small number with no explanation, unlike G−'s loop-sized γ; (ii) the term
makes V rise toward the rim for u ≲ 2c ~ 7×10⁻⁷, inside the region already outside the EFT (tower floor u ≈ 1.2×10⁻⁵), so harmless.
Not done: full supergravity check (the angle's mass now depends on c through |T + c|²). Status: post-data, locked; ranks below TWIST-G− on
naturalness, distinct from it on r.
**D228 — TWIST-C passes the full supergravity check (theory/kahler_cliff/twistc_sugra_d228.py).** c = 3.5×10⁻⁷: V/V_Twist = (1 + 2c/u)² as
intended (1.0054 at the CMB point, 1.00007 at the cliff, 1 + 8×10⁻⁹ today — the dark energy is untouched); m_S²/H² unchanged; the angle's
mass +3.98 H² at the CMB point, +4.00 elsewhere — stable.

**D229 — birefringence watch (literature check, no eligible data yet).** The pre-lock ACT + Planck value β = 0.277° ± 0.057° (4.8σ; 3.5σ in the
reduced-dust test; Eskilt arXiv:2608.06480) still stands in ~4.9σ tension with the Twist's locked null (PREREG_BIREF_NULL), with the author's
own caveat that unresolved systematics must be understood first. No measurement with an independent angle calibration has appeared yet:
2512.14407 (Tau A + Moon calibration of a 31 GHz instrument) and 2606.20171 (POLOCALC airborne calibrators, goal 0.01°) are calibration
papers, not β results; Simons Observatory's sparse-wire-grid calibration (2512.19102) is in place. The locked reading will be triggered by the
first calibrator-based β with total error ≤ 0.10°. This remains the Twist's sharpest near-term risk besides n_s: a calibrated β ≈ 0.28° at ≥ 5σ
would make PREREG_BIREF_NULL NOT SUPPORTED, leaving only the anomaly route (β ≤ 0.075°), which that value would also exclude.

**D230 — a naive field-theory loop does NOT give TWIST-G−'s tilt (check of D222).** Try the simplest explicit loop: N chiral pairs with
W ⊃ (y S + λ T) Φ Φ̄, integrated out, give the one-loop Kähler correction ΔK = −(N/16π²)|yS + λT|² ln(|yS + λT|²/Λ²), so
ΔK_SS̄ ≈ −(N y²/16π²) ln(λ²|T|²/Λ²) — an ABSOLUTE correction ∝ ln u. But the helper's tree metric is K⁽⁰⁾_SS̄ = 3gE/u ≈ 3/u on the plateau
(large, ~10⁴ at the CMB point), so the relative change is ~(N y²/48π²) u ln u ~ 10⁻⁵ there — far too small, and not a power law. A pure
tilt u^{−2γ} needs the loop correction to be MULTIPLICATIVE on the helper's metric, i.e. to carry the same modular weight as the tree term:
K_SS̄ = (3gE/u)[1 + c ln u]. That is the structure of string one-loop matter-metric corrections (the T-dependence multiplies the tree metric,
AGNT hep-th/9212045), not of a generic field-theory loop with T-independent cutoff. So D222's "loop-sized γ" holds only if the helper behaves
like string matter with a modular weight (its loops scale with u like the tree metric); in a plain field-theory completion the tilt is not
generated. Status of TWIST-G−'s origin: plausible in a string-like completion with a cutoff tied to the modulus (Λ ∝ M_s-type scale with the
right weight), not in a generic EFT. Recorded so the paper does not overclaim "naturally a loop".

**D231 — a literature lead that could reopen the strong-coupling home: the runaway-dilaton "least coupling" attractor (Damour–Piazza–
Veneziano, hep-th/0205111; constraints Vacher et al. arXiv:2301.13500).** D204/D209 concluded that the Twist's field sits at strong heterotic
coupling today and that the shield "fails there". That conclusion assumed the matter couplings keep their weak-coupling field dependence. DPV
posit the opposite for the string dilaton: the full coupling functions are EXTREMISED as the bare coupling → ∞, so a field running to strong
coupling DECOUPLES from matter, with residual couplings falling off (they quote EP violation ~10⁻¹² for simple inflation, tied to the density
amplitude) — exactly the "leaks must fall with x" behaviour the shield needs (D142), achieved by dynamics rather than symmetry. Vacher et al.
(2023, incl. CMB data) rule out O(1) DPV coupling parameters; our requirement today is |d ln α/dφ| < 1.6×10⁻⁸ (D225), so a DPV-type home would
need the attractor to be very efficient by today. Status: a hypothesis about strong-coupling string physics (not derivable here), but the only
known mechanism under which the Twist's strong-coupling location (D204) HELPS rather than hurts the shield. Added to the open-problem questions:
do the heterotic gauge and matter couplings extremise at infinite coupling along the Twist's direction? If so, the leak is falling and its
redshift shape is the locked band (D216 distinguishes it from a growing leak).

**D232 — if a DPV-type attractor holds, the Twist predicts the shield's falling exponent p = 3 and a leak near today's clock limit (estimate).**
In the DPV picture the first correction to a coupling at strong coupling goes as the inverse string coupling squared, 1/g_s². Along the Twist's
direction g_s ∝ x^{3/2} (D209), so the leak goes as x⁻³: p = 3 — inside the locked PREREG_SHIELD band (p = 3–4, derived earlier from what clocks
allow), now with a physical origin. Size, with leak = c·x⁻³ and today's clock bound |d ln α/dφ| < 1.6×10⁻⁸ (D225):
- degree-1 heterotic (x today ≈ 89): needs c < 4.6×10⁻³; a loop-sized c = 1/(16π²) = 6.3×10⁻³ gives 2.2×10⁻⁸ — just ABOVE today's 2σ clock bound
  (and Δα/α ≈ 6×10⁻⁹ since z = 1, far below quasar sensitivity). So a DPV-type Twist with a one-loop coefficient would sit at the clock limit now
  and be detected or excluded by thorium nuclear clocks (~3×10⁻¹², D225).
- the M9 history (x today ≈ 2.4×10⁴ at the Twist's heat share): the leak is ~10⁻¹⁵ — invisible.
Status: a conditional, falsifiable sharpening — IF strong-coupling couplings extremise (open question 11), the Twist's leak is p = 3 with a
clock-scale amplitude for the degree-1 history. Recorded as a hypothesis-dependent forecast, not a locked prediction.

**D233 — CORRECTION to D231–D232: the strong-coupling regime already breaks neutrality at TREE level, so a DPV-type attractor cannot rescue it.**
D231/D232 treated the strong-coupling problem as a matter of small corrections that might be extremised away. But at strong heterotic coupling
the correct description is heterotic M-theory, where the tree-level relations (Witten; D206 add, D208) already fix the answer: holding the
4-d gauge coupling fixed, M_GUT/M_P ∝ (ρ M_GUT)^{−1/2}, so the overall modulus cannot move without moving either the Standard-Model scale
(β ≈ 0.41) or the Standard-Model coupling (d ln α/dφ ≈ 0.71); only Calabi–Yau shape moduli are neutral, and they are not rung 3 (D208). DPV's
least-coupling attractor concerns the coupling functions of the DILATON in the limit of infinite bare coupling, with the internal geometry
fixed — not this tree-level geometric relation along the Twist's direction. So the hope that "strong coupling helps the shield" (D231) does not
survive, and the x⁻³ forecast (D232) applies only to a hypothetical setting in which the overall modulus at strong coupling had no tree-level
scale relation — none is known. D231/D232 are kept on record but marked superseded; question 11 in the open-problem doc gets this caveat.
Lesson: before importing a mechanism, check it against the tree-level relations already derived in our own notes (here D206/D208).

**D234 — the late-ISW cost is far below current sensitivity (literature).** The Twist's late ISW is ~5% stronger than ΛCDM (D172b), i.e.
A_ISW ≈ 1.05. The best galaxy cross-correlation measurement quoted in arXiv:2512.24369 is A_ISW = 0.98 ± 0.35 (DESI Legacy Survey, Hang et al.
2021); void/supercluster stacks give 1.5–5 with larger errors. The Twist and ΛCDM differ by 0.05, i.e. ~0.15σ of the best measurement — this
cost is not testable before LSST-era cross-correlations (σ(A_ISW) ~ 0.1 would still give only 0.5σ). Removed from the list of near-term risks.

**D235 (pp loop 1) — the Hubble cost in context: every DESI-preferred dynamical dark energy lowers H₀ (literature, arXiv:2503.21600).**
w0wa fits give H₀ = 63.6 (+1.6/−2.1) for CMB + DESI DR2, and 67.5 ± 0.6 / 65.9 ± 0.8 / 66.7 ± 0.6 with Pantheon+ / Union3 / DES-Y5 supernovae.
The Twist's ≈ 65.7 (D169) sits inside that family (between the Union3 and DES-Y5 values), so its H₀ cost is the generic cost of the dynamical
dark energy DESI prefers, not a Twist-specific defect. The same paper shows the other side: adding a SH0ES prior (with early dark energy to
accommodate it) drops the dynamical-dark-energy preference from 2.8–4.2σ to 1.3–2.4σ. So if the local H₀ ≈ 73 is confirmed as cosmological,
the case for thawing dark energy — the Twist's included — weakens; if it turns out to be a local/systematic effect, nothing changes.
Gap 9 status: unchanged in size, re-labelled "shared with all DESI-favoured dark energy"; it couples to the dark-energy evidence (gap 4).

**D236 (pp loop 2) — D219's strong-CP corollary checked against the literature (arXiv:2506.03348): confirmed, with one named loophole.**
Standard isocurvature bound for a pre-inflationary QCD axion: H_I/(f_a θ_i) < 2.8×10⁻⁵ with θ_i = (7.4×10¹¹ GeV/f_a)^{7/12}, i.e.
H_I ≲ 2.3×10² GeV (f_a/GeV)^{5/12}: 2×10⁷ GeV at f_a = 10¹², 10⁹ GeV at 10¹⁶, 7×10⁹ at 10¹⁸. The Twist's H_I = 1.5×10¹³ GeV exceeds these by 2×10³–7×10⁵ —
D219's conclusion (pre-inflationary axions excluded) stands, and the literature's numbers are close to my own estimate. Loophole the paper
develops: a non-minimal coupling ξR|Φ|² with small quartic makes the PQ field larger DURING inflation (f_a^(inf) ≫ f_a), weakening the bound;
but for Starobinsky-type inflation they find f_a^(inf)/f_a ≲ 60–180 before parametric resonance restores PQ and makes strings, while the Twist
would need an enhancement of ~1.5×10⁴ at f_a = 10¹⁶ GeV — outside the rescued range. So for the Twist: post-inflationary axion (m_a ≈ 40–180 μeV if
it is all the dark matter) remains the only standard option. Gap 8 status: confirmed by literature; prediction sharpened, not changed.

**D237 (pp loop 3) — the dark-energy evidence after the DES supernova recalibration (literature, arXiv:2511.07517).** With the DES-Dovekie
recalibration plus CMB (Planck + ACT + SPT) and DESI DR2, flat w0wa gives w0 = −0.803 ± 0.054, wa = −0.72 ± 0.21, rejecting Λ at 3.2σ (down from
4.2σ with the original DES-SN5YR) — the authors call it a weak preference. The Twist's (−0.899, −0.14) sits −1.8σ in w0 and +2.8σ in wa from that
best fit (one-dimensional, ignoring their strong w0–wa correlation, so this overstates the distance along the degeneracy line); thawing
exponential models cannot reach wa ≈ −0.7 with w0 ≈ −0.8, because the data's best fit crosses into the phantom regime at higher z, which a
single canonical field cannot do. This is the known "phantom crossing" issue for all minimally coupled quintessence; our own full-likelihood
fit (Δχ² −3.4 vs ΛCDM, D157 context) is the right comparison, not the w0wa point. Gap 4 status: the overall evidence for evolving dark energy
softened (4.2 → 3.2σ with DES); the Twist's own Δχ² vs ΛCDM should be re-checked against DES-Dovekie when its likelihood is public (added to the
future-data list; no lock change needed — WATCH-PURE-DR3 is scored on DESI DR3).

**D238 (pp loop 4) — gap 5 (n) via the "dark dimension": no help; and a needed caveat to D212 (literature, arXiv:2402.00981).** The dark-
dimension scenario ties the dark-energy scale to a tower, m_tower ≲ Λ^{1/4} (R ≳ 88 μm), treating Λ as a constant. The Twist's tower today is
~3×10¹⁶ GeV (D123) — about 10²⁸ times heavier than Λ^{1/4} ~ meV — so this relation cannot fix n in the Twist; it would require a completely
different (micron-decompactified) picture. Gap 5 unchanged.
**Caveat to D212 (important):** the same paper quotes the asymptotic slope bound as (V′/V)² ≥ 4/(d − 2), i.e. |V′/V| ≥ √2 in 4-d — the
"sharpened" de Sitter conjecture (Rudelius; also the form in Bedroya–Vafa's abstract), STRONGER than the TCC-derived 2/√((d − 1)(d − 2)) = √(2/3)
used in D212. Under the sharpened form only rung 1 (λ = √2) is allowed, and rung 1 is ~4σ from DESI DR2's exponential fit (D224). So: with the
TCC-derived bound the Twist saturates it (D212); with the sharpened bound the Twist — like every exponential quintessence that fits DESI —
violates it. Which bound applies is itself debated in the swampland literature. D212's "rung 3 is the shallowest allowed tail" holds only for the
weaker (TCC-derived) form; the paper section should state both. Recorded; the paper text is updated to say so.

**D239 (pp loop 5) — birefringence systematics: the signal survives an internal consistency test (literature, arXiv:2609.09149, Sept 2026).**
A "birefringence-blind" estimator compares Planck NPIPE detector-set maps (the common rotation cancels) without using the foreground EB model:
the relative detector-angle pattern agrees with the Minami–Komatsu calibration (χ² = 8.18/7, PTE 0.32); dust EE/BB ratios ≈ 1.4 imply a
cross-frequency bias < 0.01°; a conditional reconstruction gives β = 0.37° ± 0.12° (~3σ). The authors stress this is NOT an independent absolute
measurement (same maps; the absolute zero point is not fixed). arXiv:2602.12019 is a methods paper (fits instrument angle jointly; no new β).
For the Twist: the two most obvious systematic explanations (inconsistent detector angles; dust EB bias in the frequency combination) are
now disfavoured for the Planck part of the signal, which RAISES the chance the 0.28° signal is real. The locked rule still waits for a
calibrator-based β (PREREG_BIREF_NULL), and the absolute-angle loophole remains open. Gap 2 status: risk raised from "high" to "high and
growing"; it is now the single most likely way the Twist (in its anomaly-free form, β = 0) fails in the next ~2 years.

**D240 (pp loop 6) — n_s: the literature now treats the CMB+BAO shift as possibly a statistical artefact (literature).** arXiv:2507.12459
("The BAO–CMB tension and implications for inflation"): ACT alone 0.9666 ± 0.0076; ACT + DESI DR2 0.9770 ± 0.0070; P-ACT-LB 0.9739 ± 0.0034. Starobinsky
-type models (0.960–0.967 for N* 50–60) remain viable with CMB alone and are disfavoured at ~2σ+ only in the CMB+BAO combination; the authors warn
that CMB+BAO n_s should be read cautiously until the tension is resolved ("neither possibility makes a firm prediction"). A 2026 news report
(Ferreira et al., Kavli IPMU; no arXiv number or numbers given in the report — not verified against the paper) says that modelling the
covariance properly makes the n_s shift largely disappear. Our own reading (D223) agrees: the Twist is −0.3σ from ACT alone and −1.7σ from
CMB-SPA alone. Gap 1 status: unchanged as a LOCKED verdict (NS-SPA used CMB+BAO and stays INCONSISTENT as scored), but its interpretation is
now explicitly contested in the literature; the plain Twist and the post-data variants are effectively waiting on the BAO–CMB resolution. To do
when the Ferreira paper is found: read it and record its numbers (no rescoring of the locked test).
D240 add (pp loop 7) — the "Ferreira et al." report is the SAME paper already read: arXiv:2507.12459 by Ferreira, McDonough, Balkenhol,
Kallosh, Knox and Linde, published in Phys. Rev. D on 18 Feb 2026 (Editor's Suggestion, DOI 10.1103/lq71-b84v). Its numbers are those recorded
above (ACT alone 0.9666 ± 0.0076; ACT + DESI DR2 0.9770 ± 0.0070); the press release's "evidence against standard inflationary models weakens
significantly" is the paper's dataset-consistency argument, not a new fit. To-do closed; nothing to rescore. Notable for the paper: two of the
authors (Kallosh, Linde) are the α-attractor authors, so the Twist's family has authoritative backing that the CMB+BAO n_s is not yet a
clean test.

**D241 (pp loop 8) — gap 3: the closest published relative of the shield is Higgs-dilaton cosmology, and it shows the difference sharply
(literature, Shaposhnikov–Zenhäusern line; arXiv:1712.04956, 1107.2163).** There, exact (spontaneously broken) scale invariance makes the
dilaton a Goldstone with only derivative couplings to matter — the same logic as the Twist's shield (SM neutral under the disk's scaling
isometry, D140). Two contrasts: (i) in Higgs-dilaton the scale symmetry is broken ONLY by the unimodular-gravity term that makes dark energy,
whose potential e^{−4γΦ} is tiny in slope (γ small), so w0 = −0.997 ± 0.003 — a near-cosmological constant; the Twist's tail slope √(2/3) is
large, so its dark energy is far more dynamical (w0 −0.90) and its symmetry breaking (the tail potential) is much larger. The review notes the
non-derivative potential is not covered by the derivative-coupling argument "at the present epoch" — the same loophole the Twist's shield has
to close with the instanton-only breaking (D140–D142). (ii) Higgs-dilaton ties inflation to dark energy, n_s = 1 − (2/N*) X coth X with
X = 3N*(1 + w)/(4F(Ω_DE)): w0 ≳ −0.98 would need too few e-folds, i.e. it CANNOT give DESI-like dynamics; the Twist decouples the two (rung 3
sets both slopes but not via this relation), which is why it can give w0 ≈ −0.9 with n_s ≈ 0.965. So the shield idea has a respected precedent
(scale symmetry → Goldstone decoupling), and the Twist's distinctive risk is precisely its large late-time symmetry breaking. Gap 3 status:
unchanged; the paper should cite Higgs-dilaton cosmology as the precedent and state this difference.

**D242 (pp loop 9) — gap 12: the Twist's dark-matter window is inside the "gravity portal" stability bound, but near its edge (literature,
arXiv:1611.00725).** For a singlet fermion that decays only through gravity-portal operators (lowest is dimension 6, rate ∝ M⁻⁴ with M the
Planck/new-physics scale), requiring a lifetime ≳ 10²⁴ s (conservative) allows m_DM ≲ 10⁶ GeV for an O(1) non-minimal coupling ξ, rising to
~10¹⁰ GeV for ξ ~ 10⁻¹⁶; specific channels (neutrinos, WW) are bounded at 10²⁶–10²⁷ s, which tightens the window by roughly a factor
(10²–10³)^{1/5} ≈ 3–4 in mass for fixed couplings. The Twist's conditional candidate (100–500 TeV = 10⁵–5×10⁵ GeV, from χ̃ decays, D105 context)
sits below the ~10⁶ GeV edge for ξ ~ O(1) — allowed, but within a factor 2–10 of it, so a gravity-portal Twist DM would be a DECAYING dark
matter with a lifetime possibly near current neutrino/gamma-ray limits — a potential signal (IceCube/KM3NeT high-energy neutrinos, LHAASO
gamma rays) worth flagging as a target, not a prediction (the candidate is still conditional and out of the predictions table).

**D243 (pp loop 10) — gap 6/D238: the string-side answer to DESI is the opposite of the Twist's shield (literature, Andriot "Phantom matters",
arXiv:2505.10410).** To make steep, swampland-compatible tails (λ = √2 or √(8/3)) fit DESI, Andriot couples the quintessence field to (dark)
matter: the coupling makes the effective dark energy cross into phantom at z ≈ 0.6–1.1 and reproduces w0 ≈ −0.67, wa ≈ −0.92 (vs DESI+CMB+Union3
−0.667 ± 0.088, −1.09). The paper is explicitly "agnostic" about fifth forces and varying constants, suggesting only that coupling part of the
DARK matter might reduce them. Contrast with the Twist: the Twist keeps λ = √(2/3) (TCC-saturating, D212) and forbids matter couplings (the
shield) — so it cannot phantom-cross and fits DESI less well than the coupled models (D237), but has no fifth-force problem by construction.
Two consistent pictures thus exist in the literature: (a) steep tail + dark-matter coupling (swampland-friendly, phantom-capable, fifth-force
problem pushed into the dark sector); (b) the Twist: shallower tail + exact shield. A clean discriminant: (a) predicts dark-matter–dark-energy
interaction signatures (scale-dependent growth, DM mass drift) and phantom crossing; (b) predicts none. Gap 6 status: unchanged; recorded as
the main competing string-inspired picture for the paper's discussion.

**D244 (pp loop 11) — gap 11: D214's mechanism is established in the literature (arXiv:hep-ph/0408318).** Right-handed neutrino Majorana
masses from a Giudice–Masiero-type Kähler operator T†NN/M_P with a hidden-sector F-term give M_R ~ F_T/M_P ~ m_3/2 (that paper uses TeV-scale
SUSY, so M_R ~ TeV, with an SO(3) flavour symmetry making two N degenerate and enabling resonant leptogenesis). With the Twist's high-scale
SUSY (m_3/2 ~ 2×10¹⁴ GeV in BGW's example, D202) the same operator puts M_R at the seesaw scale and gives m_ν ≈ 0.05 eV for Yukawa ≈ 0.6 (D214).
Caveats unchanged: it relies on the BGW-type sector, and the Twist's matter comes from the angle (lepto-axiogenesis), so N's leptogenesis is
not needed. Gap 11 status: the optional lead is now literature-backed; still optional and outside the predictions table.

**D245 (pp loop 12) — gap 10: lumpy starts — a 2025 numerical-relativity result puts the Twist far on the robust side (literature,
arXiv:2512.13673).** For α-attractor T-models with large gradient and kinetic inhomogeneities, inflation succeeds above a critical
tensor-to-scalar ratio r_crit ≈ 4×10⁻⁶ – 1.3×10⁻⁵ (horizon-scale perturbations, homogeneous run fixed at 100 e-folds); the authors' r–μ relation
maps r = 0.003–0.004 to μ ≈ 0.46–0.54 m_P, ~500–1000× above r_crit and beyond their scanned range (extrapolation, not simulated; the E-model/
Starobinsky shape itself was not run). The Twist (r ≈ 0.0036; TWIST-G− 0.007) therefore sits deep in the robust regime by this criterion — the
plateau curvature scale is what matters, and it is super-Planckian. Remaining Twist-specific limit: the usable plateau inside the EFT is
2.5–3.8 M_P (tower-limited, D218 correction); the paper's robust runs have ~100 e-folds available, which the Twist's plateau supplies (~900 e-folds
from the old tachyon edge, more inside the tower limit). Gap 10 status: "robust by analogy" upgraded to "robust by the published r_crit
criterion (extrapolated to the Twist's r)"; LOW.

**D246 (pp loop 13) — gap 13: D230 was too pessimistic — a field-theory loop CAN give TWIST-G−'s tilt, if the loop masses come from the
inflaton itself (literature, arXiv:2506.18077).** "Radiatively corrected Starobinsky inflation": a one-loop Coleman–Weinberg term
κ φ⁴ ln(φ/μ) in the Jordan frame (κ = N λ²/16π², from particles whose masses are set by the inflaton field φ), divided by the conformal factor,
gives n_s ≈ 0.970–0.975 with r ≈ 0.004–0.006 for N* 50–60 (their RG-improved benchmarks; κ ~ 10⁻⁴ inferred from their table). On the plateau
ln φ is linear in the canonical field, so V(1 + κ ln φ) ≈ V u^{δ} to first order — the same first-order deformation as TWIST-G−'s u^{2γ}, with
a log rather than a pure power (the slope drifts logarithmically; the difference shows only at second order). What D230 got right: a loop whose
masses do NOT track the inflaton (T-independent cutoff, helper-only couplings) gives a negligible, non-tilting correction. What it missed: if
the loop particles get their masses from the field that sets the plateau, the correction multiplies the potential and tilts it at κ ~ 10⁻⁴–10⁻²
— loop-sized. For the Twist this means γ could come from fields coupled to T through W ⊃ λ T Φ Φ̄ IF their contribution enters the potential
multiplicatively along the plateau; not computed in the Twist's supergravity structure (the Twist is not a Higgs-like non-minimal model; the
mapping is only at the level of the Einstein-frame potential shape). Status of gap 13: "TWIST-G− needs string-like loops" (D230) softened to
"a loop whose masses track the inflaton gives the tilt at first order (literature analogue); the Twist-specific calculation is not done".

**D247 (pp loop 14) — timing of the decisive dark-energy data (literature/news, UKRI 15 Apr 2026).** DESI finished its planned five-year
survey ahead of schedule (April 2026); the first dark-energy results from the full five-year data set are expected in 2027; further studies
on the first three years are expected during 2026; the survey is extended through 2028 (14,000 → 17,000 deg², fainter LRGs). For the Twist:
WATCH-PURE-DR3 (w0 −0.90, wa −0.14), PREREG_GROWTH and the BAO–CMB question behind the n_s verdict (D223/D240) will be scored on the 2027 full-
survey release (cumulative with DR2, as already noted in D136(i)). Planning note: the gap review's "near-term decisive tests" order becomes:
calibrated birefringence (any time) · DESI five-year (2027) · Simons Observatory n_s/r (2026–28) · nuclear clocks · LiteBIRD/CMB-S4 (2030s).

**D248 (pp loop 15) — Simons Observatory r reach for the Twist family (literature forecast, arXiv:2512.15833).** No SO result yet. Updated
forecast for the degree-scale survey (6 small-aperture telescopes by 2027, survey extended to 2035): σ(r) = 1.2×10⁻³ baseline, 7×10⁻⁴ optimistic
(r = 0 fiducial). Detection significance: Twist r = 0.0036 → 3.0σ (baseline) / 5.1σ (optimistic); TWIST-C 0.005 → 4.2/7.1σ; TWIST-G− 0.0068 →
5.7/9.7σ; TWIST-L (at n_s 0.974) 0.0073 → 6.1/10.4σ. TWIST-G− vs TWIST-C differ by 1.5σ (baseline). So SO alone can detect the Twist's r at
~3–5σ before LiteBIRD — making the r test a 2030-ish event rather than 2035+, and r = 0 at that precision would put PREREG r-readings
(r < 0.0030 at 95% kills TWIST-L/plain Twist variants) into play. Gap 1/variants: timeline sharpened.

**D249 (pp loop 16) — gap 2: how a calibrated birefringence result could arrive, and why the Twist cannot produce β (literature,
arXiv:2511.04459).** A DE–photon Chern–Simons coupling −(g/2)φFF̃ gives β ∝ g(φ₀ − φ_LSS) — the standard way a thawing field would make
β ≈ 0.3°. Forecast for AliCPT-1 + Planck HFI: with a 0.1° calibration prior, a 5σ detection of β = 0.35° needs ~11–18 module-years; 20 module-
years give σ(β) ≈ 0.08°; below ~0.02° calibration the error is data-limited — so calibrator-based detections at the 0.1° level are plausible
within a few years (also SO's sparse-wire-grid system, 2309.02035). Why the Twist stays at β = 0 structurally: the field that rolls today is
Re T, CP-even, which can only couple as φFF (α variation, forbidden by the shield), not φFF̃; the CP-odd angle Im T has mass ≈ 2H and sits at
its minimum, so its Δφ since last scattering is ~0 (D14 context, PREREG_BIREF_NULL). If a calibrated β ≈ 0.3° is confirmed, the Twist as a single
field is falsified on this observable; an extension would need an additional light pseudoscalar coupled to photons — a different model.

**D250 — research for the "Twist + one photon-coupled axion" option (literature: arXiv:2506.20824, 2203.08560).** If a calibrated β ≈ 0.3° is
confirmed, the minimal extension is a spectator ALP φ with −(g/2)φFF̃:
- Planck EB fits (2506.20824): masses log₁₀(m/eV) ≈ −27.8 … −26.5 are partly excluded at > 2σ (the EB acoustic structure shifts, e.g. near ℓ ≈ 400);
  m ≲ 10⁻²⁸ eV is unconstrained and needs |g φ_ini/2| ≈ 0.3° with a negligible energy fraction (spectator) — consistent with my estimate
  (c·Δθ ≈ 4.5 for a decay constant ~10¹⁶ GeV, ~0.04% of the dark energy).
- Tomography (2203.08560): for m ≲ 10⁻³² eV the field is frozen between recombination and today, so the rotation is one angle at all ℓ —
  exactly like a miscalibration; for 10⁻³² ≲ m ≲ 10⁻³¹ eV the reionisation bump (ℓ ≤ 10) is rotated differently from high ℓ — an ℓ-dependent
  signature miscalibration cannot fake, measurable only by a full-sky satellite (LiteBIRD).
Design consequence: the ALP should sit at 10⁻³² ≲ m ≲ 10⁻²⁸ eV (rolls between last scattering and today; m ≲ 10⁻²⁸ to avoid the Planck-excluded
band), and a mass in 10⁻³²–10⁻³¹ eV gives the cleanest test (LiteBIRD low-ℓ/high-ℓ ratio). Shield: the FF̃ coupling is topological — no fifth
force, no α drift — so the Twist's other predictions are untouched. Status: a ready, literature-backed extension; not built or locked (Danny's
call: it makes the Twist a two-field model). If built, its distinctive prediction would be an ℓ-dependent EB at ℓ ≤ 10 for the 10⁻³²–10⁻³¹ eV
choice, or a pure constant angle for lighter masses.

**D251 — TWIST+ALP computed (locked PREREG_TWIST_ALP 5cfafeb; theory/alp/twist_alp_scan.py; results/twist_alp_scan.txt).** Spectator axion in the
Twist background, amplitude set to β_rec = 0.30°:
| m (eV) | field left today | R = β_reion/β_rec | c·θ_ini needed | energy fraction (f = 10¹⁶ GeV) |
| 10⁻³³ | 94% (barely moved) | 0.997 | ~70 (c ≳ 22 for θ ≤ π) | 0.9% |
| 10⁻³² | 2% | 0.982 | 4.6 | 6×10⁻⁵ |
| 3×10⁻³² | 3% | 0.846 | 4.7 | 6×10⁻⁵ |
| 10⁻³¹ | 0.3% | −0.03 | 4.5 | 6×10⁻⁵ |
| 3×10⁻³¹ – 10⁻²⁹ | ~0 | −0.03 … 0.00 | 4.5 | 6–7×10⁻⁵ |
Reading: below ~2×10⁻³² eV the field starts rolling after reionisation, so both eras are rotated alike (R ≈ 1) — indistinguishable from a
miscalibrated angle; from ~3×10⁻³² eV the reionisation-era rotation is reduced (R 0.85) and above ~10⁻³¹ eV it is essentially zero (the field
has already decayed by z ≈ 8) — a sharp tomography signature: the low-ℓ reionisation bump in EB disappears while high-ℓ EB stays. The needed
coupling × initial angle is c·θ ≈ 4.5 (e.g. anomaly coefficient c ≈ 2–5 with θ ≈ 1–2 rad) — natural; the energy is 6×10⁻⁵ of the dark energy, so
the Twist's dark energy, growth and inflation are untouched. Status: the extension works cleanly for 10⁻³² ≲ m ≲ 10⁻²⁸ eV; it is a post-data
two-field option, locked, scored only if a calibrated β is confirmed; its distinctive test is LiteBIRD's low-ℓ EB (R ≈ 0 vs R ≈ 1).
D251 add: last grid point m = 10⁻²⁸ eV: R = 0.001, c·θ ≈ 8.9 (the field begins rolling before recombination, so part of its motion is missed
by β_rec), energy fraction 3.6×10⁻⁴ — still a negligible spectator; the Planck EB-shape exclusions start just above (D250).

**D252 (pp loop 17) — the TWIST+ALP option meets the same swampland tension the rest of the Twist does; a domain-wall alternative exists
(literature, "Wading the String Bog: CMB Birefringence in the Swampland", arXiv:2607.27318).** For an ultralight axion that is frozen until
recombination (m ≲ 10⁻²⁸ eV) the magnetic weak-gravity conjecture suggests m ≳ 10⁻²⁸–10⁻²³ eV — "in the right ballpark" for tension at the
lower end; the electric WGC (f·S ≲ M_P) leaves instanton effects unsuppressed for large f. The authors claim tension, not exclusion (imprecise
coefficients). Our computed window (D251: 10⁻³² ≲ m ≲ 10⁻²⁸ eV, f ~ 10¹⁶ GeV, c·θ ≈ 4.5) sits BELOW their suggested floor, so the spectator-ALP fix
is swampland-disfavoured in the same sense as the Twist's own long excursion and TCC questions (D211–D213, D238) — consistent at least: the
Twist is an EFT that the swampland programme, as currently conjectured, presses on in several places. Alternative they propose: rotation from
crossing a thin axion domain wall, Δθ ≈ C_γ α/(2π) ≈ 10⁻³ C_γ, so 0.3° (5.2×10⁻³ rad) needs C_γ ≈ 5 — no ultralight field, no Planckian range,
"little if any friction" with the swampland, and a different observational shape (the authors note isotropy tests separate the two). For the
Twist this second route adds an axion with a wall network instead of a light spectator; not built. Status: if a calibrated β is confirmed, two
extension routes are on file (spectator ALP — D251, swampland-tense; domain wall — not built, swampland-friendly); choosing between them waits
on the data's shape (anisotropy / ℓ-dependence).

**D253 (pp loop 18) — gap 3: the nuclear-clock test of the shield, with the measured thorium sensitivity (literature, Beeks et al., Nat.
Commun. 16 (2025), DOI 10.1038/s41467-025-64191-7).** Measured α-enhancement of the ²²⁹Th clock transition: K = 5900 ± 2300 (uncertainty from
the nuclear charge-radius change). A thorium/strontium frequency-ratio drift bound at 10⁻¹⁸ per year then gives |α̇/α| < 1.7×10⁻²² /yr and,
with the Twist's field speed today (3.15×10⁻¹¹ M_P/yr, D225), |d ln α/dφ| < 5×10⁻¹² — three to four orders below today's atomic-clock limit
(1.6×10⁻⁸); at 10⁻¹⁹/yr ratio stability, 5×10⁻¹³. (K = 3600, the low end, weakens these by ×1.6.) JILA's 2026 work demonstrates the clock and
the UV–strontium comparison but quotes no α bound yet. For the Twist: the shield's instanton-only breaking (~10⁻⁷⁹) passes any foreseeable
clock; any perturbative leak (D216: falling or growing) above ~10⁻¹² per M_P would be caught by a thorium clock at 10⁻¹⁸/yr. Gap 3 status:
test quantified with a measured K; timing depends on long-term Th/Sr ratio campaigns (years).

**D254 (pp loop 19) — gap 4 / PREREG_GROWTH timing: Euclid's first cosmology results are expected in 2027 (Euclid Consortium news;
Schrabback et al. 2026, A&A 708, 345 is a single-cluster lensing pilot, no S8/σ8/w0 constraint).** So both of the Twist's main late-universe
tests — DESI's five-year dark energy (D247) and Euclid's first growth/lensing cosmology — land in 2027. PREREG_GROWTH (σ8 −1.5%, f σ8 −3% at
z ≈ 0.4, growth index ≈ 0.557) will first be scored then; at fixed Ω_m the σ8 shift is small compared with early Euclid errors, so the
combined DESI + Euclid analysis (expected ~2027–28) is the realistic first decisive growth test. Gap 4 timeline sharpened; no status change.

**D255 (pp loop 20) — gap 5: "n as an instanton action" is a re-labelling, not an explanation (check).** If the cliff depth came from one
instanton of a hidden gauge group, e^{−2n} = e^{−2π/α_h}, i.e. n = π/α_h: n = 125 ↔ α_h = 1/39.8 — a perfectly ordinary weak gauge coupling (SM
couplings run to ~1/40–1/50 near the Planck scale), which makes the 10⁻¹⁰⁸ suppression look "natural". But the sensitivity is exponential:
α_h⁻¹ = 38/40/42/45 gives n = 119/126/132/141 and shifts ρ_DE by e^{+11}, e^{−1}, e^{−14}, e^{−33}; landing within a factor 2 of the observed ρ_DE
needs α_h⁻¹ to ±0.11 (0.3%). So unless a theory PREDICTS α_h⁻¹ to three digits (e.g. tied to SM couplings by unification with known
thresholds), this is the standard instanton re-labelling of the cosmological-constant problem, which the literature on Λ-from-instantons
also faces (e.g. gr-qc/0204033, hep-th/0110137 consider such origins). It is no worse than "n chosen" and reads better ("the dark-energy
scale is set by a hidden coupling α ≈ 1/40"), but it is not a derivation. Gap 5 status: unchanged; the paper may state the re-labelling
honestly, with the 0.3% precision requirement. (Consistent with D153/D136: thresholds cannot supply n; a single exponent can, given α_h.)

**D256 (pp loop 21) — LiteBIRD timing (IPMU news, KDP2 passed Sept 2025).** LiteBIRD cleared JAXA's Key Decision Point 2 in September 2025 and
heads into mission definition and Phase A; launch "in the 2030s" (no firmer date given). Consequences for the Twist's tests: the r readings of
the locked inflation variants will first be decided by the Simons Observatory (σ(r) ≈ 0.7–1.2×10⁻³ through 2035, D248), not LiteBIRD; the
birefringence TOMOGRAPHY test of TWIST+ALP (low-ℓ reionisation bump, D250–D251) needs full sky and so waits for LiteBIRD (late 2030s at the
earliest, given ≥ 3 years of observation). Ordered timeline now: calibrated β (ground, any year) → DESI 5-yr + Euclid (2027) → SO r/n_s
(~2028–2035) → nuclear clocks (years) → LiteBIRD (late 2030s).

**D257 (pp loop 22) — gap 7: the Twist's matter-sector isocurvature estimate matches the literature's scaling (arXiv:1207.2135).** For
baryogenesis set by a light field's phase during inflation, the baryon isocurvature power is P_S = H²/(4π²θ²Λ²) (Λ = field amplitude), and
α_iso = (Ω_B/Ω_DM)² P_S/P_R must stay below the CMB bound; light-field (m ≪ H) set-ups are viable only if H/Λ is small. The Twist's hidden axion σ
is exactly this case (m_σ ≈ 6×10¹⁰ GeV ≪ H): with Λ = f M_P and f = 0.05–0.3, H/Λ = 2×10⁻⁵ – 1.2×10⁻⁴ and δσ/σ₀ = H/(2πΛ) ≈ 3×10⁻⁶ – 2×10⁻⁵ —
the same numbers D134 used (≈10⁻⁵ at f = 0.1), giving S_B ≈ 6×10⁻⁶ (safe ×8) for |dlnY/dlnσ₀| ≈ 0.64. The paper's stricter "one decade of
anthropic room" criterion (H/Λ ≲ 1.2×10⁻⁵) is met only for f ≳ 0.5 M_P (not for f = 0.05–0.3: H/Λ = 2.1×10⁻⁵ at f = 0.3) — but that criterion concerns anthropic tuning room, not the CMB bound itself. Gap 7 status: the analytic part is literature-consistent; the
remaining unknown is exactly what the locked PC run D137 measures (the yield's true sensitivity |dlnY/dlnσ₀|, locked ≤ 5); a value above ~5
would push the model to larger f or fail D134. The 21:01 check scores it.

**D258 (pp loop 23) — gap 4 / PREREG_GROWTH against the current DESI growth data (literature, arXiv:2411.12022; 2512.03230).** DESI DR1
full-shape + BAO: σ8 = 0.842 ± 0.034 (4%), "broadly consistent" with the CMB's 0.813 ± 0.005; with CMB, σ8 = 0.8121 ± 0.0053; modified-gravity μ0 =
0.04 ± 0.22 (GR-consistent). DESI DR1 peculiar velocities: fσ8(z = 0.07) = 0.450 ± 0.055 (12%) vs Planck-ΛCDM 0.446. The Twist's −1.5% in σ8
and ~−3% in fσ8 are 0.1–0.4 of today's 1σ errors — current growth data neither help nor hurt; a 3σ test of the Twist's growth suppression
needs ~1% per-point fσ8 (DESI five-year + Euclid, 2027–28, D254). The Twist's GR-like growth index (≈ 0.557) is consistent with μ0 ≈ 0. Gap 4:
no change; PREREG_GROWTH stays a future test.

## Fixes after the independent referee review of the published paper (13 Nov 2026, 19:00; papers/REFEREE_REPORT_2026-11-13.md)
Numbers: theory/review/referee_fixes_d259.py → field_tests/results/referee_fixes_d259.txt.

**D259 — tail-slope fraction (referee check FAILED in v4; corrected).** The slope seen today is √(2/3)·x/(x + μ). At μ = 1: x = 2 → 66.7%,
x = 30 → 96.8%, x = 73 (frozen, 0.8% heat) → 98.6%, x = 89 (today) → 98.9%. v4's "97–100% for x_f ≈ 2–300" was wrong at the low end:
≥ 97% needs x ≳ 30. At the derived heat share (0.65–0.8%, TWIST-K consistency pass) the field sits at x ≈ 73–89, so the statement
"98.6–98.9% of √(2/3)" stands; the 0.01% heat-share case (x ≈ 360) gives 99.7%. The μ = 10⁴ range is 0.02–3%, not 0.3–3%.

**D260 — instant-reheating temperature (corrected).** From H_end = 5.2×10¹² GeV, ρ_end = 3H²M_P², g* = 106.75: T_RH(f = 1) = 1.9×10¹⁵ GeV
(v4 said 2.6×10¹⁵). Derived heat share 0.65–0.8%: T_RH = 5.5–5.8×10¹⁴ GeV (v4's 3–5×10¹⁴ corresponded to 0.15–0.5%). Effect on N*:
ΔN* ≈ ⅓ ln(2.6/1.9) ≈ 0.1, Δn_s ≈ 6×10⁻⁵ — negligible; numbers below unchanged.

**D261 — gravitino (v4 inconsistency resolved; Dudas et al. read in full).** v4 said "a gravitino heavier than T_RH is not produced",
but its own m_3/2 ≈ 10¹¹–10¹³ GeV is below T_RH ≈ 5.6×10¹⁴ GeV, and it also said "the gravitino stays massless". Resolution:
(a) W = √3 m S T vanishes at S = 0, so the inflaton sector contributes nothing to m_3/2; the gravitino mass comes from a separate
supersymmetry-breaking sector that the model does not specify (assumption), taken below the inflaton mass (m_3/2 ≲ 5×10¹³ GeV) so the
plateau is undisturbed. (b) arXiv:1710.07341 (read in full now): its escape needs ALL superpartners above the inflaton mass and T_RH, and a
stable gravitino with Ω h² ≈ 0.11 (0.1 EeV/m)³ (T_RH/2×10¹⁰ GeV)⁷ — at T_RH ≈ 5.6×10¹⁴ GeV a stable gravitino is excluded for any
m_3/2 below the inflaton mass. So the v4 citation does not support the v4 claim; withdrawn. (c) What does work (estimate, standard
thermal yield Y ≈ 1.9×10⁻¹²(T_RH/10¹⁰ GeV)(1 + m_g̃²/3m²)): superpartners at or below m_3/2 in the bath, Y ≈ 1.5×10⁻⁷; for
m_3/2 = 10¹¹–10¹⁴ GeV the gravitino decays at T ≈ 4×10⁶–10¹¹ GeV, long before nucleosynthesis, carrying ≤ 0.4% of the energy (no
dilution of the asymmetry); with R-parity violated (the v4 assumption) the LSP decays too. Status: the gravitino problem is avoided for
m_3/2 ≳ 10¹¹ GeV under two stated assumptions (separate SUSY-breaking sector; R-parity violation). The gravitino is not the dark matter.

**D262 — trials correction for PURE-TWIST (new).** Δχ² = −3.37 with no extra parameter ≈ 1.84σ locally (two-sided p = 0.066). With 6–12
late-time variants tried on the same data (six in the tournament table, plus TAIL-F, NS-PURE and the SN/DES swaps), the Šidák-corrected
significance is 0.6–1.0σ. Held-out improvements (−0.89, −0.41) are noise-level. On the full CMB-SPA + DESI + SN data (NS-SPA leg, n_s
free) PURE-TWIST is worse than ΛCDM by Δχ² = +1.45. Verdict: no evidence for the Twist's tail on current data; its value is the locked
prediction for new data.

**D263 — coupling definition (made explicit).** All matter code uses the locally canonical angle speed: with metric ds² = dφ² + e^{λφ}dθ²
and T = x + iy, θ = √(3/2)·y and the speed entering μ_A is v_θ ≡ e^{λφ/2}θ̇ = √(3/2) ẏ/x (sugra_mirror_radiation.py, "r = √g_yy |y'|").
So ℒ ⊃ (c_A/M_P) √(3/2) (∂_μy/x) J₅^μ with c_A = √(3/8) is the coupling used. The alternative reading, coupling to ∂_μ(y/x) (the
1/γ = y/x Immirzi mapping), adds −(y/x)ẋ/x, which is not small during kination; it is not what was computed. c_A = √(3/8) is "fixed" only
given this normalisation choice; stated as an assumption. (The "400× in the other frame" remark concerns the Jordan- vs Einstein-frame
temperature, a separate choice.)

**D264 — growth and w_a reconciled (one conditioning per number).** (i) E_G: at each model's own best fit (pure_twist_growth.json)
PURE-TWIST E_G is +4.9% at z = 0.5 (0.4182 vs 0.3987), but ≈ 4 points of that is the different best-fit Ω_m (0.310 vs 0.298); at equal
Ω_m the β = 0 tail gives E_G within ≈ 1% of ΛCDM. v4's two statements ("5% higher" and "matches ΛCDM") were the two conditionings
unlabelled. Adopted: quote best-fit values, with Ω_m stated. (ii) w_a: −0.10 (WA-CEILING, effective_w.py: w_eff fitted uniformly in a over
z ≤ 2, as an observer assuming ordinary dark matter) vs −0.14 (CPL fit to the field's own w over z < 2 with the paper's weighting). Same
model, two fitting conventions; the locked rule uses its own. (iii) BAO: the frozen table (each model at its own best fit, neither refitted)
is the one tied to the drafted DR3 scoring; the addendum's +1.3% / +1.9% were at fixed Ω_m and H₀ (CMB-anchored) — a theory sensitivity,
not an observable forecast. Both now labelled.

**D265 — cliff depth n reconciled.** exp(−2n) m²/[4(1 + x/μ)] = ρ_DE with m = 2.1×10⁻⁵ M_P: n = 126.9 without the (1 + x/μ) factor,
124.6 with x = 89, μ = 1. Adopted n = 124.6 (≈ 125); v4's 127 omitted the factor; 124 was rounding; n = 10 was the numerics value.

**D266 — internal contradictions removed (bookkeeping, no new physics).** One construction (TWIST-K); the hidden-gauge (SU(8) + Z₂ racetrack)
construction of the inflaton sector is dropped. The kick sector of the matter mechanism still uses a hidden gauge group with f ∝ T, whose
coupling is strong at Re T ≲ 1 where the kick acts — the same loss of control as the old cliff (stated in the exploratory note). TWIST-K's
claims that worldsheet instantons "remove the conflict found at the string level" and give "a precise route to deriving n" are withdrawn
(D189, D204–D211, D233 superseded them). Parameter values: one table (consolidated paper, Sec. 2), from MODEL_CARD_v5.

**D267 (pp loop 24) — supersymmetry breaking in the Twist's no-scale sector: v5's gravitino assumption is not consistent as stated.**
Algebra (exact for K = −3 ln(T + T̄)): m_3/2 = e^{K/2}|W| = |W|/(2x)^{3/2} on real T. Literature (read): Zwirner's no-scale review
(arXiv:2504.06190): constant W₀ gives V = 0 with m_3/2² = |W₀|²/(8t³) — the gravitino mass slides with Re T. Ellis, Nagaraj, Nanopoulos &
Olive, JHEP 11 (2018) 110, arXiv:1809.10114: Minkowski needs W = a T^{n±}, n± = (3/2)(α ± √α) → at α = 1, W = a or a T³; de Sitter needs
a(T³ − 1)-type combinations. So for the Twist's α = 1: W ∝ T⁰ → m_3/2 ∝ x^{−3/2}; W ∝ T³ → m_3/2 ∝ x^{+3/2}; the only x-independent choice,
W ∝ T^{3/2}, gives AdS (V = −3 m_3/2²), needing an extra T-independent uplift (a new tuning). Numbers for constant W₀ along the Twist's
history: (2x)^{−3/2} = 2.4×10⁵ at the CMB point (x = 1.3×10⁻⁴), 0.35 at the cliff (x ≈ 1), 5.7×10⁻⁴ at freeze (x = 73), 4.2×10⁻⁴ today
(x = 89) — a factor 5.7×10⁸ between the CMB point and today. (a) m_3/2 today ≥ 10¹¹ GeV (v5's range) → ≥ 6×10¹⁹ GeV during inflation
(super-Planckian): excluded. (b) Requiring m_3/2(CMB) ≲ H_inf = 1.5×10¹³ GeV → m_3/2 ≲ 2.6×10⁴ GeV today (~3.5×10⁴ GeV at nucleosynthesis):
thermally produced at T_RH ≈ 5.6×10¹⁴ GeV (Y ~ 10⁻⁷) and decaying near the MeV era, this violates nucleosynthesis bounds (estimate; standard
heavy-gravitino BBN limits need Y ≲ 10⁻¹³–10⁻¹⁴ for TeV–10 TeV masses). Verdict: a constant SUSY-breaking W₀ is excluded for the Twist.
What remains: (i) a near-massless gravitino (W = 0 at S = 0, superpartners not tied to m_3/2; helicity-3/2 production only, ΔN_eff ~ 3×10⁻⁸ —
earlier estimate), which requires the low-energy theory not to be softly-broken SUSY with m_soft ~ m_3/2; or (ii) W ∝ T^{3/2} plus a
sequestered T-independent uplift — an extra tuning, structurally the same problem as the fifth-force shield (soft scales tied to x).
Status: v5 Section 5.2 / assumption 4 must be corrected in the next version: replace "m_3/2 = 10¹¹–10¹⁴ GeV from a separate sector" by
options (i)/(ii) and state that the generic choice is excluded. The numerical check (w0_gravitino_d267.py: V with W₀ and S relaxed) is running.

**D269 (test of D267 option ii) — W = √3 m S T + w T^{3/2} plus a constant uplift 3m_3/2² (results/t32_gravitino_d269.txt).**
Full two-field supergravity at the CMB point (x = 1.3×10⁻⁴), S relaxed: m_3/2 = 10¹¹ GeV → V changes by 10⁻⁶, angle +4.0H²; m_3/2 = 10¹³
GeV → V −0.6%, angle +3.1H². Inflation survives. But the construction has an angle tachyon: analytically, for W = w T^{3/2} with
K = −3 ln(T + T̄), V = (3w²/8)(1 − |T|/x) after uplift, i.e. m_θ² = −2 m_3/2² for the canonical angle — negligible while H ≫ m_3/2, dominant
once H < m_3/2 (right after the cliff). (The run's numbers at x = 1 and 89 are dominated by finite-difference cancellation error, since V₀ there
is 10⁻⁵⁹–10⁻¹¹⁰ of the SUSY-breaking scale; the analytic formula is used instead.) Fix on record: the quartic Kähler term b(T − T̄)⁴ of
Ellis, Nagaraj, Nanopoulos & Olive (arXiv:1809.10114), which leaves the real-direction potential unchanged and stabilises Im T (stability for
our case not computed). Further condition: the matter mechanism needs the angle light while matter forms, m_3/2 ≲ H(T ≈ 2×10¹³ GeV) ≈ 6×10⁸
GeV (radiation value; kination raises it). Gravitino decay then (thermal Y ≈ 1.5×10⁻⁷): m_3/2 = 10⁸ → decays at T ≈ 140 GeV holding 14% of the
energy (dilution ≈ 1.15); 10⁹ → 4.4 TeV, 4.6%; 10⁷ → 4 GeV, 46% (too much). Verdict: option (ii) is viable only in a narrow window
m_3/2 ≈ 10⁸–10⁹ GeV, with two added ingredients (a tuned uplift and the quartic stabiliser) and R-parity violation — an estimate, not a
derivation. Option (i), a near-massless gravitino, stays the simpler reading. Both go into the next version's §5.2.

**D270 (pp sweep, gap 3) — Kähler-only stabilisers do NOT cure the D269 angle tachyon (stabiliser_d270.py, stabiliser2_d270.py; sympy, exact).**
For W = w T^{3/2} + uplift 3m_3/2²: with K = −3 ln(T + T̄ + b(T − T̄)⁴), m_θ²/m_3/2² = −2 for every b (the quartic is O(y⁴), no mass at y = 0);
with K = −3 ln(T + T̄ + b(T − T̄)²), still −2 for every b, and the angle's metric changes to 3(1 + 4bx)/(2x²), altering the α = 1 geometry.
(Ellis et al.'s quartic stabilises their de Sitter/Minkowski solutions, not this AdS-plus-uplift case.) A cure needs the uplift sector to
couple to the angle (e.g. K ⊃ c|Z|²(T − T̄)² for the uplifting field Z, giving m_θ² ~ c·3m_3/2² − 2m_3/2²) — which makes the angle heavy
(~m_3/2) at all times; the matter mechanism then needs m_3/2 ≲ H at matter formation (~6×10⁸ GeV), the same narrow window as D269. Verdict:
option (ii) is weaker than D269 said; option (i), a near-massless gravitino, is the reading the next version should adopt. v6 corrections
file updated.

**D271 (pp sweep, 13 Nov 20:50) — literature check of the other gaps; no status changes.**
Gap 1 (n_s): arXiv:2510.18656 (α-attractors vs Planck + BK + ACT DR6 + SPT-3G): α = 1 with standard reheating gives n_s 0.958–0.963;
P-ACT-LB 95% range at r ≈ 0.004 is 0.967–0.982, "∼2σ tension"; a stiffer post-inflation era (w > 1/3) lifts n_s to 0.965–0.968, still slightly
below P-ACT-LB — consistent with the Twist's kination value 0.9654 and our verdict. Gap 4 (birefringence): no calibrated measurement since
2609.09149; 2607.17500 is a methods paper. Gap 2 (shield): thorium proposals (2608.08133) but no new bound. Gap 5 (DE evidence):
arXiv:2609.03062 finds plain thawing at Δχ² −3.93 (ΔAIC −1.93, "insufficient"), close to PURE-TWIST's −3.37; an interacting thawing model
(Q = βHρ_de) improves to −10 — the same pattern as our fitted-β versions, which fit better but did not predict. Gaps 8–15: no new
information expected from literature; unchanged. Gap 6 waits on D268; gap 7 on the 21:01 PC check.

**D272 (pp loop 25, gap 3 option i) — what "near-massless gravitino" has to mean, and what it costs.**
With V ≈ 0 today, m_3/2 = F/(√3 M_P), so superpartners need F ≠ 0; a gravitino ≪ GeV means low-scale gauge mediation. Literature: Osato,
Sekiguchi, Shirasaki, Kamada & Yoshida (JCAP 06 (2016) 004, arXiv:1601.07386): m_3/2 < 4.7 eV (95%, Planck + lensing + cosmic shear + BAO);
Ibe & Yanagida (PLB 2017, arXiv:1608.01610): m_H ≈ 125 GeV needs m_3/2 ≳ 0.8 eV (strongly coupled messengers). Window: 0.8–4.7 eV today.
In the Twist m_3/2 ∝ x^{−3/2}: 0.8–4.7 eV today → 0.45–2.7 GeV during inflation (≪ H, harmless), ~0.7–4 keV at the cliff, 1.08–6.3 eV
at nucleosynthesis — the gravitino itself is fine (thermalised light gravitino, as in the cited bounds). The cost: V ≈ 0 at every x needs
|F|² = 3m_3/2² M_P², so F also scales as x^{−3/2}; gauge-mediated superpartner masses (∝ F/M_mess) then change by Δln m ≈ 0.30 between
nucleosynthesis (x = 73) and today (x = 89), which through threshold corrections shifts α_em by ~10⁻³ (estimate) — about 10³ above quasar
limits. So option (i) works only if the shield also keeps the SUSY-breaking scale seen by the Standard Model x-independent; the gravitino
problem reduces to the fifth-force problem (gap 2), not a separate failure. Status of gap 3: option (i) = low-scale gauge mediation,
m_3/2 ≈ 1–5 eV today, conditional on the shield; option (ii) needs the uplift sector to stabilise the angle (D270); constant high-scale W₀
excluded (D267). To go into v6 §5.2.

**D273 (pp loop 26, gap 2 shield, with the D272 twist) — literature on SUSY breaking + quintessence couplings.**
(a) Brax & Martin, "Dark energy and the MSSM" (arXiv:hep-th/0605228): in supergravity quintessence, m_3/2 = e^{κK_Q/2} m_3/2⁰ and every MSSM soft
term and fermion mass inherits Q-dependence through e^{κK_Q/2} and v_u,d(Q); u- and d-type fermions couple differently, so equivalence-principle
violation is "intrinsic" to the MSSM; no generic suppression — Cassini needs a tuned cancellation; sequestered Kähler forms left for future
work. This is exactly D272's finding (superpartner/fermion masses slide with x through e^{K/2}), now with a published precedent.
(b) Brax, Davis & Sakstein, "SUPER-Screening" (arXiv:1212.4392): SUSY breaking gives a scalar a soft mass of order m_3/2, killing light
screened scalars — "only no-scale Kähler potentials with a certain isometry group for the scalar manifold can evade these constraints."
The Twist's field is exactly such a no-scale (SU(1,1)-isometric) modulus, so its tail stays light — literature support for the field's own
lightness, not for the matter shield. (c) No published mechanism found that makes the MSSM soft terms independent of the quintessence field.
Gap 2 unchanged in severity; sharper statement for v6 §5.1: "the shield must also keep the Standard Model's SUSY-breaking scale independent of x;
generic supergravity quintessence violates this (Brax & Martin 2006); no-scale isometry protects the field's lightness (Brax, Davis &
Sakstein 2012) but not the matter couplings."

**D274 (pp loop 27, gap 2: does sequestering shield the SUSY-breaking scale?) — no.** Aparicio, Cicoli, Krippendorf, Maharana, Muia &
Quevedo, "Sequestered de Sitter string scenarios: soft-terms" (arXiv:1409.1931): with matter sequestered from the volume modulus, soft terms
are suppressed relative to m_3/2 — M_1/2 ~ m_3/2 (ln V)^{3/2}/V, m_0² ~ m_3/2² (ln V)^{3/2}/V (local) — but "the soft terms still depend on
the volume" through m_3/2 ∝ 1/V and ε_s ~ 1/ln V. In those models the volume is stabilised, so this is harmless there; for the Twist, whose
modulus rolls, any power law m_soft ∝ x^{−p} gives Δln m_soft = p ln(89/73) ≈ 0.2p between nucleosynthesis and today — the same order as
D272's 0.30, i.e. α_em shifts ~10⁻³ via thresholds. Sequestering lowers the soft scale but does not remove its x-dependence. Gap 2: unchanged;
known escapes now all checked against the SUSY-breaking scale (screening D90-91, frames, sequestering) — none works; the shield remains an
assumed symmetry acting on the hidden SUSY-breaking sector as well. Brax-Martin's open "sequestered" case answered in the negative for a
rolling modulus.

**D275 (pp loop 28, gap 15: is TWIST-G−'s tilt natural inside the Twist?) — yes at the estimate level, with the right sign
(gminus_loop_d275.py).** A chiral field X inside the no-scale log has physical mass m_X² = |W_XX|²/(2x) ∝ x⁻¹. Give it W ⊃ (M/2)X² + (λ/2)S X²:
the stabiliser's F-term splits its scalars by ±Δ with Δ² ≈ λ²V (O(1) factors not fixed). The Coleman–Weinberg supertrace then gives
δV ≈ (N/64π²)·2Δ²(ln m_X² + 3/2) — the SUSY mass M⁴ terms cancel — so δV/V ≈ −(Nλ²/32π²) ln x + const, i.e. V ∝ x^{2γ} with
γ = −Nλ²/(64π²) < 0: the SIGN TWIST-G− needs (the first TWISTG lock had the wrong sign, D1). γ = −0.0085 needs λ ≈ 2.3 (N = 1), 1.6 (N = 2),
1.2 (N = 4): λ²/16π² ≈ 0.01–0.03, perturbative. The supertrace formula was checked against the exact expression (agrees to 2% at Δ/m² = 0.5).
Consistency: today F_S is set by the dark energy, so the same loop is Δ²-sized, i.e. ~(Nλ²/32π²)ρ_DE ln x — it does not reintroduce a
Kolda–Lyth problem; it steepens the tail slightly, exactly the "tail slightly steeper" in PREREG_TWISTGN. Caveats: estimate only (O(1)
factors in Δ, gravitational loops, the X field is a new ingredient, not the reheating field χ); the constant tilt over the CMB window
assumes m_X² ≫ Δ throughout. Gap 15: G−'s naturalness concern (D230) is answered at estimate level — a perturbative coupling of one
extra field gives the needed tilt. G− stays a post-data model, scored only on future CMB data.

**D276 (pp loop 29, gaps 14 and 11).** Gap 14 (neutrino masses): the optional lead M_R ~ m_3/2 ~ 2×10¹⁴ GeV (D214, D244) assumed a high-scale
gravitino; with D267–D272 the adopted reading is a 0.8–4.7 eV gravitino, so that lead is dropped. The seesaw itself is untouched: M_R is a
free scale, and 6×10¹²–6×10¹⁴ GeV still sits inside the model's scales (Yukawa ~0.1–1 for m_ν ≈ 0.05 eV). Gap 14 stays LOW; neutrino
masses are assumed. Gap 11 (Hubble): no new primary local-H₀ result found in this search — only secondary reports (a news summary of a
~73 km/s/Mpc sub-1% distance-ladder result with no paper named, Apr 2026; a review noting CCHP values often fall between SH0ES and Planck).
Not used. The Twist's H₀ ≈ 65.7 cost is unchanged; gap 11 stays LOW–MEDIUM.

**D277 — the four locked PC matter checks, scored at full size (scheduled check 21:01 CT; runs finished 18:04–18:16 CT on the PC; copies in
field_tests/results/matter_pc/).** All at m_σ = 5.8×10¹⁰ GeV, heat share 0.8%, exp cliff 4/π, μ = 1, n = 125.
- D124 confirmation (locked: 0.6–1.6× observed): matter_refit_check n_B/s = 1.090×10⁻¹⁰ = **1.253×** → PASS. m_σ ≈ 6×10¹⁰ GeV stands
  (exact 1× would sit slightly higher, ∝ m_σ^−0.89 → ≈ 7.5×10¹⁰ GeV). Entropy dilution in this run ×4.59 (not the 1.2–1.5 quoted earlier for
  the n = 10-era runs — corrected here).
- D129 (D127 Kähler form within 10% of the refit): 1.257× vs 1.253× (0.3%) → PASS.
- D160 (TWIST-K within ×3 of the gauge construction): 1.256× vs 1.253× → PASS. The matter yield is the same in the adopted construction.
- D137 (locked: |dlnY/dlnσ₀| ≤ 5 and |dlnY/dy₀| ≤ 10⁴): σ₀ × 1.05 → 1.501×, so dlnY/dlnσ₀ = **3.70** → PASS; y₀ = 0.01 → 9244×, so
  dlnY/dy₀ = **891** (secant) → PASS. Consequences: hidden-axion isocurvature S_B = 3.70 · δσ/σ₀ = 1.1×10⁻⁵ (δσ/σ₀ = 3×10⁻⁶), 3.7×10⁻⁵
  (10⁻⁵), 7.4×10⁻⁵ (2×10⁻⁵) against the D134 bound 5×10⁻⁵: passes for decay constants f ≳ 0.1 M_P but with a margin of only ~1.4× at
  f = 0.1, and FAILS for the smallest f (δσ/σ₀ ≈ 2×10⁻⁵). The earlier "8× below" (sensitivity 0.64 assumed) is withdrawn. The angle's
  contribution, 891 × 2×10⁻¹⁰ ≈ 2×10⁻⁷, is safe — but the y₀ response is strongly non-linear (y₀ = 0.01 gives 9244×): the yield depends
  sharply on the angle's start, so the matter result needs y₀ ≈ 0 at the end of inflation (which the heavy angle, m/H ≈ 2, provides).
- TWIST-P deviation D1 condition ("void PREREG_TWISTP_L if D137 fails for the angle") not triggered: TWISTP_L stands.
Gap 7 status: matter confirmed in TWIST-K at m_σ ≈ 6×10¹⁰ GeV (still a fit); isocurvature passes the locked rule but is marginal and
restricts the hidden axion's decay constant to f ≳ 0.1 M_P (estimate from δσ/σ₀ = H/2πΛ, D257).

**D278 (pp loop 30, gap 7: is the isocurvature bound tighter now?) — no; margin stands at ~1.4–1.5×.** ACT DR6 extended models
(Calabrese et al., arXiv:2503.14454): scale-invariant uncorrelated CDM isocurvature 10¹⁰ P_II < 1.1 (P-ACT, 95%), Planck alone < 0.9; lensing
+ BAO do not change it. Converted to baryon isocurvature (S_b = S_c Ω_c/Ω_b, ratio 5.36): S_b < 5.1×10⁻⁵ (Planck), 5.6×10⁻⁵ (P-ACT) — the
same as D134's 5×10⁻⁵. With D277's sensitivity the hidden axion gives S_B ≈ 3.7×10⁻⁵ at f = 0.1 M_P: margin 1.4× (Planck) / 1.5× (P-ACT).
The axion's fluctuations are nearly scale-invariant and uncorrelated with curvature, so the scale-invariant uncorrelated bound is the right one.
Gap 7 unchanged: passes, marginal; a future factor-~2 improvement in isocurvature limits (Simons Observatory / CMB-S4 class) would test the
f ≈ 0.1 M_P end. Not a locked prediction — recorded as a sensitivity.

**D279 (pp loop 31, gap 13 + D272 consequences) — what the eV gravitino adds and changes.** With the adopted 0.8–4.7 eV gravitino (D272):
(1) It thermalises through its goldstino couplings (√F ≈ 10⁵ GeV) and is a warm relic: Ω_3/2/Ω_DM ≈ m_3/2/86 eV ≈ 0.9–5.5% (86 eV = full DM,
Osato et al. 2016) — inside the 4.7 eV bound by construction. (2) Extra radiation: ΔN_eff ≈ (10.75/g*_dec)^{4/3} ≈ 0.017–0.047 (g*_dec 229–107)
— replaces the model card's "ΔN_eff ~ 3×10⁻⁸" (that was a heavy/massless-gravitino estimate). CMB-S4-class σ(N_eff) ≈ 0.03 could reach the upper
end. (3) The main dark matter (gravity-only fermion, 100–500 TeV, from graviton bremsstrahlung in χ̃ decays) is unaffected: χ and χ̃ couple to
the SUSY-breaking sector only gravitationally, so their mass splitting is ~m_3/2 (eV) and χ̃ → χ + gravitino has no phase space to compete.
(4) The gravitino problem that excluded a gravitino dark matter (D261) no longer applies in this reading; the gravitino is a few-percent warm
component, not the dark matter. Status: estimates; to v6 (§5.2) and the model card's predictions (extra radiation row).

**D280 (pp loop 32, gap 4: specify the domain-wall fallback for birefringence) — literature, not built into the Twist.** Kitajima, Kozai,
Takahashi & Yin, "Power spectrum of domain-wall network and its implications for isotropic and anisotropic cosmic birefringence"
(arXiv:2205.05083): an axion-like field with a periodic potential forms walls; with L = −c_γ(α/4π)(φ/f)FF̃ the isotropic rotation is
β ≃ 0.21 c_γ deg, independent of the ALP mass and f. For the current β = 0.277° ± 0.057°: c_γ ≈ 1.3 (1.0–1.6 at 1σ) — consistent with D252's
"C_γ ≈ 5" only up to the definition of the coupling (D252 used a different normalisation; this paper's number is the one to quote). Its
signature: each direction is rotated by either 0 or 0.42c_γ deg (observer in one of two vacua), giving a correlated anisotropic
birefringence spectrum with a peak near the horizon scale at recombination, amplitude ∝ β² (shown in their Fig. 2, factor-2 band),
detectable by CMB-S4/PICO even at the low end of β. A homogeneous rolling ALP (TWIST+ALP) gives the same isotropic β without this pattern but
with its own tomographic ratio R = β_reion/β_rec (D250). So the two fallbacks are distinguishable: anisotropic spectrum (walls) vs R (rolling
ALP). Neither is locked as a Twist prediction beyond PREREG_TWIST_ALP; if a calibrated β is confirmed, a wall-network lock should be written
before the next anisotropic-birefringence release. Gap 4 status unchanged (HIGH, rising); fallback now specified with a literature number.

**D281 (pp loop 33, gap 10 strong CP) — the Twist's required post-inflation QCD axion (40–600 μeV, D219/D236) is not yet probed at QCD
sensitivity.** CERN Courier, "In pursuit of the post-inflation axion": ADMX/CAPP/HAYSTAC lead below ~25 μeV; MADMAX (dielectric, target
40–400 μeV) prototype run 2024 near 19 GHz beat CAST/astrophysical bounds but not KSVZ/DFSZ; its next prototype installs mid-2026–2029, 4 T magnet
~2030; ALPHA (plasma haloscope, 40–400 μeV) Phase I data 2026, axion search 40–80 μeV in 2027–28, Phase II to ~200 μeV at DFSZ. No part of
40–600 μeV is excluded at QCD-axion couplings yet. This is not a Twist prediction (the Twist needs an extra axion; it does not fix its mass
beyond the post-inflation class), but it is the experimental window for the cost item "strong CP needs a separate axion": a KSVZ/DFSZ axion
found at 40–400 μeV would be consistent with it; ALPHA/MADMAX covering 40–400 μeV with no signal would leave only 400–600 μeV. Gap 10
unchanged (LOW–MEDIUM); decided by ALPHA (2027–28) and MADMAX (~2030+).

**D282 (pp loop 34, gap 9 string home) — the published runaway-quintessence string scenario uses the same shield assumption, stated
qualitatively.** Olguín-Trejo, Parameswaran, Tasinato & Zavala, "Runaway quintessence, out of the swampland" (arXiv:1810.08634): a
supersymmetric modulus Φ = φ + iθ (volume, n = 3, or complex structure/dilaton, n = 1) rolls on e^{−2αφ} from a non-perturbative term
A e^{−αΦ}; the axion stays frozen. On matter: they assume the modulus is "localised away from the Standard Model in the extra dimensions",
coupling only gravitationally to the SUSY-breaking sector, and state there are then no observable fifth forces or varying constants — no
estimate given. Our D272–D274 analysis is exactly the quantitative version of that assumption: a gravitational coupling to the SUSY-breaking
sector already makes soft masses slide as e^{K/2} with a rolling modulus (Brax–Martin; sequestering does not remove it), giving
Δα/α ~ 10⁻³ unless the shield covers the SUSY-breaking scale. So the closest published string scenario does not supply the missing
mechanism; it assumes it. (A 2026 item, arXiv:2603.25797, was not reachable.) Gap 9 unchanged; the Twist's string-level problem is shared
with the runaway-quintessence literature, not specific to it.

**D283 (pp loop 35, gap 8: the cliff depth n) — closest published mechanism is the same relabelling as D255.** Yokoyama, "A cosmological
constant from degenerate vacua" (arXiv:hep-th/0110137): the residual vacuum energy of instanton-split degenerate vacua is
ρ_v ≅ M⁴(8π/g²)⁴ e^{−8π²/g²}; requiring 10⁻¹²⁰ M_G⁴ gives α = 1/44.4–1/47 for M = 5×10¹⁶ GeV–M_G — "without small numbers", but α is fixed
by the input, not predicted. The Twist's e^{−2n} with 2n ≈ 249 is the same structure (D255: n = π/α_h, α_h ≈ 1/39.8; the prefactors differ).
Like Yokoyama's, it trades one tuning (Λ) for one gauge coupling known to ~0.3%. Gap 8 unchanged: n is chosen; a derivation would need a
UV theory that fixes a hidden gauge coupling at the per-mille level. No further literature search planned for this gap.

**D284 (pp loop 36, gap 1 n_s: D275 against the published radiative-correction work).** (a) Ellis, Gherghetta, Kaneta, Ke & Olive,
"Effects of radiative corrections on Starobinsky inflation" (arXiv:2510.15137): non-SUSY one-loop corrections from Yukawa couplings to the
inflaton reach the ACT value (n_s 0.9752 ± 0.0030) for 3.8×10⁻⁴ < y < 5.6×10⁻⁴ (T_RH ≈ 2×10¹¹ GeV); scalar trilinears never reach it; the
corrections are additive polynomial-log terms, not a multiplicative power; in exact SUSY they cancel (supertrace), SUSY breaking gives
O(m̃²φ²/64π²), and no-scale supergravity Starobinsky is explicitly left for future work. (b) Gialamas, Karam, Racioppi & Raidal
(arXiv:2504.06002): λ_eff = λ[1 + δ ln(φ/M_P)], δ ≈ 1–3% reaches ACT, Δr ≈ 4δ/N — the multiplicative-log structure D275 finds, for
non-minimal Higgs inflation. Reading: D275's mechanism — inflaton-sector F_S splitting of a field inside the no-scale log, giving
V ∝ x^{2γ} with γ = −Nλ²/64π² — is not in the published literature we found; it is the supergravity case Ellis et al. leave open, and it
evades the exact-SUSY cancellation they note because the splitting comes from the inflaton's own F-term. Its predicted r (≈ 0.0068 for
G−, from the locked scan) is consistent with Gialamas et al.'s Δr ≈ 4δ/N scaling (δ ≈ 2γ-equivalent). Gap 1: unchanged as a verdict
(INCONSISTENT for the plain Twist); the G− variant now has a computed (estimate-level) mechanism and a literature gap it would fill. Worth a
proper one-loop supergravity calculation if Danny wants to develop G−.

**D285 (pp loop 37, gap 1/15: full-supergravity one-loop check of D275) — D275's estimate is WRONG in its mechanism; the full calculation
instead reproduces TWIST-C (gminus_sugra_loop_d285.py, gminus_ns_d285b.py).**
Setup: TWIST-K plus a field X inside the no-scale log, K ⊃ −X X̄/3, W ⊃ (M/2)X² + (λ/2)S X². Full three-field F-term potential at S = X = 0,
X's two real scalar masses by finite differences, fermion mass e^{K/2}|W_XX|/K_XX̄ = M²/(2x)… , Coleman–Weinberg with canonical masses.
Findings: (1) Every scalar in the log gets a universal Hubble-induced shift: m_s² = m_F² + δ with δ ≈ +0.2 m² ≈ 2.4H² (both real directions),
even at λ = 0; λ changes dV/V only at the 10⁻⁶ level. So STr M⁴ ≈ 4 m_F² δ, NOT 2Δ² as D275 assumed (D275 dropped the cross term) — the
λ S X² mechanism is subdominant. Correction to D275 and D284: withdraw "γ = −Nλ²/64π²" and "fills the gap Ellis et al. leave open" as stated.
(2) Because m_F² ∝ 1/x, the one-loop term is dV/V ≈ b x*/x (x* = 1.3×10⁻⁴), not a power law x^{2γ}. A heavy X (M = 1, m_F² ~ 10⁴ m²)
gives dV/V ~ 10² — it destroys the plateau; a light one (M = 10⁻³) gives a tachyonic X (m² ≈ −1.4H²). A useful size needs m_F ~ m (the
inflaton mass), which is a choice. (3) Slow roll with V_tree(1 + b x*/x), N* = 57: b = 0 → n_s 0.9650, r 0.0036 (the Twist); b = 0.003 →
0.9703, 0.0042; b ≈ 0.0053 → n_s ≈ 0.974, r ≈ 0.0048; b = 0.01 → 0.984, 0.0061. (4) This is exactly TWIST-C's form: W ∝ S(T + c) gives
V ∝ (1 + c/x)² ≈ 1 + 2c/x, and b x* = 2c gives c ≈ 3.4×10⁻⁷ — the locked TWIST-C value (3.5×10⁻⁷, r ≈ 0.005). So TWIST-C's "sharply tuned"
c is what a one-loop correction from a field of roughly the inflaton's mass inside the no-scale log generates; the tuning moves into that
field's mass and the renormalisation scale (the ln μ piece multiplies V/x, so b is scheme-dependent and effectively a renormalised
parameter). TWIST-G−'s power-law tilt is NOT what this loop produces. Status: estimate-level, one field, one-loop, no gravitational loops.
Gap 15 updated: C gains a loop origin (D285); G−'s naturalness reverts to "loop analogue only" (D246). Both stay post-data models.

**D286 (pp loop 38) — two corrections from rechecking D285, and a new assumption for the reheating field χ.**
(a) Units error in D285: its scripts set m = 1 and M_P = 1 together, so the Coleman–Weinberg term (∝ m⁴) was compared with V (∝ m²M_P²)
without the factor (m/M_P)² = 4.4×10⁻¹⁰. Real dV/V = 4.4×10⁻¹⁰ × the printed values. Consequences: M_code = 1 (m_F ~ 60m at x*) gives
dV/V ~ 5×10⁻⁸ — negligible, not "destroys the plateau" (withdrawn). TWIST-C's b ≈ 0.0053 needs W_XX ≈ 6.7×10⁻³ M_P, i.e. a field of physical
mass m_F ≈ 0.4 M_P at the CMB point inside the no-scale log — not "about the inflaton mass" (withdrawn). The qualitative D285 results stand:
the universal Hubble-induced term dominates, dV/V ∝ 1/x, and the TWIST-C form (c ≈ 3.4×10⁻⁷) follows; only the required mass changes.
The X tachyon for small M (m² ≈ −1.4H², tree level) is unaffected.
(b) The reheating field χ (W_χχ ≈ 2πh x₀ ≈ 0.13 M_P on the plateau, D118) placed inside the no-scale log would give real dV/V ≈ 6.8 at
the CMB point (4.3 at x = 2×10⁻⁴), ∝ 1/x — an order-one, b ≈ 7 deformation that would push n_s far above 1: inconsistent. Placed with a flat
Kähler term |χ|² its physical mass picks up e^{K/2} = (2x)^{−3/2} ≈ 2×10⁵ — worse. The x-independent choice is modular weight 3/2,
K ⊃ |χ|²/(T + T̄)^{3/2}: then e^K|W_χχ|²/K_χχ̄² = |W_χχ|², the loop term is ∝ V (no tilt), and D156's "loop shift negligible" holds.
D156 implicitly assumed this. **New assumption for v6: χ has modular weight 3/2** (analytic; not run numerically). Without it the plain
Twist's inflation prediction is not what is quoted. Gap 15 updated (C: loop origin needs a ~0.4 M_P field inside the log; G−: analogue
only). Corrections file updated.

**D287 (pp loop 39) — D286's weight-3/2 assumption for χ verified in full supergravity (chi_weight32_d287.py; results/chi_weight32_d287.txt).**
K ⊃ |χ|²/(T + T̄)^{3/2}, W_χχ = 6190 m (≈ 0.13 M_P, D118), λ = 0, TWIST-K background, x = 5×10⁻⁵–4×10⁻⁴: fermion and both scalar masses
m² = 3.8316×10⁷ m² at every x (x-independent to 5 digits); the Hubble-induced shift is the same at every x; the one-loop term is
dV/V = 3.994×10⁶ × (m/M_P)² = 1.8×10⁻³, constant across the CMB window — it only renormalises the amplitude (absorbed by A_s);
γ_eff ≈ −1×10⁻¹⁰ (no tilt). So with modular weight 3/2 the plain Twist's n_s ≈ 0.964–0.965 stands; D156's conclusion is confirmed, now with
its hidden assumption stated and checked. Assumption list for v6: χ weight 3/2 (verified consistent, not derived).

**D288 (pp loop 40) — Hubble-induced masses of light fields during inflation (e.g. the Higgs), three Kähler placements, full SUGRA at the
CMB point (λ = 0, M = 10⁻⁶ m; scripts gminus_sugra_loop_d285.py, chi_weight32_d287.py, light_flat_d288.py).** m²/H²: inside the no-scale
log +2.0; modular weight 3/2 +3.0; flat |X|² +3.7 (of which 0.7 is the e^{K/2}-enhanced SUSY mass). All positive: a light field stays at
its origin during inflation; no Higgs-instability or runaway from supergravity alone. For m²/H² = 2 (inside the log) superhorizon
fluctuations decay as a^{−1} (ν = 1/2), negligible after ~55 e-folds; for ≥ 2.25 they are not produced. The tachyon seen in D285
(m² ≈ −1.4H²) came from the direct coupling λ S X² with λ = 1 — so the condition is: Standard-Model scalars must not couple to the
stabiliser S at O(1). Recorded as a consistency condition (not a new assumption: the SM already has no S coupling in the model).

**D289 (overnight pp loop 1, gap 2) — D272's α drift sharpened (soft_drift_alpha_d289.py).** If MSSM superpartner masses slide as
x^{−3/2} (eV-gravitino reading without a shield on the SUSY-breaking scale), their QED threshold contributions (Δb = 8.33: squarks,
sleptons, H±, two charginos) give Δ(1/α) = (Δb/2π)Δln m = 0.394 between nucleosynthesis and today, i.e. Δα/α ≈ 2.9×10⁻³ (D272's
order-of-magnitude 10⁻³ confirmed, factor 3 larger). Today's rate, with d ln x/dt = √(2/3)·0.45H₀ = 2.5×10⁻¹¹/yr: d ln α/dt ≈ 3.7×10⁻¹³/yr,
about 4×10⁵ times the atomic-clock bound (~10⁻¹⁸/yr). So the shield on the SUSY-breaking scale must hold to ≲ 3×10⁻⁶ in d ln m_soft/d ln x —
quantified requirement added to gap 2. No status change.

**D290 (pp loop, gap 5 dark-energy evidence) — theory priors shrink the DESI preference to the Twist's level.** arXiv:2509.13318 ("How
theory-informed priors affect DESI evidence for evolving dark energy"): DESI DR2 BAO + Planck gives ~3.1σ with uniform w₀–w_a priors,
~1.8σ with an exponential-potential prior (w₀ = −0.63, w_a = −1.12) and ~1.3σ with a hilltop prior; adding SNe with the physical prior:
Pantheon+ ~1σ, Union3 ~2σ, DES Y5 ~3σ (possibly low-z systematics). No λ posterior (prior U(0, 2); λ ≲ √3 for an acceleration history).
Reading: once dark energy is required to be a physical thawing field, the evidence for evolution is ~1–2σ except with DES Y5 — the same
size as PURE-TWIST's 1.8σ local / 0.6–1.0σ trials-corrected (D262), and our DES Y5 swap also gave the Twist its strongest result. Gap 5
unchanged (no evidence on current data; DES Y5 is the one dataset that prefers it, with a systematics caveat).

**D291 (pp loop, gap 3: is the 0.8–4.7 eV gravitino window still open?) — narrowly, and only in non-minimal models.** Lu & Shirai,
"Low-scale gauge mediation after LHC Run 2" (arXiv:1712.02359): perturbative low-scale GMSB with m_3/2 = 4.7–16 eV is largely excluded
(gluino ≳ 2 TeV, wino ≳ 0.7 TeV); minimal GMSB cannot give m_H = 125 GeV below ~10 eV; strongly coupled messengers "still endure" (rough).
Hook, McGehee & Murayama, "Cosmologically viable low-energy supersymmetry breaking" (arXiv:1801.10160): a vector-mediated model with
tree-level U(1) D-term breaking gives m_H = 125 GeV, gluino > 2.03 TeV, with m_3/2 as low as 1.0–2.3 eV (v_S ≈ 44–240 TeV) — the window is
open there; they warn better cosmic-shear data (DES, HSC) could close low-energy SUSY breaking altogether. Reading for the Twist: option (i)
needs a specific non-minimal sector (e.g. Hook–McGehee–Murayama vector mediation or strongly coupled messengers); minimal GMSB does not work.
Note a tension to check later: their SUSY breaking is a D-term, while the no-scale V ≈ 0 argument of D272 used F-terms; a D-term
contributes +D²/2 and must still be cancelled by −3m_3/2² (fine at the level of the CC tuning). Gap 3 stays MEDIUM; a new falsifier: an
improved cosmic-shear bound below ~1 eV would remove option (i). Added to the v6 corrections.

**D292 (overnight pp loop 2, gap 3) — a SUSY-breaking sector with x-INDEPENDENT scales fits the Twist (weight3_polonyi_d292.py, sympy, exact).**
W ⊃ w T^{3/2} + μ² X, K ⊃ |X|² (T + T̄)^{−3} [1 + c((T − T̄)/(T + T̄))²] (Polonyi field X with modular weight 3, angle-dependent metric
coefficient c). At X = 0, exactly: V(real T) = μ⁴ − 3w²/8 — a constant for every x, set to zero by the single CC tuning μ⁴ = 3w²/8 (no
separate "uplift" put in by hand: X's F-term is the uplift); m_3/2 = w/2^{3/2}, x-independent; the physical F_X = e^{K/2}(K^{XX̄})^{1/2}μ²
= μ², x-independent; the angle mass m_θ² = (4c − 2) m_3/2² — stable for c > 1/2 (D270's −2m_3/2² is the c = 0 case). Consequences:
(1) D267's sliding gravitino and D272/D289's sliding SUSY-breaking scale are both removed by modular weights (T^{3/2} in W, weight 3 for X);
gauge-mediated soft masses ∝ F_X/M_mess are x-independent if the messengers carry weight 3/2 (as χ, D287). (2) Options (i) and (ii) merge:
the same sector serves an eV gravitino (low-scale gauge mediation, D291's non-minimal models) or a heavy one. (3) The angle gets mass
~m_3/2 at all times: for the eV gravitino that is ≪ H during matter formation (angle light then) and ≫ H₀ today (angle pinned at zero —
consistent with BIREF-NULL). (4) Effect on inflation: w ~ m_3/2 ≪ m, negligible (D269). Status: gap 3 MEDIUM → LOW–MEDIUM; the
SUSY-breaking part of the shield is achieved by weight assignments (assumed, not derived); the rest of the shield (Yukawas, gauge kinetic
functions independent of T) remains gap 2. Weights now assumed: χ 3/2, messengers 3/2, X 3, W ∋ T^{3/2}.

**D293 (pp loop, gap 2: can modular weights alone shield the Standard Model?) — no, confirming D91 with a cleaner check
(weights_shield_d293.py; exact rational algebra).** Conditions: Yukawas x-independent (p_Q + p_U + p_Hu = p_Q + p_D + p_Hd = p_L + p_E + p_Hd
= 3), gauge couplings x-independent at one loop including the Kaplunovsky–Louis terms up to a universal Green–Schwarz δ
(−3(ΣT_a(r) − T(G_a)) + 2ΣT_a(r)p_r = δ for SU(3), SU(2), U(1)_Y), and an x-independent μ-term (p_Hu + p_Hd = 3). Results: with the μ
condition — no solution, with or without δ. Dropping the μ condition — a two-parameter family exists but needs δ_GS = −27 and weights far
from string values (smallest max|p| over the family = 6, e.g. p_Q −11/3, p_U = p_D = 2/3, p_L 3, p_E −6, p_Hu = p_Hd = 6); a universal GS term of that size is unavailable on Z₃-type
orbifolds (D199). So the D292 weight trick fixes the SUSY-breaking scale but cannot make the MSSM's couplings and masses T-independent: the
remaining shield (gap 2) is not a modular-weight assignment. Gap 2 unchanged; requirement restated precisely for v6.

**D294 (pp loop, follow-up to D292: is X = 0 the vacuum?) — no, but the structure survives with a quartic stabiliser (polonyi_vac_d294.py).**
With K ⊃ |X|²(T+T̄)⁻³ − q|X|⁴(T+T̄)⁻⁶ and μ⁴ = 3w²/8: along Re X there is the usual Polonyi tadpole, dV/ds|₀ = −√6 w²/(8x^{3/2}); in
canonical units it is x-independent, −(√6/4)w². Im X has none. The sgoldstino mass is m_X² = (12q − 2) m_3/2² in both directions (needs
q > 1/6). The vacuum shifts to X_c ≈ 2√6/(12q − 2) M_P, x-independent in canonical units, so the x-independence of D292 should survive the
shift (not re-verified symbolically at the shifted point). Polonyi problem: with an eV gravitino, a weakly stabilised sgoldstino (q ~ 10²,
m_X ~ 30 eV, shift ~4×10⁻³ M_P) would be displaced after inflation and overclose the universe by ~10⁸ (estimate); it is avoided if the
sgoldstino is heavy, q ≳ 10⁷ (Λ ≲ 10¹⁵ GeV) — which is the generic case in low-scale gauge mediation, where the SUSY-breaking dynamics at
√F ~ 10⁵ GeV gives the sgoldstino a mass far above m_3/2. Added condition for v6: the SUSY-breaking sector must be dynamical
(heavy sgoldstino), not a bare Polonyi field. Gap 3 stays LOW–MEDIUM.

**D295 (overnight pp loop 3) — D294's claim verified numerically (polonyi_shift_d295.py; results/polonyi_shift_d295.txt).** q = 10,
μ⁴ = 3w²/8, V minimised over real X at x = 1, 10, 89: the vacuum sits at canonical X = 0.026964 M_P and V_min = −0.0121177 w² at all three
x, identical to 8 digits. The Polonyi shift only lowers the constant (retune μ⁴ by 1.2×10⁻² w² to restore V = 0), and the sector stays
x-independent. D294's linearised shift (2√6/(12q − 2) = 0.042) overestimated the exact value (0.027) by ~1.5×; the Polonyi-problem
condition (heavy sgoldstino) is unchanged. D292 + D294 + D295 together: a complete x-independent SUSY-breaking sector at tree level.

**D296 (overnight pp loop 4, gap 1 n_s) — no new n_s measurement; SPT-3G Ext-10k is a forecast.** Vitrier, Fichman, Balkenhol et al.
(SPT-3G, arXiv:2510.24669, dated Jul 2026): pipeline/forecast on mock Planck-cosmology data; σ(n_s) = 0.0051 (Ext-10k TT/TE/EE), 0.0045
(+φφ), 0.0029 (+ Planck). No central value, no DESI. For the Twist (n_s 0.9642–0.9654) the decisive split is still BAO–CMB (D223, D240):
an independent CMB-only σ ≈ 0.003 measurement will separate 0.965 from 0.974 at ~3σ by itself, without DESI. Gap 1 unchanged.

**D268 status note (22:05).** The coarse-step copy (step 0.1) was killed by the container's memory limit after 18 min (3.8 GB resident);
the full run (step 0.02) is at 2.3 GB and climbing after 90 min. The matter chain leaks memory in this container. On Danny's PC the same
code finished each locked run in ~5 min (D277). The coupling comparison is best run on the PC — that needs Danny's OK (no PC jobs
unattended). Leaving the full run going in case it finishes under the limit.

**D297 — D268 result: the matter yield under the alternative coupling reading (results/coupling_alt_d268.txt; cloud, 2 h).** Same run,
both readings in one pass (m_σ 5.8×10¹⁰ GeV, heat 0.8%, TWIST-K-equivalent exp cliff, μ = 1): canonical √(3/2)y′/x → n_B/s = 1.090×10⁻¹⁰
(1.253×, reproduces the locked PC result D277 exactly — validates the cloud run); alternative √(3/2)(y′ − c p′ y)/x, i.e. coupling to
∂(1/γ_BI) = ∂(y/x) → 4.82×10⁻¹¹ (0.554×); ratio 0.442. The ambiguity changes the yield by a factor 2.3, which the one fitted input absorbs:
with the yield ∝ m_σ^−0.89, exact 1× needs m_σ ≈ 7.5×10¹⁰ GeV (canonical) or ≈ 3.0×10¹⁰ GeV (alternative). So the referee's issue 10 is
quantified: the matter mechanism works under either reading; the normalisation choice moves the fitted hidden mass by ×2.5 and is a stated
choice, not a hidden one. c_A = √(3/8) remains "fixed given the normalisation". Gap 6: closed at this level (MEDIUM → LOW).

**D298 (overnight pp loop 9) — a possible new problem from D292: the angle's misalignment energy.** D292 gives the Immirzi angle a
late-time mass m_θ = √(4c − 2) m_3/2 ~ 1–5 eV. During the radiation era its Twist-sector mass (∝ V_tail) is ≪ H, so the angle is frozen
wherever the matter-genesis dynamics left it; it starts oscillating when H ≈ m_θ (T ~ 5×10⁴ GeV) and behaves like an ALP relic:
Ω h² ≈ 0.12 (m_θ/10⁻²² eV)^{1/2} (φ_i/10¹⁷ GeV)². Not overclosing needs φ_i ≲ 3×10¹¹ GeV (1 eV) – 2×10¹¹ GeV (5 eV), i.e. a leftover
|y_end| ≲ 5–8×10⁻⁶ at x ≈ 73 (canonical φ = √(3/2) y/x M_P). The matter runs print y_end = 0.000 (3 decimals; the angle reverses twice and
returns near zero), which does not settle it: |y_end| ~ 10⁻⁴ would overclose by ~10². A precision rerun of the baseline (yend_precise_d298.py,
6 significant figures) is running (~2 h in the cloud). Escapes if it fails: tune c = 1/2 (massless angle today — then its relic is pure kinetic,
∝ a⁻⁶, harmless), or a heavy gravitino branch where m_θ > H when the angle is released. Status: OPEN, pending the rerun; new gap item.

**D299 — D298 resolved: the angle relic does not overclose; it is a 12–28% dark-matter component (estimate) (results/yend_precise_d298.txt).**
Precision rerun of the baseline (m_σ 5.8×10¹⁰ GeV, heat 0.8%; also reproduces D268/D297 exactly): at the end of the matter run
(11 e-folds after inflation, x_end = 29.8) y_end = 1.1085×10⁻⁶, i.e. a canonical misalignment φ_i = √(3/2) y/x M_P = 1.1×10¹¹ GeV. With D292's
late angle mass m_θ ~ 1–5 eV (ALP misalignment, Ω h² ≈ 0.12 (m/10⁻²² eV)^{1/2}(φ_i/10¹⁷ GeV)²): Ω_θ h² ≈ 0.015 (1 eV) – 0.033 (5 eV),
i.e. ~12–28% of the dark matter — below overclosure by 4–8×. Caveats: y keeps coasting after the run ends (x 29.8 → 73); the residual velocity
decays as a⁻³, so the drift should be small but is not computed; the relic formula is order-of-magnitude. Consequences: (1) D298's problem is
not realised for the computed history; (2) the eV-gravitino branch predicts a cold ALP-like component from the Immirzi angle at the 10–30%
level, with mass √(4c − 2) m_3/2 — a new, testable consequence (not locked; would need a lock before any data comparison). (3) The escape
c = 1/2 is not needed.

**D300 (overnight pp loop 21) — is D299's eV angle relic constrained? No.** Its only matter coupling is the Nieh–Yan axial coupling
c_A ∂θ J₅/M_P; the induced axion-electron coupling is g_ae ≈ 2c_A m_e/M_P ≈ 3×10⁻²² — nine orders below red-giant/white-dwarf cooling
bounds (~10⁻¹³); no photon coupling (D249 structural), so no haloscope/helioscope or birefringence signal. As a coherently oscillating field
with m ≳ 1 eV it is ordinary cold dark matter on all cosmological scales (Jeans scale far below Mpc). So the 12–28% component is invisible to
current probes — "testable" in D299 should read "consistent but practically unobservable"; correction recorded here.

**D301 (pp loop, gap 4 birefringence) — a combined SPIDER + Planck + ACT fit points toward miscalibration.** Yin, Xiong, Kochappan, Lee &
Ghosh, arXiv:2510.25489 (v2, Nov 2025): they fit the total angle α + β (miscalibration + cosmic), since "α and β cannot be fully disentangled";
EB: SPIDER 0.35° ± 0.69°, Planck 0.29° ± 0.03°, ACT 0.19° (+0.03/−0.04°), Planck+ACT 0.21° ± 0.03°, all three 0.22° ± 0.03°. The Planck and
ACT angles "differ by > 3σ", which they say "hints that a polarisation miscalibration angle may be preferred" (their conclusion is not fully
consistent on this). A cosmic β is the same on every experiment; a > 3σ disagreement between experiments favours instrumental angles. For the
Twist (BIREF-NULL, β = 0): mildly favourable but not scored — the locked rule needs a calibration-independent measurement. Gap 4 HIGH →
HIGH but no longer "rising".

**D302 (deep loop 1, gap 2) — D293 put in string context with Ibáñez & Lüst (hep-th/9202046, read).** One-loop couplings:
1/g_a² = k_a/g_s² + (b_a/16π²) ln(M_s²/μ²) − (1/16π²) Σ_i (b'^i_a − k_a δ^i_GS) ln[(T_i + T̄_i)|η(T_i)|⁴], with
b'_a = −3C(G_a) + ΣT(R)(3 + 2n_R) for the overall modulus (their weights n = −p in our notation). The moduli dependence cancels completely only
when b'_a/k_a is the same for every group (= δ_GS), absorbed into the dilaton by the Green–Schwarz shift S → S − (k_a/8π²)δ_GS ln(…); for
Z₃ (all planes rotated, no N = 2 threshold) this is the only option. Their result: for Z₃ and Z₇ at level one, NO allowed MSSM weight assignment
satisfies the universality conditions — minimal Z₃/Z₇ models are excluded — and minimal unification instead needs T-dependent thresholds with
n_Q = n_D = −1, n_U = −2, n_L = n_E = −3 and Re T ~ 16. Reading for the Twist: D293's "no solution" is the field-theory face of this known
result (MSSM-only spectrum). Escape: a non-minimal spectrum (extra charged states) that makes b'_a/k_a universal, so the GS shift removes all
T-dependence from the gauge couplings; then the physical couplings depend only on the GS-shifted dilaton, and they are x-independent if
that dilaton is fixed independently of T (the D200 BGW route). That route already failed for another reason — the string coupling is strong
today (D204, D209). So gap 2 reduces to a single string-level problem: a heterotic model with universal δ_GS (extra matter), a BGW-type
dilaton, and weak coupling at x ≈ 89. Yukawas: untwisted-sector couplings are T-independent; twisted ones carry η(T) factors (to check in a
later loop). Gap 2 status unchanged (HIGH), but the obstruction is now located precisely.

**D303 (deep loop 2, gap 4: when will a calibration-independent β exist?)** Read: Coppi et al., PROTOCALC (arXiv:2502.14473) — a drone-borne
W-band polarised source, deployed twice in the Atacama with the Simons Observatory SATs and CLASS; field data constrain the source roll angle to
0.045° (statistical; lab camera-to-grid offset 0.03° ± 0.002°); the SO requirement for B-modes is 0.2°, and birefringence needs "even more
stringent". Novelli et al., POLOCALC (arXiv:2606.20171) — drone source, target accuracy 0.1° → 0.01°, flights to 5600 m, observed with SO SATs
and CLASS; "further improvements are required", no achieved absolute accuracy and no timeline. Reading against PREREG_BIREF_NULL (needs total
error ≤ 0.10° with calibration independent of the Galactic-foreground EB method): the hardware exists and is at the ~0.05° statistical level, but
no systematic budget ≤ 0.1° is published yet. Expected decider: SO SATs (and CLASS) with drone calibration, plausibly within a few years; LiteBIRD
in the 2030s. Combined with D301 (Planck–ACT angles disagree > 3σ), gap 4 stays HIGH but the current 0.28° signal is increasingly likely to be
tested by an absolute calibration before any satellite. No status change.

**D304 (deep loop 3, gap 9/2: can heterotic moduli space host the tail at weak coupling at all?)** Read: Cicoli et al., "Quintessence and the
swampland: the parametrically controlled regime of moduli space" (Fortsch. Phys. 2022). Result: in tree-level type II and heterotic supergravity,
no slow-roll region exists in any parametrically controlled (weak-coupling, large-volume) regime — heterotic: V = e^{K₀}|W_cs|²/(2s), runaway in
dilaton and volume with ε = ε_s + ε_κ = 1 + 3 = 4; type IIB ε ≥ 3; IIA ε ≈ 4. Slow roll needs corrections that break the tree-level Kähler
structure; their sequel finds viable quintessence "requires non-supersymmetric vacua". No fifth-force analysis. Reading for the Twist: (1) this
is the published version of our D204/D209 dead end — the controlled heterotic region does not give a w ≈ −0.9 tail; the Twist's tail (slope
√(2/3), ε ≈ 1/3 asymptotically) comes from the cliff-modified no-scale sector, i.e. from exactly the kind of non-tree-level structure they say is
required, and it sits outside the controlled regime (g_s ≥ 3 today). (2) It reinforces gap 9: a controlled string home for any DESI-like thawing
tail is an open problem in the field, not specific to the Twist. Gap 2/9 status unchanged; framing for v6 §7: "no controlled string regime is
known for this tail (consistent with Cicoli et al. 2022)".

**D305 (deep loop 4, gap 1/15: D285–D286 against the published supergravity one-loop treatment).** Read: Ellis, Gherghetta, Kaneta, Ke & Olive,
"Radiative corrections in supergravity models of inflation" (arXiv:2603.02389, 2026). They use the Gaillard–Jain one-loop Kähler correction
K⁽¹⁾ = −(1/32π²)Tr[M̄M(ln(M̄M/μ²) − 1)] (its ln μ² part in SUGRA), work in Minkowski space dropping curvature terms (suppressed by H²/M_P²), and
note that mass-splitting terms are missed when SUSY breaking is large. Results: Cecotti / KYY Starobinsky — corrections negligible (n_s ≃ 0.965,
r ≃ 0.0035 unchanged); no-scale Wess–Zumino — corrections large and coupling-dependent (n_s 0.934 or 0.964, r 0.004), viable only with tuned
tree couplings; scheme: "an extra constant … due to the different regularization schemes"; SUGRA is non-renormalisable, so counterterms are
needed; one loop is unreliable for φ ≳ 6. Comparison with D285–D286: (1) our dominant term, 4 m_F² δ with δ ≈ 2.4H², is an F-term (inflaton
F_S-induced) mass splitting — the "mass-splitting terms" they flag as missed by the Kähler-only route; it is not a curvature term, so their
H²/M_P² argument does not remove it. (2) Their finding that loop effects are negligible or large depending on which fields couple to the
inflaton matches ours (χ at weight 3/2: negligible, D287; a field inside the log: ∝ 1/x, TWIST-C form, D285). (3) Scheme dependence of the
constant confirms D286's statement that b is a renormalised, scheme-dependent parameter. Verdict: D285–D286 are consistent with the published
treatment and go beyond it on the splitting term; still estimate-level (no gravitational loops). Gap 1/15 unchanged.

**D306 (deep loop 5, gap 2: Yukawas) — the shield also forbids worldsheet-instanton Yukawa hierarchies.** Read: Parameswaran, Ramos-Sánchez &
Zavala, "On moduli stabilisation and de Sitter vacua in MSSM heterotic orbifolds" (arXiv:1009.3931). Rule (their Eq. 3.12, §3.3.1): twisted-
field Yukawas are O(1) when all three fields sit at the same fixed point; otherwise they are exponentially suppressed in the Kähler moduli,
∝ e^{−cT} (worldsheet instantons, e.g. e^{−2πT/3} in Z₆-II); bulk (untwisted) couplings are O(1); even constant holomorphic couplings get T-dependence
from the Kähler normalisation (their Eq. 3.16 — our weight condition). Consequence for a ROLLING T (computed): a Yukawa ∝ e^{−2πT/3} at x = 89 has
d ln y/d ln x ≈ −186, i.e. d ln y/dt ≈ 4.7×10⁻⁹/yr today — ~10⁸ above clock limits on mass ratios (~10⁻¹⁷/yr). So in any heterotic home for
the Twist, every Standard Model Yukawa must be untwisted or same-fixed-point (no instanton-generated hierarchy), with the D293 weight condition
on top. Fermion-mass hierarchies would then need another origin (e.g. Froggatt–Nielsen with x-independent flavon vevs). Gap 2: requirement
sharpened; status HIGH unchanged.

**D307 (deep loop 6, gaps 5/1: newest DESI) — survey complete; bispectrum weakens evolving-DE evidence.** (a) DESI finished its five-year
survey (>47 million galaxies and quasars; OSU news, 16 Apr 2026); first full-survey dark-energy results expected in 2027, observations continue
to 2028 — the WATCH-PURE-DR3 / WA-CEILING / GROWTH test date stands. (b) Forero-Sánchez et al. (DESI, arXiv:2606.23936, Jun 2026): adding the DR1
LRG bispectrum to full shape + DR2 BAO raises σ8, S8 by ~1.1–1.2σ (errors −26–28%); w0waCDM: DESI-only within 1σ of ΛCDM; DESI + CMB 2.8σ;
+ DES-Dovekie 3.1σ; DESI + DES-Dovekie 1.6σ — "the bispectrum consistently weakens evidence for time-varying dark energy". For the Twist: in line
with D262/D290 (no current evidence); the slightly higher σ8 from the bispectrum moves away from the Twist's −1.5% σ8 suppression, but within
errors. Gap 5 unchanged; gap 1 unchanged (no new n_s).

**D308 (deep loop 7, gap 2: can Froggatt–Nielsen give the fermion hierarchy without x-dependence?) — yes in principle, via the anomalous-U(1)
FI term, if the dilaton is fixed.** Read: Higaki, Kawamura, Kobayashi & Nakano (hep-ph/0311315): in heterotic models ξ = δ_GS ⟨K_S⟩ M_P², set
by the dilaton (value and Kähler form), with "the ratio of the FI term to the Planck mass squared … an origin of coupling hierarchies"
(Froggatt–Nielsen). Analysis for the Twist: the canonical flavon vev solves K_φφ̄|φ|² ≈ ξ, so ε = φ_can/M_P = (δ_GS K_S)^{1/2} depends on the
dilaton only — x-independent if the dilaton is fixed independently of T (the same BGW condition as D302). Holomorphic Yukawas
y_ij ∝ (φ/M)^{q_ij} are then x-independent after normalisation if each term's weights sum to 3 including flavon insertions, which forces the
flavon's modular weight p_φ = 0 and leaves the D293 conditions on the quark/lepton/Higgs weights. So the FN route replaces D306's forbidden
worldsheet-instanton hierarchies at no extra cost — the obstruction stays the D302 one (universal δ_GS with extra matter + fixed dilaton + weak
coupling today). Caveat: a fixed dilaton with K_S = 0 would make ξ vanish (their stabilisation point), so the FI term must come from K_S ≠ 0 at the
minimum — model-dependent. Gap 2 unchanged (HIGH); the fermion hierarchy is not an independent obstruction.

**D309 (deep loop 8, gap 2/9: is there a weakly coupled heterotic regime with a fixed dilaton while a volume modulus rolls?) — no; this is
Witten's 1996 strong-coupling relation.** Read: Witten, "Strong coupling expansion of Calabi–Yau compactification" (hep-th/9602070).
Weakly coupled heterotic: G_N = e^{2φ}α′⁴/(64πV), α_GUT = e^{2φ}α′³/(16πV), so G_N = α_GUT α′/4; weak coupling e^{2φ} ≤ 1 needs
V ≤ α′³/α_GUT. At fixed α_GUT (what the shield needs: x-independent gauge couplings), e^{2φ} = 16π α_GUT V/α′³ grows linearly with the
compactification volume — so any rolling of a volume-type modulus toward large V drives the 10d coupling strong. For the Twist, V ∝ x³ in
string units (D209: g_s ∝ x^{3/2}), and x grows from 1.3×10⁻⁴ to 89 (factor 7×10⁵, i.e. 3×10¹⁷ in V): weak coupling today would require
e^{2φ} ~ 10⁻¹⁷ during inflation — unphysical with α_GUT ~ 1/25 and string-scale V. The strong-coupling continuation is heterotic M-theory
(G_N = κ²/(16π²Vρ), α_GUT = (4πκ²)^{2/3}/(2V)), where the interval ρ — not the CY volume — can grow at fixed α_GUT; our D205–D208 found the
matter-neutral direction there is rung 4 and moves the SM coupling (d ln α/dφ ≈ 0.71). Verdict: the D302 obstruction is a theorem-level
relation of weakly coupled heterotic strings, not a model-building gap; the Twist's x-direction cannot be a heterotic volume modulus with a
fixed gauge coupling. Remaining logical options for a string home: (i) a non-volume modulus with rung-3 geometry (e.g. a complex-structure or
blow-up modulus with K = −3 ln), which D210–D211 found leaks at one loop in IIB; (ii) M-theory with a non-volume direction. Gap 9 unchanged
(MEDIUM), but its framing is sharper: "a volume modulus is excluded by α_GUT ∝ g_s²/V at fixed coupling".

**D310 (deep loop 9, gaps 9/5: α = 1 in the 2026 attractor-quintessence literature).** Read: Borys, Masias & Scalisi, "Quintessential
α-attractors fit DESI" (arXiv:2606.02701). Model: T-model V = V₁(tanh(φ/√(6α)) − c)², the "knee" between plateau and tail. Mapping the DESI
axion-like benchmark onto it gives allowed ranges — c = 0: 0.06 < α < 1.06 (Pantheon+), 0.02–2.01 (Union3), 0.04–5.80 (DES Y5); c = 1:
0.04–0.73, 0.02–1.39, 0.03–4.00 — "the preferred values are generically of order unity". So α = 1 (the Twist) is allowed with c = 0 on all
three SN sets and excluded only for c = 1 with Pantheon+. String side: they cite the seven-disk M-theory-on-T⁷ origin, α = n/3, and type IIB CY flux
compactifications with 3α = 1, 2, 3 — the same discrete "rungs" the Twist uses (3α = 3 ↔ α = 1). No fifth-force or n_s discussion.
Reading: (1) independent support that an α = 1 tail is in the DESI-allowed window (consistent with our PURE-TWIST fits and D224); (2) the
seven-disk/T⁷ picture gives α = 1 as three unit disks — in that picture T is not a single volume modulus but a combination of disk moduli, which
is a candidate "non-volume α = 1 direction" for gap 9 (to examine: whether matter can be neutral under it, cf. D309). Gap 5 unchanged; gap 9:
one concrete lead (seven-disk M-theory) to check next.

**D311 (deep loop 10, gap 9: the seven-disk M-theory lead from D310).** Read: Gunaydin, Kallosh, Linde & Yamada, "M-theory cosmology, octonions,
error correcting codes" (arXiv:2008.01494). M-theory on a twisted T⁷/G₂ has seven moduli T^i multiplying the seven associative 3-forms
(Φ = t_i φ^i); the G₂ volume is a product, V = Π(2T^i). Kähler K = −Σ log(T^i + T̄^i). The α values 3α = 7…1 come from identifying moduli
into blocks; e.g. the (4,3) split T¹=T⁴=T⁵=T⁷ ≡ T₍₁₎, T²=T³=T⁶ ≡ T₍₂₎ gives K = −4 log(T₍₁₎+T̄₍₁₎) − 3 log(T₍₂₎+T̄₍₂₎) — so a 3α = 3 (α = 1)
direction is a three-modulus block T₍₂₎ with the other block T₍₁₎ held fixed. Reading for gap 9: (1) yes — in this picture the Twist's α = 1
field is not the overall volume but a sub-block (with V ∝ T₍₁₎⁴T₍₂₎³, rolling T₍₂₎ at fixed T₍₁₎ still changes the G₂ volume as T₍₂₎³);
(2) matter/gauge localisation is not discussed — in M-theory on G₂, non-abelian gauge fields and chiral matter live on codimension-4/7
singularities, and their gauge couplings scale with the volume of the associative 3-cycle they wrap; matter is neutral under T₍₂₎ only if the SM
3-cycle's volume involves T₍₁₎ alone. That is a concrete, checkable condition (SM on a 3-cycle calibrated by T₍₁₎-type forms), not obviously
excluded — the first non-excluded lead for gap 9. Caveats: twisted T⁷ is a toy; real G₂ compactifications with chiral matter need
singularities; the 4d Planck mass scales with V, so a rolling block changes M_P/M_11 (must be checked for varying-G). Status: gap 9 MEDIUM,
with an open lead (seven-disk sub-block with the SM on a complementary 3-cycle). Worth a follow-up by an M-theory expert (question 12 for the
open-problem doc).

**D312 (deep loop 11, gaps 2/9: does M-theory on G₂ give the shield structure?) — it supplies most of it naturally; first plausible string
home for the shield.** Read: Acharya, Bobkov, Kane, Kumar & Shao (hep-th/0701034): each gauge group lives on a 3-cycle with
f_k = Σ_i N^k_i z_i (integer homology coefficients; some N^k_i can be zero), K = −3 ln(4π^{1/3}V_X), V_X = Π s_i^{a_i}, Σa_i = 7/3,
m_p = M₁₁V_X^{1/2}/√π. Acharya & Bobkov, "Kähler independence of the G₂-MSSM" (JHEP 09 (2010) 001): visible matter at conical
singularities has K̃ = κ(s_i)/V_X (κ homogeneous of degree 0), forced by locality; soft terms are insensitive to κ's form.
Consequences for the Twist (analysis): (1) GAUGE COUPLINGS: 1/g²_SM = Σ N^SM_i s_i — if the SM 3-cycle has N^SM_i = 0 on the rolling block
(the Twist's α = 1 three-modulus block, D311), the SM gauge couplings are exactly independent of it, with no Green–Schwarz/universal-dilaton
obstruction (unlike heterotic, D302/D309). (2) YUKAWAS: physical Y = e^{K/2}Y₀/(K̃K̃K̃)^{1/2} = Y₀ κ^{−3/2} — the overall V_X cancels exactly
(locality); what remains is κ(s_i), a degree-0 function of moduli RATIOS; if locality makes κ depend only on moduli near the SM singularity (the
fixed block), Yukawas are x-independent too. (3) Still sliding: m_3/2 = e^{K/2}|W| ∝ V_X^{−3/2} and hence gravity-mediated soft masses, and
M₁₁/m_p ∝ V_X^{−1/2} — the SUSY-breaking scale needs the D292 mechanism (a W ∝ block^{3/2}-type term plus weight-3-type uplift) transplanted
to G₂, not yet done; M₁₁ affects only heavy states. Status: gap 2 HIGH → HIGH with a concrete candidate; gap 9 MEDIUM with the G₂-MSSM-type
"SM on a 3-cycle away from the rolling block" as the leading lead. Not shown: that the block has the plateau→cliff→tail potential; that the fixed
block can be stabilised; chirality/singularity realism. Recorded as open-problem question 12 for M-theory experts.

**D313 (deep loop 12, gap 9: is there published G₂/M-theory quintessence to build on?) — none found; the D312 route would be new.**
Searched for M-theory/G₂ moduli quintessence; read Bento, Chakraborty, Parameswaran & Zavala, "Dark energy in string theory" (arXiv:2005.10168;
IIA/IIB/heterotic 4d SUGRA, no G₂) and Agrawal & Obied (JHEP 06 (2019) 103; EFT only). Bento et al.: non-perturbative runaways give
double-exponential tails too steep for slow roll; perturbative power-law runaways K = −n ln(T+T̄), W ∝ T^p give ε_V = (n − 2p)²/n, and in the
bulk/fibre case V > 0 is never compatible with ε_V < 1 — only a "local modulus" case (p = n) works. Check against the Twist: n = 3 and the tail
ε_V = 1/3 correspond to (3 − 2p)² = 1, i.e. p = 1 or 2; the Twist evades their no-go because V > 0 comes from the stabiliser's F_S
(W = √3 m S T), not from a pure-T superpotential — a structural difference worth stating in v6. On matter: "any scalar with mass below
~meV must have weaker than Planckian couplings to the Standard Model … sequestering could help, but no explicit construction exists" — the gap
we are addressing. Verdict: no published G₂ quintessence; D312's "SM on a 3-cycle away from the rolling block" is, as far as found, a new
proposal. Gap 9 unchanged (MEDIUM, with a novel lead).

**D314 (deep loop 13, gap 2/9: do D292 and the cliff transplant to G₂?) — analysis.** With K = −3 ln V_X, V_X = Π s_i^{a_i}, Σa_i = 7/3
(Acharya et al.), split the moduli into the rolling α = 1 block (Σa = 1, collective modulus T₂) and a fixed block (Σa = 4/3, T₁):
K = −3 ln(T₂ + T̄₂) − 4 ln(T₁ + T̄₁) + const, as in the (4,3) seven-disk split (D311). (1) SUSY breaking: m_3/2 = e^{K/2}|W| ∝ (2x)^{−3/2} ×
(fixed-block constant) — the same x-dependence as the single-field Twist, so the D292 construction transplants unchanged: W ⊃ w T₂^{3/2} + μ²X
with K ⊃ |X|²(T₂ + T̄₂)^{−3}(1 + c(…)²) gives V = μ⁴ − 3w²/8 at every x, an x-independent m_3/2, F_X and angle mass (4c − 2)m_3/2² (the fixed
block only rescales w and μ by constants). In G₂ the weight-3 metric for X must come from X living at a singularity whose local metric scales as
T₂^{−3} — a model-building requirement, not derived. (2) Cliff: a hidden gaugino condensate on a 3-cycle with f = N₁z₁ + N₂z₂ gives
W ∝ e^{−2π(N₁z₁ + N₂z₂)/N}; the Twist's cliff exponent e^{−πT/4} needs 2πN₂/N = π/4, i.e. N = 8N₂ — the SU(8)-type condensate of the
alternative construction, now on a 3-cycle with N₂ = 1. Same drawback as before (D136): its gauge coupling 1/g² = Re f ∝ s₂ is strong on the
plateau (small x), so the cliff formula is used outside control there; the TWIST-K Kähler-metric version of the cliff would need a G₂ origin
for the e^{−πu/8} metric factor (membrane instanton corrections to K are the natural candidate, not computed). (3) The SM 3-cycle must have
N₂^SM = 0 (D312) while the hidden cliff cycle has N₂ = 1 — compatible (different cycles). Verdict: the G₂ lead survives this check: SUSY breaking
transplants exactly; the cliff has the same control problem it always had. Gap 9 MEDIUM, lead intact.

**D315 (deep loop 14, gap 9: can one G₂ block be fixed while the other rolls?)** Read: Acharya, Bobkov, Kane, Kumar & Vaman, "An M theory
solution to the hierarchy problem" (hep-th/0606262). Two hidden condensates W = A₁e^{ib₁f₁} + A₂e^{ib₂f₂}, f_k = Σ N^k_i z_i; with N¹ = N² the
SUSY extremum has N_i s_i/a_i = ν for every i, ν = −3(α − 1)/(2(αb₁ − b₂)) — "fixes all moduli for a manifold with any number of moduli" (a
saddle; the SUSY-breaking minima are in the companion paper). Moduli with N^k_i = 0 in every condensate are not discussed; from their equations
such a modulus does not enter W and is not fixed by this mechanism. Reading for the Twist (analysis): this is the structure the G₂ lead needs —
(a) stabilise the fixed block T₁ with two condensates on cycles built from T₁ only (N^k_2 = 0), via the ABKKV mechanism; (b) leave the
rolling block T₂ out of those condensates, so it is flat at that level and gets its potential only from the Twist sector (stabiliser S,
cliff condensate on an N₂ = 1 cycle, D314); (c) the SM on a T₁-only cycle (D312). Each of (a)–(c) uses only ingredients of the published
G₂-MSSM framework; the novelty is the block split. Caveat: K mixes the blocks through V_X (K = −3 ln V_X), so the T₁ minimum's location and
depth depend on T₂ through e^K — V_T₁-sector ∝ e^{K} ∝ (2x)^{−3}: the T₁-stabilising potential scales with x like the gravitino mass, so its
minimum is x-independent in position (the e^K prefactor factors out of the T₁ F-terms) but its energy slides — it must be a SUSY (F = 0,
W = 0) minimum or cancelled like D292, otherwise it adds an x^{−3} term to the tail. Verdict: the G₂ lead survives a third check, with one new
condition: the fixed-block stabilisation must be supersymmetric with W = 0 there (or tuned as in D292). Gap 9 MEDIUM, lead intact; the
open-problem list for an M-theory expert now has a concrete construction to check (D311–D315).

**D316 (deep loop 15) — the G₂ lead written up.** papers/twist_v5/G2_HOME_PROPOSAL.md collects D309–D315 into one self-contained proposal
(why not heterotic; the block split; SM on a block-free 3-cycle; ABKKV stabilisation of the fixed block with W = 0; D292 SUSY breaking; cliff
condensate; what is not shown) and states question 12 for M-theory experts. v6 corrections item 14 adds it to the exploratory note.

**D317 (deep loop 16, gap 13: the conditional 100–500 TeV gravity-portal DM vs current decaying-DM limits) — squeezed (estimate).**
LHAASO, "Constraints on heavy decaying dark matter from 570 days" (arXiv:2210.15989; 10⁵–10⁹ GeV scanned; limits shown in plots, e.g.
τ(bb̄) ≈ 6.3×10²⁸ s used at 10⁷ GeV; IceCube stronger for νν); 2025 LHAASO update reported tighter limits (news release; numbers not
extracted). Scaling D242's anchor (τ ≈ 10²⁴ s at 10⁶ GeV for an O(1) non-minimal gravity-portal coupling ξ, τ ∝ m⁻⁵ ξ⁻²):
m = 10⁵ GeV → τ ≈ 10²⁹ s (at the limit); 2×10⁵ → 3×10²⁷ s (needs ξ ≲ 0.6); 5×10⁵ → 3×10²⁵ s (needs ξ ≲ 0.06) against τ ≳ 10²⁸ s for hadronic/
photon channels. Verdict: for ξ ~ 1 only the bottom of the window (~100 TeV) survives; the rest needs a suppressed gravity-portal coupling
(ξ ≲ 0.06 at 500 TeV) — or minimal coupling, where the decay must go through higher operators. Status: gap 13 LOW → LOW–MEDIUM (the
conditional DM is under pressure, still not a prediction); a decaying-DM signal at ~100 TeV (IceCube/LHAASO) remains the target named in D242.

**D318 (deep loop 17, gap 13 follow-up to D317: does the DM production work at ~100 TeV, and is the gravity-portal coupling ξ natural?) —
production yes by construction; ξ is not predicted (literature + argument).**
(1) Production: D112's bremsstrahlung yield (graviton emission in χ̃ decays) and the freeze-in yield do not depend on m_DM (m_DM ≪ T_RH, m_χ),
so the relic density fixes m_DM; 100 TeV is inside D112's 100–500 TeV band, at the end corresponding to the larger yield (heat share near
0.8%). Nothing new needs computing; the low end of the band is the one D317 leaves open.
(2) ξ: Catà, Ibarra & Ingenhütt (arXiv:1603.03696, scalar case; arXiv:1611.00725, fermions) write the leading term as −ξ R F(DM, SM). It is the
only decay source when a flat-space symmetry forbids the renormalisable coupling (for a singlet fermion, the Yukawa ψ̄ L̃ H, which would make it
decay at once). Hence: if that symmetry is gauged (e.g. a discrete gauge Z₂), gravity respects it too, so ξ = 0 and the DM is stable, giving no
signal. If it is global, quantum gravity is expected to break it, but by an unknown amount (typically exponentially small, wormhole/instanton
size). So ξ ~ O(1) is not "natural" in any sense that fixes it. For the scalar case, the same papers need ξ ≲ 10⁻¹⁶ at 300 TeV, so a scalar
candidate would be excluded unless finely suppressed; the Twist's choice of a fermion (D105) is what keeps an O(1) ξ in play at all.
Verdict: the DM's existence and mass (~100 TeV end preferred by D317) stand as conditional; the decaying-DM signal is OPTIONAL, not a prediction.
It appears only if DM stability rests on a global symmetry with gravity-strength breaking. Gap 13 stays LOW–MEDIUM; the wording "signal worth
flagging" (D242) is narrowed to "possible signal if stability is not gauged".

**D319 (deep loop 18, gap 8: does the G₂ picture (D311–D316) say anything about n beyond D283?) — a named origin, not a derivation
(literature + argument).**
Acharya, Bobkov, Kane, Kumar & Vaman (arXiv:hep-th/0701034, §2–3): hidden gauge kinetic functions f_k = Σᵢ N_iᵏ z_i, with integers N_iᵏ (the
3-cycle), and condensate exponents b_k = 2π/c_k. At the SUSY two-condensate vacuum the prefactor ratio fixes a combination of the moduli:
A₂/A₁ = (1/α) exp[−(b₁N¹ − b₂N²)·s], so the stabilised hidden volumes are set by the rank data (c₁, c₂, N's) times ln(A₁/A₂) (plus the O(1)
constant α from their linear system).
Applied to the Twist's G₂ lead: the cliff condensate sits on a cycle with N₂ = 1 and some N₁ ≥ 1 (D315), so its depth is
e^{−2π N₁·Re T₁/c_cliff}, with Re T₁ fixed by the ABKKV pair on T₁-only cycles. Hence 2n ≈ 249 (D255: n = π/α_h, α_h⁻¹ ≈ 39.8) becomes
"integers (ranks, wrapping numbers) × a logarithm of one-loop prefactor ratios". The prefactors are threshold corrections that are computable
in principle on a given G₂ manifold (Friedmann–Witten type). Today's Λ ∝ e^{−2n} needs n to ±0.4 (a factor ~2 in Λ), i.e. α_h⁻¹ to ~0.3%,
so the prefactor logarithm would need ~0.1 precision. No such computation exists for any explicit G₂ manifold.
Verdict: one step beyond D283. In the G₂ setting n is no longer a free real coupling but a discrete-data-plus-threshold quantity, "derivable in
principle". This is not a prediction: the integer choices are free, and the anthropic/landscape reading of D283 remains. Gap 8 unchanged
(n chosen). Add to question 12 of the G₂ proposal: "Can the one-loop prefactors fix Re T₁ to the per-mille level needed for n?"

**D320 (deep loop 19, gap 7: isocurvature under the alternative coupling reading) — argument, plus a locked run started.**
Argument: the alternative reading (D268/D297) changes only the source (μ₅ ∝ y′ − c p′ y instead of y′); the field histories y(t), x(t), σ(t) are
identical. δσ/σ₀ (from H and f) does not depend on the reading. What can change is the yield's sensitivity to σ₀: Y_alt also depends on the
displacement y, not only the speed y′. D277 found the canonical sensitivity, 3.70, is already non-linear, so it cannot be assumed to carry over.
It is now measured: PREREG_D320_ALT_ISOCURV (locked and pushed before running) reruns the D268 one-pass script with σ₀ × 1.05. It validates
against D277's canonical 1.306×10⁻¹⁰ and scores |S_alt| ≤ 5, with margin 5.1/S_alt at f = 0.1 M_P. Limitation (stated in the lock): the run
is at m_σ = 5.8×10¹⁰, not at the alternative fit point 3.0×10¹⁰. Running in the cloud (~2 h); result to be appended as D320b.
Gap 7 status until then: passes, marginal (canonical); alternative reading pending.

**D321 (pp, 06:00 CT, G₂ follow-up: do known compact G₂ manifolds have rigid 3-cycles of the kind D313–D315 use?) — partly; the
"SM cycle" type is not among them (literature).**
- Corti, Haskins, Nordström & Pacini (arXiv:1207.4470, Duke 2015): twisted-connected-sum (TCS) G₂ manifolds contain finitely many rigid
  associatives ≅ S¹ × S², one for each rigid (−1,−1) rational curve in a semi-Fano building block, for long necks (their Prop. 5.15). These
  were the first proven rigid compact associatives. Being S¹ × C with C in one building block, they are localised in one half of the TCS.
  The text read does not show which block hosts them in each example.
- Associative submanifolds in TCS G₂ manifolds (arXiv:2209.00156): rigid associatives glued across the neck from S¹ × curves in both halves
  (Thm 5.3), giving S³, RP³ and RP³#RP³ examples. These meet both halves.
Relevance: (i) A smooth rigid associative gives an M2-brane instanton term in W ∝ exp(−2π ∫_C Φ) = exp(−2π Σ N_i T_i), set by its class. That
is an alternative to the condensate cliff of D315, but it has the same control caveat at small cycle volume. Whether it is any better is not
known until the cliff's location in Re T₂ is mapped onto the cycle volume (not done). (ii) The SM in M-theory needs ADE singularities along a
3-cycle plus conical points for chiral matter. Smooth TCS manifolds have neither. The N₂ = 0 SM cycle of D313 therefore needs a singular G₂
(Joyce orbifold resolutions kept partly singular, or the Acharya-type local models). No compact example with that cycle is known from this search.
(iii) The "one cycle per half" localisation is the feature the block split needs; TCS provides it for instanton cycles. The (4,3) block split of D311
was found on a toroidal orbifold, so whether TCS realises the same Kähler split is open.
Verdict: question 12 is sharpened, not answered. TCS gives localised rigid instanton cycles (a possible cliff source); the SM cycle needs singular G₂.
G₂ lead status unchanged (a proposal).

**D322 (deep loop 20, G₂ follow-up: are G₂ threshold corrections computable, for D319's n and for the shield?) — yes, topologically
(literature; formula itself not extracted).**
Friedmann & Witten, "Unification scale, proton decay, and manifolds of G₂ holonomy" (arXiv:hep-th/0211269): the one-loop threshold correction
for a gauge group on a 3-manifold Q of ADE singularities is given by the Ray–Singer analytic torsion of Q. This is a topological invariant,
"computed explicitly based on topological assumptions, without needing to know the detailed form of the G₂ metric", and fully explicit for
lens spaces Q = S³/Z_q (their §3 and appendices; not read in full here).
Consequences:
(1) D319 (n): the prefactors A_k entering n are of this type. If the hidden ABKKV and cliff groups sit on lens-space cycles, ln(A₁/A₂) is an
explicit function of the integers (q, ranks, Wilson lines). n then becomes fully discrete data: a finite list of possible values, not a
continuous fit. Whether any choice gives α_h⁻¹ ≈ 39.8 to ~0.3% is a concrete, finite computation (not done; it needs their lens-space formula).
(2) Shield: the threshold for the SM on its cycle Q_SM is metric-independent at one loop. So moduli, including x, cannot enter the SM gauge
coupling through thresholds at this order. That supports D313's "SM coupling x-independent" beyond tree level, given N₂ = 0 for Q_SM.
(Caveat: the Friedmann–Witten setting expresses the threshold together with the volume V_Q, whose tree-level part is the N₂ = 0 statement.)
Verdict: positive for the G₂ lead. Question 12 gains a computable sub-task: scan lens-space hidden cycles for n. Gap 8 remains "chosen" until
that scan is done. Not a prediction.

**D323 (referee review, 06:10 CT) — CORRECTION to D312/D322 and the G₂ proposal: the shield fails at one loop (estimate).** Details in
papers/REFEREE_REPORT_2026-11-14_overnight.md (M1). M₁₁/M_P ∝ V_X^{−1/2} slides with x (exponent −1/2), while the soft scale is x-independent
in Planck units (D292). Running from the matching scale gives d ln α_em/d ln x ≈ (12/2π)(1/2)/137 ≈ 7×10⁻³, the D289 order (~10⁵–10⁶ over the
clock bound). Kaplunovsky–Louis: with Z = κ/V_X the volume terms leave (ΣT_r/3 − 3T_G)K = −7K for SU(3). D322's "no x-dependence from
thresholds at one loop" is withdrawn (Ray–Singer is the local part only). The proposal's "M₁₁/M_P affects only heavy states" is withdrawn.
Also: the non-diagonal rolling-block moduli are unstabilised (M2), and W = 0 for the fixed block is a racetrack tuning (M3).
Status: gap 2 back to HIGH with no candidate mechanism; gap 9 stays "proposal". The tree-level parts (N₂ = 0 coupling, Yukawa volume
cancellation) stand.

**D324 ("fix test", 06:15 CT): can the G₂ one-loop problem (D323) be fixed? Five fixes tested; none works (algebra + earlier results).**
First, M1 is confirmed by the proper Kaplunovsky–Louis formula: 16π²/g_a² ⊃ c_a K − 2ΣT_a(r) ln Z_r, with c_a = ΣT − T_G. With K ⊃ −3 ln t₂
and local Z = κ/V_X ⊃ −ln t₂, the ln t₂ coefficient is −3c_a + 2ΣT = **−b_a**. This is exactly the matching-scale shift M₁₁ ∝ t₂^{−1/2}.
d(1/α_a)/d ln x = −b_a/4π = −0.53 (U(1)), −0.08 (SU(2)), +0.24 (SU(3)); α_em: −0.955, d ln α_em/d ln x ≈ 7.0×10⁻³. (The referee report's
"−7K for SU(3)" was an arithmetic slip; the correct coefficient is −b_a ln t₂. The conclusion is unchanged.)
Fixes tested:
(a) T₂-dependent matter metrics (modular weights under T₂): this is D293's linear system. With an x-independent μ-term there is no solution.
FAIL.
(b) A Green–Schwarz-type mixing of the fixed block with ln t₂ (K ⊃ −4 ln(T₁+T̄₁ − δ ln(T₂+T̄₂))): one δ shifts all f_a in proportion to their
N-vectors, but the cancellation needs shifts ∝ b_a = (33/5, 1, −3), which have mixed signs. Each SM factor would need its own tuned δ.
FAIL (tuning, not a mechanism).
(c) Extra matter so that b_em = 0 between m_soft and M₁₁: added matter only raises b, and b₁ > 0 already. FAIL.
(d) Let every SM scale (soft masses, v, Λ_QCD) track M₁₁: dimensionless SM ratios are then fixed, but all masses ∝ M_P x^{−1/2}. That is a
universal matter coupling β = (1/2)/√(3/2) = 0.41 against the Cassini bound ~3×10⁻³. FAIL (this is the type IIB β_m problem).
(e) Roll along a direction at fixed V_X: then e^K is constant along it, and the Twist's x^{−3} plateau structure (rung 3) is lost. FAIL.
M2 test (non-diagonal moduli of the rolling block): stabilising them without T₂ needs cycles with Σ N_i a_i = 0. Those have mixed-sign N
and zero volume on the diagonal, which is uncontrolled. No clean fix. M3: kept as a stated tuning.
Verdict: a no-go at the estimate level. If the rolling field's x^{−3} in e^K comes from the overall volume, then at one loop the SM couplings
move as d(1/α_a)/d ln x = −b_a/4π, and no matter content, weight assignment or single counterterm removes it. The obstruction is generic
to any compactification where the UV matching scale is set by the same volume (distance-conjecture form). The shield (gap 2) therefore needs
either a tuned per-group cancellation to ~10⁻⁶ (unnatural), or a rolling field that is not a volume. Gap 2: HIGH, sharpened into a no-go
statement. G₂ proposal: downgraded to "tree-level only; fails at one loop".

**D325 ("fix test" continued, 06:30 CT): a sixth fix that lifts D293's μ obstruction, then fails on inflation (locked, PREREG_D325_GS_ALPHA).**
(1) Algebra (gm_mu_fix_d325.py): a Giudice–Masiero μ-term, K ⊃ λ(T+T̄)^{−q}H_uH_d, gives μ_phys ∝ m_3/2(2x)^{−q+(p_Hu+p_Hd)/2}. With m_3/2
x-independent (D292), q = (p_Hu+p_Hd)/2 removes the holomorphic μ condition. D293's remaining system then has a two-parameter family, always with
p_Hu + p_Hd = 12 (so q = 6) and a universal Green–Schwarz term δ = −27. The smallest weights are max|p| = 6 (p_Q −11/3, p_U = p_D = 2/3, p_L 3,
p_E −6, p_Hu = p_Hd = 6). In EFT this would cancel the one-loop drift for all three SM couplings with discrete choices, not a 10⁻⁶ tuning.
(2) Side effect: the GS term needs a dilaton with K ⊃ −ln ℓ, ℓ = S+S̄ − δ′ln(T+T̄), δ′ = 27/16π² = 0.171, and ℓ = 2/g² = 3.98 fixed by
α_GUT = 1/25. With ℓ held by the heavy dilaton, K_T K^{TT̄} K_T̄ = 3 − δ′/ℓ exactly, i.e. the no-scale α shifts to 1 ∓ δ′/(3ℓ) = 1 ∓ 0.0143.
The Twist's plateau needs α = 1 exactly (rung 3).
(3) Locked test (gs_alpha_ns_d325.py; one logged crash fix, D1): baseline n_s 0.9650, r 0.0036. α = 0.98568 → NO 57-e-fold solution (the
plateau tilts the wrong way; N = −5.5). α = 1.01432 → n_s 0.9844 (Δn_s +0.0195), r 0.0150. Rule |Δn_s| ≤ 0.004 for both signs: **FAILS for
both. The GS fix spoils inflation.** To pass, |α − 1| ≲ 0.003 would need ℓ ≳ 19, i.e. α_GUT ≈ 1/120, which is inconsistent with the SM's
f_SM = S.
Verdict: six fixes tested, none works. Remaining options: per-group tuning (~10⁻⁶); a rolling field that is not a volume; or separating
inflation from the dark-energy tail (only the tail needs the shield). Gap 2: HIGH, no-go now includes the GS route.

**D326 (deep loop 21, gap 2 option "a rolling field that is not a volume": IIB complex-structure U with twisted-moduli GS) — no clean escape
(literature + argument).** Lens-space n scan skipped: the G₂ home was downgraded (D323–D324), so n-in-G₂ is moot.
Idea: the rolling field is the diagonal U of three tori, K ⊃ −3 ln(U+Ū). M_s/M_P does not depend on U, so there is no matching-scale slide.
D3 untwisted matter has Z_i ∝ (U_i+Ū_i)^{−1}, so Yukawas e^{K/2}/√(Z₁Z₂Z₃) are U-independent automatically (μ via Giudice–Masiero, as in D325).
The Kaplunovsky–Louis term −b_a ln u remains. In IIB, sigma-model anomalies can be cancelled by twisted closed-string moduli M_k with
non-universal couplings (Ibáñez–Rabadán–Uranga). Since K ⊃ ½(M+M̄ − δ ln(U+Ū))² is quadratic, the α shift would be only second order
(δ²/3 at the D-flat point), which avoids D325's inflation failure.
Literature check (Lalak, Lavignac & Nilles, "Target-space duality in heterotic and type I effective Lagrangians", hep-th/9912206):
(i) In the Z₃/Z₇ type I orientifolds the one-loop couplings keep a non-harmonic −(b′_a/16π²) ln(T+T̄) term. The GS mechanism alone cannot cancel
both sigma-gauge and sigma-gravitational anomalies ("troublesome" term; duality is "an accidental, tree-level symmetry"). So the residual
drift is literally present in the known models.
(ii) Moduli-dependent thresholds come from N=2 subsectors, b^{N=2}_{a,i} of the invariant planes. An untwisted U modulus exists only for a
plane on which some twist acts as −1, which is exactly an N=2 sector. U-moduli therefore come with b^{N=2} terms generically.
Verdict: the non-volume route has one conditional loophole: a rolling U-plane whose N=2 sector contains no SM-charged states (b^{N=2}_a = 0
for SU(3), SU(2), U(1)_Y), together with complete twisted-moduli GS cancellation of the rest. The known orientifolds do not show the latter
(LLN). Gap 2: HIGH; no-go covers G₂ (D323–D324), EFT weights + GS (D325), and IIB U with twisted GS (this note), apart from that loophole.

**D327 (Danny "Test", 06:20 CT): inflation test of D326's loophole (locked, PREREG_D327_TWISTED_GS; results/twisted_gs_ns_d327.txt).**
Twisted-moduli GS enters K quadratically, so at the D-flat point α = 1 + δ²/3 (sign fixed, second order). Cancelling −b_a ln u needs
s_a δ = b_a/8π². Results (baseline n_s 0.9650, r 0.0036):
- s = 1: δ 0.0836, α 1.00233 → n_s 0.9693 (Δ +0.0043), r 0.0047.
- s = 2: α 1.00058 → n_s 0.9661 (Δ +0.0011), r 0.0038.
- s = ½: α 1.00932 → n_s 0.9795 (Δ +0.0145), r 0.0096.
Scored rule (|Δn_s| ≤ 0.004 at s = 1): **FAIL, narrowly (0.0043)**. It passes for s ≳ 1.04, i.e. if the twisted modulus couples to U(1)_Y slightly
more strongly than unit strength. This is far milder than D325's GS dilaton (Δn_s +0.0195 or no solution).
Note (post-data, NOT evidence): the shift is always upward (α > 1), toward ACT's higher n_s, with r rising together (0.0047 at s = 1). If this
route were ever adopted it would be a new locked variant, scored only on future data, like TWIST-P/L.
Status of the loophole: inflation-compatible for s ≳ 1, so inflation is not the obstruction here. It still rests on two unverified string
conditions: an N=2 sector with no SM-charged states, and complete twisted-moduli cancellation (which the known Z₃/Z₇ orientifolds lack, D326).
Gap 2: HIGH; the one surviving route is identified and passes the inflation test at s ≳ 1.

**D328 (pp, 06:22 CT, gap 2: does a known model realise D326/D327's loophole?) — not found, and the loophole narrows (literature).**
Lüst & Stieberger, "Gauge threshold corrections in intersecting brane world models" (hep-th/0302221; abstract read, the full text did not
render): in N=1 intersecting D6-brane orientifolds, "N=1 subsectors give rise to moduli-dependent one-loop corrections", in contrast with
ordinary orbifolds, where only N=2 sectors do. Intersecting/magnetised branes are T-dual to IIB D3/D7 models with U-dependent setups, so
"no SM-charged N=2 states" is not sufficient there. The N=1 sectors also feed moduli dependence through the brane angles. Whether the dependence
is on T or U was not extractable from the abstract.
Consequence: D326's loophole needs (i) D3-branes at an orbifold point (where only N=2 sectors carry moduli dependence), (ii) the rolling U-plane's
N=2 sector free of SM-charged states, and (iii) complete twisted-moduli GS (absent in the known Z₃/Z₇ cases, D326), plus D327's s ≳ 1.04.
No published model with all of these was found in this search. Gap 2: HIGH; the loophole stays open but narrow. Suggested next step, when Danny
chooses: treat the shield as an explicit assumption with this precise list of conditions, or split inflation from the tail.

**D329 (pp, 06:25 CT, gap 1 n_s: does the published analysis change D223?) — one new number; D223's conclusion stands (literature).**
arXiv:2512.05108 v2 (rest of the text read, offset 100k): for Planck + DESI DR2 in w0waCDM with broad priors they cite n_s = 0.9638 ± 0.0038,
"nearly identical" to Planck alone (ΛCDM 0.9638 ± 0.0040), against 0.9690 ± 0.0035 for Planck + DESI in ΛCDM. So freeing (w0, wa) fully
removes the DESI-driven upward shift of n_s; the authors call the Planck + DESI n_s "entangled with the DESI evidence for dynamical dark energy".
No CMB-SPA + DESI w0wa value is given.
Comparison with our own result (D157/D223): our NS-SPA run with the Twist's PURE background still preferred n_s 0.973–0.976, so the Twist's own
tail does not relieve the tension. Reading: the relief needs the DESI-sized evolution (w0wa free, wa ≈ −0.7 class), and the Twist's tail is much
milder (E_G conditioning, D290's 1–2σ). The Twist's 0.9642–0.9654 agrees with the w0wa-free number (0.0–0.4σ), but that is not its own
background, so this is not a rescoring. NS-SPA INCONSISTENT stands as scored.
Consequence for the paper (v6 item): state that the n_s inconsistency is conditional on the background. Under a DESI-like w0wa it vanishes for
Planck + DESI, but under the Twist's own milder tail it does not. Gap 1: HIGH, unchanged; the decider remains DESI DR3/SO resolving the
BAO–CMB tension (D223, D296).

**D330 (pp, 06:27 CT, gap 4 birefringence: anything new since D301/D303?) — Planck's relative calibration is internally consistent; the absolute
zero point is still untested (literature).** "Differential polarization calibration: a consistency test for cosmic birefringence"
(arXiv:2609.09149, Sept 2026): β cancels in map pairs, so a network of 28 Planck NPIPE detector-set pairs (100–353 GHz) measures only the
differences between instrument angles. It agrees with the Minami–Komatsu reconstruction (χ² 8.18 / 7 dof, PTE 0.32; all pulls < 1.8σ). Their MK
value is β = 0.37 ± 0.11° (anchored 0.37 ± 0.12°, or 0.40 ± 0.13° on f_sky 0.62). The authors stress this is not an independent confirmation
(same sky) and "does not establish the absolute value of β".
Reading: this removes one route to a Planck systematic (detector-to-detector inconsistency) but not the decisive one (a common absolute angle
offset). The Planck–ACT disagreement (D301) and the need for absolute calibration (drones/SO, D303) stand.
Twist status: the base model predicts β = 0. TWIST+ALP is the locked fallback if β is confirmed. Gap 4: HIGH, not rising (unchanged); the decider
is still an absolutely calibrated measurement (SO with drone calibrators, ~2027+).

**D331 (pp, 06:30 CT, gap 11 Hubble): a 2026 compilation makes the Twist's low H₀ a sharper cost (literature + arithmetic; estimate).**
"Dissecting the Hubble tension" (arXiv:2601.00650): of 54 sound-horizon-free, non-ladder H₀ values, the combined one-step value is
68.67 ± 0.46. By category: local with ΛCDM assumed (sirens, lensing, FRBs) 67.18 ± 0.90; pure local, model-independent (masers, cosmic
chronometers, cosmography, EPM) 70.38 ± 1.00; CMB r_s-free 68.71 ± 0.63. Distance ladder 72.74 ± 0.40, which is 4.5σ (correlations included)
from one-step. TDCOSMO (A&A, Jan 2026): ≈ 71.6, 4.6%.
The Twist's background-only H₀ = 65.7 (D169), with an assumed ±0.5 (not computed): 1.4σ below category 2, 4.2σ below category 3, 3.7σ below
category 4, 4.4σ below the one-step combination, and 1.8σ below TDCOSMO. The fair comparison for a non-ΛCDM background is the model-independent
category 3 (≈ 4σ). Categories 2 and 4 assume ΛCDM.
Caveats: the compilation is heterogeneous (cosmic-chronometer systematics; the paper itself finds a 2.4σ internal tension among one-step methods);
the Twist value is a background-only estimate without a full fit; and the error is assumed.
Verdict: gap 11 LOW–MEDIUM → MEDIUM. The low H₀ is no longer only "a cost against the ladder". Model-independent non-ladder probes also sit
~4σ above it (estimate). Next: a full-fit H₀ posterior from the stored NS-SPA PURE chains (computing it would be a reading of already-used data,
so state it as a sensitivity, not a test).

**D332 (pp, 06:33 CT, gap 11): CORRECTION to D331 using the stored full fits (field_tests/results/ns_pure.json; already-used data, so a
sensitivity, not a test).** Planck NPIPE + low-ℓ + lensing + DESI DR2 + Pantheon+ + DES Y6 S8 best fits: PURE Twist H₀ = 66.78, Ω_m = 0.313;
ΛCDM H₀ = 68.00, Ω_m = 0.305. D169's background-only 65.7 overstated the shift: the full fit moves H₀ by −1.2, not −1.7.
Redone with an assumed ±0.5 on the fit value: Twist vs model-independent category 3 (70.4 ± 1.0) is 3.2σ (ΛCDM: 2.1σ); vs the one-step combination
2.8σ (ΛCDM 1.0σ); vs category 2 0.4σ. So the Twist adds about 1σ to the tension that ΛCDM already has with the model-independent non-ladder
probes. D331's "~4σ" is withdrawn.
Gap 11: MEDIUM → LOW–MEDIUM. Stated cost: "the Twist's full-fit H₀ = 66.8 is ~1.2 below ΛCDM on the same data, about +1σ worse against
non-ladder probes; it does not address the ladder tension." The model card line is updated.

**D333 (deep loop 22, gap 2 loophole follow-up to D326–D328) — a concrete candidate setting, not a solution (literature + argument).**
Aldazabal, Ibáñez, Quevedo & Uranga, "D-branes at singularities: a bottom-up approach to the string embedding of the Standard Model"
(hep-th/0005067): the SM sits on D3-branes at a local C³/Z₃ orbifold singularity of an arbitrary compact bulk. A Z₃ singularity has no N=2
subsectors (no fixed planes), so the one-loop thresholds carry no b^{N=2} terms. The local gauge couplings are set by the dilaton plus local
twisted (blow-up) moduli, which the anomalous U(1) D-terms hold at the orbifold point. The bulk complex-structure moduli U do not enter the
local spectrum or the tree-level couplings, and M_s/M_P depends on the volume and dilaton, not on U.
That meets D326/D328's conditions (i) D3 at an orbifold point and (ii) no SM-charged N=2 sector, if the rolling field is a bulk U modulus
(diagonal, K ⊃ −3 ln(U+Ū)).
Open, and decisive: (a) does the Kaplunovsky–Louis Kähler-anomaly term c_a K still carry the bulk −3 ln(U+Ū)? That would give
d(1/α_a)/d ln u = −3c_a/16π², which is non-zero. Or is it cancelled by the local twisted-moduli GS (condition iii), given that local D3 matter
metrics do not depend on U? This needs a dedicated check against the exact (Arkani-Hamed–Murayama) formula; not done here. (b) Bulk U must
also give the Twist's potential: the cliff and rung-3 W would have to come from bulk fluxes/instantons depending on U, not on the volume.
(c) D327's s ≳ 1.04 applies if a GS shift is needed.
Verdict: the first concrete string setting where the shield might hold beyond tree level, pending (a). Not a claim. Gap 2: HIGH.

**D334 (pp, 06:32 CT, D333's decisive point (a)) — the loophole closes by the literature's own locality argument; a general one-loop no-go
(literature + algebra; estimate level).**
Conlon & Palti, "Gauge threshold corrections for local string models" (arXiv:0901.4350): K̂ = −2 ln𝒱 − ln∫iΩ∧Ω̄ − ln(S+S̄), and the physical
coupling is g_a⁻² = Re f_a + β_a ln(M_P/μ)·(…) + [(Σn_rT_a(r) − T(G))/16π²]K̂ − Σ_r[T_a(r)/8π²] ln det Z^r. For local D3 models they fix Z by
requiring local Yukawas to be bulk-independent, √(ZZZ) ∝ e^{K̂/2}, and the volume terms then combine into β_a ln(M_X²/μ²) with M_X = R M_s.
They drop the complex-structure term (−ln∫Ω∧Ω̄) as "not relevant to our purposes".
Applying the same locality logic to the bulk U (K̂ ⊃ −3 ln(U+Ū)): bulk-independent local Yukawas need Z ∝ e^{K̂_cs/3} = u⁻¹. The K̂ and Z terms
then leave (−3c_a + 2ΣT_a(r))·ln u = −b_a ln u, i.e. d(1/α_a)/d ln u = −b_a/4π. That is the same drift as G₂ (D324) and the volume case. If instead
Z is U-independent, the Yukawas pick up e^{K̂/2} ∝ u^{−3/2}, and masses drift. One of the two always moves.
General statement (estimate, at one loop): for any rolling field with K ⊃ −3 ln(X+X̄), x-independent holomorphic f and y, and universal
(local) matter metrics, physical Yukawas and gauge couplings cannot both be x-independent. Making Yukawas fixed forces
d(1/α_a)/d ln x = −b_a/4π (α_em: d ln α/d ln x ≈ 7×10⁻³). The escapes are non-universal weights (D293: none with a holomorphic μ), plus
GS: a dilaton GS spoils inflation (D325), and a twisted-moduli GS needs couplings s_a ∝ b_a that the known Z₃/Z₇ models lack (D326), passing
inflation only for s ≳ 1.04 (D327).
Verdict: D333's local D3 + bulk-U candidate fails condition (a), unless twisted moduli supply group-dependent GS terms ∝ (33/5, 1, −3), which
is not shown in any model. Gap 2: HIGH; the no-go now covers volume, G₂ and complex-structure rolling fields alike. The weak point is the
Twist's own e^K ∝ x^{−3}, which is what makes it rung 3.
v6 suggestion: state this no-go explicitly in §5.1 as the precise form of the shield assumption.

**D335 (deep loop 23, gap 10 strong CP: any change since D281?) — timelines confirmed, no exclusion yet (literature).** (D333(a) was settled
in D334, so this loop took gap 10.) CERN Courier, "In pursuit of the post-inflation axion": the post-inflation window lies within one or two
decades up to ~100 μeV. ALPHA (plasma haloscope, 40–400 μeV) Phase I covers 40–80 μeV, with physics data from 2026 (dark photons first)
and a full axion search in 2027–28; Phase II goes up to 200 μeV at DFSZ. MADMAX (40–400 μeV): its 2024 prototype at ~19 GHz found no excess
and set world-best dark-photon limits at 78.6–84.0 μeV. Installation in the Morpurgo magnet is planned for LHC LS3 (mid-2026–2029), with a
4 T magnet ~2030. ADMX/CAPP/HAYSTAC lead below 25 μeV. The Twist's needed separate post-inflation axion (40–600 μeV) is not yet probed at QCD
coupling; first coverage is ALPHA 2027–28 (lower end). Gap 10: LOW–MEDIUM, unchanged (D281 timelines confirmed).

**D336 (pp, 06:47 CT, gap 5 dark-energy evidence) — newest compilation agrees with D237/D290/D307; nothing changes (literature).**
"Study of dynamical dark energy using DESI DR2 BAO, CMB, and Type Ia supernovae data" (arXiv:2609.10567, Sept 2026): DESI DR2 + Planck (+ ACT DR6
lensing) + one SN set, five parametrisations. Significance vs ΛCDM: Pantheon+ 2.1–2.9σ, Union3 3.2–3.7σ, DES-Dovekie 2.9–3.3σ (they note
DES-Dovekie gives ~3σ, not the earlier 4σ). DES-Dovekie CPL: w₀ = −0.807 ± 0.056, w_a = −0.721 ± 0.221; wCDM w = −0.988 ± 0.021. Every
parametrisation prefers quintom-B (w₀ > −1 today, phantom in the past).
For the Twist: a thawing field cannot cross w = −1, so the data's preferred shape stays out of reach. The Twist captures only the w₀ > −1 part,
which is why its Δχ² gain is modest (FULL −3.4 vs ΛCDM, pure_twist.json). Physical-prior analyses (D290) give 1–2σ, and the bispectrum weakens
the evidence (D307). Gap 5: MEDIUM, unchanged. The decider is still DESI's full-survey results (2027).

**D337 (deep loop 24, gap 14 neutrino masses: cosmology vs the Twist's assumed normal ordering) — a possible new pressure point; a check is
needed (literature).** "Measuring cosmic neutrino masses independently of dark energy" (arXiv:2607.24742): DESI DR2 + CMB + lensing gives
Σm_ν < 0.056 eV (95%) in ΛCDM, < 0.080 in wCDM, < 0.152 in w0wa (σ inflated ×1.4 and ×2.5). The data prefer an effective negative mass
(≈ −0.10 eV in ΛCDM) that the positivity prior turns into the tight limit. A dark-energy-independent route gives only < 0.41.
The Twist assumes normal ordering with the lightest mass zero, Σm_ν ≈ 0.059 eV. That is just above the ΛCDM limit and inside the w0wa one. The
Twist's background is thawing (w > −1, no crossing). Thawing quintessence is generally expected to tighten neutrino bounds rather than relax them
(the w > −1 direction is degenerate with lower Σm_ν; literature expectation, not checked here). So the Twist with Σm_ν = 0.059 may sit at or
beyond the 95% edge.
To do (sensitivity, already-used data): read the Twist fits' Σm_ν setting and, if fixed at 0.06, note it. A free-Σm_ν Twist fit would be a new
computation and needs a lock plus PC/cloud time. Gap 14: LOW → LOW–MEDIUM (flagged, not yet a failure).

**D338 (pp, 06:57 CT, D337 follow-up: which Σm_ν did our fits use?) — fixed at 0.06 eV everywhere (repo read).** Every fit configuration in
the repo fixes the neutrino sector at the Planck baseline: one massive neutrino with m_ncdm/mnu = 0.06 eV and N_ur = 2.0328 (AxiCLASS:
early_late_spa.py, cross_engine_pact.py, debug_ede.py, twofield/*, torsion_shape/*; CAMB: ub2_fit.py, tf_camb_ref.py; cobaya yaml/*).
So all of our Twist and ΛCDM χ² values and the NS-SPA/PURE comparisons assume Σm_ν = 0.06 eV. That is in fact the Twist's own assumption
(normal ordering, lightest ≈ 0, Σ ≈ 0.059), so the fits are self-consistent for the model as stated.
What is not known is whether the data penalise Σ = 0.06 more in the Twist background than in ΛCDM. Since the fits fix it, our Δχ²(Twist − ΛCDM)
compares the two at the same Σm_ν, which is fair. Whether 0.06 itself is disfavoured is a statement about both models (DESI ΛCDM limit 0.056,
D337). A free-Σm_ν Twist fit would tell whether thawing tightens it further; that is a new computation (lock + PC time), left for Danny to decide.
Gap 14: LOW–MEDIUM (flagged; the Twist–ΛCDM comparison is unaffected).

**D339 (pp, 07:00 CT, gap 3 SUSY breaking: any new constraint on the eV-gravitino branch?) — one collider result; the branch stands, with a
consequence (literature).** GAMBIT, "Collider constraints on electroweakinos in the presence of a light gravitino" (arXiv:2303.09082): with
m_3/2 = 1 eV fixed ("the exact choice … has very little impact" while it is small), 13 TeV ATLAS/CMS + LEP exclude most electroweakinos below
1 TeV. Surviving regions: degenerate Higgsinos from ~140 GeV, a wino band near 400–500 GeV (2σ), winos above 700 GeV, and a light bino from
~62 GeV. Cosmology is not included. The search otherwise returned only papers already used in D291 (Ibe–Yanagida 1608.01610;
Hook–McGehee–Murayama 1801.10160; Lu–Shirai 1712.02359).
For the Twist: the adopted eV-gravitino branch (D291–D292) makes the lightest neutralino decay promptly to a gravitino, so these limits apply
directly. They constrain the mediation sector's spectrum, not the Twist's x-independence (D292). Consequence for v6 §5.2: say that the
branch implies prompt NLSP → gravitino decays at colliders, and cite GAMBIT for the surviving electroweakino regions.
Gap 3: LOW–MEDIUM, unchanged.

**D340 (pp, 07:03 CT, gap 12 initial conditions) — the Twist is in the robust class (literature).** "Robustness of inflation to kinetic
inhomogeneities" (arXiv:2405.03490, numerical relativity): plateau models with a super-Planckian field-space scale (Starobinsky,
μ = √(3/16π) M_Pl) inflate even after strong uniform kicks with the potential at only ~5% of the energy. Sub-Planckian models (μ = 5×10⁻⁴ M_Pl)
fail even for small gradient and kinetic energy. Caveats: two models only, conformally flat periodic data.
The Twist has α = 1 (x = e^{√(2/3)φ}), the same field-space scale as Starobinsky, so it is in the robust class. Its extra structure, the cliff
at the far end, lies on the side the field rolls toward, not on the side kicks come from. D288 already showed light fields are safe.
Gap 12: LOW, unchanged and better supported.

**D341 (pp, 07:06 CT, referee m1 on D317: limits at 10⁵ GeV, not 10⁷) — D317 is somewhat too strong; the ξ ~ 1 window reaches ~200 TeV
(literature; order of magnitude).** IceCube 6-year HESE update (arXiv:1903.12623): limits appear only as curves (their Fig. 5, not read
numerically). The text says they are largely unchanged from the 4-year analysis, except ν and charged-lepton channels at ~100–200 TeV, which
tighten by ~10×. The best-fit lifetimes (Table 1) set the scale, in 10²⁸ s: W⁺W⁻ 0.37 at 412 TeV, bb̄ 0.07 at 1.1 PeV. So hadronic limits at a few
hundred TeV sit at ~10²⁷–10²⁸ s, below the 6×10²⁸ s LHAASO number at 10 PeV used in D317. HAWC (Virgo, arXiv:2309.03973) is in the same
range; not read.
Revised reading of D317 (τ ≈ 10²⁴ s (10⁶ GeV/m)⁵ ξ⁻²): against ~10²⁷–10²⁸ s, ξ ~ 1 is allowed up to ~150–250 TeV (10²⁸ at 100 TeV; 3×10²⁷ at 200
TeV). At 500 TeV it needs ξ ≲ 0.06–0.2. D317's "only ~100 TeV survives" becomes "≲ 200 TeV survives for ξ ~ 1". Both are order-of-magnitude,
and the anchor (D242) is itself a reading of plots. Gap 13: LOW–MEDIUM, unchanged; the decaying-DM signal is still optional (D318).

**D342 (pp, 07:09 CT, gap 15: naturalness of the post-data n_s variants) — the literature keeps finding tree-level deformations of the
Starobinsky attractor that reach ACT's n_s; nothing new for the Twist's variants (literature).** Ijaz, Pirzada & Rehman (arXiv:2607.04504,
Jul 2026): in a shifted-hybrid non-minimal Higgs model, the leading non-renormalisable superpotential operator "induces a controlled
deformation of the Starobinsky attractor" that shifts n_s into the ACT-preferred range, with r ~ 10⁻³–10⁻². This is the same class as
TWIST-P/L (Kähler deformations) and TWIST-G− (W ∝ T^{1+ε}), and they do not compute loops. The search also returned 2504.06002 ("Has ACT
measured radiative corrections to tree-level Higgs-like inflation?"), a radiative route analogous to D285's TWIST-C origin.
Reading: an ACT-sized n_s shift from one small deformation is generic in this model class. The Twist's variants are neither more nor less natural
than published ones, and their agreement with ACT is not evidence (they are scored only on future data). Gap 15: LOW, unchanged.

**D343 (pp, 07:12 CT, gap 2: is D334's one-loop drift an artefact that higher orders could remove?) — no; the structure is exact
(literature, partly read).** Arkani-Hamed & Murayama, "Holomorphy, rescaling anomalies and exact β functions in supersymmetric gauge
theories" (hep-th/9707133; first 100k characters read): going from holomorphic to canonical normalisation is a rescaling with an anomalous
Jacobian. "The F terms given above are exact"; the canonical coupling's change is given by the NSVZ β function, and higher-dimension D-terms
are 1/M-suppressed. The matter-field rescaling (the ln Z terms) is the same kind of anomaly; that part was not in the portion read and is the
standard Shifman–Vainshtein/NSVZ statement.
Consequence: the moduli dependence in D323/D334, which comes from the rescaling anomalies via K and ln Z, is fixed by holomorphy and anomalies.
It is not a one-loop accident that higher orders could cancel. Beyond one loop, only the NSVZ-type ln g_c term adds, which multiplies the same
drift by 1 + O(α). So D334's no-go holds to all orders in the gauge couplings (up to 1/M D-terms), with the same escapes (weights, GS).
Gap 2: HIGH; the no-go is firmer.

**D344 (pp, 07:14 CT, gap 1 n_s: any new SPT-3G release?) — none found (literature).** Searches return SPT-3G D1 (2019/20 Main field,
arXiv:2506.20707; used in NS-SPA), an APS April 2026 talk on D1 ΛCDM constraints, and a Perimeter talk (June 2026) on the same 2019/20
polarisation maps, with no new data release, no new n_s value and no Ext-10k timeline. The forecast in D296 (Ext-10k + Planck σ(n_s) ≈ 0.003)
stands as the next decisive SPT step. Gap 1: HIGH, unchanged; the deciders remain DESI DR3 / SO resolving the BAO–CMB tension (D223, D329)
and SPT-3G Ext-10k.

**D345 (pp, 07:17 CT, gaps 2/9: does the string literature already state D334's kind of no-go?) — yes, in general form; D334 is a sharper
special case (literature, partly read).** Acharya, Maharana & Muia, "Hidden sectors in string theory: kinetic mixings, fifth forces and
quintessence" (arXiv:1811.10633; first 100k characters): light moduli must live in hidden sectors with weaker-than-Planck couplings to the SM;
"the sequestering is never complete", since loops and kinetic mixings always couple geometrically separated sectors. Their results are "lower
bounds on the strengths of the interactions", and the couplings fall only as inverse powers of the volume. Quintessence also needs
functional-level tuning against visible-sector loops.
Relation to the Twist: this is the general statement, while D323–D334 give a specific and stronger one for a K ⊃ −3 ln rolling field. There the
leak is O(1) per e-fold of x, fixed by rescaling anomalies, d(1/α_a)/d ln x = −b_a/4π, not volume-suppressed, because the rolling field itself
sets e^K. Citing 1811.10633 alongside Kaplunovsky–Louis and Conlon–Palti makes v6 item 16's framing standard rather than novel. The new part is
the explicit −b_a/4π coefficient and the six-fix test.
Gap 2: HIGH, unchanged; v6 item 16 should add this citation.

**D346 (pp, 07:20 CT, test timelines for gap 1 and the r prediction) — CMB-S4 is cancelled; the paper's "CMB-S4 class" wording is outdated
(literature).** Scientific American: on 10 July (2025, per the article's dating) DOE and NSF jointly ended support for CMB-S4 ("can no longer
support the CMB-S4 project"), citing ageing South Pole infrastructure and budgets; the PI (Carlstrom) calls it effectively cancelled. DOE plans
near-term upgrades of existing South Pole and Chile experiments. What remains: Simons Observatory (now operating in Chile), BICEP Array and
SPT-3G at the Pole, AliCPT (Tibet; phase 1 built), and LiteBIRD (JAXA, launch targeted for the early 2030s). The article gives no quantitative r
reach. SO's design goal is σ(r) ≈ 0.002–0.003 (prior knowledge, not re-checked here).
For the Twist: TWIST-INFLATION's r = 0.0035–0.0038 is about 1.5–2σ for SO, so the decisive r test moves to LiteBIRD (2030s). The exploratory
note says "LiteBIRD and CMB-S4 can separate" the variants, and the paper's table says "Simons Observatory, LiteBIRD, CMB-S4 class". v6 item 17:
replace "CMB-S4" with "SO (+ upgrades), BICEP Array, LiteBIRD", and note that the r decision is likely early-2030s.

**D347 (pp, 07:23 CT, checking D346's prior-knowledge number) — SO target confirmed (literature).** "The Simons Observatory: combining
delensing and foreground cleaning for improved constraints on inflation" (arXiv:2405.13201): nominal target σ(r = 0) ≤ 0.003; delensing
lowers σ(r) by 27–37% depending on the foreground model (exact delensed values only in their Fig. 4). Hence σ(r) ≈ 0.002–0.003, as D346 assumed.
For TWIST-INFLATION (r = 0.0035–0.0038): ~1.2–1.9σ with SO. That is a hint, not a decision. The locked rule fails the model if r < 0.002 or
r > 0.008 at 95%, so SO can fail it only on the r > 0.008 side or with a clear null. Decisive: LiteBIRD (σ(r) ≲ 0.001 design, early 2030s).
D346 now rests on a source.

**D348 (pp, 07:25 CT, LiteBIRD reach) — confirmed (literature).** "The LiteBIRD mission to explore cosmic inflation" (arXiv:2406.02724,
SPIE 2024): target total δr = 0.001 "including systematic errors and margin"; launch aimed at Japan's fiscal year 2032. For TWIST-INFLATION
(r = 0.0035–0.0038): a ~3.5σ detection is expected if the model is right. The locked failure conditions (r < 0.002 or > 0.008 at 95%) become
decisive, so the r test date is ~2033–35, allowing for survey time. Recent status not re-checked (the 2024 paper is the latest found).
Together with D346–D347: SO gives a ~1–2σ hint in the late 2020s, and LiteBIRD decides in the 2030s.

**D349 (pp, 07:28 CT, test calendar for the tail predictions (E_G, growth, w_a)) — Euclid cosmology slips to mid-2027 at the earliest
(blog report of the official timeline).** P. Coles, "Euclid update – revised timeline" (telescoper.blog, 16 Jun 2026): DR1 is now staged. The
first tranche ("DR-Foundation", LE1+LE2 only) comes in November 2026, and the full DR1 in mid-2027 (probably June). "There will be no official
cosmology results from Euclid DR1 until mid-2027 at the earliest", since LE3 (needed for cosmology) is added in 2027. The official ESA page
(cosmos.esa.int DR1 timeline) was not read.
Test calendar for the Twist (D290, D307, D346–D348):
- 2027: DESI full-survey dark energy (w₀/w_a, WATCH-PURE-DR3, WA-CEILING, GROWTH) and Euclid DR1 cosmology (growth/E_G at stated conditioning).
- Late 2020s: SO r hint (~1–2σ), SO absolute birefringence calibration, ALPHA axion (2027–28), SPT-3G Ext-10k n_s.
- 2030s: LiteBIRD r (decisive).
So the dark-energy-side tests come first, in 2027.

**D350 (pp, 07:33 CT, CORRECTION to D346–D348: SO's expanded array) — SO can nearly decide r before LiteBIRD (literature).** "The Simons
Observatory: forecasted constraints on primordial gravitational waves with the expanded array of Small Aperture Telescopes"
(arXiv:2512.15833, Dec 2025): the SAT array doubles from three to six telescopes by 2027, and the survey is extended to 2035. Forecasts at
r = 0: σ_r = 1.2×10⁻³ baseline (moderate foregrounds, ℓ_knee 50, 70% delensing) and 7×10⁻⁴ optimistic, ~2.5× better than the original plan.
D347's σ(r) ≈ 0.002–0.003 was the original nominal design and is superseded.
For TWIST-INFLATION (r = 0.0035–0.0038): ~3σ baseline (r/σ ≈ 2.9–3.2) and ~5σ optimistic by ~2035, comparable to LiteBIRD (δr = 0.001,
launch JFY 2032). The locked failure conditions (r < 0.002 or > 0.008 at 95%) become decisive with SO alone on the baseline forecast. The test
calendar (D349) is revised: an r decision is likely ~2032–35 from SO and/or LiteBIRD, with SO hints growing through the late 2020s.
The isocurvature question that started this search (an SO forecast for D278's margin) was not answered; the gap 7 status stands.
