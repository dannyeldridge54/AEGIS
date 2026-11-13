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
