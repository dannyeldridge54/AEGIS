DEVELOPMENTS 72–75: the four weak spots (13 Nov 2026). AI-assisted. Insert into the matter doc after D71.
> From D739 on, every D-note carries one map line: `MAP: node=<id> status=<status> touches=[ids]` (or `MAP: none`). Run `python tools/ladder/ladder.py update` after writing it (docs/UPDATE_LADDER_PLAN.md).

> **Numbering rule (from 15 Nov 2026).** Before writing a note, claim its number: `sh tools/dnotes/claim_d.sh "short title"`
> (pulls, takes the number in `NEXT_D.txt`, increments it, commits and pushes the claim; retries if another session got there first).
> Write the note under the number it prints. Index: `python tools/dnotes/build_index.py` → `docs/D_INDEX.md`.

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

**D351 (pp, 07:36 CT, gaps 7 and 1: SO enhanced-LAT forecasts) — n_s error halved; no isocurvature number (literature, first 100k chars).**
"The Simons Observatory: science goals and forecasts for the enhanced Large Aperture Telescope" (arXiv:2503.00636): SO "will halve the current
error bar on … n_s". Against the current CMB-SPA σ ≈ 0.003 (D223), that gives σ ≈ 0.0015. Isocurvature is listed as a target without a number.
For the Twist: at σ(n_s) ≈ 0.0015, the gap between the Twist (0.9642–0.9654) and the CMB-SPA + DESI ΛCDM value (0.9737) would be ~6σ if the
central value held. If the BAO–CMB tension resolves toward the CMB-only/w0wa value (0.964–0.969, D329), the Twist is fine. SO therefore sharpens
gap 1 into a clean test, with its outcome tied to the BAO–CMB resolution. The gap 7 isocurvature margin (1.4–1.5×) has no SO forecast here; the
general expectation of a factor ~2 (D278) is unchanged and unsourced.

**D352 (pp, 07:39 CT, gap 7: a sourced isocurvature forecast?) — still none for scale-invariant uncorrelated modes (literature).** "The
benefits of CMB delensing" (arXiv:2111.15036): delensing substantially improves f_cdi constraints, nearly reaching unlensed-spectra precision
for blue-tilted uncorrelated CDI, for generic experiments A/B/C. It gives no numbers in the text, no SO/S4 naming, and no baryon isocurvature.
Other hits (compensated isocurvature forecasts for LiteBIRD/CORE, 1701.07039; CORE inflation, 1612.08270) cover other modes or a
non-funded mission.
Conclusion: there is no sourced forecast for the scale-invariant uncorrelated isocurvature bound the Twist's hidden axion faces. D278's "factor
~2 (SO class)" stays an unsourced expectation, and it should not be stated as a forecast in v6. Gap 7: LOW–MEDIUM, unchanged; the D320 locked
run is still pending.

**D353 (pp, 07:42 CT, gap 4: ACT DR6 birefringence paper read directly) — ACT gives β ≈ 0.22 ± 0.07° (2.9σ) and declines to draw
conclusions (literature).** "Cosmic birefringence from the Atacama Cosmology Telescope DR6" (arXiv:2509.13654): the mean rotation is
⟨ψ⟩ ≈ 0.20° ± 0.03° (stat), ± 0.08° with calibration uncertainty. The instrument angles come from a polarisation-sensitive optics ray-tracing
model (σ 0.09° PA4/PA5, 0.11° PA6), independent of Galactic dust. A joint fit with the optics priors gives β = 0.215° ± 0.074° (2.9σ from zero),
"consistent with WMAP and Planck". The authors say unresolved systematics (an unexplained PA5 f090/f150 discrepancy) "do not yet allow us to
draw strong cosmological conclusions", and they ask for calibrator-based confirmation.
Relation to D301: D301's ">3σ Planck–ACT difference" compares the total angles (Planck 0.29 ± 0.03 vs ACT 0.19 ± 0.03, statistical only).
With ACT's 0.08° calibration error, the gap (0.10°) is only ~1.2σ, so D301's miscalibration hint was overstated, and the experiments are
mutually consistent once systematics are included. Combined evidence: Planck MK 0.37 ± 0.11° (D330), ACT 0.215 ± 0.074°, both ~3σ, and neither is
absolutely calibrated.
Twist (BIREF-NULL, β = 0): ~3σ against it on each experiment taken at face value, unscored (the locked rule needs an absolutely calibrated
measurement). Gap 4: HIGH, not rising. D301's favourable reading is withdrawn. The decider is still SO with drone calibration (D303).

**D354 (pp, 07:45 CT, gap 4: when does an absolutely calibrated β arrive?) — the calibrator goal is 0.01°, with no date (literature).**
POLOCALC overview (arXiv:2606.20171, Jun 2026): drone-borne calibrators aim at an absolute polarisation-angle accuracy of 0.01° for small-aperture
CMB telescopes. No achieved accuracy, no named experiments and no date for a calibrated birefringence measurement are given. PROTOCALC
(arXiv:2502.14473) is a W-band calibrator applied to SO and CLASS (D303 context: 0.045° statistical). SO's wire-grid system (2309.02035) is
relative calibration.
Reading: 0.01° would test β = 0.2–0.37° at ≫10σ, so the BIREF-NULL rule becomes decisive once a drone-calibrated SO/CLASS β is published.
The date is open; likely late 2020s. Gap 4: HIGH, not rising, unchanged.

**D355 (07:25 CT, Danny's choices: split model + free-neutrino PC fit + scheduled loops) — locks written; PC job prepared.**
(1) PREREG_TWISTI.md (locked and pushed): TWIST-I = v5 inflation/reheating/matter/DM unchanged, x stabilised after reheating (m_x ≥ 5 meV),
Λ for dark energy. It removes gap 2 (no drift if x is frozen), the H₀ cost (D332) and the tail's n_s background dependence, and gives up the
"Λ from the cliff" and the tail predictions. Four future-data rules: r, n_s, w = −1, β = 0. The already-seen ΛCDM-background n_s cost (8.46)
is stated as not evidence. Open (to check in loops): does the matter yield need x to keep rolling after reheating? (freeze-out ~2×10¹³ GeV;
the stabilisation must come later); and what stabilises x without reintroducing drift.
(2) PREREG_D355_MNU_FREE.md + DEVIATIONS (D1, before running), mirrored and hash-checked on the PC (34da959e…). Runner:
cmb-fit/axiclass/run_mnufree_d355.sh (two fits in parallel, OMP 4 each, then score to field_tests/results/d355_mnufree.json); launcher
Desktop\RUN_D355_MNUFREE.bat. These are new files only, with no git operation on the PC repo. The fits run in WSL, which this session cannot
start, so Danny double-clicks the .bat (~1.5 h, by the NS-SPA timings of 5100 s/fit).

**D356 (review of D355/TWIST-I, 07:30 CT) — two issues found and fixed in the record.** (1) The TWIST-I lock said x is stabilised "after
reheating", but the v5 matter yield needs x to keep rolling until freeze-out (x_end ≈ 29.8, T ~ 2×10¹³ GeV). Fixed by deviation D1: x rolls as
in v5 through matter genesis, then settles at x_min ≥ 30 before BBN. (2) The angle relic of D299–D300 scales as (73/x_min)². At x_min ≈ 30 the
12–28% becomes ~70–170% of DM, a possible overclosure (estimate). TWIST-I needs x_min ≳ 50 in the eV-gravitino branch, or a stabilising sector
that also fixes the angle. Recorded as deviation D2 (a consequence, not a rule change).
Other checks in this review: the D355 wrapper reuses ns_spa_fit.setup() unchanged (the same likelihoods, including S8, the same builds and
best_of 4); the hashes match on cloud and PC; the launcher path matches the connected repo; E.save's derived Ω_m keeps 0.06 hard-coded (a
derived quantity only, it does not affect χ²; noted). D320 is still running (started 05:50).

**D357 (second review, 07:40 CT) — TWIST-I has a moduli problem; the assumption is revised (deviation D3).** A field that arrives at its
minimum while rolling oscillates with a Planckian amplitude. A light x (the lock's m_x ≥ 5 meV) would overclose. The standard way out is a heavy
modulus that decays before BBN: Γ ≈ m³/8πM_P² gives T_decay ≈ 0.12 / 1.4 / 3.9 MeV for m = 10 / 50 / 100 TeV, so m_x ≳ 100 TeV (estimate).
Alternatively the settling is adiabatic. If the stabiliser also makes the angle heavy, D356's relic problem (x_min ≳ 50) disappears.
New consequences to compute: entropy from x decay dilutes n_B/s (the fitted m_σ shifts down again) and changes N* slightly (and so n_s, r at
the 10⁻⁴ level). Both are inside the TWIST-I record as open items. Status: TWIST-I stays adopted; its open list is (a) a stabiliser with
m_x, m_y ≳ 100 TeV or adiabatic settling, (b) the x-decay dilution of the matter yield, (c) the N* shift.
Also checked in this pass: TWIST-I rule 3 ("any of the three SN samples" at > 5σ) is strict but well defined; rule 2 uses ΛCDM-background
n_s, which is the right background for TWIST-I; D355's setup is unchanged.

**D358 (pp loop, 07:28 CT, TWIST-I open item (a): how can x be stabilised after matter genesis?) — strong (supersymmetric) stabilisation is
the only route compatible with the eV-gravitino branch (literature + argument).** Review "Inflation, the scale of supersymmetry breaking, and
moduli stabilization" (arXiv:1511.03413): in KKLT/LVS, modulus masses and barriers scale with m_3/2 (stability needs m_3/2 ≳ H; KKLT with chaotic
inflation needs m_3/2 > 2×10¹⁴ GeV). In "strong" stabilisation the modulus sits in a supersymmetric Minkowski vacuum (racetrack, or couplings to
extra chiral fields), so its mass does not depend on m_3/2. The review does not discuss the moduli problem.
For TWIST-I: the adopted eV gravitino (D291–D292) rules out m_3/2-scaled stabilisation (it would give an eV modulus, the D357 moduli problem).
D357's m_x, m_y ≳ 100 TeV therefore needs strong, SUSY-preserving stabilisation of T at x_min: a racetrack-type W(T) with W = ∂W = 0 at x_min,
switched on only for x ≳ 30 (e.g. condensates whose e^{−a T} turn on as the field arrives). This is the same tuning type as D315/M3, here as a
model-building requirement. Not constructed. Open item (a) is restated as "a strong SUSY-preserving stabiliser of T at x_min ≳ 30 with
m ≳ 100 TeV". D320 is still running; D355 has not started (waiting for Danny's launcher).

**D355a (07:42 CT) — D355 started.** Danny was away from home, so the launcher was opened through computer use (File Explorer, click
tier; double-click on Desktop\RUN_D355_MNUFREE.bat). The log reads "2026-11-14 07:40:21 D355 start". Both fits (PURE, LCDM) initialised their
likelihoods (DESI DR2 BAO etc.) and entered the minimiser. Expected ~1.5 h, so the score is due ~09:15 CT. No other PC action was taken.

**D359 (pp loop, 07:45 CT, TWIST-I open item (b): entropy from x settling) — a 100 TeV decaying x is NOT enough; settling must be adiabatic
(estimate).** Checks first: D320 still running (cloud); D355 running on the PC since 07:40 (both fits in the minimiser).
Estimate (standard moduli cosmology; g* = 106.75, Γ = m³/8πM_P²): x starts oscillating when H ≈ m_x (capped at matter freeze-out,
T ≈ 2×10¹³ GeV) with ρ_x/ρ_r ≈ (Δφ/M_P)²/6, grows ∝ 1/T, and dilutes everything by Δ ≈ (Δφ²/6M_P²) T_osc/T_decay when it decays.
- m_x = 100 TeV: T_osc 2.7×10¹¹, T_decay 2.2 MeV → Δ ≈ 2×10¹³ at Δφ = M_P, still 2×10⁷ at 10⁻³ M_P.
- m_x = 10⁹ GeV: T_decay 2 TeV → Δ ≈ 1.5×10⁹ (M_P) and 1.5×10³ (10⁻³ M_P).
- m_x = 10¹³ GeV: T_decay 2×10⁹ GeV → Δ ≈ 1.5×10³ (M_P) and ≈ 1 (10⁻³ M_P).
The v5 matter yield is 1.25× observed (D277), so any Δ ≫ 1 destroys n_B/s, and the gravity-only DM yield (D112) as well.
Verdict: D357's "≳ 100 TeV, decays before BBN" removes the BBN problem but not the dilution problem. TWIST-I needs the field to arrive at
x_min with a canonical displacement ≲ 10⁻⁷ M_P (100 TeV) to ≲ 10⁻³ M_P (10¹³ GeV), i.e. ADIABATIC capture: the minimum must form gradually
around the rolling field, with m_x ≫ H throughout. Equivalently, the stabiliser must switch on smoothly as the field arrives (a minimum that
tracks the field). This is the hardest TWIST-I requirement so far; it is an estimate (no full computation; f_x at arrival is model-dependent).
Status: TWIST-I stays adopted, but its open list now leads with "(a') adiabatic capture of x". The x-only dilution of item (b) is moot if
capture is adiabatic.

**D320b (scored, locked PREREG_D320_ALT_ISOCURV; results/alt_isocurv_d320.txt, finished 07:4x CT) — PASS.** Validation: the canonical
yield with σ₀ × 1.05 is 1.3078×10⁻¹⁰ against D277's 1.3060×10⁻¹⁰ (+0.14%, within 1%), so the run is valid. The same run gives a
canonical sensitivity of 3.734 (D277: 3.70). Alternative reading: n_B/s 5.7694×10⁻¹¹ at σ₀ × 1.05 (baseline 4.8209×10⁻¹¹), giving
**S_alt = 3.681 ≤ 5 → PASS**. Margin at f = 0.1 M_P: 5.1/3.681 = 1.39 ≥ 1, so isocurvature passes under the alternative reading too, with the
same ~1.4× margin as the canonical one (D278). Stated limitation (in the lock): m_σ = 5.8×10¹⁰, not the alternative fit point 3.0×10¹⁰.
Gap 7: LOW–MEDIUM, unchanged; the coupling-reading question no longer affects isocurvature.

**D360a (Danny "More test", T2 scored; PREREG_D360_TESTS + D1; results/modulus_dilution_d360.txt) — D359's arithmetic holds where its
assumptions hold; one case fails, and the failure exposes an UNDERESTIMATE in D359 (correction).**
Averaged modulus + radiation + decay from H = m: m = 10⁹, A = 1 gives 2.48×10⁹ (est 1.5×10⁹, ratio 1.66, pass). m = 10⁹, A = 10⁻³ gives 2.17×10³
(ratio 1.44, pass). m = 10¹³, A = 10⁻³ gives 1.19 (pass). m = 10¹³, A = 1 gives 2.48×10⁵ (est 1.5×10³, ratio 166, FAIL).
Reason for the fail: D359 capped the start of oscillation at matter freeze-out (T = 2×10¹³ GeV) but kept the energy fraction at A²/6. That
fraction is only right when oscillation starts at H = m. For m ≫ H_arrival (H at 2×10¹³ GeV is 5.6×10⁸ GeV), the fraction at arrival is
(A²/6)(m/H)², which is larger. Corrected requirement for Δ ≤ 1 (aegis-check: recomputed in code): A ≲ 2×10⁻⁷ M_P at m = 10⁵ GeV,
≲ 1.4×10⁻⁵ M_P at 10⁹ GeV, and ≲ 1.4×10⁻⁶ M_P at 10¹³ GeV. D359's "≲ 10⁻³ M_P at 10¹³ GeV" is withdrawn.
Conclusion strengthened: TWIST-I needs adiabatic capture with a residual displacement of 10⁻⁷–10⁻⁵ M_P for any m_x. T1 (isocurvature at
the alternative fit point) is running in the cloud (~2 h).

**D355c (07:55 CT) — PURE fit crashed; crash rerun queued (deviation D2).** The log shows "07:52:09 fit PURE FAILED", ~10 min in, with no Python
traceback (most likely the process was killed for memory while two coupled-build fits ran in parallel). The LCDM fit is still running. Under
deviation D2 (written and pushed first), RUN_D355_PURE.bat was opened by computer use at 07:54:58. It waits for the LCDM result, then runs
PURE alone with unchanged settings, then scores. New ETA: LCDM ~09:15, PURE ~10:45, score right after. The original runner will log
"D355 score FAILED" when LCDM ends (no PURE result yet); that is expected, and the D2 runner scores afterwards.

**D361 (pp, 08:05 CT, TWIST-I (a'): adiabatic capture) — Linde's adiabatic mechanism does not apply directly; the right criterion is the
kinetic share of x at capture (literature + estimate; aegis-checked in code).**
Read: "Relaxing the cosmological moduli problem by adiabatic suppression" (arXiv:1109.2073). With a Hubble-induced mass cH (c ≳ 30), the
modulus tracks its moving minimum and the relic is suppressed exponentially in c. But: (i) the field must sit in a Hubble-induced minimum
throughout; (ii) the minimum must not move faster than the curvature; (iii) a finite-H start leaves power-law residuals. "The adiabatic solution
does not work" if the curvature vanishes temporarily or the minimum jumps.
For TWIST-I: x is the inflaton and then a rolling field, so it is never in a heavy Hubble-tracked minimum before capture, and condition (i)
fails. Reframing (this corrects D359/D360a's static-displacement picture): a field arriving with velocity φ̇ in a well of mass m ≫ H keeps
an oscillation amplitude ≈ φ̇/m, so ρ_osc/ρ_tot ≈ Ω_kin,x at capture, independent of m. The dilution is then Δ ≈ Ω_kin,x · T_arr/T_decay(m).
Δ ≤ 1 needs Ω_kin,x < 1×10⁻¹⁰ (m = 10⁹ GeV), 1×10⁻⁷ (10¹¹), 1×10⁻⁴ (10¹³), 3.5×10⁻³ (10¹⁴), 0.1 (10¹⁵ GeV) (T_arr = 2×10¹³ GeV).
So the realistic TWIST-I is a very heavy stabiliser (m_x ≳ 10¹⁴–10¹⁵ GeV, decaying almost at once), with x slow (Ω_kin ≲ 10⁻³–10⁻¹) when captured.
Next check: x's kinetic share at T ≈ 2×10¹³ GeV in the v5 matter run (hidden_kick_decay_v2.py tracks x; its output gives the fraction).
A heavier stabiliser also means m_x near the inflaton/heavy-scale range. Is the cliff itself the stabiliser? That is open.
Status: TWIST-I open item (a') is restated: "a ≳ 10¹⁴ GeV stabiliser capturing a slow x at x ≈ 30".

**D362 (pp, 08:12 CT, TWIST-I (a') follow-up: x's kinetic share at freeze-out, and what capture really needs) — kinetic energy is harmless if
capture is late; the real cost is a ~10⁻⁶ M_P TUNING of the minimum's position (estimate; aegis-checked in code; corrects the emphasis of
D361).**
(1) The kinetic share (estimate from the v5 background: f_heat 0.65–0.8% at H_end = 5.2×10¹² GeV, then kination): radiation equals x's kinetic
energy at a/a_end ≈ 11–12. At T = 2×10¹³ GeV, Ω_kin,x ≈ 0.13–0.17, or ≈ 0.02 after the ×4.6 entropy from σ decay (D277). It falls as T² after that.
With D361's Δ ≈ Ω_kin(T_c)·T_c/T_d ∝ T_c³, capturing later always works for the kinetic part. For example, m = 100 TeV needs T_c ≲ 2×10⁸ GeV;
m = 10¹³ GeV needs T_c ≲ 2×10¹² GeV. D361's "m ≳ 10¹⁴ GeV" was too strict for this part.
(2) But a field captured by a minimum also carries the potential energy of its offset from that minimum, ½m²Δφ² (D360a). Falling into a
well, or a well forming around the field away from x's resting point, gives oscillations of that size. In the radiation era a freely rolling
x comes to rest at a definite x_∞ (Hubble friction), so the stabiliser's minimum must coincide with x_∞ to within the D360a bound:
Δφ ≲ 2×10⁻⁷ M_P (m = 100 TeV) to ~10⁻⁶–10⁻⁵ M_P (10⁹–10¹³ GeV). The overdamped variant (well present while H ≫ m) does not help: the offset
is not relaxed before H ≈ m and gives the standard moduli problem. Linde's exponential suppression needs the field in the minimum from the start
(D361).
Verdict: TWIST-I costs a positional tuning of x_min to x_∞ at the 10⁻⁷–10⁻⁵ M_P level, unless a mechanism ties the minimum to x's own resting
point (none known). This is a third tuning besides Λ and n, and it should be stated in v6 item 18. D359–D361's statements are folded into this one.

**D363 (pp, 08:17 CT, TWIST-I: a mechanism that ties the minimum to where x stops?) — moduli trapping at enhanced symmetry points is the
natural candidate (literature, abstract only; not yet checked quantitatively).** Kofman, Linde, Liu, Maloney, McAllister & Silverstein,
"Beauty is attractive: moduli trapping at enhanced symmetry points" (hep-th/0403001; abstract read, the HTML did not render): particles that
become light at special points of moduli space are produced as a modulus rolls through, and their back-reaction (a confining potential
∝ g|φ − φ_ESP| n_χ) traps the modulus at that point. In an expanding universe, Hubble friction limits how far it rolls. The authors say trapping
"ameliorates" the moduli problem. A follow-up with higher-dimensional couplings: arXiv:1310.4751.
For TWIST-I this would replace the 10⁻⁶ M_P positional tuning (D362) with a dynamical one. x would be trapped at an enhanced symmetry point
x_ESP ≥ 30 that it rolls through after matter genesis, and the oscillation energy would go into the produced χ particles, which decay to radiation.
Conditions to check: (i) an ESP exists on the Twist's field range (the cliff region is a natural place: the cliff condensate/instanton sector
changes there); (ii) trapping must happen after freeze-out, with residual oscillations damped by particle production rather than left as a
coherent modulus; (iii) χ must decay before BBN; (iv) at the trapped point x must still get a mass, since trapping alone gives a linear,
n_χ-dependent potential that dilutes. Possible caveat: as n_χ dilutes, the trap weakens and the modulus can drift again unless a true
minimum exists at the ESP (the usual statement is that trapping holds the field long enough for other effects to stabilise it).
Status: TWIST-I open item (a') becomes "an ESP at x ≳ 30 plus a stabilising minimum there". This is a mechanism to evaluate, not a solution.

**D364 (pp, 08:22 CT, D363 follow-up: does ESP trapping meet D362's 10⁻⁷–10⁻⁵ M_P bound?) — plausibly yes, and symmetry removes the
positional tuning (estimate; standard trapping formulas, aegis-checked in code).** Trapping: when x passes the ESP, χ particles with mass
g|Δφ| are produced, n_χ ≈ (gφ̇)^{3/2}/(2π)³, and the field stops within d ≈ φ̇²/(2g n_χ) of the ESP. With x's kinetic share
Ω_kin ≈ 0.02 (T_c/2×10¹³ GeV)² (D362) and φ̇ = √(6Ω_kin) H M_P:
- T_c = 10¹² GeV: d ≈ 1.2×10⁻⁵ M_P (g = 1), 3.9×10⁻³ (g = 0.1).
- T_c = 10¹⁰ GeV: 1.2×10⁻⁸ (g = 1), 3.9×10⁻⁶ (g = 0.1).
- T_c = 10⁸ GeV: 10⁻¹¹ to 4×10⁻⁹.
So trapping at T_c ≲ 10¹⁰ GeV with g ≳ 0.1 lands x within D362's bound.
Key point: at an enhanced symmetry point, the stabilising potential is stationary by symmetry, so its minimum sits exactly at the ESP if it
is a minimum rather than a maximum. The 10⁻⁶ M_P coincidence of D362 then becomes a property of the symmetry, not a tuning. The kinetic energy
goes into χ, which must decay to radiation before BBN, and is harmless because capture is late (D362).
Revised TWIST-I requirement (replacing D362's tuning): an ESP on the Twist range at x ≳ 30, crossed at T ≲ 10¹⁰–10¹² GeV, with coupling g ≳ 0.1
to some χ, and a stabiliser for which the ESP is a minimum (m ≳ 100 TeV for BBN). All of this is model building, with no tuning of positions.
Not yet checked: whether x actually still rolls at those temperatures (in v5 it keeps thawing to today, so yes); and the n_B/s and DM
dilution from χ decay (≈ Ω_kin at capture, ≲ 10⁻⁴: negligible).

**D365 (pp, 08:27 CT, D364 follow-up: is there an ESP at x ≳ 30?) — not in standard moduli spaces; one can be added by a χ sector, and then
the minimum is at the ESP by structure (argument; rough mass estimate).**
(1) Standard ESPs of an SL(2,Z)-type T-modulus are the self-dual points T = 1 and T = e^{iπ/6} (x ~ 1), far below x ≳ 30. Large x is the
decompactification direction, where the "light particles" are a whole tower (the distance conjecture, D-notes on the string search), not a trap.
So the Twist's own moduli space offers no ESP at x ≳ 30.
(2) An ESP can be added: W ⊃ λ M_P (T − T_E) χχ̄ makes χ massless at T = T_E. That gives trapping there (D364) for x_E inside x's remaining roll
range. Its position is a parameter, not a 10⁻⁶ tuning: trapping puts x at T_E, and any potential generated by the χ loop depends on
|m_χ|² ∝ |T − T_E|², so it is stationary exactly at T_E.
(3) Whether T_E is a minimum, and how heavy x is there, depends on SUSY breaking. With the D292 soft scale m_soft (gauge mediation,
~10⁴–10⁵ GeV), a one-loop CW term gives roughly m_x ~ (λ/4π) m_soft × O(x) after canonical normalisation. That is ~10⁴–10⁵ GeV for λ ~ 1,
x ~ 50, so borderline against the ≳ 100 TeV BBN requirement (D357). Rough; the sign (minimum versus maximum) is not computed.
(4) Cross-check with the shield: once trapped, x is frozen, so the χ sector reintroduces no drift. χ itself must not couple to SM gauge groups
with x-dependent thresholds after trapping. It does not matter, because x no longer moves.
Verdict: TWIST-I's capture problem reduces to a specific, testable piece of model building (a χ sector with an ESP at x_E ≳ 30, λ ≳ 1, and
a minimum there from SUSY-breaking loops). The remaining number to compute is the CW mass and its sign; it needs a lock before it is called a
prediction. Status: the open item stays open but is now concrete.

**D366 (pp, 08:32 CT, D365's open point: is the added ESP a minimum, and how heavy is x there?) — likely a MAXIMUM; the ESP route needs one
more ingredient (argument from a standard result; not a locked computation).**
With W ⊃ λ M_P (T − T_E) χχ̄, near the ESP the canonical displacement δ of x gives χ a supersymmetric mass ∝ λ δ. If χ feels SUSY breaking
through soft masses m̃_χ² > 0 (needed for any one-loop potential; an SM- and messenger-neutral χ gets none in gauge mediation, and with an eV
gravitino its gravity-mediated soft mass is ~eV, so the potential vanishes), then a Yukawa-coupled field gets a NEGATIVE one-loop mass², the same
mechanism as radiative electroweak breaking from the top loop: δm_x² ≈ −(N λ²/8π²) m̃_χ² ln(Λ/m̃_χ). The ESP is then a local MAXIMUM of the
loop potential, unless x has its own positive mass there of at least that size. x's own tree-level soft mass is ~m_3/2 ~ eV, via K ⊃ |X|²|ΔT|²,
which is far too small.
Consequences: (i) trapping at the ESP still happens (particle production), but once n_χ dilutes, x would roll off the maximum. (ii) A minimum at
the ESP needs either χ with negative soft mass² (unusual; tachyonic χ), or a separate positive x mass ≳ (λ/2π)m̃_χ at the ESP from another
sector, with its minimum at T_E. That reintroduces the positional coincidence of D362, unless that sector shares the symmetry fixing T_E.
Verdict: the ESP route does not by itself give a stabilised TWIST-I. A Z₂ or larger symmetry that fixes T_E in all sectors (both χ and the
stabiliser) would. Status: TWIST-I capture is still open, now sharply stated: "a symmetry point at x ≳ 30 respected by the stabilising sector,
with net positive curvature there, ≳ 100 TeV". Correction to the optimism of D364–D365 (the trapping numbers stand; the minimum does not
follow).

**D367a (08:12 CT, compute plan; Danny: "Schedule all needed compute").** Needed compute and where it runs:
(1) D355 free-ν fits (PC): LCDM running, PURE rerun queued (D2), score due ~10:45.
(2) D360 T1 isocurvature at the alternative fit point (cloud): two runs, started 07:57, due ~09:30–10:00.
(3) D367 x kinetic share from the v5 matter run (cloud): locked. It starts when the T1 runs free the cloud cores (a background job is
capped at 2 h, so the pp loop launches it then), and is due ~2.5 h after start.
(4) D366's sign question (is the ESP a minimum?) is settled by the standard radiative argument, so no compute is needed unless a model is chosen.
(5) TWIST-I N* shift: none if capture is late and adiabatic (D362: dilution ≪ 1), so no compute is needed.
No other open item needs compute now. The free-ν fit already covers TWIST-I's ΛCDM background (its LCDM half).

**D368 (pp, 08:15 CT, TWIST-I distinctiveness check) — under TWIST-I, the inflationary predictions coincide with Starobinsky's at the same
N* (arithmetic, aegis-checked in code).** Starobinsky/α = 1 attractor: n_s = 1 − 2/N*, r = 12/N*². For the Twist's N* = 55.7–57.6: n_s
0.9641–0.9653, r 0.0039–0.0036. The Twist's computed values are n_s 0.9642–0.9654, r 0.0035–0.0038, the same within 10⁻⁴ in n_s and 0.0003 in r.
So the TWIST-I rules on r and n_s (PREREG_TWISTI 1–2) test "α = 1 plateau with this N*", not the Twist specifically. A Starobinsky model with the
same reheating would pass and fail identically.
What still distinguishes TWIST-I: (i) the N* window itself, fixed by the Twist's reheating (f_heat 0.65–0.8%, T_RH 5.5–5.8×10¹⁴ GeV, and kination
after inflation). Starobinsky's usual N* is 51–55 with gravitational reheating, so the Twist predicts the HIGH end, n_s ≈ 0.965 rather than
0.961–0.964. (ii) Matter genesis through the angle, and its isocurvature (D278, D320b). (iii) The DM window (~100–200 TeV, D341). (iv) β = 0, w = −1.
Consequence for v6 item 18: say plainly that TWIST-I's CMB predictions are Starobinsky-class at high N*. The distinguishing content is
N* ≈ 56–58 (testable through n_s at the ±0.0015 level with SO, D351) and the matter/DM sector. This is an honest narrowing, not a failure.

**D369 (pp, 08:20 CT, checking D368's "Starobinsky usual N* 51–55" claim) — partly corrected; the Twist's distinctive point is stronger
than stated (literature, abstract).** "Refined predictions for Starobinsky inflation and post-inflationary constraints in light of ACT"
(arXiv:2504.20757): with refined (non-analytic) predictions, Starobinsky is consistent with ACT at 2σ only for N* ≳ 58. That needs a
stiff reheating equation of state, ω ≳ 0.462 (perturbative reheating, ω ≈ 0, is excluded). With ω ≤ 1, T_rh ≲ 2×10¹⁰ GeV; 1σ with ACT needs
0.8 ≲ ω ≤ 1 and 4 MeV ≲ T_rh ≲ 10 GeV.
Correction to D368: "the usual N* 51–55" was from memory; the relevant literature statement is that standard (perturbative) reheating gives
too low an N* for ACT, and reaching N* ≳ 58 requires a kination-like phase. The Twist's post-inflation history IS a kination phase (f_heat
0.65–0.8%, D362: x's kinetic energy dominates until a/a_end ≈ 11–12), with T_RH ≈ 5.6×10¹⁴ GeV. So the Twist naturally realises the stiff, ω → 1,
high-N* history that ACT-compatible Starobinsky needs, though at a much higher T_RH than that paper's 1σ window (its bound T_rh ≲ 2×10¹⁰ assumes
the reheating phase ends at T_rh; in the Twist, radiation coexists with kination from the start). Not directly comparable; an N* comparison in
the paper's conventions would need their formulas (not read).
D368's conclusion stands and strengthens: TWIST-I's CMB distinctiveness is its N* via its built-in kination. That is a real model-specific
statement worth putting in v6 item 19.

**D370 (pp, 08:24 CT, self-check of D369; aegis-check like-with-like) — D369 overstated the match. The Twist's kination gives N* 55.7–57.6,
just BELOW the N* ≳ 58 that refined Starobinsky needs for ACT at 2σ.** The Twist's own N* (TWIST-K table: 55.7 instant, 57.6 with the 0.65–0.8%
heat share) already includes its kination phase, and its n_s 0.9642–0.9654 is what the NS-SPA test found INCONSISTENT with SPA + DESI. So the Twist
has a stiff post-inflation phase of the kind that raises N*, but not enough of it: it falls ~0.5–2 e-folds short of the ACT-preferred region
(n_s ≥ 0.966 needs N* ≳ 59 in the attractor formula 1 − 2/N*; aegis-checked: 1 − 2/59 = 0.9661). This is consistent with gap 1 (HIGH) and with
D329 (the tension is background-conditional).
Correction: v6 item 19's added clause is softened to "the Twist's built-in kination raises N* toward, but not into, the ACT-preferred range
(N* ≳ 58)". The distinctive content is still N* through its reheating history; the direction of the n_s tension is unchanged.

**D371 (pp, 08:45 CT, D366 follow-up: does finite temperature save the ESP?) — only until T ~ m̃_χ; a zero-temperature stabiliser is still
needed (standard finite-T result; order-of-magnitude, aegis-checked in code).** In the thermal bath, χ gives x a positive thermal mass²
~ λ²T²/6 around the ESP, so the ESP is a thermal minimum. That beats the negative radiative (CW) term ~ (λ²/8π²) m̃_χ² ln(Λ/m̃_χ) while
T ≳ m̃_χ. For λ = 1 and m̃_χ = 10⁵ GeV: thermal wins at T = 10¹⁰ and 10⁶ GeV, and CW wins at T = 10⁴ GeV. So thermal effects hold x at the ESP
from trapping down to T ~ m̃_χ (≈ 10⁴–10⁵ GeV), well before BBN. Below that, the ESP turns into a maximum unless the stabiliser of D366 is
present. Consequence: the time the stabiliser has to act is late (T ≲ m̃_χ), so its mass only needs to exceed H at that time (trivially true
for ≳ 100 TeV). The positional match still comes from the symmetry. No change to the TWIST-I open item; it is narrowed to "zero-temperature
symmetric stabiliser at the ESP".

**D372 (pp, 08:50 CT, can "minimum at the ESP by symmetry" be exact in a no-scale theory?) — no; the no-scale e^K tilts any reflection-
symmetric stabiliser, but the shift is small if the stabiliser is sharp (estimate, aegis-checked in code).** The Twist's K = −3 ln(T + T̄)
is not symmetric under a reflection about T_E, and in canonical units the factor e^K ∝ x⁻³ has slope 3√(2/3) ≈ 2.45. A stabiliser of depth
~m_x² w² over a canonical width w therefore gets a linear tilt ~2.45 m_x² w², which moves its minimum off the ESP by Δφ ≈ 2.45 w² (M_P = 1):
w = 0.1 M_P gives Δφ ≈ 2×10⁻², w = 10⁻² gives 2×10⁻⁴, and w = 10⁻³ gives 2.4×10⁻⁶ M_P. D360a/D362 need Δφ ≲ 10⁻⁷–10⁻⁵ M_P, so the stabiliser
must be SHARP: canonical width ≲ 10⁻³ M_P (≈ 2×10¹⁵ GeV in field space), or its sector must sit at a modular weight that removes the e^K
tilt, as in the D292 weight-3 trick. The weight route is natural in the Twist framework (D292 already uses it), so the symmetric stabiliser
should be built with x-independent normalisation; then the tilt vanishes at tree level. Loop-level tilts (D323) would then set the residual.
Status: TWIST-I's capture item is now "a sharp (≲ 10⁻³ M_P) or weight-neutral symmetric stabiliser at an ESP x ≳ 30". This is still model building.

**D373 (pp, 08:55 CT, a weight-neutral symmetric stabiliser, as suggested in D372) — exists at tree level, and is exactly untilted, but a
global one causes its own moduli problem; it must be localised (computed, sympy; theory/review/weight3_stabiliser_d373.py).**
Construction: a stabiliser field Y at modular weight 3, K ⊃ |Y|²/(T + T̄)³, with W ⊃ k Y (T − T_E). Exact result at Y = 0:
**V = k²|T − T_E|²**. The e^K factor cancels against K^{YȲ}, so there is no tilt, and the minimum is exactly at T = T_E (D372's problem is solved
at tree level). The canonical mass is m_x² ≈ (4/3) k² x_E² (M_P = 1). Y must get its own mass, since it is flat at T = T_E; W ⊃ ½ m_Y Y² will do.
Problem (aegis-check, cross-sector): a GLOBAL quadratic V is present along the whole roll. For m_x = 100 TeV it is ~10⁻²⁷ M_P⁴ at x ≈ 0,
negligible during inflation (~10⁻¹¹), but larger than radiation for T ≲ 10¹¹ GeV. x would then be pulled in and oscillate with an O(1)
energy share, which is the D359 moduli problem again. So g(T) must be LOCALISED: flat far from T_E and steep near it. For example
g = k(T − T_E) times a factor that switches off for |T − T_E| ≫ w with w ≲ 10⁻³ M_P, or a ζ-type higher-order K term. Weight 3 removes the tilt
whatever the shape.
Status: TWIST-I capture now has a concrete tree-level skeleton: an ESP-trapping χ sector, plus a localised weight-3 stabiliser Y with
W ⊃ Y g(T) and g(T_E) = 0. It is untilted, its minimum is exact at T_E, and it decays before BBN if m ≳ 100 TeV. Open: the origin of a localised
g(T) and of T_E; loop-level tilts (D323-type) on the minimum.

**D374 (pp, 09:00 CT, D373 open point: do loops tilt the weight-3 stabiliser's minimum?) — negligibly, in the eV-gravitino branch (estimate,
aegis-checked in code).** A one-loop vacuum term tilts the minimum only through fields whose masses depend on x and whose boson–fermion
splitting is non-zero (STr M⁴ ln M²). (i) Weight-neutral sectors (the D292 SUSY-breaking sector and messengers, χ at weight 3/2, Y) have
x-independent masses: no tilt. (ii) The χ trapping sector depends on |T − T_E|², which is stationary at T_E: no tilt. (iii) Heavy sectors with
x-dependent masses (e.g. the inflaton partner S, m_S ~ 10¹⁰–10¹³ GeV) are split only by gravity-mediated SUSY breaking, ~m_3/2 ~ eV, which
gives a tilt ~ m_S² m_3/2²/16π² and a minimum shift ~10⁻⁴⁷–10⁻⁴¹ M_P for m_x = 100 TeV. That is utterly negligible. (iv) The SM itself: the
D323 drift concerns couplings, not the vacuum energy at the minimum; once x is frozen there is no drift. Its vacuum loop is x-independent
through the D292 weights, up to the same −b_a/4π threshold effect, which shifts SM loop energies by ~(m_soft⁴/16π²)×7×10⁻³ per unit ln x.
That gives a tilt ~10¹¹–10¹⁵ GeV⁴/M_P (m_soft = 10⁴–10⁵ GeV) and a shift ≲ 10⁻³¹ M_P (recomputed). Also negligible.
Verdict: at loop level the stabiliser minimum stays at T_E to far better than the 10⁻⁷ M_P needed. TWIST-I's capture skeleton (D373) is
consistent at one loop. What is still open is model building only: where a localised g(T), T_E and the χ sector come from.

**D375 (pp, 09:05 CT, tying the ESP and the stabiliser minimum together) — one shared factor (T − T_E) does it without any symmetry or
localisation (argument + D373's exact result; aegis-checked).** Let the trapping sector and the weight-3 stabiliser come from the same
factor: W ⊃ (T − T_E)(λ M_P χχ̄ + k Y). Then χ is massless exactly where the stabiliser minimum is (V = k²|T − T_E|², D373), so trapping (D364)
puts x at the stabiliser minimum up to the trapping distance d ≲ 10⁻⁸–10⁻⁵ M_P. There is no positional coincidence to tune, and no reflection
symmetry or sharp localisation is needed: the zero of a single holomorphic factor fixes both.
Global-well energy: before trapping, a global k²|T − T_E|² can dominate radiation (T ≲ 10¹¹ GeV for m_x = 100 TeV, D373) and accelerate x.
That kinetic energy goes into χ particles at the ESP, which decay to radiation at once rather than into a long-lived coherent modulus. The
cost is an O(1) entropy release at T_c (dilution ≲ (1 + Ω)^{3/4} ~ 2), not 10³–10¹³. This assumes trapping is efficient (g ≳ 0.1) and χ decays
promptly. To be checked if TWIST-I is built: whether the matter yield (1.25× observed) tolerates a factor ~2.
Radiative stability (D366): the stabiliser's positive m_x² = (4/3)k²x_E² must exceed the χ-loop negative term (λ²/8π²) m̃_χ² ln(Λ/m̃_χ), i.e.
m_x ≳ 6×10⁴ GeV for λ = 1, m̃_χ = 10⁵ GeV (computed). That is consistent with the ≳ 100 TeV BBN requirement.
Status: TWIST-I's capture problem now has a consistent tree + one-loop skeleton with a single new parameter set (T_E, k, λ, and the χ, Y masses)
and no fine-tuning. The open items are its origin (UV) and the factor-~2 dilution against the matter yield. This upgrades D362–D366.

**D376 (pp, 09:10 CT, D375's open point: can the matter and DM yields absorb TWIST-I's capture dilution Δ ~ 1.5–3?) — yes, by refits;
it moves two numbers (estimate from known scalings; aegis-checked in code).**
(1) Matter: the yield scales as m_σ^−0.89 (D297), and exact 1× observed sits at m_σ ≈ 7.5×10¹⁰ GeV (canonical reading). A dilution Δ is absorbed
by m_σ → 7.5×10¹⁰ Δ^{−1/0.89}: Δ = 1.5 gives 4.8×10¹⁰, Δ = 2 gives 3.4×10¹⁰, Δ = 3 gives 2.2×10¹⁰ GeV. m_σ is the one fitted input, so this is a refit,
not a failure. The isocurvature sensitivity was ~3.7 at both m_σ values tested so far (D277, D320b; D360 T1 at 3×10¹⁰ is pending), so the margin
should hold.
(2) Dark matter: the gravity-only fermion's yield is mass-independent (D112), so Ω ∝ m_DM/Δ and its mass rises by Δ: 100–200 TeV becomes
150–300 (Δ = 1.5) or 200–400 TeV (Δ = 2). That pushes it into the region where an O(1) gravity-portal coupling is excluded (D341: ξ ~ 1 survives to
~200 TeV). The candidate still survives with ξ ≪ 1 or a gauged stabilising symmetry (ξ = 0, D318). The decay signal becomes less likely, and
the DM itself is unaffected.
Status: TWIST-I's capture skeleton (D375) is consistent with the matter and DM sectors after refits. Recorded consequences: m_σ moves down by
up to ×2–3, and m_DM moves up by Δ.

**D377 (pp, 09:15 CT, cross-sector check of D375: does the χ trapping sector disturb inflation or the EFT?) — only for a window of the
coupling (estimate; aegis-checked in code).** Put χ, χ̄ at modular weight 3/2 each, so their physical mass is x-independent apart from
the factor: m_χ = λ M_P |T − T_E|. During inflation (x ≈ 10⁻⁴, T_E ≈ 30) that is ≈ 30λ M_P, so staying below M_P needs λ ≲ 1/30 ≈ 0.033.
Trapping efficiency near T_E needs a canonical coupling g = λ x_E √(2/3) ≳ 0.1, so λ ≳ 0.004. Window: **0.004 ≲ λ ≲ 0.033** (for x_E = 30).
Inflation: χ is heavy (≫ H), and its Hubble-split one-loop term is ~2λ²(30)²H²M_P²/16π² relative to... i.e. CW/V_inf ~ 7×10⁻⁵–4×10⁻³
across the window, with a slope ∝ x/x_E ~ 10⁻⁵ at the CMB point. That is negligible for n_s and r. The Y stabiliser contributes
k²|T − T_E|² ~ 10⁻²⁷ M_P⁴ (k ~ 10⁻¹⁵), also negligible.
Verdict: the D375 skeleton is consistent with inflation and the EFT for 0.004 ≲ λ ≲ 0.03. TWIST-I's capture sector is now a bounded, consistent
proposal: T_E ≳ 30, λ in that window, k from m_x ≳ 10⁵ GeV, χ and Y at weights 3/2 and 3.

**D378 (09:20 CT) — TWIST-I capture consolidated in papers/twist_v5/TWISTI_CAPTURE.md (D355–D377).** No new physics; this is one place for the
construction W ⊃ (T − T_E)(λ M_P χχ̄ + k Y) (χ at weight 3/2, Y at weight 3), its bounds, its consequences and its open items.

**D379 (pp, 09:25 CT, status + one candidate origin for (T − T_E)).** Status: D355's LCDM fit has 3 of 4 minimiser runs converged; PURE is
still waiting. D360 T1 is still running. Candidate UV origin (idea, not checked): in D-brane language, χ would be strings stretched between
two branes whose separation is tied to T, so m_χ ∝ |T − T_E| arises when the branes coincide at T = T_E. That is the setting of the original
trapping paper (hep-th/0403001, D363). A Twist-specific realisation would need the brane separation to be a function of the same modulus
whose −3 ln K drives inflation (e.g. a D3/D7 position combined with the volume, K = −3 ln(T + T̄ − |φ|²) type). This is listed as the first
place to look for the UV origin; not pursued further here.

**D380 (pp, 09:30 CT, quick check of D379's brane idea) — inconclusive, mild negative (search only).** The standard place where a D3 position
sits inside the no-scale log, K = −3 ln(T + T̄ − |φ|²) (KKLMMT-type; e.g. the reviews arXiv:0708.2865 and 1108.2659), has the brane separation as a
SEPARATE field φ, not the volume T. In the Twist, the rolling field is Re T, so m_χ ∝ |T − T_E| would need the separation to be locked to T,
which is not automatic. A route where φ is the rolling field changes the Twist's construction (its −3 ln structure comes from T). Not
pursued; the UV origin of (T − T_E) stays open.

**D381 (pp, 09:35 CT, run-risk check) — D360 T1 may hit the cloud 2-hour cap.** Its two runs were started at ~07:52 CT. The comparable D320
single run took 1 h 56 min. The cloud background cap is 2 h, so T1 is due ~09:48–09:52 with a hard stop at ~09:52. If it is killed, that is
recorded as a crash (no result), and a crash rerun under a deviation will be proposed with a split plan (e.g. one run per session slot, or
on the PC). Not a result-chasing rerun.

**D367a (08:55 CT, PRELIMINARY reading of the locked D367 run; segments 1–3 to N − N_e = 9.4; not yet scored, since the validation at
N − N_e = 11 is still pending).** From seg1, v5 matter-run background (m_σ 5.8×10¹⁰, heat 0.8%):
T = 2.19×10¹³ GeV: Ω_kin,x = 0.741, x = 3.09. T = 8.2×10¹²: Ω_kin 0.24, x 12.7. T = 1.7×10¹²: Ω_kin 2.2×10⁻³, x 27.2. T = 1.5×10¹¹: Ω_kin 1.5×10⁻⁵,
x 29.6. n_B/s settles to ≈ 1.10×10⁻¹⁰ by T ≈ 2×10¹¹.
Two corrections to D362 follow, if confirmed. (1) Ω_kin,x at 2×10¹³ GeV is ≈ 0.74, not 0.02–0.17 (D362 ignored the potential-driven roll down
the cliff), which is outside ×3, so the rule will read FAILED. (2) More important: x is only ≈ 3 at matter freeze-out and reaches ≈ 30 only at
T ≈ 10¹¹–10¹² GeV, when Ω_kin,x ≈ 10⁻⁵–10⁻³. D355/D356's "x ≈ 30 at freeze-out" was wrong. The matter yield keeps evolving until
T ≈ 10¹² GeV (σ entropy), so capture at x_E ≳ 30 automatically happens late (T_c ≲ 10¹² GeV), with Ω_kin ≲ 10⁻³. That makes D362's
"capture late" condition automatic for x_E ≳ 30. The D375 trapping-plus-stabiliser skeleton then sees a small kinetic share, and the global-well
issue becomes the main source of capture energy. To be finalised in D367b.

**D382 (pp "research gaps", 09:30 CT, gaps 10 and 13 under TWIST-I: what happens to the Twist angle y?) — the angle becomes heavy, which
removes two old costs (argument from D373's exact potential).** The weight-3 stabiliser gives V = k²|T − T_E|² = k²[(x − x_E)² + y²]
(D373), so after capture the angle y gets the same mass as x, ≳ 10⁵ GeV, and decays with it before BBN.
(1) Gap 10 (strong CP): the v5 cost "the angle would overproduce axion dark matter by ~4×10⁵" assumed a light, long-lived angle acting as the
QCD axion. Under TWIST-I the angle is not a light axion today, so it cannot be the QCD axion and cannot overproduce. The cost becomes simply
"strong CP is not addressed; a separate post-inflation QCD axion (40–600 μeV, ALPHA/MADMAX) would be needed". It is the same requirement,
without the overproduction tension.
(2) Gap 13 / D298–D300 (the eV-branch angle relic, 12–28% of DM, and the D356 x_min ≳ 50 bound): moot under TWIST-I, since a heavy angle
decays and leaves no relic. D356's bound is withdrawn for the D375 construction.
(3) Matter genesis is unaffected: the angle's dynamics that make n_B/s happen at T ≳ 10¹² GeV, before capture (D367a: x reaches ~30 only at
T ~ 10¹¹–10¹²). Birefringence (β = 0, TWIST+ALP fallback) is also unaffected.
Status changes under TWIST-I: gap 10 is unchanged in severity (LOW–MEDIUM) but loses its overproduction clause; the D298–D300 relic item is closed.
To go into v6 item 18.

**D383 (pp, 09:40 CT; locked PREREG_D383 + D1 bug fix; results/n_twisti_d383.txt) — CORRECTION: TWIST-I need not give up "Λ from the
cliff".** The D373 stabiliser has V = 0 at its minimum, so the vacuum energy after capture is the Twist potential at x_E,
Λ = V_Twist(x_E) ∝ e^{−2n}/(1 + x_E/μ). That is the same mechanism as v5, evaluated at x_E ≈ 30 instead of today's x ≈ 89. Then n shifts by
Δn = ½ ln(90/31) = 0.533 (n ≈ 124.1 instead of 124.6). Effect on inflation: n_s 0.96497 and r 0.00359 for both n (computed); a sanity check gives
n = 100 vs 125 → Δn_s = 3×10⁻⁶. The attractor makes n_s and r insensitive to n. (The first run printed identical numbers because of a runpy
globals bug, fixed in deviation D1 before reading.)
So TWIST-I explains Λ exactly as v5 does (cliff depth e^{−2n} at the captured value, with the same D292 constant tuned to ≪ Λ). What it gives
up is the thawing tail (w = −1 exactly), not Λ itself. Statements in D355, D378, TWISTI_CAPTURE.md and v6 item 18 ("gives up Λ from the cliff",
"Λ is a free tuning") are corrected.

**D384 (pp, 09:45 CT, the capture energy budget using D367a's actual trajectory) — capture can be almost free (Δ ≈ 1 + O(10⁻³)) if x_E
lies inside the range x actually crosses; this corrects D375/D376's Δ ~ 2 (estimate, aegis-checked in code).**
With m_x = 10⁵ GeV and x_E = 30, k = 1.2×10⁻¹⁵, the global well's energy relative to radiation along the computed roll is:
4×10⁻⁹ (T 2.2×10¹³, x 3.1), 1×10⁻⁶ (1.7×10¹², x 27.2), 5×10⁻⁴ (1.5×10¹¹, x 29.6), 1×10⁻² (5×10¹⁰, x 29.7).
Key fact from D367a: x converges to x_∞ ≈ 29.8 (dp falls ~×0.6 per half e-fold). So:
- If x_E ≳ x_∞ (e.g. 30), x never reaches T_E by itself. The well has to pull it in once V_stab ~ ρ_rad (T ~ 2×10¹⁰ GeV), giving an O(1) energy
  release (Δ ~ 2, as D375 assumed).
- If x_E is crossed during the roll (x_E ≲ 29.5, crossed at T ~ 10¹¹–10¹² GeV), trapping happens with Ω_kin,x ~ 10⁻⁵–10⁻³ and V_stab/ρ ≲ 5×10⁻⁴,
  so Δ ≈ 1 + O(10⁻³).
Revised recommendation: take x_E ≈ 27–29.5 (crossed at T ≈ 10¹¹–2×10¹² GeV, after the matter yield has settled, D367a). Then D376's refits are
unnecessary: m_σ stays at the v5 fit and m_DM stays at 100–200 TeV. The D383 n shift is essentially unchanged (Δn = ½ ln(90/(1 + x_E)) ≈ 0.54–0.58).
TWISTI_CAPTURE.md and v6 item 18 are updated accordingly. Final numbers wait for D367b (validation pending).

**D360b (T1 scored, locked PREREG_D360_TESTS; results/alt_isocurv_d360_base.txt and _s105.txt; both exit 0, finished before the 2 h cap) —
PASS, with a larger margin.** At the alternative reading's fit point m_σ = 3.0×10¹⁰ GeV: Y_alt(base) = 7.915×10⁻¹¹ (0.910× observed, inside the
0.5–2× "fit point" window); Y_alt(σ₀ × 1.05) = 8.394×10⁻¹¹; **S_alt = 1.205 ≤ 5 → PASS**. Margin at f = 0.1 M_P: 5.1/1.205 = **4.2×**. The same
runs give a canonical-reading sensitivity of 1.19 at m_σ = 3×10¹⁰ (yield 2.04× observed there).
Reading: the yield's sensitivity to σ₀ depends on m_σ. It is ≈ 3.7 at 5.8×10¹⁰ (D277, D320b) and ≈ 1.2 at 3.0×10¹⁰, so the isocurvature
margin grows from 1.4× to 4.2× at the lower mass. This is relevant to D376: a lower m_σ, if ever needed, would improve the isocurvature margin.
D320's stated limitation is closed. Gap 7: LOW–MEDIUM → LOW at the alternative fit point. The canonical fit point (m_σ ≈ 7.5×10¹⁰) keeps the
~1.4× margin.

**D355b (scored, locked PREREG_D355_MNU_FREE + D1–D2; field_tests/results/d355_mnufree.json; scored 09:51 CT on the PC) — TIGHTER.**
On the NS-SPA data set (n_s free): with the PURE Twist tail, χ² is 2405.554 at Σm_ν = 0.06 and 2400.332 with m free (best m = 0.001 eV, the prior edge),
so P_PURE = 5.222. For ΛCDM, χ² is 2404.102 and 2402.232 (best 0.016 eV), so P_ΛCDM = 1.870. **D = 3.352 > 1 → TIGHTER** (aegis-check:
recomputed). The thawing tail penalises the minimal normal-ordering neutrino mass by Δχ² ≈ 5.2 (~2.3σ), against 1.9 (~1.4σ) for ΛCDM: it
tightens the neutrino bound, as expected for w > −1 dark energy (D337). This is a sensitivity on already-used data, not evidence.
Consequences: (1) under the adopted TWIST-I (Λ, w = −1), the relevant penalty is ΛCDM's 1.9, so gap 14 is unchanged for the adopted model;
(2) the original tail (the conditional variant) carries an extra neutrino-mass cost of ΔD ≈ 3.4. That is one more cost of the tail, alongside
the shield no-go and the H₀ shift, and it further supports the TWIST-I choice. Gap 14: LOW–MEDIUM (TWIST-I); MEDIUM for the tail variant.

**D385 (pp "research gaps", 10:55 CT, gap 1 n_s: what do the newest CMB+BAO combinations say about the Twist's N*?) — the tension is
~1σ against CMB alone and ~2.8σ once DESI is added; under TWIST-I (ΛCDM background) the DESI number applies, so gap 1 stays HIGH
(literature + arithmetic in code, aegis-checked).** "A Global Overview of Starobinsky Inflation beyond slow-roll with CMB-BAO data"
(arXiv:2609.19296): CMB-SPA n_s = 0.9684 ± 0.0030; CMB-SPA+DESI 0.9728 ± 0.0027. Starobinsky's fitted N* (prior N(60,20)) is 62.5 (+5.3/−7.6)
for CMB-SPA and 72.1 (+5.6/−7.6) for CMB-SPA+DESI, so the data want N* ~ 63–72, with best-fit T_re ~ 10¹² GeV (SPA) or ~4×10⁸ GeV (SPA+DESI)
at instant reheating. "The spectrum of n_s constraints from DESI and CMB data" (arXiv:2512.05108): adding DESI raises n_s in every CMB
combination, most with ACT, and τ moves up with it (an n_s–τ interplay); Starobinsky-type models are disfavoured at >2σ for SPA+DESI.
Twist (kination_Nstar.txt, heat share 0.04–0.4%; 0.65–0.8% extrapolates to N* ≈ 57.2): N* 57.4–57.9, n_s 0.9651–0.9655.
Distance (computed): CMB-SPA 1.0–1.1σ (inside the 68% N* interval, whose lower edge is 54.9); CMB-SPA+DESI 2.7–2.8σ (N* is ~7 below the
68% lower edge 64.5). Instant reheating (N* 55.7): 1.4σ and 3.2σ.
Reading: consistent with D329/D370 (the tension is background-conditional). Two possible relief routes, both outside our control:
(i) a better τ (n_s–τ correlation; LiteBIRD/CLASS low-ℓ), (ii) the BAO–CMB tension resolving away from ΛCDM. TWIST-I has a ΛCDM
background (w = −1), so it cannot use (ii) itself. No model change and no new prediction; the locked TWIST-I n_s rule is unchanged.
Open check for later (not computed, needs a lock first): kination_Nstar.py predates the TWIST-I/σ sector; the D367 trajectory keeps
Ω_kin > 0.5 until N − N_e ≈ 3.5 (vs ≈ 2.4 for a pure 0.8% heat share), which would add ~+0.5 to N*, while σ's matter-like share (up to
0.58 at N − N_e ≈ 4.5) would subtract. Net sign unknown; |ΔN*| ≲ 1 cannot close the ~7 e-fold gap to SPA+DESI.
Status: gap 1 HIGH, unchanged; quantified as ~1σ (CMB-SPA) / ~2.8σ (CMB-SPA+DESI).

**D386 (pp "continue", 11:00 CT, gap 4 birefringence: anything since D353?) — no new calibrated β; nothing changes (literature, abstracts).**
(1) SPT-3G polarised-beam paper (arXiv:2602.06334): measures the sidelobe depolarisation parameter β_pol (0.89 ± 0.10 / 1.08 ± 0.10 /
0.90 ± 0.22 at 95/150/220 GHz), not a birefringence angle; it reduces one SPT-3G polarisation systematic, which matters for a future
SPT β but gives none now. (2) Rigouzzo (KCL), CERN "Cosmological Probes of the Early Universe" talk, 30 June 2026: a cross-instrument
calibration method that recovers the DIFFERENCE of two instruments' angles from data alone (proof of concept on SO LAT and Planck). A
relative method; it does not fix an absolute zero by itself, which is what an isotropic β needs (consistent with D330). No numbers in the abstract.
Status: gap 4 HIGH, unscored; latest numbers are still ACT DR6 0.215 ± 0.074° and Planck 0.37 ± 0.11° (D353). TWIST-I predicts β = 0
(TWIST+ALP fallback locked). The first decisive input is still a calibrated SO/LiteBIRD measurement (late 2020s).

**D387 (scored, locked PREREG_D387_NSTAR_TRAJ; results/nstar_traj_d387.txt, rc 0) — on the full TWIST-I trajectory the kination
shift is dN* = +0.996 (converged: identical at N − N_e = 8.0 and 9.0), so N* = 56.70 and n_s = 0.9648. This is LOWER than the
55.7–57.6 range quoted since D84 and below the ACT-2σ Starobinsky region (N* ≥ 58). CORRECTION to the "N* 57.6" figure for TWIST-I.**
The radiation share stalls at Ω_rad ≈ 0.31–0.41 for N − N_e ≈ 4–5 because the hidden σ sector (matter-like, Ω_σ up to 0.58) holds part of
the energy; dN* peaks at +1.18 (N − N_e = 4) and falls back to +1.00 once σ decays. Development 84's +1.66–2.23 had no σ sector and lower
heat shares, so it overstated the shift by 0.66 (vs its 0.4% row). Arithmetic in code (aegis-checked): N* 55.70 + 0.996 = 56.70;
n_s (table interpolation) 0.9648, attractor 1 − 2/N* 0.9647 (agree). Distances: CMB-SPA 1.2σ; CMB-SPA+DESI 3.0σ; shortfall to the
SPA+DESI 68% edge (64.5) is 7.8 e-folds.
Cross-sector: n_B/s and the DM yield are not changed by this (same trajectory as D367); r = 12/N*² = 0.0037.
Docs to correct: TWISTI_CAPTURE.md, MODEL_CARD_v5.md, v6 item 19 and the D368–D370 range "55.7–57.6" → "56.7 (TWIST-I trajectory; 55.7
instant)". Status: gap 1 HIGH, slightly worse (2.8σ → 3.0σ for SPA+DESI).

**D388 (pp "continue", 11:35 CT, UV origin of TWIST-I's (T − T_E), after D380) — the two standard ways a Kähler modulus enters W both fail
D373's localisation requirement; the χ-trapping coupling is safe, the Y stabiliser's potential is the real open problem (literature +
arithmetic estimate in code; not a locked test).**
(1) Type IIB: the axionic shift symmetry of Im T forbids polynomial T in W to all orders in perturbation theory; T enters only as e^{−aT}
(standard; KKLT-type). The nearest allowed form is W ⊃ (A e^{−aT} − B)Y, which is linear near x_E with slope aA e^{−a x_E}. Localisation
(D373: width w ≲ 10⁻³ M_P) needs a ≳ 10³, and then a slope ~ λ = 0.004–0.033 needs log₁₀ A ≈ 1.2×10⁴: absurd. With a ~ 1 (log₁₀ A ≈ 10–11)
the potential is not local and is 10²² times larger at x ≈ 3 than near x_E, which would act on the roll after inflation. With a ≲ 0.03
(gauge group rank ≳ 2π/a ≈ 200) it is effectively (T − T_E) but global, which is D373's moduli problem.
(2) Type IIA: RR and NS fluxes give a polynomial W in T, including W_NS ⊃ U(h + f T) (arXiv:2007.00672, eqs. 2.15–2.16). This gives a
(T − T_E) factor with T_E = −h/f, a ratio of flux quanta (so x_E ≈ 28 would be quantised, a nice feature). But it is global, it multiplies
a modulus U with a non-zero vev rather than a matter field at Y = 0 (so D373's untilted form does not apply), and IIA flux vacua fix all
moduli in a SUSY AdS point (no roll). Fails as is.
(3) The χχ̄ coupling λ(T − T_E)χχ̄ does NOT need localisation: away from T_E, χ is simply heavy (D377). Only the stabiliser's potential,
k²|T − T_E|², must be local. So the open problem narrows to: a LOCAL stabiliser, e.g. one generated by the χ sector itself after trapping
(χ condensate / Coleman–Weinberg pinning near T_E) rather than a global tree-level W term.
Status: UV origin of (T − T_E) stays OPEN (now narrowed to the stabiliser). No change to locked tests. Next look: whether D374's one-loop
pinning from χ alone can give m_x ≳ 10⁵ GeV (needs a lock if computed).

**D389 (pp, 11:55 CT, DM window: anything tighter than D341 at 100–200 TeV?) — no; the window is unchanged (literature + arithmetic in code).**
LHAASO KM2A 570 days (PRL 129, 261103; arXiv:2210.15989) covers 10⁵–10⁹ GeV; the only number in the text is τ ≳ 6.3×10²⁸ s (bb̄) at 10 PeV, and
the press summary gives ≳ 10²¹ yr = 3.2×10²⁸ s at PeV. Curves at 100–200 TeV are figures only (not read numerically); the search found no
2025–26 update with numbers. Twist (D317 scaling τ ≈ 10²⁴ s (10⁶ GeV/m)⁵ ξ⁻², ξ = 1): 1.0×10²⁹ s at 100 TeV, 1.3×10²⁸ at 150, 3.1×10²⁷ at 200,
1×10²⁴ at 1 PeV. Against ~10²⁷–10²⁸ s hadronic limits at a few hundred TeV (D341), 100–150 TeV is safe, 200 TeV marginal, PeV excluded
for ξ ~ 1. Status: DM window ~100–200 TeV unchanged; a numerical read of LHAASO Fig. S6 / IceCube Fig. 5 at 100–200 TeV would sharpen it.

**D390 (pp, 12:20 CT, D388's narrowed problem: can the χ sector itself give a LOCAL stabiliser?) — the one-loop route fails; a
Higgs-branch route is a candidate but trades localisation for a timing/tuning condition (estimates; idea not computed or locked).**
(1) One-loop (Coleman–Weinberg) pinning from χ: χ's boson–fermion splitting is set by m_3/2 ~ eV (D374), so m_x ~ λ m_3/2/4π ~ 10⁻³ eV.
Fails m_x ≳ 10⁵ GeV by ~17 orders.
(2) Higgs branch: if χ and χ̄ get equal vevs v (D-flat), F_χ = λ(T − T_E)χ̄ = 0 forces T = T_E and gives (T − T_E) a supersymmetric mass
~ λv times O(1) Kähler factors, so m_x ≳ 10⁵ GeV needs v ≳ 10⁷ GeV for λ ~ 0.01. The potential λ²v²|T − T_E|² is still quadratic and global,
but it exists only once χ condenses (below T_c ~ v, if thermal masses keep ⟨χ⟩ = 0 above). By then x has stopped by Hubble friction:
from D367's line at N − N_e = 9.5 (x 29.741, dp 3.4×10⁻³) the free roll adds Δx ≈ 0.08 (radiation era, dp ∝ e^{−N}), so x_∞ ≈ 29.83
(arithmetic in code). So D373's "global potential acting along the whole roll" problem is avoided.
New condition: when the potential switches on, x sits at x_∞ while the minimum is at x_E. The oscillation energy is set by |x_∞ − x_E|,
and D359/D360a require a residual ≲ 10⁻⁷–10⁻⁵ M_P. So either x_E = x_∞ to that precision (a tuning of ~10⁻⁷ relative), or the Kofman
trapping (D363) holds x at x_E from crossing until T_c, which needs the trapped χ density (∝ a⁻³) to keep winning from T ~ 10¹¹ down to
~10⁷ GeV. Neither is checked.
Status: UV/IR origin of the stabiliser OPEN; best candidate now "Higgs-branch pinning switched on at T_c ~ v". Next step (needs a lock):
compute whether trapping holds x at x_E down to T_c, using D367's trajectory and D377's λ window.

**D367b (scored PROVISIONAL, locked PREREG_D367_OMEGAKIN + D1–D6; results/omegakin_d367.txt) — D362 FAILED: x's kinetic share at
T = 2×10¹³ GeV is Ω_kin,x = 0.70, ×4.1 above D362's upper value 0.17 (outside the ×3 band). Validation NOT REACHED (integrator stalls at
N − N_e = 10.36); post-hoc, n_B/s at the last printed point (9.5) is 1.0942×10⁻¹⁰, 0.39% from 1.090×10⁻¹⁰. x still rolling at 9.5
(dp 3.4×10⁻³ > 10⁻³).** Arithmetic in code: log-T interpolation between 2.186×10¹³ (0.7409) and 1.330×10¹³ (0.5219) gives 0.702 (the 0.741
quoted at 11:00 was the 2.186×10¹³ value; corrected). Kination dominates (Ω_kin > 0.5) until N − N_e ≈ 3.5; σ peaks at Ω_σ 0.58 (4.5);
radiation-dominated (Ω_rad > 0.99) from 6.5 on (D387). x: 3.09 at 3.0 (freeze-out), 27.2 at 6.0, 29.74 at 9.5, free-roll limit ≈ 29.83 (D390).
Consequences: D362's numbers are replaced by these. TWIST-I capture (D375/D376/D384) used D367a's trajectory, which these lines confirm,
so its conclusions stand (crossing of x_E ≈ 27–29.5 at T ≈ 1.7×10¹²–1.5×10¹¹ GeV, per the 6.0–8.5 lines). The verdict is provisional until a
stiff-integrator run (Radau/BDF; deviation first) reaches 11.

**D391 (scored, locked PREREG_D391_NSTAR_NOSIGMA; results/nstar_nosigma_d391.txt) — without the hidden σ sector the kination shift is
+1.53 / +1.48 at heat share 0.65% / 0.8% (converged), so N* = 57.24 / 57.19, n_s 0.9651, r 0.0036.** vs D387 (with σ) N* 56.7: σ costs
0.5 e-fold. Below 58 (ACT-2σ refined Starobinsky). Distances (code): ACT alone 0.2σ, CMB-SPA 1.1σ, CMB-SPA+DESI 2.85σ, P-ACT-LB 2.7σ.

**D392 (13:20 CT, Danny: "research and create one that can modulate itself … keeping our end view same") — Twist-2 design note
written (papers/twist_v6/TWIST2_DESIGN.md; design only, nothing scored).** Literature (2025–26): n_s with DESI in ΛCDM 0.973–0.977, CMB
alone 0.967–0.968, T-model ceiling 0.9682 (2511.14673); dynamical DE 2.3–4.2σ depending on SNe (2511.22512); axion quintessence fits
DESI+CMB+SNe and, with c_γ ~ 1–20, the birefringence angle (2504.17638). Design: every sector an attractor or symmetry-protected, one
dial each, nested fallbacks. Key new finding (estimate, code): the Twist angle y cannot be quintessence: f = √(3/2)/(a x₀) ≈ 0.004 M_P
for a potential of size ρ_Λ (a x₀ ≈ 277), so m/H₀ ~ 250 and a hilltop tuning ~10⁻¹¹⁶ would be needed; an aligned second axion
(f_eff 0.1–1 M_P) is the candidate fix. Next computations listed in §5 of the note; each to be locked first.

**D393 (scored, locked PREREG_D393_AXION_THAW; results/axion_thaw_d393.txt, rc 0) — Twist-2 sector II: PASS against
CMB+DESI+PantheonPlus, FAIL against CMB+DESI+DESY5; the pass needs f ≈ M_P and c_γ ≈ 10.** Best grid point f = 1 M_P, θ_i = 1.5:
w0 = −0.812, wa = −0.290, Ω_DE 0.690, Δθ = 0.332 since recombination, β = 0.222° for c_γ = 10. Distances (code): PantheonPlus w0 0.4σ,
wa 1.8σ, β 0.6σ → PASS. DESY5 w0 1.1σ, wa 2.6σ → FAIL (wa too shallow). Consistency check (aegis): the thawing relation
wa ≈ −1.58(1 + w0) = −0.297 matches the fit (−0.290). f = 0.3 gives a solution only at θ_i = 0.1 (near-Λ: w0 −0.981, β 0.18° at c_γ = 10).
Limitation (not fixed, to avoid chasing): most f = 0.1/0.3 points and θ_i ≥ 2 return "no flat solution" because the locked L4 bracket
[10⁻³, 50] is too narrow for hilltop starts; those points are untested, not excluded.
Reading: one thawing axion can give the PantheonPlus-preferred dark energy AND the birefringence angle with a single coupling c_γ ≈ 10,
but only for f ≈ M_P. That sharpens D392's obstacle: the alignment must reach f_eff ~ M_P (the Twist angle alone has ~0.004 M_P), which
is where weak-gravity-type arguments push hardest. It cannot give the steeper DESY5 wa (a known limit of thawing fields).

**D394 (13:40 CT, Twist-2 sector IV viability, estimate in code; not locked) — leptogenesis has ample room.** m_inf = 5.0×10¹³ GeV, so
inflaton decay to N₁ needs M₁ < 2.5×10¹³ GeV (D214's M_R ~ 2×10¹⁴ is too heavy for that channel; heavier N₂,₃ can keep it for m_ν).
With T_RH ~ 5×10¹⁴ GeV > M₁, N₁ is thermal: standard thermal leptogenesis. Davidson–Ibarra maximum ε₁ = 3M₁m₃/(16πv²) = 10⁻⁴ (M₁ =
10¹²) to 10⁻³ (10¹³); with n_B/s ~ 10⁻³ ε₁ κ and washout κ ~ 0.01–0.1 this gives ~10⁻⁹–10⁻⁷ ≫ 0.87×10⁻¹⁰. Viable with room; it
becomes a prediction only once the neutrino Yukawas are tied to the Twist (not done). Caveat: T_RH ≫ 10⁹ GeV needs the light-gravitino
branch (D292) to avoid gravitino overproduction; not rechecked here.

**D395 (13:15 CT, Danny: "Based on everything … map out one") — Twist-2 baseline mapped (papers/twist_v6/TWIST2_MODEL_MAP.md; design,
nothing scored).** Baseline: Twist inflation (N* 57.2, D391) + kination + thermal leptogenesis (D394) + TWIST-I capture with χ-condensate
pinning (D390, open) + Λ from the cliff (w = −1) + a separate light axion for birefringence + gravity-only 100–200 TeV DM. Six dials, each
fixed by one dataset. Single-axion dark-energy-plus-birefringence (D393) kept as the switch-on variant if DESI's evolution is confirmed
by a non-DESY5 sample. Trade-offs recorded: the angle-driven matter genesis and its isocurvature signature are given up; β is fitted in
the baseline.

**D396 (scored, locked PREREG_D396_PINNING; results/pinning_d396.txt) — PASS (robust, estimate-grade): χ can pin x at x_E without a
moduli problem, for a late capture point (x_E ≈ 29.6, crossing at T ≈ 1.5×10¹¹ GeV) and a condensate at v ≈ 10⁹ GeV, for all three λ
in the D377 window.** Chain: as x crosses x_E, the light χ, χ̄ in the bath give a thermal trap (frequency gT/2, g = λ x_E √(2/3)); x is
trapped in every scan point (kinetic/barrier 0.002–0.015). The trapped amplitude shrinks ∝ T, so at T_c it is 10⁻¹⁴–10⁻¹⁰ M_P (below the
10⁻⁷–10⁻⁵ M_P that D360a requires). The condensate gives m_x = g v. At the robust point (x_E 29.60, v 10⁹ GeV): m_x ≈ 10⁸–8×10⁸ GeV,
T_d ≈ 65 GeV–1.6 TeV, dilution D = 886 / 225 / 38 for λ = 0.004 / 0.01 / 0.033. Partial passes: x_E 29.45 (v 10⁹; λ ≥ 0.01) and x_E 29.21
(v 10⁹; λ = 0.033). Lower v (10⁵–10⁷ GeV) gives D ≫ 10³ (moduli-dominated) or T_d < 5 MeV. Arithmetic check: ρ_x/ρ_r at T_c is
independent of v (as the scaling requires) and D ∝ v^{−1/2}.
What it means: the "tuning to 10⁻⁷" worry of D390 disappears, since the thermal trap centres x on x_E automatically; x_E needs only to sit
below x's free-roll limit 29.83 and close to it (late crossing, small velocity). Costs: an entropy dilution D ~ 40–900, which leptogenesis
can absorb (D394 room ~10³) but which also dilutes gravity-only DM, so the DM mass window must be recomputed with D. Assumptions:
χ, χ̄ in thermal equilibrium (needs gauge charge, which the D-flat condensate needs anyway); O(1) factors in m_th, m_x and Γ not fixed.
Status: open problem 1 → PASS at estimate level; a field-theory check (thermal potential and condensation transition) remains.

**D397 (13:45 CT, cross-sector consequences of D396's dilution D; arithmetic refit in code, same scalings as D376) — DM and matter survive
the dilution, but the DM becomes PeV-scale and must be stable; λ ≈ 0.01–0.033 is preferred.** (1) DM: the gravity-only yield is
mass-independent (D112), so Ω ∝ m_DM/D and the 100–200 TeV window moves to 3.8–7.6 PeV (λ 0.033, D 38), 22–45 PeV (λ 0.01, D 225),
89–180 PeV (λ 0.004, D 886). Decay limit τ ≳ 10²⁸ s with D317's scaling then needs ξ ≲ 10⁻⁴ (λ 0.033) down to ≲ 10⁻⁷ (λ 0.004): the
decaying-DM signal disappears unless stability is only global and very weakly broken; with a gauged Z₂ (ξ = 0, D318) the DM is simply
stable. Masses stay ≪ T_RH and ≪ m_χ̃, so the production mechanism is unchanged. (2) Matter: leptogenesis must make 0.87×10⁻¹⁰ × D before
dilution: 3.3×10⁻⁹ (λ 0.033), 2.0×10⁻⁸ (λ 0.01), 7.7×10⁻⁸ (λ 0.004), against D394's reach of ~10⁻⁷: comfortable for λ ≥ 0.01, at the
edge for λ = 0.004. (3) Correction to the Twist-2 map: the heat share is not a free dial; it is already derived from χ̃ decay after the
cliff (D118 and D80–D82: 0.65–0.8% over decay-rate conventions). The map's "derive the heat share" item is replaced by "re-derive it
without σ (unchanged by construction, since σ never entered it)".
Status: Twist-2 baseline after D396–D397: pinning OK (estimate), matter OK, DM shifts to 4–45 PeV for λ ≥ 0.01 and is stable (no signal).

**D398 (13:50 CT, Danny: "Is our theory unique") — partly; the combination is ours, the parts are known, and a close prior paper was not
cited (literature).** arXiv:2008.09099 builds quintessential inflation in N = 1 no-scale supergravity: one inflaton drives inflation,
then kination (ρ ∝ a⁻⁶) with instant preheating through a Higgs-like field, then its residual potential acts as dark energy (scale tuned
by a SUSY-breaking parameter); n_s 0.9631 / r 0.0027 at N* = 55, blue-tilted GW from kination. That is structurally the v5 Twist
(no-scale inflaton, kination, instant preheating via χ̃, Λ from the residual potential). It is not cited anywhere in the repo or the v5
papers: v6 must cite it (and Ellis–Nanopoulos–Olive no-scale Starobinsky, arXiv:1307.3537; Peebles–Vilenkin quintessential inflation;
Kofman et al. moduli trapping, hep-th/0403001). Known ingredients: no-scale Starobinsky inflation; quintessential inflation with
kination; moduli trapping at enhanced-symmetry points; axion birefringence; thermal leptogenesis; gravity-only heavy DM.
What is specific to the Twist / Twist-2 (as far as the searches found): Λ = the cliff value at a trapping point x_E, with the trap set
thermally by χ and locked by a χ condensate (D396); the one-loop no-go for a rolling −3 ln field as dark energy (D323; to be checked
against literature before claiming novelty); the locked-test record. Observationally the inflation sector is Starobinsky-class (D368);
distinctive handles are N* ≈ 57.2 from built-in kination, the kination blue GW tilt (D86), and the sector-split predictions.
Added to v6: item 23 (prior-art citations).

**D399 (14:00 CT, Danny: "continue search; if it's ours, write a Zenodo paper and post") — the two candidate novelties are NOT ours in
substance; no paper posted (literature).**
(1) The modulus-quintessence no-go (our D323) was argued by K. Choi, "String or M theory axion as a quintessence" (hep-ph/9902292, 1999):
modulus components that set gauge couplings cannot be quintessence (δRe f_a/δQ ≲ 10⁻⁸¹ over a Planckian range; loop potentials too large),
and an axion whose partner modulus sits at a large value (Re T ≈ 32) is proposed instead. Our D323 adds the specific route (rescaling
anomalies, −b_a/4π, even when f_a is made T-independent by weights) and the number d ln α_em/d ln x ≈ 7×10⁻³; that is a refinement of a
known result, not a new no-go. Related: Quintessence and varying α from shape moduli (hep-ph/0402075; KK-threshold route).
(2) Trapping at enhanced symmetry points is established: particle-production trapping (Kofman et al., hep-th/0403001), thermal trapping
of a modulus by light states with a second stabiliser acting together (Danos, Frey & Brandenberger, arXiv:0802.1557), and "trapped
quintessential inflation" (Dimopoulos, hep-ph/0702018: ESP trapping + kination + frozen modulus as dark energy). Our D396 chain (late
thermal trap, then a χ condensate lock, with Λ = the cliff value at the trap) is a new arrangement of known parts, at estimate grade only.
(3) Choi's axion at Re T ≈ 32 is close to Twist-2's sector II idea and to our x_E ≈ 29.6; cite it.
Verdict: no publishable novelty claim of a new mechanism. What is ours: the integrated, pre-registered model and its computed numbers
(D367b, D387, D391, D393, D396). A Zenodo item could only honestly be a "model study with locked tests", not a discovery; per Danny's
condition ("if it's ours") nothing was posted. Citations added to v6 item 23.

**D400 (scored, locked PREREG_D400_DESI_ALPHA; results/kl_coeff.txt, results/desi_alpha_d400.txt) — EXCLUDED: every DESI-preferred CPL
fit realised by a modulus with K ⊃ −k ln(X+X̄) (k = 1, 2, 3) violates α-variation and equivalence-principle bounds at one loop by
large factors.** Coefficient (sympy, kl_coeff.py): with locality weights, 16π² d(1/g_a²)/d ln x = −b_a (k = 3; MSSM b = 33/5, 1, −3),
d ln α_em/d ln x = 6.97×10⁻³; general k: ×k/3, with d ln x/dφ = √(2/k), so ζ ≡ d ln α_em/dφ = 3.3–5.7×10⁻³. No choice of matter weights plus a
universal GS shift cancels all three gauge drifts with x-independent Yukawas and μ (empty solution set); dropping the μ condition forces
n_Hu + n_Hd = 12, so μ ∝ x^4.5 (the electroweak scale drifts). The earlier "−3b_a" in chat was a slip (it ignored matter metrics).
Field excursion since z = 1.15 (canonical, w clipped at −1, an underestimate): Δφ = 0.107 (PantheonPlus), 0.147 (DESY5), 0.184 (Union3).
Results: Δα/α(z = 1.15) = 3.5×10⁻⁴–1.0×10⁻³ (250–750σ vs ESPRESSO); α̇/α today = 1.3–3.3×10⁻¹³ yr⁻¹ (5×10⁵–1.3×10⁶σ vs clocks);
η ≈ 10⁻³ζ² = 1.1–3.2×10⁻⁸ (0.8–2.5×10⁶σ vs MICROSCOPE). Hand checks (aegis): 5.69×10⁻³ × 0.107 = 6.1×10⁻⁴; √(3·0.69·0.167)·6.89×10⁻¹¹ yr⁻¹
× 5.69×10⁻³ = 2.3×10⁻¹³ yr⁻¹; 10⁻³ × (5.69×10⁻³)² = 3.2×10⁻⁸.
Reading: to survive, the one-loop coupling must be suppressed by ≳ 10³ in ζ (EP) — i.e. the modulus must not be the field that sets e^K
for the visible sector, or the SM must be sequestered beyond locality, or dark energy must be axionic. This is the basis of the
paper draft papers/alpha_nogo/ (D401).

**D401 (14:35 CT, Danny: "Start that and draft paper") — draft written: papers/alpha_nogo/ALPHA_NOGO_DRAFT.md + PDF (3 pages; DRAFT,
not posted).** Title: "One-loop gauge-coupling drift rules out modulus quintessence at DESI-preferred dark energy." Content: D400's
coefficient −(k/3) b_a, the empty weights+GS solution set, DESI field excursions, the exclusion table, escapes (axions, true sequestering,
per-factor GS), caveats, prior work credited (Carroll 1998, Choi 1999/2000, Acharya–Maharana–Muia 2018, Kaplunovsky–Louis, Arkani-Hamed–
Murayama, Conlon–Palti). Framed as a quantitative sharpening of Choi's argument for the DESI era, not a new mechanism. Needs before posting:
an independent check of the coefficient against Kaplunovsky–Louis eq. (and the n_r = k/3 locality argument for k ≠ 3), the EP conversion
η ≈ 10⁻³ζ², and a reference check; then Danny's "Publish".

**D402 (14:45 CT, pre-posting checks of the D401 draft) — passed.** (1) Coefficient: the Kaplunovsky–Louis form quoted in Conlon–Palti
(0901.4350, eq. 1: g⁻² ⊃ (Σn_rT_a(r) − T(G))K̂/16π² − Σ_rT_a(r) ln det Z^r/8π²) is the one used in kl_coeff.py. Cross-check: for the
volume of local D3 models (K̂ = −2 ln𝒱, Z ∝ 𝒱^{−2/3}) our rule gives −(2/3)b_a per ln𝒱, which is exactly Conlon–Palti's b_a ln M_X² with
M_X ∝ 𝒱^{−1/3}. Added to the draft. (2) EP conversion η ≈ 10⁻³ζ² is the one used by Martins et al. (2204.02930), attributed. (3) References
verified: Choi PRD 62, 043509 (2000); Filzinger et al. PRL 130, 253001 (2023); Murphy et al. A&A 658, A123 (2022); MICROSCOPE PRL 129, 121102
(2022); DESI DR2 arXiv:2503.14738. Remaining before posting: Danny's "Publish". (A separate-reviewer pass was offered, not run.)

**D403 (scored, locked PREREG_D403_BRIDGES; results/bridges_d403.txt) — three "Wheatstone bridge" null tests set up (Danny 14:17).**
Bridge 1 (inflation; N* cancels): Twist B1 = r − 3(1−n_s)² = −9.2×10⁻⁵ (N* 57.2; −1.03 to −0.80×10⁻⁴ over N* 55–60), tolerance 1.2×10⁻⁴;
B2 = α_s + ½(1−n_s)² = +1.5×10⁻⁷ (tolerance 2×10⁻⁴). So the Twist balances both to ~10⁻⁴, far below LiteBIRD's σ_r ~ 10⁻³: an imbalance
would kill the whole α = 1 plateau class independent of reheating. Not scoreable yet (r is an upper limit). Implied r: 0.0029 ± 0.0006
(CMB-SPA n_s) or 0.0021 ± 0.0004 (+DESI n_s); the Twist's own N* gives r = 0.0036.
Bridge 2 (dark energy ↔ clocks): R = (α̇/α)/[H0√(3Ω_DE(1+w0))] measured (4.4 ± 6.2)×10⁻⁹ (PantheonPlus w0) vs modulus prediction ζ =
3.3–5.7×10⁻³: OUT OF BALANCE by ~5×10⁵σ (same content as D400, now one line).
Bridge 3 (birefringence ↔ dark energy; initial angle cancels): VALID — K1 = β(c_γ=1)²/(1+w0) is constant to ±4% across θ_i at f = 1 M_P,
and K1 f² ≈ 2.1–2.5×10⁻³ deg² over f = 0.5–2, so β² ≈ 2.5×10⁻³ (c_γ/f)² (1 + w0) deg² (f in M_P). Scored at c_γ = 10, f = 1: predicted β =
0.203 ± 0.034° (PantheonPlus) and 0.249 ± 0.028° (DESY5) vs 0.261 ± 0.061°: BALANCED (0.8σ, 0.2σ). Honest reading: with c_γ/f free this
measures c_γ/f ≈ 10–13 rather than testing it; it becomes a test with a second, independent arm (e.g. the reionization-era rotation, whose
ratio to the recombination value is also θ_i-free — a fourth bridge, not yet locked), or once c_γ/f is fixed by the model.

**D404 (scored, locked PREREG_D404_BRIDGE4; results/bridge4_d404.txt) — bridge 4 computed: ρ_β = β_reio/β_rec = 0.9965–0.9989 for the
single thawing axion (all grid points), i.e. ρ_β = 1 − ε with ε ≤ 3.5×10⁻³ (z_re = 7), 2.5×10⁻³ (z_re = 8), 1.3×10⁻³ (z_re = 10). No measurement
yet: not scored (literature).** The ratio is c_γ- and θ_i-free as intended (spread across f and θ_i < 10⁻³). Data: no reionization-era β
exists; the recombination-era combination is β ≈ 0.3° (4.6σ combined, Planck/WMAP/ACT; arXiv:2602.12019), and Planck ℓ > 42 shows no scale
dependence (consistent). LiteBIRD (2030s) is the first experiment able to measure both bumps (arXiv:2203.08560, 2602.12019).
Honest limit (aegis cross-check): a pure polarisation miscalibration ALSO gives ρ_β = 1. So bridge 4 separates "late field (dark-energy
axion) or miscalibration" (ρ ≈ 1) from "field that moved before reionization" (early-dark-energy or dark-matter-like axion, ρ ≠ 1); it does
not by itself separate the dark-energy axion from a systematic. That separation needs the calibration-independent methods (D330, D386)
or a reionization-bump analysis that fits miscalibration jointly (2108.09287).

**D367c (FINAL score, locked PREREG_D367_OMEGAKIN + D1–D8; results/omegakin_d367.txt) — VALID; D362 FAILED (final). Validation:
n_B/s at N − N_e = 11 is 1.0920×10⁻¹⁰, 0.18% from 1.090×10⁻¹⁰ (within 1%). Reading: Ω_kin,x at T = 2×10¹³ GeV = 0.70 (D367b), outside ×3
of D362's 0.02–0.17 → D362 FAILED. Still rolling at the end (dp > 10⁻³)? NO: dp = 7.7×10⁻⁴ at N − N_e = 11 (x = 29.806, T = 1.2×10¹⁰ GeV);
x = 29.813 at 11.5.** The Radau continuation (D7) passed the LSODA stall in seconds; D8 fixed a print-tolerance bug that had hidden the
lines (also the missing 10.00 line). D367b's "provisional" label is removed. The free-roll limit 29.83 (D390) is consistent with the
trajectory (29.81 at 11.5, still creeping). Consequence for TWIST-I/Twist-2: unchanged (crossing of x_E ≈ 27–29.6 happens at T ≈ 10¹²–10¹¹ GeV
while x still moves; D396's late-capture point x_E ≈ 29.6 is crossed at T ≈ 1.5×10¹¹ GeV, as used).

**D405 (15:58 CT, Danny: "Publish") — the α no-go paper is on Zenodo: record 24232382, DOI 10.5281/zenodo.24232382 (v1).** Content as D401 +
D402 cross-check + D403 bridge 2. Linked to the Twist concept DOI (isDerivedFrom). Log in papers/ZENODO_UPDATE_2026-11-13.md.

**D406 (scored, locked PREREG_D406_BALANCE; results/balance_d406.txt) — first centre check of the two-ladder process: NO BALANCE
(narrowly). The right ladder's pinning dilution always costs the left ladder more than 0.5 e-fold of N*.** Every scan point passes the right
ladder (trapped, T_d ≥ 5 MeV, D ≤ 10³), but ΔN* = −(1/3) ln D ranges from −2.26 (λ 0.004, v 10⁹, D 886) to −0.518 (λ 0.033, v 10¹¹ GeV, D 4.7).
Best point: N* = 56.68, n_s = 0.9648, r ≈ 0.0037 (1.2σ from CMB-SPA, 3.0σ from CMB-SPA+DESI) — the same N* as D387 with σ, so Twist-2's
gain from dropping σ (D391, +0.5 e-fold) is cancelled by the pinning dilution. Corrections: D396/D397 did not include this cross-effect;
D395's map value N* = 57.2 must read 56.7–56.0 with pinning (λ 0.033, v 10¹¹–10⁹). The balanced region wants the largest λ (D377's upper edge)
and v close to the crossing temperature (condensate right after capture), i.e. the least dilution. Returned to rung 10 (right ladder) with
the task: reduce D below ~4.5 without breaking trapping or T_d (options: v at T_x, a larger λ if D377's upper bound can move, or a decay
channel for x that is faster than gravitational).

**D407 (cycle 1; RIGHT ladder, scored, locked PREREG_D407_GAUGE_DECAY; results/gauge_decay_d407.txt) — the pinning dilution disappears if x
decays through the gauge channel of the χ condensate: D = 1.000 (≤ 1.001) at every grid point, even with κ = 10⁻⁶.** Reason: at gauge strength
Γ = κ g_X² m_x/8π, x decays at T_d ≈ 10⁹–10¹³ GeV, before its oscillation energy (ρ_x/ρ_r ≲ 4×10⁻⁴ at T_c, D396) can grow. CENTRE: BALANCED —
ΔN* ≈ 0, so the left ladder keeps N* = 57.2, n_s 0.9651 (D391); F2 passes (T_d ≫ 5 MeV, D ≈ 1); F5: DM mass returns to 100–200 TeV (no D shift),
leptogenesis needs only 0.87×10⁻¹⁰ (D394 room ×10³). This supersedes D397's PeV DM and resolves D406 (CONFIRMED, conditional).
Conditions (to be checked in later cycles): (i) the light U(1)_X-charged decay products must not be dark radiation (F7: they should be
SM-charged, e.g. U(1)_X mixing with hypercharge, or decay further); (ii) x's multiplet really contains the decaying scalar with κ ≳ 10⁻⁶
(field theory of the Higgs branch); (iii) U(1)_X must be anomaly-free and its D-term must allow the D-flat condensate.

**D408 (cycle 2; PART 2 inflation plateau, LEFT; scored, locked PREREG_D408_PART2; results/part2_d408.txt).**
(a) ALONE: CMB exit at p* = −10.92 (x* ≈ 1.4×10⁻⁴), end of inflation p = −5.79, capture at x = 29.81 (p = 4.16). Field excursion: 5.13 M_P during
the last 55.7 e-folds, 9.95 M_P from the end of inflation to capture, 15.1 M_P in total. ε* = 2.35×10⁻⁴ (r = 16ε = 0.0038 ✓), |V'|/V = 0.022,
V*^{1/4} = 8.0×10¹⁵ GeV, H* = 1.5×10¹³ GeV. String flags (F6, report not veto): dS slope conjecture (s₁ ~ O(1)) VIOLATED (0.022); TCC
(arXiv:1909.11106: V^{1/4} ≲ 6×10⁸ GeV, r ≲ 10⁻³⁰) VIOLATED by ×1.3×10⁷ in scale; distance conjecture SEVERE — a tower would drop by
e^{−λΔφ} = 2×10⁻³ (λ = 1/√6) to 3×10⁻⁷ (λ = 1) over the full range. The first two are shared by every plateau model with detectable r (Starobinsky
included); the third is Twist-specific because the same field also travels ~10 M_P after inflation. New flag: CMB exit happens at x ~ 10⁻⁴,
far from a large-volume regime if x is read as a volume modulus (x ∝ V^{1/3}); control of the EFT there is not established.
(b) IMMEDIATE CONNECTIONS: part 3 (kination) inherits the 9.95 M_P post-inflation roll — the distance-conjecture tower, if it is the KK tower
of this modulus, gets lighter in Planck units as x grows; whether it stays above T and H along the roll is the check for part 3. Part 11
(string embedding) inherits the control flag at x ~ 10⁻⁴.
(c) WHOLE / CENTRE: B1 = −0.9×10⁻⁴, B2 ≈ 0 balanced (D403); F3 n_s 0.9651 (1.1σ / 2.9σ); F6 three flags as above. Result recorded (no model change).

**D409 (cycle 3; PART 3 kination/reheating, LEFT; scored, locked PREREG_D409_PART3; results/part3_d409.txt) — the distance-conjecture tower
is NOT a danger after inflation: m_KK/T ≥ 2.4×10⁴ and M_s/T ≥ 4.4×10⁴ at every D367 point (volume reading 𝒱 ~ x^{3/2}, O(1) factors = 1).**
(a) ALONE: heat share derived (0.65–0.8%, χ̃ decay, D80–D82/D118); kination dominates to N − N_e ≈ 3.5 (D367c); +1.5 e-folds of N* (D391).
(b) CONNECTIONS: from part 2 (D408) — the tower drops by e^{−λΔφ} along the roll, but it starts far above T and H (m_KK = M_P/x falls only from
~10¹⁹ to 8×10¹⁶ GeV while T falls from 3×10¹⁴ to 10¹⁰), so no tower state is excited and the 4d description holds once x ≳ 1. The weak point is
the start: for x < 1 (N − N_e ≲ 2.5, and all of inflation) m_KK and M_s formally exceed M_P, i.e. the volume is sub-stringy and the geometric
reading fails — D408's control flag extends through the first ~2.5 e-folds of kination. To part 4 (leptogenesis): T_RH ~ 5×10¹⁴ GeV < M_s, OK.
To part 5 (capture): unchanged.
(c) CENTRE: filters F2/F3 unchanged; bridges unchanged. Verdict: D408's "distance conjecture SEVERE" downgraded to "control issue at x ≲ 1
only"; the post-inflation roll is safe. Result → no wall.

**D410 (16:36 CT, Danny: "Set this up" — the CROWN) — five-sense joint fit locked (PREREG_D410_CROWN) and running on the PC.** THAW_FREE
(n_s free) and THAW_TWIST (n_s = 0.9651) on CMB-SPA + DESI DR2 + Pantheon+, thawing line wa = −1.58(1+w0); launched 16:36 via
RUN_D410_CROWN.bat (both minimisers initialised; best of 4). Pre-run note (stated in the lock, from stored non-locked fits): with these
likelihoods ΛCDM n_s = 0.9737, free w0–wa n_s = 0.9720, CMB-only 0.9711, so letting dark energy evolve lowers n_s only by ~0.002; C1 is at risk.
Score with `python crown_d410.py score` (runs automatically at the end; log cmb-fit/results/d410_log.txt).

**D411 (cycle 4; PART 4 leptogenesis, LEFT/RIGHT; estimate from existing numbers, no new locked computation).**
(a) ALONE: thermal leptogenesis needs M₁ ≳ 10⁹ GeV (Davidson–Ibarra); with D407's D ≈ 1 it must only make the observed 0.87×10⁻¹⁰; the
Davidson–Ibarra ε₁ ≤ 10⁻⁴ (M₁ 10¹²)–10⁻³ (10¹³) gives up to ~10⁻⁷ before washout (D394), i.e. a washout efficiency κ ≳ 10⁻³ suffices.
Literature: leptogenesis in a quintessential-kination background was studied by Chun–Scopel (arXiv:0707.1544): a faster expansion keeps
N₁ out of equilibrium and weakens washout.
(b) CONNECTIONS: part 3 — from D367c, Ω_kin < 1% below T ≈ 2.5×10¹² GeV, so for M₁ ≲ 2×10¹² GeV leptogenesis is standard radiation-era;
for M₁ ~ 10¹³ GeV it happens while Ω_kin ≈ 0.2–0.5 (washout mildly reduced, in the favourable direction). Inflaton decay into N₁ needs
M₁ < m_inf/2 = 2.5×10¹³ GeV (D394). Part 9 — T_RH ~ 5×10¹⁴ GeV is only safe with the light (eV) gravitino branch (D292); flagged for part 9.
Part 1 — no dilution (D407), so no extra demand.
(c) CENTRE: F2 (D ≈ 1) and F3 unchanged; matter sector consistent for M₁ ∈ [10⁹, 2.5×10¹³] GeV. Verdict: consistent, nothing new scored → WALL 1.

**D412 (cycle 5; PART 5 capture/pinning, RIGHT; scored, locked PREREG_D412_PART5; results/part5_d412.txt) — D407 condition (i) PASSES:
if x decays into a hidden vector-like pair (the minimal anomaly-free U(1)_X content), the dark radiation is ΔN_eff = 0.034 (MSSM g* at
decoupling, appropriate since T_d ≈ 10⁹–10¹³ GeV ≫ soft masses) or 0.094 (SM g*), below ACT DR6's ΔN_eff < 0.14 (95%; via arXiv:2512.19633).**
Single hidden Weyl/scalar: 0.017–0.054. Only a large chiral hidden content with SM g* would reach the bound (0.141). Correction to the script
label: the "3 Weyl" row is illustrative; the minimal anomaly-free choice is the vector-like Dirac pair. The U(1)_X boson is massive (g_X v), not light.
(a) ALONE: thermal trap (D396) + condensate + gauge decay (D407) now has conditions (i) checked; (ii) Higgs-branch field theory and (iii) the
D-term/anomaly structure remain. (b) CONNECTIONS: part 1/8 — decay products hidden, so DM and SM bath unaffected; part 6 — the capture point
x_E ≈ 29.6 fixes Λ (unchanged). (c) CENTRE: F7 passes; NEW PREDICTION: ΔN_eff ≈ 0.03–0.09 if the decay is hidden (CMB-S4/SO σ ≈ 0.03–0.05 can
test it); if instead U(1)_X mixes with hypercharge, ΔN_eff ≈ 0. Result → walls reset.

**D413 (cycle 6; PART 6 Λ from the cliff, RIGHT; scored, locked PREREG_D413_PART6; results/part6_d413.txt) — ROBUST: Λ ∝ x_E^{−0.97}
(d ln V/d ln x = −0.964 to −0.968 over x_E = 27–29.83), so moving the pin from 29.6 to the free-roll limit 29.83 changes Λ by only −0.75%.**
(a) ALONE: past the cliff the potential is essentially the e^{−2n} plateau times a slowly falling prefactor (~1/x); Λ is set by n (one dial,
n ≈ 124.1, D383) and is insensitive to exactly where x is pinned — no fine tuning of x_E is needed. String flag (F6): a pinned positive Λ is a
de Sitter minimum, which the refined dS conjecture disfavours and which no controlled string construction yet provides (review
arXiv:2603.25797). (b) CONNECTIONS: part 5 — the pin (D396, x_E ≈ 29.6) only needs ±1% accuracy for Λ at the ±1% level; part 7 — the
birefringence axion is separate and does not shift Λ. (c) CENTRE: w = −1 exactly in the baseline; the crown fit (D410) tests the thawing
variant. Result → walls 0. Crown status: THAW runs converging (runs 1–2 of 4 done at 16:52).

**D414 (cycle 7; PART 7 birefringence axion, RIGHT; scored, locked PREREG_D414_PART7; results/part7_d414.txt) — NATURAL: a separate
light axion with m between ~2 H0 and H_rec (3×10⁻³³–3×10⁻²⁹ eV), θ_i ~ 1–2.5 and photon coupling c_γ ≈ 1.6–3.9 gives β = 0.261°, with a
sub-Planckian f ≤ 0.1 M_P and an energy share Ω_a ≤ 3×10⁻³ (estimate).** So the baseline does NOT need the f ≈ M_P that troubled the
single-axion dark-energy variant (D392/D393); it is weak-gravity-conjecture friendly. (a) ALONE: frozen at recombination, oscillates or
rolls by today, Δθ ≈ θ_i for m ≳ 2H0; for m ≲ H0 it barely moves and needs c_γ ≳ 40–90. (b) CONNECTIONS: part 6 — Ω_a ≤ 3×10⁻³ leaves Λ and
w ≈ −1 untouched; part 10 — CP-odd coupling, no α drift (F1 passes). The Twist's own angle is heavy after capture (D382), so this must be
another axion (e.g. a second modulus's). (c) CENTRE: B3 (β–w link) does not apply to the baseline; NEW bridge consequence for B4: for
m ≳ H(z ≈ 10) ≈ 20 H0 the field is already oscillating at reionization, so β_reio/β_rec < 1 — unlike both the dark-energy axion and a
calibration error (ratio ≈ 1). LiteBIRD's two-bump measurement can therefore tell this baseline apart (to be quantified when computed).
Result → walls 0.

**D415 (cycle 8; PART 8 dark matter, RIGHT; scored, locked PREREG_D415_PART8; results/part8_d415.txt) — COLD: the gravity-only DM born in
χ̃ decays (p ≤ m_χ̃/2 = 6.3×10¹⁶ GeV, p/T ≈ 113 at birth) becomes non-relativistic at T_NR ≥ 0.9–1.8 TeV for m_DM = 100–200 TeV, ~10⁶ above the
1 MeV margin (Lyman-α warm-DM bounds act at ~keV).** (a) ALONE: mass 100–200 TeV restored by D407 (D ≈ 1); yield mass-independent (D112);
stability by a gauged Z₂ (no signal) or global with ξ ≲ 0.6 at 200 TeV (D317/D389 decay window). (b) CONNECTIONS: part 1 — no dilution, so
D397's PeV shift is withdrawn; part 3 — production during the kination/reheating epoch (T ~ 5×10¹⁴ GeV), momentum redshifts normally after.
(c) CENTRE: F5 passes (stable, or decay window), structure formation unaffected. Result → walls 0.
Crown status: THAW_TWIST finished 17:06; THAW_FREE on its last runs.

**D416 (cycle 9; PART 9 light gravitino, LEFT/RIGHT; scored, locked PREREG_D416_PART9; results/part9_d416.txt) — PASS for the preferred
pairing: total extra radiation ΔN_eff = 0.047 (gravitino, g* = 106.75) + 0.034 (hidden pair, g* = 228.75) = 0.081 < 0.14; the most conservative
pairing (both at SM-like g*) gives 0.141–0.153, just above the bound.** CROSS-SECTOR CATCH (centre): the gravitino and the D412 hidden decay
products share the same ΔN_eff budget, which neither part saw alone. Requirement recorded: m_3/2 ≤ 4.7 eV (95%, arXiv:1601.07386), so the
SUSY-breaking scale √F = (√3 m_3/2 M_P)^{1/2} ≲ 1.4×10⁵ GeV — consistent with D292's x-independent eV-gravitino branch and soft masses 10⁴–10⁵
GeV; low-scale gauge mediation with m_h = 125 GeV also bounds m_3/2 from below (arXiv:1608.01610; not read — next cycle on part 9). (b) Part 4:
the light gravitino is what allows T_RH ~ 5×10¹⁴ GeV (no gravitino overproduction for m_3/2 ≲ 16 eV), so leptogenesis stands. (c) CENTRE:
F7 PASS (0.081) with a sharpened prediction: ΔN_eff ≈ 0.05–0.10 in total (SO/CMB-S4 testable). Result → walls 0.

**D417 (cycle 10; PART 10 SM couplings / α, RIGHT; consistency arithmetic from locked results, no new locked computation).** (a) ALONE:
D400's one-loop drift d ln α_em/d ln x = 6.97×10⁻³ applies to Twist-2 only while x moves, i.e. before capture. From matter freeze-out (x ≈ 3.1,
T ≈ 2×10¹³ GeV) to the pin (x_E ≈ 29.6, T ≈ 1.5×10¹¹ GeV) α_em shifts by 1.6% — all long before BBN, with no observable at that epoch except
the matter yield, which D367c computed along the same trajectory (couplings in the yield are taken at the matter epoch, consistent). After
pinning and the gauge decay (T_d ≈ 10⁹–10¹³ GeV), the residual displacement ≲ 10⁻¹⁰ M_P (D396) gives Δln α ≲ 2×10⁻¹⁴: α at BBN, recombination,
quasars, Oklo and today is the same → F1 passes by construction (clock bridge balanced at R = 0, unlike any rolling modulus).
(b) CONNECTIONS: part 1 — D407 condition (iii): U(1)_X must be anomaly-free; a vector-like hidden pair (D412) is, and with no state charged
under both U(1)_X and hypercharge the kinetic mixing is not generated at one loop (ε = 0), so the hidden decay products stay hidden
(consistent with D412's ΔN_eff budget). Part 7 — the birefringence axion's CP-odd coupling does not shift α (F1). Part 9 — soft masses
x-independent (D292), so no sliding SUSY scale after capture.
(c) CENTRE: F1 PASS, bridges unchanged. No new scored result → WALL 1.

**D418 (cycle 11; PART 11 string embedding, WHOLE; literature + collected flags, no new locked computation) — first full pass complete.**
(a) ALONE: closest prior art for the capture-and-pin chain is the "string Higgs effect" (Watson, hep-th/0404177): extra states become
massless at an enhanced-symmetry point of the radion, and their backreaction plus Hubble damping stabilises it there — our thermal trap
(D396) is the same physics in a 4d supergravity form; cite it with Kofman et al. and Danos–Frey–Brandenberger. Hidden U(1)s with vector-like
matter are generic in IIB orientifolds with D7-branes (Goodsell–Jaeckel–Redondo–Ringwald, arXiv:0912.4206), so U(1)_X (D407, D412, D417) has a
natural home. Open, unchanged: (i) a local (T − T_E) coupling is not available from IIB shift symmetry or IIA fluxes (D388); (ii) control at
x ≲ 1 during inflation and the first ~2.5 e-folds after it (D408, D409); (iii) string flags TCC/dS/distance (D408, D413).
(b) CONNECTIONS: parts 2, 5, 6, 10 — consistent with their notes; the birefringence axion (part 7) wants a second modulus axion, generic in
multi-moduli compactifications. (c) CENTRE: no filter or bridge changes. No scored result → WALL 2 → interval 5 → 30 min.

**D410 scored (CROWN, locked PREREG_D410_CROWN; results/crown_d410.json; PC run 16:36–17:32 CT) — SENSES DISAGREE.**
χ²: THAW_TWIST (n_s fixed 0.9651, thawing line) 2408.06; THAW_FREE (n_s free) 2400.11; ΛCDM 2402.26; free w0–wa 2392.30.
C1 FAIL: fixing n_s at the Twist value costs Δχ² = 7.95 (~2.8σ for one parameter) even with thawing dark energy.
C2 FAIL: against ΛCDM, the CMB block is worse by +5.80 and BAO by +4.22 (SN better by −2.25) — sight and hearing reject the Twist's n_s.
C4 FAIL (marginally): at THAW_TWIST's w0 = −0.971, a single dark-energy axion would need c_γ/f = 30.4 (> 30) for β = 0.261°. (C4 concerns the
single-axion variant; the baseline's separate axion, D414, is not tested by it.) C3 passes by construction.
Key numbers: n_s in a thawing background = 0.9736 (ΛCDM 0.9737) — letting dark energy thaw does NOT lower n_s; the thawing line itself
helps little (Δχ² −2.2 vs ΛCDM with one extra parameter) while free w0–wa gains −10.0, so the data prefer a steeper (phantom-crossing)
shape than any single thawing field. Reading (outcome 3 of the 16:19 discussion): the Twist's inflation sector is ~2.8σ off on CMB-SPA+DESI
+Pantheon+ regardless of the dark-energy branch; all other sectors pass their checks. This goes into the Twist-2 paper's abstract.

**D419 (LEFT ladder + CENTRE; scored, locked PREREG_D419_ROUTE_A; results/routeA_d419.txt) — ROUTE A WORKS: one tiny holomorphic term,
F → (T + ε)·cliff/√(1+T/μ) with K = −3 ln(T + T̄) unchanged, gives n_s = 0.9736 at N* = 57.2 for ε = +3.04×10⁻⁷ (M_P units).**
Locked new inflation predictions (n_s is now FITTED, not predicted): r = 0.0046, α_s = −7.7×10⁻⁴, B1 = r − 3(1−n_s)² = +2.5×10⁻³ (bridge 1 now
broken in a definite direction: r is 2.2× the plain-Starobinsky value 0.0021 at the same n_s), B2 = −4.2×10⁻⁴. Cross-sector (centre): factor at
the end of inflation 1.00007 (kination, heat share, N* unchanged), Λ factor 1 + 2×10⁻⁸ (absorbed in n). Window: n_s ∈ 0.9736 ± 0.003 needs ε ∈
(1.8–3.7)×10⁻⁷ (linear estimate) — a ±35% window, comparable to the R³ precedent (arXiv:2505.03608, α ∈ −4.2 to −1.9×10⁻⁵); ε/x* ≈ 2.5×10⁻³ at the CMB point.
Crown consequence (from the scored D410 fits, no new run): at n_s = 0.9736 the THAW_FREE fit is better than ΛCDM in every sense (CMB −2.77,
BAO −0.41, SN −2.48; total −2.15), and the single-axion β link needs c_γ/f = 24.9 ≤ 30 — so with Route A all five senses agree. Honest label:
this agreement is partly by construction (ε fitted to n_s); the real tests move to r = 0.0046 (LiteBIRD σ_r ~ 10⁻³: ~4.5σ detection; 2.4σ from
plain Starobinsky at the same n_s), α_s = −7.7×10⁻⁴ and B1 = +2.5×10⁻³. Physical reading: a small constant-like piece in the stabiliser
superpotential (W ⊃ ε S·cliff/√(1+T/μ)), natural in no-scale models with a flux constant; its size relative to the main term (~2.5×10⁻³ at x*)
is a mild tuning, stated.

**D420 (17:55 CT) — Twist-2 paper published: Zenodo record 24235736, DOI 10.5281/zenodo.24235736 (v1).** Abstract states the crown failure of the
undeformed n_s (Δχ² 7.95) and the Route A fit (ε = 3.0×10⁻⁷ → r = 0.0046, α_s = −7.7×10⁻⁴); weak points listed; prior art credited.

**D421 (17:58 CT, Danny: "Has anyone done this yet") — the bound side is done; the one-loop prediction side appears not to be (literature).**
Martins et al. / Euclid (arXiv:2105.09746) treat dark energy's coupling to electromagnetism as a free parameter ζ and, combining quasars,
clocks and MICROSCOPE (with Euclid forecasts), get ζ = (−3.6 ± 5.9)×10⁻⁸ (w0wa fiducial) — ~60× tighter than the MICROSCOPE-only 3.6×10⁻⁶ used
in the α paper; they note such couplings "unavoidably exist in string theory" but do not compute them. arXiv:2209.12189 couples the field's
kinetic term to F²; arXiv:2604.12032 (DESI-era coupled DE) couples to dark matter only; arXiv:2411.08774 uses JWST α constraints; none
derives ζ from a Kähler potential. So the α paper's specific contribution — ζ = 3.3–5.7×10⁻³ predicted at one loop for K ⊃ −k ln(X+X̄),
hence ~10⁵ above the combined bound — was not found elsewhere (Choi 1999 is the qualitative precursor). For a v2 of the α paper: add the
2105.09746 combined bound (strengthens the exclusion from ~10³ to ~10⁵ in ζ).

**D422 (cycle 12, second pass; PART 1 condition (ii), RIGHT; scored, locked PREREG_D422_PART1B; results/part1b_d422.txt) — condition (ii)
is SATISFIABLE but the decay products are heavy: CORRECTION to D412/D416's ΔN_eff.** On the Higgs branch, δT pairs with the neutral radial
mode of χχ̄ into a multiplet of mass m_S = √2 λ' v ≈ 1.4×10⁸–1.1×10¹¹ GeV. A fast decay needs W ⊃ y χψψ̄', which gives Γ = y² m_S/8π (κ ≥ 10⁻⁶
needs y ≥ 5×10⁻⁴) but also gives the products a mass m_ψ = y v; kinematics allow y up to 0.07–0.56 (window exists for every λ). So the products
are NOT massless: m_ψ ≈ 5×10⁵–10⁹ GeV. If ψ-number were conserved they would overclose the universe (thermal-relic estimate Ωh² ≈ 4×10⁴–
2×10¹¹). New requirement (recorded): ψ must decay to the SM, e.g. by mixing with SM leptons (W ⊃ y' ψ L H-type), which is allowed since U(1)_X
is broken. Their energy share is ≲ 4×10⁻⁴ of radiation (D396), so no dilution (D ≈ 1 stands). Consequence: the hidden-pair dark radiation of
D412 (0.034) disappears; total ΔN_eff = gravitino only ≈ 0.047 (range 0.017–0.059 over g*) — the published Twist-2 table's "0.05–0.10"
should read "0.02–0.06" (to be corrected in a v2). CENTRE: F2, F5, F7 pass with the new requirement; bridges unchanged. Result → walls 0.

**D423 (cycle 13, "pp"; second pass PART 2, LEFT; scored, locked PREREG_D423_PART2B; results/part2b_d423.txt) — SAFE: with Route A the
plateau still gives 219 e-folds of slow roll (start at x ≈ 4.7×10⁻⁸ where (1 + ε/x)² makes it steep; end at x = 8.8×10⁻³), 162 more than
N* = 57.2 needs, so no tuning of initial conditions.** The deformation makes V rise toward small x (dlnV/dφ < 0 there), so the field
rolls in the same direction as before. Flags (F6, report): the field range from the start of slow roll to capture is 24.8 M_P (14.9 M_P of it
during inflation), worse for the distance conjecture than D408's 15.1 M_P from the CMB point; only the last ~5 M_P before the end of inflation
are observable. (b) CONNECTIONS: part 3 (kination) unchanged (end-of-inflation factor 1.00007, D419); part 11 — the control flag at x ≲ 1 now
covers x down to ~10⁻⁸. (c) CENTRE: bridges as in D419 (B1 = +2.5×10⁻³); no filter changes. Result → walls 0.

**D424 (cycle 14, "pp"; second pass PART 3, LEFT; scored, locked PREREG_D424_PART3B; results/part3b_d424.txt) — SAFE and undetectable:
with r = 0.0046 the radiation-era GW plateau is Ω_GW h² ≈ 1.7×10⁻¹⁷; the Twist's ~3.5 e-folds of kination boost modes above ~3×10⁵ Hz by up to
×33, to a peak ≈ 5.6×10⁻¹⁶ at ≈ 10⁷ Hz.** ΔN_eff(GW) ≈ 10⁻¹⁰ (estimate), negligible. The boosted band lies at 0.3–12 MHz, far above LISA/ET
and orders of magnitude below proposed high-frequency GW searches; the blue tilt is a real feature (D86) but not a near-term test.
(b) CONNECTIONS: part 2 (r from Route A); part 9 (ΔN_eff budget: gravitino 0.02–0.06 dominates, D422). (c) CENTRE: F7 pass; no bridge change.
Result → walls 0.

**D425 (cycle 15, "pp"; second pass PART 4 leptogenesis, LEFT/RIGHT; consistency estimate in code, no new locked computation) — D422's new
requirement does not disturb leptogenesis.** If the heavy decay products ψ (m_ψ ≈ 5×10⁵–10⁹ GeV) decay through W ⊃ y' ψ L H with ψ carrying
lepton number +1 (vector-like lepton partner), the decays conserve L and cannot wash out the N₁ asymmetry. Decaying before BBN (T = 1 MeV,
H = 2.2×10⁻²⁴ GeV) needs only y' ≳ 2×10⁻¹⁶ (m_ψ = 10⁹ GeV) to 1×10⁻¹⁴ (5×10⁵ GeV) (computed), so any natural y' works; their energy share ≲ 4×10⁻⁴ of radiation
(D396) means no entropy dilution (D ≈ 1, leptogenesis still needs only 0.87×10⁻¹⁰). Mixing with SM leptons is ~y' v_EW/m_ψ ≪ 10⁻³, so
lepton-flavour and neutrino-mass effects are negligible. (b) CONNECTIONS: part 1 (D422), part 3 (T_RH), part 9 (gravitino-safe T_RH).
(c) CENTRE: F2/F3 unchanged. No scored result → WALL 1 (at 30-min pace).

**D426 (cycle 16, "pp"; second pass PART 5, RIGHT; scored, locked PREREG_D426_PART5B; results/part5b_d426.txt) — CONSISTENT, with a new
explicit requirement: the hidden χ sector must share the SM temperature at capture, which the D422 lepton portal provides if y' ≳ 5×10⁻³
(x_E = 29.6; 6.5×10⁻³ and 8.4×10⁻³ for earlier capture points).** Then the ψ–lepton mixing is only y' v_EW/m_ψ ≈ 2×10⁻⁶ (m_ψ = 5×10⁵ GeV),
far below 10⁻³, so no flavour or neutrino-mass trouble. If the hidden sector were instead colder (T_h = ξT, no portal), trapping still works
for ξ ≥ 0.21 (x_E = 29.6), 0.28 or 0.35 — so a hidden sector reheated separately (e.g. by χ̃ decays) at a fifth of the SM temperature or more
is also enough. Cross-effect closed: D417's ε = 0 (no photon mixing) is compatible, because the thermal link runs through leptons, not
photons. This lower bound on y' joins D425's (y' ≳ 10⁻¹⁶–10⁻¹⁴ for decays before BBN): y' ∈ [5×10⁻³, ~1]. Result → walls 0.

**D427 (cycle 17, "pp"; second pass PART 6 Λ, RIGHT; estimate in code) — CORRECTION/CLARIFICATION of "Λ from the cliff": the χ condensate
adds a vacuum energy that the cliff cannot absorb; Twist-2's Λ is the cliff value only AFTER the standard one-off cosmological-constant
cancellation, which must now also cancel the condensate sector.** The Higgs branch is supersymmetric (D- and F-flat, zero energy) only before
SUSY breaking; with soft masses 10⁴–10⁵ GeV (D292) and v = 10⁹–10¹¹ GeV the condensate's soft vacuum energy is ~m_soft² v² ≈ 10²⁶–10³² GeV⁴,
i.e. 10⁷²–10⁷⁹ times ρ_Λ (2.5×10⁻⁴⁷ GeV⁴), x-independent after pinning. D292 already needed one tuning (μ⁴ = 3w²/8) to cancel the SUSY-breaking
energy; that same constant now has to absorb this term too, to ~1 part in 10⁷²–10⁷⁹. So the honest statement is: Twist-2 does not solve the
cosmological-constant problem; given the one cancellation every model needs, the leftover x-dependent piece is the cliff value e^(−2n) at x_E
(D383, D413), which is what n sets. Earlier wording ("residual potential sets the vacuum energy", Twist-2 paper v1 abstract and §2) should say
this explicitly → added to the v2 correction list. (b) CONNECTIONS: part 5 (condensate), part 9 (SUSY-breaking scale). (c) CENTRE: no filter
fails; the claim is narrowed. Result (correction) → walls 0.

**D428 (cycle 18, "pp"; second pass PART 7, RIGHT; scored, locked PREREG_D428_PART7B; results/part7b_d428.txt) — bridge B4 for the
baseline birefringence axion computed: ρ_β = β_reio/β_rec ≈ 1 for m ≲ 10 H0 (0.96–1.00), 0.85–0.94 at 20 H0, 0.24–0.66 at 50 H0, and ≈ 0
(0.003–0.19) for m ≥ 100 H0 (z_re = 7–10).** Distinguishable from the dark-energy axion and from miscalibration (both ρ ≈ 1, D404) when
|1 − ρ_β| ≥ 0.2, i.e. m ≳ 30 H0 (z_re = 7) to ≈ 40 H0 (z_re = 10) — CORRECTION to D414's "≳ 20 H0" (at 20 H0 the ratio is still 0.85–0.94).
For m ≥ 100 H0 the field already oscillates around reionization, so the large-angle (reionization) rotation nearly vanishes while the
recombination one stays ≈ θ_i — a sharp LiteBIRD signature. Δθ_rec ≈ 1 for m ≥ 10 H0 (θ_i = 1), consistent with D414's c_γ ≈ 3.9.
(b) CONNECTIONS: part 6 (Ω_a ≤ 3×10⁻³, Λ untouched), part 10 (CP-odd, no α drift). (c) CENTRE: B4 now has a quantified baseline branch.
Result → walls 0.

**D429 (cycle 19, "pp"; second pass PART 8 dark matter, RIGHT; estimate in code, no new locked computation) — the newest corrections do not
touch the dark matter.** (1) The x-multiplet decays (D407/D422) could make gravity-only DM by graviton bremsstrahlung: with n_S/s ≈ 3×10⁻⁴–2×10⁻³ and a
branching ~(m_S/M_P)²/16π² ≈ 2×10⁻²³–10⁻¹⁷ the extra yield is ≲ 4×10⁻²¹ (computed), against the 4.4×10⁻¹⁵ needed for 100 TeV: negligible. (2) The heavy ψ
(D422) decay to SM leptons and do not mix with the DM fermion (gravity-only by construction). (3) Route A changes nothing after inflation
(D419), so T_RH, the χ̃-decay yield (D112) and coldness (D415) stand. DM remains 100–200 TeV, cold, stable under a gauged Z₂ (no signal) or
decaying with ξ ≲ 0.6. (c) CENTRE: F5 pass, unchanged. No scored result → WALL 1.

**D430 (cycle 20, scheduled tick; second pass PART 9 gravitino, LEFT/RIGHT; literature + arithmetic) — the gravitino is squeezed into a
narrow window, 1 eV ≲ m_3/2 ≤ 4.7 eV, which makes Twist-2's SUSY sector sharply testable.** Low-scale gauge mediation that gives m_h = 125 GeV
needs m_3/2 ≳ 0.8 eV (4π/y), i.e. ≳ 1 eV for a strongly coupled messenger sector (arXiv:1608.01610, N_m = 4); cosmology gives ≤ 4.7 eV
(arXiv:1601.07386). Hence √F ≈ 65–140 TeV (computed). After D422 the only extra radiation is the gravitino's: ΔN_eff = 0.047 (g* = 106.75,
preferred) within 0.017–0.059 — the v2 prediction "0.02–0.06". The window is testable by 21 cm observations (per 1608.01610) and by CMB-S4's
ΔN_eff. (b) CONNECTIONS: part 4 (T_RH ~ 5×10¹⁴ GeV allowed only for this light gravitino), part 5/6 (soft vacuum energy of the condensate uses
m_soft from this sector, D427), part 10 (x-independent soft masses, D292). (c) CENTRE: F7 pass; window recorded. Result → walls 0.

**D431 (cycle 21, "pp"; second pass PART 10 SM couplings, RIGHT; arithmetic in code) — the lepton portal (D422/D426) forces two structural
choices, or neutrino masses come out far too large.** (1) Gauge invariance: ψLH_u is renormalizable only if the lepton-coupled partner is a
SM singlet AND U(1)_X-neutral; so in W ⊃ y χ ψ ψ̄' the partner ψ̄' must be neutral and ψ carries −q_χ; anomaly freedom of U(1)_X then needs a
mirror pair (ψ̃ with +q_χ and its own neutral partner, coupled to χ̄). (2) Lepton number: if the portal violated L, the heavy ψ would act as a
seesaw: m_ν ≈ y'² v_EW²/m_ψ = 0.76 eV–0.6 MeV for y' = 5×10⁻³–0.1 and m_ψ = 10⁹–5×10⁵ GeV (computed), above the Σm_ν ≲ 0.07 eV bound in every
case. So ψ, ψ̄' must form an L-conserving (Dirac, inverse-seesaw-like) pair; then light neutrino masses are untouched and only the tiny
mixing angles y' v_EW/m_ψ ≈ 10⁻⁹–3×10⁻⁵ remain (negligible for flavour and unitarity). With these two choices F1 (α frozen, D417) and the
neutrino sector (Σm_ν ≈ 0.06 eV, D355b) stand. (c) CENTRE: pass with recorded requirements. Result → walls 0.

**D432 (cycle 22, "pp"; second pass PART 11 string embedding, WHOLE; literature + arithmetic) — second pass complete; the eV gravitino adds
two embedding requirements, both consistent with the strongly coupled messenger sector D430 already needs.** (1) Every modulus other than the
Twist must be stabilised supersymmetrically (fluxes, heavy), since anything fixed by SUSY breaking would get m ~ m_3/2 ~ eV and mediate a
long-range force or a moduli problem; the Twist itself is pinned by the χ condensate (m ~ 10⁸–10¹¹ GeV), and the birefringence axion is light
by design but CP-odd (no force on matter at linear order). (2) The SUSY-breaking field X (D292's Polonyi-type field) must not be an eV-mass
scalar: with a strongly coupled hidden sector at Λ ~ √F, the sgoldstino mass ~ 2F/Λ ≈ 1.3×10⁴–2.8×10⁵ GeV (√F = 65–140 TeV, Λ = √F–10√F;
computed), heavy enough — the same strong coupling (y ~ 4π) that 1608.01610 needs for m_h = 125 GeV with m_3/2 ≳ 1 eV. Open items unchanged:
local (T − T_E) origin (D388), control at x ≲ 1 (now down to x ~ 10⁻⁸ with Route A, D423), TCC/dS (D408, D413, D427). Hidden U(1)_X content now
specified (D417, D422, D431): vector-like χ, χ̄; ψ, ψ̃ with neutral partners coupled to L H_u (L-conserving). No new scored result → WALL 1.
SECOND PASS DONE (cycles 12–22): corrections to the published paper are queued as v2 items.

**D433 (cycle 23, "pp"; third pass begins; CENTRE audit) — consolidated Twist-2 numbers written to papers/twist_v6/TWIST2_NUMBERS.md (each
entry traced to its D-note; the v2 paper's source). Cross-checks: B1 = r − 3(1−n_s)² with Route A values 0.0046 − 3(0.0264)² = +2.5×10⁻³ ✓;
total ΔN_eff (gravitino only after D422) 0.047 ✓ (< 0.14); all F1–F7 filters pass with the recorded requirements. No new physics → WALL 2 at
30-min pace → interval 60 min.

**D434 (cycle 24, "pp"; third pass PART 2, LEFT; scored, locked PREREG_D434_PART2C; results/part2c_d434.txt) — Route A's locked prediction
band: over n_s = 0.9706–0.9766 (ε = 2.0–4.0×10⁻⁷), r = 0.0042–0.0050 and α_s = −7.1 to −8.4×10⁻⁴, with B1 = +1.6 to +3.3×10⁻³.** The key
signature: r RISES with n_s (0.0042 → 0.0050), opposite to plain Starobinsky, where r = 3(1−n_s)² FALLS (0.0026 → 0.0016) across the same n_s
range. So the two separate more as n_s grows (ratio 1.6× at 0.9706, 3.0× at 0.9766). A measurement in the (n_s, r) plane outside this band
(2σ) falsifies Route A. Correction to D419's ε window (linear estimate 1.8–3.7×10⁻⁷ for ±0.003): computed 2.0–4.0×10⁻⁷. Result → walls 0.

**D435 (cycle 25, "pp"; third pass PART 3, LEFT; arithmetic in code) — Route A does not shift N*: the deformation raises V at the CMB point by
(1 + ε/x*)² ≈ 1.0046 and at the end of inflation by 1.00007, so the matching term ¼ ln(V*²/V_end) moves N* by ≈ +0.002 e-fold (Δn_s ~ 10⁻⁶);
the kination gain (+1.5) and heat share are untouched (D419, D424). N* = 57.2 stands for Twist-2 with Route A. Nothing new scored → WALL 1
(60-min pace).

**D436 (DEEP STUDY, Danny "Deep", 19:00 CT; theory/deep/DEEP_STUDY_FI_ORIGIN.md + fi_origin_check.py) — a candidate origin for the
capture coupling: a moduli-dependent Fayet–Iliopoulos term on a magnetised D7-brane.** ξ = (1/𝒱)Σ M_i t^i (flux integers; arXiv:0711.3389)
depends on Re T, so D388's holomorphy no-go does not apply. Sympy (two moduli, GS shifts δ₁, δ₂): ξ = δ₁/(2x₁) + δ₂/x₂ vanishes at
x_E = −(δ₁/2δ₂)x₂ (quantised by flux charges), and charged states have m_φ² ≈ −g²Q (dξ/dx)(x − x_E) — linear in (x − x_E), the D-term analogue
of λ(T − T_E). Near capture it gives the light states, a steep D-term wall past x_E, and (with soft masses) a gentle slope that pins x at x_E;
energy released ~10⁻⁷–10⁻⁵ of radiation (computed, δ₂ = 0.01, x₂ = 30). OBSTACLE: at small x the same FI term is huge (ξ ≈ −76 M_P² at the CMB
point, −1.1 M_P² at the end of inflation; unscreened V_D ≈ 10³ M_P⁴ vs V_inf ~ 10⁻¹⁰), and screening needs trans-Planckian condensates — the
D7 sector must be absent or differently described at x ≪ 1 (the region already flagged as uncontrolled, D408/D423). Status of the (T − T_E)
origin: OPEN → candidate found, conditional. Next (locked first): a two-modulus toy with the D7 sector present only for x ≳ 1.

**D437 (DEEP STUDY step 2; scored, locked PREREG_D437_FI_TOY + D1; results/toy_fi_d437.txt) — CAPTURES: in the two-modulus toy the
D-term (FI) mechanism alone, without the thermal trap, catches and pins the Twist at x_E.** From D367c's trajectory (N − N_e = 6), x hits the
D-term wall at x_E = 29.6 at T ≈ 1.5×10¹¹ GeV, reflects to x_min = 29.43 (m_s = 10⁴ GeV) or 29.51 (10⁵ GeV), is pulled back by the soft-mass
slope and returns to the wall at T ≈ 1.7×10¹⁰ / 5.6×10¹⁰ GeV, then settles on it (bounces damped by Hubble friction; final offset ~10⁻¹⁵).
So the soft term (x-independent, D292) supplies the pinning that D390/D396 needed a condensate scale for, and the wall stops the overshoot
to the free-roll limit 29.83. The thermal trap of D396 becomes a backup rather than a requirement. Energy involved ≲ 10⁻⁵ of radiation (D436):
no moduli problem, D ≈ 1. Conditional exactly as D436: valid only where the magnetised D7 sector is present and screened (x ≳ 1); the
small-x (inflation) region still needs a different description. A first run had two reporting bugs (fixed via D1 before scoring; first
output kept as toy_fi_d437_run1_bug.txt).

**D438 (DEEP STUDY step 3; scored, locked PREREG_D438_STRINGY_FI; results/stringy_fi_d438.txt) — OBSTACLE RESOLVED IN THE TOY: with the
stringy (Π-stability) FI term, ζ = difference of central-charge grades, the small-volume blow-up of D436 disappears.** Toy: magnetised D7
on T²×T², fluxes (m₁, n₁) = (10, 400) on the rolling cycle, constant c = −0.373 from the fixed cycle; ζ(x) = (1/π)[atan(x/m₁) − atan(x/n₁)] + c.
(i) Capture root at x_E = 29.6 approached from small x (second root at 135, irrelevant for a field arriving from below). (ii) |ζ| ≤ 0.373 M_s²
for all x < x_E: ζ ≈ −0.373 at the CMB point and at the end of inflation, −0.28 at x = 3.1 — instead of the supergravity extrapolation's
−76 M_P² (D436). Screening needs only |φ|² ≈ 0.37 M_s², sub-Planckian if M_s ≲ M_P; ζ is almost constant at small x, so the screened
condensate adds essentially no slope to the inflaton (corrections ~(M_s/M_P)² × 0.37 to V, nearly x-independent). (iii) At large x the toy
reproduces the supergravity 1/x form (at x = 1000: 0.118 vs (n₁ − m₁)/πx = 0.124, computed). Note: in this toy x_E lies on the stringy branch
(x < √(m₁n₁) ≈ 63), not in the strict large-volume regime. Caveats: no α′ or worldsheet-instanton corrections to Z (relevant at x ≲ 1); the
D7 gauge coupling at small volume not modelled; a toy torus, not a Calabi–Yau. Status of the capture-coupling origin: candidate mechanism
with its main obstacle removed at toy level (D436–D438).

**D439 (cycle 26, "pp"; PARTS 2+5 link, CENTRE; scored, locked PREREG_D439_SCREEN_INFL; results/screen_infl_d439.txt) — locked verdict
"SAFE IF M_s ≤ 0.1 M_P"; the tilt is safe for any M_s.** The φ condensate that screens the stringy FI term (D438) leaves, through its
Hubble-induced mass, δV/V = (c_H/3)|ζ|(M_s/M_P)². Because ζ is almost flat at small x (x·dζ/dx ≈ 4e-6 at x* = 1.3e-4), the shifts are
tiny even at M_s = M_P: δn_s = −2.0e-6 (c_H = 1) to −5.9e-6 (c_H = 3), δr ≤ 1.3e-6 (both ≪ 1e-4; hand check of 2δη agrees). Only the
1% amplitude criterion fails at M_s = M_P (δV/V = 12–37%, a nearly constant offset that renormalises the amplitude A_s and is absorbed by
it); at M_s = 0.1 M_P, δV/V = 0.12–0.37%, so every criterion passes. Bridges B1/B2 unchanged within 1e-5. CENTRE: balanced (left:
plateau untouched; right: capture unchanged). Status: the FI-term origin survives inflation at toy level; requires M_s ≲ 0.1 M_P for a clean pass.

**D440 (cycle 27, "pp"; third pass PART 4, LEFT/RIGHT; arithmetic in code, standard formulas, no new model; results/part4c_numass_d440.txt)
— leptogenesis survives the DESI DR2 neutrino-mass bound; no new restriction.** DESI DR2 + CMB give Σm_ν < 0.0642 eV (95%, ΛCDM;
arXiv:2503.14744). Normal ordering then needs m₁ < 0.0043 eV (minimum sum 0.0587); inverted (min 0.100) is disfavoured — the Twist
takes no side on ordering, so nothing breaks. Thermal leptogenesis (Davidson–Ibarra ε_max = 3M₁m_atm/16πv², Y_B ≈ 1.3e-3 εκ, strong-washout
κ fit) with D ≈ 1 needs M₁ ≥ 6.8e8 GeV (κ ≈ 1), 2.9e10 (m̃₁ = m_sol), 7.3e10 (0.02 eV), 2.0e11 GeV (m̃₁ = m_atm). Because m̃₁ ≥ m₁ only, m̃₁
remains free, and all of these lie inside D411's window 1e9–2.5e13 GeV (lower edge consistent with 6.8e8). Labels: estimate (κ fit ±30%).
No scored result → WALL.

**D441 (cycle 28, "pp"; third pass PART 5, RIGHT; scored, locked PREREG_D441_STRINGY_CAPTURE; results/stringy_capture_d441.txt) — CAPTURES
with the stringy FI term at M_s = 0.1 M_P.** (a) The wall is hard: arrival speed dφ/dN = 0.010 at T = 1.5e11 GeV (H = 1.3e-14 M_P, kinetic
energy 8.4e-33 M_P⁴) penetrates past x_E by only 7.5e-12 (M_s = 0.1 M_P) or 7.5e-10 (0.01 M_P) — far below 1e-2. (b) The soft slope near
x_E is ζ′ = 2.47e-3 M_s² per unit x, i.e. 2.19× D437's slope at M_s = 0.1 M_P, so D437's return-to-the-wall result carries over
conservatively; it drops below D437's slope for M_s < 0.0675 M_P (not shown to fail there, just not covered). Combined with D439
(clean plateau for M_s ≤ 0.1 M_P): **the FI-term origin works at toy level for 0.068 ≲ M_s/M_P ≲ 0.1 (clean), or for any M_s ≥ 0.068 M_P if the
constant amplitude offset of D439 is accepted.** CENTRE: balanced; this narrows the string scale (new conditional prediction of the toy:
M_s ≈ 1.6–2.4×10¹⁷ GeV). Caveat: toy fluxes (10, 400) fixed; a different flux pair moves the window.

**D442 (cycle 29, tick; third pass PART 6, RIGHT; scored, locked PREREG_D442_FI_VACUUM; results/fi_vacuum_d442.txt) — locked verdict
"KEEPS D427 PIECE", but only as a numerical limit; the tree-level answer is zero.** The bounded minimiser stopped at x = 29.6069 with
ζ = −3.6e-10, giving V = 2.1e33 / 2.1e35 GeV⁴ (m_s = 1e4 / 1e5 GeV). Two facts to record honestly: (i) the exact root of the D438 toy is
29.6069, not 29.600 (the constant c = −0.3728 was rounded in D438; immaterial for D438–D441, whose numbers move by < 0.03%); (ii) the
potential is V = m_s²|ζ|M_s² (ζ < 0) or (g²/2)ζ²M_s⁴ (ζ > 0), both ≥ 0 and both zero at ζ = 0, so the true minimum is V = 0 (the screening
condensate vanishes exactly on the wall). With M_s² ≈ 6e34 GeV² the double-precision floor on ζ (~1e-17) alone corresponds to ≳ 6e25 GeV⁴,
so this test as locked could never reach the 1e23 threshold — a badly designed lock (my error), not a physical result. No rerun.
Reading (analytic, not scored): in the FI picture the pinning sector leaves no condensate vacuum energy at tree level, so D427's
1e26–1e32 GeV⁴ piece is absent; the SUSY-breaking CC cancellation (one tuning) remains. Loop corrections not computed. Verdict for the
loop: no scored result → WALL.

**D443 (cycle 30, "pp"; third pass PART 7, RIGHT; data update, arithmetic in code; results/part7c_beta_d443.txt) — birefringence input
updated, nothing breaks.** Joint ACT DR6 + Planck (arXiv:2608.06480): β = 0.277° ± 0.057° (4.8σ from zero; 0.236° ± 0.067° in the high-ℓ,
30% Galactic-cut check; depends on the instrumental priors as reported). D414 used β = 0.261°: shift 0.28σ. Required photon coupling
scales by 1.061 → c_γ ≈ 1.7–4.1 (was 1.6–3.9); f ≤ 0.1 M_P and Ω_a ≤ 3e-3 unchanged (Ω_a does not depend on β). The paper does not
separate reionization from recombination, so B4 (β_reio/β_rec) remains untested; LiteBIRD remains the decider. No scored result → WALL.

**D444 (cycle 31, "pp"; third pass PART 8, RIGHT; scored, locked PREREG_D444_PHI_RELIC; results/phi_relic_d444.txt) — locked verdict
"NEEDS φ DECAY OR ADIABATIC": a NEW open condition for the FI picture.** The screening field φ is charged under the anomalous D7 U(1),
whose Stückelberg mass M_V ≈ 1.7e17 GeV cuts φ off from the plasma (Γ/H = 7e-19 at 1.5e11 GeV). If the condensate energy at capture
(≤ 1e-5 of radiation, D436) ended as φ quanta, ρ_φ/s = 1.1e6 GeV — 2.6e15 × the DM value. The condensate dissolves adiabatically
(A = 1.4e-8 at 1e-3 below the wall, 4.5e-4 at 1e-6) except within ~6e-9 of x_E, where A → ∞ as m_eff → m_s. Post-lock estimate (NOT
scored): the energy left there is ~5e-21 of radiation → ρ/s ~ 6e-10 GeV, the same order as all of dark matter, and D437's thousands of
bounces off the wall could each add to it. So: φ needs a decay channel into lighter states (τ < 1 s for BBN), or it becomes a second
DM component that must be counted (overclosure risk). The perturbative U(1) charge acts as a global symmetry broken only by D-instantons, so
a superpotential coupling to lighter hidden states (e.g. W ⊃ λ φ X Y) is needed — added as an open condition. CENTRE: F5 (DM) flag on the FI
picture; the pinning itself is unaffected.

**D444a (correction to D444, same cycle; arithmetic in code, appended to results/phi_relic_d444.txt)** — my hand estimate of the
non-adiabatic remnant was wrong by 1e6. Computed: the residual energy where A = 1 (m_eff = 6.5e11 GeV, 5.9e-9 below x_E) is 8.6e31 GeV⁴ =
4.9e-15 of radiation, so ρ_φ/s ≈ 5.5e-4 GeV — **1.3e6 × the DM density, not "the same order"**. So the condition is firm, not marginal:
in the FI picture φ MUST decay (τ < 1 s) or the model overcloses. Estimate (single crossing; bounces only add).

**D445 (cycle 32, "pp"; third pass PART 9, L/R; scored, locked PREREG_D445_PHI_FATE; results/phi_fate_d445.txt) — locked verdict "NEEDS
NON-PERTURBATIVE CHARGE BREAKING" for a charged state at the soft mass.** The goldstino channel is fast (τ = 6e-29 to 1.3e-22 s for
√F = 65–140 TeV, m = 1e4–1e5 GeV) but only moves the U(1) charge to ψ_φ; the lightest charged state stays stable. Hidden annihilation through
W ⊃ λφXY as a thermal relic needs σv ≥ 1.9e-9 GeV⁻² (Ω ≤ Ω_DM) or 1.9e-7 GeV⁻² (≤ 1%): λ ≥ 1.75 / 5.54 at m = 1e4 GeV and 5.54 / 17.5 at
1e5 GeV — the 1% case exceeds the perturbative limit √(4π) ≈ 3.5. Post-lock reading (not scored): since λ_needed ∝ √m, a lightest charged
state below ~3 TeV (1% case) or a charged relic counted as a DM component would avoid this; otherwise the global charge must be broken by
D-instantons (e^{−S} small but only τ < 1 s is needed) or by a second brane U(1) mixing. CENTRE: F5 flag stands; the FI picture now carries
the explicit condition "lightest D7-charged state light (≲ TeV) and annihilating, or charge broken non-perturbatively". Pinning, Λ and
inflation are unaffected.

**D446 (cloud run, Danny 19:16 CT; scored, locked PREREG_D446_CLOUD_CAPTURE; results/cloud_capture_d446.txt) — CAPTURES in all 8 cases;
the lower string-scale edge of D441 goes away; the remnant is dominated by bounces.** Full D437 integration with the stringy FI term
(exact root 29.6000): for M_s/M_P = 0.03, 0.0675, 0.1, 0.3 and m_s = 1e4, 1e5 GeV the field hits the wall at T = 1.5–1.7e11 GeV, bounces
down to x = 29.41–29.54, returns at T = 1.1e10–1.1e11 GeV and settles (offset at the float floor). Check: at M_s = 0.0675 M_P, where the slope
equals D437's, x_min = 29.4272 and return T = 1.67e10 GeV reproduce D437 exactly. So D441's conservative bound M_s ≥ 0.068 M_P is lifted; with
D439, capture + clean plateau hold for 0.03 ≲ M_s/M_P ≲ 0.1 (0.3 also captures; plateau then carries the amplitude offset). Remnant summed over
all 5001 recorded hits (cap reached): ρ/s = 4.8e4–1.5e6 GeV = 1e14–3e15 × DM. That is far above the first hit alone (5.5e-4 GeV, D444a) and
reaches the energy-conservation ceiling (1.1e6 GeV, D444) in the 0.3/1e5 case, so the per-hit estimate overcounts there and the true remnant
lies near the ceiling. Consequence: the φ sector is effectively heated to the condensate energy, so the initial abundance is erased if φ
thermalises, and D445's annihilation/charge-breaking conditions govern the outcome. They become mandatory, not optional.

**D447 (cloud run 2, Danny 19:20 CT; scored, locked PREREG_D447_HIDDEN_RELIC; results/hidden_relic_d447.txt) — the leftover particles can be
removed perturbatively if the lightest D7-charged state is ≲ 10 TeV (1%), or ≲ 100 TeV as a full DM component.** Hidden-bath freeze-out
(complex scalar, σv = λ⁴/16πm²). With the D446 energy ceiling (ε_h = 1e-5 → T_h/T = 0.102): λ for Ω = Ω_DM / 1% Ω_DM = 0.026/0.088 (10 GeV),
0.085/0.29 (100 GeV), 0.28/0.94 (1 TeV), 0.91/3.04 (10 TeV), 2.96/9.8 (100 TeV); for a hotter bath (ε_h = 1e-3, T_h/T = 0.32) the 1% case
fails at 10 TeV (λ = 4.2) and both fail at 100 TeV. Check: scaling the standard ξ = 1 value (λ = 1.75 at 10 TeV, D445) by ξ^{1/4} gives 0.99
vs 0.91 computed. This sharpens D445 (whose ξ = 1 limit was ~3 TeV): the colder bath helps. **Interesting by-product (not a claim): at
m ≈ 10–100 TeV with λ ≈ 1–3 the charged state is a natural second DM candidate in the same mass range as the Twist's gravity-only DM.**
Lock items not done: the rough thermalisation check (Γ_th vs H) was specified but not coded. Process note: the script was executed once,
unviewed, about a minute before the lock commit (import test); the scored run was started after the lock was pushed.
CENTRE: F5 now passes conditionally (light charged state + λ ≲ 3); open condition narrowed.

**D448 (cycle 33, "pp"; third pass PART 10, RIGHT; literature reasoning, no computation) — the D7 U(1) and hypercharge: condition stated,
nothing scored.** With the lightest D7-charged state now at ≲ 10–100 TeV (D447) and possibly a DM component, mixing with hypercharge matters.
(i) Kinetic mixing χ alone with the Stückelberg-massive D7 boson (M_V ≈ 1.7e17 GeV) gives the hidden state NO millicharge under the
massless photon. Its effects on SM currents are suppressed by (E/M_V)², i.e. invisible. (ii) Stückelberg MASS mixing (Kors–Nath, hep-ph/0402047;
1401.5880) would make the massless photon a mixture and give the hidden state a millicharge ε ~ δ, which direct detection
constrains very tightly for a TeV-scale DM component (LZ/XENONnT; size of the bound not extracted here). Condition added: the axion eaten by the D7 U(1)
must not couple to hypercharge (δ = 0, the usual D-brane requirement for a massless Y), or δ must lie below the direct-detection bound. F1 (α drift)
is unaffected: x is pinned (D417). No scored result → WALL.

**D449 (cycle 34, "pp"; third pass PART 11, WHOLE; scored, locked PREREG_D449_MS_FROM_XE; results/ms_from_xe_d449.txt) — CONSISTENT: the
volume at capture predicts a string scale inside the window the capture and plateau tests needed.** At x_E = 29.6 the volume is
𝒱 = (2x_E)^{3/2} = 455.5 (string units), so M_s/M_P = g_s^{1/4}√(π/𝒱) = 0.047–0.070 for g_s = 0.1–0.5 (M_s ≈ 1.1–1.7×10¹⁷ GeV), inside the
D446+D439 window 0.03–0.1. Without the √π convention factor the band is 0.026–0.039, which still overlaps (the g_s = 0.1 end falls just below
0.03). Not fitted: the window came from dynamics (capture and plateau), the band from geometry. Caveats: the toy torus fluxes and the single-modulus
volume are not one geometry; and D439 held M_s fixed, whereas in string units M_s varies with volume during inflation (x ~ 1e-4). The
consistency is for the late-time scale only, and the plateau test should be redone with M_s(x) (next deep item, needs its own lock). CENTRE:
balanced. THIRD PASS DONE.

**D450 (cycle 35, "pp"; fourth pass PART 2, LEFT; scored, locked PREREG_D450_PLATEAU_MSX; results/plateau_msx_d450.txt) — OUTSIDE CONTROL:
in string units, the inflationary point sits at a sub-string volume.** At x* = 1.3e-4 the volume is 𝒱 = (2x*)^{3/2} = 4.2e-6, so
M_s/M_P = 490–730 (g_s 0.1–0.5) — string scale far above Planck. Taken literally, the screening energy would be 3e4–2e5 × the inflaton
energy (the δn_s, δr values printed are meaningless there and are not quoted). By the locked rule the string-unit formula does not apply, so
D439's fixed-M_s result stands only as an assumption. This confirms and sharpens the control flag already noted in D408/D409 (x ≲ 1): the whole
inflationary phase of Twist-2 lies outside the geometric (large-volume) regime. Possible ways out (not computed): a T-dual description
(x → 1/x-type duality maps small to large volume), or reading x during inflation as a different modulus/regime. Until one is shown, the
'inflation and Λ from one string modulus' claim carries this flag. CENTRE: no balance change, flag recorded; v2 paper must state it plainly.

**D451 (cycle 36, "pp"; fourth pass PART 2/11; scored, locked PREREG_D451_TDUAL; results/tdual_d451.txt) — "DUAL FRAME CONTROLLED, F NOT
MODULAR": T-duality would give control, but the Twist's F breaks it by ~120 orders of magnitude.** Under T → 1/T the inflationary point
maps to 𝒱′ = 1.9e6 (M_s′/M_P = 7e-4–1e-3): well inside the large-volume regime. Because K = −3 ln(T+T̄) changes only by a Kähler transformation,
the escape works only if V(1/x) = V(x), i.e. F(1/x) = ±F(x)/x³. The Twist's F is far from that: log₁₀[V(1/x)/V(x)] = −119.4 at x* (and +109.4
at x_E; 0 at the self-dual point x = 1, as it must be; ε makes no difference). The cliff factor exp[−n(1 − e^{−x/m₂})] is what breaks it.
Reading (not scored): a modular completion of F would make V symmetric about x = 1, which would put a mirror image of the Λ cliff at
x = 1/29.6 ≈ 0.034, on the field's path between inflation and capture. So the T-dual escape is not free: it would reshape the model. The
D450 control flag therefore stands. Remaining escapes: a non-geometric/Landau-Ginzburg description of the small-volume phase, or a
different modulus driving inflation. CENTRE: no change; flag stands (v2 list already updated by D450).

**D452 (cycle 37, "pp"; PART 2/5/11 link; scored, locked PREREG_D452_RESCALE; results/rescale_d452.txt) — CONTROL + CAPTURE COMPATIBLE:
a different (allowed) normalisation of the modulus removes the D450 flag at the level of 𝒱 ≥ 1–10.** K = −3 ln(T+T̄) is unchanged under
T → aT, so the roll is identical if F's scales move with it; only the map to the physical volume changes. With a = 3846 (𝒱 = 1 at the CMB
point) or a = 17852 (𝒱 = 10), the volume at capture is 1.1e8 / 1.1e9, so M_s at capture is 3e-5–1.4e-4 M_P (7e13–3.5e14 GeV), and the
D446 integrator still CAPTURES in all 8 cases (bounce to x = 29.36–29.37; the weaker soft slope returns the field later, once m_eff > H; final offset at
the float floor). The D446 "window" 0.03–0.1 M_P was therefore only the tested range, not a lower limit (D441's 0.068 bound was already
conservative). Plateau: with 𝒱(x*) = 1, M_s(x*) ≈ 1.0–1.5 M_P → D439's constant amplitude offset (absorbed by A_s) and δn_s ~ 1e-6. Checks: M_s at
capture (≥ 7e13 GeV) > H_inf ≈ 1.7e13 GeV; M_KK ≈ M_s/𝒱^{1/6} ≈ 1e13 GeV ≫ T_capture = 1.5e11 GeV. Not checked: how 𝒱 ≈ 1–10 at the CMB point
fares against α′ corrections (O(1) at 𝒱 ~ 1, so 𝒱 = 10 is the safer choice), and how the new M_s scale affects D447's hidden sector (masses ≲ 10 TeV
unchanged in form). D449's 'consistency' held for a = 1 only; with a ≈ 4e3–2e4 the string scale is ~1e14 GeV instead. CENTRE: balanced; the
D450 flag is downgraded from 'outside control' to 'marginal control (𝒱 ≈ 1–10) at the CMB point'.

**D453 (cycle 38, "pp"; fourth pass PART 3, LEFT; scored, locked PREREG_D453_TOWER_RESCALE; results/tower_rescale_d453.txt) — MARGINAL: the
D452 rescaling squeezes the KK tower toward the plasma temperature.** On D409's trajectory points, the minimum m_KK/T falls from 2.4e4 (a = 1) to
23.6 (a = 1000), 6.1 (a = 3846, 𝒱(x*) = 1) and 1.3 (a = 17852, 𝒱(x*) = 10). The minimum sits at N − N_e ≈ 4, x ≈ 12.7, T ≈ 8e12 GeV; M_s/T stays ≥ 29.
A margin m_KK/T ≥ 10 needs a ≤ 2356, which leaves 𝒱(x*) = 0.48 < 1. With the looser m_KK/T ≥ 3, a ≤ 7852 and 𝒱(x*) ≤ 2.9. So control at the CMB point
(𝒱 ≳ 1) and a cold KK tower after inflation pull in opposite directions. Only a narrow band, a ≈ 3.8e3–7.9e3 (𝒱(x*) ≈ 1–2.9, m_KK/T ≈ 3–6), satisfies both, and only
loosely. The D452 choice 𝒱 = 10 is excluded by this test (KK modes would be thermally produced, relic risk). O(1) conventions are as in D409 (factor-2 spread).
CENTRE: D452 is narrowed to a = 3.8e3–7.9e3; the control flag stays 'marginal'; the v2 list is updated.

**D454 (cycle 39, "pp"; fourth pass PART 4, L/R; arithmetic in code, no new model; results/part4d_window_d454.txt) — leptogenesis window
trimmed at the top by the rescaled KK scale; nothing breaks.** In the D453 band (a = 3.8e3–7.9e3) the late-time m_KK = M_P/(a x_E) = 2.1e13 /
1.05e13 GeV (D409 conventions), below D411's upper edge 2.5e13 GeV. A 4D right-handed neutrino needs M₁ < m_KK, so the window becomes
M₁ ≈ 7e8 (D440, κ ≈ 1) to ~1e13 GeV. D440's preferred values (2.9e10–2e11 GeV for m̃₁ = m_sol–m_atm) are untouched, and the temperature at
capture (1.5e11 GeV) still exceeds them. Hidden-sector heating (ε_h ≤ 1e-5, D447) adds negligible entropy (no washout of Y_B). No scored
result → WALL.

**D455 (cycle 40, "pp"; fourth pass PART 5/8; scored, locked PREREG_D455_THERMALISE; results/thermalise_d455.txt) — THERMAL in all 10
cases: the item D447 left out is now done, and D447 holds.** The hidden 2→2 rate λ⁴T_h/16π equals H at T_h = m for λ_th = 2.9e-4–5.1e-3
(m = 10 GeV–100 TeV, T_h/T = 0.10–0.32). Every coupling D447 needs (≥ 0.026) is 5–1000 × larger, so the hidden sector reaches its own
equilibrium before freeze-out, and the injected abundance (D446) is forgotten. Hand check at m = 1e4 GeV, ξ = 0.102: T = 9.8e4 GeV,
H = 1.35e-8 GeV, λ_th = 2.9e-3 ✓. CENTRE: the F5 conditional pass (D447) is now complete: lightest D7-charged state ≲ 10 TeV (1%) / ≲ 100 TeV (all DM).

**D456 (cycle 41, tick; fourth pass PART 6, RIGHT; scored, locked PREREG_D456_FLUX_LAMBDA; results/flux_lambda_d456.txt) — FINE: one unit of
D7 flux moves Λ by as little as 0.08%.** In the D438 toy with the fixed-cycle constant held: n₁ = 399/401 → x_E = 29.624/29.576, ΔΛ/Λ =
∓0.078%; m₁ = 9/11 → x_E = 25.84/33.68, ΔΛ/Λ = +14%/−12% (the D413 power law is only approximate for steps this large). Honest reading: within this
toy, the flux integers choose x_E, and hence the O(1) factor in Λ, from a fine set of options (steps ≪ the ~1–2% observational precision). So the Twist does NOT
predict Λ's O(1) value. It accounts for Λ's magnitude (the e^{−n} cliff, n = 124.1) and leaves an O(1) value picked by flux choice, as in a landscape.
Unknown: whether n itself is flux-fixed, and whether unit steps survive tadpole cancellation. CENTRE: no balance change; the paper-v2 wording 'Λ from the
cliff' should say 'magnitude from the cliff, O(1) factor flux-selected'.

**D457 (cycle 42, "pp"; fourth pass PART 7, RIGHT; arithmetic in code, estimate; results/part7d_axion_f_d457.txt) — the birefringence axion
in the rescaled geometry: consistent, nothing new scored.** If it is a closed-string axion of the large 4-cycle at capture (τ = 2ax_E =
2.3e5–4.7e5 in the D453 band), then f ≈ M_P/(√2 τ) = 3.7–7.6e12 GeV (1.5–3.1e-6 M_P), far below the D414 limit 0.1 M_P (WGC-friendly).
β depends only on c_γΔθ, so β = 0.277° still needs c_γ = 1.7–4.1. The photon coupling is then g_aγγ = c_γα/(2πf) = 2.6e-16–1.3e-15 GeV⁻¹, about 500×
below the ~6e-13 GeV⁻¹ X-ray bounds on ultralight axions (bound value quoted approximately). Its energy share is Ω_a ≈ 1e-12 (negligible). The mass m ~ 2–1e4
H0 must come from an instanton with e^{−S} tuned; not computed. No scored result → WALL.

**D458 (cycle 43, "pp"; fourth pass PART 8, RIGHT; scored, locked PREREG_D458_KK_RELIC; results/kk_relic_d458.txt) — "NEEDS NO KK PARITY".**
At the D453 pinch point (T = 8.2e12 GeV) the lightest KK modes (m = 5.0e13 / 2.5e13 GeV for a = 3846 / 7852) are partly thermal:
Y = 9e-5 / 7e-4 per species. If they were stable (KK parity) they would overclose by 1e19–4e19. They decay gravitationally in 3e-29–3e-28 s,
carrying 0.07–0.28% of the radiation energy, so the worst case (all into dark radiation) gives ΔN_eff = 0.005–0.021 per species. Added to the D430
budget (0.047) that is ≤ 0.07 < 0.14 for one species. The a ≈ 7.9e3 end becomes risky if several KK species are this light (e.g. ≳ 4 species → > 0.14).
Conditions: no KK parity (generic for a Calabi–Yau, unlike orbifold/UED-type setups) and few light KK species, which favours the a ≈ 3.8e3 end of the band.
CENTRE: balanced with conditions; F7 (ΔN_eff) margin narrows at the upper end.

**D459 (cycle 44, "pp"; fourth pass PART 9, L/R; scored, locked PREREG_D459_SOFT_MASS; results/soft_mass_d459.txt) — locked reading: by
N − N_e = 20 (T = 1.4e6 GeV) the field returns to the wall for m_s ≥ 1 GeV, not for an eV-scale (gravity-mediated) mass.** Return
temperatures: 7.5e6 (1 GeV), 7.5e7 (100 GeV), 2.4e8 (1 TeV), 7.5e8 GeV (10 TeV) — T_ret ∝ √m_s (×10 per ×100 in m_s, computed). At
m_s = 1e-9 GeV the field is still parked at x = 29.36 at N − N_e = 20. By the lock: either φ couples directly to the SUSY-breaking sector (m_s ≳ GeV)
or the D396 thermal trap holds the field. Post-lock extrapolation (not scored): T_ret(1 eV) ≈ 2.4e2 GeV, still long before BBN, so even gravity-mediated
masses would pin the field in time if the √m_s law holds outside the run. A longer integration (N − N_e to ~30) would settle this. While parked, x sits 0.24
below x_E (Λ is irrelevant at those times; F1: no SM coupling, D417). CENTRE: balanced, with condition 'm_s ≳ GeV or extended run'; D447's lightest
charged state could then be as light as m_s.

**D460 (cycle 45, "pp"; PART 9/5; scored, locked PREREG_D460_EV_RETURN; results/capture_ext_d460.txt) — RETURNS BEFORE BBN, and the D459
√m_s law holds as predicted.** Integrating on to N − N_e = 32 (T = 8.7 GeV): with an eV-scale (gravity-mediated) soft mass m_s = 1e-9 GeV
the field returns to the wall at T = 2.37e2 GeV (predicted beforehand 2.4e2), and with 1e-6 GeV at 7.48e3 GeV (predicted 7.5e3). Both then
settle on the wall. The g* = 106.75 approximation is valid down to these temperatures (above the electroweak scale). So the eV gravitino of D430 is
enough by itself: φ needs no direct coupling to the SUSY-breaking sector, and the D396 thermal trap is not needed. CENTRE: balanced; the D459
condition is removed. A pre-registered prediction confirmed (within this toy).

**D461 (cycle 46, tick; fourth pass PART 10, RIGHT; arithmetic in code, standard formula; results/part10d_gauge_d461.txt) — the SM cannot live on
D7-branes wrapping the Twist's cycle in the rescaled geometry; it must sit on D3-branes or a small cycle.** With f = T for D7 on the rolling 4-cycle,
1/g² = Re T_phys = a x_E = 1.1e5–2.3e5 in the D453 band → α = 1/(4π Re T) ≈ 7e-7–3e-7, ~6e4–1e5 × weaker than α_GUT ≈ 0.04. So the SM sits on D3-branes
or a small blow-up cycle (the standard LVS arrangement), consistent with F1/D417 (no SM coupling to the rolling modulus through f), and the
D7 that carries the FI term is a hidden brane (g = 0.7 was assumed in D437–D446 for it, which then requires that hidden D7 to wrap a different, small
cycle whose volume is ~1/(4π·0.49) ≈ 0.16 in units where the gauge coupling is 1/Re T). Open: the FI term of D438 used fluxes on the large cycle; consistency of
'small-cycle hidden D7 with g = 0.7' and 'FI depending on the large cycle' needs a magnetised D7 wrapping a combination; not checked. No scored result → WALL.

**D462 (cycle 47, back-to-back run "till null"; fourth pass PART 11, WHOLE; structural reasoning, no computation) — the hidden FI brane needs a
Calabi–Yau with NON-diagonal intersections; swiss-cheese geometries are excluded.** For a magnetised D7 on divisor D with J = Σ tᵢDᵢ, the FI term is
ξ ∝ (1/𝒱)Σᵢ tᵢ (D·Dᵢ·F) and its coupling is 1/g² ≈ Re T_D (D461 needs a small cycle, Re T_D ≈ 0.16 for g = 0.7). For the FI term to track the Twist's
large cycle t_b, the triple intersection D·D_b·F must be non-zero. In swiss-cheese LVS models (𝒱 = τ_b^{3/2} − τ_s^{3/2}, the standard home of
'SM on D3/small cycle'), small and large divisors do not intersect (D_s·D_b = 0), so a small-cycle D7 has an FI term independent of the Twist. That would
remove the capture mechanism. So the geometry must be of fibred/non-diagonal type (e.g. K3-fibred CY with a small divisor meeting the big one,
as in fibre-inflation-type models), with the SM on D3s or a separate blow-up. This is a model-building condition, not a scored result → WALL.

**D463 (cycle 48, "pp"; fifth pass PART 1/5/8 → F7; scored, locked PREREG_D463_HIDDEN_DR; results/hidden_dr_d463.txt) — SAFE: the hidden radiation
that the φ remnant annihilates into adds ΔN_eff = 0.013, but this sets a new upper limit on the energy share, ε_h ≤ 5.5e-5.** With g_h = 10
light hidden dof and the D446 ceiling ε_h = 1e-5, T_h/T = 0.102 at capture rises to 0.218 at BBN (SM entropy dumps), giving ΔN_eff = 0.013. Total budget
0.047 (gravitino, D430) + 0.005–0.021 (KK, D458) + 0.013 = 0.065–0.081 < 0.14. ΔN_eff ∝ ε_h, so the limit is ε_h ≤ 5.5e-5 (worst KK case). The hotter
D447 case ε_h = 1e-3 (T_h/T = 0.32) is excluded (ΔN_eff = 1.3), so only D447's colder column applies. Margin: ×5 above the D436/D446 estimate ≤ 1e-5.
Prediction sharpened: total ΔN_eff ≈ 0.06–0.08 (CMB-S4 σ ≈ 0.03 → 2–3σ reach). The v2 list is updated (ΔN_eff 0.02–0.06 → 0.06–0.08 if the hidden sector is present).
CENTRE: balanced.

**D464 (cycle 49, "pp"; fifth pass PART 2, LEFT; literature + arithmetic in code; results/part2e_fibre_d464.txt) — prior-art overlap: Route A's
(n_s, r) sits on the fibre-inflation line.** D462 requires a fibred Calabi–Yau, which is the home of fibre inflation (Cicoli–Burgess–Quevedo,
0808.0691; 1603.06789), an α-attractor-like class with r ≈ 3α(1 − n_s)², α ≈ 2. The Twist's Route A point (n_s = 0.9736, r = 0.0046) gives
r/(1 − n_s)² = 6.6, i.e. α_eff = 2.2; the fibre line (α = 2) gives r = 0.0042 at the same n_s. So, in (n_s, r), Route A cannot be told apart from fibre
inflation; the undeformed Twist (α = 1, Starobinsky-like, B1) could, but it is disfavoured by the crown fit (D410). What still differs: the Twist ties
the same field to Λ and to the capture/FI sector (D436–D463), and makes the ΔN_eff ≈ 0.06–0.08 and β_reio/β_rec predictions. Fibre inflation's
reheating/dark-radiation predictions (1809.01159) were not compared here (not read). Must be credited in v2. No scored result → WALL.

**D465 (cycle 50, fast loop; fifth pass PART 3, LEFT; structural reasoning, no computation) — the LVS dark-radiation problem (volume modulus →
its own light axion; e.g. 1809.01159 for fibre inflation) does not arise in the FI picture, for a structural reason.** The same intersection
number that D462 requires (D·D_b·F ≠ 0, so that the FI term tracks the Twist's cycle) also gives the Twist's axion y a Green–Schwarz shift charge
under the hidden D7 U(1). So y takes part in the Stückelberg mass (M_V ≈ g M_s ~ 1e14 GeV in the D453 band) and is not a light axion. This replaces
D382's mass argument (from the D373 stabiliser), which does not apply to the FI version. Also, after capture the Twist's residual motion drains into
φ through the bounces (D444–D447), not into a modulus → axion decay. Caveat: if several axions mix, the light combination may lie mostly along other cycles; its couplings are not
checked. No scored result → WALL.

**D466 (cycle 51, "pp"; fifth pass PART 4, L/R; scored, locked PREREG_D466_PORTAL_WINDOW; results/portal_window_d466.txt) — WINDOW OPEN; D426's
'thermal hidden sector via the lepton portal' option is now EXCLUDED.** If the portal equilibrated the hidden sector with the SM, its 10 light dof
would give ΔN_eff = 0.268 > 0.14. So the portal must stay out of equilibrium: y′ ≤ 4.2e-6 (m_ψ = 5e5 GeV) to 1.9e-4 (1e9 GeV), from Γ = H at T = m_ψ.
It still has to let ψ decay before BBN (y′ ≳ 1e-14–2e-16, D425), which leaves a window 4e8–9e11 wide. Correction to D426: only its 'colder hidden bath' branch survives,
and that branch is what D447/D463 use. CENTRE: balanced; leptogenesis (L-conserving ψ decays, D425) unaffected.

**D467 (cycle 52, "pppp"; fifth pass PART 5; scored, locked PREREG_D467_EPS_H; results/eps_h_d467.txt) — WITHIN D463 for all m_s, with a
large margin in the rescaled geometry.** At r = 1.43e-4 the summed bounce injection is ρ/s = 2.5e-12 / 7.9e-2 / 3.7e3 GeV for m_s = 1e-9 / 1 /
1e4 GeV, i.e. ε_h = 2e-23 / 7e-13 / 3e-8, all ≪ 5.5e-5. So the hidden dark radiation of D463 is far below 0.013 here, because the injection scales
roughly as m_s² r^{4/3}. Post-lock reading (not scored): (i) for a gravity-mediated eV soft mass the remnant is 2.5e-12 GeV ≈ 0.6% of DM even with no
annihilation at all, so D445–D447's removal conditions are not needed in that case; (ii) for m_s ≳ GeV the remnant exceeds DM and must annihilate, but with
ε_h this small the hidden bath is very cold (ξ ~ 0.02 or less) and D455's thermalisation threshold rises as ξ^{-1/2}. That case needs re-checking with the actual ξ.
CENTRE: balanced; F7 margin improves; F5 for m_s ≳ GeV flagged for a re-check.

**D468 (cycle 53, "pppp"; PART 8/5; scored, locked PREREG_D468_COLD_BATH; results/cold_bath_d468.txt) — OK in both cold-bath cases: the D467 flag is
cleared.** m = 1 GeV (ξ = 1.7e-3): λ_th = 0.002; holding the relic to ≤ 1% of DM needs λ ≥ 0.006 (thermal, perturbative). The 100% value lies below the scanned
λ = 1e-4 (no root), i.e. any λ ≥ 1e-4 gives less than all of DM. m = 1e4 GeV (ξ = 0.024): λ_th = 0.006, λ(100%) = 0.60, λ(1%) = 2.0, so it is thermal and
perturbative. The colder bath lowers the λ needed (0.60 vs D447's 0.91 at ξ = 0.10), which more than offsets the higher thermalisation threshold. Note on the
verdict logic: the NaN in the 1 GeV case fell through to 'OK', which is correct here (the 1% condition is the binding one). CENTRE: F5 passes for every m_s
tested (eV: no annihilation needed, D467; GeV–10 TeV: λ ≈ 0.006–2).

**D469–D471 + D472 (cycles 54–57, Danny "Pp x 20"; locked PREREG_D469_PROTON, _D470_UNIF, _D471_AXION_S; results/d469_d471.txt)**

**D472 (cycle 54; PART 6, RIGHT; literature) — DESI evidence status.** A 2026 review (arXiv:2602.05368) finds the evolving-DE preference is dataset-dependent and
sensitive to redshift-dependent SN calibration/selection residuals at the few×10⁻² mag level (its significance figures were not extracted). The Twist after capture
predicts w = −1 to high accuracy (frozen x; axion Ω_a ~ 1e-12, D457). So it stands or falls with ΛCDM on this point: if recalibrated SNe remove the preference,
it is fine; if DESI DR3 confirms w₀ > −1, the baseline is disfavoured (the thawing variant was already shown not to help, D410). No scored result → WALL.

**D469 (cycle 55; PART 10, RIGHT; scored) — EXCLUDED UNLESS FORBIDDEN: generic string-scale proton decay.** With M_X = M_s = 0.7–3.5e14 GeV (the D453 band),
τ_p ≈ M_X⁴/(α_U² m_p⁵) = 4e26–3e29 yr, against Super-K's > 2.4e34 yr; M_X ≳ 6e15 GeV would be needed. So baryon number must be protected. In D-brane
models it typically is: B is a perturbative global symmetry left over from an anomalous U(1), broken only by D-instantons with tiny e^{−S}. That becomes an
explicit condition on the SM D3 sector (no string-scale B-violating couplings; dimension-5 SUSY operators also forbidden). Result → walls 0.

**D470 (cycle 56; PART 11/10; scored) — NO STANDARD UNIFICATION BELOW M_s.** One-loop MSSM running (SUSY threshold 1e5 GeV) meets α₁ = α₂ at 2.4e15 GeV
(α₂⁻¹ − α₃⁻¹ = 1.6 there), above M_s. At M_s = 7e13 / 3.5e14 GeV the inverse couplings are (33.0, 29.9, 26.0) / (31.4, 29.6, 26.8), so a D3 (non-GUT)
SM must match these at M_s through local string thresholds of size ~3–7. That is common in D3-at-singularity models, but it gives up GUT-style
unification as a prediction. Credit: low-string-scale non-unification is a known feature of LVS-type models. Result → walls 0.

**D471 (cycle 57; PART 7; scored) — NEEDS AN INTERMEDIATE CYCLE.** For m = 2–1e4 H0, f = 3.7–7.6e12 GeV and M_s = 0.7–3.5e14 GeV, the instanton action is
S = 242–267, i.e. a cycle of volume τ = S/2π ≈ 39–43. That lies between the small FI cycle (~0.16, D461) and the large Twist cycle (~1e5). So the geometry needs at least three
Kähler moduli (big, ~40, small), which fits a fibred CY with blow-ups (D462). It is a mild new prediction of the structure, not of a number. Result → walls 0.

**D473 (cycle 58; PART 8; scored, PREREG_D473_D475; results/d473_d475.txt) — NEEDS GAUGED STABILITY.** With M_s = 0.7–3.5e14 GeV, a 100–200 TeV gravity-only DM fermion
decays through generic M_s-suppressed operators in τ₅ = 1e-11–2e-9 s (dim-5) or τ₆ = 1e6–2.5e10 s (dim-6), far short of 1e28 s. It must be stable through a
gauged (discrete Z_N from a D-brane U(1)) symmetry, the F5 option 'stable by gauged symmetry', which is now mandatory. Result → walls 0.

**D474 (cycle 59; PART 9; scored) — minimal gauge mediation needs N ≥ 4 (√F = 140 TeV) to N ≥ 7 (65 TeV) messengers for a gluino > 2.3 TeV.** With no GUT
(D470), the bound is Landau-pole safety of α₃ up to M_s: α₃⁻¹(1e14) = 10.0 / 6.7 / 3.4 / 0.1 for N = 4/5/6/7 (computed). So N ≤ 5–6, which needs √F ≳ 85–106 TeV
and narrows the gravitino window to **m₃/₂ ≈ 1.7–4.7 eV** (was 1–4.7). This refines D430's prediction and gives a v2 entry. Result → walls 0.

**D475 (cycle 60; PART 2; scored) — NOT DISTINGUISHABLE by running.** Route A α_s = −7.1 to −8.4e-4 vs the fibre/α-attractor line −3.5e-4 at n_s = 0.9736: the
difference is 3.6–4.9e-4, i.e. 0.2σ for σ(α_s) ≈ 2e-3 (approximate forecast). So the D464 overlap with fibre inflation is not broken by α_s either. WALL.

**D476 (cycle 61; PART 1/10, RIGHT; scored, locked PREREG_D476_KINK_FIFTH; results/kink_fifth_d476.txt) — SCREENED: the pinned Twist exerts no fifth
force anywhere, even with a universal (volume-modulus) matter coupling.** At the wall the potential has a kink with one-sided slope
k = m_s² r² M_P² ζ′ c x_E = 3e8–7e9 GeV⁴ for an eV soft mass and 3e34–7e35 GeV⁴ for 10 TeV, equal to matter densities of 7e25–2e53 g/cm³. Real matter
(water 1, Earth's core 13, neutron star 1e15 g/cm³) pushes with βρ ≪ k, so the field does not move at all (the hard wall blocks pushes the other way). The response is
linear-threshold, not Yukawa, so there is no long-range force to bound. This removes the usual volume-modulus fifth-force/EP problem (MICROSCOPE, Cassini) for
the Twist without tuning β. It complements F1 (no α drift, D400/D417). Result → walls 0.

**D477 (cycle 62; PART 6; scored, PREREG_D477_D478; results/d477_d478.txt) — STABLE: our vacuum at x_E is metastable in principle but lives
forever in practice.** The stringy FI term has a second zero at x_E2 = 135.1, where the cliff energy is lower (Λ₂ ≈ 0.23 Λ, approximate). The barrier is
the D-term bump (ζ_max = 0.0274 at x = 63.2, V_b = 1.5e-22–1.8e-8 M_P⁴ for r = 3e-5–0.1) across Δφ = 1.86 M_P. Thick-wall estimate S ≈ 1e10–1.6e24, so decay
∝ e^{−S}, which is negligible (O(10) uncertainty in S is irrelevant). This is a new structural feature: the Twist's landscape has (at least) a lower-Λ neighbour,
safely separated. Result → walls 0.

**D478 (cycle 63; F4; scored) — NO ISOCURVATURE from φ.** During inflation (𝒱(x*) = 1) the screening field's D-term mass is m_φ ≈ g|ζ|^{1/2}M_s(x*) = 1.0–1.6e18 GeV
= 6e4–9e4 H_inf, so it is frozen and heavy, with no isocurvature or extra fluctuations. Result → walls 0.

**D479 (cycle 64, tick; PART 8, RIGHT; review only) — nothing new on DM beyond D467/D468/D473 from minutes ago.** Summary of DM status: gravity-only 100–200 TeV
fermion, stable by a gauged discrete symmetry (D473); optional second component from the lightest D7-charged state (≲ 10 TeV, λ ≈ 0.006–2, D468), or a ≈ 0.6%
remnant for an eV soft mass (D467). WALL.

**D480–D483 (cycles 65–68, Danny "Pp x 10"; locked PREREG_D480_D483; results/d480_d483.txt)**
**D480 (PART 9) PASS:** the sgoldstino (1.3e4–2.8e5 GeV) decays to γγ in τ = 1.6e-25–1.2e-20 s (bino 1 TeV, √F = 85–140 TeV), long before BBN. Result.
**D481 (PART 4) PASS:** if B − L is gauged and broken after inflation at v ≥ M₁, the strings have Gμ = 1.9e-17–8.4e-16 for v = 3e10–2e11 GeV. That is below
LVK O3's Gμ ≲ 4e-15 (PRL 126, 241102; model-dependent: 2.1–7.0e-15 for models B/C), with v_max = 4.4e11 GeV. Upgraded LVK/ET/CE could reach 1e-16–1e-18, so
this is a potential future signal if B − L is gauged. Result.
**D482 (PART 7) — B4 forecast missing:** LiteBIRD's isotropic-β paper (arXiv:2503.22322) forecasts σ(β) ≈ 0.02–0.045° for a single constant angle (5–13σ on 0.3°),
with no reionization/recombination split, so B4's distinguishability (D428) is not yet quantified in the literature we read (2108.09287 on tomography not read). WALL.
**D483 (PART 5) ROBUST:** halving or doubling the kinetic energy at N − N_e = 6 still captures. With 0.5× the field first hits at N − N_e = 14.1 (T ≈ 5e8 GeV);
with 2× it hits at 6.6 (T ≈ 9e11 GeV) and bounces to x = 26.75. Note: the capture temperature then spans ~5e8–9e11 GeV, so numbers quoted 'at T_cap = 1.5e11'
(ε_h, the D441 arrival speed) carry this spread. Leptogenesis is independent of capture. Result.

**D484 (cycle 69; PART 7; scored, locked PREREG_D484_B4_FORECAST; results/b4_forecast_d484.txt) — B4 quantified: for axion masses ≳ 50–100 H0 LiteBIRD can
test the Twist's tomography at 2–5σ (headline noise).** Using σ(Δβ) from arXiv:2108.09287 (0.05° headline; 0.09° with foreground residuals; 0.025° with
external delensing) and β_rec = 0.277°: m ≲ 10 H0 → Δβ ≈ 0 (indistinguishable from a constant angle or a calibration error); m = 50 H0 → Δβ = 0.09–0.21° → 1.9–4.2σ
(1.0–2.3σ with foregrounds; 3.8–8.4σ delensed); m ≥ 100 H0 → Δβ = 0.28° → 5.5σ (3.1σ with foregrounds; 11σ delensed). The Twist does not fix m
(D471's instanton S ≈ 240–270 spans 2–1e4 H0), so B4 is a conditional test: a measured Δβ ≈ 0.1–0.28° would point to m ≳ 50 H0 and a separate light axion.
Result → walls 0.

**D485 (cycle 70; F7 forecast; scored, PREREG_D485_D486; results/d485_d486.txt)** — total ΔN_eff = 0.065–0.081 is 2.2–2.7σ for σ = 0.03 (CMB-S4-class), 1.3–1.6σ
for 0.05 (SO-class), 0.4–0.5σ today (σ ≈ 0.17); σ values are approximate forecasts. So CMB-S4 would give a first hint, not a discovery. Result.
**D486 (cycle 71; PART 1, rigor for D476; scored) — PASS: rounding the kink by φ fluctuations leaves a field mass of 3.7e10 GeV (range 5e-27 m), independent of m_s**
(k and the rounding width both scale as m_s²). So the pinned Twist has no light mode at all, and D476 (no fifth force) stands. Result.
**D487 (cycle 72; CENTRE audit) — reproducibility:** four of tonight's scripts (D439, D445, D449, D456) were re-executed and reproduce their saved outputs byte for byte
(determinism check, not a rerun to chase results). Result (audit).
**D488 (cycle 73; CENTRE) — numbers table updated:** papers/twist_v6/TWIST2_NUMBERS.md gains a 'D436–D486 FI picture' block (below). Result (consolidation).

**D489 (Danny 20:26 CT "look for golden ratio silver ratio overlaps"; scored, locked PREREG_D489_RATIOS; results/ratios_d489.txt) — NO MORE THAN CHANCE.**
Over 25 model outputs (all pairwise ratios), 4 ratios fall within 1% of φ, φ², or the silver ratio 1 + √2: 0.9736/0.3728 = 2.612 (φ²), 0.23/0.3728 = 1.621 (φ), and 4.1/1.7
= 2.412 (silver; counted twice because 1.7 appears twice in the set, a duplicate I did not catch before locking, which inflates the observed count). Random log-uniform sets of
the same size give 1.8 hits on average, and 10% of them give ≥ 4 (p = 0.10). So the overlaps are what chance gives. No golden/silver structure is supported.
Sefirot mapping recorded as an organisational aid (theory/deep/SEFIROT_MAP.md): the twin ladder already has the three-pillar form; the centre (Tiferet) is where
balance is checked. Not physics evidence.

**D490 (Danny 20:29 CT "Design one that does" [a Twist with an 'as above, so below' symmetry]; scored, locked PREREG_D490_MODULAR_TWIST + DEVIATIONS D1, D2;
results/modular_twist_d490.txt, first buggy run kept as _run1_bug.txt) — locked verdict "SYMMETRY KILLS INFLATION FIT" for the two pre-set ε values; the design
itself works.** Design: F_sym(x) = G(x) + x² G(1/x) with G the Twist's F. Then V_sym(1/x) = V_sym(x) exactly (checked to 1.4e-14). Inflation sits on the small-x
plateau, its mirror at large x, and Λ at the self-dual point x = 1, where the FI root is symmetry-enforced. Control: the code reproduces the original Twist
(n_s = 0.9651 / 0.9736 for ε = 0 / 3.04e-7). Fixing Λ at x = 1 needs n = 233.9 (vs 125). Then n_s = 0.9651 (ε = 0, 2.9σ low) or 0.9817 (ε = 3.04e-7, too high),
both outside the 2σ window. Fixes before rerun: D1 (wrong V formula: |F|²/(4x²), not /(T+T̄)³) and D2 (an edit typo).
**D491 (scored, locked PREREG_D491_MODULAR_ROUTEA; results/modular_routeA_d491.txt) — VIABLE WITH ONE FIT.** With ε fitted to n_s = 0.9736 (as Route A),
ε = 1.61e-7, n = 233.9, x* = 6.6e-5. Predictions: r = 0.00453, α_s = −8.0e-4 (r/(1 − n_s)² = 6.5, i.e. the same fibre-like line as Route A). So the symmetric 'Twist-M'
fits the data as well as Route A, with the same number of fitted parameters, and adds a structural reason for the capture point: the self-dual point of the duality.
Consequences, NOT yet recomputed: capture moves from x_E = 29.6 to x = 1, so every capture-side number of D436–D489 (volume at capture, M_s, KK band, ε_h,
T_cap) must be redone for Twist-M. Also, the mirror plateau at large x means a region that starts at large volume would also inflate and roll down to x = 1. Status: candidate
variant, not the baseline.

**D492 (Twist-M cycle M1, Danny "Pp x 20 on this design"; scored, locked PREREG_D492_TWISTM_HISTORY + DEVIATIONS D1 [closure bug, first run kept];
results/twistm_history_d492.txt) — SELF-RELAXES TO x = 1: with no FI capture at all, the Twist-M field tracks the background and arrives at the self-dual point
just as dark energy takes over.** History (single field + radiation + matter, from the end of inflation at x = 4.7e-3, Ω_r0 = 0.0075):
 - kination (N ≈ 0–5, w = +1); overshoot to x ≈ 11.7, then pushed back by the mirror wall;
 - tracking through the radiation era (Ω_x ≈ 3e-4, w ≈ +0.33) while x slides from 5.3 (N = 10) through 3.5 (N = 20) and 1.68 (N = 40) to 1.12 at equality;
 - near today x = 0.9992 (z ≈ 1.7, w = −0.996) and x = 1.0001 at N_tot (w = −0.999).
Readings: (a) |ln x_today| = 1e-4 < 0.05 PASS. (b) Ω_V today = 0.15 at the assumed N_tot = 63.5 (vs 0.69). Λ is set by n through an approximate calibration
(V_inf ≈ 4e63 GeV⁴, N_tot ± 1). Ω_V reaches 0.69 about 0.84 e-folds later, inside that uncertainty, so this is not a failure but needs an exact calibration. w ≈ −1 today.
(c) BBN: Ω_x = 3e-4 at T ~ MeV ≤ 0.05 PASS (≈ +0.002 to ΔN_eff, estimate).
Meaning: the duality makes x = 1 a true minimum of V (V′(1) = 0 by symmetry), and the tracker brings the field there when the background density drops to V(1) = Λ,
i.e. late. The capture sector (D436–D468) is NOT needed for the field to reach x = 1 in Twist-M. Open: the field's mass at x = 1 is set by Λ (ultralight), so
fifth forces / α drift (F1) must be re-checked; the FI kink may still be needed for that (next cycle).

**D493 (Twist-M M2; scored, locked PREREG_D493_TWISTM_MASS; results/twistm_mass_d493.txt) — FIFTH FORCE UNLESS SCREENED.** At the self-dual point V′ = 0 exactly (checked),
and κ = d²lnV/dφ² = 9378, so m = √(3Ω_Λκ) H0 = 139 H0 = 2.0e-31 eV (range 32 Mpc). The field is already oscillating (it started at z ~ 27), consistent with D492's
small residual kinetic energy. A volume modulus with β = 1/√6 would give 2β² = 0.33 ≫ Cassini's 2.3e-5. So Twist-M still needs the FI kink, now at x = 1. Structural
reading (not computed): the duality swaps the two branes, so on the x > 1 side the opposite-charge field screens the D-term. The kink is then two-sided
(V ≈ m_s²|ζ|M_s² on both sides) and D476's screening (threshold ≫ any matter density) carries over. Also, the field now reaches x = 1 by slow tracking, not by a
fast hit, which suggests the non-adiabatic φ remnant of D444–D447 is absent (to be checked).

**D494–D496 (Twist-M M3–M5; scored, locked PREREG_D494_D496_TWISTM; results/twistm_late_d494.txt)**
**D494:** exact calibration V_* = (3π²/2)A_s r M_P⁴ = 4.95e63 GeV⁴ → Λ/V_* = 5.05e-111 → n = 234.05 (was 233.90; ε held).
**D495 — Λ-LIKE:** defining today as Ω_x = 0.69, the field sits at x = 1.00004 with w₀ = −1.0000 and w_a = +0.0001. The early-dark-energy share at recombination is
Ω_x = 1.7e-4. So Twist-M looks exactly like ΛCDM at late times (it does NOT explain a DESI-type w₀ > −1). Caveat (my setup): matter–radiation equality was held at
63.5 − ln 3400 while 'today' came out at N = 64.40, so z_eq in this run is ~8000, not 3400. The late-time w is insensitive to that, but Ω_x(rec) carries a factor-~2 uncertainty.
**D496:** kination lasts 3.28 e-folds (D391 assumed 1.5), so N* rises by ≈ +0.89 and n_s by ≈ +5.4e-4. The fitted ε of D491 must be lowered slightly (re-fit pending), and
r stays ≈ 0.0045.

**D497 (Twist-M M6; scored) — PASS:** with a = 7599 (𝒱 = 1 at x* = 6.6e-5), the KK tower stays above the plasma: min m_KK/T = 3.4 at N = 4.3 (x = 6.9, T = 1.4e13 GeV),
during the overshoot. Marginal, like D453 (the same ~3–6 band).
**D498 (Twist-M M7; scored; locked verdict 'CHECK') — the FI sector and the tracker picture are INCOMPATIBLE as they stand; this is a real tension.** The remnant formula
gave a residual 'share' of 2.5e15, which is impossible, and the reason matters. With M_s = 2.7e15 GeV (𝒱(1) = 1.2e5), the FI condensate's soft energy away from the root,
m_s²|ζ|M_s² ~ 7e12·|ζ| GeV⁴ even for an eV soft mass, dwarfs the tracker's energy (ρ ~ 1e-43 GeV⁴ near arrival). So if the FI sector exists, D492's history (which
left it out) is wrong: the FI soft slope would grab the field and pin it at x = 1 early, as in the original capture, bringing back the bounce/remnant issues (D444–D468) for
re-check. If the FI sector does not exist, D493's fifth force is unscreened. Twist-M therefore needs ONE of: (i) FI present → recompute the capture with x_E = 1 (the D446 machinery
applies; the remnant conditions return); (ii) no FI, with another fifth-force suppression (β ≲ 3e-3 for the volume modulus, i.e. matter not coupling through the volume, or a
different screening). D492's self-relaxation result stands only for case (ii).

**D499 (Twist-M M8; CENTRE consolidation) — Twist-M status after D490–D498.**
Works: an exact duality V(1/x) = V(x) (D490); fits n_s/r/α_s with one fitted ε like Route A (D491: r = 0.0045, α_s = −8e-4); Λ at the symmetry-fixed point x = 1 with n = 234.05 (D494);
late-time w₀ = −1.0000, w_a ≈ 0 (D495); EDE at recombination ~2e-4; KK tower marginal-OK (D497); vacuum = global minimum (V′(1) = 0, mirror plateaus).
Tension: the tracker 'self-relaxation' (D492) and fifth-force screening (D493) cannot both hold with the same FI sector (D498). Case (i), FI present: the field crosses x = 1 during
kination (N ≈ 1–2), overshoots, and is pulled back by a two-sided V-shaped soft potential (duality-screened on both sides). That is the original capture story moved to x = 1, so
the remnant conditions (D444–D468) apply again; an eV soft mass keeps them mild (D467-type). Not yet run. Case (ii), no FI: needs β ≲ 3e-3. Corrections pending: ε re-fit for
the longer kination (D496: ΔN* = +0.89). Next decisive computation: the full case-(i) run (Twist-M + two-sided FI + radiation from the end of inflation).

**D501 (cycle 76, "pp"; Twist-M PART 2; scored, locked PREREG_D501_TWISTM_REFIT; results/twistm_refit_d501.txt) — Twist-M predictions after the kination correction.**
At N* = 58.09 (D496), ε = 1.494e-7 gives n_s = 0.9736 with **r = 0.00435, α_s = −7.6e-4** (was r = 0.00453, −8.0e-4 at N* = 57.2). The Λ condition moves n only to 234.017
(held 234.054; a 0.02% change, negligible). Twist-M's r now sits slightly below non-symmetric Route A (0.0046) and just above the fibre line (0.0042): distinguishing them
needs σ(r) ~ 1e-4, beyond planned experiments. Result → walls 0.

**DEEP 1 (deep loop tick, topic 1 pinning/capture; literature; theory/deep/DEEP_topic1.md).** Prior art found and compared:
(a) arXiv:1110.3333 (Cicoli et al.): magnetised-D7 FI terms fix a combination of Kähler moduli for non-diagonal divisors in K3-fibred CYs, and the U(1) eats an axion.
This confirms D462/D465, and the static fixing is theirs.
(b) hep-th/0403001 (Kofman et al., 'Beauty is attractive') and 1310.4751: moduli trapping at enhanced-symmetry points by non-adiabatic particle production. That is our D444/D446
bounce production, which they show aids trapping. Twist-M's self-dual point is the classic T-duality enhanced-symmetry point.
No contradictions. Credits are added to the v2 list. The novelty claim narrows to the cosmological chain (inflation → capture → Λ) and the stringy small-volume FI treatment.

**DEEP 2 (Danny "Deep", 21:03 CT; topic 2 inflation / Twist-M; literature; theory/deep/DEEP_topic2.md).** Duality-symmetric (modular) inflation is established prior art
(1604.02995, 2403.02125, 2503.13682, 2411.18603); moduli attraction to fixed points (2211.00659); dark energy near the S-dual point (2506.02731, but there on a hilltop with w₀ ≈ −0.8).
Twist-M's distinct content: one duality-symmetric modulus giving inflation on the small-x plateau and Λ at the self-dual MINIMUM (w₀ = −1). That is distinguishable from 2506.02731
by w₀. Credits go to the v2 / any Twist-M write-up. No contradiction with D490–D501.

**DEEP 3 (Danny "Continue", 21:05 CT; topic 3 kination/reheating; literature + scaling estimate; theory/deep/DEEP_topic3.md).** Twist-M's history (D492: inflation → kination →
tracking → dark energy) is the quintessential-inflation scenario (Peebles–Vilenkin; Dimopoulos; quintessential α-attractors 2311.02730). It differs only in the end point, a
duality-fixed minimum (w₀ = −1), not a runaway. Credit the class. The kination GW peak rises ~35× for Twist-M's 3.3 e-folds (estimate) to ~2e-14 at high frequency, still undetectable
(2111.01150, 2307.12913).

**DEEP 4 (Danny "Again", 21:06 CT; topic 4 leptogenesis; literature + reasoning; theory/deep/DEEP_topic4.md).** The kination–leptogenesis link is known (0707.1544, 1911.02657);
credit it. In Twist-M, kination ends (T ~ 1e13 GeV) before M₁ ≈ 3e10–2e11 GeV, and the tracking field shifts H by ~1.5e-4 only. Leptogenesis is unchanged.

**DEEP 5 (Danny "Again", 21:07 CT; topic 5 capture/screening; literature).** No direct prior art for a V-shaped minimum turned up in the screening literature (1011.5909), but on
reflection D476/D486 amount to 'the field is heavy (3.7e10 GeV) at its minimum'. That is the ordinary heavy-modulus result, not a new screening mechanism, and no novelty is claimed.
It does mean the conclusion (no fifth force) is robust.

**DEEP 6 (Danny "Again", 21:08 CT; topic 6 Λ; literature).** Prior art for 'Λ from an exponential': Demirtas–Kim–McAllister–Moritz–Rios-Tascon (2107.09064, 2107.09065) build explicit
flux vacua with exponentially small W₀ and vacuum energy (even 1e-144). The Twist's cliff is the phenomenological version, and they get credit. A new connection to test (not a claim):
n ≈ 234 ≈ 2π × 37, close to the τ ≈ 39–43 cycle that D471 needs for the birefringence axion's mass. One intermediate cycle might set both Λ and the axion mass. It needs a lock.

**D502 / DEEP 7 (Danny "Again", 21:10 CT; topic 7 birefringence axion; scored, locked PREREG_D502_ONE_CYCLE; results/one_cycle_d502.txt) — CONSISTENT (k = 1) for Twist-M,
INCONSISTENT for Twist-2.** One intermediate cycle τ_c ≈ 40 can set both Λ's cliff (n = 234 = 2π × 37.2) and the birefringence axion's mass (S = 252–269, τ_c = 40–43). n/S = 0.93 at
m ≈ 1e4 H0 is 7% from 1. Twist-2's n = 125 gives n/S ≈ 0.5, which is not an integer within tolerance. Mild support only: identifying the cliff exponent with a unit-charge instanton action is
an O(1)-uncertain step, and the 15% tolerance was generous. If it holds, it gives a falsifiable prediction. The axion is then at the heavy end, so β at reionization ≈ 0, while β at recombination =
0.28° (Δβ ≈ 5.5σ at LiteBIRD's headline noise, D484). Result.

**DEEP 8 (Danny "Pp", 21:11 CT; topic 8 DM; literature).** The Twist's gravity-only DM is a Planckian-interacting-DM instance (Garny–Sandora–Sloth; 1709.09688, 1810.01428,
2003.07366), so it gets credit. Because the gravitational freeze-in yield scales as T_max³, the 100–200 TeV window is model-history dependent. It must be recomputed for Twist-M
(longer kination, different T_max) before being quoted. Open item, not computed.

**D503r (Danny "Pp", 21:12 CT; follow-up of DEEP 8; reasoning from D112, no new computation) — Twist-M's DM window mostly carries over.** D112: ≥ 99% of the gravity-only DM
comes from bremsstrahlung in the χ̃ (heat-sector) decays, a yield that does not depend on the DM mass or on T_max. The T_max³-sensitive freeze-in part supplies ≤ 1%. With the same
heat sector (heat share 0.75%, as D492 assumed), Twist-M keeps m_DM ≈ 100–500 TeV (100–200 TeV after D415). What changes: any dilution (Twist-M has no separate dilution step;
D397's D factor does not apply) and the freeze-in sliver. The DEEP 8 flag is downgraded to 'freeze-in sliver only'. Label: estimate, not recomputed.

**DEEP 9 (Danny "Pp", 21:13 CT; topic 9 SUSY/gravitino; literature).** The Higgs mass bounds an eV gravitino from below: with perturbative messengers m₃/₂ ≳ 10 eV, which the 4.7 eV
cosmology bound excludes. Only a strongly coupled messenger sector leaves ~0.8–4.7 eV (arXiv:1608.01610). The Twist's window 1.7–4.7 eV (D474) fits, and D432 already assumed strong coupling.
That makes it an explicit condition: strongly coupled SUSY-breaking/messenger sector. Future 21 cm data (1605.09191) can test m₃/₂ ~ 1 eV. Credits: 1601.07386, 1608.01610.

**D504 / DEEP 10 (Danny "Pp", 21:15 CT; topic 10 gauge couplings; scored, locked PREREG_D504_TWISTM_UNIF; results/twistm_unif_d504.txt) — UNIFICATION BELOW M_s in Twist-M.**
Twist-M's string scale (2.65e15 GeV) sits just above the MSSM-like meeting point (M_12 = 2.41e15 GeV, ratio 0.91). The couplings at M_s agree to 1.6 in α⁻¹ (~5%). Twist-2 had no
such match (D470). Proton decay: X-bosons at 2.4e15 GeV would give τ_p ≈ 6e32 yr, below Super-K's 2.4e34. So the match must be string-scale (D-brane) unification without light X-bosons,
with baryon number protected (D469). It is a mild point in Twist-M's favour, and it comes from geometry, not a fit.

**DEEP 11 (Danny "Pp x 10", 21:16 CT; topic 11 string embedding; literature).** Exact T-duality on a Kähler modulus is a property of toroidal compactifications and orbifolds
(hep-th/9401139; modular-invariant condensates in Z_N orbifolds, hep-th/9510022, hep-ph/9210219), not of generic Calabi–Yaus. TENSION: Twist-M's exact duality points to an orbifold,
while the FI capture wanted a fibred CY with intersecting divisors (D462). A possible reconciliation, not checked, is a IIB orientifold of a toroidal orbifold with blow-up cycles.
This is now the main open string-side question for Twist-M. DEEP PASS 1 COMPLETE (topics 1–11).

**DEEP 2.1 (Danny "Deep", 21:16 CT; pass 2 topic 1: Twist-M embedding; literature).** The concrete class to look in is IIB orientifolds of T⁶/Z_N with fluxes and magnetised D7-branes
(arXiv:2404.18995; hep-th/0512287). They have the ingredients: magnetised D7s, blow-up cycles, and untwisted Kähler moduli as the natural carriers of a duality. But the dualities used there
act on the axio-dilaton (S) and complex structure (U), not on a Kähler modulus with fluxes and branes. Whether a Kähler-modulus SL(2,Z) survives in that setting is not established. DEEP 11's open question
stands, now with a concrete class to examine.

**DEEP 2.1b (Danny "Research like this again", 21:19 CT; Twist-M embedding; literature).** An exact SL(2,Z) is available in two places. (a) The heterotic orbifold volume modulus:
exact perturbatively, weight −3 matching K = −3 ln(T+T̄), and fixed points always extrema (2411.06516). (b) An isotropic IIB complex-structure modulus U: exact SL(2,Z)_U with the same
K = −3 ln(U+Ū) (1608.06129, 1804.06644, 2404.18995). On IIB Kähler moduli no exact T-duality is established (0705.3253). In both homes the FI term does not depend on the
Twist field, so the FI-capture link does not carry over naturally. That favours Twist-M case (ii) and makes the matter coupling β (D498) the decisive question for that variant.

**DEEP 2.2 (Danny "Again", 21:20 CT; Twist-M case (ii) and matter coupling; literature + estimate in code; results/deep2_beta_estimate.txt).** In the natural homes for an exact
duality (DEEP 2.1b), the dual modulus usually sets the matter Yukawas: modular-flavour models make fermion masses functions of τ and therefore need the modulus heavy and stabilised
(2201.02020, 2506.23343, 2601.09542; 2211.00659). Twist-M's field is light at its minimum (m = 139 H0, D493). It is still oscillating today, with amplitude δφ ≈ 1.1e-4 M_P (from D492's residual kinetic
energy) and a period ≈ 0.045 Hubble times. A matter coupling β then makes masses oscillate by ~β × 1e-4. Quasar/Oklo-type bounds (~1e-6–1e-7, approximate) need β ≲ 1e-2 to 1e-3, as tight as or
tighter than Cassini (β ≲ 3e-3, D498). Conclusion (estimate): Twist-M case (ii) works only if the Standard Model is blind to the Twist field (no Yukawa or mass dependence). That is the opposite of
modular-flavour constructions, where the dual modulus IS the flavour modulus. So case (ii) needs a sector separation the literature does not supply by default. Case (i) (FI kink, heavy field) avoids
this but needs the embedding question solved. Both open; neither is closed by this tick.

**D505 (Danny 21:19 CT "add the split/lens as a variation"; scored, locked PREREG_D505_SPLIT_LENS; results/split_lens_d505.txt) — LENS SOLVES CASE (ii), with one caveat.**
Variant Twist-M-L: the mapped Twist-M scalar A (dark, duality-symmetric, light) and a 'quantum-side' modulus B that the SM actually feels (e.g. the flavour modulus, heavy, β_B ~ 1)
communicate only through a lens term μ²ΔAΔB. Integrating out B gives β_eff = β_B μ²/m_B², and stability of the pair forces μ⁴ < m_A²m_B², so β_eff < β_B m_A/m_B: the lens can only dilute.
For m_B = 1e-3 eV to 1e5 GeV, β_eff,max = 2e-28 down to 2e-45 and the oscillating-mass effect is ≤ 2e-32, far below Cassini (3e-3) and the varying-constant bounds (~1e-7). A's mapped
dynamics are untouched to that order. B's own force is short-ranged for m_B > 4e-3 eV. Caveat (the real condition): this covers potential mixing only. If A also enters the matter Kähler metric
or the gauge kinetic functions directly (as the volume does for D7/D3 matter), that coupling is not diluted. So the requirement becomes: A appears only in the dark sector's K and W, and talks
to the SM solely through the heavy B. That is a sharper, checkable model-building condition than 'SM blind'. Status: candidate variant on top of Twist-M.

**D500 status (note).** Cloud reruns D3 and D5 were both killed, the second with nothing else running, so the memory growth is in the script (LSODA over the fast late oscillation). A DOP853 test
crashed, so it is not a fix. D500 now waits on the PC route (DEVIATIONS D6).

**D506 (Twist-M-L cycle 1; scored, PREREG_D506_D507_LENS; results/lens_d506_d507.txt) — B must be ≳ 100 TeV.** If B (the SM-facing modulus) is displaced after inflation, it decays gravitationally
at T_dec = 0.01 / 0.17 / 0.90 / 5.5 MeV for m_B = 1 / 10 / 30 / 100 TeV. So m_B ≳ 100 TeV for BBN safety (the standard cosmological-moduli bound). Alternatively, B must never be displaced (its
minimum is the same during and after inflation). The sgoldstino/soft scales of D432 (1e4–3e5 GeV) are the same order: plausible. Result.

**D507 (Twist-M-L cycle 2; scored) — the lens is bounded by inflation too, but stability (D505) is tighter.** A moves ΔA ≈ 11.8 M_P during and after inflation, shifting B's minimum by μ²ΔA/m_B².
Keeping B's displacement ≤ 1e-7 M_P needs μ²/m_B² ≤ 8.5e-9, i.e. β_eff ≤ 8.5e-9 (4e5 × below Cassini). D505's stability bound (β_eff < m_A/m_B ≤ 2e-28) is far tighter still, so the binding
constraint remains stability. The lens is automatically weak enough that B is not dragged by A's large excursion. (The verdict label 'INFLATION BOUND DOMINATES' printed by the script compares only
with Cassini; against D505 it does not dominate.) Result.

**D508 (Twist-M-L cycle 3; structural reasoning) — a concrete home for the split.** On T⁶ = T²₁×T²₂×T²₃ (IIB orientifold), put the SM on D7-branes wrapping T²₁×T²₂, point-like in T²₃,
and take A = U₃, the complex structure (shape) of the third torus. (i) SL(2,Z)_{U₃} is an exact duality of the torus, giving Twist-M's symmetry. (ii) The SM gauge kinetic function f = T₃ involves
the 4-cycle volume, not U₃, and the SM matter Kähler metrics and Yukawas on branes transverse to T²₃ depend on U₁, U₂ (flavour-type) but not on U₃ at leading order. So A is naturally 'dark': the
D505 condition is met by geometry, not by assumption. (iii) B can be U₁ or U₂ (the flavour moduli, heavy), with A–B contact only through bulk/flux terms (the lens). Caveats: 3-form fluxes generically
involve all U's (need a flux choice leaving U₃ for the Twist superpotential), and brane-position moduli in T²₃ may couple. Open, but a specific, checkable construction.

**D509 (Twist-M-L cycle 4; reasoning) — where the cliff comes from if A = U₃.** IIB D-instantons depend on Kähler moduli, not U, so the exponential cliff e^{−n(...)} in U₃ must come from
large-complex-structure (mirror world-sheet-instanton-type) corrections to the flux superpotential, ~e^{2πiU}, the mirror of the IIA worldsheet instantons. A cliff with n ≈ 234 ≈ 2π × 37 then
needs a ~37-fold charge or winding. That is consistent in size with D502's τ_c ≈ 40 if the 'one cycle' is the mirror 3-cycle. Not computed; flagged.

**D510 (Twist-M-L cycle 5; literature anchor).** Toroidal IIB orientifolds with partial flux stabilisation leaving some complex-structure moduli flat are discussed in the classic
programme (hep-th/0506090 'Moduli stabilization in type IIB orientifolds (I)'; also 2004.04518, 2212.02533). This makes D508's requirement (fluxes leave U₃ for the Twist superpotential)
plausible, but it was not verified in a specific model this tick. Open.

**D511 (Twist-M-L cycle 6; arithmetic in code; results/lens_d511_neff.txt) — ΔN_eff for Twist-M-L.** With no FI hidden sector (case ii), the hidden-bath term of D463 is absent: ΔN_eff = 0.047
(gravitino) + 0.005–0.021 (KK) = 0.052–0.068, a 1.7–2.3σ hint at CMB-S4 (σ ≈ 0.03, approximate). Slightly lower than Twist-2's 0.065–0.081 (D485), so ΔN_eff could in principle separate
the variants. Result (estimate).

**D512 (Danny 21:23 CT "build on next, see if it sticks"; locked PREREG_D512_U3_K1 + DEVIATIONS D1; results/u3_k1_d512.txt, first run kept as _run1_superseded) — INCONCLUSIVE;
the printed verdict 'STICKS WITH CHANGED PREDICTIONS' is NOT valid.** Test: in the D508 home the Twist field is a single torus shape, so its Kähler potential is K = −ln(U₃+Ū₃) (k = 1), not k = 3.
V(x) can be kept, but the field's canonical length shrinks (φ = ln x/√2 instead of √(3/2) ln x). The control (k = 3) reproduces D501 exactly. With k = 1: at ε = 0, n_s = 0.9658, r = 0.0012; at
ε = 1e-8, n_s = 0.9705, r = 0.0013; at ε = 1.494e-7, n_s = 1.097, r = 0.017. The refit's 'root' ε = 1.64e-8 returned n_s = 1.097, identical to the ε = 1.494e-7 point. So brentq found a JUMP, not a
root: the end-of-inflation point switches branch (x* jumps to 1.0e-5) between ε = 1e-8 and 1.6e-8. No reruns (locked). Honest reading: with k = 1 the Twist-M plateau gives n_s up to ≈ 0.970
(1.3σ below CMB-SPA+DESI's 0.9728 ± 0.0027) with r ≈ 1.3e-3 (≈ ⅓ of k = 3, as α-attractor scaling expects) before the solution becomes unstable. A clean fit at 0.9736 was not demonstrated. So the
single-torus home does not cleanly stick. Options: an isotropic three-torus Twist (k = 3, U₁ = U₂ = U₃) but then the SM couples to it (conflicts with D508), or a finer ε scan / different deformation
(new lock). Status: D508's home is in doubt for inflation.

**D513 (Danny 21:25 CT "do a single torus and build it like it's meant to be in our model"; scored, locked PREREG_D513_TWIST1T; results/twist1t_d513.txt) — Twist-1T FITS CMB-SPA,
not SPA+DESI.** Twist-1T: the Twist field is the shape U of one torus that the SM branes do not wrap; K = −ln(U+Ū); exact duality; Λ at the self-dual square shape; NO ad-hoc tilt (ε = 0).
Predictions: n_s = 0.9658, r = 0.00116, α_s = −6.7e-4, cliff n = 232.8 (Λ), x* = 2.3e-5. Against CMB-SPA alone (0.9684 ± 0.0030): −0.9σ. Against CMB-SPA+DESI (0.9728 ± 0.0027): −2.6σ. So this is the
most predictive version so far (no fitted tilt; the inflation numbers follow from one torus + one duality + Λ), and its fate is tied to the CMB-vs-DESI n_s question. If DESI's pull on n_s
(the D410 crown fit's 0.9736) holds, Twist-1T is disfavoured at ~2.6σ; if the CMB-only value holds, it fits. r = 1.2e-3 is a sharp target (below LiteBIRD's ~2e-3 goal, so a null r is the
prediction). Status: candidate variant; predictions scored only by future data.

**D514 (Danny 21:27–21:28 CT, the polygon ladder; locked PREREG_D514_POLYGONS; results/polygons_d514.txt) — the ladder exists, and it is built from the triangle.**
(1) Crystallographic restriction (computed with Euler's φ): a 2D torus admits only N = 1, 2, 3, 4, 6 (flat/rectangle, triangle-hexagon, square). Pentagon, octagon, decagon and dodecagon (5, 8, 10, 12)
appear only with 4 extra dimensions, and 7, 9, 14, 18 with 6. These are exactly the Z_N orbifold orders string theory uses.
(2) Pythagoras: both special 2D shapes sit on the self-dual circle: |i|² = 1 and |ρ|² = (½)² + (√3/2)² = 1.
(3) In Twist-1T, evaluated off the real line, the triangle/hexagon point lies ABOVE the square point: ln V(ρ)/V(i) = +3.5. So the shape ladder in our potential runs flat (inflation) → triangle/hexagon
(higher, intermediate) → square (vacuum, Λ). Caveat: F_sym has only the T → 1/T part of SL(2,Z), so ρ is not guaranteed to be an extremum here; a fully modular F would make it one.
Danny's reading ('it spreads out from the triangle') matches a real mathematical fact (stated, not computed): the higher-N symmetries come from simplex lattices, the higher-dimensional triangles. The A_n
lattice's Coxeter element is an (n+1)-fold rotation: A₂ (triangle) → 3/6-fold, A₄ → 5-fold (pentagon), A₆ → 7-fold, and E₆ → 12-fold (dodecagon, Coxeter number 12). So the polygon ladder IS the
triangle family scaled up in dimension. Test not yet run: whether a fully modular Twist with its vacuum at the triangle point (τ = ρ) also works (Λ, inflation).

**D515 (Danny 21:32 CT "Set this up", roadmap step A; toolkit theory/modular/ + selftest; scored, locked PREREG_D515_FULL_MODULAR + DEVIATIONS D1 [overflow crash, no first output];
results/full_modular_d515.txt) — VIABLE vs CMB-SPA: a FULLY modular Twist inflates like Starobinsky.** Toolkit check: j(i) = 1728, j(ρ) = 0 (2e-43), SL(2,Z) invariance of ln V to 3.6e-14.
Model: V = |H(j)|²/((2 Im τ)³|η|¹²) with H = (j−1728)^a j^{−¼−a} [ln(j/1728)]^{3/2}. Result, identical for a = ½, 1, 3/2 (a only shapes the region near τ = i): inflation on the cusp plateau at
Im τ ≈ 146, ending at Im τ ≈ 3.2, gives n_s = 0.9665 and r = 0.00323 (−0.6σ vs CMB-SPA, −2.3σ vs SPA+DESI). Sanity: V ∝ (1 − c/Im τ)³, an α = 1 attractor; Starobinsky's 1 − 2/N* = 0.9656 and
12/N*² = 0.0036 agree. Structure, by construction: the square torus τ = i is an exact Minkowski vacuum (V = 0), and the triangle/hexagon point ρ is a wall (V → ∞), so the field can never settle on the
triangle. Λ is NOT yet included: it needs a small extra term, the next step. So the full SL(2,Z) version works for inflation and naturally has the polygon structure (square = vacuum, triangle = barrier),
but its inflation numbers are the generic Starobinsky ones; any distinctiveness must come from the Λ term and the late universe.

**Naming (Danny 21:34 CT):** the fully modular Twist of D515 (exact SL(2,Z), V = |H(j)|²/((2 Im τ)³|η|¹²)) is called **SERAPIS**. Variant names in use: Twist-2 (baseline), Twist-M (T → 1/T
duality, D490), Twist-M-L (split/lens, D505), Twist-1T (single torus, D513), SERAPIS (full modular group, D515).

**D516 (SERAPIS step 2; locked PREREG_D516_SERAPIS_LAMBDA + DEVIATIONS D1 [double-precision floor; run1 kept]; results/serapis_lambda_d516.txt at 50 digits) — Λ added cleanly; inflation
untouched; but the vacuum is too FLAT (a light field): a design flaw to fix.** At 50-digit precision the c-term puts V(i)/V_plateau exactly on target (7.08e-111) with c = 6.7e-53 (a = ½) or
2.8e-51 (a = 1), i.e. an action S = −ln c ≈ 120 / 116 = 2π × 19.1 / 18.5. That is instanton-sized, so Λ could be an e^{−S} effect (a link to check against D502's τ ≈ 40: 19 ≈ half of 40). Inflation is unchanged
(the c-term changes V on the plateau by 0.0 at 50 digits). τ = i is a minimum in both directions. BUT the field mass there is tiny and set by numerics/c, not by the inflation scale: m ≈ 1.7e-4 GeV (a = ½)
and 5e-10 GeV (a = 1). The 1.7e5 GeV of run 1 was double-precision noise. Reason (analytic): near τ = i, j − 1728 ∝ (τ−i)², and ln(j/1728) ∝ (τ−i)², so |H|² of the main term vanishes like |τ−i|^{4a+6}. That is far
flatter than quadratic, so the vacuum curvature comes only from the tiny c-term. A light modulus brings back the fifth-force problem (D493). Fix for the next step: replace [ln(j/1728)]^{3/2} by a factor that
does not vanish at τ = i but still gives the cusp plateau (e.g. [ln(j/1728) + κ]^{3/2} or ln j), so the vacuum gets an inflation-scale curvature. New lock needed.

**D517 (SERAPIS-1, Danny 21:37–21:39 CT; scored, locked PREREG_D517_SERAPIS1 + DEVIATIONS D1 [50-digit floor; run1 kept]; results/serapis1_d517.txt at 200 digits) — VIABLE and STIFF:
the single-torus, fully modular Twist works end to end at this level.** K = −ln(2 Im τ), F = η^{−2}H(j), H = (j−1728)^{1/2} j^{−7/12}[ln(j/1728) + 1]^{1/2} + c·j^{−7/12}.
(1) Inflation on the cusp: n_s = 0.9667, r = 0.00108 (−0.6σ CMB-SPA, −2.3σ SPA+DESI), from Im τ ≈ 126 to the end at Im τ ≈ 2.1, with no fitted tilt. The κ = 2π sensitivity check gives n_s = 0.9685,
r = 0.00097: the constant κ moves n_s by ~0.002, a mild model dependence.
(2) Vacuum: τ = i (square torus) is a minimum in both directions, with V(i) exactly on the Λ target (2.11e-110 of the plateau).
(3) Vacuum mass m = 4.0e13 GeV, about 5 H_inf: STIFF, so no fifth force, no moduli problem and no need for the FI kink or the lens. The (j−1728)^{1/2} factor fixed D516's flatness.
(4) Λ's coefficient c = 1.6e-53, S = −ln c = 121.6 = 2π × 19.35, instanton-sized.
The triangle point ρ is a wall by construction (j^{−7/12}). Status: SERAPIS-1 is now the cleanest version. It is exactly modular, has one torus, inflation fits CMB-SPA with no tilt, Λ sits at the square torus
and the vacuum is heavy. Remaining: the CMB-vs-DESI n_s question decides it (−2.3σ with DESI); κ and the 'two secondary tori' are assumptions; Λ's c is one number fixed by data (an e^{−121.6} instanton
would explain it, untested).

**D518 (SERAPIS-1 reheating; scored, locked PREREG_D518_SERAPIS_REHEAT; results/serapis_reheat_d518.txt) — INCONSISTENT: SERAPIS-1's own reheating gives N* ≈ 52, not 58.09, so its n_s
drops by ≈ 0.005.** The heavy inflaton (m = 4e13 GeV) decays with Γ = (c_Γ/8π)m³/M_P² = 4.3e2–4.3e3 GeV → T_RH = 1.8e10–5.5e10 GeV. Hand check: ¼ln(V_*/M_P⁴) = −6.1 and
ln(k*/a₀H₀) = 5.4 give instant-reheating N* ≈ 55.5. A long matter-dominated reheating phase (w = 0) then subtracts (1/12)ln(ρ_end/ρ_RH) ≈ 4, giving N* = 51.6–52.0. With attractor scaling,
Δn_s ≈ 2ΔN*/N*² ≈ −0.0045 to −0.0049, i.e. n_s ≈ 0.962. That is −2.2σ vs CMB-SPA and −3.9σ vs SPA+DESI, so SERAPIS-1's D517 'fit' used the wrong N* (58.09 belonged to Twist-M's kination history).
Leptogenesis: T_RH reaches the lower part of the M₁ window (≥ 3e10 GeV only for c_Γ ≈ 10). Fix paths (new locks needed): a faster decay channel (c_Γ ≫ 10, e.g. direct coupling to the hidden/SM sector, which raises
T_RH and N*); or a kination phase like Twist-2's (needs a steep post-inflation direction, which SERAPIS's potential does not have near τ = i). Status: SERAPIS-1 is NOT yet self-consistent; the D517 'VIABLE' is
withdrawn pending this.

**DEEP 2.3 (Danny 21:43 CT "deep dive online … if this exists anywhere else, if not Zenodo"; literature) — SERAPIS largely EXISTS already; no Zenodo record (not novel enough).**
(a) arXiv:2405.06497 ('Modular invariant slow-roll inflation'): W = Λ³Ω(S)H(τ)/η⁶ with H = (j−1728)^{m/2} j^{n/3} P(j), K with modular weight 3. This is the same building block as SERAPIS (D515/D516),
with vacua at τ = i or ω and Starobinsky-like inflation. They note that a dS minimum needs a ~1e90 fine-tuning, the analogue of our c ≈ 1e-53 term for Λ.
(b) arXiv:2407.12081 ('Modular invariant Starobinsky inflation and the species scale'): V ∝ (Im τ)²|G̃₂|²/N² with N ≃ −log(Im τ|η|⁴), a log-type factor giving a Starobinsky plateau at the cusp, as our
[ln(j/1728)]^{1/2 or 3/2} does.
(c) arXiv:2405.08924 (King–Wang, modular hilltop inflation) and 2411.18603 (modular inflation with reheating) complete the family.
Distinct in SERAPIS-1: the single-torus weight −1 version (K = −ln, F = η⁻²H) with the specific (j−1728)^{1/2} j^{−7/12}[ln(j/1728)+κ]^{1/2} combination and Λ placed at τ = i with a stiff vacuum. These are
variations inside a known family, not a new mechanism, and D518 found its reheating gives N* ≈ 52 (n_s ≈ 0.962), a tension the literature cases share or avoid by other choices. Decision: credit these papers; do NOT publish
SERAPIS to Zenodo as a novel result. Its value is as the duality-complete end point of the Twist line, inside the AEGIS write-ups.

**D519 (SERAPIS-1 at its own N*; scored, locked PREREG_D519_SERAPIS_NSTAR; results/serapis_nstar_d519.txt) — CANNOT REACH THE DESI VALUE; FITS CMB-SPA for every reheating history.**
Instant reheating gives N* = 55.58, n_s = 0.9652 (−1.1σ SPA, −2.8σ SPA+DESI), r = 0.00118. At N* = 54: 0.9642 / r = 0.00125. At N* = 52 (D518's gravitational decay): 0.9629 (−1.8σ SPA, −3.7σ SPA+DESI),
r = 0.00134, α_s ≈ −6.4 to −6.8e-4. So SERAPIS-1's real prediction is n_s ≈ 0.963–0.965, r ≈ 0.0012–0.0013. It is consistent with CMB-SPA alone at < 2σ throughout and in 2.8–3.7σ tension with CMB-SPA+DESI.
**D520 (reasoning + arithmetic from D519) — the two fix routes do not work.** (i) A faster decay cannot exceed instant reheating, so it buys at most +3.6 e-folds (n_s ≤ 0.9652). A Planck-suppressed decay of a
modulus cannot reach instant reheating anyway (it would need Γ ~ H_end ~ 1e13 GeV vs ~4e3 GeV). (ii) Reaching the SPA+DESI 2σ edge (0.9674) needs N* ≈ 59.3 (from n_s ≈ 1 − 1.934/N*), i.e. ~+3.7 e-folds beyond instant,
so ~7.5 e-folds of kination. SERAPIS's potential is quadratic near τ = i, with no steep runaway, so it has no kination phase. Conclusion: SERAPIS-1 makes a sharp prediction, n_s ≈ 0.963–0.965, that stands or falls with the
CMB-vs-DESI question. It is not 'fixable' within the model without adding structure.

**D521 (CENTRE, variant comparison; arithmetic in code; results/variants_d521.txt).** The variants split cleanly by data. With CMB-SPA alone, every untilted version fits (−1.4σ to −0.6σ): Twist-2 undeformed,
Twist-1T, SERAPIS k = 3, SERAPIS-1. With CMB-SPA+DESI, only the tilted ones fit (Route A, Twist-M: +0.3σ, each with one fitted ε), and every untilted version sits at −2.3σ to −3.2σ. One data question, whether DESI's
pull on n_s is real, therefore picks between 'predictive but DESI-tense' (SERAPIS-1, Twist-1T) and 'fits all but tuned' (Route A, Twist-M). The decisive future tests are n_s to ±0.002 (Simons Observatory/CMB-S4)
and r: ~0.001 (untilted single-torus) vs ~0.0045 (tilted). LiteBIRD/CMB-S4 reach σ(r) ~ 1e-3, which separates them at ~3σ.
D521a (correction): the computed table gives untilted versions at −1.5σ to −0.6σ vs SPA and −3.3σ to −2.3σ vs SPA+DESI (SERAPIS-1 at its D519 midpoint 0.9640: −1.5σ / −3.3σ); tilted ones at +1.7σ vs SPA and +0.3σ vs SPA+DESI. The D521 prose ranges were slightly off.

**Naming (Danny 21:51 CT):** the two data branches of SERAPIS are named **SERAPIS–Kairos** (the predictive branch, untilted: SERAPIS-1/Twist-1T; n_s 0.963–0.967, r ≈ 0.001; kairos = the
decisive, unmeasured moment, with the shape alone setting the time) and **SERAPIS–Chronos** (the tuned branch, one fitted tilt: Route A/Twist-M; n_s 0.9736, r ≈ 0.0045; chronos = measured, calibrated time).

**Naming (Danny 21:53 CT):** the overall framework is **Janus Twist theory** (Janus, the two-faced god of beginnings and passages: one shape facing both the beginning, inflation, and the end
state, Λ). Its two paths, left and right, are **Kairos** (predictive, untilted) and **Chronos** (one fitted tilt). **SERAPIS** remains the name of the fully modular model within it. Paper draft renamed
papers/twist_v7/JANUS_TWIST_PAPER.md (PDF Eldridge_JanusTwist_draft_2026-11-14.pdf; earlier PDF kept in _old/).

**D522 (Janus/Kairos κ scan; scored, PREREG_D522_D524_JANUS; results/janus_d522_d524.txt) — κ barely matters, and cannot carry Kairos to DESI.** For κ = 0.5–π, n_s is fixed to ±0.0001 (0.9629 at
N* = 52; 0.9652 at instant reheating). κ = 2π raises it by ~0.002 (0.9651 / 0.9672, r ≈ 0.0011–0.0012), still just short of the SPA+DESI 2σ edge (0.9674). For κ = 10 and 20 my end-of-inflation search window
failed (no number, not a physics statement). So Kairos stays Kairos: its n_s is essentially set by the shape and the reheating, not by κ. Result.

**D523 (gravitinos from the inflaton decay; scored) — a mild condition.** With T_RH = 5.5e10 GeV and m₃/₂ = 4.7 eV (worst case), Y₃/₂ = 1e-3 × Br gives Ω₃/₂h² = 1.3e-3 × Br. Br = 1 slightly exceeds the
~1e-3 hot-relic bound (approximate); Br = 0.01 is safe (1.3e-5). Condition: the torus shape must not decay mainly into gravitinos (Br ≲ 0.7), or m₃/₂ must sit at the low end of 1.7–4.7 eV. Result.

**D524 (axion direction during inflation; scored) — PASS, a harmless spectator.** Re τ is massless on the plateau (potential variation ∝ e^{−2π Im τ} = e^{−790}). Its random walk is 1.0e-4 per e-fold
→ ~7e-4 over 55 e-folds, ≪ the period 1. The trajectory stays on Re τ = 0 to good accuracy and the axion relaxes with the inflaton at the end (single decay channel, so no separate isocurvature component). Result.

**D525 (Janus: a SERAPIS-native Chronos path; scored, locked PREREG_D525_SERAPIS_CHRONOS + DEVIATIONS D1 [bracket]; results/serapis_chronos_d525.txt) — CHRONOS-IN-SERAPIS.**
Raising the plateau factor's power from ½ to ½ + δ gives a slow power-law tilt on the cusp. δ = 0.0023 yields n_s = 0.9736 at the instant-reheating N* = 55.7, with **r = 0.0020** and α_s = −5.9e-4. At the
gravitational-decay N* = 52 the same δ gives n_s = 0.9712, still within 1σ of SPA+DESI. The response is steep: δ = 0.01 already gives n_s = 0.990, so δ is a finely set fitted parameter (Chronos's price, like ε). Consequence: inside
SERAPIS, the two Janus paths differ in r by less than in Twist-M: Kairos r ≈ 0.0012–0.0013 vs SERAPIS-Chronos r ≈ 0.0020–0.0022 (not 0.0045). σ(r) ≈ 1e-3 separates them at ~1σ only, so n_s is now the
main discriminator. Result.

**DEEP 2.4 (Danny "Pp", 21:58 CT; latest n_s data; literature, arXiv:2510.18656 and related).** The current n_s landscape (68%): SPT-3G D1 + Planck 0.9636 ± 0.0035; CMB-SPA 0.9684 ± 0.0030;
CMB-SPA + DESI 0.9728 ± 0.0027; Planck + ACT DR6 + lensing + DESI BAO 0.9752 ± 0.0030 (0.9709 ± 0.0038 without BAO). The same paper finds standard α-attractors/Starobinsky with quadratic-minimum
reheating give n_s ≈ 0.958–0.963 (N* ≈ 50–55), i.e. ~2σ tension with the DESI-including ACT combination. That is an independent confirmation of our Kairos numbers (D519: 0.963–0.965). Kairos vs each:
SPT+Planck +0.1σ to +0.4σ (fits well); CMB-SPA −1.1σ to −1.8σ; SPA+DESI −2.8σ to −3.7σ; P-ACT-LB −3.6σ to −4.1σ. So the data-split is real and dataset-dependent, exactly the Kairos/Chronos fork.
Design lead from the same paper: a STIFFER minimum (V ∝ φ^k, k ≥ 6) makes reheating kination-like, extends N* to ~56–58 and raises n_s to ~0.965–0.968. In SERAPIS that means a higher-order zero of H at τ = i, which is exactly what made
the D516 vacuum too light (fifth force). Trade-off flagged: stiff reheating (higher n_s) vs heavy vacuum (no fifth force). A possible way through: a vacuum that is high-order near τ = i yet heavy through the c-term or the
lens. Not computed; a candidate locked test. Credit: 2510.18656, 2511.06640, 2609.19296.

## D526 — PC job J4: Janus/SERAPIS prediction map (computed on Danny's PC, locked PREREG_PCJOBS_J4)
500 points: κ ∈ {0.25…8}, δ ∈ {0…0.006}, N* ∈ {50, 52, 54, 55.6, 58}. Raw: field_tests/results/pcjobs_J4_janus_map.txt.
- κ barely matters for κ ≲ 6 (n_s shifts < 0.003). κ = 7 shifts n_s up; κ = 8 breaks (n_s > 1 or nonsense: a feature enters the plateau). Validity range: κ ≲ 6. Recorded as a result, not fixed.
- Over the reheating window N* = 52–55.6 (κ ≤ 2π):
  - Kairos (δ = 0): n_s 0.963–0.967, r 0.0011–0.0013 → fits SPT+Planck and CMB-SPA; misses SPA+DESI and P-ACT-LB. Confirms D519/D520.
  - Chronos δ = 0.002: n_s 0.970–0.974, r 0.0017–0.0021 → fits all four sets at N* = 52; three at 55.6.
  - Chronos δ = 0.0023 (D525 value): n_s 0.971–0.975, r 0.0018–0.0022 → fits CMB-SPA, SPA+DESI, P-ACT-LB. Confirms D525.
  - δ ≥ 0.004: only P-ACT-LB (and SPA+DESI at low N*); δ = 0.006 fits none.
- Sharp, falsifiable pair: Kairos says r ≈ 0.0012, Chronos r ≈ 0.002 (both far below r < 0.036; both inside reach of LiteBIRD/CMB-S4 σ(r) ~ 0.001 only marginally — honest: a 1–2σ distinction at best).
Status: COMPUTED. Kairos/Chronos fork confirmed on a full grid; Chronos window δ ≈ 0.0015–0.003.

## D527 — RIGHT + CENTRE (pp, 14 Nov 22:10 CT; literature + algebra, nothing computed) — proton protection from SERAPIS's own symmetry (candidate)
Open problem: D469 showed string-scale proton decay is excluded unless baryon number is protected (τ_p 4e26–3e29 yr vs > 2.4e34 yr); D473 needs DM stable by a gauged symmetry.
Literature:
- Kobayashi, Nishimura, Otsuka, Tanimoto, Yamamoto, arXiv:2207.14014: with couplings that are modular forms, matter fields of modular weight 1/M carry a Z_{2M}. Suitable weights realise R-parity, Z_3 baryon triality and Z_6 proton hexality. Their tables show that hexality forbids the dimension-4 and dimension-5 proton-decay operators (QQQL, ŪŪD̄Ē).
- Kobayashi et al., arXiv:1812.11072: parity of modular weight enforces a Z_2 (lepton number) perturbatively. It is broken only through Green–Schwarz e^{−aS} terms, giving λ′ ~ 1e-68–1e-14.
Link to SERAPIS (my reasoning, to be checked):
1. This Z_{2M} comes from the centre (−1) of SL(2,Z), which leaves τ fixed. So it survives at every τ, including the SERAPIS vacuum τ = i and the whole inflation path. The vacuum choice does not break it.
2. SERAPIS already uses η⁻² (weight with a multiplier system), so fractional weights like 1/3 are natural there, not an add-on.
3. Baryon triality / hexality are discrete baryon number (mod hypercharge). They forbid ΔB = 1 at every operator dimension in perturbation theory, Kähler terms included. That would cover D469's dimension-6 problem, not just dimensions 4–5. (The dimension-6 statement is the standard Ibáñez–Ross result for B3; it has not yet been checked inside this modular set-up.)
4. In string theory modular invariance is a gauge symmetry. So this is a gauged discrete symmetry, as F5/D473 requires for DM stability. One centre parity could do both jobs (CENTRE link: D469 + D473).
Not yet shown: an explicit weight assignment for the SERAPIS matter (D3 sector) that gives hexality while allowing the Yukawas, μ and Weinberg terms; the discrete anomaly (GS) condition; and the size of non-perturbative breaking at our S values. Next: a locked weight-assignment search (PREREG first).
Shared quantities: unchanged (no effect on N*, n_s, r, D, DM mass). Centre: balanced.
Status: proton protection moves from "assumed (D-brane anomalous U(1))" to "candidate mechanism inside SERAPIS's own symmetry", pending the locked search.

## D528 — modular-centre matter parity: weight search (locked PREREG_D528 + DEVIATIONS D1 [interrupted run, identical rerun]; results/parity_d528.txt) — PASS
Searched family-independent weights k = n/M for (Q, U, D, L, E, Hu, Hd). Each assignment must allow the Yukawas, μ and Weinberg terms and forbid LHu, UDD, LQD, LLE, QQQL, UUDE, QQQHd (W) and QQU†E†, QLU†D† (Kähler, dim 6).
- Rigid convention (W weight 0): no solution for Z₂; solutions for every M ≥ 2: 8 (Z₄), 24 (Z₆), 48 (Z₈), 80 (Z₁₀), 120 (Z₁₂).
- Supergravity convention (W weight −1): solutions only for even M: 16 (Z₄), 96 (Z₈). None for M = 1, 3, 5. M = 6 was still running when written; it will be appended.
Verdict: proton protection to dimension 6 is achievable with SERAPIS's own modular-centre parity. Status of D527 rises from "candidate" to "exists (perturbative)".

## D529 — discrete anomaly check (locked PREREG_D529; results/anomaly_d529.txt) — PASS for a subset
Condition: Ibáñez–Ross with Green–Schwarz, A₃ ≡ A₂ (mod N/2), three generations.
- Rigid convention: Z₄ 0/8 pass; **Z₆ 12/24 pass**; Z₈ 0/48 pass. Example: Q = 0, U = 1/3, D = 5/3, L = 4/3, E = 1/3, Hu = 5/3, Hd = 1/3, with A₃ = A₂ = 9. This is the hexality-type Z₆, the same example D528 printed.
- Supergravity (R-symmetry) convention: **Z₄^R 8/16 pass**; Z₈^R 16/96 pass. Example: Q = 0, U = D = E = 1/2, L = 0, Hu = Hd = 1/2 (weights n/2).
- Context: a Z₄^R that forbids proton decay is known in the literature (Lee, Raby, Ratz, Ross et al., arXiv:1102.3595). Their version forbids μ perturbatively; ours keeps μ by construction, so the two are related but not the same.
Not checked: hypercharge and gravity anomalies (they need the heavy spectrum); non-perturbative breaking ~e^{−S}.
Status: an anomaly-free, gauged (modular) parity protecting the proton to dimension 6 exists in both conventions. The remaining open point is to embed it in a concrete orbifold home.
D528 addendum (run completed): supergravity convention, M=6 (Z_12): 240 solutions e.g. Q=0/6, U=0/6, D=6/6, L=3/6, E=3/6, Hu=6/6, Hd=0/6.

## D530 — RIGHT (pp, 22:14 CT; literature, nothing computed) — the orbifold home has to be factorisable
Question: which string orbifolds keep the FULL SL(2,Z) on one torus, as SERAPIS needs (V built from j and η, vacuum at τ = i, walls at ρ)?
- Mayr & Stieberger, hep-th/9303017: in toroidal heterotic orbifolds the moduli-dependent threshold (the source of the η-function factors) keeps the full SL(2,Z) only when the six-torus lattice splits as T² ⊕ T⁴, with the N = 2 fixed plane's lattice even and self-dual.
- Non-factorisable lattices reduce the group:
  - Z₄ on SU(4)² gives Γ⁰(2) in T;
  - Z₆ on SU(3)×SO(8) gives Γ₀(3) / Γ⁰(3);
  - Z₈ on SU(2)×SO(10) gives Γ⁰(2) in T and Γ₀(2) in U.
- Per-plane form (standard: Dixon–Kaplunovsky–Louis; Cvetič–Font–Ibáñez–Lüst–Quevedo): K = −ln(T + T̄) per plane, so W must have weight −1 in that plane's modulus, which forces η(T)⁻² there. That is exactly SERAPIS-1's F = η⁻² H(j).
Consequences:
1. SERAPIS's home must be a factorisable orbifold, with the SERAPIS torus as the N = 2 fixed plane T²; the other two tori form the T⁴ and are heavy, as assumed. Its modulus can be that plane's T (Kähler) or U (shape); both have full SL(2,Z) there.
2. Non-factorisable homes would turn SERAPIS into a congruence-subgroup model. That means more cusps and fixed points and a different vacuum structure, so not the tested model. Excluded as SERAPIS homes; they could be a later variant.
3. Tension flagged: this lineage is heterotic, while the Twist-2 FI capture and the D3 sector are type IIB. The IIB analogue is the shape modulus U of a T² factor in T²×K3 / T⁶/Z_N orientifolds (SL(2,Z)_U). Whether IIB fluxes and the FI term keep the full group is not settled.
Shared quantities: unchanged. Centre: balanced.
Status: home narrowed. Factorisable T² ⊕ T⁴ with the SERAPIS torus as the N = 2 plane is required; heterotic vs IIB is still open.

## D531 — CENTRE (3-min loop tick 1; scored, locked PREREG_D531_LAMBDA_AXION; results/lambda_axion_d531.txt) — FAIL (narrowly)
Question: could Λ's instanton (SERAPIS-1: V(i) ∝ |c|², so the V-level suppression is e^{−243.2}) and the D471 ultralight axion's instanton (V-level action 242–267) be one family? The model tested: the axion potential is the interference term of Λ's W-instanton (S_W = 121.6) and a second one with action S′.
Computed: Λ = 2.56e-47 GeV⁴ and V_a/Λ = 4e-12 to 5e-4, giving S′ = 129–148.
- Heavy-axion end (m = 1e4 H0): implied axion action 251–252, inside 242–267.
- Light end (m = 2 H0): 268–269, outside by 1–2 units.
Locked verdict: FAIL. Comment, not a rescue: the D471 band itself used an order-one prefactor convention. A 1–2 unit shift in an action is within prefactor uncertainty, so this does not show the picture is wrong either.
Learned (robust):
- Λ's V-level suppression, 243.2, lands inside the axion-instanton band. Both point to cycles of 2π-volume ≈ 19–24 (W-level).
- The interference picture predicts the axion is the heavier kind (m ≳ 10² H0) if the same cycles do both jobs.
Status: Λ-instanton origin stays OPEN. There is one consistent sub-window (heavy axion), not adopted. Shared quantities unchanged.

## D532 — RIGHT (pp, 22:18 CT; literature, nothing computed) — in type IIB, the SERAPIS torus must carry no flux
Follow-up to D530's heterotic-vs-IIB tension.
- Ishiguro, Kobayashi, Otsuka, arXiv:2011.09154. Setup: IIB on T⁶/(Z₂×Z₂′) with three-form fluxes and isotropic τ. SL(2,Z) is a symmetry only together with a transformation of the flux quanta; any fixed flux choice breaks it. Flux vacua cluster at τ = ω, about 40–62% depending on the flux bound. τ = i holds only about 4–6%.
Consequences for SERAPIS:
1. If τ were a flux-stabilised complex-structure modulus, three things would break. V(τ) would not be exactly modular at fixed flux. τ would be pinned near its flux minimum, so there would be no roll from Im τ ≈ 126. And the vacuum would favour ω, which SERAPIS makes a wall. So the IIB SERAPIS torus cannot be flux-stabilised.
2. A consistent IIB option: a T² with no flux through it (for example T² × K3 with flux on the K3 part only). There its U stays a modulus with the full SL(2,Z), and its potential comes from non-perturbative, modular-covariant terms, as in the heterotic case.
3. This is a real constraint, not a fit. Together with D530: the SERAPIS torus is an N = 2 plane with no flux, and the full SL(2,Z) comes from the factorised T² lattice.
4. Mild statistical note: landscapes that stabilise by flux prefer ω over i. SERAPIS's vacuum at i is therefore NOT a typical flux vacuum. That is fine, because τ is not flux-stabilised in our set-up, but it should be stated in the paper.
Shared quantities unchanged; centre balanced. Status: the home is narrowed further. The IIB route needs an unfluxed T²; heterotic stays the most natural.

## D533 — RIGHT (loop tick 2; scored, locked PREREG_D533_PARITY_NP; results/parity_np_d533.txt) — PASS
Question: does non-perturbative (Green–Schwarz) breaking of the D528/D529 modular parity bring proton decay back?
Model: λ_np ≈ e^{−2π α_U⁻¹/δ_GS} (from 1812.11072), taken in the worst case of our numbers: α⁻¹ = 26 at M_s = 3.5e14 GeV, squarks 10 TeV.
Bounds:
- dim-4 (λ′λ″): needs λ_np < 3e-12, so δ_GS ≤ 6.2.
- dim-5 (QQQL/M_eff ≳ 1e24 GeV): needs λ_np < 3.5e-10, so δ_GS ≤ 7.5.
Combined: δ_GS ≤ 6.2; natural values δ_GS = 1–3 give λ_np = 1e-71 to 2e-24. PASS.
Caveats: the bounds are standard order-of-magnitude ones, and δ_GS depends on the home. A concrete orbifold has to give δ_GS ≲ 6.
Status: proton protection is now perturbative (D528), anomaly-free (D529) and safe against instantons for δ_GS ≲ 6 (D533). It stays model-level until the orbifold home exists.

## D534 — LEFT + CENTRE (pp 22:22 CT; scored, locked PREREG_D534_STIFF_ROOM; results/stiff_room_d534.txt) — FAIL: no room for stiff reheating
Question (DEEP 2.4): can SERAPIS get a stiff, kination-like reheating phase, which would raise N* to 56–58 and n_s toward the DESI-including data, while keeping a heavy vacuum?
Computed: V*^{1/4} = 6.0e15 GeV and V_end^{1/4} = 3.4e15 GeV. Reheating gravitationally to T_RH = 5.5e10 GeV needs m ≥ (T_RH² M_P)^{1/3} = 2.0e13 GeV. Even at that minimum, the quadratic term ½m²φ² at 1 M_P already exceeds V_end, by 8.6×; at SERAPIS-1's own mass, 4e13 GeV, by 36×. So the oscillations after inflation never leave the quadratic region, and there is no stiff phase.
Verdict: FAIL. The stiff-vs-heavy trade-off is sharp for a self-reheating SERAPIS. Kairos keeps N* = 52–55.6 and n_s = 0.963–0.967 (D518–D520, D526).
The only escapes (not adopted):
- a lighter vacuum that reheats through a stronger, non-gravitational coupling (needs a new coupling, and a light modulus brings back fifth-force and moduli issues);
- an order-one φ_end ≪ M_P geometry (not the SERAPIS-1 shape).
Consequence: the SERAPIS–Kairos/Chronos fork cannot be closed by reheating. It rests on the CMB-vs-BAO question (D223, McDonough & Ferreira 2512.05108).

## D535 — LEFT (pp 22:23 CT; literature + exponent arithmetic, no lock needed) — SERAPIS-1's H(j) lies OUTSIDE the string-derived class (honest flag)
Literature:
- Knapp-Pérez, Liu, Nilles, Ramos-Sánchez, Ratz, arXiv:2304.14437. Gaugino condensation gives W = Ω(S)H(τ)/η⁶ with H = (j−1728)^{m/2} j^{n/3} P(j). In the Cvetič–Font–Ibáñez–Lüst–Quevedo class m, n are integers and P is a polynomial, required for no singularities in the fundamental domain. Matter (ISS-type) uplift gives dS vacua at or near τ = i. That supports our vacuum location.
- Baur, Nilles, Ramos-Sánchez, Trautner, Vaudrevange, arXiv:2207.10677: a realistic heterotic T⁶/(Z₃×Z₃) model whose T modulus sits near 3.2i (not at i), with a finite T′ = Γ′₃ flavour group.
Check of SERAPIS-1 (H = (j−1728)^{1/2} j^{−7/12}[ln(j/1728)+κ]^{1/2} + c j^{−7/12}) against that class:
- m = 1: (j−1728)^{1/2} is allowed.
- j^{−7/12} would need n = −7/4, which is NOT an integer, so it is outside the class. The exponent is forced: a flat cusp plateau with η⁻² needs |j|^{2a}·e^{πy/3} constant, so a = −1/12, so n/3 = −7/12. With η⁻⁶ (three equal moduli) the same logic needs n/3 = −3/4, also non-integer. Conclusion: no integer-n CFILQ potential has an exactly flat cusp plateau. They run away or grow at the cusp, the known decompactification problem.
- [ln(j/1728)+κ]^{1/2} is not a polynomial P(j). It is a branch-type factor that is singular where ln(j/1728) = −κ.
Verdict: SERAPIS-1's inflationary plateau uses an H outside the string-derived CFILQ class. It is a modular-invariant phenomenological H, not yet a string-derived one. The vacuum and Λ structure (τ = i, (j−1728)^{1/2}) is in the class; the plateau factors are not.
Required paper change: say this explicitly (do not imply a string derivation of the plateau).
Open task: either (a) find a string source for fractional j-powers (multiplier systems or several moduli, e.g. η-quotients of congruence subgroups, though D530 excludes those homes for exact SL(2,Z)), or (b) take the plateau from the Kähler side (corrections in ln(2 Im τ), as in some modular-inflation papers), or (c) accept it as an effective model.
Status: a new honest gap, "string origin of the plateau", rated HIGH. Predictions unchanged.

## D536 — LEFT (pp 22:25 CT; literature, nothing computed) — what string-class modular inflation looks like, and how SERAPIS differs
Follow-up to D535: how do papers that stay inside the CFILQ class (integer m, n; polynomial P(j)) get inflation?
- Ding, Jiang, Zhao, arXiv:2405.06497: W = Ω(S)H(τ)/η⁶, K = −3 ln(2 Im τ), H in the class with P(j) quadratic in (1 − j/1728).
  - Inflation runs along the unit arc from τ = i toward ω; ω is the Minkowski minimum.
  - n_s ≈ 0.965 needs the P(j) coefficients; P = 1 gives 0.942–0.955.
  - r ≲ 1e-6, running ~ −1e-4.
- King & Wang, arXiv:2405.08924: H = 1 + α(j/1728 − 1)². Hilltop inflation near τ = i, ending toward the dS vacuum at ω; p = 4 hilltop is in tension with the data, p = 6 is better. Also tiny r.
Comparison (honest):
- String-class modular inflation is a hilltop near i or the arc, with the vacuum at ω and r ≲ 1e-6.
- SERAPIS-1 is the reverse: a cusp plateau, the vacuum at i, ω a wall, and r ≈ 1e-3 (Kairos 0.0011–0.0013; Chronos ≈ 0.002). Its plateau factors are outside the class (D535).
- That gives a clean observational split. LiteBIRD/CMB-S4 (σ(r) ~ 1e-3) can separate r ~ 1e-3 from r ≲ 1e-6.
  - A detection of r ≈ 0.001–0.002 would favour the SERAPIS-type plateau over the in-class string models.
  - A firm upper limit r < 5e-4 would exclude SERAPIS (both paths).
- This is a sharper statement than "r is small" and is worth putting in the paper's predictions.
Credits already listed for both papers (ZENODO_UPDATE); this note adds the comparison.
Status: SERAPIS is positioned as the large-r, cusp-plateau alternative to in-class modular hilltops. A decisive near-term test is r ≥ 5e-4 vs < 5e-4.

## D537 — CORRECTION (independent referee, 22:30 CT; verified by its script, ~10 s) — Λ at τ = i is WITHDRAWN; the vacuum is supersymmetric Minkowski
Finding: serapis1_d517.py builds (j−1728)^{1/2} with the principal square root.
- That root flips sign across the line through τ = i (sqrt(j−1728)/(τ−i) jumps from −157.57i to +157.57i), so F = η⁻²H is NOT holomorphic at the vacuum.
- The holomorphic choice is E₆/η¹² ≈ −157.57i (τ−i). With it, H ≈ j^{−7/12}[157.6·(…)(τ−i) + c] has a zero at |τ − i| ~ 1e-55. That is a supersymmetric Minkowski point with V = 0, not Λ.
- E₆/η¹² is odd under S, while c·j^{−7/12} is even. So the c-term breaks SL(2,Z) unless c = 0.
- This agrees with the no-go of Leedom–Righi–Westphal (arXiv:2212.03876): no dS at τ = i from H ∝ (j−1728)^{1/2}.
Withdrawn:
- D517 (2) "V(i) on the Λ target" and (4) "c = e^{−121.6}, instanton-sized".
- Everything built on them: D531's input S_Λ = 243.2 (the D531 verdict is void, not just FAIL), the synthesis line "Λ is the leftover energy at the square torus", and the paper's Λ claims.
Survives: the plateau inflation numbers (n_s, r, N*; D518–D520, D525, D526) and a heavy, supersymmetric Minkowski minimum at τ = i (m ~ 4e13 GeV, to be recomputed at the model's own N*). Λ returns to an added constant (the standard tuning).
Other referee points accepted:
- Kairos is the α = 1/3 attractor (K = −ln 2Im τ), not a modular-specific prediction.
- The D515 table row used N* = 58.09 (wrong history).
- "Every computation pre-registered" should read "every scored test". The D525 DEVIATIONS file was committed together with its rerun result.
- For D528/D529 only the supergravity convention applies (W weight −1); the rigid solutions are irrelevant. A non-zero ⟨W⟩ (gravitino mass) breaks the Z₄^R/Z₈^R.
Zenodo: the referee verdict is NOT READY until these are fixed. Post as a SEPARATE record, a status/synthesis preprint.
Process note: my own checks missed the branch issue, because the 200-digit runs looked only along the imaginary axis (Re τ = 0), where the sign flip is invisible. Lesson: holomorphy checks must go off-axis.

## D538 — RIGHT (pp 22:26 CT; analytic reasoning, not a scored test) — can a corrected SERAPIS put Λ back at τ = i? No: you get a saddle or Minkowski
After D537, three options with a nilpotent S (V = e^K|F|², F = η⁻²H holomorphic of weight −1, H invariant):
(a) H odd at i, e.g. ∝ E₆/η¹² ∝ (τ − i). Then F(i) = 0 and the vacuum is SUSY Minkowski (V = 0), the D537 result. Any constant added to H has the opposite S-character and breaks invariance.
(b) H even and non-zero at i: H ≈ c + A(τ − i)² + …. Then V ∝ |c|² + 2 Re[c̄A(τ − i)²] + …. The term Re[c̄A δ²] changes sign with the direction of δ (Re δ² = δ_x² − δ_y²). So τ = i is a SADDLE at order |c|. The positive curvature from e^K and |η|⁻⁴ is itself ∝ |c|², far smaller, so it cannot lift the saddle unless |A| ≲ |c|. That would make the "stiff" mass ~ c·(scale), i.e. tiny: a light field and the fifth-force problem again (D493).
(c) H even and vanishing at i: back to (a)-type Minkowski.
Conclusion: within this minimal set-up (one modulus, nilpotent S, exact SL(2,Z)), "heavy vacuum at τ = i" and "Λ ≠ 0 at τ = i" cannot both hold. This is the Leedom–Righi–Westphal no-go (arXiv:2212.03876) in our language.
Known ways out (literature): matter/ISS uplift with a limited coupling range gives near-zero or slightly dS vacua near i (Knapp-Pérez et al., arXiv:2304.14437, D535), or a separate uplift sector. In both, Λ is an added and tuned sector, not a property of the torus.
Status: SERAPIS now = plateau inflation + heavy SUSY-Minkowski vacuum at i + separately tuned Λ (as in 2405.06497). The "one torus explains Λ" claim is closed as NOT supported. The synthesis and paper must change accordingly (in progress).

## D539 — LEFT (loop tick 3; scored, locked PREREG_D539_VACUUM_MASS; results/vacuum_mass_d539.txt) — vacuum mass at the model's own N* (referee fix 4)
m = 4.5e13 (N* = 52), 4.3e13 (54), 4.2e13 (55.6) GeV; m/H_inf = 4.9 throughout. The D517 value of 4.0e13 was at the wrong N* (58.09) and is replaced by 4.2–4.5e13 GeV. The holomorphic correction (D537, E₆/η¹², c = 0) does not change this curvature. The vacuum is a heavy SUSY Minkowski point (D537/D538). Gravitational reheating (D518) is unchanged at this level (T_RH ∝ m^{3/2}: +6–10%).

## D540 — LEFT (pp 22:28 CT; literature + arithmetic, not scored) — a string-side source for the log factor, and species-scale control
Literature: Casas & Ibáñez, arXiv:2407.12081.
- For one elliptic modulus with SL(2,Z), V ≃ (Im τ)²|Ĝ₂|²/N², with N ≃ −log(Im τ|η|⁴). That is the genus-one/threshold function, i.e. the number of species.
- The potential tends to a constant at large Im τ (a Starobinsky-like plateau), and N_e ≃ N.
Link to SERAPIS (D535 gap):
- Our non-polynomial factor [ln(j/1728) + κ] grows like 2π Im τ at the cusp.
- The string-derived, modular-invariant −log(2 Im τ|η|⁴) grows like (π/3) Im τ − ln(2 Im τ). Same linear growth, string origin, but NON-holomorphic.
- So the log factor has a natural string counterpart, but it belongs in V through the Kähler/threshold sector (one-loop gauge kinetic function f = S + b ln η-type terms, or species-scale corrections), not in a holomorphic W. This is option (b) of D535.
- Proposed SERAPIS-2: replace [ln(j/1728)+κ]^{1/2} in H by the factor from the threshold, (−log(2 Im τ|η|⁴) + κ′)^{1/2}, entering V directly. Not computed; it needs its own lock. The j^{−7/12} factor still has no string source.
Species-scale check (arithmetic):
- At the start of inflation in SERAPIS-1, Im τ* ≈ 126, so N ≈ (π/3)(126) − ln(252) ≈ 126.4.
- Λ_sp ≈ M_P/√N ≈ 2.2e17 GeV, compared with H_inf ≈ 9e12 GeV, so the EFT is under control by ~4 orders.
- In the Casas–Ibáñez relation N_e ≃ N, about 126 species is of the same order as the 52–56 e-folds needed. That is consistent, not a tension.
Status: the log factor now has a plausible string-side origin (threshold/species function); j^{−7/12} does not. Next: lock and test SERAPIS-2.

## D541 — LEFT (loop tick 4; scored, locked PREREG_D541_SERAPIS2; results/serapis2_d541.txt) — SERAPIS-2 (threshold-log plateau): NOT VIABLE
I replaced SERAPIS's non-polynomial factor [ln(j/1728)+κ] by the string-derived threshold function −ln(2y|η|⁴) + κ′ (D540), using the same method as J4.
- Primary κ′ = 0: n_s = 0.9606 (N* = 52; −2.6σ SPA) and 0.9631 (55.6; −1.8σ); r = 0.0019–0.0022. It fails the 2σ condition at N* = 52, so it is NOT VIABLE by the lock.
- Sensitivity is severe: κ′ = 1 gives n_s 0.92–0.93 (r ≈ 0.01), and κ′ = 2π gives n_s ≈ 1.045. The slower (πy/3) growth of the threshold function makes the plateau's approach depend strongly on the constant. So the string-side version is not predictive without fixing κ′ from first principles.
Lesson: the threshold function can make a plateau, but not a stable, predictive one at this level. D535's gap (string origin of the plateau) stays open; SERAPIS-1 remains an effective model.

## D542 — RIGHT (pp 22:34 CT; reasoning + arithmetic, not scored) — the Z₄^R/Z₈^R parity with a non-zero gravitino mass: still safe
Referee caveat (D537/v2.1 §4): a non-zero ⟨W⟩ breaks the R-symmetry. What is left?
- ⟨W⟩ has R-charge 2 (mod N). A non-zero ⟨W⟩ = m₃/₂ M_P² breaks Z₄^R → Z₂ (matter/R-parity) and Z₈^R → Z₄. Operators forbidden only by the broken part can reappear, but only with explicit powers of ⟨W⟩/M_P³ = m₃/₂/M_P². This is the standard Z₄^R argument (Lee, Raby, Ratz, Ross et al., arXiv:1102.3595); there μ ~ m₃/₂ appears the same way.
- dim-4 (UDD, LQD, LLE, LHu): still forbidden by the residual Z₂ matter parity.
- dim-5 (QQQL, UUDE): reappear with M_eff ~ M_P²/m₃/₂. For gauge-mediated m₃/₂ = 1.7–4.7 eV (D474) this gives M_eff ≈ 1.3–3.5e45 GeV; even m₃/₂ = 100 TeV gives 5.9e31 GeV. The bound M_eff ≳ 1e24 GeV is met by more than 7 orders of magnitude.
- dim-6 Kähler (QQU†E†, QLU†D†): an R-charge mismatch of 2 can be filled by one ⟨W⟩ insertion, giving an extra suppression ~ m₃/₂/M_P, which is negligible. A mismatch of 1 or 3 (mod 4) cannot be filled at all, so the operator stays forbidden.
Verdict: proton protection survives SUSY breaking and the Λ uplift as long as m₃/₂ ≲ 1e5 GeV, which covers every Twist realisation. The referee's caveat is resolved at the order-of-magnitude level. Not yet written into the published v2.1; it goes into a future version.

## D543 — LEFT (pp 22:36 CT; reasoning, not scored) — j^(−7/12) is multi-valued around ρ: the "wall" is a branch point of W (a D537-type check, done off-axis)
Lesson from D537 applied to the other fractional factor. Near ρ, j ∝ (τ − ρ)³, so j^(−7/12) ∝ (τ − ρ)^(−7/4). Equivalently j^(−7/12) = (E₄/η⁸)^(−7/4), and E₄ has a simple zero at ρ.
So F = η⁻²H is not single-valued around ρ: going once around ρ multiplies it by e^(−7πi/2) = i. The factor ln(j/1728)+κ adds more branch points, where j = 0 (at ρ) and where ln(j/1728) = −κ.
What this means:
- V = e^K|F|² contains |j|^(−7/6), which IS single-valued. The plateau and vacuum numbers along the imaginary axis are unaffected, since the path never circles ρ.
- But W must be holomorphic and single-valued on field space for a consistent supergravity. SERAPIS-1 is only well-defined on the upper half plane with branch cuts from ρ and its images. The "wall at ρ" is really a singularity of W, not a smooth repulsive feature.
- Compare the CFILQ class, where n is an integer so j^(n/3) = (E₄/η⁸)^n is single-valued: D535's "outside the class" is not only about stringy origin but also about global consistency.
Verdict: SERAPIS-1 is a LOCAL effective model, valid in a region that avoids the branch cuts (the cusp-to-i path is inside it), not a global modular supergravity. The predictions along the path are unchanged.
Paper wording to fix in the next version: "j^(−7/12) makes τ = ρ a wall" should read "a branch point of W; the model is defined away from cuts from ρ". It does not affect the published numbers. Self-check run off-axis as D537's lesson requires; no other fractional factor is left unchecked.

## D544 — LEFT (pp 22:37 CT; literature, important) — MAJOR PRIOR ART MISSED: Kallosh & Linde, "SL(2,Z) Cosmological Attractors" (arXiv:2408.05203), plus arXiv:2412.19324
What they do:
- One complex field τ, kinetic term (3α/4)|∂τ|²/(Im τ)², and an exactly SL(2,Z)-invariant potential built from L_j = (1/4π) ln(|j|² + 1728²), L_η ∝ −ln(Im τ|η|⁴) or the Casas–Ibáñez Ĝ₂ form, for example V₀((I−1)/(I+1))ⁿ.
- Inflation runs on the CUSP plateau, with the axion double-exponentially flat (stable; 2412.19324).
- Predictions are α-attractor: n_s = 1 − 2/N, r = 12α/N². For a T² (CY) compactification, 3α = 1, i.e. our K = −ln(2 Im τ).
- Vacuum: τ = ω is the minimum (V = 0) and τ = i is a dS saddle. Λ is added as a constant.
- Supergravity: a nilpotent X with a chosen metric G_XX̄ encodes V. There is no holomorphic W(τ), so they avoid the branch and single-valuedness issues (cf. our D537, D543).
Relation to SERAPIS:
- SERAPIS-1 is in substance an SL(2,Z) cosmological attractor with α = 1/3. The cusp plateau, the α-attractor numbers (our "Kairos = α = 1/3 attractor", D537 referee point 2) and "Λ added" are all already in Kallosh–Linde (Aug 2024).
- What differs:
  - our vacuum at τ = i, with ω as a singular point, versus their minimum at ω with i a saddle;
  - our choice of a holomorphic W (which caused D537/D543);
  - the Chronos tilt branch;
  - the proton-parity and string-home constraints.
- Their G_XX̄ route is the clean way to make SERAPIS globally consistent. Put V in the X metric, not in W. That fixes D543 and keeps τ = i as the minimum by the choice of invariant (for example a function of |j − 1728|).
Consequences:
1. The published Zenodo v2.1 (10.5281/zenodo.24238833) does NOT credit 2408.05203 or 2412.19324, and the referee did not find them either. That is a credit omission in a published record. Fix: a v2.2 with the citations and a sentence placing SERAPIS as a variant of SL(2,Z) attractors. It needs Danny's explicit "Publish" for the new version.
2. The novelty claim narrows further: what remains is the two-branch data framing, the τ = i-vacuum variant, the parity/home constraints and the audit trail.
Status: flag raised to Danny; v2.2 to be prepared.

## D545 — LEFT + CENTRE (loop tick 5; scored, locked PREREG_D545_SERAPIS_KL; results/serapis_kl_d545.txt) — SERAPIS-KL: CONSISTENT (a globally well-defined SERAPIS)
Model: K = −ln(2 Im τ) (α = 1/3). The potential sits in the nilpotent-field metric, in the Kallosh–Linde way:
I = (1/4π) ln(1 + |j − 1728|²/1728²), V = V₀[I/(I+1)]ⁿ.
Checks:
(a) V(i) = 0, and τ = i is a minimum in every direction tested (n = 1: V ≈ 1.6e-7 at |δ| = 0.01, nearly isotropic).
(b) V depends only on |j − 1728|, so it is single-valued. There are no branch points: D537 and D543 are both cured.
(c) V(ω) = 0.052 V₀ > 0, so ω is not a singularity, just a higher point.
Inflation (primary n = 1):
- N* = 52: n_s = 0.9631, r = 0.00131 (−1.8σ SPA, −3.6σ SPA+DESI).
- N* = 55.6: n_s = 0.9654, r = 0.00116 (−1.0σ, −2.7σ).
- n = 2 gives 0.9625–0.9649. Both are close to the α = 1/3 attractor formula (0.9615–0.9640, r = 4/N²).
Verdict: CONSISTENT. This is SERAPIS–Kairos rebuilt as a well-defined SL(2,Z) attractor with its minimum at τ = i (KL put theirs at ω). The numbers are essentially those of D519/D526, confirming that Kairos's predictions do not depend on the problematic holomorphic factors.
- Λ: added as F_X² − 3W₀² (KL form).
- Chronos: the same tilt route (plateau power ½ + δ, i.e. I-power) would carry over; not computed here.
- Credit: Kallosh & Linde 2408.05203. What this note adds is the τ = i-minimum invariant built on |j − 1728|.
Status: SERAPIS is now well-defined globally in this form. Use SERAPIS-KL as the reference model in v2.2+.

## D546 — LEFT (pp 22:39 CT; scored, locked PREREG_D546_SERAPIS_KL_CHRONOS; results/serapis_kl_chronos_d546.txt) — CHRONOS CARRIES OVER to SERAPIS-KL
V = V₀[I/(I+1)]·I^{2δ}, with the D525 value δ = 0.0023 (not refitted).
- n_s = 0.9715 (N* = 52) and 0.9738 (55.6), i.e. −0.5σ and +0.4σ vs SPA+DESI. r = 0.0020–0.0022.
- τ = i stays the V = 0 minimum (neighbours at 1.5e-7 V₀).
- Grid: δ = 0.0015–0.003 spans n_s 0.969–0.976; δ ≈ 0.002 at N* = 55.6 lands exactly on 0.9728.
These match D525/D526 (0.971–0.974, r ≈ 0.002), so both branches carry over unchanged to the globally consistent form.
Status: SERAPIS-KL now has both branches.
- Kairos (D545): n_s 0.963–0.965, r 0.0012–0.0013, no tilt.
- Chronos (D546): n_s 0.971–0.974, r 0.0020–0.0022, one tilt.
The published numbers stand, and the model behind them is now well-defined. Should go into v2.2+ (prepared v2.2 does not yet mention D545/D546).

## D547 — RIGHT (PC job J1 = D500 Twist-M case (i), scored by PREREG_D500 + DEVIATIONS D1–D7; results/pcjobs_J1_D500.txt) — NOT CAPTURED (both points)
- m_s = 1e-9 GeV: 20,093 crossings of x = 1 (the 20,000 cap was hit), first at N = 3.0. At the stop (N = 33.8): |ln x| = 7e-7 but |dφ/dN| = 2.2, so the field is still moving fast through the self-dual point and is not settled. Ω_x = 1.0 ≫ 0.05, so BBN fails. The remnant is 3.6e3 × DM. Verdict: NOT CAPTURED.
- m_s = 1e4 GeV: a math-domain error (runaway), counted as no capture by D7.
Status: the two-sided FI trap at the self-dual point does not capture the Twist-M field, so Twist-M case (i) FAILS. This does not affect SERAPIS, whose minimum is a heavy symmetric point with no capture needed (D517/D539/D545). J2 (Twist-M grid) is running; its first 6 points all FAIL with numerical runaways, consistent with this.

## D548 — RIGHT + CENTRE (pp 22:41 CT; arithmetic, not scored) — the Λ sector in SERAPIS-KL can be the gauge-mediation SUSY-breaking sector
In the Kallosh–Linde form, the vacuum energy is Λ = F_X² − 3|W₀|²/M_P², i.e. the F-term of the nilpotent X minus the gravitino term. Λ ≈ 0 then requires F_X ≈ √3 m₃/₂ M_P.
- With √F_X = 85–140 TeV (the D474 gauge-mediation window), m₃/₂ = F/(√3 M_P) = 1.7–4.6 eV: exactly the D474 gravitino window.
- So the same X that carries the inflaton potential (through its metric) can be the SUSY-breaking sector seen by gauge mediation, and the Λ cancellation is the usual F_X² ≈ 3m₃/₂²M_P² tuning.
- The inflation scale enters only through the τ-dependent metric amplitude: V_inf/F_X² ≈ 3.4e41 at √F = 140 TeV. That is a large but harmless ratio set by the metric function, not a new tuning.
- Λ itself remains tuned at the 1e-120 level, as in every such model. What this note shows is internal consistency, not an explanation. It also fixes the proton-parity status: m₃/₂ ~ eV, so the D542 margin is about 1e21.
Status: the Λ sector is consistently embedded (tuned). Nothing in SERAPIS-KL conflicts with the gauge-mediation and gravitino results of the Twist line (D474, D523).
D548a (correction): the computed ratio is V_inf/F_X² ≈ 3.4e42, not 3.4e41 as typed above. No conclusion changes.

## D549 — LEFT (pp 22:42 CT; literature) — Chronos is also prior art: Kallosh & Linde, "Singular α-attractors" (arXiv:2512.02969), and arXiv:2607.07684
- 2512.02969 (Dec 2025): "S-models". A small singular term with coefficient δ lifts the α-attractor plateau polynomially or exponentially at large field, which raises n_s toward the ACT/SPT/DESI values. Their §5.3 builds an SL(2,Z)-invariant version from j(τ). Example: a T-model with δ = 1e-2 gives n_s ≈ 0.978, r ≈ 0.0035 (N = 55, α = 1/3).
- 2607.07684 (Jul 2026): attractors interpolating between exponential and polynomial, scanning n_s to fit any CMB+DESI combination.
Relation: our Chronos tilt (V ∝ [I/(I+1)]·I^{2δ}, a slowly rising plateau; D525/D546) is the same idea as their singular/lifted plateau, published before our D525 (14 Nov 2026). Kairos = SL(2,Z) attractor (2408.05203) and Chronos = singular SL(2,Z) attractor (2512.02969). Both branches of the Janus framing therefore correspond to existing Kallosh–Linde constructions.
What remains ours: the τ = i-vacuum invariant (|j − 1728|), the two-branch data framing tied to the CMB-vs-BAO split, the proton-parity and string-home constraints, the Twist-line consistency (D548), and the audit trail.
Action: add both citations to v2.2 and state that Chronos is a singular-attractor (S-model) lift. Novelty statement narrows again.

## D550 — LEFT (pp 22:44 CT; literature, novelty check) — is the τ = i-minimum invariant ours?
I checked the nearest work:
- Kallosh & Linde, "Landscape of Modular Cosmology" (arXiv:2411.07552): V = V₀(1 − ln|j(i)|²/(ln|j|² + j(i)²)), plateau at the cusp, α = 2/3. τ = n + i are SADDLES; the V = 0 minima are at the ω-type points.
- 2408.05203: minimum at ω, i a dS saddle.
- Ding et al. 2411.18603 (modular inflation and reheating, A₄ lepton sector): r ~ 1e-7, a hilltop-type model, not a cusp plateau.
- 2512.02969: an SL(2,Z) S-model built from j, with no vacuum at i.
In this (limited, 2-search) check I found no prior cusp-plateau SL(2,Z) attractor whose V = 0 minimum is at τ = i. Our invariant I = (1/4π) ln(1 + |j − 1728|²/1728²) (D545) does that, using the zero of j − 1728 (E₆) at i.
Label: a "variant not found in the checked literature", NOT a claim of priority. It is a small construction, and a referee may know of others.
Physical difference from KL: at τ = i the residual symmetry is Z₂ (S), versus Z₃ (ST) at ω. That affects the modular-centre/flavour selection rules for matter at the vacuum (relevant to D528–D533) and the vacuum's mass spectrum. Worth a sentence in v2.2.
Credit added: 2411.07552.

## D551 — RIGHT + CENTRE (loop tick 6; scored, locked PREREG_D551_VACUUM_I_SELECTION; results/vacuum_i_selection_d551.txt) — PASS: the τ = i vacuum's selection rule is compatible with the proton parity
At τ = i, level-1 modular forms of weight k ≢ 0 (mod 4) vanish (for example E₆(i) = 0). So each required coupling needs a coefficient weight k_Y = Σk_i − 1 ≡ 0 (mod 4).
- Z₄^R: 4 of the 8 anomaly-passing assignments admit weights giving all five required couplings (QHuU, QHdD, LHdE, HuHd, LHuLHu) with k_Y ≡ 0 (mod 4), i.e. non-zero at the vacuum. Example: Q = 0, U = D = E = Hu = Hd = 1/2, L = 0, all k_Y = 0 (constant couplings).
- Z₈^R: 8 of 16 do.
Physical note: the τ = i vacuum (residual Z₂ from S, a Z₄ acting on matter) adds a real constraint. Half of the anomaly-free parities survive it. This is specific to SERAPIS's i-vacuum; at ω the rule would be mod 6. Counts as the vacuum-dependent check suggested in D550.
Status: the proton parity, its anomaly check, the m₃/₂ breaking (D542) and the vacuum selection rule are all consistent for 4 Z₄^R and 8 Z₈^R assignments.

## D552 — LEFT/RIGHT (pp 22:46 CT; literature) — the string origin of the Kallosh–Linde metric form is not automatic
- Kallosh, Linde, Roest, Yamada, "D̄3-induced geometric inflation" (arXiv:1705.09247): any V(T, T̄) can be encoded in the nilpotent metric, G_SS̄ = |m₃/₂|²/(V + 3|m₃/₂|²). As a supergravity statement this is the method D545 used. Their examples are α = 1/3 attractors for one disk/half-plane modulus.
- Garcia del Moral, Parameswaran, Quiroz, Zavala (arXiv:1707.07059): for an actual anti-D3 on an O3 in a GKP background, the X-metric is NOT arbitrary. It is fixed by the brane action: power-law factors (T + T̄), (τ_dil + τ̄_dil)⁻¹ and the complex-structure-dependent warp factor e^{−4A₀(Z)}.
Consequence for SERAPIS-KL:
- the j-dependent X-metric we need (V ∝ I/(I+1), I from |j − 1728|) is not what a single anti-D3 naively gives;
- the IIB axio-dilaton has exact SL(2,Z), but GKP fluxes stabilise it, so it cannot be the rolling τ (same logic as D532);
- a string origin would need modular-invariant warping/threshold dependence on an UNFLUXED T² modulus, for example through one-loop (η-function) corrections to the brane action. That is not established.
Status: SERAPIS-KL is consistent as supergravity but its V is put in by hand, exactly as in Kallosh–Linde's own models. The string-origin gap (D535) is restated, not closed. No change to predictions.

## D553 — LEFT + RIGHT (pp 22:48 CT; scored, locked PREREG_D553_SWAMP_PERT; results/swamp_pert_d553.txt) — perturbativity caps the N = 2 beta coefficient: |b^{N=2}| ≲ 2
Ishiguro, Kai, Kobayashi, Otsuka (arXiv:2508.12392): one-loop thresholds grow ∝ Im U on the N = 2 plane, and gauge couplings stay perturbative only for U₂ < −(3/π)W₋₁(…exp(−16π² Im S/b)). With b = 10 and Im S = 2 they get Im U ≲ 34.3, and they argue large Im τ is "in the Swampland".
Computed (reproduces their 34.3 as 34.5 at b = 10):
- U₂,max = 308 (b = 1), 157 (b = 2), 106 (b = 3), 65 (b = 5), 35 (b = 10).
- SERAPIS needs Im τ at horizon exit = 112–158 (D545/D546), so |b^{N=2}| ≲ 2.0 for every gauge group whose coupling feels the SERAPIS plane.
Consequences:
- This sharpens D530/D532 into a number. The SERAPIS T² must be (almost) invisible to the gauge sectors: b^{N=2} = 0 for the SM (consistent with "SM on branes not wrapping it"), and ≤ 2 for any hidden group.
- The holomorphic SERAPIS-1 route needs a hidden gaugino condensate with a non-zero threshold on that plane (the η⁻² factor). It therefore lives at b ≲ 2, a narrow corner.
- SERAPIS-KL needs no condensate, so b = 0 is allowed: another reason to prefer the KL form.
- Their "Swampland" claim for τ → i∞ applies to models with b ~ O(10). Our inflation range is compatible only in the small-b corner. This is a real, checkable condition on any future home.
Status: the home requirement is now: factorised T² ⊕ T⁴, flux-free T², and gauge sectors with |b^{N=2}| ≲ 2 on that T² (ideally 0).

## D554 — DEEP (Dp 1, 22:52 CT; literature + scored estimate, locked PREREG_D554_KK_CUTOFF; results/kk_cutoff_d554.txt) — the cusp is a decompactification limit; the SERAPIS path stays inside the EFT for a high string scale
Literature:
- Leedom, Righi, Westphal (arXiv:2605.05322, May 2026): heterotic orbifolds with a Wilson line have an Sp(4,Z) duality group, W = Ω(S)H/χ_γ (Siegel cusp forms), and no dS at the elliptic fixed points (metastable dS only for A(S,S̄) > 3). At large Im T/U the string-derived potential DIVERGES, because a KK tower becomes light and the EFT breaks down. String-derived modular potentials therefore have no cusp plateau, consistent with D535 and D553.
- Kobayashi, Nitta, Urakawa (arXiv:1604.02995): in-class modular inflation is small-field, a hilltop near |T| = 1 driven by the axion, with r ~ 1e-8 (adds to D536).
Estimate: M_KK = M_s/√(A·y) at y* = 158.
- M_s = 1e17 GeV, A = 1: M_KK = 8e15 GeV, M_KK/H = 870, M_KK/V^{1/4} = 1.3.
- M_s = 3.7e17 GeV (weak-coupling heterotic): M_KK = 9e15–3e16 GeV (A = 10–1), i.e. 1.5–4.9 × V^{1/4}.
- M_s = 1e16 GeV: M_KK/V^{1/4} = 0.04–0.13, so the inflation energy would be above the KK scale.
Verdict: EFT CONTROLLED for M_s ≳ 1e17 GeV with A ≲ 10 (H ≪ M_KK everywhere; V^{1/4} < M_KK). Not controlled for a low string scale.
Consequences:
- SERAPIS needs a high string scale (M_s ≳ 1e17 GeV). That is natural for the weakly coupled heterotic string and fits D530's heterotic preference.
- It is in tension with the Twist-2 IIB branch's low M_s (7e13–3.5e14 GeV, D453): SERAPIS and the Twist-2 FI realisation cannot share a string scale. Recorded as a CENTRE incompatibility. SERAPIS is the inflation-side model; the Twist-2 numbers do not carry over.
- The light KK tower near the cusp is exactly why string-derived potentials blow up there. SERAPIS-KL's plateau must therefore come from physics that dominates the KK-tower effects at y ≲ 160. An open, sharp question for the string-origin gap.
Status: the home requirement now includes M_s ≳ 1e17 GeV.

## D555 — DEEP (loop tick 7 / Dp 2; scored, locked PREREG_D555_CASAS_IBANEZ; results/casas_ibanez_d555.txt) — CORRECTION to D550: a modular cusp-plateau potential with V = 0 at τ = i already exists (Casas–Ibáñez)
- Casas & Ibáñez (arXiv:2407.12081): V ∝ y²|Ĝ₂|²/N², with Ĝ₂ = E₂ − 3/(π Im τ). Computed: Ĝ₂(i) = 0 and Ĝ₂(ρ) = 0 (to 1e-16). So V = 0 at τ = i AND at ρ, and τ = i is a minimum in all four tested directions.
- Their potential therefore already has a species-scale (string-motivated) cusp plateau with its zero at τ = i. D550's "τ = i minimum not found in the checked literature" is WITHDRAWN. Our |j − 1728| invariant differs only in making ρ a non-zero point (V(ω) = 0.052 V₀, D545), versus Casas–Ibáñez's double zero at i and ρ.
- Inflation as I implemented their formula (canonical φ = √(3α/2) ln y; N = −ln(y|η|⁴)) is NOT viable:
  - α = 1/3: n_s ≈ 1.06, r ≈ 0.006–0.007;
  - α = 1: n_s ≈ 0.5.
  This may be my reading of their normalisation (their paper relates N_e to the number of species and works in a regime I may not reproduce). Labelled: "our implementation of the quoted form", not a verdict on their paper.
Action: v2.2 must drop the "not found in the checked literature" sentence and credit Casas–Ibáñez for a τ = i zero with a cusp plateau. The novelty of SERAPIS-KL shrinks to "an α = 1/3 attractor invariant with its single zero at i, regular at ρ".
Process lesson: two of tonight's novelty checks (D544, D550) were reversed by the next search. Novelty statements need a dedicated search before they go into a paper.

## D556 — DEEP (Dp 3, 22:56 CT; literature, dedicated novelty audit as D555 required) — the SERAPIS inflation model has no novel element left
Searches: one extended and one standard. Checked: Kallosh–Linde 2412.19324 (potentials vanish at ω; i is a dS saddle; no E₆/|j−1728| forms) and Abe, Higaki, Kaneko, Kobayashi, Otsuka, arXiv:2303.02947, "Moduli inflation from modular flavor symmetries".
Finding: 2303.02947 uses W = Λ²Y(τ)X with a weight-6 modular form (E₆-type, zero at i) and a Kähler flattening V = Λ⁴Ṽ/(1+αṼ). The vacuum is at τ = i. Inflation runs near Im τ ≈ 1–3 (pole/attractor-like), with n_s 0.962–0.974 and r ~ 1e-5. So "vacuum at τ = i through the E₆ / j − 1728 zero" is prior art (2023), and Casas–Ibáñez (2024) also vanish at i (D555).
Audit result (honest):
- cusp plateau with exact SL(2,Z): Kallosh–Linde 2408.05203, Casas–Ibáñez 2407.12081;
- vacuum at τ = i from the E₆/j − 1728 zero: Abe et al. 2303.02947, Casas–Ibáñez;
- lifted plateau raising n_s (Chronos): Kallosh–Linde 2512.02969;
- α = 1/3 attractor numbers (Kairos): standard.
SERAPIS-KL is a combination of published ingredients, with no new mechanism.
What remains as the work's own contribution:
(1) the specific combination tested end to end, with reheating at the model's own N* and the stiff-reheating no-go (D534);
(2) the D553/D554 home conditions applied to a cusp-plateau model (|b| ≲ 2, M_s ≳ 1e17 GeV);
(3) the parity scan with anomaly and τ = i selection checks (D528–D533, D542, D551), applying 2207.14014's mechanism;
(4) the data framing and the public audit trail, including withdrawals.
v2.2 must credit 2303.02947 and state plainly that the inflation model is assembled from published ingredients.

## D557 — DEEP (Dp tick, 22:53 CT; literature + arithmetic) — light-tower corrections to SERAPIS's predictions are negligible
Lüst, Masias, Pieroni, Scalisi (arXiv:2512.07930): a tower whose masses fall with the inflaton corrects n_s, r and f_NL by ~ (H/Λ_sp)^{2+p} (p = 1 for an equispaced KK tower). Consistency needs H ≪ Λ_sp.
SERAPIS: H = 9.1e12 GeV and Λ_sp ≈ 2.2e17 GeV at Im τ* (D540), so H/Λ_sp = 4e-5 and the corrections are ~ (4e-5)³ ≈ 7e-14. Negligible.
PC: J2 at 11 of 16 points (all FAIL so far); J3 not started.
Status: the tower is no threat to the predictions in the controlled regime (M_s ≳ 1e17 GeV, D554). The open string-origin question is about the plateau's existence, not about corrections to it.

## D558 — DEEP (Dp, 23:01 CT; scored, locked PREREG_D558_CI_CORRECT; results/ci_correct_d558.txt) — Casas–Ibáñez with their exact N: my numerics do NOT reproduce their quoted n_s; discrepancy unresolved
Their v2 (read 22:59 CT): V ∝ (τ₂G̃₂/N)², G̃₂ = G₂ − π/τ₂, N = −6 ln[2τ₂|η|⁴] + Ñ₀ with Ñ₀ = 25, τ₂ = e^{aφ}. Quoted: n_s ≈ 0.966, r ≈ 0.0033 (a = √(2/3)) and r ≈ 0.0011 (a = √2) at N_e = 60, from the large-τ₂ form V ∝ |π/3 − e^{−aφ}|².
My full numerics, with the −6 ln(2τ₂) and Ñ₀ terms kept:
- a = √(2/3): n_s 0.953–0.958, r 0.0010–0.0014;
- a = √2: n_s 0.941–0.946, r ~ 2e-4 (N* = 52–60).
The log term in N slows the approach to the plateau and lowers n_s. Their quoted numbers match the leading large-τ₂ form, which drops it.
I cannot tell from here whether they justify dropping it or whether I mis-normalised something else. Labelled: an unresolved discrepancy, not a verdict on their paper.
- D555's inflation numbers used a wrong N (missing the factor 6 and Ñ₀) and are superseded by this note.
- D555's vacuum finding (V = 0 at τ = i, G̃₂(i) = 0) stands.
Also: Aoki & Otsuka (arXiv:2411.08467) tie n_s to the species scale in this class (N_e ≈ (M_P/Λ_sp)²/(2πa²c_n)); for the Planck n_s, Λ_sp ≈ 9e16 GeV (a = 1). Our D540 estimate, Λ_sp ≈ 2.2e17 GeV at Im τ* ≈ 126, is in the same range.
Relevance to SERAPIS: the species-scale route is the leading candidate string mechanism for a cusp plateau. If the log correction in N is physical, it lowers n_s for that route (worse for both branches), so the string-origin question and the n_s prediction are coupled.

## D559 — DEEP (Dp, 23:06 CT; scored, locked PREREG_D559_CI_DIAG; results/ci_diag_d559.txt) — D558 discrepancy explained: the species-scale plateau is strongly Ñ₀-dependent once the log term is kept
Setup: a = √(2/3), N* = 60.
- (A) N = 2πτ₂ (their analytic limit): n_s = 0.9679, r = 0.0030. Close to their 0.9654 / 0.0033 (eq. 5.29/5.30), which validates my code and normalisation.
- (B) Full N, Ñ₀ = 0: n_s = 1.041, r = 0.009.
- (C) Full N, Ñ₀ = 25: n_s = 0.958, r = 0.0010 (= D558).
- (D) Full N, Ñ₀ = 100: n_s = 0.965, r = 0.0030, but the horizon-exit point moves to y* ≈ 890.
Conclusion: with the exact species function, n_s swings from 0.958 to 1.04 as Ñ₀ goes from 0 to 100. That contradicts the paper's statement that the parameters are "practically independent" of Ñ₀ ≲ 100 and its footnote that a full numerical calculation gives the same results (arXiv:2407.12081v2, §4, §5.1, fn. 3). The reason: at τ₂ ~ 100, the −6 ln(2τ₂) and Ñ₀ pieces of N give 1/τ₂ corrections that are LARGER than the −3/(πτ₂) term kept in their analytic limit.
Same pathology as D541 (our SERAPIS-2 with −ln(2y|η|⁴) + κ′): plateaus built from the genus-one/threshold function are not predictive unless the constant is fixed from first principles.
Label: our numerics against their analytic claim. A possible issue for their paper, worth a careful recheck before anyone says so publicly (could be a convention I have not matched). Not a verdict.
Consequence for SERAPIS: the leading string-motivated plateau mechanism does not give a sharp n_s without knowing Ñ₀ (the number of species at the desert point). Kairos's sharpness (D545) holds for the attractor invariant, not for this route.

## D560 — DEEP (DpL tick 1, 23:03 CT; literature + arithmetic estimate, not locked) — the UNIVERSAL N = 2 threshold rules out the N = 2-plane home: SERAPIS needs a torus with no N = 2 threshold (Z₃-like or N = 4)
Literature:
- Kiritsis, Kounnas, Petropoulos, Rizos (hep-th/9608034): N = 2 thresholds are Δ_i = b_i Δ − k_i Y. The universal part Y is gauge-independent and has the same coefficient in every N = 2 model (it is fixed by N_H − N_V = 242). It is minimal at the self-dual points (Y(i,i) ≈ 24.4) and grows like Y ≈ 4πR² ∝ Im T at large radius: the decompactification problem. The proposed remedy is N = 4 with spontaneously broken SUSY. The Z₃ orbifold, with no N = 2 sectors, has Δ^{N=2} = 0.
- Parameswaran, Ramos-Sánchez, Zavala (arXiv:1009.3931): in MSSM Z₆-II heterotic orbifolds the N = 2 planes (T₂, T₃, U) enter through η-functions; T₁ (an N = 1 plane) does not enter the thresholds. No fully stable vacuum was found.
Estimate (arithmetic, label: estimate): perturbativity 16π² k Im S > Y with Y ≈ 4π Im T gives Im T ≲ 4π Im S = 25 (Im S = 2), 38 (3) or 63 (5). That is far below SERAPIS's Im τ* = 112–158, and it holds EVEN WHEN b^{N=2} = 0. So D553's "|b| ≲ 2" escape is insufficient on an N = 2 plane.
Consequence (revises D530): the SERAPIS torus must NOT be an N = 2 fixed plane. It must be a plane without N = 2 thresholds, such as an N = 1 plane like T₁ in Z₆-II, a Z₃-type plane, or an N = 4 sector with spontaneously broken SUSY.
- For SERAPIS-KL this is fine: it needs no η-threshold in W (D545).
- For holomorphic SERAPIS-1 it is fatal: its η⁻² factor needed an N = 2 threshold (D530), and that threshold makes large Im τ non-perturbative.
So SERAPIS-KL on an N = 1/N = 4 plane is the only consistent home class. Its full SL(2,Z) on such a plane, and the source of its potential (no threshold, so not CI-type either), remain open.
Status: home class revised: T² ⊕ T⁴ with the SERAPIS T² in an N = 1 or N = 4 sector (no N = 2 threshold), flux-free, M_s ≳ 1e17 GeV. Retires D530's "N = 2 fixed plane".

## D561 — DEEP (Dp now, 23:05 CT; literature + arithmetic estimate, not locked) — the two escape routes from D560 each carry a price
(i) The N = 1-plane route (no N = 2 threshold on the SERAPIS T²).
- Kähler moduli carry a [SL(2,Z)]_T per modulus, but Wilson lines in semi-realistic heterotic models break it to congruence subgroups (Nilles, Ramos-Sánchez, Vaudrevange et al., arXiv:1707.09966). So the SERAPIS plane must carry NO Wilson line, consistent with D530's full-SL(2,Z) need.
- Price: with no threshold there, nothing perturbative generates a potential for that T. The SERAPIS-KL V must come from elsewhere (non-perturbative, or the nilpotent sector), which is the open D552 gap again.
(ii) The N = 4 → N = 2 Scherk–Schwarz route.
- Kiritsis, Kounnas, Petropoulos, Rizos, "Solving the decompactification problem" (hep-th/9606087): with N = 4 spontaneously broken by a Z₂ translation on the T², the universal threshold VANISHES at large radius and non-universal ones grow only like log R². That cures D560.
- Price: SUSY breaking is tied to the radius, m₃/₂ ~ M_s/R ~ M_s/√(Im τ). At M_s = 1e17 GeV this gives m₃/₂ ~ 8e15 GeV at Im τ* = 158 (6.6e16 GeV at the end). That is incompatible with the eV gravitino of the gauge-mediation sector (D474, D548), which would have to be replaced.
- A one-loop Casimir energy ~ (n_F − n_B) m₃/₂⁴/16π² has V^{1/4} ~ 2.2e15 GeV per net degree of freedom at Im τ*, the same order as V_inf^{1/4} = 6e15 GeV. It would distort or destroy the plateau unless the spectrum is Bose–Fermi degenerate (n_F = n_B, "super no-scale" models).
Verdict: neither route is free. Route (i) leaves the potential's origin open. Route (ii) needs Bose–Fermi degeneracy and gives up the eV-gravitino phenomenology.
Status: the home question is now sharp. SERAPIS-KL on a Wilson-line-free N = 1 plane with a non-perturbative/nilpotent origin of V, or on a Scherk–Schwarz T² with a Bose–Fermi-degenerate spectrum. Either is a substantial model-building project; neither is resolved here.

## D562 — DEEP (Dp now, 23:08 CT; literature + reasoning, not locked) — the Scherk–Schwarz route fails AT THE VACUUM: only the N = 1-plane route survives
Literature:
- Kounnas & Partouche (arXiv:1701.00545): in heterotic N = 2 → 0 models (T²×T⁴/Z₂) the one-loop potential is ≈ ξ(n_F − n_B)m₃/₂⁴ + O(e^{−cM_s/m₃/₂}), with m₃/₂ ∝ 1/(SS-circle volume). Under the super no-scale condition n_F = n_B the potential and tadpoles are exponentially small. Λ can come out near the observed value when m₃/₂ ≈ 1e-2 cM_s. m₃/₂ is a tree-level flat direction.
- Florakis, Rizos, Violaris-Gountonis (arXiv:2110.06752): super no-scale Pati–Salam models; the potential is exponentially suppressed only for a compactification scale well below M_s.
Reasoning for SERAPIS:
- On the plateau (Im τ ~ 100–160), n_F = n_B would suppress the Casimir term to ~e^{−c√Im τ}. The D561 competition could be cured during inflation.
- But the SERAPIS vacuum is at τ = i, the self-dual point. The SS circle is at string size there, so m₃/₂ ~ M_s, the exponential suppression is gone (e^{−c} ~ O(1)), and the vacuum energy would be ~ M_s⁴ ~ 1e68 GeV⁴. Self-dual points also bring extra massless states (enhanced symmetry), which spoils n_F = n_B.
- Exponentially small Λ in these models needs m₃/₂ ≪ M_s, i.e. a LARGE radius today. That is the opposite of SERAPIS's τ = i vacuum.
Verdict: route (ii) is incompatible with a vacuum at τ = i. With D560 and D561, the only surviving home class is a Wilson-line-free N = 1 plane (no N = 2 threshold), flux-free, M_s ≳ 1e17 GeV, with the SERAPIS-KL potential coming from a non-perturbative or nilpotent sector whose string origin is unknown.
Status: home class narrowed to one option. The decisive open question is a non-perturbative, SL(2,Z)-invariant source on an N = 1 plane that is flat at the cusp. That is exactly where string-derived modular potentials diverge (D554), so it may not exist. Flagged as the critical test for whether SERAPIS can have a string home at all.

## D563 — DEEP (Dp now, 23:13 CT; scored, locked PREREG_D563_SERAPIS_NP; results/serapis_np_d563.txt) — SERAPIS-NP: an instanton-type plateau inflates near Im τ ≈ 2 and escapes every home problem, at the price of tiny r
Model: K = −ln(2 Im τ), V = V₀|j − 1728|²/(|j − 1728|² + 1728²). The approach to the plateau is e^{−4π Im τ}, as from an instanton.
Checks: V(i) = 0, a minimum in all directions; single-valued.
Results:
- N* = 52: n_s = 0.9600, r = 2.5e-6 (−2.8σ SPA, −4.7σ SPA+DESI).
- N* = 55.6: n_s = 0.9626, r = 2.2e-6 (−1.9σ, −3.8σ).
- The pre-stated analytic expectation (n_s ≈ 1 − 2/N, r ≪ 1e-3) is confirmed; n_s comes out ~0.0015 below 1 − 2/N.
- Inflation happens at Im τ* ≈ 2.07, ending at 1.44. The horizon scales exit near the square torus, NOT at the cusp.
Why this matters:
- Im τ ≈ 2 is far inside every bound: perturbativity Im T ≲ 25 even on an N = 2 plane (D560); KK tower M_KK ~ M_s/1.4 (D554); |b| condition (D553).
- The decompactification, threshold and Scherk–Schwarz problems (D553–D562) all disappear, and a non-perturbative (instanton-like) origin is natural.
Price:
- r ~ 2e-6, unobservable by LiteBIRD or CMB-S4. It is falsified by any r ≳ 1e-4 detection.
- n_s 0.960–0.963 sits slightly BELOW Kairos: tension 1.9–2.8σ with CMB-SPA and ≥ 3.8σ with SPA+DESI.
Prior art: very close to Abe, Higaki, Kaneko, Kobayashi, Otsuka (arXiv:2303.02947): vacuum at τ = i from a weight-6 form, inflation near Im τ ≈ 1–3, r ~ 1e-5, n_s 0.962–0.974 with their Kähler flattening. SERAPIS-NP is essentially in their class; not novel.
Status: a third branch exists. It is string-friendly (low Im τ) but disfavoured by current n_s and has unobservable r.
- Data split: r ≳ 1e-3 → SERAPIS-KL type (needs the unsolved cusp home); r unobserved and n_s ~ 0.96 → NP type.
- The current n_s (≥ 0.968) disfavours NP. So the "home" problem and the "n_s" problem pull in opposite directions.

## D564 — DEEP (Dp now, 23:16 CT; scored, locked PREREG_D564_SERAPIS_P; results/serapis_p_d564.txt) — HOME-SAFE KAIROS EXISTS: raising the invariant's power moves inflation inside Im τ ≲ 25 with n_s unchanged
Model: V = V₀ Iᵖ/(Iᵖ + 1), with the D545 invariant I; minimum at i checked for p = 2.
| p | y* (N* = 52–55.6) | n_s | r | home (y* ≤ 25) |
|---|---|---|---|---|
| 1 | 112–119 | 0.9631–0.9654 | 1.3e-3 | no |
| 1.5 | 42–44 | 0.9634–0.9657 | 4.8–5.4e-4 | no |
| 2 | 23.5–24.2 | 0.9635–0.9658 | 2.5–2.9e-4 | YES |
| 3 | 12.0–12.2 | 0.9636–0.9659 | 1.0–1.1e-4 | YES |
These confirm the pre-stated expectation (y* ∝ N^{1/p}; r ≈ 4/(p²N²), somewhat below the analytic value). p acts as an effective attractor parameter, α_eff = α/p².
Result:
- Kairos's n_s (0.963–0.966) is independent of p, but r and the location of inflation trade off one-to-one.
- A perturbatively safe home (Im τ* ≲ 25, D560; even on an N = 2 plane; also inside the D553 b-bound for |b| ≲ 10, since 25 < 34) requires p ≳ 2, i.e. r ≲ 3e-4.
Sharp, falsifiable relation (our application of known attractor scaling to the modular home bounds):
- r ≳ 5e-4 → horizon exit at Im τ ≳ 40 → no perturbative heterotic home known (D553–D562);
- r ≲ 3e-4 → home-safe.
CMB-S4-class σ(r) ~ 4e-4 would partly test the boundary; LiteBIRD σ(r) ~ 1e-3 only the p = 1 case.
Novelty caution (per D555 lesson): this is the standard α-attractor r–α relation (r = 12α/N²; small α ↔ small field range is known in the swampland literature). Only its mapping onto the modular perturbativity bound is ours. Not claimed as new physics.
Status: SERAPIS now has a home-compatible Kairos variant (p = 2–3: n_s 0.964–0.966, r 1–3e-4) and a home-incompatible original (p = 1: r 1.2e-3). Chronos with p = 2 is not computed (expected: n_s ~0.972, r ~ 5e-4). Revises the v2.2 r-prediction range: "r = 1e-4 to 2e-3 depending on p, with string-home consistency requiring r ≲ 3e-4."

## D565 — DEEP (DpL tick 2, 23:19 CT; scored, locked PREREG_D565_CHRONOS_P2; results/chronos_p2_d565.txt) — home-safe Chronos FAILS with the D525 tilt
p = 2 with δ = 0.0023: n_s = 0.980–0.982 (+2.6σ to +3.3σ vs SPA+DESI), r = 7.5–8e-4, y* = 31–33, outside Im τ ≤ 25. Verdict by the lock: NOT HOME-SAFE (it fails both conditions). The tilt bites harder at p = 2 and also pushes horizon exit outward.
Grid: δ = 0.002 → n_s 0.978–0.980, y* 30–32; δ = 0.003 → 0.983–0.985; δ = 0.005 → 0.990.
Interpolating between δ = 0 (D564: 0.9635, y* 23.5) and δ = 0.002 (labelled an estimate, NOT a fit to be adopted): n_s = 0.9728 would need δ ≈ 0.0013 and gives y* ≈ 27, just outside the bound.
Conclusion: a string-home-compatible SERAPIS fits CMB-SPA (Kairos p ≥ 2, D564) but NOT the DESI-including n_s. Chronos-type n_s ~ 0.973 pushes inflation to Im τ ≳ 27, where the perturbativity bound fails (marginally at Im S = 2; it passes for Im S ≥ 3, where the bound is 38).
The fork becomes:
- DESI-n_s real → Chronos → weaker coupling (Im S ≳ 3) or no perturbative home;
- CMB-only n_s → home-safe Kairos (p ≥ 2, r ~ 1–3e-4).

## D566 — DEEP (Dp now, 23:22 CT; scored, locked PREREG_D566_BOUND_ALPHA; results/bound_alpha_d566.txt) — the home bound is Im T ≲ k·α⁻¹(M_s) ≈ 29: home-safe Kairos fits, and DESI-level Chronos is marginal
Identity: Im T_max ≈ 4πk Im S = k·α⁻¹(M_s).
One-loop running (SM to 1e5 GeV, then MSSM): α⁻¹(U1, SU2, SU3) = 25.4, 28.7, 29.5 at M_s = 1e17 GeV and 24.0, 28.5, 30.1 at 3.7e17. With k = 1 for SU(2)/SU(3), Im T_max ≈ 28.5–28.7. U(1)_Y with k = 5/3 gives about 40–42.
Inside the bound:
- Kairos p = 3 (y* = 12): inside.
- Kairos p = 2 (23.5–24.2): inside.
- Chronos at the DESI n_s with p = 2 (y* ≈ 27): inside, marginally. That y* is the D565 interpolation for δ ≈ 0.0013, a post-hoc value, not a locked fit.
- Kairos p = 1 (112–119): outside.
Caveats: Y ≈ 4π Im T is an asymptotic coefficient, and O(10%) margins are not decisive. The bound is ~29, not D560's 25 (which used Im S = 2, i.e. α⁻¹ = 25).
Status: both branches can sit inside a perturbative heterotic home if p ≳ 2, but Chronos only with a retuned tilt (δ ≈ 0.0013 instead of 0.0023), just under the bound, and with r ~ 4–6e-4 (estimate).
A clean falsifiable package (home-consistent SERAPIS): n_s 0.964–0.966 with r 1–3e-4 (Kairos p = 2–3), or n_s ≈ 0.973 with r ≈ 4–6e-4 (Chronos p = 2, retuned). Locking Chronos p = 2 with δ = 0.0013 as a new forward prediction needs its own PREREG and is scored only on future data.

## D567 — FORWARD PREDICTIONS (Dp now, 23:25 CT; locked PREREG_D567_FORWARD_HOMESAFE; results/forward_homesafe_d567.txt) — frozen bands for home-consistent SERAPIS, scored only on future data
- HS-Kairos (p = 2, δ = 0): n_s = 0.9635–0.9658, r = 2.5–2.9e-4, y* = 23.5–24.2 (inside the bound of ≈ 28.5).
- HS-Chronos (p = 2, δ = 0.0013; post-hoc δ declared in the lock): n_s = 0.9736–0.9759, r = 4.8–5.3e-4, y* = 27.5–28.6. This is ON the home bound (≈ 28.5), i.e. marginal at N* = 55.6.
Scoring rule (from the lock): DISFAVOURED if a future n_s lies > 3σ outside the band; or if r is detected at > 3σ outside [0.5 r_min, 2 r_max]; or if r < 0.5 r_min at 95% CL.
Concretely:
- HS-Kairos is excluded by r < 1.3e-4 (95%) or by a detection of r > 5.8e-4.
- HS-Chronos is excluded by r < 2.4e-4 (95%) or by a detection of r > 1.06e-3.
Who can test it: CMB-S4-class σ(r) ~ 4e-4 (delensed) reaches the HS-Chronos level only at about 1σ. A full test needs σ(r) ≲ 1e-4 (next-generation, post-LiteBIRD).
Note: the original Kairos/Chronos (p = 1; r ≈ 1.2e-3 / 2e-3) remain the published v2.2 predictions. D567 adds the home-consistent pair.

## D568 — DEEP (Dp now, 23:28 CT; literature + reasoning) — the home-safe versions need an effective α below the "maximal-SUSY" lower end: a tension with B-mode-target lore
- Kallosh, Linde, Wrase, Yamada (arXiv:1704.04829; from Ferrara–Kallosh): maximal-supersymmetry (seven-disk) constructions give 3α = 1…7, i.e. B-mode targets r ≈ 1e-3 to 1e-2. The LOWEST value, 3α = 1, gives r ≈ 1e-3. Values below 1 are possible in generic N = 1 supergravity but do not come from that construction.
- SERAPIS's field-space geometry stays α = 1/3 (K = −ln 2 Im τ, the unit disk, 3α = 1). HS-Kairos/HS-Chronos (p = 2) instead act like α_eff = α/p² = 1/12 (3α_eff = 1/4) because the potential's leading 1/Im τ term is absent (V ≈ 1 − c/Im τ²). So the home-safe models sit BELOW the maximal-SUSY B-mode targets (r ~ 2.5–5e-4 versus ≥ 1e-3).
- Naturalness: a cusp potential with no 1/Im τ term needs that coefficient to vanish. String corrections (α′, loop) generically produce 1/Vol ∝ 1/Im τ terms. HS models therefore need either a symmetry that forbids the 1/Im τ term, or a tuning of order (1/Im τ*) ~ 4% between the induced 1/Im τ coefficient and the 1/Im τ² one. That is a real cost, to be stated alongside D567.
Synthesis of D560–D568:
- p = 1 (natural attractor, r ~ 1e-3, the B-mode target) needs Im τ* ~ 115: no perturbative home.
- p ≥ 2 (home-safe) needs a missing 1/Im τ term: a mild tuning, and r below the standard targets.
So SERAPIS faces a "home vs naturalness" trade-off, quantified by r: detecting r ≈ 1e-3 would favour the natural-but-homeless version.
Status: recorded as the main theoretical tension of the home-consistent variants.

## D569 — DEEP (Dp now, 23:33 CT; scored, locked PREREG_D569_EISENSTEIN; results/eisenstein_d569.txt) — Eisenstein-series plateaus are natural and home-safe, but their vacuum is at ρ, not i
Idea: the non-holomorphic Eisenstein series E(τ, s) (the coefficients of higher-derivative string couplings, s = 3/2, 5/2, 3, …) are SL(2,Z)-invariant and grow as y^s with NO 1/y term. A plateau V = V₀[1 − E_min/E(τ, s)] therefore has p = s naturally, answering the D568 naturalness cost.
Computed (lattice sum):
- For every s tested (1.5, 2, 2.5, 3), E(ρ) < E(i), so the minimum (V = 0) is at ρ.
- s = 2.5: n_s 0.962–0.964, r = 2.0–2.3e-4, y* = 18.6–19.1 (home-safe, below the bound of ≈ 28.5).
- s = 3: n_s 0.962–0.964, r = 1.4–1.6e-4, y* ≈ 12.5.
Verdict: a natural, string-motivated, home-safe Kairos-like plateau EXISTS, but it puts the vacuum at ρ (the hexagonal torus), as in Kallosh–Linde. SERAPIS's τ = i vacuum is the unnatural element here; it needs the |j − 1728| construction (D545/D564), which has no Eisenstein-type motivation.
Consequences:
- A ρ-vacuum variant would change the matter selection rule from mod 4 to mod 6 (D551 would need redoing) and loses the "square torus today" picture.
- n_s is slightly below HS-Kairos (−1.3σ to −2.2σ SPA; ≥ 3.1σ off SPA+DESI).
Honest summary: the most natural string-motivated modular plateau (Eisenstein s ≥ 2, ρ-vacuum, r ~ 1–2e-4) is not SERAPIS. SERAPIS's distinctive τ = i vacuum costs naturalness. Prior art: Eisenstein invariants are standard (Kallosh–Linde list L_G₂ / E-type invariants; Green–Gutperle for the string couplings); the r-values here are our computation.

## D570 — the SERAPIS equation and scorecard (Danny 23:15 "make an equation for mine and test the scores"; locked PREREG_D570; results/serapis_equation_d570.txt)
Equation: n_s ≈ 1 − 2/N* + Δ_δ; r ≈ (1 − n_s,0)²/p²; α_s ≈ −(1 − n_s,0)²/2. α = 1/3 geometry, p = invariant power, N* = 52–55.6.
Validation against the full computations:
- n_s: the equation is low by 0.0014–0.0021 (computed n_s is slightly higher).
- r: computed/equation = 0.89–0.90 (p = 1), 0.77–0.78 (p = 2), 0.68–0.69 (p = 3).
- Usable form: n_s ≈ 1 − 2/N* + 0.0018, and r ≈ (1 − n_s)²/p² to within 10–30%.
Scorecard (POST-DATA, descriptive; worst N* end; grades A < 1σ, B < 2σ, C < 3σ, F > 3σ):
- Kairos p = 1: A Planck, A SPT+Planck, B CMB-SPA, F SPA+DESI, F P-ACT-LB.
- Chronos p = 1: C, C, B, A, B.
- HS-Kairos p = 2: A, A, B, F, F.
- HS-Chronos p = 2: C, F (SPT+Planck), C, B, A.
- SERAPIS-NP: B, B, C, F, F.
- Eisenstein s = 2.5 (ρ vacuum): A, A, C, F, F.
- All variants pass r < 0.036.
Reading: no single variant scores well on every data set, because the data sets disagree with each other (the CMB-vs-DESI split). Kairos-type wins on CMB-only data; Chronos-type wins on DESI-including data. The real scored test is D567 (future data only).

## D571 (ATLAS): four catalogue discovery hunts, H2–H4 results (H1 pending)
Lock: field_tests/rules/PREREG_D571_DISCOVERY_HUNTS.md (sha256 committed in e434cc1, before any download). Scripts: apps/cosmos_atlas/hunts/. Results: field_tests/results/D571_H*.json. Data: Gaia DR3 through the AIP TAP mirror, NASA Exoplanet Archive TOI table, VizieR (CfA) VSX and Milliquas v8.

**H2: fast-star origins** (190 vetted "solid" stars; galpy MWPotential2014 scaled to v_c = 236 km/s; 300 Myr backward integration).
- Validation: S5-HVS1 traces back to r_min = 36 pc from the Galactic Centre (GC), 4.8 Myr ago, matching Koposov+2020.
- 15 stars have a Gaia RV.
  - The known HV* UCAC2 13256026 (Gaia 6675997285440115328) is recovered: 87% of draws pass within 1 kpc of the GC and 55% are unbound in this potential.
  - Gaia DR3 6870578373607170432 (G = 13.4, ϖ/σ = 23, d = 2.5 kpc, RV = +164): v_GC = 471 vs v_esc = 426 km/s (76% of draws unbound), but r_min,GC = 6.1 kpc, so it does NOT come from the GC. It is not in SIMBAD, and a web search for the ID found nothing.
  - Caveat: MWPotential2014's v_esc is low. Against the measured local v_esc ≈ 530 km/s this star is most likely a bound, fast halo star, not a hypervelocity star.
- 175 stars without RV: 56 reach r_min,GC < 1 kpc for some RV within ±800 km/s. Each has a predicted RV window (median width 130 km/s), so a spectrum can test it.
  - Honest reading: bound halo stars on radial orbits pass near the GC routinely. A GC passage at bound speed (only 4 of the 56 would be unbound at RV*) is NOT evidence of ejection.
- Verdict: no new hypervelocity star. The method is validated. One candidate (6870578373607170432) is worth a follow-up spectrum.

**H3: TESS planet candidates for amateurs.**
- Selection: 8175 TOIs → 776 pass PC/APC, Tmag ≤ 12, depth ≥ 3 ppt.
- 5294 transits fall between 15 Nov and 15 Dec 2026; 4142 are non-stale (timing 1σ ≤ 1 h), covering 579 targets. 163 targets have only stale ephemerides.
- Top by score: TOI-6806.01 (48.6 ppt), TOI-890.01 (41.8 ppt; Rp = 34.6 R⊕, likely an eclipsing binary), TOI-3241.01, TOI-3491.01, TOI-3501.01.
- Caveats: deep, large-radius candidates are often eclipsing binaries, which amateur photometry (TFOP SG1) is good at catching. Times are BJD_TDB shown as UTC (error < 2 min).

**H4: bright Gaia variables vs VSX** (G < 11, score ≥ 0.7).
- 50,943 Gaia variables; 46,479 match VSX (max < 13) within 10″; 4464 do not.
- Of the unmatched, 227 have a VSX entry 10–60″ away (probably the same star at a poorer position), and 4237 have none within 60″.
- The 4237 by class: 3799 LPV, 375 ACV/CP, 32 SPB, 13 δSct/γDor, 11 αCyg, 4 βCep, 2 ECL, 1 Be. G ranges from 5.2 to 11 (median 10.6).
- Caveat: the VSX max < 13 cut drops entries that have no max magnitude, and Gaia's "LPV" class includes many low-amplitude red giants. A SIMBAD check by Gaia ID is queued on the PC (fetch_hunts2.py).
- Verdict: these are follow-up candidates (VSX-submission material), not discoveries.

**H1:** the AIP async result for the Gaia quasar join (job 00627678…) completed server-side; the download to the PC was still in progress when the PC went offline. Pending.

## D572 — DEEP (DpL tick 1, 01:35 CT 15 Nov; literature, not locked) — prior art for SERAPIS-NP, and still no τ = i source on an N = 1 plane
Gap (D562): is there a non-perturbative or loop-generated SL(2,Z) potential, flat at the cusp, with its vacuum at τ = i?
New papers (none previously cited in our notes):
- **Abe et al., "Finite modular Coleman–Weinberg inflation", arXiv:2607.00528.**
  - Mechanism: a one-loop CW potential from vector-like quarks whose mass is a Γ₃ modular form, W = M_Q Y^(k)(τ) Q̄Q.
  - Inflation: double-exponential plateau toward the cusp; vacuum at Im τ₀ ≈ 1.7–4.2 (typically ~2), not at i or ω.
  - Numbers (N = 55): n_s ≈ 0.960–0.962, r ≈ 3e-6 to 2e-5, α_s ≈ −7e-4, T_R ~ 1e9 GeV.
  - Needs a constant F-term uplift; the authors call it bottom-up.
  - → **Our SERAPIS-NP (D563: Im τ ≈ 2, n_s 0.960–0.963, r ~ 2e-6) is the same regime, already published.** D563 is not novel. It also gains a concrete origin (matter loops), so it is no longer an orphan.
- **Jiang, Zhao, Ding, "Sp(4,Z) modular inflation", arXiv:2512.21597.**
  - α = 1/3 attractors in genus 2, with Minkowski vacua on τ_i = i.
  - Numbers: n_s 0.967, r ≈ 2e-3 at N = 60 (diagonal case).
  - → A τ = i vacuum with plateau inflation exists in a higher-genus setting, but not on a single SL(2,Z) torus. The N = 1-plane question stays open.
- **Aoki, Otsuka, Yanagita, "Higgs-modular inflation", arXiv:2504.01622.**
  - Uses the known SL(2,Z) forms (η, j) with V ≃ V₀(1 − c/Im τ)², vacuum near τ = i; no UV derivation.
  - → Same bottom-up status as SERAPIS-KL.
Verdict: no string-derived τ = i plateau source found (the gap stays open). Prior-art list extended: D563 ≈ 2607.00528, and τ = i Minkowski vacua ≈ 2512.21597 and 2504.01622. No computation was needed.

## D573 — DEEP (DpL tick 2, 01:27 CT 15 Nov; literature check) — NULL: no new CMB data since our filter inputs; the D567 bands are unscored
Checked whether any 2026 measurement scores the locked D567 bands.
- Balkenhol et al., arXiv:2512.10613 ("Inflation at the end of 2025") uses SPA (Planck PR3/PR4 + ACT DR6 + SPT-3G D1) + BK18 (+ DESI DR2).
  - SPA+BK: n_s = 0.9682 ± 0.0032, r < 0.034. SPA+BK+DESI: n_s = 0.9728 ± 0.0029, r < 0.035.
  - These are the same data as our F3 inputs (0.9684 ± 0.0030 and 0.9728 ± 0.0027) with r freed. The differences are below 0.1σ.
- No BICEP/Keck or SPT B-mode result newer than BK18 or SPT-3G 2-yr (2505.02827) was found. Also seen: 2601.20958 (causal-source GW constraints) and 2608.20236 (the SPT-3G+ proposal); neither is a primordial-r measurement.
- Ijaz et al. (arXiv:2607.04504) quote the same combinations.
Verdict: NULL. There is no new measurement, so the D567 forward bands stay unscored (their scoring rule needs future data). Distances for information only, not a score:
- HS-Kairos: −0.8 to −1.5σ vs SPA+BK; −2.4 to −3.2σ vs SPA+BK+DESI.
- HS-Chronos: +1.7 to +2.4σ vs SPA+BK; +0.3 to +1.1σ vs SPA+BK+DESI.
The next decisive inputs are Simons Observatory SAT r and DESI DR3. The monthly DESI watch is already scheduled.

## D574 — DERIVATION (Danny 07:28 CT "Derive τ = i"; locked PREREG_D574_TAU_I_DERIVATION; results/tau_i_d574.txt) — what symmetry forces at τ = i, and a flaw it exposes in SERAPIS-KL
What can be derived, with no model input (all three checks passed):
- **A. Stationarity.** S: τ → −1/τ fixes i and acts there as δτ → −δτ. So any S-invariant V that is smooth at i has ∇V(i) = 0.
  - τ = i is ALWAYS a critical point; the symmetry derives this, nothing is chosen. Numerically |∇V(i)| = 0 for p = 1, 2.
- **B. Weight parity.** f(i) = iʷ f(i), so any modular form with w ≢ 0 (mod 4) vanishes at i.
  - E₆(i) = 0 with a simple zero: |E₆(i)| = 7e-16, |E₆′(i)| = 6.66. By contrast |E₄(i)| = 1.456.
  - So j − 1728 ∝ E₆²/Δ has a DOUBLE zero at i (slopes 2.000/1.998/1.999).
  - This is why a superpotential carrying one E₆ factor gives the SUSY Minkowski vacuum at i (D537/D538). It is derived, not tuned.
- What is NOT derived: that i is a MINIMUM rather than a saddle, and that the vacuum has V = 0 rather than Λ (the Leedom–Righi–Westphal no-go, D538). Those depend on the model.

Flaw exposed (C, verified):
- SERAPIS-KL builds I from |j − 1728|². That gives V − V(i) ∝ |τ − i|^{4p}: measured slope 4.00 at p = 1 and 8.00 at p = 2.
- So the reference vacuum is **massless**: quartic at p = 1, octic at p = 2.
- The D539 mass (4.2–4.5e13 GeV) belongs to SERAPIS-1, not SERAPIS-KL. No KL mass was ever computed, and none exists at quadratic order.
- Consequence: after inflation the field oscillates anharmonically, with w = (n − 2)/(n + 2):
  - p = 1 (n = 4): w = 1/3, radiation-like;
  - p = 2 (n = 8, the home-safe versions): w = 3/5, STIFF.
- The D567 N* window [52, 55.6] assumed matter-like reheating, so the D567 bands are conditional (see D567a).

Derived fix tested (C′): build I₁ from |j − 1728|¹ ∝ |E₆|²/|Δ|, the holomorphic-E₆ route.
- p = 1: quadratic, massive vacuum with m/H_inf = 3.70 (slope 2.00).
- p = 2: still quartic (slope 4.00).
- The cusp growth halves (I₁ ≈ y/2), so inflation moves outward:
  - p = 1: y* = 213–227, NOT home-safe; n_s = 0.9621–0.9645 (−4.0 to −3.1σ vs SPA+DESI); r = 1.2–1.4e-3.
  - p = 2: y* = 44–45, NOT home-safe; n_s = 0.9627–0.9650; r = 2.8–3.2e-4.
- Within the one-function family V = f(I^p) there is a trade-off:
  - a massive τ = i vacuum needs V ∝ |τ − i|² near i, which means p·(power of |j − 1728|) = 1;
  - being home-safe needs p ≥ 2 (D564).
  - **No member has both.**

Status: τ = i as a critical point and as a SUSY-Minkowski zero is DERIVED (symmetry plus weight parity). τ = i as a massive, home-safe vacuum is NOT available in SERAPIS-KL as built. One possible way out, not computed and needing its own lock: a two-term V, a plateau plus a separate ε·I₁ mass term. That term grows ∝ y at the cusp, i.e. it acts like a Chronos-type tilt.

## D567a — CORRECTION to D567 (from D574): the forward bands are conditional
The HS-Kairos and HS-Chronos bands assume matter-like reheating, N* ∈ [52, 55.6]. D574 shows the SERAPIS-KL vacuum at p = 2 is octic, giving a stiff oscillation phase (w = 3/5), which raises N*. The bands stand as locked, but are now labelled "conditional on an added vacuum-mass source". Any rescoring needs its own lock; nothing is refitted here.

## D575 — pp (07:40 CT; locked PREREG_D575_TWO_TERM; results/two_term_d575.txt) — the two-term SERAPIS breaks the D574 trade-off only in a narrow ε window, and the mass term IS a Chronos-type tilt
Literature (1 search): Ding et al. arXiv:2411.18603 uses H = (j − j(τ₀))²[…] with its Minkowski vacuum near ω and τ = i as a saddle; it quotes no quadratic vacuum mass. That is consistent with D574: squared j-differences give flat-bottomed vacua. No prior art was found for the plateau + ε·I₁ combination; no novelty is claimed.
Results (p = 2; all four ε values reported):
- **ε = 1e-4**
  - Quadratic vacuum (slope 2.00), m/H_inf = 0.037.
  - N* = 52: y* = 24.8, HOME-SAFE; n_s = 0.9726 (+1.4σ SPA, −0.1σ SPA+DESI); r = 4.0e-4.
  - N* = 55.6: y* = 25.7, just outside; n_s = 0.9751; r = 3.7e-4.
- **ε = 3e-4:** y* = 28–30 (outside); n_s = 0.992–0.996 (+7σ to +9σ). Fails.
- **ε = 1e-3 and 3e-3:** the linear rise destroys slow roll (no viable inflation).
Verdict by the lock: the trade-off is BROKEN at ε = 1e-4, N* = 52. It has a quadratic vacuum, is home-safe, and is within 3σ of both data sets.
Caveats:
1. The window is narrow: ε ≈ 1e-4 works, 3e-4 fails. ε is a post-hoc scan value, so this is tuning-sensitive, and the result is scored only on future data.
2. The vacuum is light (m ≈ 0.04 H_inf). Early oscillations with large amplitude still feel the octic part, so the stiff phase from D574 is shortened, not removed.
Physics link (the main finding): the term that gives τ = i its mass grows like y/2 at the cusp, so it automatically tilts the plateau upward and raises n_s. So **Chronos's tilt can come from the same source as the vacuum mass.** At ε = 1e-4 it lands n_s on the SPA+DESI centre (0.9726 vs 0.9728). Before this, δ was an unexplained post-hoc number (D565/D568).
Next: derive the ε ↔ δ map (ε·I₁ vs I^{2δ}), and check whether ε ~ 1e-4 has a natural size (e.g. a loop factor or e^{−2π·…}). Each needs its own lock.

## D576 — pp (07:45 CT; analytic map plus arithmetic, not locked, labelled as estimates) — the ε ↔ δ map, and why the ε window is narrow
Map (cusp forms: I ≈ y, I₁ ≈ y/2; canonical φ with y = e^{√2 φ}, α = 1/3):
- Chronos adds V₀·2δ ln I ≈ 2√2 δ·φ, a LINEAR ramp in φ. It is pure slope with no curvature.
- The two-term model adds V₀·ε I₁ ≈ (ε/2)·e^{√2 φ}, an EXPONENTIAL ramp. Its slope is (ε/√2)·y and its curvature V_φφ = ε·y.
- Matching the slopes at horizon exit gives ε = 4δ/y*. For HS-Chronos (δ = 0.0013, y* ≈ 28) that means ε ≈ 1.9e-4; for the D525 δ = 0.0023 it means ε ≈ 3e-4.
- Conversely, ε = 1e-4 at y* = 24.8 acts like δ_eff ≈ 6e-4.
Why ε = 1e-4 raises n_s as much as a δ twice as large:
- The exponential ramp also adds positive curvature, η ∋ ε y* ≈ 2.5e-3, which pushes n_s up.
- That same exponential growth is why the window is narrow: ε = 3e-4 already overshoots to n_s ≈ 0.99 (D575).
- So the two-term model is NOT a re-parametrisation of Chronos. It is a steeper, curvature-carrying tilt, closer to the rising loop term of fibre-type inflation (Cicoli et al., 0907.0665, as an analogy only).
Natural size of ε (estimate):
- The natural string source of a term linear in y is the threshold/species function −ln(2y|η|⁴) ≈ (π/3)y (D540). Writing ε·y/2 ≈ (b/16π²)(π/3)·y·(normalisation to V₀) gives b ≈ 24π·ε ≈ 0.0075.
- But D560–D562 require NO N = 2 threshold on the home plane. So the most natural source of ε is the one the home rules out. Holomorphic |E₆|² (I₁) itself has no known string derivation.
Verdict: ε is a cleaner way to write the tilt than I^{2δ} (it ties the tilt to the vacuum mass), but its size is unexplained: either it needs an N = 2 sector with tiny |b| ~ 1e-2, or a separate source. Status: OPEN, sharpened. Next: test whether a small-|b| N = 2 sector is compatible with the home bound (D560/D566 used |b| ≲ 2, and the bound weakens as |b| shrinks). That needs a lock.

## D577 — DEEP (Ddl, 07:50 CT; locked PREREG_D577_SPECIES_MASS + DEVIATIONS D575/D577; results/species_mass_d577_rerun.txt) — a string-motivated mass term for τ = i that leaves Kairos untouched
Literature (3 searches):
- Casas & Ibáñez, "Moduli self-fixing", arXiv:2507.05345 (new to our notes).
  - Their one-loop, gravitino-mass-driven term is δV ∝ g^{ττ̄}|∂Λ_sp/Λ_sp|². It is positive-definite with minima at the "desert points".
  - Derived and checked numerically: ∂_τ ln(2y|η|⁴) = (πi/6)Ĝ₂ (matches to 8 digits). So δV = y²|Ĝ₂|²/N², which is the 2407.12081 form.
  - Ĝ₂ has a simple zero at i, so this term is QUADRATIC there: slopes 2.000/1.998.
- Gravitational-threshold paper 1611.10323: the R² thresholds grow linearly in T₂ from N = 2 sectors (supports D576's identification of the linear-in-y source). Gives no potential.
Model: V = I²/(I² + 1) + κ·y²|Ĝ₂|²/N², with N = −6 ln(2y|η|⁴) + Ñ₀; p = 2.
Process note: the first run had an artifact in the "broken inflation" check (first step at eps = 1). DEVIATIONS were written first, then one rerun.
- All unaffected rows reproduced unchanged.
- D575's affected rows are corrected: ε = 1e-3 now gives n_s = 1.11–1.14 (fails anyway); ε = 3e-3 gives "N* not reached". The D575 verdict is unchanged.
Results (rerun; reference κ = 0, HS-Kairos: n_s = 0.9635/0.9658, r = 2.9/2.5e-4):
- κ = 1e-3: m/H = 0.005 (Ñ₀ = 25) and 0.001 (Ñ₀ = 100); |Δn_s| ≤ 1e-4; home-safe.
- κ = 1e-2: m/H = 0.016 and 0.004; |Δn_s| ≤ 4e-4; home-safe.
- κ = 0.1:
  - Ñ₀ = 25: m/H = 0.050, Δn_s = +3e-4, home-safe.
  - Ñ₀ = 100: Δn_s = +3.5e-3 and y* = 25.3 at N* = 55.6. FAILS the decoupling rule.
Verdict by the lock: mass and tilt ARE DECOUPLED for κ ≤ 1e-2 (both Ñ₀). A species-scale (one-loop, string-motivated) term gives the τ = i vacuum a quadratic mass while leaving the HS-Kairos predictions intact to < 0.0004 in n_s. The D559 Ñ₀ pathology is suppressed because this term is small.
Caveats:
- The masses are small (m ≈ 0.005–0.05 H_inf, i.e. ~1e10–1e11 GeV with H_inf ~ 4e12). Large-amplitude oscillations right after inflation still feel the octic part, so a short stiff phase remains (D574/D567a).
- κ ∝ m₃/₂²/(8π)² sets SUSY breaking during inflation; its size is not derived here.
- The HS-Kairos n_s is still −2.5σ to −3.4σ from SPA+DESI. The mass term does not change that.
Status:
- The τ = i vacuum now has two candidate mass sources: (a) ε·I₁, which tilts the plateau (n_s → 0.9726, D575); (b) the species term, which does not (D577).
- So "Kairos vs Chronos" is now a question about WHICH one-loop sector gives τ = i its mass.
- D567a stays: the bands remain conditional until the oscillation history (octic → quadratic crossover) is computed. That needs its own lock.

## D578 — DEEP (Ddl, 07:58 CT; locked PREREG_D578_OSC_NSTAR; results/osc_nstar_d578.txt) — the light vacuum mass gives LOW reheating and N* ≈ 48–51, outside the D567 window; the Chronos-like two-term model survives, the mass-completed Kairos does not
Near the vacuum: V ≈ c₈δ⁸ with c₈ = 269, plus the mass term. The octic part dominates for 6–8 decades in energy density after inflation ends (ρ_x/ρ_end = 1e-8 (K1), 2.5e-7 (K2), 2.4e-6 (C1)).
Masses: m = 2.2e10 (K1), 7e10 (K2), 1.9e11 GeV (C1). Gravitational-strength decay gives T_RH = 2e5 to 2e7 GeV, so there is a long matter phase after the stiff one.
N* (stiff bound to matter bound, c_Γ = 1–10):
- K1: 47.8–50.5. K2: 48.4–50.7. C1: 48.9–50.9.
- ALL are below the D567 window [52, 55.6]. The stiff phase adds about +2 e-folds; the long matter phase removes more.
- So D567a resolves AGAINST the window. The D567 bands assumed the wrong N* for every mass-completed version. They stay locked as written; this note records that their reheating premise fails.
Resulting predictions (post-hoc bands; scored only on future data):
- Kairos + species mass (K1/K2): n_s = 0.9604–0.9626, r = 3.0–3.4e-4, y* = 22.6–23.3 (home-safe). That is −1.9σ to −2.7σ vs SPA and −3.8σ to −4.6σ vs SPA+DESI. On today's data, mass-completed Kairos is in serious tension with the DESI-including combination.
- Two-term C1 (ε = 1e-4): n_s = 0.9701–0.9717, r = 4.1–4.4e-4, y* = 24.0–24.5 (home-safe; lower N* moves y* inward). That is +0.6σ to +1.1σ vs SPA and −1.0σ to −0.4σ vs SPA+DESI. Consistent with both.
New problem flagged: T_RH ≤ 2e7 GeV is far below thermal leptogenesis (M₁ ≳ 3e10 GeV, D440). Baryogenesis would need a non-thermal or low-scale mechanism (e.g. inflaton-decay leptogenesis or resonant leptogenesis). Open.
Status: the self-consistent home-safe SERAPIS is now the Chronos-like two-term model: plateau p = 2, with ε·I₁ giving τ = i its mass AND the tilt. N* ≈ 49–51, n_s ≈ 0.970–0.972, r ≈ 4.1–4.4e-4. Its remaining weak points are ε's size (D576) and baryogenesis.

## D579 — DEEP (DpL tick 1, 08:05 CT; locked PREREG_D579_NONTHERMAL_LEPTO; results/lepto_d579.txt) — non-thermal leptogenesis from inflaton decay rescues baryogenesis for the Chronos-like model only
Method: Ding et al. (arXiv:2411.18603, eq. 4.29), Y_B = (8/23)(3/4)(T_RH/m)·ε₁·2Br, with the Davidson–Ibarra bound ε₁ ≤ 3M₁m₃/(16πv²) and Br = 1. That paper is the in-family prior art: modular inflation with inflaton → N decays, needing m_φ ≳ 1e11 GeV.
Clean bound (derived; independent of m): T_RH ≥ 5.1e6 GeV (M₁ = m/3) or ≥ 3.4e6 GeV (M₁ = m/2, the kinematic edge).
Results (all 12 D578 rows):
- C1 (two-term, ε = 1e-4; m ≈ 1.9e11 GeV, T_RH = 5.6e6–1.8e7 GeV): PASSES in every row. Y_B,max = 0.96–4.7e-10, versus the 8.75e-11 needed. The c_Γ = 1 rows pass only by ~10% at M₁ = m/3.
- K2 (Kairos + species, κ = 1e-2): passes only at c_Γ = 10 AND M₁ = m/2 (the phase-space edge). Fails otherwise.
- K1 (κ = 1e-3): FAILS everywhere (Y_B ≤ 1.9e-11).
Caveats: Br = 1 and the M₁ choice are optimistic, and the T_RH convention carries a ~20% uncertainty. Resonant leptogenesis could lift the bound (not used).
Verdict: baryogenesis is possible for the Chronos-like two-term SERAPIS, near the edge if decays are gravitational-strength (c_Γ ~ 1), comfortably at c_Γ ~ 10. Kairos + species mass is disfavoured on a second, independent front (D578 n_s, plus baryogenesis).
Status: the surviving model is two-term SERAPIS (p = 2, ε ≈ 1e-4).
- n_s 0.970–0.972, r 4.1–4.4e-4, N* 49–51, T_RH 6e6–2e7 GeV, M₁ ≈ 6e10–9e10 GeV, non-thermal leptogenesis.
- Open: ε's size (D576), and a microscopic inflaton → N₁N₁ coupling (Br ≈ 1).

## D580 — DEEP (Ddl 07:43 CT; dedicated novelty audit of the two-term model, as the D555 rule requires; literature, no computation) — the rising-term tilt is Kallosh–Linde prior art; only the "mass at i = tilt" pairing remains unfound
Searches: 3 (one extended). Fetched: 2512.02969 (KL), 2507.15076, 2602.06027.
- **Kallosh & Linde, "Singular α-attractors", arXiv:2512.02969, §5.3**
  - Adds δ·ln^β(|j(τ)|² + j(i)²) to an SL(2,Z) α-attractor. At the cusp it grows ∝ e^{β√(2/3α)φ}, the same exponential-in-φ (linear-in-y for β = 1) scaling as our ε·I₁ (D576).
  - The deviation of n_s from 1 − 2/N is ∝ δ, and n_s can be raised to the ACT/DESI range with r ~ 1e-3.
  - → The TILT MECHANISM of the two-term model is prior art (consistent with D546, where Chronos ≈ KL lifted attractors).
- What differs:
  - KL's term is built from |j|², with its minimum at ρ (j = 0), and they say nothing about the vacuum mass.
  - Our ε·I₁ uses |j − 1728|¹, so the same term vanishes QUADRATICALLY at i and supplies the vacuum mass that the plateau lacks (D574/D575).
  - The resulting consistency chain (N* ≈ 49–51, T_RH 6e6–2e7 GeV, non-thermal leptogenesis; D578/D579) was not found anywhere.
- Other checks (no match): 2507.15076 (hilltop vs ACT), 2602.06027 (Witten–O'Raifeartaigh, n_s 0.9785), 2411.18603 (j-based, vacuum near ω), 2607.00528 (CW, vacuum at Im τ ~ 2).
Verdict: novelty is limited to "one modular term (∝ |j − 1728|) gives the τ = i vacuum its mass AND supplies the KL-type tilt, with a self-consistent reheating/leptogenesis history". Allowed wording: "not found in the checked literature (D580 audit)". Must credit: KL 2512.02969 for the tilt mechanism, and Ding et al. 2411.18603 for inflaton-decay leptogenesis in modular inflation.

## D581 — DEEP (Ddl 07:45 CT; locked PREREG_D581_EPS_WINDOW; results/eps_window_d581.txt) — the allowed ε window is narrow, ε ≈ 1.0–1.3e-4, and no reference "natural" value falls in it
Full chain per ε (D578 N* history, both reheating bounds, c_Γ = 1 and 10; D579 leptogenesis at M₁ = m/3):
- ε = 5e-5 and 7e-5: fail leptogenesis at c_Γ = 1 (Y_B ≤ 5–7e-11). n_s = 0.965–0.969 (−2.7σ to −1.4σ vs SPA+DESI).
- ε = 1.0e-4: all pass. n_s 0.9701–0.9717, r 4.1–4.4e-4, y* 24.0–24.5.
- ε = 1.3e-4: all pass. n_s 0.9729–0.9745 (+0.0σ to +0.6σ SPA+DESI; +1.5σ to +2.0σ SPA), r 4.6–4.8e-4, y* 24.4–24.9.
- ε = 1.6e-4: two rows leave home (y* = 25.3–25.4). ε = 2e-4: all rows leave home, n_s ≈ 0.98.
Verdict by the lock: ALLOWED = {1.0e-4, 1.3e-4} on this grid, width 1.30 (about a 30% tuning window). Combined post-hoc band: n_s = 0.970–0.975, r = 4.1–4.8e-4, N* = 49–51, m = 1.9–2.3e11 GeV, T_RH = 6e6–2.4e7 GeV.
Naturalness (reference values fixed before computing): e^{−3π} = q(i)^{3/2} = 8.1e-5, (1/16π²)² = 4.0e-5 and 1/(64π³) = 5.0e-4 are all OUTSIDE the window. The nearest, e^{−3π}, sits about 20% below its lower edge, where leptogenesis fails at c_Γ = 1. Numerology aside, ε is unexplained.
Reading:
- The window is fixed from three sides: below by leptogenesis (and n_s), above by home-safety. The surviving model is therefore sharp: r ≈ 4–5e-4 is a firm target.
- But it needs a ~30%-tuned small parameter with no known origin.
- Future test: CMB-S4/LiteBIRD-class σ(r) ≈ 1e-4 would detect r ≈ 4.5e-4 at about 4σ. Excluding r > 2e-4 would kill two-term SERAPIS.

## D582 — DEEP (Ddl 07:46 CT; literature + arithmetic estimates, not locked) — the axion partner Re τ is massless during inflation (as KL warn), but in two-term SERAPIS it leaves no observable isocurvature
Literature:
- Carrasco, Kallosh, Linde, Roest, "Axion stabilization in modular cosmology", arXiv:2503.14904 (9 Jun 2025; new to our notes).
  - In unstabilized SL(2,Z) attractors the θ = Re τ potential is "almost exactly flat" during inflation, which they say produces large axion isocurvature perturbations.
  - Their fix adds A‖j − j̄‖² inside the log, giving valleys at θ = k/2.
- KL 2408.05203 §7: V_θ and V_θθ are double-exponentially suppressed at large φ.
Our case (estimates; arithmetic in code):
- The x-dependence of |j − 1728| at y* = 24.5 is ~1488·e^{−2πy} = 2e-64. θ is massless during inflation, as warned.
- Geometric destabilisation (α = 1/3, field-space curvature R = −8): εR ≈ −2.3e-4. Its growth over ~50 e-folds is ≤ e^{0.004}, which is negligible.
- Fluctuation: δx_rms ≈ √2·y*·H/(2π) = 1.2e-5 (H/M_P = 2.2e-6). It stays frozen to the end of inflation; even at y_end = 2.8, the x-dependence is only 3e-5.
- Conversion to curvature: V is symmetric under x → −x (the CP map τ → −τ̄), so δN starts at second order in δx. That gives δN ~ δx² ~ 1e-10, against ζ ≈ 5e-5, so it is negligible.
- After inflation:
  - The Hessian at τ = i is isotropic (D574: the Re and Im directions have equal mass), so θ joins the vacuum oscillation.
  - The energy fraction in the axial mode is ~(δx/Δy)² ≈ 4e-11. Even with different CP-odd decay channels, the modulated-reheating isocurvature is ~1e-11, far below Planck's limits.
  - No separate axion relic survives, since it decays with the inflaton.
Verdict: KL's isocurvature warning applies when the axion survives as a separate component or the potential lacks the CP symmetry. For two-term SERAPIS, which has a CP-symmetric path and an isotropic massive vacuum at i, the isocurvature is ≲ 1e-10 (estimate). No stabilisation term is needed.
Caveat: estimates, not a two-field numerical run. A locked two-field δN computation would confirm this.

## D583 — DEEP (DpL tick 2, 07:48 CT; literature + arithmetic estimates, not locked) — the gravitino problem: generic modulus decay overproduces gravitinos; the residual symmetry at τ = i is the natural cure
Literature: Endo, Hamaguchi, Takahashi / Kawasaki et al., hep-ph/0611166 (eqs. 2–7): Γ(φ → 2ψ₃/₂) ≃ |G_eff|² m_φ⁵/(288π m₃/₂² M_P²), with G_eff = √3·g_{φ̄zz}·m₃/₂/m_φ, and Y₃/₂ ≃ 4.5e5|G_eff|²(m₃/₂/TeV)⁻²(m_φ/1e10 GeV)⁴(T_R/1e6 GeV)⁻¹. Bound for m₃/₂ ~ 1 TeV, B_h ~ 1: |G_eff| ≲ 1e-11·(m_φ/1e10)⁻². Also KKMY 0804.3745 for thermal production; its numerical T_R bounds were not reached in the fetched text.
Two-term SERAPIS (m_φ ≈ 2e11 GeV, T_R ≈ 1e7 GeV; arithmetic in code):
- Required: |G_eff| ≲ 2.5e-14.
- A generic modulus (g_{φ̄zz} ~ O(1), vev ~ M_P) has G_eff ~ m₃/₂/m_φ = 5e-9 (TeV gravitino), giving Y₃/₂ ~ 2e-7. That is many orders above any BBN bound, so overproduction is FATAL unless the coupling is suppressed by about 2e5.
Cure (reasoning, consistent with EHT's "symmetry" route):
- At τ = i the residual S-symmetry acts on the fluctuation as δτ → −δτ (D574A).
- If the SUSY-breaking field z (the nilpotent sector) is S-neutral, the linear mixing g_{φ̄zz} ∝ ⟨∂_φ K⟩ is FORBIDDEN, so φ → 2ψ₃/₂ starts only at higher order.
- This is the same residual Z₄^R/Z₈^R that already protects the proton (D528–D533, D551). One symmetry would then do two jobs.
- Caveat: z's modular weight must be chosen neutral, and the nilpotent-sector couplings (D545) must respect it. Not yet checked.
Thermal production at T_R ~ 1e7 GeV: for an unstable TeV-scale gravitino with large B_h, the commonly quoted BBN limits are around 1e6–1e7 GeV (to verify against KKMY tables). It is safe for m₃/₂ ≳ O(10) TeV or for a light stable gravitino.
Verdict: OPEN, with a concrete condition. Two-term SERAPIS needs (i) the S-parity of the τ = i vacuum to forbid inflaton–SUSY-breaking mixing, and (ii) m₃/₂ outside the TeV unstable window. Condition (i) ties back to the proton-parity result: a consistency requirement, not yet a derivation.

## D584 — DEEP (Ddl 07:49 CT; literature + reasoning + arithmetic estimates, not locked) — CORRECTION to D583's cure: the S-parity does not help, because the inflaton carries an F-term; the viable escape is m₃/₂ > m_φ/2 ≈ 1e11 GeV
Checked the KL supergravity embedding (2408.05203, eqs. 9.1–9.2):
- G = −3α ln(T + T̄) + G_XX̄ XX̄ + ln|W₀ + F_X X|², with X² = 0 and Λ = F_X² − 3W₀².
- The paper gives no F_τ, gravitino or goldstino analysis. Its full-supergravity SL(2,Z) invariance is asserted, not shown (W₀ is a constant without modular weight).
Reasoning:
1. With X nilpotent, EHT's sgoldstino coupling g_{φ̄zz}φ̄XX vanishes identically (X² = 0). And the linear δτ·XX̄ mixing ∝ ∂_τV(i) = 0 is killed by D574A's stationarity. So D583's S-parity argument is moot for those terms.
2. But W₀ ≠ 0 (needed for m₃/₂ and Λ ≈ 0, which forces F_X ≈ √3 W₀) gives F_τ = K_τ W₀ ≠ 0 at τ = i.
   - For α = 1/3, the inflaton's share of SUSY breaking is about 3α|W₀|²/(F_X² + 3α|W₀|²) ≈ 1/4. So the inflaton is partly the goldstino.
   - The symmetry does not forbid this, so the moduli-induced gravitino problem applies with an O(1) F-term.
3. Estimate: Br(φ → 2ψ₃/₂) ~ 0.01–0.1 gives Y₃/₂ ~ Br·(3/2)T_R/m_φ ≈ 7e-7 to 7e-6 (m_φ = 2.1e11, T_R = 1e7). That is fatal for any TeV-scale or light stable gravitino.
Escape: kinematic closure, m₃/₂ > m_φ/2 ≈ 1.0–1.15e11 GeV (high-scale SUSY, below H_inf ≈ 4e12).
- Then the inflaton cannot decay to gravitino pairs.
- Thermal production at T_R ~ 1e7 GeV is negligible.
- A gravitino this heavy decays long before BBN.
- Bonus: m_φ ≈ 2m₃/₂ is a typical modulus/gravitino relation, so this may be natural rather than tuned (not shown).
- Constraint on the model: the SUSY breaking scale is fixed near F ~ m₃/₂M_P ~ (1e14.7 GeV)².
Verdict: D583's "S-parity cure" is WITHDRAWN. The gravitino problem is solved only if m₃/₂ ≳ 1e11 GeV. This is a new, testable-in-principle requirement: high-scale SUSY, with no TeV superpartners from this sector. Still to check: the proton-parity results with m₃/₂ this large (D542 assumed a non-zero m₃/₂ but not this scale).

## D585 — DEEP (Ddp 07:51 CT; literature + arithmetic, not locked) — with m₃/₂ ≈ 1e11 GeV: proton parity survives, and the Higgs mass needs sequestered soft masses, which the α = 1/3 no-scale structure naturally gives
1. **Proton (re-check of D542 at the D584 scale).**
   - Dim-5 operators reappear with M_eff ~ M_P²/m₃/₂ = 5–6e25 GeV, against the TeV-SUSY bound of 1e24. That passes by a factor ~50.
   - The margin is larger in practice: with sfermions far above a TeV, the dim-5 dressing is suppressed further.
   - Dim-4 operators are still forbidden by the residual Z₂. Dim-6 Kähler operators pick up an extra factor m₃/₂/M_P ~ 4e-8.
   - D542's "safe for m₃/₂ ≲ 1e5 GeV" extends to 1e11 GeV. PASS.
2. **Higgs mass** (Bagnaschi, Giudice et al., arXiv:1407.4081).
   - High-scale SUSY with all sparticles at M_S needs M_S ≲ 2e10 GeV (degenerate) or ~1e11 (spread ×3). A top mass 1σ lower gives ~3e11.
   - Split SUSY needs M_S ≲ 1e8.
   - If soft masses ≈ m₃/₂ ≈ 1e11 (plain gravity mediation), we are AT THE EDGE.
3. **The way out is built in.**
   - K = −ln(2 Im τ) is the α = 1/3, i.e. 3α = 1, no-scale form. In no-scale/sequestered set-ups the tree-level soft scalar masses cancel.
   - Soft terms then come at loop order, ~m₃/₂/16π² ≈ 6–7e8 GeV (anomaly-mediation-like; estimate). That is well inside the 2e10 bound.
   - Caveat: sequestering of the visible sector is assumed, not derived. The nilpotent-metric choice (G_XX̄ with the 3|W₀|²(1 − α) term) must be checked to keep the cancellation.
Verdict: CONSISTENT, conditionally. The two-term SERAPIS chain now reads: m_φ ≈ 2e11 GeV, m₃/₂ ≈ 1.0–1.15e11 GeV (closing gravitino decay), soft masses ~1e9 GeV (no-scale sequestering), proton safe, Higgs mass OK.
- Prediction-level consequence: no superpartners at the LHC or any planned collider from this sector.
- Dark matter is not from this sector (consistent with the Twist's separate DM, unchanged).

## D586 — DEEP (Ddl 07:52 CT; literature + reasoning + arithmetic, not locked) — the Kallosh–Linde problem: H_inf/m₃/₂ ≈ 37, so KKLT-type stabilisation of the other moduli would fail; a SUSY racetrack (as in D178/D193) evades it
Issue: in KKLT-type stabilisation the barrier protecting the volume/dilaton is ~m₃/₂, which requires H ≲ m₃/₂ (Kallosh & Linde 2004, hep-th/0411011; the standard lore searched today, e.g. 1510.00376). Two-term SERAPIS has H_inf ≈ 4.1e12 GeV against m₃/₂ ≈ 1.1e11 GeV (D584/D585), so H/m₃/₂ ≈ 37. The KL problem applies to the dilaton Y and to any other T-moduli.
Evasion (already in our toolkit):
- Stabilise Y (and the companion T's) with a KL racetrack at a SUSY Minkowski point, W_Y = W_Y′ = 0 (D178, D193). The heavy-modulus mass is then set by the racetrack, not by m₃/₂.
- Requirement: m_Y ≳ 10 H_inf ≈ 4e13 GeV.
- The nilpotent-sector W₀ ~ m₃/₂M_P² then perturbs the racetrack minimum by ~m₃/₂/m_Y ≈ 3e-3 (small).
- Residual displacement of Y during inflation ~(H/m_Y)² ≈ 1e-2 in units of the curvature scale. It tracks adiabatically, so the misalignment energy is small (estimate).
Price and open item:
- The D193 window was narrow (A ≈ 5e-7 – 2e-6, ×4); it needs re-evaluating for SERAPIS's H_inf (lower than the Twist's 1.5e13, so the window should widen; not computed).
- With m_Y ≈ 4e13 > 2m₃/₂, the decay Y → 2ψ₃/₂ is open. With F_Y ≈ 0 at the SUSY racetrack point, G_eff ~ m₃/₂/m_Y ~ 3e-3 gives Br ~ O(1e-2) (estimate). Y's abundance is suppressed by its small displacement. Whether the resulting gravitino yield is safe is NOT computed. Flagged.
Verdict: the KL problem is real but evadable by a known mechanism already used in this project. Open: the racetrack window at SERAPIS's H, and dilaton-induced gravitinos (both need locks).

## D587 — DEEP (DpL tick 3, 07:58 CT; locked PREREG_D587_TWO_FIELD_DN; results/two_field_dn_d587.txt) — two-field δN CONFIRMS D582 (axion harmless), but the self-check FAILED: exact e-fold counting differs from our slow-roll counting by 1.7 e-folds
Two-field integration: hyperbolic metric, exact Christoffels, mpmath gradients (dps 150) to avoid cancellation; ε = 1e-4, starting from y* = 24.29.
- The axion stays frozen: x_end/x₀ = 0.99949 for every offset.
- ΔN(x₀) = 3.6e-11, 3.6e-9, 3.6e-7, 3.2e-6 for x₀ = 1e-4 … 3e-2. This is cleanly quadratic, N_xx ≈ 7.2e-3.
- δN_iso = ½N_xx δx² = 5e-13 (δx = 1.2e-5). Ratio to ζ: 1.1e-8, below the 1e-3 threshold. **D582 CONFIRMED.**
Self-check FAILED (as locked: |N(0) − 50| ≤ 0.5):
- The exact two-field background from the single-field y*(N = 50) gives N = 51.70. So the slow-roll ∫V/V′dφ count used in D564–D581 undercounts by about 1.7 e-folds at this y*.
- Implication: in our scripts, the y* labelled "N*" actually corresponds to N_exact ≈ N* + 1.7. Rough attractor scaling, Δn_s ≈ −2ΔN/N², means our quoted n_s may be HIGH by ~0.001–0.0014 relative to a correct N* assignment, and y* slightly too large (which helps home-safety).
- This is NOT corrected here (no rerun to chase results). A locked follow-up must:
  1. confirm the offset with an exact single-field integration;
  2. recompute n_s, r and y* from the exact background (ideally with the Mukhanov–Sasaki or second-order slow-roll n_s);
  3. propagate to D575/D577/D578/D581 and the D567 bands.
- Caution flag on every n_s quoted since D564: systematic ≈ −0.001 pending verification.

## D588 — CORRECTION/CHECK (Ddl 07:54 CT; locked PREREG_D588_EXACT_NS + DEVIATIONS D1 [crash, no results seen] and D2 [atol bug; results seen and declared invalid]; results/exact_ns_d588.txt) — exact background + Mukhanov–Sasaki: the D587 alarm is mostly a cancellation; the true n_s shift is only −0.0002 to −0.0004
Validation (locked): HS-Kairos MS n_s = 0.9611/0.9626 against the attractor 1 − 2/N* = 0.9592/0.9608. The difference is 0.0019, inside the 0.002 limit (PASS, narrowly).
Exact results (N* counted exactly from the end):
- HS-Kairos: N* = 49: y* = 22.52, n_s = 0.9611, r = 3.28e-4. N* = 51: y* = 22.93, n_s = 0.9626, r = 3.04e-4. (−1.9σ to −2.4σ SPA; −3.8σ to −4.3σ SPA+DESI.)
- Two-term ε = 1.0e-4: n_s = 0.9698–0.9714, r = 4.2–4.4e-4, y* = 23.6–24.1.
- Two-term ε = 1.3e-4: n_s = 0.9725–0.9742, r = 4.6–4.9e-4, y* = 24.0–24.5. (+1.4σ to +1.9σ SPA; −0.1σ to +0.5σ SPA+DESI.)
Compared with the old slow-roll scripts at the same nominal N*:
- Δn_s = −0.0002 to −0.0004; r is +2–3%; y* is 0.36–0.45 lower.
- The y* shift does equal the D587 offset (dN/dy ≈ 4.9, so Δy = 0.36 ↔ ΔN ≈ 1.75). But in n_s it is largely cancelled by the first-order slow-roll error in the n_s formula itself.
Verdict: D587's flag of a "systematic ≈ −0.001" is REVISED to −0.0002 to −0.0004 in n_s. All conclusions since D564 stand. Every y* is ~0.4 smaller (slightly MORE home-safe).
Reference numbers for two-term SERAPIS going forward: n_s = 0.970–0.974, r = 4.2–4.9e-4 (ε = 1.0–1.3e-4, N* = 49–51). Post-hoc; scored only on future data.

## D589 — DEEP (Ddl 07:57 CT; locked PREREG_D589_N_COUPLING; results/n_coupling_d589.txt) — a natural inflaton → N₁N₁ coupling is ~4× too weak for hierarchical non-thermal leptogenesis; resonant leptogenesis (or λ ≳ 6) is required
Coupling: M(φ) = M₁f(τ), with λ = d ln M/dφ. For a modular form like E₄: d ln E₄/dτ|_i = (πi/3)E₂(i) = i (E₂(i) = 3/π, verified to 1e-12), so |λ| = √2.
Width: Γ = (M₁λ/M_P)²·m/16π·(1 − 4M₁²/m²)^{3/2}, i.e. c_eff = ½(M₁/m)²(1 − 4M₁²/m²)^{3/2}λ² ≈ 0.023λ².
Results (C1, m = 1.9e11 GeV, Br = 1, Davidson–Ibarra bound):
- λ = 1 or √2: c_eff = 0.02–0.05, T_RH = 0.9–1.2e6 GeV, Y_B ≤ 1.5–2.1e-11. FAIL, by about 4–6×.
- λ = 3: Y_B ≤ 4.5e-11. FAIL.
- λ needed: 5.9 (M₁ = m/3) to 6.2 (M₁ = 0.316m).
Consequences:
1. D579's PASS assumed a decay width with c_Γ ≥ 1. A modular-form coupling of natural size gives c_eff ≈ 0.05, so the D579 PASS does not survive a microscopic coupling.
2. Ways out:
   - (a) Resonant leptogenesis: quasi-degenerate N₁, N₂ evade the Davidson–Ibarra bound; Ding et al. 2411.18603 use exactly this. It needs a mass splitting ~Γ_N (a tuning, but a standard one).
   - (b) A steeper modular dependence of M (|λ| ≳ 6, e.g. higher weight or several forms). Not natural from E₄.
   - (c) A different baryogenesis mechanism (e.g. Affleck–Dine).
3. The lower T_RH (≈1e6 GeV) also lengthens the matter phase: N* drops by about ¼·(1/3)·ln(5–6) ≈ 0.15, a negligible n_s change (< 1e-4; estimate).
4. Open (flagged in the lock): the linear δτ·NN coupling must be allowed by the residual S-symmetry at i, which constrains N's modular weight. SM couplings with k_Y ≡ 0 (mod 4) (D551) are S-even, so their linear inflaton couplings are S-forbidden. That FAVOURS Br(NN) ≈ 1 if the N channel is allowed.
Verdict: two-term SERAPIS needs resonant leptogenesis (or an un-natural λ). The baryogenesis status is downgraded from "PASS" (D579) to "PASS only with resonant enhancement".

## D589a — CORRECTION to D589 (Ddl 07:59 CT; identity check run in code) — the "natural λ = √2" used the holomorphic form alone; the PHYSICAL coupling of the inflaton to any diagonal mass vanishes at τ = i
- The physical mass of a field pair with Yukawa Y of weight k includes the Kähler normalisation, M_phys ∝ (2y)^{k/2}|Y|, which is modular INVARIANT.
- By D574A, any invariant is stationary at i, so d M_phys/dφ = 0 there.
- Checked: |∇(y²|E₄|)| at i = 1e-10 (zero), while the holomorphic-only |∇|E₄||/|E₄| = 2.000 (the D589 input).
- Analytic: Y′(i) = DY(i) + (ik/2)Y(i). The Serre derivative DY has weight k + 2 ≡ 2 (mod 4), so it vanishes at i. The remaining (ik/2)Y is cancelled exactly by the Kähler factor.
- So the diagonal decay φ → N₁N₁ has NO two-body width at leading order. D589's numbers (λ = 1–√2 failing by 4–6×) are void as stated. The true diagonal width is zero, which is worse for the N₁N₁ channel.

## D590 — DEEP (Ddl 07:59 CT; literature + reasoning + identity check, not locked) — at τ = i the inflaton can only decay through OFF-DIAGONAL (flavour-changing) couplings; that points naturally to quasi-degenerate N pairs and resonant leptogenesis
Reasoning:
- The eigenvalues of M_N†M_N (and of the SM mass matrices) are modular invariants, so all are stationary at i. Linear inflaton couplings to diagonal mass eigenstates vanish, for N AND for SM fermions.
- What survives at linear order are off-diagonal couplings δτ·N_iN_j (i ≠ j): the eigenvectors rotate with τ even where the eigenvalues are stationary.
- These require N_i, N_j that are related by the flavour structure: the same residual-symmetry multiplet, or states that the residual S-symmetry (Z₂ for A₄ at i, per 2604.04585's introduction) relates. Such states are naturally quasi-degenerate at the fixed point, split only by small deviations from i or by symmetry breaking.
- So the decay channel the symmetry permits (φ → N₁N₂) and the condition for resonant enhancement (M₁ ≈ M₂) come from the same structure. That turns D589's "needs resonant leptogenesis" from an added tuning into a plausible consequence. NOT shown: it needs an explicit Γ_N-flavour model.
- The SM gets the same structural suppression: its diagonal masses are also stationary. With D551's S-even SM couplings, the SM's linear decay channels are suppressed too, which supports Br(N-sector) ~ O(1).
Literature: modular-flavour work at fixed points (e.g. 2604.04585, 2026) studies leptogenesis near other fixed points with hierarchical N and gives no τ = i results. A dedicated search found nothing that treats inflaton decay at τ = i (search-only claim).
Status: baryogenesis for two-term SERAPIS = resonant leptogenesis via off-diagonal φ → N₁N₂ in a near-degenerate pair. This is the leading candidate, but it needs an explicit flavour model (Γ₂/Γ₃ weights at τ = i) to compute Γ(φ → N₁N₂), the splitting, and Y_B. That needs a lock.

## D591 — DEEP (Ddl 08:00 CT; arithmetic estimates reusing the D193 racetrack, not locked) — the dilaton racetrack window is WIDE at SERAPIS's scale, but heavy-dilaton decays create a serious LSP over-abundance problem
1. **Racetrack window** (SU(8) × SU(9), Re Y₀ = 2, D193 conditions W = W′ = 0). With K = −ln(Y + Ȳ) − ln(2y), m_Y ∝ A(2y)^{−1/2}, so it varies only ×5 between y* ≈ 24.5 and the vacuum. That is far milder than the Twist's x^{−3/2}.
   - Requiring m_Y(y*) ≥ 10H_inf (H = 2.2e-6 M_P) and m_Y(vacuum) ≤ M_s (1e17 GeV) gives A ∈ [1.4e-3, 0.51], a window of ×377. Compare the D193 Twist window of ×4.
   - m_Y = 5e13 – 3e14 GeV at the bottom of the window, up to ~5e15 GeV at its geometric mean. **KL problem (D586): solved comfortably.**
2. **New problem: the moduli-induced LSP problem.**
   - The heavy dilaton decays to sparticle pairs (m_soft ~ 6e8 GeV < m_Y) and to gravitinos, Br ~ O(1) in total. Every sparticle cascades to the LSP.
   - The residual Z₂ (matter/R-parity, D542) makes the LSP STABLE. An LSP at ~6e8 GeV cannot annihilate efficiently.
   - The Y decay products are diluted by the later inflaton decay (T_RH ~ 1e6 GeV), giving Y_LSP ≈ (3/4)(T_RH/m_Y)·f_Y ≈ 1.9e-8·f_Y, where f_Y = ρ_Y/ρ_φ when Y decays.
   - Overclosure needs Y_LSP·m_LSP ≲ 4e-10 GeV, i.e. **f_Y ≲ 4e-11**.
   - Worse, during the octic (stiff, w = 3/5) phase ρ_φ ∝ a^{−4.8} redshifts faster than an oscillating Y (a^{−3}). So any Y displacement GROWS relative to φ, by about 180× over the stiff phase (estimate).
3. **Ways out** (none shown yet):
   - (a) strong adiabatic suppression of Y oscillations for m_Y/H_inf ≫ 1 (top of the A window, m_Y/H ~ 1e3; Linde / Nakayama–Takahashi–Yanagida-type); this needs computing;
   - (b) a tiny R-parity violation so the LSP decays, which must stay compatible with the D528 proton parity (dim-4 B-violation still forbidden); possible in principle with L-violating couplings only;
   - (c) a lighter, annihilating LSP, which would require breaking the no-scale soft-mass structure (D585).
Verdict: the KL problem is solved, but a moduli-induced LSP problem appears and needs f_Y ≲ 4e-11. It is currently the most severe open problem for two-term SERAPIS. Next: a locked adiabatic-suppression computation for Y.

## D592 — DEEP (Ddl 08:01 CT; locked PREREG_D592_ADIABATIC_Y; results/adiabatic_y_d592.txt) — adiabatic suppression works: a dilaton with m_Y ≳ 300 H_end evades the D591 LSP problem, inside the racetrack window
Toy: the exact SERAPIS two-term background through the end of inflation and 1.5 e-folds of oscillation; a dilaton with a Hubble-induced shift d = c·V/m², c = 1; start in tracking 3 e-folds before the end.
Free-oscillation energy fraction f_Y at 1.5 e-folds after the end:
- m/H_end = 10: 6.0e-2
- m/H_end = 30: 3.3e-5
- m/H_end = 100: 2.2e-9
This is a steep power law (local slopes −6.8 and −8.0), not a clean exponential. The forced (tracking) part, 2.5e-8 at 100, follows V and decays with it; it is not a relic.
Requirement (D591, with the ~180× stiff-phase growth): f_Y ≲ 2e-13. Extrapolating with the last slope gives m/H_end ≳ 320 (extrapolation, flagged).
- In physical units: H_end ≈ 3.2e12 GeV, so m_Y(y_end) ≳ 1.0e15 GeV and m_Y(vacuum) ≳ 1.7e15 GeV.
- That is the racetrack amplitude A ≳ 8.7e-3. The window shrinks from [1.4e-3, 0.51] (D591) to [8.7e-3, 0.51], still ×58 wide.
Caveats:
- c = 1 is a toy normalisation (f ∝ c², so c = 3 needs ~1.3× larger m by the power law).
- The extrapolation runs ~3× beyond the computed range.
- The stiff-phase growth factor is an estimate.
- Y decay timing is not followed.
Verdict: the moduli-induced LSP problem (D591) is AVOIDABLE by adiabatic suppression with a heavy dilaton (m_Y ≳ 2e15 GeV). That is a mild constraint inside the stabilisation window. It is the leading resolution; it needs a locked follow-up with full Y decay and stiff-phase evolution.
Chain status for two-term SERAPIS: n_s 0.970–0.974, r 4.2–4.9e-4, m₃/₂ ≈ 1.1e11, m_soft ~ 1e9, m_Y ≳ 2e15 GeV, baryogenesis via resonant off-diagonal decays (D590, model needed).

## D593 — DpL tick 5 (08:03 CT; 1 search + arithmetic) — NULL: no natural origin for ε ≈ 1.0–1.3e-4 found; loop ends
- Candidates (1) and (2) of this tick were already done manually as D590–D592.
- (3) ε origin. The search returned only 2512.02969 (already in D580); KL also leave their δ unexplained.
- One idea checked by arithmetic: a gravitino-mass-driven one-loop term, δV ~ m₃/₂²M_P²/(64π²) relative to V₀ = 3H²M_P², gives ε ~ (m₃/₂/H)²/(192π²) ≈ 4e-7 at m₃/₂/H ≈ 0.027. To reach 1e-4 it would need m₃/₂ ≈ 0.45H.
- But that loop term has the species (Ĝ₂) form, which gives mass without tilt (D577). It cannot supply ε·I₁. Rejected.
Verdict: NULL (no new literature, no new locked computation). The DpL loop ends here. Open items for future locks:
  (i) an explicit Γ_N flavour model at τ = i for off-diagonal φ → N₁N₂ and resonant leptogenesis (D590);
  (ii) the full Y-decay + stiff-phase follow-up of D592;
  (iii) the origin of ε.

## D594 — DEEP (Ddl 08:04 CT; locked PREREG_D594_ADIABATIC_Y_EXT; results/adiabatic_y_d594.txt) — D592 extrapolation checked directly: the suppression is even steeper; m_Y ≳ 160 H_end suffices
Same toy and code (only R changed):
- f_Y(200) = 2.4e-15 and f_Y(320) = 3.2e-17, both above the 1e-18 numerical floor. The forced parts are 6e-9 and 2e-9, and they decay with V.
- Local slopes: 100→200: −19.8; 200→320: −9.2. The suppression steepens past R ~ 100 (approaching exponential), so D592's power-law extrapolation was conservative.
- The requirement f_Y ≤ 2e-13 is met already at R ≈ 160 (log interpolation between 100 and 200). **CONFIRMED directly at R = 200 and 320.**
Updated bound: m_Y(y_end) ≳ 5e14 GeV, m_Y(vacuum) ≳ 8.5e14 GeV, racetrack A ≳ 4.3e-3. The window widens back to ×119 (versus ×58 in D592).
Caveats unchanged: c = 1 toy normalisation (f ∝ c²); the stiff-phase growth factor (~180×) is an estimate; Y decay is not followed.

## D595 — DEEP (Ddl 08:05 CT; locked PREREG_D595_STIFF_GROWTH; results/stiff_growth_d595.txt) — the stiff-phase growth is ×8.6, not ×180; the dilaton needs only m_Y ≳ 140 H_end
Computed from the exact background:
- Effective w = 0.556 over [N_end + 0.5, +1.5] and 0.537 over [+1.5, +3]. This is close to the octic 0.6, which confirms the stiff phase (D574/D578).
- ρ(N_end + 1.5)/ρ_end = 1.15e-3. Reaching the octic → quadratic crossover (ρ_x/ρ_end = 2.4e-6) takes another 1.34 e-folds, over which a free Y gains G = 8.6 relative to φ.
- D591's ~180× counted the whole stiff phase from the end of inflation, but the Y oscillation only becomes free after ~1.5 e-folds. CORRECTED.
Requirement: f_Y(N_end + 1.5) ≤ 4.6e-12, giving R = m_Y/H_end ≳ 137 (interpolated from D592/D594).
Final bound: m_Y(y_end) ≳ 4.4e14 GeV, m_Y(vacuum) ≳ 7e14 GeV, racetrack A ≳ 3.6e-3, window ≈ ×140.
The LSP problem (D591) is resolved within the toy, with comfortable margin.

## D596 — DEEP (Ddl 08:06 CT; reasoning + arithmetic, not locked) — the toy coefficient c is fixed by supergravity: c = √2, a negligible change
- With K ⊃ −ln(Y + Ȳ), the inflaton potential carries the overall factor e^{K_Y} = 1/(2 Re Y). The canonical dilaton is σ, with dY/dσ = √2·Y₀ (K_YȲ = 1/(4Y₀²)).
- So ∂_σV_inf = −√2·V_inf. The Hubble-induced shift is d = √2·V/m², i.e. c = √2 (D592 assumed c = 1).
- Since f_Y ∝ c² = 2 and f ∝ R^{−20} near R ~ 140 (D594 slope), the requirement moves R by a factor 2^{1/20} = 1.035: R ≳ 142. Negligible.
- Hubble-induced MASS terms (c_H H²σ²) would add to m_Y during inflation; they help adiabaticity. They are not included.
Final: m_Y(vacuum) ≳ 7e14 GeV; racetrack A ≳ 3.7e-3; window ≈ ×140. The c caveat on D592/D594/D595 is CLOSED.

## D597 — DEEP (Ddl 08:07 CT; locked PREREG_D597_S3_FLAVOUR; results/s3_flavour_d597.txt) — minimal S₃ flavour toy at τ = i: off-diagonal decay + resonance falls short by ~7×; NOT VIABLE as is
Checks: the Γ₂ weight-2 doublet expansions are verified at τ = 4i (y₁ = 1/8 + 3q exactly, y₂ = √3q^{1/2}).
- At i: Y = (0.1306, 0.0754), s = 0.1508, Y′ = (0.0353i, 0.2404i).
- Off-diagonal (UᵀA(Y′)U)₁₂ = −0.1906i, so κ = 1.26. The off-diagonal channel EXISTS, confirming D590's structural claim.
The tension D590 did not resolve:
- The off-diagonal coupling scales with the splitting, λ₁₂ = √2κ(ΔM/2M), so T_RH ∝ ΔM. The resonant asymmetry falls as ε ∝ 1/ΔM above resonance.
- Below resonance (ΔM ≲ Γ_N ≈ 4e-6 M), T_RH is only 0.01–4 GeV: too cold for sphalerons and too little asymmetry.
- Above it, Y_B reaches a PLATEAU independent of ΔM: Y_B ≈ 1.25e-11 for all ΔM/M ≳ 1e-4 (T_RH from 110 GeV up to 1e5 GeV).
- Required: 8.75e-11. Short by ×7. No scan point passes.
- Scaling: Y_B,plateau ∝ κ·m_ν (via Γ_N). Passing needs κ ≈ 9, the same "needs ~5–7× stronger coupling" wall as D589.
Verdict (by the lock): NOT VIABLE in the minimal S₃ toy.
Remaining routes (none computed):
- (a) several N pairs or larger Γ_N structures (three generations add at most ~×2–3);
- (b) higher-weight doublets with larger κ at i;
- (c) a non-leptogenesis mechanism (Affleck–Dine along a flat direction, natural with high-scale SUSY);
- (d) a larger inflaton mass. Y_B,plateau grows with m, but m is fixed by ε (D581).
Status: baryogenesis is the WEAKEST link of two-term SERAPIS. Leptogenesis from inflaton decay at τ = i is suppressed by symmetry (diagonal couplings vanish, off-diagonal ones ∝ ΔM) and falls ~×7 short in the minimal realisation.

## D598 — DEEP (Ddl 08:08 CT; locked PREREG_D598_HIGHER_WEIGHT; results/higher_weight_d598.txt) — higher-weight doublets raise κ, but none passes; the best (k = 8) is ×1.75 short
κ at τ = i for the Γ₂ doublets (built by 2⊗2 → 2 products):
- k = 2: κ = 1.26 (D597).
- k = 4: κ = 2.53, Y_B,plateau = 2.5e-11.
- k = 6: κ = 1.26, Y_B,plateau = 1.25e-11.
- k = 8 (Y⁽⁴⁾⊗Y⁽⁴⁾): κ = 5.05, Y_B,plateau = 5.0e-11.
All FAIL against 8.75e-11 (needs κ ≥ 8.85). The pattern (κ doubles along the Y⁽⁴⁾-power chain) suggests a k = 16 doublet might pass, but that was NOT in this lock. Picking ever-higher weights until something passes would be chasing a result, so it is not done here.
Caveats:
- At weight ≥ 6, Γ₂ has more than one doublet; κ depends on which combination is used. Only the product chain was tested.
- Three generations or several pairs could add a factor ~2–3. Combined with k = 8 (×1.75 short), leptogenesis becomes MARGINALLY possible. That combination is not computed.
Verdict: route (b) narrows the gap from ×7 to ×1.75 but does not close it. Baryogenesis stays the weakest link: possible only in a fairly specific flavour set-up (high-weight N doublet plus several pairs), or via Affleck–Dine.

## D599 — DEEP (Ddl 08:09 CT; literature + scaling arithmetic, not locked) — Affleck–Dine leptogenesis along LH_u can supply the asymmetry at SERAPIS's low T_R, at the price of an essentially massless lightest neutrino
Literature: Fujii, Hamaguchi, Yanagida, hep-ph/0109154 (the U(1)_{B−L} D-term-stopping variant; read in part, the final formula is beyond the excerpt):
- n_B/s ∝ T_R, independent of m₃/₂, and "almost determined by" the lightest neutrino mass. Anchor: m_ν1 ~ 1e-4 eV for T_R ~ 1e10 GeV.
- In the low-T_R (gauge-mediation) case, T_R ≲ 1e5 needs m_ν1 ≲ 1e-10 eV.
Scaling (n_B ∝ T_R/m_ν1, from the anchor):
- T_R = 1e7: m_ν1 ~ 1e-7 eV. T_R = 1e6: 1e-8 eV. T_R = 1e5: 1e-9 eV. T_R = 1e3: 1e-11 eV.
- SERAPIS's T_R is now set by the symmetry-suppressed inflaton decay (D589a/D597, roughly 1e2–1e7 GeV), so the LIGHTEST NEUTRINO MUST BE ~MASSLESS (≲ 1e-7 eV).
Why it fits:
- High-scale SUSY (m_soft ~ 1e9, D585) still has flat directions.
- The low T_R that hurts thermal and inflaton-decay leptogenesis is what this mechanism wants.
- The lepton asymmetry is converted by sphalerons, which needs T_R ≳ 150 GeV. That is satisfied in most of the range.
Testable consequence: the lightest neutrino mass ≈ 0, so Σm_ν takes its minimum (≈ 0.059 eV normal ordering or ≈ 0.10 eV inverted). 0νββ is then fixed by the oscillation parameters alone. DESI/Euclid-era Σm_ν measurements test this directly.
Caveats:
- The FHY set-up uses a U(1)_{B−L} D-term to stop the flat direction. Our model has not specified the B − L sector; that needs adding, or a different stopping mechanism (higher-dimensional W term), which changes the coefficient.
- Thermal effects and our stiff (w ≈ 0.55) post-inflation phase (FHY assume matter domination) can change the scaling.
- Not locked; an order-of-magnitude scaling only.
Verdict: the most promising baryogenesis route for two-term SERAPIS is Affleck–Dine leptogenesis, which predicts m_ν1 ≲ 1e-7 eV (estimate). It replaces the ×1.75–7 shortfalls of the inflaton-decay routes (D589a–D598). Needs: a locked AD computation adapted to the stiff phase and SERAPIS's T_R.

## D600 — DEEP (Ddl 08:13 CT; arithmetic + reasoning, not locked) — timing check: the Affleck–Dine field starts oscillating AFTER the stiff phase, so the standard matter-dominated AD scaling (D599) applies
- The crossover from octic (w ≈ 0.55, D595) to quadratic (matter-like) inflaton oscillation happens at H_x = H_end·(ρ_x/ρ_end)^{1/2} = 3.2e12 × (2.4e-6)^{1/2} ≈ 5.0e9 GeV (C1).
- The AD flat direction starts oscillating at H_osc ≈ m_soft ≈ 6–10e8 GeV (D585 no-scale soft masses). That gives H_osc/H_x ≈ 0.13–0.2, so AD dynamics begin in the inflaton-MATTER era. This is exactly FHY's assumption, so n_L/ρ_φ is conserved until reheating and n_B/s ∝ T_R holds. D599's main caveat about the stiff phase is RESOLVED.
- The stiff phase only affects the Hubble-induced evolution BEFORE H_osc, which sets the initial phase and amplitude. It enters through an O(1) factor, not the scaling (estimate).
Remaining caveats:
- (i) The flat direction must be lifted by a B − L D-term (FHY) or by the neutrino-mass operator (LH_u)²/M with M = v²/m_ν1 (Murayama–Yanagida type). Both give n_B ∝ T_R/m_ν1, with coefficients differing by ~O(10).
- (ii) Thermal effects can trigger early oscillation. They are weaker here because φ_osc is large and the plasma is diluted (T_R ≪ m_soft).
- (iii) Q-ball formation (gravity-mediated, m_soft ~ 1e9): Q-balls would decay well before BBN at these masses (estimate).
Status: baryogenesis is now via AD leptogenesis along LH_u. It predicts m_ν1 ≲ 1e-7 eV for T_R ≲ 1e7 GeV, i.e. Σm_ν at its minimum. Needs: fixing T_R from the actual inflaton decay channels (D597 showed T_R ∝ the N splitting; channels to the hidden/racetrack sector are not yet counted).

## D601 — DEEP (Ddl 08:13 CT; reasoning + arithmetic, not locked) — the inflaton at τ = i is nearly "sterile": every linear decay to an equal-mass pair vanishes; T_R is set by flavour splittings, ~1e3–1e5 GeV
Reasoning, building on D574A/D589a:
1. Physical masses (fermion, scalar, gauge-boson thresholds) are modular invariants, so they are stationary at i. The linear coupling δτ·m²(τ)χχ vanishes after canonical normalisation.
2. Kinetic couplings from the matter metric (2y)^{−k} survive the field redefinition only as current couplings (∂φ)·(χ*∂χ − c.c.). For χχ* final states, the on-shell matrix element is ∝ (m₁² − m₂²) = 0.
3. Gravitational and trace couplings (φ/M_P)·T^μ_μ ∝ m², and the conformal-anomaly φFF ∝ ∂(threshold), reduce to derivatives of invariants: zero at i.
4. The CP-odd δx·FF̃ coupling (∂ Im f ≠ 0) exists, but the oscillating mode is radial; the axial amplitude is ~1e-5 (D582). Negligible.
5. What survives: OFF-DIAGONAL couplings between states of the same multiplet with DIFFERENT masses, ∝ (m_i² − m_j²)/M_P (D597's λ₁₂ ∝ ΔM is one case).
T_R estimates (arithmetic):
- Heavy-N doublet with ΔM/M ~ 0.1 (generic, non-degenerate; D597): T_R ~ 1e5 GeV.
- Sfermion multiplets (m_soft ~ 1e9, O(1) splittings, ~20 states): g ~ √2 m_soft²/M_P, so T_R ~ 2–4e2 GeV.
- SM fermions: negligible (masses ≪ m_φ, coupling ∝ m²).
So T_R ≈ 1e3–1e5 GeV, dominated by the heaviest split multiplet (the heavy neutrinos).
Consequences:
- Above sphaleron decoupling (~150 GeV): OK for AD leptogenesis. With D599's scaling, m_ν1 ~ 1e-11 – 1e-9 eV: a sharp "massless lightest neutrino" prediction.
- N*: T_R lower than D578's c_Γ = 1–10 (T_R 6e6–2e7) means a longer matter phase. ΔN* ≈ (1/12)ln(T_R,old⁴/T_R,new⁴)·… ≈ −(1/3)ln(60–2e4) ≈ −1.4 to −3.3 e-folds. Then n_s drops by ≈ 2ΔN/N² ≈ 0.001–0.003, to about 0.968–0.972, and y* moves inward. The direction stays the same; the D581 window must be re-run with this T_R (needs a lock).
- Gravitino (D584, closed kinematically) and LSP (D592–D596) conclusions are unchanged.
Verdict: the "sterile inflaton at a fixed point" structure is the key physics of two-term SERAPIS reheating. It gives low T_R, which favours AD leptogenesis with a massless lightest neutrino, and it shifts the n_s band down by ~0.001–0.003 (estimate).
D601a (typo correction, same tick): the sfermion-channel arithmetic printed T_R ≈ 350–710 GeV, not "2–4e2". The range conclusion (T_R ≈ 1e3–1e5 GeV, N-dominated) is unchanged.

## D602 — DEEP (Ddl 08:15 CT; locked PREREG_D602_EPS_WINDOW_LOWTR; results/eps_window_lowtr_d602.txt) — at the D601 reheating temperature the ε window shifts UP to 1.3–1.6e-4; the prediction band is n_s ≈ 0.970–0.975, r ≈ 4.8–5.7e-4
With T_R = 1e3–1e5 GeV: N* = 46.1–49.2 (versus 49–51 in D581). n_s includes the D588 offset (−0.0003); y* includes the D588 shift (−0.4).
- ε = 1.0e-4: n_s 0.9672–0.9700. The T_R = 1e3, w = 0 row is −2.1σ vs SPA+DESI, so it fails the 2σ rule. Excluded.
- ε = 1.3e-4: n_s 0.9698–0.9727, r 4.8–5.2e-4, y* 23.2–24.1. All pass.
- ε = 1.6e-4: n_s 0.9725–0.9754, r 5.2–5.7e-4, y* 23.6–24.5. All pass (+0.4σ to +1.0σ SPA+DESI; up to +2.3σ SPA).
- ε = 2.0e-4: one row leaves home (y* = 25.0). ε = 2.5e-4: out.
ALLOWED: {1.3e-4, 1.6e-4}. The window moved up and stays about 25–30% wide.
Updated post-hoc band for two-term SERAPIS (scored only on future data): n_s = 0.970–0.975, r = 4.8–5.7e-4, N* = 46–49, T_R = 1e3–1e5 GeV.
The r prediction strengthens slightly: r ≈ 5e-4 is a ~5σ target for σ(r) = 1e-4 experiments.

## D603 — DEEP (Ddl 08:16 CT; literature, no computation) — the LH_u Affleck–Dine "massless lightest neutrino" prediction is robust across stopping mechanisms
- Fujii, Hamaguchi, Yanagida, hep-ph/0102187 (flat direction lifted by the neutrino-mass operator itself, W = (m_ν1/2⟨H_u⟩²)(LH_u)², with thermal effects included):
  - The asymmetry is almost independent of T_R over 1e5–1e12 GeV, because the thermal-log term triggers early oscillation. It is set by m_ν1 ≈ 1e-10 – 3e-9 eV for n_B/s ≈ (0.4–1)e-10.
  - The abstract and introduction quote slightly different ranges (0.3–1 vs 0.1–3 × 1e-9 eV); read in part only.
  - Their set-up has TeV-scale m₃/₂ and m_φ.
- FHY hep-ph/0109154 (B − L D-term stopping): n_B ∝ T_R/m_ν1, with m_ν1 ~ 1e-4 eV at T_R = 1e10 (D599).
Application to SERAPIS (m_soft ~ 1e9 GeV, T_R ~ 1e3–1e5 GeV; D601/D602):
- The heavy AD mass makes oscillation start at H ~ m_soft, before the thermal-log term can matter (estimate). This is closer to the T_R-proportional regime. Both papers point to m_ν1 ~ 1e-11 – 1e-8 eV.
- Robust qualitative prediction, whichever stopping mechanism applies: **the lightest neutrino is essentially massless (≲ 1e-8 eV)**. So Σm_ν sits at its oscillation minimum (≈ 0.059 eV NO / ≈ 0.10 eV IO), and 0νββ (if IO) is fixed by the mixing angles.
Caveat: no dedicated computation for heavy-SUSY AD at low T_R; the coefficients are uncertain by ~×10, so m_ν1 is pinned only to within about two orders of magnitude.

## D604 — DEEP (Ddl 08:17 CT; literature, no computation) — the "massless lightest neutrino" prediction lands right at the newest DESI bound
DESI DR2 Results IV (arXiv:2607.27410, §VI.D.2; Lyα AP + full shape with BAO + CMB):
- ΛCDM: Σm_ν < 0.0592 eV (95%). Without Lyα full shape: < 0.0565 eV.
- w₀w_aCDM: < 0.166 eV (0.128 eV with DES-Dovekie SNe).
- The ΛCDM limit is "nearly identical" to the normal-ordering oscillation minimum, Σm_ν > 0.059 eV. Inverted ordering is excluded at > 3σ in ΛCDM. The paper notes that much of the posterior volume is inconsistent with both orderings, and that NO is favoured only modestly (Δχ² = −5.2).
Two-term SERAPIS plus AD leptogenesis (D599–D603) predicts m_ν1 ≲ 1e-8 eV, i.e. Σm_ν = 0.0588–0.059 eV (NO). That is EXACTLY at the minimum DESI allows in ΛCDM, so the prediction is maximally consistent with today's tightest bound. Inverted ordering would give Σ ≈ 0.10 eV, disfavoured by DESI in ΛCDM, so the model prefers NO.
Testability:
- Any future Σm_ν detection clearly above ~0.065 eV (with NO) would mean m_ν1 ≳ 0.01 eV. That is incompatible with AD-LH_u leptogenesis at our T_R and would push baryogenesis back to the failing inflaton-decay routes (D589–D598).
- A cosmological preference below 0.059 eV is a problem for oscillation physics in ΛCDM generally, not for this model specifically.
Note: SERAPIS's late universe has a separately tuned Λ (D538). If dark energy is dynamical, the bound relaxes and the test weakens.

## D605 — FORWARD PREDICTIONS (Ddl 08:18 CT; locked PREREG_D605_FORWARD_TWOTERM) — the two-term SERAPIS package is frozen for future data
Bands:
- n_s 0.970–0.975; r 4.8–5.7e-4; n_t = −r/8.
- Σm_ν ≈ 0.059–0.060 eV, normal ordering.
- No superpartners below ~1e8 GeV; m₃/₂ ≈ 1e11 GeV.
- Negligible isocurvature; f_NL ≈ 0.01.
Scoring rules are in the lock. ε is post-hoc, declared.
Main tests and their order:
- Simons Observatory / CMB-S4 / LiteBIRD: r at ~5σ if σ(r) ≈ 1e-4.
- DESI DR3 / Euclid: Σm_ν.
- JUNO / DUNE / Hyper-K: mass ordering.
This supersedes D567 as the CURRENT forward package. D567 stays locked as a historical record (D567a: its reheating premise failed).

## D606 — DEEP (Ddl 08:19 CT; arithmetic + reasoning, not locked) — origin of ε: loops of our own heavy states are far too small; a two-sector Coleman–Weinberg ratio gives ε ~ 1e-4 for a mass ratio ≈ 0.1 (an idea, not derived)
- (a) A Coleman–Weinberg term from the heavy-N sector, δV ~ m_soft²M_N²/16π², relative to V₀ = 3H²M_P²: ε ~ 1e-25. Hopeless.
- (b) Abe et al. (2607.00528, D572) generate a whole modular plateau from one loop of vector-like quarks with M_Q·Y(τ) masses, V_CW ∝ M_Q⁴-type.
  - If the plateau comes from such a sector (Y_a), and a second sector couples through E₆-type forms (giving the |j − 1728|¹-like I₁), then ε ~ (λ₂/λ₁)²(M₂/M₁)⁴.
  - ε ≈ 1.3–1.6e-4 needs M₂/M₁ ≈ 0.11 for equal couplings: a mild hierarchy, (0.1)⁴ = 1e-4.
  - Not shown:
    1. whether a CW loop with E₆-weighted masses actually produces the I₁ = ln(1 + |j − 1728|/1728) shape;
    2. whether it is compatible with the plateau sector's τ = i vacuum and SUSY structure.
- (c) Gravitino-loop (species) term: wrong shape (D593/D577).
Verdict: ε is still unexplained. The most plausible origin is a ratio of two loop sectors with a ~10× mass hierarchy, which would make ε ~ 1e-4 natural-looking. That would need a dedicated construction, which is a substantial project, not a single Dp.

## D607 — DEEP (Ddl 08:21 CT; reasoning, not locked) — D606's two-sector CW idea FAILS at the level of shape: a CW loop cannot produce I₁'s linear-in-y growth
- I₁ = (1/4π)ln(1 + |j − 1728|/1728) grows like y/2 at the cusp because it is the LOG of a holomorphic weight-0 function (j − 1728 ∝ E₆²/Δ).
- A CW loop gives V ∝ Σ m⁴(τ)ln(m²/μ²), with physical m² a modular invariant built from forms and Kähler factors:
  - (i) weight-0 ratios such as |E₆|²/|E₄|³ ∝ |j − 1728|/|j| → const at the cusp: no growth, no tilt;
  - (ii) y^k|E_k|²-type invariants grow ∝ y^k, i.e. like e^{k√2φ}: far too steep (a power ≥ 4 in m⁴);
  - (iii) Abe-type exponentially decaying forms (q^t) fall at the cusp: a plateau approached from below, the opposite sign of tilt.
  None reproduces a term ∝ ln|j − 1728| ∝ y.
- A log of a holomorphic function arises naturally in gauge kinetic functions or thresholds, f ⊃ b·ln(E₆²/η²⁴), entering V through gaugino-condensate or threshold corrections. That is the N = 2-threshold-type origin D576 identified, which the home conditions (D560–D562) forbid on the SERAPIS plane, and the E₆ zero at i would make any condensate ∝ e^{−f/b} singular.
Verdict: D606's route (b) is WITHDRAWN as an origin of the ε·I₁ shape (only its magnitude estimate worked). ε·I₁ still has no consistent microscopic source. The tension is sharp: the shape needs a threshold-like log; the home forbids N = 2 thresholds. This is now the main theoretical weakness of two-term SERAPIS, alongside the unexplained size of ε.

## D608 — DEEP (Ddl 08:21 CT; reasoning + an UNLOCKED diagnostic, not a scored test; disclosed) — CORRECTION to D607's "forbidden", and a new obstruction: the natural threshold-type tilt term has a SADDLE at τ = i
1. Correction to D607:
   - D560–D562 excluded N = 2 planes only because SERAPIS then needed y* = 112–158. The home bound itself (D566: Im T ≲ k·α⁻¹ ≈ 29) IS the universal N = 2 threshold bound.
   - The home-safe two-term model has y* ≈ 23–25 < 29 (D602), so an N = 2 plane is ALLOWED for it. D553's |b| ≲ 2 bound also relaxes (U₂,max ≥ 35 even at b = 10).
   - So a threshold-type log term is not forbidden. D607's "forbidden on the home plane" is WITHDRAWN.
2. New obstruction (diagnostic; computed before writing a lock, so disclosed as unlocked and NOT used for any score):
   - The standard threshold function L = −ln(2y|η|⁴) has L(i) = 0.3615 with Hessian (L_xx, L_yy) = (−0.298, +1.298): a SADDLE at i.
   - At ρ: L(ρ) = 0.3404 with (0.667, 0.667), a MINIMUM.
   - Adding ε_th·L to the plateau (which is octic and flat at quadratic order at i) makes the axial direction TACHYONIC at τ = i, so the vacuum would slide toward ρ.
   - Our E₆-based I₁ is S-invariant with an isotropic positive Hessian at i (D574 C′); the DKL-type threshold is not.
3. Consequence: the tilt-plus-mass term must be "j − 1728-like" (zero at i, isotropic) for τ = i to stay the vacuum. The natural string threshold is "η-like" and prefers ρ.
   - A natural route is threshold-type (allowed, gives the right linear growth) but puts the vacuum at ρ: the Kallosh–Linde choice (D569 found Eisenstein plateaus also prefer ρ).
   - SERAPIS's τ = i is a consistent but NON-natural choice that needs the |j − 1728| structure, which has no known string source.
Verdict: the core tension, sharpened. String-natural ingredients point to ρ; τ = i needs an extra, unexplained |j − 1728|-type ingredient. Open option (needs a lock): a "SERAPIS-ρ" variant with the vacuum at the hexagonal torus, using the DKL threshold for both mass and tilt. It might be natural and string-sourced; check its n_s, r and home-safety.

## D609 — DEEP (Ddl 08:22 CT; locked PREREG_D609_SERAPIS_RHO + DEVIATIONS D1 [crash; no inflation results seen]; results/serapis_rho_d609.txt) — SERAPIS-ρ: the vacuum works (isotropic, at ρ), but on the locked ε grid it is NOT VIABLE; the DKL term is about twice as steep as I₁
Vacuum checks PASS: V(ρ) = 0; Hessian isotropic (0.667ε in both directions); V(i) ≈ 3.0e-3 > 0, so i is not the vacuum.
Inflation along Re τ = 1/2 (D588 offsets applied):
- ε = 1e-4:
  - N* = 47: y* = 24.3 (home-safe), n_s = 0.9775 (+1.7σ SPA+DESI, +3.0σ SPA), r = 6.3e-4.
  - N* = 50 and 53: y* = 25.3–26.2 (OUT), n_s 0.980–0.983.
- ε = 3e-4: n_s ≈ 1.02–1.03, y* 31–37. Fails.
- ε = 1e-3: no viable inflation.
Verdict by the lock: NOT VIABLE (no ε passes for all N*).
Reason: at the cusp L ≈ (π/3)y ≈ 1.05y, about TWICE the slope of I₁ ≈ y/2, so for the same ε it tilts twice as hard. The locked grid started at 1e-4, already too large.
Post-hoc observation (stated AFTER seeing results; not a verdict): by this scaling, ε_ρ ≈ ε_i/2 ≈ 6–8e-5 should reproduce the two-term SERAPIS numbers. Testing that needs a NEW lock declared as post-hoc.
Physics note: the vacuum mass is light (m/H ≈ 0.017 at ε = 1e-4), and the plateau near ρ is very flat (j has a triple zero, so the plateau term ∝ |δ|¹²). Reheating would again be a sterile, splitting-dominated history (D601 logic applies at ρ too).

## D610 — DEEP (Ddl 08:24 CT; locked PREREG_D610_SERAPIS_RHO_LOWEPS, DECLARED POST-HOC; results/serapis_rho_d610.txt) — SERAPIS-ρ is VIABLE at ε ≈ 4–6e-5 (post-hoc-tuned)
Results (D588 offsets applied):
- ε = 4e-5: n_s = 0.9664–0.9713 (−2.4σ to −0.6σ SPA+DESI), r = 3.7–4.4e-4, y* = 22.9–24.3. All home-safe. Passes the 2σ rule (worst row −2.4σ ⇒ |Δ| = 0.0064 > 0.0054: FAILS at N* = 47).
- ε = 6e-5: n_s = 0.9701–0.9752 (−1.0σ to +0.9σ), r = 4.2–4.9e-4, y* = 23.4–24.9. **ALL PASS.**
- ε = 8e-5: N* = 53 has y* = 25.5 (OUT). Fails.
Verdict by the lock: VIABLE at ε = 6e-5 (post-hoc-tuned; scored only on future data; not citable as an a-priori success).
Why it matters: SERAPIS-ρ uses only string-motivated ingredients.
- The KL j-plateau and the DKL/species threshold function L = −ln(2y|η|⁴) supply the vacuum mass AND the tilt in one term. The vacuum is at ρ, where L has an isotropic minimum (D608).
- The threshold is allowed on an N = 2 plane, since y* ≤ 25 < 29 (D608 correction).
- It reproduces essentially the SAME observables as two-term SERAPIS: n_s ≈ 0.970–0.975, r ≈ 4–5e-4.
- The price: the vacuum moves from the square torus (i) to the hexagonal torus (ρ). The "τ = i" identity of SERAPIS would be dropped in favour of naturalness.
Open for SERAPIS-ρ:
- (i) the residual symmetry at ρ (Z₃ rather than Z₂/Z₄): the proton-parity and selection-rule analysis (D528–D551) must be redone mod 6;
- (ii) reheating (sterile-inflaton logic applies, D601), gravitino/LSP/dilaton chains as for two-term (D584–D596);
- (iii) a dedicated novelty audit. KL already put vacua at ρ (2408.05203), and Casas–Ibáñez use L; the combination plateau(j) + ε·L may exist.
Decision is Danny's: keep SERAPIS at τ = i (consistent, ε·I₁ unexplained) or move to SERAPIS-ρ (string-natural ingredients, vacuum at ρ). Both give the same D605-type forward numbers.
D610a (wording fix, same tick): the ε = 4e-5 line should read "FAILS the 2σ rule at N* = 47 (−2.4σ)". It is not allowed. The verdict (only ε = 6e-5 passes) is unchanged.

## D611 — DEEP (Ddl 08:25 CT; dedicated novelty audit for SERAPIS-ρ, literature only) — the combination is not found; every ingredient is prior art
Searches: 2 (one extended). Fetched: 2503.21030 and 2605.04415 (Kallosh & Linde, "New exponential and polynomial ξ-attractors", 2026: reaches n_s ≈ 0.973 by lowering the polynomial power, not by a modular rising term). Listing-level checks: 2411.08467, 2407.12081, 2507.03610, 2411.18603, 2504.01622.
Ingredients and credits:
- L_j = (1/4π)ln(|j|²/1728² + …) plateaus with the vacuum at ρ: Kallosh–Linde 2408.05203 (D544).
- L_η = −ln(2y|η|⁴) as a modular plateau or species function: Casas–Ibáñez 2407.12081, Aoki–Otsuka 2411.08467; also used by KL as an alternative plateau function (D544).
- A small rising term to tilt n_s: KL singular attractors 2512.02969 §5.3 (j-based).
Not found in the checked literature: plateau(L_j) + ε·(L_η − L_η(ρ)) with the vacuum at ρ, where the SAME threshold term supplies the vacuum mass and the tilt and keeps y* ≤ 25 (inside the N = 2 home bound).
Allowed wording: "a combination not found in the checked literature (D611 audit), built from known ingredients (credit KL, CI, Aoki–Otsuka)". This is the same status as two-term SERAPIS (D580): novelty lies only in the combination and its consistency chain.

## D612 — RIGHT (Ddl 08:26 CT; locked PREREG_D612_VACUUM_RHO_SELECTION; results/vacuum_rho_selection_d612.txt) — PASS: the proton parity is compatible with a ρ vacuum
Checks: |E₄(ρ)| = 1.5e-15 and |E₄²(ρ)| = 2e-30 (zero); |E₆(ρ)| = 2.88 and |E₆²(ρ)| = 8.30 (non-zero). This confirms the mod-6 rule.
Results:
- Z₄^R: 8/8 anomaly-passing assignments admit lifts with all five required couplings non-zero at ρ.
- Z₈^R: 16/16.
- Example: n = (0, 1, 1, 0, 1, 1, 1), no lift, all k_Y = 0 (constant couplings). That is the same assignment that works at τ = i (D551).
Caveat: the comparison with τ = i (4/8, 8/16 in D551) is not like-for-like. Here the lifts were {0, 2, 4} (needed for mod 6); D551 used {0, 2}. The constant-coupling solution works at both vacua.
Status: SERAPIS-ρ open item (i) from D610 is cleared at the selection-rule level. The anomaly check (D529) and the m₃/₂ argument (D542/D585) are vacuum-independent and carry over.

## D613 — DEEP (Ddl 08:27 CT; locked PREREG_D613_RHO_NSTAR; results/rho_nstar_d613.txt) — SERAPIS-ρ at ε = 6e-5 stays VIABLE with its own post-inflation history
Near ρ: the plateau term is ∝ δ¹² (fitted exponent 12.008; c = 3.1e3), plus the ε·L mass term (m̂² = 6.0e-5). The crossover is at ρ_x/ρ_end = 1.3e-6.
The stiff phase is stiffer than at i: w = 5/7 = 0.714, versus 3/5 for the octic case.
N* = 46.1–49.5 (T_R = 1e3–1e5 GeV, both w bounds).
Results: n_s = 0.9691–0.9723 (−1.4σ to −0.2σ SPA+DESI; +0.2σ to +1.3σ SPA), r = 4.6–5.1e-4, y* = 23.1–24.0. All rows pass.
Verdict: VIABLE (post-hoc ε, as in D610).
Comparison with two-term SERAPIS at i (D602, ε = 1.3–1.6e-4): the same observable band (n_s ≈ 0.969–0.975, r ≈ 4.6–5.7e-4).
So current and near-future data CANNOT distinguish the i and ρ vacua through n_s and r; the vacuum location shows up only in reheating details and the flavour/selection structure.
Status of SERAPIS-ρ: vacuum, inflation, home bound, proton parity (D612) and N* history all pass. String-natural ingredients; novelty only in the combination (D611).
Remaining, as for two-term: the gravitino/dilaton/LSP chain (D584–D596; vacuum-independent in form, re-check the numbers), and baryogenesis (AD route, D599–D604; vacuum-independent).

## D614 — DEEP (Ddl 08:28 CT; arithmetic re-check of D584–D596 for SERAPIS-ρ; estimates, not locked) — the SUSY/dilaton/LSP chain carries over to ρ with shifted numbers
(H from r = 4.6–5.1e-4: H ≈ 5.2–5.5e12 GeV; m_vac/H ≈ 0.0134, D610/D613.)
- Inflaton mass m_φ ≈ 7.0–7.4e10 GeV (versus 1.9e11 at i).
- Gravitino closure (D584): m₃/₂ > m_φ/2 ≈ 3.5–3.7e10 GeV. No-scale soft masses ~m₃/₂/16π² ≈ 2.3e8 GeV (D585). The Higgs-mass bound (≲ 2e10) is satisfied with more margin than at i. Proton dim-5: M_eff ~ M_P²/m₃/₂ ≈ 1.6e26 GeV, safe.
- Kallosh–Linde problem (D586): H/m₃/₂ ≈ 150 (versus 37 at i). It still needs the SUSY racetrack with m_Y ≫ H.
- LSP via the dilaton (D591–D596):
  - The stiff phase is stiffer here (w = 5/7, ρ_x/ρ_end = 1.3e-6), so the growth from N_end + 1.5 to the crossover is G ≈ 11 (versus 8.6 at i).
  - Requirement: f_Y(N_end + 1.5) ≲ 3.5e-12. By the D592/D594 power law this is R = m_Y/H_end ≳ 140–150, i.e. m_Y ≳ 1e15 GeV. It fits in the racetrack window (×100+).
- Baryogenesis: AD along LH_u (D599–D604) is vacuum-independent. T_R ≈ 1e3–1e5 GeV under the D601 sterile logic, which carries over because physical masses are stationary at ρ too (ρ is a fixed point of ST).
- So the same Σm_ν ≈ 0.059 eV (NO) prediction holds.
Verdict: SERAPIS-ρ passes the same consistency chain as two-term SERAPIS, with a lighter inflaton (~7e10 GeV), a lighter gravitino (≳ 3.5e10) and lighter soft masses (~2e8). Estimates; the AD and dilaton toys were not re-run at ρ.

## D615 — FORWARD PREDICTIONS (Ddl 08:28 CT; locked PREREG_D615_FORWARD_RHO) — SERAPIS-ρ frozen alongside D605
Bands: n_s 0.969–0.972; r 4.6–5.1e-4; Σm_ν ≈ 0.059 eV (NO); no low-scale SUSY; negligible isocurvature.
These overlap D605 (two-term, τ = i: n_s 0.970–0.975, r 4.8–5.7e-4). Together they form the current SERAPIS forward package. The one weak discriminator: n_s ≳ 0.974 favours the τ = i version.

## D616 — DEEP (Ddl 08:29 CT; reasoning + arithmetic, not locked) — for SERAPIS-ρ, ε may simply be (m₃/₂/H_inf)²: a threshold-dependent uplift ties the tilt to the SUSY-breaking scale
Idea: in the KL nilpotent form, V = (F_X² − 3W₀²) + V_plateau, with F_X² ≈ 3W₀² ≈ 3m₃/₂²M_P² (Λ ≈ 0).
- If the uplift term carries the threshold dependence, F_X² → F_X²e^{ξ′(L − L(ρ))} (e.g. a brane/hidden-sector tension depending on the N = 2 threshold), then δV ≈ 3m₃/₂²M_P²·ξ′(L − L(ρ)). That is exactly the ε·(L − L(ρ)) term, with ε = ξ′(m₃/₂/H)².
- A correction on the −3|W|² side instead has the WRONG sign (it would make ρ a maximum). So the identification needs the L-dependence on the F-term side.
Consequences (arithmetic):
- From D610/D613, m_φ/H = κ√ε with κ = 1.73.
- Gravitino closure (m₃/₂ ≥ m_φ/2, D584) becomes ξ′ ≤ (2/κ)² = 1.34, INDEPENDENT of ε. The O(1) coefficient expected from a threshold sits right where closure needs it.
- ε = 6e-5 then means m₃/₂/H ≈ 7–11e-3 for ξ′ = 0.5–1.3, consistent with D614 (H/m₃/₂ ≈ 150).
Reading: ε is no longer an arbitrary 1e-4. It is the squared ratio of the SUSY-breaking scale to the inflation scale, with an O(1) coefficient, and the gravitino-safety condition becomes an O(1) statement about ξ′.
NOT derived:
1. why F_X depends on L as e^{ξ′L};
2. why m₃/₂/H ≈ 0.01 (it moves the question from ε to the SUSY scale);
3. whether the same works at τ = i: no, the DKL L has a saddle at i (D608).
So this is an argument for SERAPIS-ρ only.

## D617 — DEEP (Ddl 08:31 CT; reasoning, not locked) — can modular-invariant gaugino condensation supply D616's e^{ξ′L} uplift? It gives ξ′ = 1 naturally, but the full SUGRA potential cancels the linear term unless the F-term and W₀ carry DIFFERENT modular dependence
1. With K = −ln(2y) (α = 1/3), modular invariance needs W of weight −1. A hidden condensate gives W ∝ Ω(S)·η(τ)⁻² (the FILQ structure at α = 1/3; SERAPIS-1's original η⁻², D530; allowed on an N = 2 plane since y* < 29, D608).
   Then e^K|W|² ∝ (2y|η|⁴)⁻¹ = e^{L} exactly. So a SUSY-breaking scale set by such a condensate scales as e^{ξ′L} with **ξ′ = 1**, inside D616's closure bound ξ′ ≤ 1.34.
2. But if BOTH F_X and W₀ come from the same condensate (W = η⁻²(W₀ + F_X X)), then:
   - V ⊃ e^{L}(F_X² − 3W₀²) + (terms ∝ |D_τW|² ∝ |Ĝ₂|²);
   - tuning Λ ≈ 0 at the vacuum (F_X² = 3W₀²) cancels the linear-in-e^{L} term everywhere;
   - what is left is the species-type |Ĝ₂|² piece. That is D577's shape (mass, no tilt), not the tilt.
3. The tilt survives only if F_X and W₀ have different modular dependence, e.g. W₀ from a modular-neutral sector (racetrack/flux, D586) and F_X from the τ-dependent condensate:
   - V ⊃ 3W₀²(e^{L − L(ρ)} − 1) ≈ 3W₀²(L − L(ρ)), with the right sign;
   - ε = (m₃/₂/H)²·ξ′, with ξ′ = 1.
   - This is D616's identification with ξ′ fixed to 1. It requires the gravitino mass to come from a DIFFERENT sector than the uplift. That is plausible, since the dilaton racetrack already sits at W_Y = 0 and m₃/₂ is set by the nilpotent-sector W₀, but it is not shown here.
Verdict: suggestive, not derived. The natural α = 1/3 condensate gives exactly ξ′ = 1 (satisfying the gravitino closure bound with ~15% margin, since m₃/₂/m_φ = 1/(κ√ξ′)·2 … ≥ 0.58 ⇒ OK). It works only if the uplift's modular dependence differs from W₀'s. A full SUGRA computation of V for this two-sector set-up needs a lock.
D617a (clarity fix): with ξ′ = 1, m₃/₂/H = √ε and m_φ/H = 1.73√ε, so m₃/₂/m_φ = 1/1.73 = 0.578 ≥ 0.5. Gravitino-pair decay is closed with a ~16% margin.

## D618 — CORRECTION to D616/D617 (Ddl 08:42 CT; arithmetic) — the e^{ξ′L} uplift is EXPONENTIAL at the cusp; the linearisation fails, and the "ξ′ = 1 is natural" argument is WITHDRAWN
- D616 expanded F_X²e^{ξ′(L − L(ρ))} ≈ F_X²(1 + ξ′(L − L(ρ))). But L − L(ρ) ≈ (π/3)y − ln(2y) − 0.34 reaches ≈ 21 at y* ≈ 24.
- With ξ′ = 1 the uplift grows by e^{21} ≈ 1.6e9 (arithmetic in code: ε·e^{L−L₀} ≈ 1e5 ≫ 1 at y = 24). It would swamp the plateau and destroy inflation.
- So D617's natural α = 1/3 condensate (e^K|W|² ∝ e^{L}, ξ′ = 1) gives a double-exponential wall in φ, NOT a linear tilt. That route FAILS.
- The linear tilt needs ξ′·(L − L₀) ≲ 0.3 across inflation, i.e. ξ′ ≲ 0.014. Then ε = ξ′(m₃/₂/H)² needs m₃/₂/H ≈ √(ε/ξ′) ≳ 0.065. Closure (ξ′ ≤ 1.34) is trivially satisfied, but the "O(1) coefficient" naturalness is lost: ξ′ ~ 1e-2 is itself a small, unexplained number.
- The identification ε ↔ (m₃/₂/H)² therefore survives only as a reparametrisation with a small ξ′. It does not explain ε.
Net: ε for SERAPIS-ρ (and ε·I₁ at i) remains UNEXPLAINED. D616/D617 are downgraded to "reparametrisation, not explanation". Recorded as a correction, not a silent edit.

## D619 — Ddl (08:44 CT; 2 searches) — NULL: no new r or n_s data that could score D605/D615
- Simons Observatory: only SAT commissioning papers (e.g. 2609.26938, mid-frequency SATs); no r result.
- BICEP/Keck: nothing newer than the BK18-based analyses (2512.10613 is the latest combination, D573).
- The D605/D615 forward packages stay unscored. The next decisive inputs are the first SO SAT r constraint and DESI DR3.

## D620 — DEEP (Ddl 08:44 CT; literature, no computation) — a STRING SOURCE for the |j − 1728| structure at τ = i: the Harvey–Moore threshold ln|J(T) − J(U)| at the enhanced-symmetry point T = U = i
Literature:
- Harvey & Moore, hep-th/9510182 (heterotic N = 2 one-loop thresholds/prepotential):
  - Eq. 4.26 has ½ log[J(iT) − J(iU)] in the holomorphic factor; eqs. 4.33 and 6.7 have log|J(T) − J(U)|.
  - §5.4: the divisor T = U and its modular images carry ENHANCED gauge symmetry (extra massless states), with "a double intersection at T = U = i and a triple intersection at T = U = ρ".
- Kofman, Linde, Liu, Maloney, McAllister, Silverstein, "Beauty is attractive", hep-th/0403001: moduli are dynamically TRAPPED at enhanced-symmetry points by particle production of the states that become light there.
Why this matters for SERAPIS at τ = i:
1. If the second torus modulus is frozen at U = i, the threshold becomes ln|J(T) − 1728|. U = i is natural, since a Z₄-type orbifold action on that T² FIXES U = i. That is exactly the "j − 1728" structure SERAPIS uses (I₁ ∝ ln(1 + |j − 1728|/1728)). It grows ∝ 2πy at the cusp: the linear tilt (D576). And it is centred on τ = i.
2. T = U = i is a DOUBLE enhanced-symmetry point. So τ = i is singled out physically, not only by modular symmetry: extra states become massless there, and the KLLMMS trapping mechanism attracts the modulus to it.
3. This sits on an N = 2 plane. That is ALLOWED for the home-safe models (y* < 29; D608 correction).
What is NOT shown (needs locks and careful work):
- (a) how ln|J(T) − J(U)| enters the scalar potential (via gauge-coupling-dependent condensates, Kähler corrections, or a CW potential of the states becoming massless), and with which sign;
- (b) the regularisation: the log diverges at T = U (massless states). Our I₁ = ln(1 + |·|/1728) is a regular stand-in, plausibly cut off by SUSY-breaking masses ~m₃/₂, but this is not derived;
- (c) whether the coefficient comes out ε ~ 1e-4 (e.g. a loop factor × b/16π² × (m₃/₂/H)²-type suppression);
- (d) a dedicated novelty search (HM thresholds + τ = i inflation).
Verdict: the most promising lead so far for the τ = i branch's missing ingredient (D607/D608). It turns "|j − 1728| has no string source" into "a known string threshold has exactly this structure, at the point where enhanced symmetry and moduli trapping single out τ = i". It is a lead, not a derivation.
D620a (internal cross-reference): hep-th/0403001 (moduli trapping) was already used in the Twist context (D363, D444/D446). What is new in D620 is the Harvey–Moore ln|J(T) − J(U)| threshold as the source of SERAPIS's j − 1728 structure at T = U = i. That combination does not appear in the earlier notes.

## D621 — DEEP (Ddl 08:46 CT; dedicated novelty search for D620 + reasoning) — no prior use of the Harvey–Moore T = U threshold as the source of a τ = i inflationary vacuum found; the likely potential shape near i is |δ|²ln|δ|², not I₁'s pure quadratic
Novelty search (1 extended search; one fetch):
- Kadota & Stewart, hep-ph/0409330 (PASCOS04): inflation near enhanced-symmetry points, with light fields renormalising the modulus mass. It has no heterotic T–U structure, no ln|j(T) − j(U)|, and no τ = i vacuum.
- Abe et al. 2607.00528 (CW modular, vacuum at Im τ ~ 2) is already in D572.
- Nothing found that combines the HM threshold with a τ = i inflationary vacuum. Allowed wording: "not found in the checked literature (D621)".
Reasoning on the potential's form (not computed):
- The HM log|J(T) − J(U)| comes from integrating out the states that become massless at T = U. Their masses near the point behave as m_W² ∝ |T − U|²·M_s²/(T₂U₂).
- After SUSY breaking (soft scale m), a CW-type contribution goes like V ∝ (m²/16π²)·m_W²·ln(m_W²/μ²).
  - Near i (U = i), V ∝ |δ|²ln|δ|². The vacuum curvature is LOG-ENHANCED, so the vacuum is massive (more strongly than I₁'s pure |δ|²), consistent with trapping.
  - At the cusp, m_W² ∝ y·M_s²/U₂ grows, so V ∝ y·ln y: nearly linear, a Chronos-type tilt with a log correction.
- Size estimate: ε ~ (m²M_s²/16π²)/V₀ ~ (1/16π²)(m/H)²(M_s/M_P)², with M_s/M_P ≈ 0.04 and m/H ~ 0.01–0.1, gives ε ~ 1e-9 to 1e-7 (estimate). That is TOO SMALL compared with 1.3e-4, unless m ~ H (SUSY breaking during inflation is Hubble-scale, which is plausible via Hubble-induced soft terms: m ≈ cH gives ε ~ c²(M_s/M_P)²/16π² ~ 1e-5·c²; c ~ 3–4 reaches 1e-4).
Verdict: the HM/enhanced-symmetry route gives the right STRUCTURE (centred on τ = i, linear-ish tilt, massive vacuum) and a magnitude that reaches ε ~ 1e-4 only if the light states feel Hubble-scale SUSY breaking during inflation (c ≈ 3–4). That is plausible but unshown. A locked computation of V_CW from these states (using HM's mass formula) would be the next real step.

## D622 — DEEP (Ddl 08:48 CT; locked PREREG_D622_YLNY_TILT; results/ylny_tilt_d622.txt) — the predictions are ROBUST to an HM-like y·ln y tilt; only ε shifts
Tilt T = I₁·ln(e + I₁), normalised to I₁ at y = 24 (grows ∝ y·ln y at the cusp, D621). D588 offsets applied; N* = 46–50.
- ε = 0.8e-4: n_s 0.9686–0.9723, r 4.3–4.9e-4, y* 22.8–23.9. All pass.
- ε = 1.0e-4: n_s 0.9712–0.9750, r 4.7–5.3e-4, y* 23.1–24.2. All pass.
- ε = 1.3e-4: fails at N* = 50 (+2.4σ). ε = 1.6e-4: fails.
ALLOWED: {0.8e-4, 1.0e-4}. Band: n_s 0.9686–0.9750, r 4.3–5.3e-4.
Verdict by the lock: ROBUST.
- The band overlaps D605's (n_s 0.970–0.975, r 4.8–5.7e-4) within 0.0012 in n_s and 10% in r.
- The steeper (y ln y) tilt simply moves the allowed ε down by about 30%.
- Whether the tilt is I₁-like or HM-like (y ln y), the observable predictions (n_s ≈ 0.97, r ≈ 5e-4) stand. The D605 lock does not need revising for this change of microscopic source.

## D623 — DEEP (Ddl 08:50 CT; arithmetic estimate, not locked) — with the minimal-Kähler Hubble-induced mass (c² = 3) and the home string scale, the HM route gives ε ≈ 1e-4 without tuning
Estimate from D621: ε ≈ c²·(M_s/M_P)²/16π², where c²H² is the Hubble-induced SUSY-breaking mass² of the states that become light at T = U.
- Minimal Kähler (K ⊃ |Φ|², V = e^K V_inf) gives the standard m² ≈ 3H², i.e. c² = 3, with no free choice.
- With c² = 3:
  - M_s = 1e17 GeV gives ε ≈ 3.0e-5;
  - M_s = 1.7e17 gives ε ≈ 9e-5;
  - M_s = 2.5e17 gives ε ≈ 2.0e-4;
  - M_s = 3.7e17 gives ε ≈ 4.4e-4.
- The D622 window (ε = 0.8–1.0e-4 for the y·ln y tilt) corresponds to M_s ≈ 1.6–1.8e17 GeV. That lies inside the home range (M_s ≳ 1e17, D554; heterotic M_s ≈ g·M_P/√8 ~ 1e17–4e17).
Reading: if the tilt/mass term is the Hubble-induced CW potential of the Harvey–Moore states at T = U = i, then ε is the loop factor 1/16π² times 3 times (M_s/M_P)². It comes out at ~1e-4 for a string scale in the expected range. That would turn "ε ≈ 1e-4 unexplained" into "ε fixed by the string scale".
Caveats (large):
- O(1) factors are unknown: the number of states, the CW log factor, and the sign of the SUSY-broken supertrace. The Hubble mass coefficient is model-dependent beyond minimal Kähler.
- During inflation the CW term's H-dependence varies along the trajectory; this estimate treats it as constant.
- Not computed.
Status: this is the best current candidate explanation of ε, for the τ = i branch via HM and the ρ branch via the analogous threshold. It suggests a testable relation, ε ↔ M_s, but only if the O(1) factors can be fixed. Needs a locked, explicit CW computation with the HM spectrum.

## D624 — DEEP (Ddl 08:51 CT; HM coefficients + arithmetic, not locked) — CAUTION on D620–D623: with Harvey–Moore's actual weights, the universal η-part dominates the cusp slope with the OPPOSITE sign; the HM route works only if the j-part enters V separately
Harvey–Moore eq. 6.7 (fetched): Ĩ₂,₂ ⊃ +20·log|J(T) − J(U)| + 264·[log(2T₂U₂|η(T)η(U)|⁴) − 𝒦] + … The gauge threshold is ∝ −(1/12)(1/16π²)(Ĩ₂,₂ − I₂,₂) (eq. 4.16).
With U = i fixed: Ĩ ⊃ 20·ln|J(T) − 1728| − 264·L(T) + const.
- Cusp slope per unit y: +20·2π = +125.7 versus −264·(π/3) = −276.5, a net of −150.8. The η-part dominates.
- Near i: 20·ln|J − 1728| is log-singular (a well or a peak, depending on the overall sign). −264·L contributes Hessian (+78.7 in x, −342.7 in y), but the log term dominates close to i.
Sign analysis, if V ∝ ±Ĩ via a Hubble-induced CW potential over the whole tower:
- +Ĩ: a log WELL at i (a minimum, good), but the cusp slope is −151y: V DECREASES toward the cusp, which drives decompactification and gives the wrong-sign tilt. ✗
- −Ĩ: the right-sign tilt, but a log PEAK at i. ✗
So with the full Ĩ₂,₂ the HM route CANNOT give both a τ = i minimum and the upward tilt.
Possible escapes (unverified):
- (a) the gauge threshold is Ĩ − I₂,₂, and the subtraction can change the η coefficient (I₂,₂ is the DKL integral). The right object for a CW potential must be identified.
- (b) only the states that become light at T = U feel the relevant Hubble splitting. That isolates the 20·log|J − J| piece, which gives a well at i and the right-sign (+125.7y) tilt.
- (c) a different U (not i) or a Wilson-line deformation changes the weights.
Verdict: D620–D623's "HM explains |j − 1728| and ε" is DOWNGRADED to conditional. It requires the j-part to enter V without the universal η-part (escape b), or a cancellation via (a). D623's ε ≈ 3(M_s/M_P)²/16π² estimate implicitly assumed only the light states contribute. Not resolved; a full computation is needed.

## D625 — DEEP (Ddl 08:53 CT; reasoning linking D577 and D624, not locked) — the tower part should enter V in the species form (Casas–Ibáñez), not as −264·L; that supports escape (b) of D624, conditionally
- D624 assumed the one-loop potential is ∝ the full HM integral Ĩ₂,₂, which includes the universal η-part (264·log(2T₂U₂|ηη|⁴)) from the infinite KK/winding tower.
- But the explicit one-loop vacuum energy of the TOWER under SUSY breaking was computed by Casas & Ibáñez ("Moduli self-fixing", arXiv:2507.05345, D577):
  - V ≈ (m₃/₂²M_P²/(8π)²)(c − η/N), with N the species number, N ≈ −6 ln(2y|η|⁴) + Ñ₀;
  - equivalently the species form δV ∝ y²|Ĝ₂|²/N² (D577).
- That form tends to a CONSTANT at the cusp (the 1/N correction) rather than growing linearly. It has minima at the desert points (i and ρ, where Ĝ₂ = 0).
- So, by CI's computation, the tower's universal part gives a benign, mass-without-tilt contribution: at i it is quadratic and positive (D577 slopes 2.0), with no wrong-sign linear slope.
- The linear tilt can then come only from the extra states that become light at T = U = i, whose CW contribution ∝ ln|J(T) − 1728| has the right sign for a well at i AND an upward slope (+125.7y per HM's weight 20).
- That is D624's escape (b), now motivated by CI's explicit tower result rather than assumed.
Status: the HM route is conditionally viable. A careful one-loop computation must still confirm:
1. CI's species form for the tower in our set-up (U = i, N = 2 plane);
2. the sign and size of the light-state CW term;
3. that the two add as described.
The D623 estimate ε ≈ 3(M_s/M_P)²/16π² refers only to the light-state term, consistent with this split.

## D626 — DEEP (Ddl 08:54 CT; reasoning + arithmetic, not locked) — CORRECTION/REFINEMENT of D620–D625: the light states enter the VACUUM ENERGY as CW ∝ M²ln(M²/Λ²), not as ln|J − J|; this has a sign obstruction near i, which the species term (D577) cures if κ ≫ ε
1. The HM log|J(T) − J(U)| is a GAUGE-COUPLING threshold. The light W-states' contribution to the VACUUM ENERGY under SUSY breaking (scalars split by m² = c²H²) is CW-like, V_W ∝ +(m²/16π²)·M_W²·ln(M_W²/Λ²), with M_W² ∝ |T − U|²M_s²/(T₂U₂). D620–D623 conflated the two objects.
2. Shape of V_W:
   - At the cusp, M_W² ∝ y, so V_W ∝ y·ln y: an upward tilt, the right sign (D622 showed n_s and r are robust to this shape).
   - Near i, M_W² ∝ |δ|², so V_W ∝ |δ|²ln|δ|² < 0 for small δ. τ = i is a LOCAL MAXIMUM of V_W (f(x) = x ln x falls below 0 immediately).
   - With the opposite sign (fermions heavier), i becomes a minimum, but the cusp tilt is wrong.
   - So V_W alone cannot give both properties.
3. Cure: add the species term κ·y²|Ĝ₂|²/N² (Casas–Ibáñez tower, D577/D625). It is quadratic at i with positive curvature a ∝ κ.
   - Near i, V ≈ a|δ|² + b|δ|²ln|δ|² (b ∝ ε > 0). Its minimum sits on a tiny ring, |δ_vac| = exp(−(a/b + 1)/2).
   - a/b = 10 gives 4e-3; 30 gives 2e-7; 100 gives 1e-22 (arithmetic in code).
   - With κ ~ 1e-2 and ε ~ 1e-4 (a/b ~ 100 × O(1)), the vacuum sits at i to exponential accuracy. The log-enhanced curvature only makes the vacuum heavier.
   - D577 showed κ ≤ 1e-2 leaves n_s and r unchanged, so the tower supplies the vacuum mass, the light states supply the tilt, and they do not interfere.
4. Revised consistent picture for SERAPIS at τ = i: plateau + κ·(species term, CI tower) + ε·(light-state CW, y·ln y at the cusp), with κ ≫ ε. ε ≈ 3(M_s/M_P)²/16π² (D623) applies to the light-state term.
Status: conditionally consistent; every piece now has a literature-backed origin. Not computed as a whole, and the relative size κ/ε (both ∝ (SUSY-breaking scale)²/16π²) needs an actual one-loop calculation. If κ and ε have the same origin (m² = c²H²), the ratio a/b is set by the species count Ñ₀ versus the light-state count.

## D627 — DEEP (Ddl 08:55 CT; arithmetic estimate, not locked) — if the species term and the light-state CW have the SAME SUSY-breaking origin, a/b is NOT automatically large: the vacuum stays at i only for a small species count Ñ₀ ≲ 1 and few light states
Same-origin estimate (both ∝ m²/16π², m² = c²H²):
- a (tower, CI) ~ M_P²π²|Ĝ₂′(i)|²/N(i)², with |Ĝ₂′(i)| = 0.285 (numerical) and N(i) = 6L(i) + Ñ₀ = 2.2 + Ñ₀.
- b (light W-states) ~ n_W·M_s²/2.
- a/b ~ (M_P/M_s)²π²|Ĝ₂′|²/(N(i)²n_W/2), at M_s = 1.7e17 (D623).
Results:
- Ñ₀ = 0: a/b = 35 (n_W = 2) or 8.7 (n_W = 8); vacuum offset |δ| = 2e-8 or 8e-3.
- Ñ₀ = 5: a/b = 3.2 or 0.8; |δ| = 0.12–0.41.
- Ñ₀ = 25 or 100: a/b ≤ 0.2; |δ| ≈ 0.5–0.6. The vacuum is NOT at i.
Reading: D626's cure needs κ ≫ ε. If both come from the same Hubble-induced SUSY breaking, that requires a small species count at the desert point (Ñ₀ ≲ 1) and few light states. For realistic Ñ₀ (CI use Ñ₀ ≈ 25), the light-state CW term pushes the vacuum off τ = i by ~0.5, so τ = i is no longer the vacuum.
Caveats: crude O(1) factors (the CI normalisation 4/(8π)² versus 1/(32π²), the c factors, and the n_W count). This could shift a/b by ×10 either way. Not a decisive verdict.
Status: the HM/CW route to τ = i (D620–D626) is now CONDITIONAL on Ñ₀ ≲ 1 or on a separate, larger source of the species-type mass. Combined with D624, this route is fragile. The SERAPIS-ρ branch (D610–D616), where the natural threshold ALREADY prefers ρ, does not face this problem, which strengthens the case for ρ as the string-natural vacuum.

## D628 — CORRECTION to D627's last paragraph (Ddl 08:56 CT; reasoning) — the same obstruction applies to SERAPIS-ρ; neither vacuum is favoured by this argument
- D625 argued that the string TOWER enters V in the Casas–Ibáñez species form, which tends to a constant at the cusp: a mass, NO linear tilt.
- SERAPIS-ρ (D609–D615) used ε·(L − L(ρ)) with L = −ln(2y|η|⁴) growing LINEARLY at the cusp as its tilt. By D625's own logic, that linear-L term is not what the tower produces either. So SERAPIS-ρ's tilt is just as unexplained as the τ = i branch's.
- Applying the D626 picture to ρ: with a Z₃-type orbifold fixing U = ρ, the point T = U = ρ is a TRIPLE enhanced-symmetry point (SU(3)), and its light states give the same CW |δ|²ln|δ|² term, with the same local-maximum problem near ρ. The species term also has a minimum at ρ (a desert point). So the a/b ~ (M_P/M_s)²π²|∇ species|²/(N²n_W) condition applies equally. At ρ, Ĝ₂ also vanishes, and n_W is larger (SU(3): more light states), so the condition is if anything HARDER.
- So D627's "this strengthens the case for SERAPIS-ρ" is WITHDRAWN. Both branches share the structure "species term holds the vacuum, light-state CW supplies the tilt", and both need κ ≫ ε, i.e. small Ñ₀.
- D608's point stands but is narrower: the DKL function (as a pure function) has its minimum at ρ, not i. That matters only if V contains L linearly, which D625 argues it does not.
Net status of the ε/tilt origin:
- one candidate structure, (species mass) + (light-state CW tilt, ε ≈ 3(M_s/M_P)²/16π²), for EITHER vacuum;
- conditional on Ñ₀ ≲ 1 (or a non-same-origin hierarchy κ ≫ ε);
- the O(1) factors are uncertain by ~×10;
- observables (n_s, r) are robust to the details (D622).

## D629 — DEEP (DpL tick 1, Danny 09:07 "Ddl loops"; literature recap + arithmetic, not locked) — with a realistic spectrum the species count is large (Ñ₀ ~ 200), so the same-origin HM/CW route places the vacuum OFF the symmetric point
- Normalisations: CI's δV_t = (4m²M_P²/(8π)²)g^{ττ̄}|∂Λ/Λ|² with Λ ∝ N^{−1/2}, g^{ττ̄} = 4y², ∂_τN = −πiĜ₂, giving δV_t = m²M_P²y²|Ĝ₂|²/(16N²). The light-state CW is V_W = n_b(m²/32π²)M_W²ln(M_W²/Λ²).
- Ratio: a/b = (M_P/M_s)²·1.6/(N(i)²n_b) ≈ 41/N(i)² for M_s = 1.7e17 and n_b = 8. This reproduces D627's normalisation; no new O(1) factor appears.
- Casas–Ibáñez (2507.05345, read in D577): "each chiral multiplet adds 4 states to Ñ₀". An MSSM-like light spectrum (~49 chiral multiplets) gives Ñ₀ ~ 200 (60 chirals: 240; 100: 400).
- Then N(i) ≈ 200–400 and a/b ≈ 1e-3 – 3e-4. The light-state CW dominates near the symmetric point, and the vacuum sits on a ring |δ| ≈ 0.6 away from i (or ρ).
Verdict: for a realistic spectrum, the same-origin "species mass + light-state tilt" route (D626) does NOT keep the vacuum at the symmetric point. It works only if the light-state CW term has a SEPARATE, much smaller coefficient than the tower term (e.g. light states sequestered from Hubble-scale SUSY breaking). That undercuts D623's natural ε (which assumed c² = 3 for the light states).
The HM route (D620–D628) is now DISFAVOURED: structurally plausible, but with the realistic species count the vacuum is displaced.
Open: whether a displaced vacuum on the |δ| ≈ 0.6 ring (not at a fixed point) is acceptable phenomenologically. The axion and selection-rule results assumed a fixed point.

## D630 — DEEP (Ddl 09:08 CT; reasoning, not locked) — what changes if the vacuum is displaced off the fixed point (D629's ring, |δ| ≈ 0.6)? Proton safety survives, the sterile-inflaton results are LOST, and baryogenesis options REOPEN
1. Proton parity (D528–D533): it is a MODULAR-CENTRE parity. The central element −1 = S² ∈ SL(2,Z) acts trivially on τ EVERYWHERE, so the Z₄^R/Z₈^R parity holds at any vacuum.
   - The extra fixed-point selection rule (D551/D612, mod 4 at i, mod 6 at ρ) no longer applies. That only RELAXES the constraint: couplings of any weight are non-zero off the fixed points.
   - The anomaly check (D529) and the m₃/₂ argument (D542/D585) are vacuum-independent. Proton safety SURVIVES.
2. Stationarity (D574A) is lost. Physical masses are no longer stationary, so the inflaton gets generic LINEAR couplings to all states (D589a/D601 no longer apply).
   - Consequence: Planck-suppressed decays with c_Γ ~ O(1), T_R back to ~1e6–1e7 GeV (D578's estimate), N* ≈ 49–51.
   - The D589 inflaton → N₁N₁ route (λ ~ √2 from modular forms, now not cancelled by stationarity) needs re-scoring: it was ×4–6 short with Br = 1. Higher-weight couplings or thermal leptogenesis at T_R ~ 1e7 are still short of M₁ ~ 6e10. Baryogenesis options reopen but are not solved; AD (D599) still works and would then need m_ν1 ~ 1e-7 eV, still ~massless.
3. Gravitino (D584): the inflaton–goldstino mixing is no longer protected by stationarity, but D584's closure (m₃/₂ > m_φ/2) is kinematic and unaffected.
4. Axion (D582/D587): at the displaced vacuum the Hessian is generically anisotropic and both directions are massive (from the CW + species terms). The isocurvature argument (CP symmetry along the inflationary path) still holds during inflation. After inflation both modes decay; no relic.
5. Vacuum degeneracy: an exactly isotropic a|δ|² + b|δ|²ln|δ|² would give a RING of vacua (a flat axion-like direction). Modular-invariant anisotropies (the S-symmetry acts as δ → −δ) break it to discrete minima. If the ring were nearly flat, a light axion-like mode could appear; its mass depends on higher-order terms. Flagged.
Verdict: a displaced vacuum is not fatal (proton safe, gravitino closed, no isocurvature). But it loses the special "fixed-point" physics: sterile inflaton, selection rules, the elegant τ = i story. It also needs the near-flat ring direction checked. On balance, D629's displacement turns SERAPIS into a generic modular inflation model with its vacuum near, not at, the symmetric point. The forward n_s and r (D605/D615) depend only on the plateau and tilt, so they are unchanged up to the N* shift (T_R higher → N* ≈ 49–51, Δn_s ≈ +0.001 relative to the D602 rows).

## D631 — DEEP (Ddl 09:08 CT; 1 search + reasoning, not locked) — sequestering cannot rescue the HM/CW route: it suppresses the tilt together with the light-state term; the ε-origin question returns to "unexplained"
- Literature (search): the standard no-scale/sequestered Kähler structure (e.g. K = −3ln(T + T̄ − |Φ|²/3)) cancels Hubble-induced masses for sequestered matter, e.g. no-scale D-term inflation 1309.3122. That can set c² ≈ 0 for the light W-states.
- But in D626 the light-state CW term IS the tilt source: b ∝ c²m²M_s² ∝ ε. Sequestering them (c → 0) removes the tilt along with the vacuum-displacing log term, which takes SERAPIS back to Kairos-like n_s (−3σ to −4σ vs SPA+DESI, D578/D588).
- Partial sequestering (c² ≪ 3) that keeps b ~ ε ~ 1e-4 while the tower's a stays large needs a ≫ b, i.e. the tower must feel MORE SUSY breaking than the light states by a factor ≳ 100·(N(i)/√41)², about 1e5 for N ~ 200. That is a tuning at least as severe as the original unexplained ε.
Verdict: the HM/CW route (D620–D629) does NOT provide a natural origin for ε in a realistic spectrum. Within this project, the ε (tilt + mass) term of both two-term SERAPIS and SERAPIS-ρ remains UNEXPLAINED. The observables are unaffected (D622 robustness), but the theoretical status is: "an effective model with a ~1e-4 parameter of unknown origin".
Arc summary D574–D631:
- τ = i derived as a critical point.
- The massless-vacuum flaw found and fixed by the ε term.
- The full consistency chain passes (with high-scale SUSY, a heavy dilaton and AD baryogenesis).
- Forward predictions locked (D605/D615).
- Every attempted microscopic origin of ε failed or is conditional. That last item is the honest bottom line.

## D632 — DEEP (Ddl 09:09 CT; locked PREREG_D632_RUNNING; results/running_d632.txt) — a DISTINGUISHING SIGNATURE: two-term SERAPIS has 2–3× more negative running than an attractor with the same n_s
Exact MS (D588 code): α_s from n_s at k*e^{±0.05, ±0.1}.
- HS-Kairos (validation): α_s = −8.5e-4 / −7.5e-4 (N* = 47 / 50). The attractor relation −(1 − n_s)²/2 gives −8.2e-4 / −7.3e-4, ratio 1.03. VALIDATES the code.
- Two-term ε = 1.0e-4: α_s = −9.3e-4 / −8.3e-4 versus attractor −5.1e-4 / −4.3e-4, ratio 1.8–1.9.
- Two-term ε = 1.3e-4: α_s = −9.6e-4 / −8.6e-4, ratio 2.2–2.4.
- Two-term ε = 1.6e-4: α_s = −9.9e-4 / −8.9e-4, ratio 2.8–3.1.
Physics: the exponential tilt (D576) raises n_s, but its curvature (V_φφ ∝ εy) also adds running, so α_s stays near the UNTILTED (Kairos) value ≈ −9e-4 even though n_s ≈ 0.973. A plain attractor at n_s = 0.973 would have α_s ≈ −3.6e-4.
Verdict by the lock: a distinguishing signature for the allowed ε (1.3–1.6e-4: ratio 2.2–3.1 > 2).
Detectability: Δα_s ≈ 5e-4 between two-term SERAPIS and an attractor with the same n_s.
- CMB-S4 (σ ~ 2e-3): no.
- Optimistic 21 cm / spectral-distortion combinations (σ ~ 5e-4): ~1σ.
- A ~3σ separation needs σ(α_s) ≈ 1.5e-4. A real but long-term discriminator.
Locked as a forward prediction in PREREG_D633.

## D634 — DEEP (DpL tick 2, 09:11 CT; locked PREREG_D634_RHO_RUNNING; results/rho_running_d634.txt) — SERAPIS-ρ shares the running signature
Exact MS along Re τ = 1/2, ε = 6e-5:
- N* = 47: n_s = 0.9700, α_s = −9.5e-4 (attractor −4.5e-4, ratio 2.11), y* = 23.3.
- N* = 50: n_s = 0.9727, α_s = −8.5e-4 (attractor −3.7e-4, ratio 2.29), y* = 24.1.
Verdict by the lock: ratio > 2, so SERAPIS-ρ SHARES the D632 signature. α_s does NOT distinguish the i and ρ vacua; it distinguishes "exponential-tilt SERAPIS" (either vacuum) from plain attractors at the same n_s.
Extends forward line P7 to SERAPIS-ρ as R7: α_s = −(8.5–9.5)e-4, with the same scoring as PREREG_D633.
Note: candidates (1)/(2) of this tick's prompt were already done manually (D630, D631), and (3) was skipped (< 1 day since D619).

## D635 — DERIVATION (Danny 09:11 "continue derivation on them"; counts as DpL tick 3; locked PREREG_D635_JANUS_ANALYTIC; results/janus_analytic_d635.txt) — the Janus pair in closed form, and a three-observable CONSISTENCY RELATION; PASS against the exact numerics
Derivation (cusp form V ≈ 1 − y⁻² + (ε/2)y; p = 2, α = 1/3; φ = ln y/√2):
- V′ = √2(2y⁻² + εy/2) and V″ = −8y⁻² + εy, giving N = ∫ y dy/(4 + εy³).
- Kairos (ε = 0): y*² = 8N, so 1 − n_s = 2/N, r = 1/N², α_s = −2/N².
- With the tilt fraction x ≡ εy*³/4:
  - 1 − n_s = (16/y²)(1 − x/2)  (the tilt LOWERS 1 − n_s);
  - r = (64/y⁴)(1 + x)²  (the tilt RAISES r);
  - α_s = −(128/y⁴)(1 + x/4)(1 + x)  (the tilt makes the running MORE negative).
- Janus faces: Kairos is x = 0. Chronos is x ≈ 0.2–0.5. One parameter, x, moves the model from one face to the other.
- Running enhancement versus an attractor at the same n_s: R(x) = (1 + x/4)(1 + x)/(1 − x/2)². It equals 1 at x = 0 and rises steeply, ≈ 2.8 at x = 0.47. This EXPLAINS D632's signature analytically.
- **Janus consistency relation** (three observables, two parameters):
  - ρ = 2√r/(1 − n_s), x = (ρ − 1)/(1 + ρ/2), A = (1 − n_s)/(1 − x/2);
  - α_s = −(A²/2)(1 + x/4)(1 + x).
  - Kairos limit: r = (1 − n_s)²/4 and α_s = −(1 − n_s)²/2.
Check against exact MS (8 rows):
- The relation predicts α_s within −10.6% to −12.8% in EVERY row. The offset is a uniform, subleading-order bias (I ≈ y − 0.6 and the end-point corrections).
- The exact Kairos rows come out at x ≈ −0.05 instead of 0, the same subleading offset.
- Verdict by the lock: PASS (≤ 20%).
Use: a measured (n_s, r) gives x (how "Chronos" the universe is) and a predicted α_s; measuring α_s then TESTS the whole SERAPIS family with no free parameter. The relation holds for either vacuum (i or ρ), since it depends only on the cusp form. Multiplying the leading-order α_s by 1.12 removes the bias (empirical, from this check; not a new fit to data).
D583a (citation correction, found in readiness R3): hep-ph/0611166 is "The Gravitino-Overproduction Problem in Inflaton Decay" by M. Kawasaki, F. Takahashi, T. T. Yanagida (2006). D583 attributed it to "Endo, Hamaguchi, Takahashi / Kawasaki et al." The formulas quoted were fetched from that paper and stand; only the author attribution is corrected.

## D636
CENTRE — R8 independent referee pass on paper v3 (report: papers/v3/referee/R8_REFEREE_REPORT.md). Verdict: major revision. Algebra of D635 verified exact; Chronos/ρ numbers verified against results.
D585a (correction): the no-scale statement in D585 is WRONG for a single α=1/3 modulus. For K=−ln(2 Im τ), K^{ττ̄}K_τK_τ̄ = 1 (computed), not 3; no-scale needs α=1 or three α=1/3 moduli. Tree-level soft masses are then ~m3/2 ~1e11 GeV, above the high-scale-SUSY Higgs bound (~2e10). Soft-mass, Affleck–Dine onset and superpartner statements are OPEN until re-derived (candidate fix: T⁶ = T1×T2×T3 with three α=1/3 moduli).
Further corrections queued for the paper (not yet applied): τ=i is a symmetric critical point, not a SUSY-Minkowski vacuum of the model as used; Kairos numbers must be recomputed at N* 46–49 (D578 used higher T_R); normal ordering is input from data, not a prediction (prediction is m_lightest ≲ 1e-8 eV); falsifiability statements to be harmonised with published forecasts; missing primary citations.

## D637
CENTRE — Kairos at the paper's own reheating N* (locked PREREG_D637; referee R8 major #3). Exact MS (D588 code), ε = 0, N* = 46.08/47.60/49.21: n_s = 0.9587/0.9600/0.9612, r = 3.69/3.47/3.26e-4, y* = 21.9–22.6. Distances: 2.2–3.0σ below CMB (0.9682 ± 0.0032), 4.0–4.9σ below CMB+DESI. Replaces the D578/D588 Kairos numbers (N* 48–51) in the paper. Kairos is a reference face, not a frozen prediction; no lock changed.
R8b text fixes applied to papers/v3 (serapis_v3.tex, prediction_sheet.md, drafts): τ = i reworded as a symmetric critical point (not SUSY-Minkowski in the nilpotent embedding); no-scale claim replaced by the D585a correction (soft-mass sector OPEN); ordering stated as input, prediction is m_ν1 ≲ 1e-8 eV; falsifiability rewritten (r ≳ 1e-3 excludes; r ≈ 5e-4 needs σ(r) ~ 1e-4, beyond planned experiments; CMB-S4 support ended 2025); preheating and gravitino+inflatino listed as unanalysed; α_eff = 1/12 stated; 14 primary citations added (Planck 2018 X, ACT DR6, SPT-3G D1, BK18, DESI DR2 BAO, LiteBIRD, Kallosh–Linde, Ellis–Nanopoulos–Olive, Dine–Randall–Thomas, Murayama–Yanagida, Liddle–Leach, Turner 1983, Affleck–Dine 1985); 1309.3122 cite removed. Paper compiles clean, 7 pp. Still open from R8: the no-scale (three-moduli) construction; D-labels → appendix.

## D638
CENTRE — second independent referee pass on the R8b revision (papers/v3/referee/R8_REFEREE_REPORT_2.md): MINOR REVISION (close to major). Corrections recorded here:
- D602/D605 reheating caveat: efficient preheating or instant reheating would raise N* by ~6–9 e-folds (not ~1), pushing Chronos to n_s ≈ 0.976–0.98 and y* > 25. The frozen bands therefore ASSUME inefficient preheating (T_R ≲ 1e5 GeV). Stated in the paper.
- Lock D605 differs from the paper in four places, now disclosed in the paper (locks untouched): P3 α_s attractor estimate −(3–5)e-4, superseded by D632/D633 computed −(8.6–9.9)e-4; P5 no-scale soft masses (retracted, D585a); P6 isocurvature ≲1e-10 vs computed ~1e-8 (D587); r kill 2.4e-4 (D605) vs 2.3e-4 (D615).
- Citation fix: the normal-ordering preference is cited to NuFit-6.0 (arXiv:2410.05380), not to DESI 2607.27410; the 0.0592 eV limit is cited to 2607.27410 §VI.D.2.
Paper compiles clean (7 pp). Open: D-label appendix; placeholders (Danny); three-moduli no-scale.

## D639
CENTRE — tree-level visible soft masses (locked PREREG_D639 + DEVIATIONS D1 performance only; results/soft_masses_d639.txt). Exact sympy at τ = i, S = 0, W = W0 + fS, f² = 2W0² (V0 = 0):
- A canonical matter (K ⊃ |Q|²): m_Q² = 1·m3/2² → soft masses ~1e11 GeV (the problem found in D585a).
- B conformal-frame sequestering (K = −3 ln(e^{−K_h/3} − |Q|²/3)): m_Q² = 0 exactly.
- C one modulus, matter of modular weight 1 (K ⊃ |Q|²/(2 Im τ)): m_Q² = 0 exactly. Reason: F_τ carries exactly m3/2²'s share (K^{ττ̄}|K_τ W0|² = |W0|²), and the curvature term −|F^τ|²∂_τ∂_τ̄ ln K_QQ̄ cancels it.
Verdict (per lock): the soft-mass sector closes at TREE level without no-scale, provided the visible matter has modular weight 1 (standard for modular-flavour multiplets) or is sequestered; loop-level masses then ~ m3/2/16π² ≈ 6e8 GeV (estimate; pure anomaly mediation's slepton-tachyon issue not addressed). Canonical (weight-0) matter fails. This supersedes the "three moduli needed" suggestion in D585a/D636. Status: CONDITIONAL (assumption on matter weights), not open.

## D640
CENTRE (W1; locked PREREG_D640; results/janus_offset_d640.txt) — the Janus bias is REMOVED. Asymptotically I = y − c with c = ln1728/2π = 1.1868 and I1 = I/2 exactly, so the offset enters only through the field map φ = ln(I + c)/√2. To first order in c/I* (u = 1/I*, x = εI*³/4):
  1 − n_s = 8u²[(2 − x) + cu(5 − x)],  r = 64u⁴(1 + x)²(1 + 2cu),  α_s = −32u⁴(1 + x)[(4 + x) + cu(23 + 2x)].
Inverting measured (n_s, r) numerically and predicting α_s: error vs exact Mukhanov–Sasaki −0.2 … −0.4% on all 8 points (was −10.6 … −12.8% in D635). Full slow-roll map (method B): +1.1 … +1.6%, and it recovers the true ε (1.01/1.31/1.61e-4 for 1.0/1.3/1.6e-4). PASS. The relation stays parameter-free (c is fixed by j). Kairos inversion gives ε ≈ 1.5e-6, i.e. consistent with 0.

## D641
CENTRE (W2; locked PREREG_D641; results/preheating_d641.txt) — preheating and the gravitino–inflatino channel are INEFFICIENT/CLOSED (estimates + one exact mass):
- Quadratic couplings (allowed by stationarity, g² = a m0²/M_P², a = 1): q = 5e-9 / 5e-5 / 0.46 at the end of inflation and 2e-8 / 2e-4 / 2.1 at the octic→quadratic switch for m0 = 1e9 / 1e11 / 1e13 GeV. Fields with m0 ≲ m_φ have q ≪ 1 (no broad resonance); fields with q ~ 1 have m0 ≫ ω (Mathieu A ≈ (m0/ω)² ~ 2000 ≫ 2q → adiabatic, no production). Non-resonant energy transfer ≲ 1e-13 of ρ_φ for m0 ≤ 1e11 GeV.
- Self-resonance: plateau scale ~M_P → slow (Lozanov–Amin 1710.06851); w drifts toward 1/3 at most, inside the D602 bracket w ∈ [0, 3/5]. N* unaffected beyond the bracket.
- Inflatino mass (exact sympy, W = W0 + fS, Λ = 0, goldstino projected out): m_χ̃ = (4/3) m3/2. φ → ψ3/2 + χ̃ is open only if m3/2 < m_φ/(1 + 4/3) = 9.0e10 GeV; the chain already requires m3/2 > m_φ/2 = 1.05e11 GeV, so the channel is CLOSED.
Verdict: the frozen bands' assumption (inefficient preheating, T_R ≲ 1e5 GeV) is justified at estimate level; caveat a = O(1) and the standard fermion-mass formula in the nilpotent embedding.

## D642
CENTRE (W4; locked PREREG_D642; results/running_nstar_d642.txt) — running at the paper's own N* bracket (46.08–49.21), exact MS + D632 stencil: Chronos α_s = −(8.8–10.2)e-4 (ε = 1.3e-4: −9.91/−8.82e-4; ε = 1.6e-4: −10.2/−9.12e-4), ratio to the attractor value 2.2–3.0. Kairos −(7.7–8.8)e-4, ratio 1.03. The frozen D633 band −(8.6–9.9)e-4 (N* 47–50) overlaps; the paper quotes the N*-consistent band and notes D633.

## D643
CENTRE (W6; locked PREREG_D643; results/matter_weights_d643.txt) — soft masses vs matter modular weight k (K ⊃ |Q|²/(2 Im τ)^k): exact m_Q²/m3/2² = 1 − k (k = 0, 1/3, 2/3, 1, 4/3, 2 → 1, 2/3, 1/3, 0, −1/3, −1). Vanishing tree masses need k = 1 exactly (untwisted-type matter); k > 1 is tachyonic, k < 1 gives (1−k)·m3/2² — any k ≤ 0.97 would exceed the Higgs bound (m ≳ 2e10). Gauginos: ∂_τL(i) = 0 (3e-17), so a modular-invariant threshold gives no tree gaugino mass from F_τ; gauginos are loop/anomaly-induced. Loop scale (estimates): gauginos 3e8–2.5e9 GeV; scalars between two-loop AMSB ~4e8 and generic one-loop m3/2/4π ~ 1e10 GeV — all below the high-scale-SUSY Higgs bound 2e10 GeV (marginal at the top). Sign of the one-loop scalar term is model-dependent (pure AMSB sleptons would be tachyonic). Superpartner prediction restated: none below ~3e8 GeV, conditional on k = 1 (to better than ~3%).

## D644
CENTRE (W3; arithmetic estimate, not locked) — Kairos's own reheating history. With the species-scale mass (D577) instead of εI1, the octic→quadratic switch point ρ_x depends on κ (free, ≤ 1e-2) and Ñ0. Liddle–Leach bookkeeping: an octic phase (w = 3/5) contributes (1−3w)/(12(1+w)) = −1/24 per unit ln ρ versus +1/12 for matter, so moving the switch from ρ_x = 2e-6 ρ_end to ρ_x′ shifts N* by ΔN* = −(1/8) ln(ρ_x′/ρ_x): −1.64 (immediate switch), +0.66 (1e-8), +1.81 (1e-12), +4.12 (1e-20) (computed). So Kairos's N* is NOT fixed by its potential; it rises by several e-folds for a very light species mass, moving n_s up by ~0.0008 per e-fold. The paper's Kairos numbers assume the Chronos switch point; stated as such. Kairos is a reference face, not a frozen prediction.

## D645
CENTRE (W7; 1 extended search + arithmetic, not locked) — origin of ε at τ = i, status after one more dedicated search (2025–26 modular-inflation literature: 2504.01622, 2405.08924, 2405.06497, 2411.08467, 2607.00528, 2411.18603, 2512.21597): no paper derives a term linear in ln(1+|j−1728|/1728) with a small coefficient. Two observations:
- The local structure appears naturally in the classic modular-invariant superpotential W ∝ (j − 1728)^{m/2} j^{n/3} P(j)/η⁶ with m = 1 (|H|² ∝ |j − 1728|), but there it grows as e^{2πy} at the cusp, destroying the plateau; only a LOGARITHMIC (threshold-type) dependence gives I1 ≈ y/2. So the F-term route fails at the cusp (consistent with D606–D608).
- Size: if the uplift F_X² ≈ 3m3/2²M_P² carries a one-loop threshold dependence linear in I1, F_X² → F_X²(1 + ξI1), then ε = 3ξ(m3/2/H_inf)² (cf. D616 for ρ). With m3/2 = 1.05e11, H_inf = 3.7e12: (m3/2/H)² = 8.0e-4 and ε = 1.3–1.6e-4 needs ξ = 0.054–0.066 — an unremarkable one-loop-sized coefficient. But ξI1 ≈ 0.6–0.8 at horizon exit, so the linear truncation is only marginally valid; the resummed (exponential) form fails (D618). Verdict: ε has a natural SIZE (≈ 0.06 × 3(m3/2/H)²) but still no derived ORIGIN. Status unchanged: open, now with a quantified hint.

## D646
CENTRE (W5; locked PREREG_D646; results/affleck_dine_d646.txt) — Affleck–Dine along LH_u, now computed.
Part 1 (derived + checked): the tree-level A-term from F_τ is A = F^τ∂_τ ln ŷ with ŷ the physical, modular-invariant (up to a constant phase) coupling; by D574A stationarity ∂_τŷ(i) = 0 whenever ŷ(i) ≠ 0. Numerical check with Y = E4-type couplings and weight-1 matter: ∂|ŷ| = 4e-20 / 2e-19 for weight-balanced (invariant) couplings, O(1) only for unbalanced (non-invariant) ones. So A_tree = 0 at τ = i: the referee's worry (A ~ m3/2 ≫ m_soft) does not arise; A is loop-level, ~m_soft — the standard AD regime.
Part 2 (numerical, assumptions stated): matter-dominated background, Hubble-induced −c_H H²|φ|² and a_H H A-term (c_H = |a_H| = |a_m| = 1, assumed from an X–Q Kähler coupling), A = m_soft, 8 phases. Asymmetry parameter Q = Im(ψ*ψ̇)/h² = 0.014–0.087 (|Q| median 0.020); 0 at θ = 0, π. n_B/s = (8/23)(T_R M/4M_P²)Q, M = v_u²/m_ν1 — independent of m_soft. Required m_ν1 for n_B/s = 8.7e-11: 1e-13 – 4e-13 eV (T_R = 1e3), 1e-12 – 4e-12 (1e4), 1e-11 – 4e-11 eV (1e5). Sharpens "m_ν1 ≲ 1e-8 eV" to m_ν1 ~ 1e-13 – 1e-10 eV. Σm_ν unchanged (0.0588 eV NO). Caveats: no thermal effects (thermal log / early oscillation), Hubble-induced terms assumed.

## D647
CENTRE (locked PREREG_D647 + DEVIATIONS D1 [f = √3 for Λ = 0]; results/covariant_w_d647.txt) — the MODULAR-COVARIANT completion W = (W0 + fS)η(τ)^{-2} (weight −1, so G = L(τ) + ln|W0|² + … is SL(2,Z)-invariant). G_τ = 3e-25 at i and −8e-26 at ρ (vs i/2 and 0.577i for constant W0): F_τ = 0 at both fixed points. Λ = 0 then needs f² = 3|W0|²; soft masses m_Q² = 1.000·m3/2² for k = 0 AND k = 1. Consequences: the inflaton carries NO supersymmetry breaking (the D584 gravitino problem and the m3/2 > m_φ/2 condition disappear); the weight-1 cancellation of D639/D643 disappears (soft masses ~ m3/2 for any weight). Independently confirmed by referee pass 3 (item 1). D639/D643 remain correct for the constant-W0 (Kallosh–Linde) embedding only.

## D648
(locked; results/m32_bound_d648.txt) — in the covariant completion the F-term potential V_F = m3/2(i)² e^{L−L(i)}4y²|∂_τL|² grows like e^{πy/3}: f(y*) = 2.3e11 (y = 23), 1.2e12 (24.5). If the plateau sector is left unchanged, |Δn_s| < 1e-3 requires m3/2/H < 0.9–2.2e-9, i.e. m3/2 ≲ 3–8 TeV (H = 3.7e12).

## D649
(locked; results/m32_positivity_d649.txt) — using the nilpotent freedom to absorb V_F (positivity of the X F-term is the only requirement): m3/2 < 1.3e7 (y = 23), 5.9e6 (24.5), 2.6e6 (26), 8.7e5 (28), 3.0e5 GeV (30). The operative bound depends on how far above horizon exit the field must start; y ≈ 26 (≈ 12 e-folds before exit) gives m3/2 ≲ 2.6e6 GeV.

## D650
CENTRE (arithmetic estimates, not locked; standard anomaly-mediation formulas) — the covariant-completion spectrum. F_τ = 0 and f_a independent of X (assumed) → gauginos from anomaly mediation, |M_i| = b_i g_i² m3/2/16π² ≈ (8.8e-3, 2.7e-3, 1.9e-2)·m3/2 (bino, wino, gluino; g² ≈ 0.21, 0.42, 1.0); scalars and higgsinos ~ m3/2 (gravity mediation; tree A-terms 0 at i by D646). Window: gluino > 2.3 TeV (LHC) → m3/2 > 1.2e5 GeV; thermal wino LSP ≤ 2.9 TeV (relic; T_R ≫ freeze-out) → m3/2 < 1.1e6 GeV; LHC disappearing-track wino bound (~0.66 TeV, value from memory — to verify before citing) → m3/2 ≳ 2.5e5 GeV. Inside the D649 positivity bound for y ≤ 26. Prediction: m3/2 ≈ 1e5–1e6 GeV, scalars ~ m3/2, wino LSP 0.3–2.9 TeV (dark matter at the top end), gluino 2.3–21 TeV; m_h = 125 GeV with zero stop mixing at M_S ~ 1e5–1e6 GeV needs low tan β (≈ 2–4; read from the high-scale-SUSY literature, to verify). This replaces "no superpartners below 1e8 GeV" (lock D605 P5, constant-W0 chain) for the covariant completion.
Corrections from referee 3: D645 used ε = 3ξ(m3/2/H)²; correct is ε = ξ(m3/2/H)² (V0 = 3H²M_P²) → ξ ≈ 0.16–0.30, ξI1 ≈ 1.8–3: the "natural size" hint FAILS (D645a); in the covariant completion (m3/2/H ≲ 1e-6) it is irrelevant. D646a: AD normalisation M_eff = 2M → required m_ν1 doubles (2e-13 – 9e-11 eV); present as a no-thermal estimate; M = v²/m_ν1 ≫ M_P requires a symmetry forbidding (LH_u)²/M_P. c = ln1728/2π = 1.1865 (typo 1.1868 in D640 text; script used the exact value). Constant-W0 inflaton carries 1/3 of |F|² (not ~1/4).

## D651
CENTRE (W15; reasoning + arithmetic, not locked) — inflaton → gravitinos in the covariant completion. The two-gravitino rate is ∝ |G_φ|² at the vacuum (moduli-induced gravitino problem); G_τ(i) = 0 (D647), and every other linear inflaton coupling vanishes by stationarity (D589a/D601) — the goldstino has no partner with a mass splitting, so no off-diagonal loophole. φ → 2ψ3/2 is therefore absent at linear order; no lower bound on m3/2. Thermal gravitinos at T_R = 1e3–1e5 GeV: Y ≈ 2e-19 – 2e-17 (leading scaling), lifetime 1.6e-3 s (m3/2 = 2.5e5) to 1.8e-5 s (1.1e6): decay before BBN; the winos they produce give Y·m ≲ 6e-14 GeV ≪ 4.4e-10. SAFE (estimate).

## D652
CENTRE (W12; arithmetic) — dilaton–LSP problem in the covariant completion: the LSP is a 0.66–2.9 TeV wino with freeze-out at T_f ≈ M/20 = 33–145 GeV < T_R (1e3–1e5 GeV), so winos from dilaton decays are re-thermalised and the relic is the thermal one: the D591–D596 LSP bound DISAPPEARS. Even without re-thermalisation the requirement relaxes from f_Y ≲ 4.7e-12 to ≲ 3e-5 (m_Y ≳ 30 H_end by the D592 table). The operative dilaton condition is the Kallosh–Linde one, m_Y ≳ 10 H_inf ≈ 4e13 GeV (D586/D591 racetrack window, unchanged).

## D653
CENTRE (W13; arithmetic) — thermal effects on the AD flat direction at onset (H ~ m_soft ~ m3/2 = 2.5e5–1.1e6 GeV, T_R = 1e3–1e5): plasma T ≈ (T_R²HM_P)^{1/4} ≈ 2e7–3e8 GeV; φ_osc = √(m·2M) = 4e14–2e16 GeV, φ/T ≳ 1e6, so fields coupled to φ are heavy (no thermal mass) and the two-loop thermal log is ≤ 4e-9 of the soft term. Thermal effects are NEGLIGIBLE in this regime; the D646 estimate stands (×2, D646a).

## D654
CENTRE (W14; analytic) — non-vanishing couplings at τ = i. With trivial multiplier, a coupling form of weight k_Y vanishes at i unless k_Y ≡ 0 mod 4 (weight parity). For W of weight −1, k_Y = Σk_i − 1. Cubic Yukawas can satisfy this with integer weights (e.g. k = 1, 1, 3). The Weinberg operator (LLH_uH_u) has Σk_i even for integer weights, so k_Y is odd and a SINGLET coupling vanishes at i: neutrino masses (and the AD LH_u direction, and D646's ŷ(i) ≠ 0 assumption) require flavour multiplets with non-trivial ρ(S) or half-integer (metaplectic) weights — the standard situation in modular-flavour models at τ = i (e.g. 2604.04585). Stated as a model-building requirement.

## D655
CENTRE (W16; locked PREREG_D655; results/rho_covariant_d655.txt) — SERAPIS-ρ covariant completion: X-positivity bound m3/2 < 1.3e7 (y = 23), 7.6e6 (24), 2.6e6 (26), 8.6e5 (28), 2.9e5 GeV (30) — the same as at τ = i (D649). G_τ(ρ) = 0 (D647). The τ = i spectrum window (D650) carries over to ρ.

## D654a
CORRECTION to D654 (referee 4, verified): with W ∝ η^{-2} each coupling is Y = η^{-2}h, h of weight Σk_i, and η(i) ≠ 0, so Y(i) ≠ 0 iff Σk_i ≡ 0 mod 4 (at ρ: mod 6). D654's rule (k_Y = Σk − 1 ≡ 0 mod 4) assumed a trivial multiplier. Consequences: a SINGLET Weinberg operator with k_L = k_Hu = 1 (Σk = 4, h = E4, |E4(i)| = 1.456) is non-zero at i — no flavour multiplet needed; cubic Yukawas need Σk ≡ 0 mod 4 (e.g. 1, 1, 2). D654's example (1, 1, 3) is wrong.

## D656
CENTRE (locked PREREG_D656; results/selection_eta_d656.txt) — the D551/D612 proton-parity scans redone with the η^{-2} rule (Σk ≡ 0 mod 4 at i, mod 6 at ρ), everything else verbatim: Z4^R 0/8, Z8^R 0/16 at BOTH i and ρ. No anomaly-passing assignment keeps all required couplings non-zero.

## D657
CENTRE (locked PREREG_D657; results/centre_nonr_d657.txt) — the reason, and the consistent rescan: under the centre −I, η^{-2} is invariant, so W is centre-NEUTRAL and the centre symmetry is NON-R (D528 assumed an R-symmetry, t = 1). Rescan with t = 0, gaugino charge 0: 0 anomaly-passing assignments for N = 4 and 8 (before any vacuum condition) — consistent with the known result that anomaly-free non-R discrete symmetries cannot forbid the dangerous operators while allowing the MSSM couplings (Lee, Raby, Ratz et al.; from memory, to cite only after checking). VERDICT: in the covariant completion the modular-centre origin of matter parity is LOST. Proton stability then needs a separate symmetry: standard (non-R) matter parity forbids dimension-4 operators; Planck-suppressed dimension-5 QQQL/M_P, dressed by a wino with scalars at 2.5e5–1.1e6 GeV, requires coefficients c ≲ 5e-3 – 2e-2 (estimate; natural if Yukawa-suppressed). The constant-W0 chain keeps the D528–D551 mechanism.

## D658
CENTRE (arithmetic; referee 4 items 3–6) — (a) e-folds between y = 26 and horizon exit: ≈ 6 (y* = 24.5) to ≈ 12 (y* = 23); the positivity bound at y* is (0.6–1.3)e7 GeV. (b) Higgsino threshold: with μ ~ m3/2 the threshold contribution to M2 is comparable to anomaly mediation (pure-gravity-mediation lore) → window ends uncertain by ~×2. (c) Dilaton → 2ψ3/2 (G_Y ~ m3/2/m_Y): those gravitinos decay after wino freeze-out, so Y_3/2·M2 < 4.4e-10 GeV is needed: f_Y(1.5 e-folds) ≤ 1.2e-5 (T_R = 1e5, M2 = 2.9 TeV, worst case) → m_Y ≳ 35 H_end ≈ 1e14 GeV (vacuum ≈ 2e14) by the D592 table — inside the racetrack window; D652's "bound disappears" corrected to "relaxes from 140 to ~35 H_end". (d) The X-metric construction puts the plateau in by hand (as in Kallosh–Linde); beyond y ≈ 26 the potential simply steepens.

## D659
CENTRE (novelty audit addendum, literature; found while preparing outreach) — MISSED PRIOR ART: Schimmrigk, "A General Framework of Automorphic Inflation" (1512.09082) and "Modular Inflation Observables and j-Inflation Phenomenology" (1612.09559): V = Λ⁴|j(τ)|² on the Poincaré upper half-plane; zero at ρ (triple zero of j); slow-roll point at τ = i because ε_V ∝ |E6/E4|² vanishes there; n_s ≈ 0.96, r ∈ [1e-8, 0.08]. Overlap with SERAPIS: the invariant |j|² (our ρ plateau I_ρ) and E6(i) = 0 singling out τ = i. Difference: SERAPIS puts these invariants inside a bounded log plateau (Kallosh–Linde form) with inflation from the cusp, a massive vacuum from a second term, the Janus relation, and the reheating/SUSY chain. D611's "combination not found" stands, but these papers must be cited; added in v3.1 (intro, prior art, ρ section). Not in Zenodo v3 (10.5281/zenodo.24250733) — a v3.1 new version is needed.

## D660
(locked; results/centre_mp_d660.txt) — non-R centre as ORDINARY matter parity (dim-4 forbidden, dim-5 allowed), with D551's Kähler conditions: 0/0 (no assignment passes the pre-filters; the Kähler conditions reject even textbook matter parity).

## D661
(locked; results/centre_mp_nok_d661.txt) — same without the Kähler conditions (dimension-6, Planck-suppressed: amplitude 1/M_P² = 1.7e-37 GeV⁻², 3e-6 of the proton bound — harmless; justification written before running): ρ PASSES 4/4 (Z4) and 8/8 (Z8), e.g. n = (0,2,2,0,2,2,2), all couplings non-zero at ρ (Σk ≡ 0 mod 6). τ = i: 0/4, 0/8 (lifts {0,2}).

## D662
(locked + DEVIATIONS D1, D2 — script construction/syntax only, no computation had run) — like-for-like lifts {0,2,4} at τ = i: still 0/4, 0/8.

## D663
CENTRE (analytic, explains D661/D662) — at τ = i a centre-derived matter parity and a singlet Weinberg operator are incompatible. Non-R centre phase e^{−iπk}: matter parity needs k odd for Q, U, D, L, E and k even for H_u, H_d. Then Σk(LLH_uH_u) = 2k_L + 2k_Hu ≡ 2 (mod 4), so its η^{-2} coupling vanishes at i (weight parity). Likewise a singlet Majorana mass N N (k_N odd) has 2k_N ≡ 2 (mod 4) and vanishes at i. At ρ the condition is mod 6 and is satisfiable (D661). VERDICT: SERAPIS-ρ (covariant) keeps a modular origin for ordinary matter parity; SERAPIS at τ = i (covariant) needs flavour multiplets with non-trivial ρ(S) (or matter parity from outside the modular group) to have both matter parity and neutrino masses. Dimension-5 QQQL then needs c ≲ 5e-3 (D657) in both.

## D664
CENTRE (locked PREREG_D664; results/i_flavour_d664.txt) — τ = i covariant completion WITH Γ2 ≅ S3 flavour multiplets: centre matter parity (k_L = k_N = 1, k_Hu = 0; −I ∈ Γ(2) so ρ(−I) = 1) and neutrino masses COEXIST. Weinberg operator with L a doublet (Σk = 2, h = the D597 weight-2 doublet, Y(i) = (0.1306, 0.0754)): singular values (0.1508, 0.1508) — non-zero and exactly degenerate (A(Y)² = s²·1). Leptons as 2 ⊕ 1: rank 3 for b = 0.3, 1, 3 (smallest/largest = 0.077, 0.38, 0.28); no forced massless state. Majorana N doublet: (0.1508, 0.1508), degenerate at i — so the N splitting needed for the off-diagonal decays (D589–D598) must come from elsewhere (e.g. a 2 ⊕ 1 structure or small departures). The tiny m_ν1 needed by Affleck–Dine (D646) is NOT produced by this structure (it needs a tuned b); it remains a requirement. Verdict: the D663 obstruction at τ = i is lifted by the same Γ2 flavour structure already used in D597.

## D666
CENTRE (locked PREREG_D665; results/janus_ext_d665.txt) — Janus extended.
(A) Exact MS at the paper's N* brackets: τ = i (ε = 1.3/1.6e-4, N* = 46.08/49.21) and ρ (ε = 6e-5, N* = 46.09/49.49): n_s = 0.9691–0.9754, r = 4.67–5.76e-4, α_s = −(8.69–10.21)e-4. Full slow-roll map (method B) predicts α_s within +1.1–1.4% for ALL points, ρ included, and recovers ε (1.31/1.61e-4 and 6.04/6.03e-5). The τ = i offset-corrected closed form (D640) applied to the ρ points gives −1.0%: ONE relation serves both vacua to ~1%. PASS.
(B) Running of the running: exact β_s = −(2.95–4.60)e-5; method B within −17 … +15%. Leading closed form β_s = 128u⁶(1+x)(2x² − 5x − 16) (u = 1/I*, x = εI*³/4); x = 0 gives −2048u⁶ = −4/N*³, the standard attractor value. PASS (25% tolerance, fixed in advance). Forward prediction frozen as D667 (P8, P9).

## D668
DEEP (DpL tick 1 on Janus; literature, no computation) — novelty of the Janus closed form and consistency relation.
- Kallosh & Linde, singular α-attractors (2512.02969): report n_s and r only (N = 55); NO running, no n_s–r–α_s relation, no tilt-fraction parameter. Their power-law singular T-model V₀tanh^{2γ}[1 + δcosh^{2β}] has the large-field form V ≈ V₀(δ/2^{2β})e^{β√(2/3α)φ}; with α = 1/3, β = 1 this is exactly our εI1 ≈ (ε/2)e^{√2φ} ramp. So Chronos is the "power-law singular" ramp on a plateau whose own approach is e^{−2√2φ} (α_eff = 1/12) — prior art for the ingredient, already cited.
- Generalised exponential plateau (2507.17721): α_s formula only, no values, no uplift, no relation.
- One extended search (consistency relations with uplift/enhanced running, 2025–26) found nothing equivalent.
Verdict: the closed forms (D635/D640), the consistency relation and β_s (D666) appear NEW (labelled: literature check of 3 sources + 1 extended search, not exhaustive). Next: derive the Janus relation for a general plateau 1 − e^{−pφ} + δe^{qφ} (covers KL's singular T-models) — D669.

## D669
DEEP (DpL tick 2, manual "Ddl"; locked PREREG_D669; results/janus_general_d669.txt) — the Janus relation is GENERAL. For V ≈ 1 − Ae^{−pφ} + δe^{qφ} (κ = q/p, x = tilt slope / plateau slope at φ*): 1 − n_s = 2pA′(1 − κx), r = 8A′²(1+x)², α_s = −2p²A′²(1+x)(1+κ²x) ⇒ with ϱ = p√(r/2)/(1 − n_s), x = (ϱ − 1)/(1 + κϱ): α_s = −½(1 − n_s)²(1+x)(1+κ²x)/(1 − κx)². Only (p, κ) enter — fixed by the model class (p = √(2/3α_eff), κ = ramp/plateau exponent ratio); SERAPIS is (2√2, 1/2).
Test on Kallosh–Linde's power-law singular T-model (2512.02969), exact first-order slow roll: β = 1 (κ = 1) and β = 1/2, α = 1/3, δ = 3e-6…3e-5, N* = 50, 55: errors −0.67 … −0.94% at all 10 computed points (δ = 3e-5, β = 1 did not converge — no slow-roll solution found; not counted). Cross-check: δ = 1e-5, N = 55 gives n_s = 0.970, r = 0.0015, matching KL's quoted 0.969, 0.0016. PASS.
Meaning: the relation is a property of the whole "plateau + exponential ramp" family (singular attractors included); measuring (n_s, r, α_s) tests the family and, through κ, distinguishes members (SERAPIS κ = 1/2 vs KL β = 1 κ = 1). Novel per D668 (not exhaustive).

## D670
DEEP (DpL tick 3; 2 searches, 2 fetches + arithmetic, not locked) — can the Janus signature be measured soon? At fixed (n_s, r) the general relation gives (n_s = 0.972, r = 5e-4): attractor α_s = −3.9e-4, SERAPIS (κ = ½) −8.1e-4, KL β = 1 (κ = 1, p = √2) −2.5e-4; at r = 1.5e-3 SERAPIS −2.0e-3. Signature size Δα_s ≈ 2–4e-4 at SERAPIS's own r.
Forecasts (95% CL): SO alone 0.0066; S4 + SPHEREx 0.0024; S4 + CHIME + DESI + SPHEREx 0.0018; LiteBIRD + S4 + CHIME + SPHEREx 0.0017 (Constraining Inflation 2030, 2212.04115); SKAO-AA4 + SO ±0.003 (2607.08593). Best 1σ ≈ 9e-4 ⇒ the Janus/attractor difference is ≲ 0.5σ for 2030-era data. Measuring it needs σ(α_s) ~ 1e-4 (futuristic 21-cm / dark-ages class); β_s (~4e-5) further still. Paper's "long-term goal" wording is correct; now quantified. Near-term tests remain r (exclusion) and n_s.

## D671
DEEP (DpL tick 4, manual "Ddl"; locked PREREG_D671; results/beta_general_d671.txt) — general running of the running. Leading order β_s ≈ 2ηξ² + 2ϖ³ gives, for V ≈ 1 − Ae^{−pφ} + δe^{qφ},
  β_s = −¼(1 − n_s)³(1+x)[(1 − κx)(1 + κ²x) + (1+x)(1 − κ³x)]/(1 − κx)³, x from (n_s, r) as in D669.
Sympy: identical to D666's SERAPIS form (difference 0); x = 0 → −(1 − n_s)³/2 = −4/N³. Test on KL singular T-models (10 converged points): errors −0.78 … −0.95%. PASS. So the Janus family has a closed, parameter-free (given p, κ) chain n_s, r → α_s → β_s.

## D672
DEEP (DpL tick 5, manual "Ddl"; locked PREREG_D672; results/kappa_modular_d672.txt) — κ = 1/n for modular log-tilts, and the plateau power is measurable. With K = −ln(2 Im τ), every log of a modular form/invariant grows linearly in y (q = √2) and an I^n/(I^n+1) plateau approaches 1 as y^{−n} (p = n√2), so κ = 1/n whichever invariant tilts it (I1 at i, L at ρ). Treating n as unknown and inverting the exact (n_s, r, α_s) of all six D665 points with the leading-order relation gives n = 2.18–2.20 (true 2): PASS (2 ± 0.2). The ~+0.19 bias is the leading-order 11–13% offset bias (D635) propagated; the offset-corrected relation would remove it. Meaning: a future (n_s, r, α_s) measurement would test not only the family but the modular structure itself (κ tied to n), separating it from Kallosh–Linde singular T-models (κ = β, independent of the plateau).

## D673
DEEP ("Deeper"; locked PREREG_D673; results/janus_curve_d673.txt) — the Janus predictions in closed form from (N*, ε). N = ∫_{√2}^{I*} I³dI/[(I + c)²(4 + εI³)] (c = 0, lower limit 0: N = (I*²/8)₂F₁(1, 2/3; 5/3; −x)), then the D640 offset-corrected forms. Against exact MS at 7 points (Chronos and Kairos): Δn_s = +0.0005 … +0.0008 (the known slow-roll e-fold undercount, D587), r −1.8 … −3.6%, α_s −3.0 … −3.3%. PASS. Without the offset c (pure hypergeometric) n_s is off by ~0.004–0.005 and r by ~+20%: the offset is essential.
The Janus curve at N* = 47.6: x = 0 → n_s = 0.9605; 0.25 → 0.9682; 0.5 → 0.9745; 0.75 → 0.9798; 1 → 0.9844; 2 → 0.9986 (scale invariance at x ≈ 2.1, where the ramp balances the plateau); r grows from 3.3e-4 to 1.2e-3 and α_s from −7.9e-4 to −1.3e-3 along it.
NEW BOUND: horizon exit inside the string bound (y* ≤ 25) caps x ≤ 0.67 at N* = 47.6, hence n_s ≤ 0.978 (closed form; ≈ 0.977 after the +0.0008 slow-roll offset), r ≤ 6.1e-4, for ANY ε. A measured n_s ≳ 0.980 at ≥3σ would exclude the home-safe SERAPIS family regardless of the tilt strength (N* 46–49 moves the cap by about ±0.002 — estimate).

## D674
DEEP (locked PREREG_D674; results/exact_cap_d674.txt) — exact cap from the string bound. Secant on ε for exact y* = 25: N* = 46.08 → ε_max = 2.84e-4, n_s = 0.9836, r = 8.20e-4, α_s = −1.17e-3; N* = 49.21 → ε_max = 2.04e-4, n_s = 0.9795, r = 6.10e-4, α_s = −9.6e-4. ε_max lies above the D602 window (1.3–1.6e-4): the window is set by the n_s data cut, the cap by the string bound. Frozen as D675 (n_s ≤ 0.984, r ≤ 8.2e-4 for any ε).
D673a CORRECTION: D673 quoted the cap at N* = 47.6 only (n_s ≲ 0.978) and estimated "±0.002 across N* 46–49"; the exact cap varies 0.9795–0.9836, i.e. smaller N* allows a larger ε at y* = 25 and a higher n_s. The family-wide statement is n_s ≲ 0.984, not ≲ 0.978/0.980.

## D676
DEEP (locked PREREG_D676; results/rho_cap_d676.txt) — exact ρ cap: N* = 46.09 → ε_max = 1.42e-4, n_s = 0.9844, r = 8.30e-4, α_s = −1.18e-3; N* = 49.49 → ε_max = 9.97e-5, n_s = 0.9797, r = 6.01e-4, α_s = −9.6e-4. Essentially identical to τ = i (D674). Combined frozen cap D677: n_s ≤ 0.985, r ≤ 8.3e-4 for the whole home-safe family, both vacua, any ε. (Note: ρ's ε window 6e-5 sits well below its ε_max ≈ 1.0–1.4e-4, like τ = i.)

## D678
DEEP (locked PREREG_D678; results/janus_strip_d678.txt; figure papers/v3/figs/fig5_strip) — the exact allowed strip of home-safe SERAPIS (τ = i) in the (n_s, r) plane, 12 exact MS points along the two reheating-bracket edges from ε = 0 to the string-bound cap. Edges (x = n_s − 0.97): N* = 46.08: r = 5.336e-4 + 1.739e-2x + 0.261x²; N* = 49.21: r = 4.416e-4 + 1.535e-2x + 0.244x². At fixed n_s the allowed r spans ≤ 21% (n_s = 0.970 → r ∈ [4.42, 5.34]e-4; 0.975 → [5.24, 6.27]e-4). Along the strip α_s runs from −7.7e-4 to −1.17e-3. The strip passes through both the CMB and CMB+DESI 1σ bands. Frozen as D679 (2-D kill: a joint (n_s, r) measurement excluding the strip at ≥3σ). ρ strip not computed exactly (caps coincide within ~1%, D676).

## D680
DEEP (locked PREREG_D680; results/rho_strip_d680.txt) — exact ρ strip: edges N* = 46.09: r = 5.308e-4 + 1.709e-2x + 0.255x²; N* = 49.49: r = 4.328e-4 + 1.494e-2x + 0.237x² (x = n_s − 0.97); width ≤ 22% at fixed n_s; offset from the τ = i strip ≤ 2.2%. Untilted points coincide (n_s = 0.9587 / r = 3.69e-4 vs τ = i 0.9587 / 3.69e-4 at N* ≈ 46.1): the strip is a property of the modular plateau, not of which vacuum. Frozen as D681 (union, both vacua).

## D682
CENTRE (arithmetic on locked outputs D602/D678; estimate, not locked) — the strip is a reheating thermometer. Its height at fixed n_s comes only from the N* bracket, so a joint (n_s, r) measurement fixes N* within the family: dr/dN* = 2.6e-5 (n_s = 0.965), 2.9e-5 (0.970), 3.3e-5 (0.975) per e-fold. From D602, N* moves 0.76 e-folds per decade of T_R at fixed post-inflation history, and by ~1.57 between a matter-like (w = 0) and an octic (w = 3/5) stiff phase. So σ(r) ≈ 2–2.5e-5 at r ≈ 5e-4 would read T_R to about one decade, given w (T_R and w are degenerate along N*). Far beyond planned experiments (σ(r) ~ 1e-4 is already futuristic); recorded as a conceptual payoff of the closed relation, not a near-term test.

## D683
DEEP (literature only; NULL for computation) — attempted second-order slow-roll refinement of the Janus map (to remove the 1.1–1.6% first-order residual of method B). Sources checked: 1404.7214 (n_s second order with C = −2 + ln2 + γ ≈ −0.73; r = 16ε[1 + 8(C + 2/3)(2ε − η)] as quoted), astro-ph/9403001 (Kolb–Vadas form, different η/ξ conventions: r ∝ 2ε[1 − 2C(η − ε)]), astro-ph/0106020 (Hubble-flow, growing-horizon n_S − 1 = −2(ε1 + ε1²) − ε2, r = 16ε1; Stewart–Gong amplitude only). The r coefficients disagree across conventions as extracted, so no computation was run (avoids building on an unverified formula). Status: the offset-corrected closed form (0.2–0.4%) and the exact MS numerics already exceed what second-order slow roll would add; NOT pursued further.

## D684
DEEP (Danny "Origin of ε"; locked PREREG_D684 + DEVIATIONS D1 [grid range]; results/fterm_tilt_d684.txt, run 1 in fterm_tilt_d684_run1.txt) — the covariant F-term as the ORIGIN of the tilt. Model: V/V0 = I²/(I²+1) + R·f(y), f = e^{L−L(i)}4y²|∂_τL|² (D648), R = m3/2²/3H², no ad-hoc εI1.
1. Near i, f = 1.685|δ|² exactly quadratic → massive vacuum, m²/H² = 20.2R.
2. First-order slow roll: n_s = 0.9682 / 0.9728 reached at R ≈ 10^{−16.5}…10^{−16.95} (N* = 46.08 / 49.21) with y* = 22.3–22.9 (inside the string bound), r = (3.3–3.8)e-4, α_s = −(2.4–4.5)e-3 (interpolated between grid points; steep in R). Implied m3/2 ≈ (2.2–4.3)e4 GeV (H_inf = 3.7e12, estimate).
VERDICT (locked rule: n_s 0.965–0.975, y* ≤ 25, |α_s| ≤ 0.009): VIABLE observationally — the tilt CAN come from the modular-covariant supergravity sector, with ε replaced by (m3/2/H)².
NOT YET SELF-CONSISTENT (estimates): (a) the vacuum mass it provides is tiny, m_φ ≈ (5.6–9.6)e4 GeV, so even gravitational-strength decays give T_R ≈ 5–10 MeV (BBN-marginal) and the sterile-inflaton suppression makes it worse → a separate mass source is needed (e.g. the species term, D577, which gives mass without tilt) and the N* bracket must be recomputed for that history (D644); (b) m3/2 ~ 2–4e4 GeV makes anomaly-mediated gauginos 50–800 GeV, excluded → gauge kinetic functions must depend on X (gauginos ~ m3/2); (c) the D648 bound (m3/2 ≲ 3–8 TeV for |Δn_s| < 1e-3) is consistent: this is the regime where the F-term is the dominant tilt.
Distinct prediction of this branch: α_s ≈ −(2.4–4.5)e-3 with r ≈ 3.5e-4 — 3–5σ from the attractor at 2030-era σ(α_s) ≈ 9e-4 (D670), i.e. TESTABLE soon, unlike the εI1 branch. Status: candidate origin of ε ("F-term branch"), post-hoc, not frozen; next step = species-mass + F-term-tilt model with its own reheating and N*, locked.

## D685
DEEP (Danny "Deeper"; reasoning + arithmetic on locked outputs D577/D648/D649/D684, not locked) — the F-term branch of D684 is NOT self-consistent, and the reason sharpens the ε problem into a structural statement.
1. Same R sets tilt and mass: the tilt needs R ≈ 10^{−16.5…−16.95} (D684), which fixes the vacuum mass at m_φ ≈ (5.6–9.6)e4 GeV; even unsuppressed gravitational decays give T_R ≈ 5–10 MeV, and the sterile-inflaton suppression (D601) lowers it further — below BBN.
2. A second mass source cannot rescue it within the covariant supergravity sector: (a) the species-scale term of D577 is itself one-loop, gravitino-mass-driven (Casas–Ibáñez), so κ ∝ (m3/2/H)² ~ R and its mass is equally tiny; (b) a supersymmetric τ mass needs a holomorphic h(τ) with a double zero at i (e.g. (j − 1728) or E6/η^{12}), whose F-terms grow as e^{2πy} or e^{πy} at the cusp — 10²¹–10⁵⁷ faster than the F-term's e^{πy/3} at y ≈ 23–25 — so positivity (D649-type) bounds them even more tightly; any such mass is ≲ the F-term's.
3. Hence, in the modular-covariant completion, a vacuum mass large enough for reheating (m_φ ≳ 1e10 GeV) can only come from the non-holomorphic X-sector (the uplift metric, where the plateau itself is put in by hand). The mass term and the tilt then come together from that sector — which is exactly the εI1 term. CONCLUSION: ε is not derivable from the holomorphic/supergravity sector of this construction; it is a property of the uplift (X-metric / brane) sector, consistent with Garcia del Moral et al. (D552) that the X-metric is fixed by the brane action. Status of ε: open, but now LOCATED (uplift sector), and the F-term tilt branch is RULED OUT as stand-alone (D684 verdict revised: observationally viable, physically inconsistent).

## D686
DEEP (literature, 1 fetch + 1 search; not locked) — what the anti-D3 action says about the uplift sector where ε must live (D685). Garcia del Moral, Parameswaran, Quiroz, Zavala (1707.07059, §3.2.3): the uplift is V = M⁴e^{4A₀}/(T + T̄)³ with e^{4A₀} = e^{4u + A_z(Z, Z̄)} at the throat tip; the X-metric K_XX̄ ∝ e^{−4A₀}/[(S + S̄) f(Z, Z̄)] (dilaton S, complex-structure moduli Z). So a τ-dependent uplift requires τ to enter the warp factor A_z or f(Z).
Natural dependences: (i) power-law in a conifold-type modulus z, e^{4A₀} ∝ |z|^{4/3}; if z ∝ a modular form vanishing at i, |z|^{4/3} grows exponentially at the cusp (fails like D618); (ii) exponential in g_s through the flux hierarchy (relevant only if τ were the axio-dilaton). Neither gives the LINEAR-in-y (logarithmic-invariant) dependence of I1.
Only a logarithmic correction — one-loop / threshold-type — to A_z or f(Z), e.g. f → f(1 + b·ln(1 + |j − 1728|/1728)), would give εI1 with ε ≈ 4πb·(uplift share of V0). With the one-loop factor 1/16π², ε ≈ 1.45e-4 needs a coefficient ~0.02 — not unnatural, but this is a HYPOTHESIS about a string correction nobody has computed (labelled).
Status of the ε problem after D684–D686: the tilt-and-mass term must come from a logarithmic, threshold-type correction in the uplift (brane) sector; the supergravity (holomorphic) sector cannot supply it. A real derivation needs the τ-dependence of the anti-D3 warp factor in an explicit compactification — beyond cheap locked checks. ε thread PAUSED here.

## D687
DEEP (analysis + arithmetic; not locked) — shape vs size of the ε term. ρ variant: the tilt L = −ln(2y|η|⁴) is the universal N = 2 one-loop threshold (Dixon–Kaplunovsky–Louis), i.e. the regularised non-holomorphic Eisenstein series E(τ,1) (Kronecker limit formula); numerically L = πy/3 − ln 2y to 6 digits at y = 10–25. So the SHAPE of SERAPIS-ρ's tilt is derived from string one-loop physics; τ = i's I1 = (1/4π)ln(1 + |j − 1728|/1728) is not a standard threshold (closest: Harvey–Moore ln|J(T) − J(U)| at T = U = i, D620–D631). If the threshold enters the uplift energy with a one-loop factor, ε = b/(16π²) × (uplift share of V0 ≈ 1): ε_ρ = 6e-5 needs b ≈ 0.009; ε_i = 1.45e-4 needs b ≈ 0.023 — both ~100× smaller than typical O(1) β-function-type coefficients. So: shape derivable (ρ), SIZE still ~1e-2 unnatural relative to a naive one-loop estimate unless the coefficient is suppressed (e.g. by a small number of contributing N = 2 sectors weighted by a brane-localisation factor). Net: SERAPIS-ρ is the better-motivated vacuum on this criterion. ε thread at a genuine wall: needs an explicit compactification.

## D688
CENTRE (synthesis, no computation) — τ = i versus ρ after today's results:
| criterion | τ = i | ρ | source |
|---|---|---|---|
| critical point by symmetry, massless plateau vacuum | yes (S) | yes (ST) | D574, D609 |
| inflationary predictions (n_s, r, α_s, β_s, cap, strip) | identical within ~1–2% | identical | D666, D676, D680 |
| covariant completion F_τ = 0 | yes | yes | D647 |
| m3/2 positivity bound | ≲ 2.6e6 GeV | same | D649, D655 |
| tree A-terms vanish | yes | yes (same stationarity) | D646 |
| tilt function = standard string threshold | NO (I1; HM-type only at T = U = i) | YES (L = DKL N = 2 threshold) | D687 |
| matter parity from the centre (covariant) with singlets | NO (needs Γ2 doublets) | YES (all anomaly-free assignments) | D661–D664 |
| Γ2 flavour structure needed | yes | no | D664 |
| ε size | 1.45e-4 (b ≈ 0.02) | 6e-5 (b ≈ 0.009) | D687 |
| paper's frozen τ = i chain (gravitino, reheating) | worked out | carried over (D614) | — |
Verdict: on the evidence, SERAPIS-ρ is the better-motivated vacuum (derived tilt shape; matter parity without extra flavour structure), with identical observables. The τ = i model has more detailed reheating/baryogenesis work behind it. Reframing the paper around ρ (title currently "...at the square torus...") is a framing decision for Danny; not done.

## D689a (referee-5 corrections, recorded)
- D686/D687a: at τ = i, I1 = (1/4π)ln(…), so ε enters the logarithm as ε/4π: b = 4πε ≈ 1.8e-3 (not 0.023). ρ's b ≈ 0.009 stands.
- D685a: the "no second mass source" claim holds for the minimal single-modulus covariant completion only; E6/η¹² has a SIMPLE zero at i — the correct double-zero example is j − 1728 = E6²/Δ.
- D673a addendum: the closed-form cap at N* = 47.6 (0.978) is conservative by ~0.003 (y* overestimated by ~0.4); exact interpolation ≈ 0.981.
- D664a: the Γ2 fix at τ = i makes the heavy-N doublet degenerate at the vacuum, which shuts the splitting-driven off-diagonal decays behind T_R (D601) unless a 2⊕1 or other split multiplet supplies the splitting — OPEN condition of the τ = i model (not of ρ).
- D663a: assumes trivial-character singlet couplings from level-1 forms; other characters (e.g. η⁴, weight 2, non-zero at i) are not excluded.
- D687a: "shape derived" → "identified with" the DKL threshold (the numerical match at the cusp is trivially exact up to e^{−2πy}).

## D690
CENTRE (referee-5 item 1; arithmetic on locked D664 output, not a new lock) — the τ = i heavy-neutrino splitting. With N as Γ2 2 ⊕ 1 (the same structure D664 already uses for leptons), the doublet–singlet coupling through the weight-2 doublet form lifts the doublet's vacuum degeneracy: singular values (D664 b): b = 0.3 → doublet-like pair split ΔM/M = 0.080; b = 1 → 0.47; b = 3 → 0.33 (the singlet-like state lighter by ×0.08–0.38). The splitting-driven off-diagonal decays of D597/D601 therefore survive; with D601's scaling (T_R ~ 1e5 GeV at ΔM/M ~ 0.1, T_R ∝ ΔM) this gives T_R ≈ 1e5 GeV (b ≈ 0.3) up to ~5e5 GeV (b ≈ 1) — estimate; the upper end would raise N* by ≈ 0.5 e-fold (0.76 per decade, D682), within the strip's stated sensitivity but just above the frozen bracket. Status: referee-5 MAJOR item resolved at estimate level; the 2 ⊕ 1 coupling b is a free O(1) flavour parameter.

## D689
DEEP (Danny: "look up how they do it and calculate it"; locked PREREG_D689; results/bhk_tilt_d689.txt) — ε FROM A COMPUTED STRING LOOP CORRECTION. Input: Berg–Haack–Körs one-loop Kähler correction for T⁶/(Z2×Z2) orientifolds, K⁽¹⁾ = (1/256π⁶)Σ ℰ₂^{D3}(A,U)/((S − S̄)(ρ − ρ̄)) + …, ℰ₂^{D3} = 128N[E₂(A,U)+E₂(−A,U)] − 8N[E₂(2A,U)+E₂(−2A,U)].
Derived + checked: D3 stacks at the three half-periods of the inflaton torus give Σ_A E₂(A,U) = −(3/4)E(U,2) (lattice check at U = i: −4.5201 vs −4.5198; at 1/2 + 2i: −7.9100 vs −7.9095), hence K⁽¹⁾ = (15N/64π⁶)·E(U,2)/(Im S·Im ρ) > 0, SL(2,Z)-invariant; E(·,2) is minimal at ρ (5.7834 vs 6.0268 at i), isotropically quadratic there; grows as 2ζ(4)U₂².
Model V/V0 = P_ρ(τ)[1 + C(E(τ,2) − E(ρ,2))], C = 15N/(64π⁶ Im S Im ρ). Exact first-order slow roll: n_s = 0.9682 / 0.9728 at C = (2.4–3.7)e-7 / (4.0–5.5)e-7 (N* = 49.49 / 46.09), y* = 22.9–23.8 (inside the string bound), r = (3.8–5.1)e-4, α_s = −(0.89–1.18)e-3.
NATURAL SIZE: Im S·Im ρ = 440–1000 N; with g_s = 0.1 (Im S = 1.13): Im ρ ≈ 390–890 N; g_s = 0.3: Im ρ ≈ 1200–2700 N. VERDICT (locked rule Im S ≳ 1, Im ρ ~ 10–10⁴): NATURAL. For the first time the tilt has a computed string origin with an ordinary size — weak coupling, moderately large volume, branes at the torus's half-period fixed points — and it selects the ρ vacuum.
Comparisons: (i) tilt shape E(τ,2) ∝ y² → κ = 1 (vs εI1/εL: κ = ½); the D669 leading-order κ = 1 relation underestimates the exact α_s by 13–16% (subleading πζ(3)/y term of E(τ,2), cf. D635's 11–13% offset bias) — the offset-corrected form needs redoing for this shape. (ii) Predictions close to the ρ/τ = i εL branch: n_s, r inside the frozen strip region? (to check), α_s similar size.
OPEN: this correction is multiplicative (e^{K⁽¹⁾} scales the plateau), so it gives NO vacuum mass; the vacuum mass must come from another piece (next: D7 term, one-loop correction to the inflaton kinetic metric, or the uplift-cancelling part).

## D691
DEEP (locked PREREG_D691; results/epstein_plateau_d691.txt) — SERAPIS-E: plateau, vacuum mass AND tilt from one string quantity, the Epstein zeta E(τ,2). Model V/V0 = P_E(1 + CÊ), P_E = Ê/(Ê + 1), Ê = E(τ,2) − E(ρ,2) (minimum at ρ, D689); C = BHK coefficient 15N/(64π⁶ Im S Im ρ).
1. Vacuum at ρ: d²V/dφ² = 11.57 V0 ⇒ m²/H² = 34.7, m_φ ≈ 2.2e13 GeV (heavy: m > H, so post-inflation oscillation is quadratic at once — no stiff octic phase).
2. Untilted: y* = 13.7/14.2, n_s = 0.9588/0.9616, r = 4.0/3.5e-4 (N* = 46.09/49.49) — attractor-like (plateau approach 1 − 1/(2ζ(4)y²), effective I = √(2ζ(4))·y, so y* ≈ 14).
3. Tilted, exact first-order slow roll: n_s = 0.9682 at C = 1.0e-6 / 5.8e-7, n_s = 0.9728 at C = 1.3e-6 / 1.1e-6 (N* = 46.09/49.49); y* = 14.1–14.7; r = (4.2–5.7)e-4; α_s = −(0.89–1.21)e-3. Natural size Im S·Im ρ = 190–420 N.
VERDICT (locked: n_s 0.965–0.975, y* ≤ 25, |α_s| ≤ 0.009, m_φ ≳ 1e10 GeV, natural moduli): VIABLE on every criterion. For the first time the whole SERAPIS structure — plateau, massive vacuum at a fixed point (ρ, selected by the Epstein minimum), and tilt — follows from string one-loop objects (the Epstein/Eisenstein series of the torus complex structure and the Berg–Haack–Körs Kähler correction with D3s at the half-periods), with no ad-hoc ε: the tilt size is set by Im S·Im ρ ≈ 200–400 N (weak coupling, moderate volume). Horizon exit y* ≈ 14 is far inside the string bound.
Caveats (stated): the plateau P_E = Ê/(Ê + 1) is still placed in the uplift (X-metric) sector by hand (as all KL constructions); the BHK formula is for T⁶/(Z2×Z2); the N* bracket must be recomputed for the heavy vacuum (matter-like reheating from the start); exact MS spectra and frozen predictions still to do. Post-hoc model, NOT yet frozen.

## D692 (DEEP) — SERAPIS-E: exact Mukhanov–Sasaki spectra and heavy-vacuum N* bracket
Lock PREREG_D692 (+ DEVIATIONS: line-range typo only). Script theory/modular/serapis_e_exact_d692.py; results field_tests/results/serapis_e_exact_d692.txt.
N* bracket (estimate): the vacuum at ρ is heavy (m_φ ≈ 2.2e13 GeV, m²/H² ≈ 35), so oscillation is quadratic from the start (w = 0). T_R ∝ m_φ^{3/2} for sterile decays → T_R ≈ 1e6–1e8 GeV → N* ∈ [48.4, 49.9] (the D691 bracket 46.1–49.5 was the light-vacuum/stiff one; superseded for SERAPIS-E).
Exact results (double-precision E(τ,2), checked: E(ρ,2) = 5.7833593 = D689):
| C | N* | y* | n_s | r | α_s |
|---|---|---|---|---|---|
| 0 | 48.4 / 49.9 | 13.8 / 14.0 | 0.9606 / 0.9617 | 3.75 / 3.54e-4 | −7.9 / −7.4e-4 |
| 6e-7 | 48.4 / 49.9 | 14.1 / 14.3 | 0.9662 / 0.9675 | 4.32 / 4.11e-4 | −9.0 / −8.6e-4 |
| 1.0e-6 | 48.4 / 49.9 | 14.2 / 14.5 | 0.9701 / 0.9715 | 4.75 / 4.55e-4 | −9.9 / −9.4e-4 |
| 1.3e-6 | 48.4 / 49.9 | 14.4 / 14.6 | 0.9731 / 0.9746 | 5.12 / 4.92e-4 | −10.6 / −10.2e-4 |
Slow roll (D691) agrees with exact to ≤ 0.001 in n_s at matched N*.
Compare/contrast:
- vs frozen strip (lock D679): at n_s = 0.970, SERAPIS-E gives r = 4.75e-4, inside the band (4.4–5.3)e-4. SERAPIS-E lies ON the frozen SERAPIS strip — the derived tilt lands where the fitted ε did. Inside caps (D675/D677).
- vs SERAPIS τ = i (n_s 0.970–0.975, r 4.8–5.7e-4) and ρ (0.969–0.972, r 4.6–5.1e-4): same n_s range for C = (1.0–1.3)e-6, r ~5% lower at equal n_s; α_s the same band (−(9.4–10.6)e-4).
- vs itself (C = 0, untilted Epstein plateau): n_s ≈ 0.961, r ≈ 3.6e-4 — same as Kairos (0.959–0.961, 3.3–3.7e-4). The Epstein plateau and the j-plateau share the untilted attractor: both are e^{−2√2φ} plateaus.
- Janus, κ = 1 (tilt ∝ Ê ∝ e^{+2√2φ}, plateau 1 − 1/Ê, so p = q = 2√2): general relation (D669) predicts α_s to 3.5–5% on all four points (D689's 18% offset came from using the wrong p). This is the κ = 1 member of the Janus family working without an offset term.
VERDICT: SERAPIS-E is exact-spectrum viable and sits on the frozen strip. Target n_s 0.970–0.975 needs C = (1.0–1.3)e-6, i.e. Im S·Im ρ = 15N/(64π⁶C) ≈ 190–245 N. Still post-hoc; next: freeze a SERAPIS-E lock (bands above) and add as the derived branch in the paper.

## D693 (CENTRE) — SERAPIS-E frozen and written into the paper
Lock PREREG_D693_SERAPIS_E_FROZEN (+ sha256): n_s 0.970–0.975, r (4.55–5.12)e-4, α_s −(9.4–10.6)e-4, Janus κ=1 (p=2√2) ≤ 6%, N* 48.4–49.9, C = (1.0–1.3)e-6 ⇔ Im S·Im ρ = 188–244 N; post-hoc, scored on future data only.
Paper: new Sec. "A derived branch: SERAPIS-E" (before Limitations), ref BHK2005 (hep-th/0508043, JHEP 11 (2005) 030); now 12 pages. Prediction sheet: SERAPIS-E row + ε-origin line updated.
Not yet done: arXiv tarball/Zenodo v3.1 rebuild (needs Danny's "Publish" for Zenodo); outreach drafts not updated.

## D694 (DEEP) — Are SERAPIS-E's D3 stacks stable at the half-periods? Not by the loop alone.
Lock PREREG_D694; results/d3_stability_d694.txt. Per stack g(A) = 256E2(A,U) − 16E2(2A,U); with V ∝ e^K and K⁽¹⁾ = −Ng/(1024π⁶ ImS Imρ), a stack is stable where g is maximal.
Found (U = ρ): g has its maximum at the origin (Δg = −5.9 at δ = 0.01, all directions) and MINIMA at all three half-periods (Δg = +1.6 to +2.8 at δ = 0.01). At U = ½ + 14i: origin stable, (½,0) a saddle, (0,½), (½,½) minima of g. So under the one-loop potential alone the half-period stacks are UNSTABLE and roll to the origin; with all stacks at the origin K⁽¹⁾ = −45NE/(64π⁶ ImS Imρ): tilt of the WRONG sign (3× larger, negative) — no inflation. The expected ln-enhanced image-term instability is confirmed in sign; the origin is stabilised by the 256E2(A) term.
Size (estimate): tachyonic curvature δK'' ≈ −1.6e-4 per (unit a)² at U = ρ for C = 1.15e-6; with K_aa ~ ImU/Imρ (~1/200 at ρ), m_A² ≈ −0.1 H²; at horizon exit (U₂ = 14) ≈ −1 H². The instability is weak: Hubble-scale.
How to make it work (compare outward):
1. Fractional D3 branes at the Z2 fixed points: stuck, no position modulus — the cleanest fix; needs a twisted-tadpole-consistent placement at the half-periods (to be checked against the T⁶/(Z2×Z2) discrete-torsion literature). The untwisted annulus (the E2 piece used here) is unchanged; a twisted piece may add U-dependence (to compute).
2. A pinning mass m_A² ≳ H² from the tree-level D3 potential: in KKLT-type stabilisation D3 positions generically get m² ~ H² (the "η problem" of D3-brane inflation, BHK hep-th/0404087: "too large to allow for slow-roll") — here that problem works FOR us, but the minimum must sit at the half-periods (a Z2-symmetric k(A) gives extrema there; which is the minimum is model-dependent).
3. Imaginary-self-dual flux with D3s at the fixed points (flux forces vanish there by symmetry) — same requirement as 2.
VERDICT: SERAPIS-E's tilt sign rests on the D3 stacks being held at the half-periods by something stronger than ~H²; the loop correction itself pushes them to the origin. New stated caveat; does not change the frozen predictions (lock D693), but the microscopic claim is conditional on 1 or 2.

## D695 (DEEP, literature) — Pinning route 1 exists: stuck D3 branes at the Z2 fixed points
Source: Maiden, Shiu, Stefański, "D-brane spectrum and K-theory constraints of D = 4, N = 1 orientifolds" (hep-th/0602038), on T⁶/(Z2×Z2) orientifolds: (i) "stuck" branes sit at orbifold fixed points and the orientifold projection removes the moduli that would move them off — no position modulus; (ii) stuck branes carry NO twisted RR charge (before orientifolding: a pair of fractional branes with opposite twisted charges), so they add no twisted tadpole; (iii) which brane types exist depends on the discrete-torsion choice (hyper- vs tensor-multiplet model); (iv) K-theory constraints restrict their numbers.
Consequences for SERAPIS-E: the half-periods 0, ½, ½U, ½+½U of the inflaton T² are fixed points of the Z2 reflections, so stuck D3s can sit at the three non-origin ones. With no twisted charge, the twisted-sector annulus between them and the O-planes vanishes at the charge level, so the U-dependence is the untwisted E2 piece used in D689 (the counting N → per-stuck-brane normalisation changes C by O(1), absorbed into Im S·Im ρ ≈ 190–245 N → O(1) shift, still natural). The D694 instability is removed: no modulus, nothing to roll.
Remaining to check (stated): (a) that a stuck-brane configuration at the three half-periods (and not the origin) satisfies the untwisted D3 tadpole plus the K-theory parity conditions for one of the two torsion models; (b) the exact coefficient of the untwisted annulus for stuck branes (vs BHK's 128N/−8N for bulk D3s); (c) twisted NS-NS exchange (charge-neutral ≠ zero tension coupling) — may add a small U-dependent term.
VERDICT: route 1 is supported by the literature; SERAPIS-E's microscopic claim now rests on a definite, checkable configuration (stuck D3s at the three half-periods) instead of an unstable one.

## D696 (DEEP) — Tadpole budget for SERAPIS-E's stuck D3s: works, and the tilt measures brane asymmetry
Source: Maiden–Shiu–Stefański hep-th/0602038: 64 O3-planes of charge −½ each; D3 tadpole Σ N_α n¹n²n³ = 16κ_ΩR (eq. 4.10; κ = 1 for the standard O3 sign); stuck D3 = (3;0,0,0), BPS, no position moduli; K-theory probe constraints (eqs. 4.14–4.17, e.g. Σ N m¹m²m³ ∈ 4Z) involve only the magnetic numbers m, so are trivially satisfied by D3s (m = 0). Not stated there: whether one stuck brane counts as one D3 unit — ASSUMED here (to verify).
Derived (D689 conventions, arithmetic in code): three equal stacks N at the half-periods and N0 at the origin give Σℰ = −240(N − N0)N-normalised·E, so the tilt coefficient is C = (15/64π⁶)·N_eff/(Im S Im ρ), N_eff = N − N0. Placing EQUAL numbers at all four fixed points gives Σ_{4 pts} E2(A,U) = E/4 and Σℰ = 256·E/4 − 64E = 0: NO tilt. So the SERAPIS-E tilt is a direct measure of how unevenly the D3 charge sits among the four O3 fixed points of the inflaton torus.
Tadpole 3N + N0 + N_flux = 16:
| N | N0 | flux | N_eff | Im S·Im ρ for n_s 0.970–0.975 |
|---|---|---|---|---|
| 5 | 1 | 0 | 4 | 750–975 |
| 5 | 0 | 1 | 5 | 938–1219 |
| 4 | 4 | 0 | 0 | no tilt |
| 4 | 0 | 4 | 4 | 750–975 |
| 3 | 0 | 7 | 3 | 563–731 |
(This replaces the generic "≈ 190–245 N", which absorbed N; with the tadpole fixed, Im S·Im ρ ≈ 560–1220, natural: weak coupling, moderate volume.)
Mobile (non-stuck) D3s are not allowed to carry the remainder: by D694 they roll to the origin and count in N0. The flux-free choice is unique up to images: (N, N0) = (5, 1).
VERDICT: a concrete, tadpole-consistent configuration exists — 5 stuck D3s at each of the three half-periods, 1 at the origin (or 1 unit of ISD flux instead). Open: stuck-brane D3 unit (×½ would halve N_eff, Im S·Im ρ ≈ 375–610: still natural); twisted NS–NS exchange; whether κ_ΩR = +1 in the BHK model.

## D697 (DEEP, literature) — Twisted-sector contamination of SERAPIS-E: none for stuck branes
Source: Blumenhagen–Schmidt, "Gauge thresholds and Kähler metrics for rigid intersecting D-brane models" (0711.0866), T⁶/(Z2×Z2′) rigid branes (IIA, T-dual picture). Every twisted-sector annulus term is proportional to the twisted-charge overlap σ^i_ab = ¼Σ_kl ε^i_{a,kl}ε^i_{b,kl}: same-stack −32πN²Σ4σ^i_aa ln η, different charges ∝ σ ln η, different fixed points/Wilson lines a θ[…](0,iT)/η term (finite, no massless modes). Twisted pieces are functions of η and θ of the torus modulus, i.e. holomorphic-log type (κ = ½ class, like L), not Eisenstein type.
Applied: stuck D3s carry zero twisted charge (D695, hep-th/0602038) ⇒ ε = 0 ⇒ σ_ab = 0 for every pair involving them ⇒ their twisted annulus contributions vanish identically (inference from the σ-proportionality; not stated explicitly for stuck branes in either paper). The SERAPIS-E tilt is therefore purely the untwisted E(U,2) piece: no extra U-dependence, κ = 1 structure (D692 Janus check) preserved.
Normalisation of a stuck brane in D3 units: NOT found (NULL in both sources; 0711.0866 fixes normalisation by matching β-function coefficients only). Bracket kept from D696: Im S·Im ρ ≈ 375–1220.
VERDICT: open item (c) of D695 closed (no twisted contamination); item (b) normalisation remains a factor-2 bracket, not a viability issue. Remaining SERAPIS-E caveat of substance: the plateau P_E placed in the uplift sector by hand.

## D698 (DEEP) — The hand-placed plateau form does not matter: SERAPIS-E is fixed by its asymptotics
Lock PREREG_D698; results/plateau_robust_d698.txt (first-order slow roll, D691 code, N* = 49.15).
| form | m²/H² at ρ | C = 1.0e-6: n_s, r, α_s | C = 1.3e-6: n_s, r, α_s |
|---|---|---|---|
| (a) Ê/(1+Ê) | 34.7 | 0.9711, 4.59e-4, −9.67e-4 | 0.9742, 4.96e-4, −1.041e-3 |
| (b) 1 − (1−e^{−Ê})/Ê | 17.4 | 0.9716, 4.51e-4, −9.58e-4 | 0.9749, 4.88e-4, −1.033e-3 |
Δn_s ≤ 0.0007, Δr/r ≤ 1.9%, Δα_s ≤ 1% ⇒ PASS (rule: < 0.002, < 5%). Only the vacuum mass changes (×½; T_R ∝ m^{3/2} ⇒ ΔN* ≈ −0.1, negligible).
Analytic completion: any plateau P(Ê) → 1 − a/Ê + O(Ê⁻²) gives the same CMB observables up to O(Ê*⁻²) ~ 1e-5 corrections (Ê* ≈ 2ζ(4)y*² ≈ 460); a rescales y by √a (a shift of φ) and is absorbed into C → C·a, which is fitted. So the hand-placed caveat reduces from "a specific function" to "an uplift that vanishes at ρ and saturates as 1 − O(1/E(τ,2))" — a much weaker requirement: e.g. a nilpotent-X metric K_XX̄ ∝ 1 + a/Ê (Ferrara–Kallosh–Linde-type construction) or any one-loop-corrected uplift whose leading moduli dependence is through E(τ,2).
VERDICT: SERAPIS-E's predictions are insensitive to the interior plateau form; the remaining input is the qualitative structure (zero at ρ, saturation through E(τ,2)). Paper caveat can be softened accordingly.

## D699 (DEEP) — The SERAPIS-E plateau is one Epstein ratio: V = V0[1 − E(ρ,2)/E(τ,2)](1 + CÊ)
Identity: with a = E(ρ,2) = 5.7834, the plateau Ê/(Ê + a) = (E − E_ρ)/E = 1 − E(ρ,2)/E(τ,2). By D698 the choice a = 1 (D691) vs a = E_ρ changes nothing observable (a absorbed into C: C_new = C·E_ρ ⇒ same Im S·Im ρ bracket after rescaling, recorded in D696 units). So SERAPIS-E can be written entirely in one modular-invariant object: a constant uplift V0 minus a negative term ∝ 1/E(τ,2), tuned to vanish at E's minimum (the usual dS tuning), times the BHK one-loop factor.
Structure required of string theory: a negative (AdS-type) contribution scaling as 1/E(τ,2). At large Im τ, 1/E → 1/(2ζ(4)y²) — the same fall-off as e^{K}-type terms with y⁻² weight; E(τ,2) is the natural modular-invariant completion of y² (its leading term), so a modular-invariant term with y⁻² asymptotics and no other scale is plausibly ∝ 1/E(τ,2) (argument, not derivation; not unique: e.g. functions of j also exist).
Literature (1 search: non-holomorphic Eisenstein inflation potentials): no paper found writing V ∝ 1 − E(ρ,2)/E(τ,2) or deriving a 1/E(τ,2) term from a string loop; closest are modular Starobinsky/species-scale models (2407.12081, already cited) and KL modular α-attractors (2408.05203). Novelty claim NOT made (one search only).
VERDICT: reformulation, not derivation. The plateau caveat now reads: "needs an AdS-type term ∝ 1/E(τ,2)". Concrete string source: NOT found (NULL on that sub-question).

## D700 (DEEP, outward) — A concrete origin for a 1/E plateau: Casimir energy + area-modulus elimination → SERAPIS-C
Lock PREREG_D700; results/casimir_plateau_d700.txt.
Mechanism (compared outward to 6D Casimir stabilisation literature, e.g. Ponton–Poppitz-type T² Casimir energies; argument, not a string derivation): a 6D field on T² has Casimir energy ∝ E(U,3)/A³ (Epstein, Σ′ normalisation); in 4D Einstein frame V = +bE(U,3)/A⁴ (fermion-dominated sign) − |T|/A² (net negative codim-2 tension). ∂_A V = 0 ⇒ V_min = −T²/(4bE(U,3)). With a constant uplift tuned to zero at E's minimum: plateau 1 − E(ρ,3)/E(τ,3). Exact identity of the D699 structure, with s = 3 instead of 2.
Checks: E(τ,3) series = lattice to 1e-7 (4.6589136 at i; 16.888018 at ½+2i). E(τ,3) minimal at ρ (4.1413 < 4.1618, 4.1625 at ρ+0.05, ρ+0.05i; 4.6589 at i) — the vacuum is again at ρ, as the Rankin–Cassels–Ennola theorem says for Epstein zeta.
SERAPIS-C = [1 − E(ρ,3)/E(τ,3)](1 + CÊ2) (BHK tilt). Vacuum m²/H² = 18.0, m_φ ≈ 1.6e13 GeV (heavy; N* bracket 48.4–49.9 kept, ΔN* ≈ −0.1).
| N* | C=0 | n_s = 0.970 at |
|---|---|---|
| 48.4 | n_s 0.9590, r 1.87e-4 | C ≈ 1.18e-6: r ≈ 2.60e-4, α_s ≈ −1.02e-3, y* ≈ 12.6 |
| 49.9 | n_s 0.9602, r 1.76e-4 | C ≈ 1.08e-6: r ≈ 2.37e-4, α_s ≈ −0.94e-3, y* ≈ 12.6 |
Compare: plateau ∝ 1 − c/y³ (p = 3√2) vs SERAPIS-E 1 − c/y² (p = 2√2): r scales as 1/p² ⇒ r_C/r_E ≈ 4/9·(tilt-enhancement) — measured 2.5e-4 vs 4.75e-4 at n_s = 0.970. Janus κ = q/p = 2√2/3√2 = 2/3. Same tilt size C ≈ 1.1e-6 (same BHK natural size).
VERDICT: VIABLE on the locked criteria (n_s reachable, y* ≈ 12.6 ≤ 25, |α_s| ≈ 1e-3, r below caps) — but r ≈ (2.4–2.6)e-4 lies BELOW the frozen SERAPIS strip (4.4–5.3e-4, lock D679) and at the edge of the SERAPIS r-floor kill (2.3–2.4e-4). This is the first variant with a sharply different r: the plateau's Epstein index s maps directly onto r (s = 2 → r ≈ 4.7e-4; s = 3 → r ≈ 2.5e-4). A future σ(r) ~ 5e-5 separates them. Post-hoc; not frozen. Open: sign requirements (fermion-dominated Casimir, net negative 3-brane tension — the D696 stuck-D3 configuration is tension-neutral at tree level, so the tension must come from SUSY breaking/anti-branes), and whether the string setting gives s = 3 (bulk 6D field) or s = 2.

## D701 (DEEP) — Casimir-plateau family: index rule, sign condition, and why ρ survives SUSY-breaking twists
Literature: Ghilencea–Hoover–Burgess–Quevedo, "Casimir energies for 6D supergravities compactified on T²/Z_N with Wilson lines" (hep-th/0506164): KK masses M² = (2π)²|n₂+ρ₂ − U(n₁+ρ₁)|²/(𝒜U₂), ρ_i = 0/½ periodic/antiperiodic; renormalised massless part ∝ −(1/𝒜²)(2πU₂)³[…] in the 6D-frame normalisation (×1/𝒜² more in 4D Einstein frame ⇒ our 1/A⁴), i.e. an Epstein-type s = 3 sum; massless periodic bosons give a NEGATIVE energy.
1. Index rule (derived): a D-dim field sees ρ_D ∝ E(U,s)/A^s with s = D/2 (6D: s = 3; 10D with the T⁴ large: s = 5; T⁴ small: s = 3); 4D Einstein frame V ∝ E/A^{s+1}; a codim-2 (in T²) tension gives −|T|/A². Eliminating A: V ⊃ −E(U,s)^{−2/(s−1)} ⇒ plateau 1 − c·y^{−e}, e = 2s/(s−1): s = 3 → e = 3 (SERAPIS-C, D700), s = 5 → e = 2.5, s → ∞ → 2. SERAPIS-E's e = 2 is the limit, not reached by this mechanism; a codim-1 source (n = 1) gives e = 1 ⇒ r ~ 1e-3+, excluded by the SERAPIS caps.
2. Sign condition: the area minimum needs a POSITIVE Casimir term with a negative tension (a negative Casimir with positive tension gives V = +T²/4bE but at a MAXIMUM in A — checked algebraically). Periodic bosons and Scherk–Schwarz-twisted fermions both contribute negatively; positivity needs more periodic (untwisted) fermions than bosons in the light spectrum — model-dependent, stated requirement.
3. Twisted boundary conditions keep the vacuum at ρ if the twist is democratic: identity Σ over the three half-period characteristics of E_s(A,U) = (4^{1−s} − 1)E(U,s) (checked numerically at U = ½+1.3i: s = 2: −0.75005 vs −0.75; s = 3: −0.937500006 vs −0.9375; s = 5: −0.99609375 exact). A Z2×Z2-symmetric sum over spin structures is therefore again ∝ E(U,s): full SL(2,Z), minimum at ρ. A single twist would break to Γ(2) and move the minimum.
Estimate: s = 5 (e = 2.5) variant r ≈ 3.3e-4 at n_s = 0.970 (scaling r ∝ 1/e² between D692 and D700; to compute).
VERDICT: the Casimir route predicts a discrete ladder of plateaus e ∈ {3, 2.5} with r ≈ 2.5e-4 and ≈ 3.3e-4, both below SERAPIS-E (4.7e-4); which rung is realised is set by the dimension of the light Casimir field. Sign requirement stated. Not frozen.

## D702 (DEEP) — The s = 5 rung computed: the Epstein-plateau ladder is a clean r-ladder
Lock PREREG_D702; results/casimir_s5_d702.txt. Checks: E(τ,5) series = lattice to 8 digits (4.1317748 at i; 64.170867 at ½+2i); minimum at ρ (2.9382 vs 2.9869/2.9891 at ρ+0.05, ρ+0.05i; 4.1318 at i). Vacuum m²/H² = 30.0, m_φ ≈ 2.0e13 GeV.
Plateau 1 − (E(ρ,5)/E(τ,5))^{1/2} (e = 2.5) × BHK tilt: n_s = 0.970 at C ≈ (0.86–1.02)e-6: r ≈ (3.28–3.57)e-4, α_s ≈ −(0.96–1.04)e-3, y* ≈ 14.6 (N* 49.9–48.4). D701 estimate 3.3e-4 confirmed.
Ladder at n_s = 0.970 (N* 48.4–49.9, same BHK tilt, C ≈ 1e-6 in all cases):
| plateau | e | origin | r | α_s |
|---|---|---|---|---|
| 1 − E(ρ,2)/E(τ,2) | 2 | SERAPIS-E (D692, exact MS) | (4.55–4.75)e-4 | −(0.94–0.99)e-3 |
| 1 − (E(ρ,5)/E(τ,5))^{1/2} | 2.5 | 10D Casimir, large T⁴ | (3.28–3.57)e-4 | −(0.96–1.04)e-3 |
| 1 − E(ρ,3)/E(τ,3) | 3 | 6D Casimir (D700) | (2.37–2.60)e-4 | −(0.94–1.02)e-3 |
(rungs 2.5 and 3: first-order slow roll; D692 showed slow roll agrees with exact MS to ≤ 0.001 in n_s.)
Pattern: n_s and α_s are set by the tilt (all ≈ equal); r is set by the plateau index alone, r ≈ 4.65e-4·(2/e)^{1.6} (fit to three points, descriptive). An r measurement at σ(r) ~ 5e-5 reads off which Epstein index — i.e. the dimension of the light field generating the plateau — nature uses. Only the e = 2 rung lies on the frozen SERAPIS strip (D679); e = 2.5, 3 lie below it.
VERDICT: all three rungs viable; the family makes a discrete r-prediction ladder. Not frozen (post-hoc); worth a lock once the sign condition (D701) is shown realisable for one rung.

## D703 (DEEP) — Sign condition of the Casimir ladder: half realisable, half obstructed
Source: Arkani-Hamed, Dubovsky, Nicolis, Villadoro, "Quantum horizons of the Standard Model landscape" (hep-th/0703067): massless periodic fermions give POSITIVE Casimir energy, bosons (and antiperiodic fermions) negative; V ∝ −(n_B − n_F); on T² (their App. B.3) the massless-boson Casimir is ∝ −(1/A²)Σ′1/|n − mτ|⁴ (an Epstein E(τ,2)/τ₂² sum, here for 4D fields on T² → 2D, s = 2); they do not analyse the shape minimum.
1. Positive Casimir (needed by D701): REALISABLE — light periodic fermions outnumbering light bosons (ADNV: only neutrinos can flip the SM sign). In a supersymmetric bulk the towers cancel, so the residual is set by SUSY breaking (m3/2 R ≪ 1 ⇒ suppressed by (m3/2 R)²; expanding the massive Epstein sum lowers the effective index — to compute if pursued).
2. Negative net codim-2 tension (n = 2 term): OBSTRUCTED in string settings with RR charge cancelled — BPS objects have tension = charge (O3⁻: −½, D3: +1, O3⁺: +½), so tension sums to the (zero) total charge; non-BPS objects (anti-D3) add POSITIVE excess (charge cancellation with N_anti anti-D3s gives net tension 2N_anti > 0); ISD flux energy cancels O-plane tension (GKP no-scale), leaving the T² area flat at tree level rather than supplying −1/A².
Consequence: in the minimal string setting the D700 two-term competition is unavailable; positive tension + negative Casimir gives a MAXIMUM (D701). Escape routes (stated, not shown): (a) a genuinely negative n = 2 source from non-BPS O-plane configurations or from SUSY-breaking corrections to the O-plane/flux cancellation; (b) a 6D (non-string) supergravity bulk with negative brane tension (SLED-type models allow either sign as input).
VERDICT: the Casimir rungs e = 2.5, 3 (D700–D702) remain viable as effective-field-theory models but lose their string anchor; SERAPIS-E (e = 2), whose plateau uses no tension competition, is unaffected and remains the string-anchored branch. Loop stopped here (main open item now needs a model-building choice, not a lookup).

## D704 (OBSERVE) — Data watch, 15 Nov 2026: nothing new that scores the frozen predictions
Searched (3): new r / n_s results in 2026. Latest combined inflation constraints remain Balkenhol et al. (2512.10613, Dec 2025): r < 0.034 (95%, Planck+SPT+ACT+BK), n_s = 0.9682 ± 0.0032 (CMB), 0.9728 ± 0.0029 (CMB+DESI BAO) — the targets already used. New in 2026: BK+SPT B-mode constraint on CAUSAL (non-inflationary) tensor sources r_ect < 0.0077 (2601.20958) — not the inflationary r, does not test SERAPIS. Simons Observatory: LAT first light / commissioning and early maps (APS April 2026); no cosmology parameter release found.
Status of the family vs current data: SERAPIS τ = i / ρ / SERAPIS-E (n_s 0.970–0.975) sit +0.6…+2.1σ from the CMB-only n_s and −0.9…+0.8σ from CMB+BAO; r ≈ 5e-4 is ~70× below the bound. Casimir rungs (D702) identical in n_s. No kill condition triggered; next decisive data: SO SAT r (σ ~ 2–3e-3, cannot reach 5e-4) and SO LAT n_s (σ ~ 0.002).

## D705 (FORWARD) — When and how the SERAPIS family gets tested (forecast map)
Sources: Bahr-Kalus et al./"Prospects for 2030" (2212.04115) Table 5 (95% CL forecasts); SO enhanced LAT (2503.00636: halves current σ(n_s); survey 2025–2034, upgrades done by 2028; SAT r forecasts in a separate paper); LiteBIRD (JAXA, launch planned 2032 on H3, ~3 yr at L2; goal δr < 0.001 total, forecast r < ~1e-4 at 95% for r = 0 fiducial); CMB-S4 ended 2025 (combinations with S4 are now hypothetical).
1σ ≈ ½ of the 95% numbers (Gaussian). Computed:
| combination (era) | σ(n_s) | σ(α_s) | σ(r) | SERAPIS-E r/σ | |α_s|/σ |
|---|---|---|---|---|---|
| SO + SPHEREx (~2030) | 8e-4 | 1.2e-3 | 4.9e-3 | 0.1 | 0.8 |
| LiteBIRD (+LSS) (~2035–36) | 6e-4* | 8.5e-4* | 4.9e-5 | 9.6 | 1.1 |
| LiteBIRD, official requirement | — | — | 1e-3 | 0.5 | — |
(*with S4-like small scales; without S4 use SO.)
Reading:
1. n_s decides first (~2030, SO LAT + SPHEREx): the SERAPIS band 0.970–0.975 is 2.3–8.5σ from today's CMB-only central 0.9682 at σ = 8e-4 — if the CMB-only value holds, the family is under pressure by ~2030; if CMB+BAO (0.9728) holds, it is confirmed in n_s.
2. r decides second (LiteBIRD, results ≳ 2035): at the forecast reach SERAPIS-E is a ~10σ detection; the Casimir rungs 7σ / 5σ; rung separations 2.6σ (e = 2 vs 2.5) and 1.9σ (2.5 vs 3). At the official δr = 1e-3 nothing is seen, which tests only the r ≲ 1e-3 cap. The kill condition "r < 2.3–2.4e-4 at 95%" becomes decisive only at the optimistic reach.
3. α_s stays below 3σ through the 2030s (1.1–1.2σ); the Janus relation test (needs σ(α_s) ~ 1e-4, D670) is beyond all funded experiments (21-cm intensity mapping beyond CHIME would be needed).
VERDICT: the family's decisive tests are n_s ≈ 2030 and r ≈ 2035–36 (LiteBIRD, at its optimistic reach). The plateau-index ladder (r 4.7 / 3.4 / 2.5e-4) is LiteBIRD-resolvable at ~2σ per step only in the optimistic case.

## D706 (OUTWARD, literature synthesis) — Where SERAPIS-E meets the 2025–2026 research front
Searches (3, one extended) + 5 fetches. Connections, each labelled:
1. SPECIES SCALE / LAPLACIAN SWAMPLAND (strongest link; hypothesis). 2506.03253 ("Laplacians in various dimensions and the swampland", 2025): species-scale Wilson coefficients obey Laplace eigen-equations on moduli space, D²F = ηF; in 10D IIB the solution is the non-holomorphic Eisenstein E_{3/2}. Masias 2510.23715 ("Higher curvature inflation and the species scale"): plateaus arise when a curvature-series potential is multiplied by a field-dependent species scale; Casas et al. 2407.12081 (cited): modular Starobinsky from the species scale. Link: every SERAPIS-E ingredient is an Eisenstein eigenfunction of the τ-Laplacian (Δ E(τ,s) = s(s−1)E; s = 2 → eigenvalue 2). Our D699 term ∝ 1/E(τ,2) is exactly what a species scale defined by an Epstein Wilson coefficient (Λ_sp^{−k} ∝ E(τ,s)) would produce: V ⊃ −Λ_sp(τ)^k. This would replace the obstructed Casimir/tension route (D703) by the species-scale route — to be tested (next: find a torus-shape Wilson coefficient ∝ E(U,2) and its species-scale exponent).
2. COMPETITOR (new, July 2026): Abe–Goto–Higaki–Kawamura–Kobayashi, "Finite modular Coleman–Weinberg inflation" (2607.00528): CW potential from vector-like quarks with modular-form Yukawas; vacuum at LARGE Im τ (2Imτ ≈ 3.5–8.5), double-exponential plateau, n_s 0.960–0.962, r ≈ (0.3–1.6)e-5, α_s ≈ −7e-4, T_R ~ 1e9 GeV. Contrast with SERAPIS-E (vacuum at ρ, n_s 0.970–0.975, r ≈ 5e-4): r differs by 30–150× — LiteBIRD (D705) separates them cleanly; n_s separates at SO+SPHEREx (~2030).
3. FLAVOUR AT ρ (supporting): Tavartkiladze 2512.24804 ("Minimal modular flavor symmetry and lepton textures near fixed points"): τ stabilised near ω (= ρ up to T) by Eisenstein-invariant potentials with modulus masses ≈ 1.4e13 GeV and 1e15 GeV — the same scale as SERAPIS-E's m_φ ≈ 2.2e13 GeV. Our inflaton's vacuum is the flavour-favoured fixed point; SERAPIS-E can be the inflationary history of a near-ω flavour model. (Their fits prefer inverted ordering — conflicts with our NO input; noted.)
4. WORLDSHEET UV/IR (supporting): Aoufia–Basile–Leone–Lotito 2603.11157 ("UV/IR relations from the worldsheet"): modular invariance ⇒ one-loop vacuum energy and Wilson coefficients related; Eisenstein regularisation; heterotic thresholds −A log(ImT ImU|η(T)⁴η(U)⁴|) = our ρ-branch L function (D687). Our tilt and plateau are of exactly this one-loop modular type.
5. STRING-LOOP INFLATION IS MAINSTREAM (context): "Loop blow-up inflation: an overview" (2604.07288) and the review "Recent progress on inflation and dark energy from string theory" (2604.16281), both April 2026 — loop corrections to K driving inflation is an active programme; SERAPIS-E's BHK tilt (D689) belongs to it.
VERDICT: SERAPIS-E sits at the intersection of three live programmes — modular inflation/flavour at fixed points, string-loop-driven inflation, and species-scale/Laplacian swampland constraints. The most promising new direction is (1): derive the 1/E(τ,2) plateau term as a species-scale effect. Competitor 2607.00528 must be cited and contrasted (r 30–150× smaller).

## D707 (DEEP, outward) — Species-scale route to the 1/E(τ,2) plateau: a real E(U,2) coupling exists, but not where the species scale lives
Follows D706 item 1. Searches 3 (one extended) + 2 fetches. Labels: LITERATURE unless marked.
1. LITERATURE — an exact E(U,2) Wilson coefficient exists. Basu, "The D⁴R⁴ term in type IIB string theory on T² and U-duality" (0708.2950): the D⁴R⁴ coefficient in 8D is E_{5/2}(M)^{SL(3)} − 8 E_2(M⁻¹)^{SL(3)} · E_2(U,Ū)^{SL(2)}, with U the torus complex structure. The SL(3) factors do not depend on U, so at fixed (τ_dil, volume, B/C) the U-dependence is exactly affine: c(U) = A − B·E(U,2). This is the first concrete string coupling we have found with the same s = 2 Eisenstein series as SERAPIS-E.
2. INFERENCE — the shape is affine, not inverse. A species scale defined from c(U), Λ_sp⁻⁴ ∝ A − B E(U,2), gives V ⊃ Λ_sp^k ∝ (A − B E)^{−k/4}. This reduces to a pure 1/E(U,2) only if A ≪ B·E (not generic: E_{5/2} and E_2 are O(1) at moderate coupling) and k = 4. So the D699 term would be a limiting case, with a new free ratio A/B — not a derivation.
3. LITERATURE — the standard species scale uses the LOWEST higher-derivative term (R² in 4D, F₁ in N=2), which is the s = 1 Kronecker-limit object −log(Im U|η(U)|⁴) (Cribiori et al. 2023; Enriques example in 2411.08467: N ≃ −6 ln[2τ₂|η|⁴]). D⁴R⁴ is subleading and does not set Λ_sp. So the natural species route gives s = 1, not s = 2. In our Epstein ladder (D700–D702) s = 1 is the log/η rung, not the e = 2 rung that fixes r ≈ 4.7e-4.
4. LITERATURE — inflation papers built on modular species scales (2407.12081, 2411.08467) find plateaus V ≃ V₀(1 − c/τ₂) at LARGE τ₂ with n_s ≈ 1 − 2/N, r ≈ 8/(a²N²) and Λ_sp ~ 10¹⁶ GeV; none discuss a vacuum at ρ. Our ρ-vacuum construction is not covered by them either way.
VERDICT: PARTIAL / WEAKENED. D706's hope that the species scale supplies 1/E(τ,2) does not hold in its simple form: the species scale naturally gives s = 1, and the only s = 2 coupling found (D⁴R⁴) enters affinely with an extra free ratio. Keep 1/E(τ,2) labelled ASSUMED (unchanged status). Useful by-product: Basu's E_2(U) coupling is a citable precedent that s = 2 Eisenstein dependence on the torus shape does occur in string effective actions.
Next (open): does the s = 1 species route, combined with the ρ-vacuum, give a viable plateau of its own? (i.e. the e→1 end of the D702 ladder — is it log-type and what r does it give?)
Sources: arXiv 0708.2950; 2411.08467; 2407.12081; Cribiori et al., Fortsch. Phys. 2023 (prop.202300150); Ibáñez 2604.27835 (review).

## D708 (DEEP) — The s = 1 (Kronecker / species-scale) rung: NOT VIABLE for SERAPIS
Lock PREREG_D708 (pushed before running, 0b7f8ee); results/kronecker_s1_d708.txt. Follows D707.
Model: V/V0 = [1 − F(ρ)/F(τ)](1 + CÊ2), F = −log(y|η|⁴) + κ, κ ∈ {0, 2} pre-registered.
Checks (COMPUTED): |η(i)| = 0.768225422326 = Γ(¼)/(2π^¾) to 12 digits. F minimal at ρ (κ = 0: 1.03352 vs 1.03435, 1.03437 at ρ+0.05, ρ+0.05i; 1.05469 at i) — the vacuum is again at ρ, as for every rung.
Result (COMPUTED, κ = 0, N* = 48.4, C = 0): y* = 118, n_s = 0.9615, r = 1.30e-3, α_s = −7.8e-4. Vacuum m²/H² = 2.9 (κ = 0), 0.99 (κ = 2) — the modulus is LIGHT during inflation, unlike rungs e ≥ 2 (m²/H² 18–30).
Run note (honest): both runs hit the 280 s time limit; the rest of the C-grid and κ = 2 (root-finder found no solution at C = 0; start point too low for the larger y*) did not finish. No rerun: the completed point already fails the locked rule twice.
Verdict against the locked rule: r = 1.3e-3 > cap 8.3e-4 and y* = 118 > 25 → NOT VIABLE. INFERENCE (from D700/D702, where turning on the tilt to reach n_s = 0.970 raised r by ~40%): adding C only makes r larger.
Cross-check (LITERATURE): this is exactly the species-scale inflation class of 2411.08467 (V ≃ V0(1 − c/τ₂), r ≃ 8/(a²N²)); with a² = 2 and N = 48.4, r ≈ 1.7e-3 — same order as our 1.3e-3. The D701 index-rule estimate (e = 1 → r ~ 1e-3+) is confirmed.
Ladder now complete at four rungs: e = 1 (species/Kronecker) r ≈ 1.3e-3 EXCLUDED by our caps; e = 2 (SERAPIS-E) 4.7e-4; e = 2.5 3.4e-4; e = 3 2.5e-4.
CONSEQUENCE: the species scale cannot be the plateau source for SERAPIS — it gives the wrong rung, too large an r, a horizon exit far out at y ~ 120 and a light modulus. The SERAPIS r-strip (4.6–5.7e-4) remains tied to an s = 2 object whose microscopic origin is still ASSUMED. Combined with D703 (Casimir rungs lose their string anchor) and D707, the open problem is now sharply posed: find a string mechanism giving a plateau ∝ 1/E(τ,2) (not affine in E, not s = 1).

## D709 (DEEP, theory) — Any 1/E(τ,2) plateau from integrating out a modulus needs E at LEADING order: a no-go for loop-correction origins
Follows D707–D708. Searches 3 (one extended) + 1 fetch (BHK hep-th/0508043; the excerpt read did not reach eq. 3.46, so the sign of BHK's E₂ term is NOT re-verified here — our D691 notes use C = 15N/(64π⁶ Im S Im ρ) > 0 as the tilt).
1. ALGEBRA (exact, by hand; two lines). Let a modulus X (dilaton s, volume, area A) be stabilised by two terms, V = a·E(U,s)/X^p − b/X^q with p > q > 0, a, b > 0. Then ∂_X V = 0 gives a·E/X^p = (q/p)·b/X^q, and V_min ∝ −E^{−q/(p−q)}. A pure 1/E plateau (the SERAPIS-E form) needs q/(p−q) = 1, i.e. p = 2q — and then at the minimum the E-term is exactly HALF the competing term, for every value of a, b, E.
2. CONSEQUENCE (no-go, inference). If the E-term is a loop/α′ correction to the term it competes with, the minimum sits where the "correction" is 50% of tree level: perturbative control is lost by construction. This is the Dine–Seiberg problem in its sharpest form. Concrete case checked: dilaton s with tree term −b/s (from −3e^K|W0|², e^K ∝ 1/s) and the BHK loop shift ∝ E(U,2)/s² — it has p = 2q and does give V_min = −b²/(4aE(U,2)) exactly (the SERAPIS-E plateau after the usual uplift tuning), but s* = 2aE/b with a/b ~ N/(64π⁶ Re T) ⇒ s* ≪ 1 (strong coupling) unless N·E/Re T ~ 10⁶. NOT a controlled origin.
3. What survives: the E(U,2)-dependent term must be a LEADING-order energy of an independent sector, as the Casimir energy was in D700 (but D700's Casimir is s = 3, and its partner tension is obstructed, D703). A natural s = 2 candidate: the leading electrostatic/gravitational energy of D3 branes and O3 planes seen through the T² — a 1/r⁴ potential (6 transverse dimensions) summed over the T² lattice gives Σ′|n + mU|⁻⁴ ∝ E(U,2)/U₂² at leading order (HYPOTHESIS; this is the same annulus physics that produces BHK's E₂, so it is string-anchored). Then the question becomes concrete: which competing term, with which power q, makes p = 2q in the 4D Einstein frame? — a power-counting exercise, next.
4. LITERATURE context: loop blow-up inflation (2502.14953; overview 2604.07288) does inflate from loop-corrected Kähler moduli, but its plateau comes from the volume/blow-up structure, not from E(U) in a denominator; 2510.19927 (symmetry points of N=1 modular geometry) treats fixed-point vacua — to read if this line is pursued.
VERDICT: NEGATIVE for "1/E(τ,2) from a loop correction" (any perturbative origin, not just species scale) — exact algebraic reason, labelled. POSITIVE narrowing: the source must be leading-order brane/O-plane (or Casimir) energy with a p = 2q partner; this is where the plateau term must come from if SERAPIS-E is string-derived. 1/E(τ,2) remains ASSUMED.
## D710 (TEST PLAN RUN; locked as PREREG_D707_MULTISCALE before a parallel session's D707–D709 landed — renumbered, lock file unchanged) — SERAPIS against every scale: results of Tests 1–10
Lock PREREG_D707; results/multiscale_d707.txt; Fig. 6 (papers/v3/figs/fig6_ns_history). Data verified this session where marked in the lock. Scoring per dataset: <2σ consistent, 2–3σ tension, >3σ fail. Consistency only (model fitted to 2025 data).
T1 n_s by release (band 0.970–0.975; nearest edge / centre 0.9725): WMAP9 inside (0.04σ); Planck 2013 1.33σ / 1.67σ high; 2015 0.73σ / 1.13σ; 2018 1.21σ / 1.81σ; P-ACT-LB inside (−0.50σ); SPA 0.56σ / 1.34σ; SPA+DESI inside (−0.10σ). Never > 2σ from the band's near edge in any release; the model's standing tracks the Planck-low vs ACT/DESI-high split. CONSISTENT throughout.
T2 running α_s = −1.0e-3: Planck 2018 +0.52σ; ACT DR6 −1.38σ; ACT+P+SPT −1.58σ (CMB prefers slightly positive); Planck+eBOSS Lyα (−0.0108 ± 0.0022) +4.45σ — FAIL against the Lyα-driven running (shared with every slow-roll plateau model, whose running is ~−(1−n_s)²/2 ≈ −1e-3).
T3 Σm_ν = 0.0587 eV (NO floor, m1 = 0): Planck 2018 < 0.12 pass; DESI DR1 < 0.072 pass; DESI DR2+CMB < 0.0642 pass (margin 5.5 meV); DESI DR2 Feldman–Cousins < 0.053 EXCLUDED by 5.7 meV — but that bound excludes every normal-ordering spectrum (0.0587 is the NO minimum), so it is the general cosmology–oscillation neutrino tension, not a SERAPIS-specific failure. Sharpest live test: any robust bound < 0.0587 eV rules out NO and SERAPIS's AD input together.
T4 Lyα compressed (z = 3, k_p = 0.693/Mpc; eBOSS Δ²_L 0.310 ± 0.020, n_L −2.340 ± 0.006), CAMB: ΛCDM-P18 Δ²_L 0.349 (+1.96σ), n_L −2.305 (+5.84σ) [reproduces the known ~5σ CMB–Lyα tension: method check]; SERAPIS n_L −2.298…−2.303 (+6.3…+7.0σ), Δ²_L +2.1…+2.4σ. SERAPIS does NOT relieve the Lyα tension; it worsens it by 0.4–1.2σ (higher n_s outweighs the −1e-3 running, which alone shifts n_L by −0.0028 vs the needed ≈ −0.035). Same status as the T2 Lyα running. TENSION/FAIL inherited from ΛCDM + slightly worse.
T5 early halos z = 10 (Press–Schechter, estimate): n(>M) relative to ΛCDM-P18 ×1.07–1.17 (1e9 M_sun), ×1.10–1.24 (1e10), ×1.15–1.37 (1e11). SERAPIS slightly EASES the JWST bright-early-galaxy excess (by 10–40%, far short of the factors of several sometimes claimed). Running costs ~5% vs the same n_s without running.
T6 μ-distortion (estimate): ΛCDM 1.81e-8 (matches the standard ≈ 2e-8: method check); SERAPIS 1.81–1.88e-8 (+0.3…+4%). FIRAS 9e-5 far above; PIXIE-class σ(μ) ~ 1e-8 could just see the standard value, not the SERAPIS difference. CONSISTENT, null.
T7 f_NL^local = (5/12)(1 − n_s) = 0.010–0.0125 vs Planck −0.9 ± 5.1: 0.18σ. CONSISTENT; any |f_NL| ≳ 1 detection falsifies single-field.
T8 Ω_GW h² ≈ 7.1e-19 (flat; n_T = −r/8) at PTA, LISA, DECIGO/BBO frequencies: ~1e10 below the PTA signal (~1e-8), 1e5–1e6 below LISA, ~1e2 below BBO. NULL: the PTA background cannot be SERAPIS's.
T9 P_R at the end of inflation ~ ε*/ε_end × P_R* ≈ 7e-14 (estimate) ≪ 1e-2: NO primordial black holes. NULL.
T10 m_ββ (NO, m1 = 0) = 1.4–3.7 meV: below LEGEND-1000/nEXO reach (~10–20 meV). NULL.
SUMMARY: CMB-scale tests (n_s all eras, running vs CMB, f_NL, r limits) consistent; neutrino mass passes the standard DESI DR2 bound with 5.5 meV to spare; the ONE real tension is with the Lyman-α forest (n_L and the Lyα-preferred running at 4–7σ) — inherited from ΛCDM and slightly worsened, shared with all plateau models; small-scale nulls (μ, PBH, PTA/LISA GWs, 0νββ) all hold. New sharp risk identified: Lyα; if the Lyα tension proves physical rather than systematic, every slow-roll plateau model, SERAPIS included, is in trouble.

## D711 (TEST PLAN, round 2) — DESI's Lyman-α forest removes the one tension; S8 and N_eff consistent
Lock PREREG_D711; results/multiscale2_d711.txt (CAMB, same set-up as D710).
T11 DESI DR1 Lyα P1D (2601.21432; Δ²* 0.379 ± 0.032, n* −2.309 ± 0.019 at the same k* = 0.009 s/km, z = 3): ΛCDM-P18 −0.93σ / +0.22σ; SERAPIS −0.68…−0.82σ / +0.35…+0.59σ. Running: SERAPIS −1e-3 vs P1D+BAO+CMB 0.0014 ± 0.0041: −0.59σ. CONSISTENT. DESI's independent forest measurement does NOT reproduce the eBOSS slope (n* −2.309 vs eBOSS −2.340, a 1.6σ difference between the two forest measurements given their errors; DESI agrees with the CMB-ΛCDM extrapolation). So the D710 T2b/T4 "fail" rests on eBOSS alone: the Lyα tension is now most plausibly an eBOSS-specific systematic, not physics. D710's single tension is DOWNGRADED from "real" to "dataset-dependent (eBOSS only)".
T12 S8 (A_s fixed): ΛCDM 0.8309, SERAPIS 0.8323–0.8338 (ΔS8 = +0.0014…+0.0029, primordial tilt only); vs HSC+BOSS 0.8294 ± 0.0110: +0.26…+0.40σ; vs CMB 0.836: −0.17…−0.30σ. CONSISTENT; the tilt moves S8 by < 0.3σ — the S8 question (DES Y6 2.4–2.7σ vs KiDS-Legacy < 1σ, 2602.12238) is not touched by SERAPIS.
T13 N_eff = 3.044 (no dark radiation) vs ACT DR6 2.86 ± 0.13: +1.42σ. CONSISTENT.
UPDATED SCORECARD (D710 + D711): every test consistent or a holding null, except the eBOSS-only Lyα slope/running, which the newer DESI DR1 forest does not confirm.

## D712 (DEEP, theory) — The brane-interaction candidate for 1/E(U,2) hits the same sign wall as D703
Follows D709 item 3. No new searches (power counting + one symbolic check, sympy, inline; no prediction, so no lock).
1. BPS no-force (LITERATURE, standard): D3s and O3s are mutually BPS (tension = charge), so their gravitational and RR exchanges cancel and the leading-order interaction energy is ZERO. The E(U,2) dependence of D3 positions only appears at one loop (the BHK annulus), i.e. as a correction — which D709 rules out. So the D709 candidate needs a non-BPS source: an anti-D3.
2. Signs (inference from standard charges T, Q): an anti-D3 (T = 1, Q = −1) feels energy −2G Σ_j Q_j over the other sources and their images: attracted to D3s, repelled by O3⁻ (T = Q = −½). With charge cancellation (Σ_j Q_j = +1 per anti-D3) the net lattice energy is attractive.
3. Power counting (inference): with the T⁴ large compared with the T² separations, the 6D-transverse Green's function 1/r⁴ summed over T² images, |r|² = A|n + mU|²/U₂, gives Σ′ ∝ E(U,2)/A² (characteristic sums at half-periods recombine to E(U,2) by the D701 identity); the 4D Einstein-frame factor 1/𝒱₆² = 1/(A𝒱₄)² gives p = 4. The brane tension in the same frame scales as 1/A², i.e. q = 2 — so p = 2q holds and this sector WOULD produce an exact 1/E(U,2) plateau.
4. But (COMPUTED, sympy): V = aS/A⁴ + t/A² has V''(A*) = −t³/(a²S²), so the extremum is a MINIMUM only if the net tension t < 0. Numeric check: aS < 0, t > 0 → V(A*) = 0.25 > V(0.9A*), V(1.1A*): MAXIMUM; aS > 0, t < 0 → minimum. An anti-D3 adds POSITIVE net tension (D703), and its interaction is attractive (aS < 0): maximum, the area runs to collapse. Identical to D701/D703's Casimir case.
5. Side estimate (inference): the D709 half-ratio means interaction energy ≈ tension energy, i.e. separations r ~ (g_s N)^{1/4} l_s — the AdS-throat radius. Even with the right sign, the setup would sit in the warped-throat regime, not on a flat T².
VERDICT: NEGATIVE. Every two-term origin of an exact 1/E(U,s) plateau we have tried (Casimir s = 3, 5; brane interaction s = 2) needs a NEGATIVE codim-2 tension in the T², which charge-cancelled string vacua do not give (D703). The obstruction is now general and sharp, not a feature of one mechanism. 1/E(τ,2) remains an ASSUMED effective term; SERAPIS-E should be presented as an effective model with this stated gap, not as a string derivation.
Open (needs a model-building choice, not a lookup — same as D703): a genuinely negative codim-2 source (e.g. O-planes not cancelled by flux, or SUSY-breaking corrections to the GKP cancellation), or a 6D (non-string) supergravity bulk where tension sign is free.
## D713 (TEST PLAN, round 3; locked as PREREG_D712_MULTISCALE3 — renumbered because a parallel session's D712 landed first) — Dark matter removes the heavy end of the wino window; NO input favoured; birefringence unexplained
Lock PREREG_D712; results/multiscale3_d712.txt (arithmetic; window mapping by linear AMSB scaling, estimate).
T14 DARK MATTER (Fermi-LAT inner Galaxy, 2507.15934): thermal wino (2.86 TeV) as all of DM EXCLUDED (μ95 = 0.07–0.12), even with cores up to 3.7–6.7 kpc; winos 1.85–2.86 TeV excluded even as a subfraction. Our covariant-completion window (wino 0.66–2.9 TeV, "all of DM at the upper end") loses its top 30% (log): surviving wino 0.66–1.85 TeV ↔ m3/2 ≈ (2.5–7.0)e5 GeV, gluino ≈ 4.8–13.4 TeV. Below 2.8 TeV a thermal wino is underabundant ⇒ SERAPIS (covariant completion) now NEEDS a non-wino dark-matter component (e.g. an axion from another sector). Partial exclusion of an estimate-level prediction; kill condition "wino above 2.9 TeV overclosing" unaffected.
T15 COLLIDERS: wino lower end 660 GeV sits at the CMS 650 / ATLAS 660 GeV disappearing-track limits (the window's lower end was set by ATLAS); gluino ≥ 4.8 TeV vs LHC ~2.3 TeV: factor 2 margin. CONSISTENT (HL-LHC disappearing tracks will probe the low end).
T16 ORDERING: global fit with first JUNO data Δχ²(IO−NO) = 4.62 / 9.41 (without/with SK-atm; 2601.09791) → NO favoured at ~2.1–3.1σ. Our NO input is the favoured one. CONSISTENT (input, not prediction).
T17 BIREFRINGENCE: ACT+Planck β = 0.277° ± 0.057° (4.8σ from 0; 2608.06480, preliminary). The inflaton sector has no light axion (Re τ heavy at ρ) ⇒ β = 0 from SERAPIS: the signal, if real, needs a separate light axion (string compactifications generically supply C4/B2 axions). UNEXPLAINED, not contradicted.
T18 ISOCURVATURE ~1e-8 of ζ: CONSISTENT.
SCORECARD after 18 tests: CMB, LSS (DESI forest, S8), neutrinos, collider and isocurvature consistent; small-scale nulls hold; eBOSS-only forest tension (likely systematic); NEW: wino window shrinks to 0.66–1.85 TeV and DM must come partly from elsewhere; birefringence hint (4.8σ, preliminary) not explained by the model.

## D715 (AUDIT, Job 7) — TorsionΛ's background: β is exactly Ω_m in disguise, and the October parameterisation fails the CMB distance priors
(D714 skipped: consumed by a failed first run of the claim script.) Lock PREREG_D715 (AION-locked 972df42 before running); script theory/review/torsionlambda_audit_d715.py; results field_tests/results/torsionlambda_audit_d715.txt. Code audited: torsion-lambda-toolkit v0.2.0, src/physics/cosmological-distances.ts, E² = Ω_r(1+z)⁴ + Ω_m(1+β)(1+z)³ + λ.
Method check (COMPUTED): flat ΛCDM (Planck best fit) gives R = 1.7497 (−0.1σ), ℓ_A = 301.45 (−0.2σ) against the Planck 2018 compressed priors R = 1.7502 ± 0.0046, ℓ_A = 301.471 ± 0.090 (Chen, Huang & Wang 2019, arXiv 1808.05724).
1. DEGENERACY (exact, algebraic + computed): β enters E(z) only through Ω_m(1+β); (β = 0.192, Ω_m = 0.315) and (β = 0, Ω_m = 0.3755) give identical R, ℓ_A, z*. At background level TorsionΛ is flat ΛCDM with a relabelled matter density; β is not separately measurable from distances.
2. NORMALISATION BUG: with λ = 0.685 fixed, E(0) = 1.0298 ≠ 1 for β = 0.192 (the "F(a) normalisation" item from October). Renormalising λ = 1 − Ω_r − Ω_m(1+β) is required.
3. FORMULA INCONSISTENCY: the toolkit's shift parameter uses the bare p.Ωm0, not the matter actually in E; at β = 0.192 that alone moves R by −26σ (1.6307 vs 1.7804).
4. VERDICT (locked rule, case c: β = 0.192, H0 = 72.95, λ renormalised): R = 1.7804 (+6.6σ), ℓ_A = 294.73 (−75σ) → FAIL. This is the familiar statement that a ΛCDM-like background cannot move H0 to 73 while keeping the CMB acoustic scale; TorsionΛ as coded does not evade it.
Consequence for Job 7: relabel, not repair. TorsionΛ is useful as a pre-simulation consistency checker and teaching tool; its README must say that (i) β ≡ Ω_m rescaling at background level, (ii) the H0 = 73 parameterisation is excluded by Planck distance priors, (iii) the R formula should use Ω_m(1+β). Proposed README section in docs/torsionlambda/README_LIMITS.md (the toolkit repo is read-only from this session).

## D717 (DEEP, theory + computed) — The supergravity route around the tension wall, and a ghost theorem for Epstein Kähler potentials
Lock PREREG_D717 (AION-locked before running); script theory/modular/sugra_rung_d717.py; results field_tests/results/sugra_rung_d717.txt (run stopped at the first case, see 3).
Idea (going round the D703/D712 wall instead of through it): ordinary N = 1 supergravity already has a negative term with no negative-tension source — the gravitino term −3e^K|W0|². With a modular-INVARIANT Kähler potential K = −(3α/2) ln E(τ,2), a constant W0 is allowed, and V = e^K|W0|²(K^{ττ̄}|K_τ|² − 3) + V_up (V_up > 0, e.g. an anti-brane) gives a plateau V_up − (3 − 3α)|W0|² y^{−3α} at the cusp: approached from below only for α < 1, exponent p = √(6α) < √6 — so this family could never reproduce SERAPIS-E's p = 2√2 (stated in the lock).
1. COMPUTED, case α = 1/3: V is negative somewhere on Re τ = ½ and its minimum sits at y ≈ 1.93, not at ρ → NOT VIABLE under the locked rule. Asymptotics confirmed (K^{ττ̄}|K_τ|² → 1.000 = 3α at y = 60).
2. WHY (exact, analytic; checked numerically): because the Epstein series is a Laplace eigenfunction, Δ_hyp E(τ,s) = s(s−1)E, the metric of K = −ln E is
   K_ττ̄ = −s(s−1)/(4y²) + |∂_τE|²/E².
   At every critical point of E (τ = i and ρ, where ∂E = 0) the metric is NEGATIVE for s > 1: K_ττ̄(ρ) = −2/3, K_ττ̄(i) = −1/2 for s = 2 (numerical: −0.66667, −0.50000, exact). The kinetic term is a ghost exactly where the vacuum should be. (Far out it is fine: +0.00495 at y = 10 vs 1/(2y²) = 0.005.)
3. GENERAL (inference from 2): any SL(2,Z)-invariant Kähler potential K = −c ln F with F a positive Laplace eigenfunction of eigenvalue λ > 0 has K_ττ̄ = −cλ/(4y²) < 0 at F's critical points. This connects to the "Laplacian swampland" programme (D706; 2506.03253: species-scale coefficients obey D²F = ηF with η > 0): those same objects cannot serve as −ln F Kähler potentials around a fixed-point vacuum. Escape routes: eigenvalue λ < 0, i.e. 0 < s < 1 (E(τ,s) in the critical strip); or K = −ln(2y) + small invariant corrections (the BHK structure, where E stays a perturbation).
VERDICT: NOT VIABLE as posed, but the reason is a clean theorem, not a dead end. Next: test the escape 0 < s < 1 (positive metric at the fixed points; does E(τ,s) stay positive with its minimum at ρ, and what plateau does it give?).

## D718 (DEEP, computed) — The 0 < s < 1 escape fails too: the continued Epstein series is negative at the bottom of the fundamental domain
Lock PREREG_D718 (AION-locked before running); script theory/modular/strip_kahler_d718.py; results field_tests/results/strip_kahler_d718.txt.
Series check (COMPUTED): continued Fourier series vs lattice sum at s = 2 (6.5569 vs 6.5504) and s = 1.5 (9.331 vs 9.278; lattice tail slow), consistent.
Step 1 (health) FAILS for every s tested:
| s | E(ρ) | E(i) | E > 0 on Re τ = ½? | sign change at y ≈ | metric of −ln|E| at ρ (pred −s(s−1)/(4y²)) |
|---|---|---|---|---|---|
| 0.6 | −5.444 | −5.432 | no | 7.2 | +0.0800 (+0.0800) |
| 0.75 | −10.10 | −10.08 | no | 8.5 | +0.0625 (+0.0625) |
| 0.9 | −28.90 | −28.88 | no | 14.8 | +0.0300 (+0.0300) |
The metric sign flips as predicted (healthy at the fixed points), but E(τ,s) itself is negative near i and ρ, so K = −c ln E is undefined there, and −c ln(−E) blows up where E changes sign (y ≈ 7–15), a wall across the inflationary region. Reason (exact): the y^{1−s} term carries 2√π Γ(s−½) ζ(2s−1)/Γ(s), and ζ(2s−1) < 0 for ½ < s < 1, so it dominates negatively at moderate y. (s < ½ maps to 1 − s by the functional equation.)
The boundary s = 1 (Kronecker limit): K = −ln(2y|η(τ)|⁴) is modular-invariant with exactly the hyperbolic metric (ln|η|⁴ is a Kähler transformation), i.e. it IS the covariant completion W = (W0 + fX)η⁻² of D647, whose plateau is the e = 1 rung that D708 found NOT VIABLE (r ≈ 1.3e-3).
VERDICT: the Epstein-Kähler route is closed for every real s: s > 1 ghost (D717), ½ < s < 1 negative E (this note), s = 1 the known e = 1 rung. Together with the tension wall (D703, D712) and the species route (D707–D709), every mechanism tried for an exact 1/E(τ,2) plateau is excluded or sits on the e = 1 rung. Status: SERAPIS-E's plateau remains an assumed effective term; what is derived is the tilt (BHK), the vacuum at ρ, and the stuck-brane setup. Loop stopped: the next step is a model-building choice (a non-string 6D supergravity bulk with a free tension sign, or accepting the plateau as effective), not another lookup.

## D719 (CHECK, computed) — SERAPIS-E's N* bracket from the matching equation: 0.6 e-folds lower than locked
Lock PREREG_D719 (AION-locked before running); script theory/modular/nstar_check_d719.py; results field_tests/results/nstar_check_d719.txt.
Method: Planck 2018 X matching equation, N* = 67 − ln(k/a0H0) + ¼ ln(V*²/(M_P⁴ρ_end)) + (1−3w)/(12(1+w)) ln(ρ_th/ρ_end) − (1/12) ln g*, with w = 0 (heavy vacuum), k = 0.05/Mpc (ln k/a0H0 = 5.404), V* from A_s = 2.1e-9 and the model's r*, ρ_end = 1.5 V_end (V*/V_end = 1.357, y_end = 1.715), C = 1.15e-6, iterated to |ΔN| < 0.01.
| T_R (GeV) | N* | n_s | r | V*^{1/4} (GeV) |
|---|---|---|---|---|
| 1e4 | 46.29 | 0.9696 | 5.18e-4 | 4.88e15 |
| 1e6 | 47.81 | 0.9713 | 4.95e-4 | 4.82e15 |
| 1e7 | 48.58 | 0.9720 | 4.85e-4 | 4.80e15 |
| 1e8 | 49.34 | 0.9728 | 4.75e-4 | 4.77e15 |
| 1e10 | 50.87 | 0.9743 | 4.56e-4 | 4.72e15 |
VERDICT (locked rule ±0.5): INCONSISTENT at the low end — the D692 estimate (48.4–49.9 for T_R 1e6–1e8) is 0.6 e-folds too high; the computed bracket is N* = 47.8–49.3. Implied shift at fixed C: Δn_s ≈ −0.0005, Δr ≈ +1.5%. Both stay inside the frozen SERAPIS-E bands (n_s 0.970–0.975, r 4.55–5.12e-4), so lock D693 is NOT retuned; this note is the correction record (D692/D693 N* inputs should read 47.8–49.3). The T_R bracket itself is still an estimate (×m_φ^{3/2} scaling, D692) — next: compute T_R from the sterile decay widths for m_φ ≈ 2.2e13 GeV.

## D720 (DEEP; locked PREREG_D720; results/tr_rho_d720.txt + tr_rho_d720_structure.txt) — T_R at ρ: NULL by the locked method, because the Γ2 doublet's Majorana matrix is rank 1 at ρ
Computed:
- Sterility carries over to ρ: |∇(invariant mass²)|/mass² = 9e-11 at ρ (7.6e-11 at i). Diagonal inflaton → N N widths vanish at ρ, as at i (D589a). Sfermion channel ~30–70 GeV (estimate, D601 scaling), subdominant.
- The weight-2 Γ2 doublet at ρ satisfies Y₂ = i·Y₁ exactly (to 1e-16), so A(Y) is NILPOTENT (A² = 0): singular values (0.2241, 5e-17). At ρ the doublet gives ONE massive and ONE MASSLESS Majorana state, not the degenerate pair found at i (0.1508, 0.1508; D664).
- The D597 construction (eigen-decomposition, κ = |…|/s with s = √(Y₁²+Y₂²)) divides by s = 0 at ρ: κ came out 3.7e15 and the T_R grid (1e21–1e24 GeV) is meaningless. By the lock's NULL rule ("κ(ρ) cannot be computed") the T_R result is NULL; the N* run on those numbers was stopped and is not reported.
What this means (reasoning, not computed): at ρ the N splitting is maximal (ΔM/M = 1), so the D597 "λ ∝ ΔM" suppression does not apply. The off-diagonal coupling must be computed with a Takagi (SVD) decomposition, and the channel φ → N_heavy + N_massless is open whenever M < m_φ. A massless N in the doublet also means a second massless or very light neutrino state, which needs checking against oscillation data (two mass splittings need at least two massive ν). This changes D601/D602's "heavy-N doublet, ΔM/M ~ 0.1" picture for SERAPIS-E's vacuum.
Next: D721 = new lock, Takagi/SVD κ at ρ, Γ(φ → N₁N₂) with M₂ = 0, then T_R and N*.

## D721 (DEEP; locked PREREG_D721; results/tr_takagi_d721.txt) — NULL: the off-diagonal channel φ → N1 N2 is CLOSED at ρ, but the massless state's own coupling is not
Computed (Takagi residual 4e-17): M1 = 0.2241, M2 = 5e-17. Off-diagonal coupling in the Takagi basis a12 = 0 (to 1e-16), so by the locked rule the T_R result is NULL. The Kähler factor contributes no off-diagonal term (3e-17), as expected.
Observed in the same output, not yet analysed: the DIAGONAL holomorphic couplings are non-zero, |(Uᴴ ∂A U*)₁₁| = 0.259 and |(Uᴴ ∂A U*)₂₂| = 0.421. For N1 the Kähler factor can cancel the diagonal term (sterility, D589a). For the MASSLESS state it cannot: the Kähler term is ∝ A, whose (2,2) entry is 0. Reason (reasoning, not computed): M2 grows LINEARLY in |δτ| (a cone), so M2² is stationary at ρ, which is what the D720 sterility check measured, while the Yukawa δτ·N2N2 is not zero. The sterility argument (stationary invariants ⇒ no linear coupling) assumed non-degenerate, non-zero masses; it fails for a state that is massless at the fixed point.
Consequence if confirmed: φ → N2 N2 is open with an O(0.4)×(Kähler and canonical factors) Yukawa times the N mass scale over M_P, so SERAPIS-E is NOT sterile at ρ in the Γ2-doublet model, and T_R could be much higher than D692's 1e6–1e8 GeV.
Next: D722 = new lock for the φ → N2N2 width (Kähler-corrected B22, canonical normalisation, M2 = 0), T_R and N*.

## D722 (DEEP; locked PREREG_D722; results/phi_n2n2_d722.txt) — the inflaton is NOT sterile at ρ: φ → N2N2 gives T_R ≈ 7e8–7e10 GeV; D692's 1e6–1e8 bracket is superseded
Checks (computed, both pass): |B22| = 0.42077 is unchanged under the Takagi phase freedom (α = 0.3, 1.1, 2.0, to 1e-10). The massless state's mass rises linearly, M2/δ → 0.42076 at δ = 1e-5 (ratio 1.0000). The coupling is real, not a basis artefact; D720's sterility check (on M², which is stationary) could not see it.
Width (computed; overall O(1) N-kinetic prefactor not modelled, estimate): g22 = 1.33·M1/M_P, Γ = g22² m/16π.
| M1/m | 0.1 | 0.2 | 0.33 | 0.45 | 1 | 10 |
|---|---|---|---|---|---|---|
| T_R (GeV) | 6.7e8 | 1.3e9 | 2.2e9 | 3.0e9 | 6.7e9 | 6.7e10 |
N* (D719 code, C = 1.15e-6): T_R 6.7e8 → N* 49.97, n_s 0.9735, r 4.67e-4; T_R 6.7e10 → N* 51.50, n_s 0.9749, r 4.49e-4.
VERDICT (locked rule): INCONSISTENT with D692's 1e6–1e8 GeV. Correction note, no retuning of lock D693.
- n_s stays inside the frozen 0.970–0.975 over the whole range (top end 0.9749, at the edge).
- r: 4.49e-4 at M1/m = 10 falls just BELOW the frozen r band (4.55–5.12e-4). For M1 ≤ m_φ (T_R ≤ 6.7e9, N* ≲ 50.8) r ≈ 4.56–4.67e-4, inside.
- The corrected SERAPIS-E N* is ≈ 50.0–51.5 (vs locked 48.4–49.9). This is recorded, and the frozen bands are scored as locked.
New problem raised (reasoning): if Br(φ → N2N2) ≈ 1, reheating goes into a state that is massless at ρ. Unless N2 thermalises with the SM through its Dirac Yukawa (or gets a mass elsewhere), this is dark radiation, ΔN_eff ≫ 0.3: a potential kill. Also, a massless N2 in the seesaw changes the light-neutrino spectrum. Next: D723.

## D723 (CENTRE; locked PREREG_D723; results/n2_darkrad_d723.txt) — KILL for the doublet-only N sector at ρ: φ → N2N2 makes the universe dark-radiation dominated
Computed (order-of-magnitude bookkeeping; the verdict holds by many orders of magnitude):
- Neutrino bound: a massless N2 pairs with a light ν into a Dirac state of mass y_D v, so y_D < 4.0e-13 (Σm_ν < 0.07 eV).
- Thermalisation at T_R = 6.7e8–6.7e10 GeV needs y_D > 3.4e-4 – 3.4e-3, i.e. 9e8–9e9 times above the allowed value. N2 never thermalises and cannot decay (it is massless).
- Competing SM channel (D601 sfermion scaling, T_R,SM ≈ 30–70 GeV): Br_SM ≈ 1e-19 – 1e-14, so ΔN_eff ~ 1e14–1e19 vs the limit ~0.3 (ACT DR6 N_eff 2.86 ± 0.13). Anomaly and trace channels vanish at the fixed point (D601), so nothing rescues it within the doublet-only model.
VERDICT (locked): KILL for SERAPIS-E's vacuum at ρ with the Γ2 weight-2 doublet as the whole N sector.
Escape (reasoning, not computed): N2 needs a mass from extra structure, e.g. a third singlet N3 mixing with the doublet at ρ (the 2 ⊕ 1 of D664). With M2 ≠ 0 the seesaw allows y_D ≈ √(m_ν M2)/v. N2 then decays or thermalises into SM radiation if y_D ≳ 3e-4, i.e. M2 ≳ (3.4e-4 × 174)²/0.05 eV ≈ 7e7 GeV. If M2 > m_φ/2 ≈ 1.1e13 GeV the channel closes entirely. So SERAPIS-E needs an N sector beyond the bare doublet, with M2 ≳ 1e8 GeV at ρ. This is a stated condition on the model; the frozen inflation bands (lock D693) are not affected, but the reheating story (T_R, N*) now depends on that extra structure.
The paper's reheating/T_R sentences for SERAPIS-E need a caveat (not yet edited).

## D724 (CENTRE; locked PREREG_D724; results/two_plus_one_d724.txt) — MIXED: a 2 ⊕ 1 sector rescues ρ if the singlet mixes through the weight-2 doublet; the weight-4 mixing cannot
Computed (Takagi singular values; scan b ∈ {0, 0.3, 1, 3}, c ∈ {0.3, 1, 3}):
- W2 (N3–doublet mixing through the weight-2 doublet Y): rank 3 at ρ in EVERY case. Smallest/largest ratio R = 2.5e-4 (b = 3, c = 0.3) up to 0.71; for b = 0, R = 0.21–0.71, with an exactly degenerate pair (0.0475c). With M_heavy = 1e12–1e13 GeV the light state has ≳ 2.5e8 GeV, above the D723 escape bound (~1e8 GeV). RESCUE POSSIBLE.
- W4 (mixing through the weight-4 doublet (2Y₁Y₂, Y₁² − Y₂²)): rank 2 at ρ for ALL b, c (smallest SV ~1e-17). Reason (algebra, checked by the scan): at ρ, Y₂ = iY₁, so the weight-4 doublet is ∝ the null vector n = (1, −i) of A(Y), with nᵀn = 0, and it cannot lift the massless state. The KILL extends to this choice.
Weights (reasoning): consistent weights for W2 need k_N = k_N3 = −1 (2k_N + 2 = 0, k_N3 + k_N + 2 = 0). Then N3N3 needs a weight-2 SINGLET form, and Γ2 has none (its weight-2 space is the doublet). So b = 0 at leading order, unless a non-modular or higher-order source exists. b = 0 still gives rank 3 (R ≥ 0.21) but leaves an exactly degenerate pair at ρ. The Takagi phases in the degenerate b = 0 cases did not converge (residual up to 0.5), so their off-diagonal couplings are not reliable; their singular values are.
Inflaton couplings: with all masses non-zero, the stationarity theorem kills the diagonal couplings again, so sterility is restored for the non-degenerate states. Off-diagonal holomorphic couplings at ρ are O(0.01–0.9) for b > 0 (Kähler corrections for mixed weights not modelled). The reheating temperature now depends on this sector: open, next.
Paper: SERAPIS-E section updated with the D720–D724 caveat (frozen numbers kept, revision stated); builds at 13 pp.

## D725 (CENTRE; locked PREREG_D725; results/tr_2p1_d725.txt, tr_2p1_nstar_d725.txt) — the consistent 2 ⊕ 1 sector at ρ: T_R ≈ 3e8–3e9 GeV, no dark radiation, frozen bands hold
Computed (Takagi residual ≤ 3e-16; degenerate block handled with a symmetric square root, so the D724 phase failure is removed):
- The exactly degenerate light pair (0.0823 / 0.2745 / 0.8234 for c = 0.3 / 1 / 3, in model units) SPLITS LINEARLY away from ρ: rates ±0.3644, the same for all c, and matching direct δ = 1e-4 and 1e-5 shifts to < 0.1%. So the inflaton is again NOT sterile for degenerate states. This is the same cone mechanism as D722: the sum of the pair's masses is stationary, the splitting is not. The non-degenerate state's own coupling is 1e-11 ≈ 0 (theorem). The heavy–light couplings are 0.11 / 0.36 / 1.10.
- Open channels and T_R (M_heavy = 1e12 / 1e13 / 5e13 GeV; m_φ = 2.2e13):
  - c = 0.3: 3.2e8 / 3.0e9 / 2.1e9
  - c = 1: 4.3e8 / 2.5e9 / closed (M_light > m/2)
  - c = 3: 9.5e8 / closed / closed
  - Closed cases are sterile at linear order; their T_R would come from the D601-type estimate and is not computed here.
- Dark radiation: the light states have M_L = 2e11–1e13 GeV, so the seesaw allows y_D ≈ √(m_ν M_L)/v = 0.02–0.13, ≫ 3e-4 (D723). They decay to SM radiation. No ΔN_eff problem.
- N* (D719 code, C = 1.15e-6): T_R 3.2e8 → N* 49.72, n_s 0.9732, r 4.70e-4; T_R 3.0e9 → N* 50.47, n_s 0.9739, r 4.61e-4.
VERDICT (locked rule): T_R band 3e8–3e9 GeV does not overlap D692's 1e6–1e8, so INCONSISTENT as a T_R statement (correction; no retuning). But n_s 0.9732–0.9739 and r (4.61–4.70)e-4 sit INSIDE the frozen D693 bands (0.970–0.975; 4.55–5.12e-4), and N* 49.7–50.5 is only ~0.6 above the locked 48.4–49.9.
Net D719–D725 result: SERAPIS-E at ρ is consistent only with a 2 ⊕ 1 heavy-neutrino sector mixing through the weight-2 doublet. Its reheating is fast (T_R ~ 1e8.5–1e9.5 GeV, through the linear splitting of the degenerate pair). The frozen predictions survive unchanged; the paper's caveat (D724) already says the history depends on this sector.
Open: (a) leptogenesis at T_R ~ 1e9 GeV (thermal leptogenesis becomes plausible; the Davidson–Ibarra bound needs M1 ≳ 1e9); (b) the D601/D602 sterile-τ=i story should be re-checked for the same cone effect wherever degenerate states exist (D664: the doublet at i is exactly degenerate).

## D726 (DEEP; locked PREREG_D726; results/cone_i_d726.txt) — NULL by lock: at τ = i the degenerate doublet does NOT split linearly; but a pseudoscalar coupling is visible and unanalysed
Computed: doublet-only M_phys = 2y·A(Y) at i has singular values (0.3016, 0.3016) (Takagi residual 3e-16). Linear splitting rates along the imaginary axis are 0 and 0; the direct shifts are ∝ δ² (5e-5 at δ = 1e-4, 1e-5 at δ = 1e-5). The cone effect of D722/D725 is ABSENT at i. By the locked rule this is NULL, and the loop stops here. (The 2 ⊕ 1 part of the script did not run, because the script exits on NULL.)
Observed in the same output, not yet analysed: the coupling matrix in the degenerate block is purely IMAGINARY, ±0.120i on the diagonal and 0.362i off-diagonal (eigenvalues ±0.381i under the residual O(2) basis freedom). Reasoning (not computed, to be checked):
- A is traceless, so its eigenvalues are +s and −s. Takagi makes both positive with a factor i on one state, so a REAL mixing of the two eigenvectors appears as an imaginary, pseudoscalar-type coupling of size (M1 + M2)·θ′, not (M1 − M2)·θ′.
- D597 wrote the off-diagonal coupling as λ₁₂ = √2κ(ΔM/2M) (∝ splitting); for opposite-sign eigenvalues that suppression may not apply.
- A pseudoscalar Majorana Yukawa is physical (removing it by a chiral rotation leaves an axial-current coupling whose on-shell matrix element ∝ (M_a + M_b)).
- If confirmed, φ → N N at τ = i is unsuppressed (κ ~ 1), T_R ~ 1e6 GeV (the D589 c_eff ~ 0.02–0.05 range), not 1e3–1e5. That would revise D601/D602's sterile-τ=i bracket and the low-T_R arguments built on it (AD leptogenesis with a massless ν1, N* = 46–49).
Next if resumed (D727): lock a test of whether the imaginary coupling is physical. Compute Γ(φ → N N) with the correct pseudoscalar width, and cross-check by the axial-current form. Then T_R at m_φ = 1.9e11 GeV, N*, and n_s and y* against the τ = i frozen bands. The same question applies to every earlier off-diagonal width (D597, D690).

## D727 (CENTRE; locked PREREG_D727; results/pseudo_i_d727.txt) — CONFIRMED: the inflaton at τ = i is NOT sterile; an axion-like coupling to the N doublet gives T_R ≈ 1–3e6 GeV
Computed:
- Method A (Takagi): |P₁₂| = 0.190559, purely imaginary; κ = |P₁₂|/s = 1.2635, the same as D597's κ = 1.26.
- Method B (real eigenvectors, independent): A(Y) has eigenvalues ∓0.150819 (traceless), θ′ = −0.6317, (λ₁ − λ₂)θ′ = 0.190559. A and B agree to 1.2e-10, so the coupling is PHYSICAL by the locked rule.
- Analytic reason (written in the lock before running): for opposite-sign eigenvalues the off-diagonal coupling is (λ₁ − λ₂)θ′ = 2sθ′. Removing θ(φ) by a field rotation leaves a current coupling whose on-shell element is ∝ 2s, an axion-like decay to a massive Majorana pair.
- D597's λ₁₂ ∝ ΔM used |M₁| − |M₂| and is WRONG for this doublet. D601's item 2 (current couplings ∝ m₁² − m₂²) holds for same-sign masses only.
- T_R (λ = √2κ = 1.787, pseudoscalar width ∝ (1−4x²)^{1/2}, m = 1.9e11 GeV): 1.0e6 / 2.0e6 / 2.9e6 / 3.0e6 GeV for M/m = 0.1 / 0.2 / 0.33 / 0.45 (g* = 106.75); ×0.83 for g* = 228.75.
Consequences (estimates):
- Relative to the frozen bracket's T_R = 1e3–1e5: +1 to +3.5 decades, so ΔN* ≈ +0.8 to +2.7, Δn_s ≈ +0.0006 to +0.0021, Δy* ≈ +0.2 to +0.8.
- The ε = 1.3e-4 row moves to n_s ≈ 0.971–0.973. The ε = 1.6e-4 row's top end moves to ≈ 0.976 with y* ≈ 24.7–25.3, so the top of the frozen τ = i band is at risk of the y* ≤ 25 cap.
- Frozen bands are NOT retuned (lock D633/D679); the history behind them changes.
- AD leptogenesis: the required m_ν1 scales ∝ T_R, to ≈ 1e-9 – 3e-9 eV. Still "essentially massless".
- NEW OPENING: D597's leptogenesis tension came from T_R ∝ ΔM against ε ∝ 1/ΔM. With an unsuppressed decay, T_R no longer depends on ΔM, so resonant leptogenesis from φ → N₁N₂ with a quasi-degenerate pair may now work. To compute (D728).
Paper: reheating section given a correction sentence (D727); builds.

## D728 (CENTRE; locked PREREG_D728; results/lepto_i_d728.txt) — PASS: non-thermal leptogenesis from φ → N₁N₂ at τ = i works once the decay is unsuppressed
Computed (D597 conventions with the D727 T_R; maximal CP phase, Br = 1, washout neglected since T_R/M = 4–5e-5):
| M/m | T_R (GeV) | passing ΔM/M | D690 2⊕1 range (0.08 / 0.2 / 0.5) |
|---|---|---|---|
| 0.1 | 1.0e6 | 1e-8 – 0.014 | fail / fail / fail |
| 0.2 | 2.0e6 | 1e-8 – 0.15 | PASS (1.7e-10) / fail / fail |
| 0.33 | 2.9e6 | 1e-8 – 0.20 | PASS / PASS (1.65e-10) / fail (6.6e-11) |
| 0.45 | 3.0e6 | 1e-8 – 0.50 | PASS / PASS / PASS (9.4e-11) |
VERDICT (locked): PASS; NATURAL PASS for M/m ≈ 0.33–0.45 (the 2⊕1 splitting 0.08–0.2 needs no tuning to resonance). D597's NOT VIABLE is superseded: its ×7 shortfall came from the wrong T_R ∝ ΔM.
Caveats:
- ε = x/(1+x²) used far from resonance (x ~ 1e4–1e5), where ε/ε_DI = 1.3–8.3. That is the expected M/ΔM self-energy enhancement, but the regulator is not a full Boltzmann treatment.
- Maximal CP phase assumed.
- The ρ branch (D725, T_R ~ 1e9) is a separate case: thermal leptogenesis is plausible there, not computed.
Paper: the "Leptogenesis from inflaton decay fails" paragraph is corrected (D728). AD is now an alternative, not a requirement. Builds at 13 pp.

## D729 (CENTRE; locked PREREG_D729; results/chronos_tr_d729.txt) — Chronos (τ = i) at the corrected T_R: half the rows leave the frozen band
Computed (D602 machinery, only the ε and T_R loops changed):
| ε | T_R | w | N* | y* | n_s | r | in frozen band? |
|---|---|---|---|---|---|---|---|
| 1.3e-4 | 1e6 | 3/5 | 49.95 | 24.3 | 0.9733 | 4.67e-4 | NO (r < 4.8e-4) |
| 1.3e-4 | 1e6 | 0 | 48.38 | 23.8 | 0.9720 | 4.87e-4 | yes |
| 1.3e-4 | 3e6 | 3/5 | 50.31 | 24.4 | 0.9737 | 4.63e-4 | NO (r) |
| 1.3e-4 | 3e6 | 0 | 48.75 | 23.9 | 0.9723 | 4.83e-4 | yes |
| 1.6e-4 | 1e6 | 3/5 | 49.93 | 24.7 | 0.9761 | 5.14e-4 | NO (n_s > 0.975) |
| 1.6e-4 | 1e6 | 0 | 48.40 | 24.2 | 0.9747 | 5.34e-4 | yes |
| 1.6e-4 | 3e6 | 3/5 | 50.30 | 24.8 | 0.9765 | 5.10e-4 | NO (n_s) |
| 1.6e-4 | 3e6 | 0 | 48.76 | 24.3 | 0.9750 | 5.30e-4 | edge (n_s = 0.9750) |
All rows satisfy y* ≤ 25 and the D602 data rule (largest pull +1.4σ vs SPA+DESI, +2.7σ vs SPA).
VERDICT (locked rule; no retuning):
- With the corrected reheating, the frozen τ = i band (n_s 0.970–0.975, r 4.8–5.7e-4) is matched only by the matter-like (w = 0) half of the bracket.
- The stiff-phase rows (w = 3/5) leave it: low r at ε = 1.3e-4, n_s > 0.975 at ε = 1.6e-4.
- The frozen band stays as locked and is scored on future data. Where it fails, the D727 correction is the cause, recorded here.
- Physics question this raises: at T_R ~ 1e6 GeV the inflaton decays early, so does the octic (stiff) phase even last? If decay happens during the octic phase, w = 3/5 holds only until H ~ Γ. The w = 0 rows assume an immediate switch. To check (D730).
Paper: the D727 estimate sentence is replaced by these computed numbers; builds.

## D730 (CENTRE; locked PREREG_D730; results/octic_decay_d730.txt) — the stiff-phase rows are the physical ones; corrected Chronos meets the frozen band only in a narrow ε strip
Code reading: in nstarT, 'w=3/5' = octic from ρ_end to the switch ρ_x, then matter down to ρ_R; 'w=0' = matter throughout (conservative).
Computed: m = 2.28e11 / 2.65e11 GeV (ε = 1.3 / 1.6e-4); ρ_x/ρ_end = 3.4e-6 / 4.5e-6; H_x = 8.4e9 / 1.0e10 GeV. With the D727 Γ = 1.4e-6 – 1.3e-5 GeV, Γ/H_x = 1e-16 – 1.5e-15, and ρ_R/ρ_x ~ 1e-30. Decay during the octic phase is negligible (ω/H ∝ ρ^{-1/8} grows only slowly toward the switch, estimate).
VERDICT: the physical τ = i history is octic → matter → radiation, so the D729 w = 3/5 rows are physical and the w = 0 rows are only a conservative bound:
- ε = 1.3e-4: n_s 0.9733–0.9737, r 4.63–4.67e-4 — below the frozen r band (4.8–5.7e-4).
- ε = 1.6e-4: n_s 0.9761–0.9765, r 5.10–5.14e-4 — above the frozen n_s edge (0.975).
- Interpolated (estimate): the corrected history meets the frozen band only for ε ≈ 1.40–1.46e-4, at n_s ≈ 0.974–0.975, r ≈ 4.8–4.9e-4.
Status: the frozen τ = i band (lock D633/D679) stands as locked. With the corrected reheating, the model's own history now lands in its upper-n_s corner or just outside it. The lock is not retuned, and any new τ = i band would be post-hoc and scored on future data only. Comparison: SERAPIS-E (ρ, D725) stays well inside its band (n_s 0.9732–0.9739); the ρ branch is now the more robust one, as the paper already argues.
Paper: one sentence added (D730); builds.

## D731 (CENTRE; locked PREREG_D731; results/lepto_rho_d731.txt) — PASS (estimate): non-thermal leptogenesis works for SERAPIS-E at ρ with a moderate CP phase
Computed with the Davidson–Ibarra bound as ε, sin δ = 1 upper estimate, over the D725 open cases. In every case M/T_R = 500–5000, so thermal washout is negligible.
| c | M_H (GeV) | decaying state | Y_B(max) | needs sin δ ≥ |
|---|---|---|---|---|
| 0.3 | 1e12 | light 2.1e11 | 1.6e-10 | 0.56 |
| 0.3 | 1e12 | heavy 1e12 | 7.4e-10 | 0.12 |
| 0.3 | 1e13 | light / heavy | 1.5e-8 / 7.1e-8 | ≤ 0.01 |
| 0.3 | 5e13 | light 1.1e13 | 5.2e-8 | ≤ 0.01 |
| 1 | 1e12 | light / heavy | 7.1e-10 / 1.0e-9 | 0.12 / 0.09 |
| 1 | 1e13 | light / heavy | 4.2e-8 / 5.9e-8 | ≤ 0.01 |
| 3 | 1e12 | light / heavy | 1.0e-9 / 2.2e-9 | 0.08 / 0.04 |
VERDICT (locked): PASS at maximal phase in all cases. The required sin δ ranges from ≲ 0.01 (M_H = 1e13) to 0.56 (the lightest case).
Caveats:
- The exactly degenerate light pair gives no mutual resonant asymmetry. ε comes from the non-degenerate partner; the DI bound is an upper estimate, and the actual phases need a flavour model.
- Self-energy enhancement for M_L/M_H ~ 0.7 is ignored, which is conservative.
- ρ-branch status after D719–D731: viable with the 2⊕1 (W2) heavy-neutrino sector. T_R 3e8–3e9 GeV, frozen bands hold, no dark radiation, leptogenesis possible.
Next risk: gravitinos thermally produced at T_R ~ 3e9 GeV decay to winos (covariant completion: m3/2 ~ 1e5–1e6 GeV, TeV wino LSP). Non-thermal wino DM from them may overclose; to check (D732).
Paper: SERAPIS-E caveat extended (D725, D731); builds.

## D732 (CENTRE; locked PREREG_D732; results/gravitino_wino_d732.txt) — gravitino → wino: fine at the lower ρ T_R, squeezes the wino to 0.66–0.75 TeV at the upper
Computed (literature formulas as locked; Y_3/2 = 1.9e-12 T_R/1e10):
- τ_3/2 = 1.6e-3 s / 1.8e-5 s and T_dec = 14 / 127 MeV for m3/2 = 2.5e5 / 1.1e6 GeV. Both are far below wino freeze-out, and the re-annihilation cap (Y_ann 6e-12 – 5e-10) is far above Y_3/2, so every gravitino leaves one wino.
- T_R = 3.2e8 (M_H ~ 1e12 cases): Ω_total = 0.017 / 0.031 / 0.080 for M2 = 0.66 / 1.0 / 1.85 TeV. PASS over the whole window; non-thermal winos are a 10–40% DM component.
- T_R = 3.0e9 (M_H ~ 1e13 cases): Ω_total = 0.109 / 0.170 / 0.338. PASS only for M2 ≲ 0.745 TeV (arithmetic on the same formulas). In that corner non-thermal winos are ~90% of the dark matter.
VERDICT (locked): PASS with a restriction. The fast ρ reheating links the heavy-neutrino scale to the wino. M_H ~ 1e12 GeV leaves the D713 window intact, while M_H ~ 1e13 forces M2 = 0.66–0.75 TeV with winos as nearly all the DM.
Flag (from memory, NOT checked): wino DM at ~0.7 TeV making all the DM is strongly constrained by gamma-ray searches (Fermi dwarfs, H.E.S.S. Galactic Centre lines; profile-dependent). If so, the M_H ~ 1e13 corner is excluded and SERAPIS-E prefers M_H ~ 1e12 (T_R ~ 3e8). Next: search the current limits (D733).
Comparison: D651's Y_3/2 ≲ 2e-17 (old T_R 1e3–1e5) is superseded by 6e-14 – 6e-13.

## D733 (RIGHT; literature, no computation) — the M_H ~ 1e13 / T_R ~ 3e9 corner of SERAPIS-E is excluded by gamma rays (for standard profiles)
Sources:
- Cohen, Lisanti, Pierce, Slatyer, "Wino Dark Matter Under Siege", arXiv:1307.4082: "the combined H.E.S.S. and Fermi results completely exclude the non-thermal scenario" (wino = all DM) for NFW. H.E.S.S. excludes winos down to 500 GeV for NFW; Fermi dwarfs (profile-marginalised) cover lower masses. Only a ~10 kpc Burkert core (J-factor ~1e-2 of NFW) escapes.
- arXiv:2507.15934 ("Wino and Real Minimal Dark Matter Excluded by Fermi Gamma-Ray Observations", 14 yr Fermi-LAT inner Galaxy): the thermal 2.8 TeV wino is excluded even for cores up to ~6.7 kpc. Non-thermal winos are excluded from 1.85 TeV to the thermal mass even as a sub-fraction (< 50% at the lower end). The page read gives no 0.66–0.8 TeV statement. Collider disappearing tracks exclude the minimal wino below ~0.7 TeV.
- Cross-check with D713: consistent (D713 used the 1.85–2.86 TeV exclusion and kept 0.66–1.85 TeV).
VERDICT:
- The T_R ≈ 3e9 corner of D732 needs M2 = 0.66–0.75 TeV with winos ≈ 90% of the DM, i.e. effectively non-thermal all-DM winos. It is EXCLUDED for NFW and Einasto (H.E.S.S. + Fermi), and survives only for kpc-scale cores that the 2025 Fermi analysis disfavours. It is also squeezed from below by the ~0.7 TeV collider bound.
- So SERAPIS-E prefers M_H ~ 1e12 GeV (T_R ≈ 3e8). There the non-thermal winos are 10–40% of the DM and the full 0.66–1.85 TeV window passes the relic bound.
- Open: whether a 10–40% wino sub-fraction at 0.66–1.85 TeV survives the gamma-ray limits (flux ∝ f²). Needs the cross-section and limit curves (D734).
Consequence: in SERAPIS-E the heavy-neutrino scale is now tied to M_H ~ 1e12 GeV (M_light ~ 2e11–7e11), and leptogenesis then needs sin δ ≳ 0.1–0.6 (D731).

## D734 (RIGHT; literature; NULL by the tick rule) — the wino sub-fraction limits below 1.85 TeV are given only in a figure
Source: arXiv:2507.15934, text after offset 100k:
- Below 2 TeV the strongest limit is a gamma-ray LINE search at the wino endpoint (reinterpreted, Thelma profile).
- Its Fig. 6 shows two excluded regions: wino as 100% of DM (light shading) and wino as a standard thermal sub-fraction f_χ (dark shading). The text gives no numbers below 2 TeV.
- The robust statement remains: winos are excluded from 1.85 TeV to the thermal mass even as a thermal sub-fraction. Below 1.85 TeV the thermal sub-fraction is therefore not excluded.
SERAPIS-E's case sits between those two (D732, T_R 3.2e8): f_total = 0.14 / 0.26 / 0.67 at 0.66 / 1.0 / 1.85 TeV, against f_thermal = 0.05 / 0.12 / 0.41. Whether these survive needs Fig. 6's numbers, which the text does not give. Verdict: NULL (needed numbers not found in text). The DpL loop stops here.
To resume: digitise Fig. 6 of 2507.15934 (or find a table / the Ref. [91] line-search limits), then lock a f²⟨σv⟩ rescale.

## D735 (CENTRE; locked PREREG_D735; results/wino_fraction_d735.txt) — estimate: SERAPIS-E's wino must be 0.66–0.80 TeV for an Einasto Galaxy; any mass for kpc cores
Rescale (order of magnitude): H.E.S.S. 2018 line limit 4e-28 cm³/s at 1 TeV (Einasto, 1805.05741), scaled ∝ M². Wino line rate σ_γγ + ½σ_Zγ ≈ 7.1e-27 (1307.4400). Allowed fraction f_max = √(L/σ_line):
- M2 = 0.66 TeV: f_max 0.16 vs f 0.14 → PASS.
- M2 = 1.0 TeV: f_max 0.24 vs 0.26 → FAIL, marginal (× 2 uncertainty: 0.17–0.34).
- M2 = 1.85 TeV: f_max 0.44 vs 0.67 → FAIL; consistent with 2507.15934 excluding ≥ 1.85 TeV.
- Einasto passing range: M2 ≈ 0.66–0.80 TeV (≈ 0.66–1.0 within the × 2 read-off uncertainty). For kpc-scale cores (limits weaker by 1e2–1e3) every mass passes.
VERDICT (estimate): with a standard cuspy halo, SERAPIS-E at ρ (M_H ~ 1e12, T_R ~ 3e8) predicts a wino LSP at 0.66–0.8 TeV, just above the collider disappearing-track bound (~0.66–0.7 TeV). It makes up ~15% of the DM, with the rest needing another component (as D713 already said). This is a sharp, falsifiable target for HL-LHC disappearing tracks and CTA line searches. Post-hoc; scored on future data only. Caveat: the line shape and Sommerfeld mass dependence are ignored; a dedicated reanalysis (or the Fig. 6 values of 2507.15934) would supersede this.

## D736 (RIGHT; literature, no computation) — SERAPIS-E's wino window is 0.67–0.80 TeV now, and Run 3 / HL-LHC disappearing tracks will close or find it
Sources:
- ATLAS arXiv:2603.08315 (137 fb⁻¹, 13 TeV, disappearing tracks; supersedes 2201.02472). Wino-like benchmark (SM-loop splitting ≈ 160 MeV, cτ ≈ 6 cm): excluded up to 670 GeV observed, 770 GeV expected. For lifetimes ~1 ns: 880 GeV (1020 expected).
- HL-LHC projection: ATL-PHYS-PUB-2018-031 is cited in arXiv:1902.10229 §4.5, but its numbers were not in the part I read. From memory (unchecked): the pure-wino HL-LHC reach is ~0.9–1.1 TeV.
Verdict:
- The window (D735, Einasto) is 0.67–0.80 TeV, not 0.66: the lower edge moves up 10 GeV.
- The expected Run-2 sensitivity (770 GeV) already sits inside the window. A Run-2 + Run-3 combination (~3× luminosity) should cover most or all of it, and the HL-LHC reach exceeds it.
- So SERAPIS-E (ρ, standard cuspy halo) is decisively testable by ~2030: a disappearing-track signal at 0.67–0.8 TeV, or exclusion of this corner. With a kpc-cored halo the gamma-ray side relaxes and the wino can sit up to 1.85 TeV, beyond the HL-LHC reach.
Status: post-hoc; scored on future data only. prediction_sheet "falsify" line updated.

## D737 — consolidation only (docs, index, tracker; no physics). Number claimed under the wrong title; no locked computation.

## D738 (CENTRE; locked PREREG_D738; results/two_plus_one_i_d738.txt) — correction to D728: the consistent 2 ⊕ 1 sector at τ = i splits the light pair far more than D690 said; leptogenesis becomes marginal
Computed (D725 method at i):
- No degenerate states: singular values (0.025, 0.302, 0.327) / (0.186, 0.302, 0.488) / (0.302, 0.767, 1.068) for c = 0.3 / 1 / 3. Lightest-pair ΔM/M = 11.0 / 0.62 / 1.54, not D690's 0.08–0.5.
- Shifts are quadratic: no cone. Diagonal couplings are 0 (sterile). Off-diagonal |P| = 0.12–1.12, not ∝ ΔM.
- T_R ≈ 4–5e6 GeV when an off-diagonal channel is open (M_a + M_b < m). When only the diagonal lightest pair is open, the linear decay vanishes and T_R falls back to the D601 sfermion estimate (~1e2–1e3 GeV; not recomputed; the printed 1e-4 GeV is just the residual).
- Y_B (D728 formula): PASS only for c = 1, M1/m = 0.33 (9.7e-11, just above 8.75e-11). All other cases fail by ×2 up to ~1e11.
VERDICT (locked rule): INCONSISTENT with D728's "natural pass". With the doublet alone, ΔM = 0 exactly at i, so ε = 0. With the consistent 2⊕1, ΔM/M ≳ 0.6, so ε is hierarchical-size and Y_B is marginal. Leptogenesis from inflaton decay at τ = i is MARGINAL (one corner passes); AD (D646) stays the robust route at i. The ρ branch (D731) is unaffected. Paper's D728 sentence needs revision.

## D739 (CENTRE; locked PREREG_D739; results/doublet_weights_d739.txt) — at ρ only the weight-2 doublet can lift the massless heavy neutrino; b = 0 is natural there
Computed (product chain Y_{k+2} = Y ⊗ Y_k → 2, at ρ):
- k = 2: Y ∝ (1, i), overlap with the null vector n = (1, −i) is maximal; with mixing c = 1 the 3×3 matrix has rank 3. LIFTS.
- k = 4: Y₄ ∝ (i, 1) ∝ n, so nᵀY₄ = 0 (2e-32) and the rank stays 2. CANNOT lift (confirms D724).
- k ≥ 6: the chain vanishes at ρ (|Y₆| = 2e-18). Rank 1 with b = 0.
Reasoning, not computed: other weight-k doublets are products with level-1 forms (E4·Y_{k−4}, E6·Y_{k−6}). Since E4(ρ) = 0 and E6(ρ) ≠ 0, the weight-8 doublet E6·Y also lifts, while E4·Y does not. Singlet N3N3 terms need level-1 forms of weight ≢ 0 (mod 6) in the consistent assignments (weight 2: none; 14: E4²E6 = 0 at ρ), so b = 0 at ρ is generic, not tuned.
Literature: arXiv:2512.24804 (Γ2 ≅ S3 modular flavour) analyses τ = i∞ and τ = i only. It explicitly leaves the ω (≅ ρ) fixed point for future work, and its τ = i models prefer INVERTED ordering. That is a possible tension for our τ = i Γ2 completion (frozen Σm_ν assumes normal ordering), to check. I found no treatment of the rank-deficient Γ2 doublet at ω (search-only claim, one search).
VERDICT: the 2⊕1 weight-2-mixing sector with b = 0 used in D724–D725 is the minimal and natural Γ2 structure at ρ, not an arbitrary choice. Weight-4 mixing is excluded by the residual Z3 alignment, and higher weights add nothing new. Node n_sector_rho: assumed → computed (natural within Γ2; the choice of Γ2 itself is still an input).
MAP: node=n_sector_rho status=computed touches=[mnu] ripple=no

## D740 (RIGHT; literature + arithmetic, no lock needed) — mass ordering: the Γ2 "inverted ordering" result is model-specific; data favour our normal ordering
Literature (arXiv:2512.24804, read 16 Nov):
- Its IO preference comes from its texture and fit, not from S3 itself. Leptons are L = 2 with l₃, e^c as PSEUDO-singlets 1′. The τ = i Model A has N ~ 2 with k_L = k_e = k_N = −1, k_l3 = 1.
- The IO fit gives m₃ = 0, m₁ ≈ m₂ ≈ 0.049 eV. Normal ordering is set aside because it needs tan θ_e ≈ 1.7–2.6 (strong Z₂ᵀ breaking), not because it is forbidden.
- Our τ = i completion (D664) uses a different assignment: leptons 2 ⊕ 1 (trivial singlet), a full-rank Weinberg operator, and k_L = k_N = 1. The paper's ordering result does not carry over.
Arithmetic (computed, Δm²₃₁ = 2.5e-3, Δm²₂₁ = 7.42e-5 eV²):
- Minimal Σm_ν = 0.0586 eV (NO, m₁ = 0) vs 0.1007 eV (IO, m₃ = 0).
- DESI DR2+CMB gives Σm_ν < 0.0642 eV (D707 table). IO with a massless lightest state sits ~0.036 eV ABOVE that bound, so it is disfavoured by cosmology. NO passes with a +0.0055 eV margin.
VERDICT: no change to the frozen Σm_ν = 0.0587 eV (NO, m₁ ≈ 0; lock D605). Our model does not yet DERIVE the ordering: that needs the full lepton texture at ρ / i, an open item. Present data side with NO, and the IO-preferring Γ2 textures are in tension with DESI DR2.
MAP: node=mnu status=frozen touches=[n_sector_i] ripple=no

## D741 (CENTRE; locked PREREG_D741; results/ordering_d741.txt) — TENSION: the minimal D664 lepton texture at τ = i cannot give the frozen Σm_ν
Computed: m_ν ∝ [[A(Y), bY],[bYᵀ, 0]] scanned over 400 |b| × 24 phases.
- At τ = i: NO-like for 1560 of 9600 points, IO-like for 8040. Points matching the observed splitting ratio Δm²₂₁/Δm²₃₁ = 0.0297 (±10%):
  - NO: 48 points, |b| ≈ 1.4, m_light/m_heavy = 0.49, Σm_ν = 0.116 eV.
  - IO: 312 points, m_light/m_heavy ≈ 0.014, Σm_ν = 0.100 eV.
  - Both exceed DESI DR2+CMB Σm_ν < 0.0642 eV.
- At ρ (same matrix form, cross-check only): NO points matching the ratio.
VERDICT (locked rule): TENSION. The one-parameter 2⊕1 Weinberg texture of D664 does not produce a normal-ordered spectrum with a light enough lightest neutrino. The frozen Σm_ν = 0.0587 eV (lock D605) stays frozen and is scored as locked. The τ = i branch's lepton sector needs more structure: e.g. a nonzero 3-3 entry from another form, charged-lepton mixing, or the D646 Affleck–Dine requirement m_ν1 ≈ 0 imposed as a constraint. D664's "no forced massless state" already pointed this way. Caveat: one complex coefficient and the A-term normalised to 1; a texture with more free coefficients could fit, so this rules out the minimal texture only. Same IO lean as 2512.24804 at τ = i, reached independently.
Node n_sector_i stays an input, now with a known gap (the light-neutrino texture).
MAP: node=n_sector_i status=open touches=[mnu] ripple=no

## D742 (CENTRE; locked PREREG_D742; results/texture_ext_d742.txt) — RESOLVED with a singlet 3-3 entry: normal ordering and Σm_ν ≈ 0.059–0.064 eV at τ = i, about 0.5% of parameter space
Computed (fixed grids):
- (a) adding the singlet entry d: 464 of 102,400 points pass (NO, splitting ratio within ±10% of 0.0297, Σ ≤ 0.064 eV), a fraction of 4.5e-3. Best Σm_ν = 0.0592 eV; m₁/m₃ = 0.004–0.07.
- (b) a second doublet form in the 2-2 block instead: 0 of 102,400.
- (c) both: 4.0e-3, best Σ 0.0589 eV, m₁/m₃ 0.001–0.08.
VERDICT (locked rule): RESOLVED. The minimal fix is a nonzero 3-3 Weinberg entry from an allowed singlet form (reasoning: weights ≡ 0 mod 4 at i, where E4(i) ≠ 0). The τ = i lepton sector then reaches the frozen normal-ordered spectrum, at ~0.5% tuning of the grid.
Two caveats:
- Σ here is ≥ 0.0589 eV rather than exactly 0.0587, because m₁ is small but not zero; within the frozen prediction's precision.
- The Affleck–Dine requirement (D646: m₁ ~ 1e-9 eV, i.e. m₁/m₃ ~ 2e-8) is NOT produced generically; the grid's smallest m₁/m₃ is 1e-3. AD at τ = i therefore stays a tuned requirement (as D664 said), while inflaton-decay leptogenesis at i is marginal (D738). Baryogenesis at τ = i remains the weakest link of that branch; the ρ branch is unaffected (D731).
MAP: node=n_sector_i status=computed touches=[mnu, lepto_i] ripple=no

## D743 (RIGHT; literature, no computation) — no published modular baryogenesis route fits the τ = i branch's low reheating temperature
- arXiv:2604.04585 (modular fixed points, type-III seesaw): leptogenesis only at τ = (3+i)/2, 1, −1 (not i, ω or i∞). Thermal, hierarchical, strong washout, M_Σ1 ≈ 5e11–3e12 GeV, so it needs T_R ≳ 1e11. Far above our τ = i T_R ≈ 1–3e6 GeV (D727). No resonance discussed.
- arXiv:2602.03384 (modular S4, type-III, resonant leptogenesis tied to light DM): the modulus is a flavour/CP parameter only, with no inflaton role and no fixed-point dynamics.
- arXiv:2512.24804 (Γ2 ≅ S3): no leptogenesis at τ = i.
- 2405.07165 (A4 modular Dirac seesaw + leptogenesis): thermal Dirac leptogenesis, not checked in detail; it also relies on high-scale thermal production (from its abstract, unverified).
Comparison with our notes: thermal routes need T_R ≫ 1e9 GeV (Davidson–Ibarra). The τ = i branch has T_R ≈ 1e6, so only non-thermal routes remain: inflaton decay (marginal, D738) and Affleck–Dine (needs m₁ ~ 1e-9 eV, tuned, D742).
VERDICT: the literature offers no ready-made rescue. Baryogenesis stays the τ = i branch's weakest link, and the ρ branch (D731, non-thermal, sin δ ≳ 0.01–0.6) is preferred on this count too. Loop pauses here (no new computation; next real step would be a dedicated τ = i baryogenesis construction).
MAP: node=lepto_i status=estimate touches=[] ripple=no

## D744 (DEEP; literature + reasoning; first "reverse ladder" tick) — the τ = i baryon problem, worked backwards: a degeneracy breaker η_N, and radiative resonant leptogenesis as the in-model candidate
Reverse path (reasoning):
1. Target: Y_B = 8.75e-11 at T_R ≈ 1–3e6 GeV, from inflaton decay. That needs ε·Br ≈ 3e-5.
2. Obstacle: the Γ2 doublet N is exactly degenerate at τ = i, so ε = 0. The tree-level 2⊕1 mixing over-splits it (ΔM/M ≥ 0.6, D738).
3. Requirement: from D728, ANY splitting η_N = ΔM/M between ~1e-8 and ~0.1 works. Seven decades, no tuning.
4. New term: η_N, the degeneracy breaker (added to the theory map as node eta_n, upstream of lepto_i).
5. In-model candidate: renormalisation-group running from the degeneracy scale Λ to M splits an exactly degenerate pair ("radiative leptogenesis").
Literature:
- Turzyński hep-ph/0311029: two exactly degenerate N with running-induced splitting falls SHORT of the observed asymmetry in the minimal SM case.
- Branco, González Felipe, Joaquim, Nobre, hep-ph/0507092 ("Enlarging the window for radiative leptogenesis"):
  - the asymmetry vanishes at Λ (alignment, Re H₁₂ = 0);
  - running generates both the splitting, δ_N ≃ 2(H₂₂ − H₁₁)t, and the phase, through y_τ²;
  - ε⁰ ≃ (3y_τ²/32π)·Im H₂₁·Re[(Y_ν)₃₁*(Y_ν)₃₂]/[H_jj(H₂₂ − H₁₁)];
  - mixing with a THIRD heavy neutrino (θ₂ ≠ 0) is "crucial" for m₁ = 0;
  - the hierarchical light spectrum is viable for 2e-5 ≲ m₁ ≲ 3e-2 eV, largely independent of M (1e5–1e10 GeV), for thermal leptogenesis.
Fit to our τ = i setup (reasoning):
- The ingredients match. The N doublet is exactly degenerate at τ = i by symmetry, a natural Λ-scale degeneracy. A third singlet N₃ is already needed for the light texture (D742's 3-3 entry). Normal ordering with small m₁ is in their viable range.
- In the MSSM-like spectrum, y_τ² is enhanced by tan²β.
- Differences: our production is NON-thermal (T_R ≈ 1e6 ≪ M), so their thermal Y_B does not carry over directly; and the N₃–doublet MASS mixing must be absent (or small) at tree level, otherwise D738's large splitting returns.
- Rough size (estimate): ε ~ (3y_τ²/32π)·t, t = ln(Λ/M)/16π² ≈ 0.16, y_τ ≈ 0.01·tanβ, gives ε ~ 5e-7·tan²β, i.e. ~1e-5 – 5e-5 for tanβ ≈ 5–10. The right range for the non-thermal requirement (~3e-5).
VERDICT: a promising, in-model route. It needs no added symmetry breaking, only the model's own running plus a third heavy neutrino it already has. To compute next (D745, locked).
MAP: node=eta_n status=estimate touches=[lepto_i] ripple=no

## D745 (CENTRE; locked PREREG_D745; results/radlepto_d745.txt) — PASS: radiative resonant leptogenesis rescues baryogenesis at τ = i
Computed (Casas–Ibarra grid of 729 complex R; NO; alignment Re H₁₂ = 0 at Λ = 1e16 GeV; literature ε formula of hep-ph/0507092; non-thermal yield at T_R = 2.9e6 GeV, M = 6.3e10, N₃ = 10M):
| m₁ (eV) | tanβ = 5 | tanβ = 10 | tanβ = 20 |
|---|---|---|---|
| 1e-4 | 34% pass (max Y_B 9e-10) | 70% (3.5e-9) | 86% (1.4e-8) |
| 1e-3 | 36% (1.2e-9) | 68% (4.6e-9) | 84% (1.8e-8) |
| 5e-3 | 38% (1.4e-9) | 65% (5.4e-9) | 83% (2.2e-8) |
δ_N < Γ_N/M (where D_j = 1 fails) in only 1–3% of points.
VERDICT (locked rule): PASS. ≥ 10% of the grid passes already at tanβ = 5, the moderate tanβ the superpartner chain prefers.
- The exact degeneracy the residual symmetry imposes at τ = i, which made ε = 0 in D728/D738, is broken by the model's own running (η_N ~ δ_N = 2(H₂₂ − H₁₁)t). The τ-Yukawa running supplies the phase.
- No tuned m₁ ≈ 1e-9 eV is needed, so Affleck–Dine is no longer required at τ = i. m₁ = 1e-4 – 5e-3 eV keeps Σm_ν ≈ 0.059–0.064 eV, still consistent with D742 and the frozen value.
Caveats: leading-order analytic ε (not a full RGE integration); upper estimate with signs aligned; MSSM y_τ = m_τ/(v cosβ); a third heavy N₃ with no tree mass mixing to the doublet is required (consistent with weight choices, not derived here).
Reverse-ladder record: target Y_B → requirement η_N ∈ [1e-8, 0.1] → new term η_N → in-model source (RG running) → PASS. The same path as ρ's "hidden effect" rescues (D722, D725, D727).
MAP: node=eta_n status=computed touches=[lepto_i] ripple=no
MAP: node=lepto_i status=computed touches=[] ripple=no

## D746 (DEEP; reverse ladder; reasoning + 2 searches, no computation) — what the SERAPIS-E plateau needs, stated as one term; no in-string source found yet
Target: V/V₀ = 1 − E(ρ,2)/E(τ,2), i.e. a constant V₀ (uplift) minus a NEGATIVE term ∝ 1/E(τ,2), which → e^{−2√2φ} on the plateau.
Requirement (reasoning). Three ways to get the shape:
- (i) An F-term piece −3e^K|W|² with |W|² ∝ E(τ,2)^{−1}. For a gaugino condensate this means a gauge kinetic function with a threshold f ⊃ (1/2a)·ln E(τ,2), the "Epstein threshold".
- (ii) A negative term ∝ g²(τ) with Re f dominated by a one-loop piece β·E(τ,2) at large Im τ.
- (iii) A ratio of invariants from the Kähler side: closed (Epstein-Kähler ghost, D717/D718).
New term named: the Epstein threshold, a ln E(τ,2) (or E(τ,2)-linear) contribution to a gauge kinetic function, distinct from the DKL threshold ln(2y|η|⁴), which is the s → 1 (Kronecker) member and gives the ρ-variant/covariant shapes, not E(τ,2).
Literature (2 searches):
- Non-holomorphic Eisenstein series of the axio-dilaton appear in type IIB higher-derivative couplings (E(τ,3/2), E(τ,5/2) for R⁴, D⁴R⁴; Green–Gutperle line; 0807.0389, 1001.2535). On T², E(U,s) appear in one-loop amplitudes.
- The one-loop D3/D7 annulus gives E(U,2) in the KÄHLER potential (Berg–Haack–Körs; our tilt C).
- I found no source giving ln E(U,2) or E(U,2) in a gauge kinetic function. Option (ii) is also numerically weak: β ~ 1e-3, E ~ 2e2 at horizon exit, so βE ~ 0.2 ≪ Re S ~ 4.
VERDICT: the requirement is now sharp: one negative-energy term scaling as E(τ,2)^{−1}. But no in-string source is known (search-limited claim). Node plateau_origin stays OPEN. This is the model's main unexplained input, together with ε at τ = i (eps_tilt). Next real step: a direct computation of D3-brane gauge thresholds at the half-periods (whether the annulus that gives E(U,2) in K also gives ln E(U,2) in f) is a research project, not a loop tick. Loop pauses.
MAP: node=plateau_origin status=open touches=[] ripple=no

## D747 (CENTRE; locked PREREG_D747; results/halfperiod_thresholds_d747.txt) — gauge thresholds from D3 stacks at the half-periods cannot make the plateau
Computed (U = ½ + iy, y = 2–20):
- ϑ₂ϑ₃ϑ₄ = 2η³ holds to 1e-30. With equal stacks at the three half-periods, the combined gauge threshold is U-INDEPENDENT (holomorphic part).
- Single-stack thresholds are LINEAR in y: ln|ϑ₃/η|² = ln|ϑ₄/η|² = πy/6 exactly, and ln|ϑ₂/η|² ≈ −πy/3 + ln 4. A condensate built on them therefore gives potentials ∝ e^{−c·y}, while the SERAPIS-E plateau needs a POWER law 1/E(U,2) ∝ y^{−2} (E(U,2) grows as y²: 55, 217, 425 at y = 5, 10, 14).
Source of the threshold form: Berg–Haack–Körs hep-th/0404087 eqs. 40/44, where a stack at Wilson line A gives −ln|ϑ₁(A,U)/η|² plus a non-holomorphic πU₂a₄², which is also linear in U₂.
VERDICT (locked rule): route (i) of D746, a gauge-threshold condensate from this brane setup, is EXCLUDED. A power law in U₂ comes naturally only from Kähler/volume factors, and the Epstein-Kähler route is closed (D717/D718). The plateau term remains an assumed effective term. Reverse-ladder status: requirement known (D746); two candidate sources ruled out, Kähler (D717/D718) and gauge thresholds (D747); no third in-model source in sight. The loop stops here: a natural pause.
MAP: node=plateau_origin status=open touches=[] ripple=no

## D748 (LEFT; literature + arithmetic; outward check) — if the DESI-driven n_s shift is an artefact, the frozen n_s band still holds within ~1.8σ of every CMB-only fit
New literature:
- arXiv:2512.05108 ("The spectrum of n_s constraints from DESI and CMB data"): the upward n_s shift when DESI BAO is added is driven by the BAO–CMB tension, through the n_s–ω_m/r_d·h degeneracy. DESI acts much like a prior on τ.
- Ferreira et al., PRD Feb 2026 (Kavli IPMU press release, 23 Mar 2026): the shift "may be a statistical artefact". The evidence against standard inflation models "weakens significantly" once the tension is accounted for, and which n_s is most reliable is unclear.
Computed (distance from the frozen band 0.970–0.975):
| Data | n_s | distance |
|---|---|---|
| Planck | 0.9638 ± 0.0040 | 1.55σ |
| ACT | 0.9666 ± 0.0076 | 0.45σ |
| SPT | 0.948 ± 0.012 | 1.83σ |
| CMB-SPA | 0.9693 ± 0.0029 | 0.24σ |
| P-ACT | 0.9709 ± 0.0038 | inside |
| Planck+DESI | 0.9690 ± 0.0035 | 0.29σ |
| ACT+DESI | 0.9767 ± 0.0068 | 0.25σ |
| SPA+DESI | 0.9737 ± 0.0025 | inside |
VERDICT: the frozen bands (τ = i, ρ, SERAPIS-E: n_s 0.970–0.975) are within 1.83σ of every combination, with or without DESI. If DESI's pull is an artefact, the CMB-only centre (~0.964–0.969) sits just below the band, a mild pressure (≤ 1.6σ for Planck), not a fail. The untilted Kairos (0.959–0.961) would then be competitive again. These data are pre-freeze: consistency only, not scored. Decisive tests stay SO + SPHEREx (~2030) and LiteBIRD r.
MAP: node=band_e status=frozen touches=[band_i] ripple=no

## D749 (LEFT; literature + arithmetic; outward check) — r ≈ 5e-4 cannot be tested by any planned experiment this decade; n_s, α_s and the wino carry the near-term tests
Literature:
- SPT-3G two-year B-modes (arXiv:2505.02827): r < 0.25 (95%), σ(r) = 0.067 from SPT-3G alone over the BK field. The best combined limit remains BICEP/Keck-class, r ≲ 0.03–0.04 (from memory; not re-checked this tick).
- Simons Observatory forecast with delensing and foreground cleaning (arXiv:2405.01621, Table III, 5 years): σ(r=0) = 1.2e-3 (simple foregrounds), 2.3–2.4e-3 (realistic).
Arithmetic:
- Our r ≈ 5e-4 (τ = i 4.8–5.7e-4; SERAPIS-E 4.55–5.12e-4) is 0.2–0.4σ for SO, so undetectable.
- The frozen kill condition "r < 2.4e-4 at 95% CL" needs σ(r) ≈ 1.2e-4, ~10–20× better than SO. LiteBIRD's target total uncertainty is ~1e-3 (from memory), also short.
VERDICT: the r prediction is a long-horizon test (post-2035, needs a successor to SO+LiteBIRD; CMB-S4 is no longer planned, from memory). Near-term decisive tests are n_s with SO+SPHEREx (~2030, D705), the Janus α_s relation, and the post-hoc wino window at Run 3 / HL-LHC (D736). D705's "r at LiteBIRD, optimistic" wording should read "r beyond LiteBIRD's reach at 2σ". Paper and prediction-sheet wording to check next session.
MAP: node=tests_cmb status=literature touches=[band_e, band_i] ripple=no

## D750 (CENTRE; reverse ladder; locked PREREG_D750; results/falsifiers_d750.txt) — the near-term falsifiers are in the neutrino sector, not r
Reverse path: target "a test before 2035". r fails (D749). What tonight's results fix instead is the neutrino spectrum: NO, with m₁ bounded below by the radiative-leptogenesis grid (D745, ≥ 1e-4 eV) and above by cosmology.
Computed (PMNS from memory; Majorana phases scanned 72×72):
| m₁ (eV) | Σm_ν (eV) | m_ββ (meV) | m_β (meV) |
|---|---|---|---|
| 0 | 0.0586 | 1.4–3.7 | 8.8 |
| 1e-4 | 0.0587 | 1.4–3.7 | 8.8 |
| 1e-3 | 0.0597 | 0.8–4.4 | 8.9 |
| 5e-3 | 0.0652 | 0.1–7.5 | 10.1 |
- DESI DR2+CMB (Σ < 0.0642 eV) caps m₁ < 4.36e-3 eV (computed). D745's top grid value (5e-3) is therefore just excluded, and the viable τ = i window is m₁ ≈ 1e-4 – 4.4e-3 eV.
New falsifiers (sensitivities from memory, labelled):
1. Neutrinoless double beta decay: predicted m_ββ ≤ 7.5 meV, below the next-generation reach (~10–20 meV for LEGEND-1000 / nEXO / CUPID). Prediction: NO signal in those experiments. A confirmed signal with m_ββ ≳ 10 meV would falsify the normal-ordering/small-m₁ branch, unless a non-standard mechanism contributes.
2. β-decay mass: m_β ≈ 9–10 meV, below KATRIN (~0.3 eV) and the Project 8 goal (~40 meV). Prediction: null.
3. Cosmological Σm_ν: 0.0586–0.064 eV. With σ ≈ 0.015–0.02 eV around 2030 (DESI final + Euclid + CMB), this predicts a 3–4σ DETECTION of nonzero neutrino mass. A robust bound Σ < 0.058 eV kills NO with any m₁ ≥ 0, and the model with it. Of the three, this is the sharpest near-term test, and current DESI trends (preference for low Σ) make it live.
Status: consistent with the frozen Σm_ν = 0.0587 (lock D605), which sits at the low end of the computed range. The m_ββ and m_β ranges are post-hoc derived statements and enter the prediction sheet as "derived, not frozen".
MAP: node=mnu status=frozen touches=[lepto_i] ripple=no

## D751 (LEFT; reverse ladder; literature + arithmetic; results/discriminant_d751.txt) — by 2030 only n_s itself separates SERAPIS from plain attractors; the running α_s cannot
Target: a 2030-era signal that tells SERAPIS from a generic e^{−2√2φ}/Starobinsky-type attractor.
Forecasts (arXiv:2212.04115, Table 5; the caption says 95% intervals, the text says σ, so both readings are shown): SO+SPHEREx σ(n_s) = 0.0016, σ(α_s) = 0.0024; the best combination (LiteBIRD + CMB-S4 + CHIME + SPHEREx) gives 0.0012 and 0.0017.
Computed:
- Plain attractor n_s = 1 − 2/N*, α_s = −2/N*²: N* = 50 / 55 / 60 gives n_s = 0.9600 / 0.9636 / 0.9667 and α_s = −8.0 / −6.6 / −5.6e-4.
- SERAPIS-E: n_s 0.970–0.975, α_s −(9.4–10.6)e-4.
- n_s separation from the N* = 55 attractor (band edge 0.970): 4.0σ (SO+SPHEREx) to 5.3σ (best combination); twice that under the 95% reading. Against the N* = 60 attractor (0.9667), only 2.1σ (4.1σ under the 95% reading).
- α_s separation: SERAPIS − attractor ≈ −(3–5)e-4, i.e. 0.1–0.3σ. Correction to the printed script line: it used 3.9e-4 for the attractor α_s; the right value is 5.6–8.0e-4, which makes α_s even less discriminating.
VERDICT: the running α_s (and so the Janus relation, which also needs r) is NOT a 2030 discriminant. The discriminant is n_s itself: if SO+SPHEREx centre n_s near 0.972, plain untilted attractors (and our own Kairos, 0.959–0.961) are excluded at ≳ 4σ, while a long-reheating attractor at N* ≈ 60 survives at ~2σ. SERAPIS's distinctive content (the tilt and its modular origin) is therefore tested by n_s plus the neutrino and wino predictions (D750, D736), not by α_s or r. Together with D749 this sets the model's test calendar: ~2027–2030 Σm_ν (cosmology) and wino (LHC); ~2030 n_s (SO+SPHEREx); 2030s 0νββ null; r and α_s beyond the 2030s.
MAP: node=tests_cmb status=literature touches=[] ripple=no

## D749a (correction note to D749) — LiteBIRD's reach for r
D749 called LiteBIRD's reach "also short" (from memory). The repo's prediction sheet (D705) records two LiteBIRD numbers: the mission REQUIREMENT δr < 1e-3 (total), under which r ≈ 5e-4 is invisible, and an optimistic forecast σ(r) ≈ 5e-5 for an r = 0 fiducial, under which it would be seen at ~10σ. Correct statement: r ≈ 5e-4 is below the SO reach and below LiteBIRD's requirement level; it is detectable only if LiteBIRD reaches its optimistic forecast (results ≳ 2035). The paper's sentence ("requires σ(r) ~ 1e-4, beyond the currently planned experiments") is the requirement-level reading and stays as is; the sheet already shows both. No edit needed. Ladder flags band_i and band_e cleared.

## D752 (LEFT; reverse ladder; locked PREREG_D752; results/attractor_kination_d752.txt) — a plain attractor cannot reach the SERAPIS n_s band, even with the longest reheating gravitational waves allow
Reverse path: D751 left one competitor alive, an attractor at N* ≈ 60. Ask what it needs to reach n_s = 0.970 (N* = 2/(1 − n_s) ≈ 67), and whether that history is allowed.
Computed (estimates as labelled in the lock):
- Instant reheating gives N* = 55.15 (attractor n_s = 0.9637).
- A kination phase raises N* by (1/12)·ln(ρ_end/ρ_k), but makes the primordial GW spectrum blue (∝ f). With r = 5e-4 and ΔN_eff < 0.2, the allowed enhancement caps ρ_end/ρ_k ≈ e^81, so kination must end by T ≈ 2e6 GeV.
- Then ΔN* ≤ 6.8, N* ≤ 61.9, attractor n_s ≤ 0.9677. Robust: 0.9676–0.9679 for Ω_GW,flat ×3 or ÷3.
- Separation from SERAPIS: the band edge 0.970 is 1.4σ above the attractor maximum (SO+SPHEREx, 1σ reading; 2.9σ under the 95% reading). For a central n_s = 0.972 it is 2.7σ / 5.4σ.
VERDICT: n_s ≥ 0.970 is out of reach of any plain e^{−2√2φ}/Starobinsky-type attractor with a standard or kination reheating, by the GW ΔN_eff bound. An SO+SPHEREx measurement centred at ≈ 0.972 would favour a TILTED plateau like SERAPIS over every plain attractor at ~3–5σ, even allowing the most extreme reheating. This sharpens D751 and turns n_s into the model's main 2030 discriminant. Caveats: Ω_GW,flat and the ΔN_eff → Ω_GW conversion are from memory (×3 tested); other ways to raise n_s (e.g. other plateau shapes, non-minimal attractors) are not excluded by this.
MAP: node=tests_cmb status=computed touches=[band_e, band_i] ripple=no

## D753 (CENTRE; reverse ladder; locked PREREG_D753; results/eps_candidates_d753.txt) — no in-model small number gives the τ = i tilt; at ρ, a two-loop-sized coefficient is a weak lead
Computed: 28 physical candidates (15 single quantities + loop factor × each), spanning 5e-10 to 0.17.
- τ = i (target ε = 1.45e-4): 0 hits within ×2.
- ρ (target 6e-5): 3 hits — L² = (1/16π²)² = 4.0e-5; √A_s = 4.6e-5; L·|η(ρ)|²⁴ = 3.0e-5.
- Look-elsewhere: with 28 candidates over ~20 decades, the chance of ≥ 1 accidental hit is ≈ 0.84. Hits are numerology unless the functional form also matches.
Form check (reasoning):
- √A_s is an OUTPUT of the model (the normalisation), so it is circular. Rejected.
- L·|η(ρ)|²⁴: the needed tilt shape at ρ is the DKL threshold L = −ln(2y|η|⁴) itself, not a power of η. No structural reason. Rejected.
- L² × (DKL threshold): a tilt ε_ρ = b′·(1/16π²)² with b′ = 1.5, an O(1) number, replacing D687's unnatural one-loop b ≈ 0.01. Physically: the universal one-loop threshold entering the uplift sector through one further loop (e.g. the X-sector coupling to the threshold-corrected gauge kinetic function arises at one loop). The functional form (L) is unchanged, so it is form-consistent. WEAK LEAD only: the high look-elsewhere chance, and no derivation of the second loop.
VERDICT: eps_tilt stays an assumed input at τ = i (no candidate). At ρ there is a plausible reinterpretation: a two-loop-sized coefficient, b′ ≈ 1.5. SERAPIS-E's tilt is already derived (C from Im S·Im ρ ≈ 190–245N, D692), so the τ = i ε is the branch's open input, not the model's. Loop pauses (no strong lead).
MAP: node=eps_tilt status=assumed touches=[] ripple=no

## D754 (DEEP; reasoning + arithmetic; results/rho_tilt_volume_d754.txt) — deeper on D753: the ρ-variant tilt fits the same one-loop-over-volume mechanism that DERIVES SERAPIS-E's tilt
Reverse path: D753 left "a two-loop-sized coefficient" (ε_ρ ≈ 1.5·(1/16π²)²) as a weak lead. Deeper question: is there a mechanism the model already uses that makes a one-loop factor times a SECOND small number? Yes. SERAPIS-E's tilt is a one-loop Kähler correction divided by moduli volumes, C = 15N/(64π⁶ Im S·Im ρ) (Berg–Haack–Körs; D692).
Apply the same structure to the ρ variant (reasoning): its tilt function is the universal one-loop DKL threshold L = −ln(2y|η|⁴). If L enters the Kähler potential the same way (a one-loop correction suppressed by Re S·Im ρ_vol; the Green–Schwarz/threshold-type term, form from memory), then ε_ρ = δ/(16π²·Re S·Im ρ_vol).
Computed:
- ε_ρ = 6e-5 needs (Re S·Im ρ_vol)/δ = 106.
- SERAPIS-E needs Im S·Im ρ = 188–244 (×N) for its derived C.
- The τ = i value (ε = 1.45e-4) would need 44, but its I₁ is not a standard threshold function, so the analogy does not apply there.
VERDICT (reasoning, labelled): the ρ tilt is naturally sized if it is a one-loop, volume-suppressed Kähler correction with the DKL function. The required volume product (~1e2) matches the SERAPIS-E value to within ×2–4 (the two differ only by O(1) normalisation, N and δ). The ρ variant and SERAPIS-E then share one tilt mechanism (one loop ÷ ~100–250 volume units), and the D687 "unnaturally small coefficient" problem disappears for ρ. This upgrades D753's weak lead to a STRUCTURAL lead. Still to do:
- (a) confirm in the literature that the DKL/GS one-loop term enters K with a 1/(Re S·Im ρ) suppression in a type-IIB orientifold with branes at the half-periods;
- (b) recompute ρ's n_s, r with ε tied to the SERAPIS-E volume product (a joint prediction instead of two free tilts).
τ = i's I₁ tilt stays unexplained, one more reason the paper calls ρ the better-motivated vacuum.
MAP: node=eps_tilt status=estimate touches=[vac_rho, serapis_e] ripple=no

## D755 (CENTRE; locked PREREG_D755; results/joint_tilt_d755.txt) — the ρ tilt tied to the SERAPIS-E volume comes out ×2 too small with δ = N = 1; the structural lead survives only with δ/N ≈ 2
Literature (a): the hep-th/0508043 excerpt I read does not show the N = 1 one-loop K formulas (eqs. 3.46, 4.3 were not reached). Its introduction says the D3/D7 one-loop corrections are "suppressed for large values of the volume", but whether the DKL function itself enters K with 1/(Im S·Im ρ) is UNCONFIRMED. The heterotic Green–Schwarz form (from memory: K ⊃ −ln(S + S̄ + δ_GS/8π²·L)) has no volume factor; it would give ε ≈ δ_GS/(16π² Re S) ≈ 3e-3·δ_GS, ~50× too large for O(1) δ_GS.
Computed (b), D613 machinery, only E changed:
- E = 2.6e-5 and 3.4e-5 (tied, δ = N = 1, X = 244 / 188): n_s 0.9631–0.9676, r 3.7–4.4e-4. Below the frozen ρ band (0.969–0.972); 1.9–3.6σ low vs SPA+DESI in most rows.
- E = 6e-5 (fitted): n_s 0.9691–0.9723, r 4.6–5.1e-4. Reproduces D613 (check passed).
VERDICT: the tied relation with δ = N = 1 under-tilts by ×2. It works only with δ/N ≈ 1.8–2.3, an O(1) factor but a fudge until the one-loop K normalisation is known. The D754 lead is therefore downgraded to "same order of magnitude, normalisation open"; it is not a joint prediction.
Caveat: D613's reheating bracket (T_R 1e3–1e5) predates today's corrections. A higher T_R (the ρ heavy sector gives fast reheating, D725, though for SERAPIS-E's m_φ) raises N* and n_s by ~0.0008 per e-fold, which would close part of the gap. To recheck if this line is pursued. Loop pauses: the next step needs the full BHK N = 1 formulas (read eqs. 3.46/4.3 of hep-th/0508043 at offset ≥ 100k).
MAP: node=eps_tilt status=estimate touches=[] ripple=no

## D756 (DEEP; literature, deeper at the D755 wall) — the IIB one-loop Kähler potential contains ONLY Eisenstein E₂ functions: SERAPIS-E's tilt is the natural one, and the ρ variant's DKL tilt has no loop origin there
Read (hep-th/0508043, text beyond offset 180k):
- Eq. (3.46), T⁶/(Z₂×Z₂): K⁽¹⁾ = ½Σ_I c·ℰ₂(A_i^I, U^I)/[(S−S̄)(T^I−T̄^I)] + ½Σ_I c·ℰ₂(0, U^I)/[(T^J−T̄^J)(T^K−T̄^K)]. ℰ₂ are spin-structure/orbifold sums of E₂(A, U).
- Eq. (4.3), T⁶/Z₆′: the same structure, with ℰ₂^{(2,P/W)}(0, U²) ∝ E₂(0, U²).
- The N = 1 result "cannot" be absorbed into ln K⁽⁰⁾. In the visible text NO ln(Im U|η|⁴) (DKL) term appears in K.
Consequences:
1. The D754/D755 lead is CLOSED for the IIB setting. The ρ variant's tilt L = −ln(2y|η|⁴) is not produced by the one-loop Kähler potential. It stays a fitted ε (D687), and its natural home would be heterotic (Green–Schwarz), where D755 showed it is ~50× too large.
2. SERAPIS-E's tilt is the IIB-natural one: Ê ∝ E₂(0,U) is exactly the second-term function, and E₂(A,U) at the half-periods is the first.
3. New detail for SERAPIS-E: the E₂(0,U) term is suppressed by the OTHER two Kähler moduli, 1/[(T^J−T̄^J)(T^K−T̄^K)], with no S. The tilt coefficient C therefore receives two contributions, C ≈ c₁/(Im S·Im T^I) + c₂/(Im T^J·Im T^K). D692's Im S·Im ρ ≈ 190–245N is then "the effective volume product". The frozen bands are unchanged (they depend on C only), but the microscopic reading is broader.
VERDICT: going deeper at the wall resolved it, by elimination: in IIB orientifolds the one-loop tilt is E₂-shaped. SERAPIS-E is the derived branch, while the ρ variant (DKL) and τ = i (I₁) tilts are fitted inputs. This supports the paper's choice to present SERAPIS-E as the derived branch; one caveat sentence to add there (the two suppression channels for C).
MAP: node=bhk_tilt status=literature touches=[serapis_e, eps_tilt] ripple=no

## D757 (CENTRE; locked PREREG_D757; results/inverse_metric_d757.txt) — the loop-corrected inverse Kähler metric does not make a plateau; the BHK term can only tilt
Computed:
- Δ_hyp E(τ,2) = 2.0000·E at y = 1, 2, 5. So K_{UŪ} = (1 + 2c′E)/(4y²) > 0 for c′ > 0: no ghost.
- With W = W₀ and the other moduli no-scale, V ∝ e^{c′E}[K^{UŪ}|K_U|² − 1]/(2y) along Re U = ½:
  - c′ = 1e-4: monotonic, no flattening, c′E ≤ 0.18 up to y = 29.
  - c′ = 1e-3: a shallow extremum near y ≈ 15–17, where c′E ≈ 0.5–0.6; beyond it V turns over and grows.
  - c′ = 1e-2: an exponential runaway (e^{c′E}) once c′E ≳ 1.
- No region has V approaching a constant while c′E ≤ 0.3. The y²/E → const (approach y^{−3}) behaviour of the inverse metric needs c′E ≳ 1, where e^{K⁽¹⁾} is no longer a small correction (non-perturbative in the loop expansion).
VERDICT (locked rule): NO. In its perturbative regime the BHK loop term changes V only by a factor (1 + O(c′E)), i.e. a TILT. That is exactly SERAPIS-E's use of it (D692), and it cannot also supply the plateau. Plateau-origin routes now closed: Casimir/tension (D703, D712), species (D707–D709), Epstein-Kähler (D717, D718), gauge thresholds (D747), loop-corrected inverse metric (D757). The plateau stays an assumed effective term.
Wall status: the in-model routes are exhausted. Going deeper now means leaving the model, e.g. non-perturbative (instanton) or warped-throat sources of a 1/E term, a separate project. Loop pauses.
MAP: node=plateau_origin status=open touches=[] ripple=no

## D758 (DEEP, outward; locked PREREG_D758; results/logderiv_epstein_d758.txt) — a log-derivative (species-type) Epstein plateau
Reverse-ladder step: the wall at D757 says the plateau cannot come from a loop correction to K. Working backwards from "a plateau that tends to a constant", 2407.12081's species-scale potentials have the form V ∝ G^{ττ̄}|∂ ln Λ_sp|², and with Λ_sp tied to E(τ,2) this gives, along Re τ = ½, V ∝ y²(d ln E/dy)².
Computed: V(ρ) = 5.5e-38 (zero at the vacuum, as needed); E(ρ) = 5.7833593 (matches D689). V → 4 as y → ∞, with the approach ∝ y^{−3} (read from the printed values: 4 − V = 0.163, 0.021, 0.0026 at y = 5, 10, 20). Untilted α = 1, N* = 48: n_s = 0.95842, r = 1.92e-4.
Errors recorded: the script's "approach exponent" and "1 − V/V∞" lines used V∞ = 1 instead of 4 and are wrong. "V(i)" was evaluated at y = 1 on Re τ = ½, which is not τ = i. The mpmath slow-roll was too slow and was stopped. D759 supersedes the n_s/r numbers.
VERDICT: a plateau shape with the right vacuum, but untilted n_s ≈ 0.958–0.962 is below the band. The tilt is needed (D759).
MAP: node=logderiv_plateau status=computed touches=[plateau_origin] ripple=no

## D759 (DEEP; locked PREREG_D759 + DEVIATIONS D1; results/logderiv_tilted_d759.txt; run1 kept as INVALID) — log-derivative plateau + SERAPIS-E BHK tilt
Model: V = y²(d ln E/dy)²·(1 + C(E − E(ρ))) along Re τ = ½. Run1's nested finite differences gave noisy n_s; D1 (written before the rerun) switched to mpmath derivatives. The C = 0 rerun reproduces D758 exactly (n_s 0.958418 at N* = 48).
Computed (N* = 48 / 50 / 52):
- α = 1 (y* 16.5–22.7):
  - C = 0: n_s 0.9584/0.9601/0.9616, r 1.9/1.8/1.6e-4.
  - C = 5e-7: n_s 0.9660/0.9679/0.9697, r 2.4/2.2/2.1e-4.
  - C = 1e-6: n_s 0.9741/0.9763/0.9783, r 3.0/2.8/2.7e-4.
  - C = 1.15e-6: n_s 0.9767/0.9789/0.9811.
  - C = 1.3e-6: n_s 0.9793/0.9816/0.9839.
  - C = 2e-6: n_s 0.992–0.998.
  - C = 4e-6: n_s 1.04–1.05 (excluded).
- α = 1/3 (y* 11.5–12.2): the tilt barely moves n_s (0.958 → 0.968 at N* = 48 for C = 4e-6). The band is reached only at C ≈ 3.2–3.9e-6 for N* = 50–52, with r ≈ 6.8–7.2e-4.
Band, interpolated in code: for α = 1, n_s 0.970–0.975 needs C = 7.5e-7–1.05e-6 (N* 48), 6.2–9.2e-7 (N* 50) or 5.2–8.1e-7 (N* 52), with r = 2.1–3.1e-4. That is the same order as SERAPIS-E's derived C ≈ 1.0–1.3e-6 (D692), but slightly lower.
VERDICT (locked rule): CANDIDATE. A natural C (≪ 4e-6) puts n_s in the band with y* ≤ 25 (α = 1). It is a post-hoc second plateau form, distinguished from SERAPIS-E by r: ≈ 2.1–3.1e-4 vs 4.55–5.12e-4. The α = 1/3 version is marginal (band only at the edge of natural C) and has a high r of about 7e-4.
Caveats:
- The plateau's origin still needs the species/Laplacian coefficient ratio A ≪ B·E, which D707 judged not generic. 2407.12081 is agnostic about why Λ_sp tracks E. This is a candidate form, not a derivation.
- The frozen bands are unchanged.
- A precise r (SO/BICEP σ(r) ~ 1e-3 cannot; LiteBIRD-class σ(r) ≲ 1e-4 could) separates the two.
MAP: node=logderiv_plateau status=computed touches=[plateau_origin, serapis_e] ripple=no

## D760 (DEEP, reverse; literature, no computation) — what would make the species scale track E(τ,2)? Nothing known does
Reverse step from D759. The candidate V ∝ y²(d ln E/dy)² needs a species number N_sp ∝ E(τ,2) (Λ_sp² ≃ M_P²/N_sp), with E the same non-holomorphic weight-2 Epstein function as the BHK tilt.
Literature (2407.12081, fetched): the paper's own species number is NOT E(τ,2).
- It uses N ≃ −6 log[2τ₂|η|⁴] + Ñ₀ (eqs 2.6–2.7, 4.3; Ñ₀ = 25 in their numerics), from the genus-one topological free energy F₁ of type IIA on the Enriques CY (K3×T²)/Z₂, an N = 2 setting.
- ∂N ∝ G̃₂, the almost-holomorphic weight-2 form, which vanishes at i and ρ.
- Its potential is V = K²|τ₂G̃₂|²Λ⁴ (eq 1.5), with a Starobinsky-like large-τ₂ limit (eq 4.10).
- The only Eisenstein series in it is E_{3/2} for 10D IIB (Λ⁶ = 1/E_{3/2}). Species-scale functions in lower dimensions (2310.07213) are R⁴ coefficients: E_{3/2} for the axio-dilaton and Ê₁ = −π log(Im τ|η|⁴) for the T² structure. Neither is E(τ,2).
Deduction (requirement → term): the D759 form would need a higher-derivative gravitational coupling whose moduli-dependent coefficient is E(U,2). New term "E₂-species": an N = 1 orientifold R² coefficient built from the same annulus/Möbius N = 2 sectors as BHK. By the D747/D756 pattern, the moduli dependence those sectors give to holomorphic-anomaly-type couplings (gauge thresholds, F₁-like) is log η (DKL/Ê₁) type, while E₂ appears in the Kähler potential. That is an inference from memory, not checked against a computed R² amplitude.
VERDICT: WALL. No known string coupling makes the species scale track E(τ,2).
- The D759 candidate keeps its numbers, but its plateau has no microscopic source. Label: phenomenological, post-hoc.
- The literature's version is a different model: the F₁ (log η) species plateau of 2407.12081. It lives in an N = 2 IIA setting, while the BHK tilt is N = 1 IIB. Grafting one onto the other mixes settings, so it is not pursued.
Deeper next: an explicit N = 1 orientifold R² threshold, to test the inference above. It is a known-type string amplitude, a separate project; the loop pauses here.
MAP: node=logderiv_plateau status=assumed touches=[plateau_origin] ripple=no

## D761 (RIGHT; literature, no computation) — 2507.15934 Fig. 6: method matches D735; the paper states no exclusion of a sub-fraction wino below 1.85 TeV
Source (2507.15934v2 html, read in two of three parts): for m_χ < 2 TeV the paper switches from its Fermi continuum search to a re-interpretation of a gamma-ray line search at the endpoint E ≈ m_χ (Fig. 6). The signal is suppressed by f_χ². Two profiles are used: Einasto and the more conservative "Thelma". HESS Galactic Centre line limits and Fermi dwarfs each rule out a 100% wino. For a thermal sub-fraction the stated exclusion is only 1.85 TeV up to the thermal mass, where the wino is < 50% of the DM at the lower end.
Comparison with D735: the same f² line-limit logic, consistent at 1.85 TeV. SERAPIS-E's wino is non-thermal (from gravitinos), with f ≈ 0.14–0.17 at 0.67–0.80 TeV. That is about 2–3× the thermal sub-fraction (m/2.86 TeV)² ≈ 0.055–0.08, so the paper's thermal-fraction shading does not apply directly. The Fig. 6 values are not in the text and cannot be digitised here.
VERDICT: no change. The window 0.67–0.80 TeV (Einasto, estimate) stands, and is not excluded by any stated limit. Digitising Fig. 6 is still open; it needs the figure image (Danny could save it, or it waits for the PC).
MAP: node=wino_window status=estimate touches=[] ripple=no

## D762 (REVERSE, ρ-side; Jl tick 1; locked PREREG_D762; results/cp_phase_rho_d762.txt; postulate P1) — the inflaton line Re τ = ½ is CP-conserving, so the leptogenesis phase at ρ cannot come from τ
Reverse step: D731's PASS needs sin δ ≥ 0.01–0.56. Requirement: a CP phase in the heavy-ν sector during reheating. Source search:
- Literature (1905.11970 §4.3, fetched): with generalised CP plus modular invariance, the CP-conserving τ are the imaginary axis and the boundary of the fundamental domain, including Re τ = ±½ (CP maps ½+iy → −½+iy = T⁻¹-equivalent). In the symmetric basis all couplings are then real (§4.1).
- Consequence [derived from the literature statement]: SERAPIS-E rolls along Re τ = ½ and ends at ρ, which lies on that line. With gCP, ε = 0 exactly at every stage of inflation and reheating. D731's PASS therefore silently assumed CP violation in the couplings.
- No source fixes these phases inside the model, so I wrote POSTULATE P1 (theory/derivations/POSTULATES.md): no gCP; coupling phases independent and uniform.
Computed under P1 (K4 regression passed): P(|sin δ| ≥ s_min) across the nine D731 cases runs from 0.62 (c = 0.3, M_H = 1e12, light state) to 0.99. The median is 0.95, and 8/9 cases have P ≥ 0.9.
VERDICT (locked rule): NATURAL under P1. Branch status:
- ρ-leptogenesis is now CONDITIONAL. It passes naturally if the flavour sector breaks CP explicitly (P1), and fails if gCP is imposed. In that case it needs another baryogenesis source (AD, or a CP phase from a second modulus off its CP locus).
- The paper's D731 text should state this condition (one sentence; Danny's call).
Mirror question (forward, i-side, next tick): τ = i is also CP-conserving (imaginary axis). Does D745's radiative resonant leptogenesis at i likewise rely on non-gCP couplings? If yes, is P1 needed on both branches, and what does P1 predict for the low-energy Dirac phase δ_CP (DUNE/Hyper-K)?
MAP: node=lepto_rho status=assumed touches=[lepto_i] ripple=no

## D763 (FORWARD, i-side; Jl tick 2; locked PREREG_D763; results/delta_cp_i_d763.txt) — τ = i leptogenesis needs P1 too; P1 makes no δ_CP prediction, but gCP does (δ ∈ {0, π}), so DUNE/Hyper-K test the CP structure
Computed on the D745 set-up (NO, m₁ = 1e-3 eV, tanβ = 10). K4 regressions: (A) at δ = 230° reproduces D745, 68.2% pass with max Y_B 4.64e-9; (B) at δ = 0 gives Y_B = 0.
- (A) Complex R (high-energy phases): pass fraction 71.3 / 68.3 / 67.5 / 68.2 / 68.3% for δ_CP = 0 / 90 / 180 / 230 / 270°. The spread is 3.8 points, under the 10-point rule, so there is NO δ_CP dependence.
- (B) Real R, with CP only in the PMNS phase: 0 of 1728 points pass for every δ. Max Y_B ≤ 2e-25, which is numerical noise.
- Reason [derived]: H = Y†Y = √D R†·diag(m)·R √D / v_u², so U cancels. Im H₂₁ = 0 for real R whatever δ is, and the radiative ε ∝ Im H₂₁ vanishes. This is the standard decoupling of unflavoured leptogenesis from the low-energy phases.
VERDICT (locked rule):
- D745's PASS rests on complex R, i.e. on high-energy CP phases in the heavy-ν couplings, which P1 supplies. τ = i is CP-conserving (imaginary axis), so with gCP, R is real, ε = 0 and δ ∈ {0, π}.
- Both branches therefore need P1. lepto_i is now conditional, like lepto_rho (D762).
Forward prediction (new, post-hoc structure statement):
- SERAPIS + gCP (either vacuum) predicts δ_CP ∈ {0, π} AND no leptogenesis.
- SERAPIS + P1 predicts generic δ_CP (no preferred value) AND viable leptogenesis.
- A DUNE/Hyper-K discovery of leptonic CP violation (sin δ ≠ 0 at ≥ 3–5σ, late 2030s) would exclude the gCP completion for both vacua and favour P1. A firm δ ≈ 0/π would exclude only half of P1's phase space at |sin δ| < 0.1 (about 6% of a uniform prior), so it does not kill P1. Current fits allow both.
Correction to P1's falsifier (ii): a δ_CP ≈ 0/π measurement only weakly disfavours P1. The sharp test is the reverse: CP violation discovered ⇒ gCP excluded.
MAP: node=lepto_i status=assumed touches=[lepto_rho] ripple=no

## D764 (REVERSE, ρ-side; Jl tick 3; locked PREREG_D764; results/second_modulus_cp_d764.txt) — P1 retired: a second modulus fixed by the flux relation U₁U₂ = b₃/a⁰ (2405.18813) supplies the CP phase at ρ for most flux ratios
Deep research:
- 2405.18813 (fetched). U₁ stabilised at ω (≅ ρ) plus the flux relation U₁U₂ = b₃/a⁰ fix U₂ off the CP locus. CP violation is "readily induced" when b₃ ∤ a⁰ and a⁰ ∤ b₃. Example a⁰ = 2, b₃ = −3 gives U₂ = 3/4 + (3√3/4)i.
- 2004.04518 (fetched): fluxes alone have flat directions joining CP-even and CP-odd vacua. Spontaneous CP violation needs an extra lifting, e.g. matter couplings, which is what 2405.18813 provides.
Computed (CP test: j(U₂) real ⇔ CP-conserving). K4 regressions: s(i) = 0, j(ρ) = 0, s(0.1 + 1.3i) = 0.49, and the paper's example gives s_CP = 0.98 (CP-violating, as stated).
- Over 46 distinct ratios |b₃/a⁰| (a⁰ ≤ 6, |b₃| ≤ 12), 63% have s_CP > 0.1, with median s_CP = 0.77.
- The 17 CP-conserving cases are exactly the integer and 1/integer ratios, matching the paper's divisibility statement.
VERDICT (locked rule): P1 REPLACED by P2. P2 takes the mechanism from the literature and postulates only the assignment of the heavy-ν couplings to U₂.
- Leptogenesis on both branches now has a concrete CP source: a non-divisible flux ratio.
- With U₁ = i (τ = i branch) and weight 6, 2405.18813 finds Re U₂ = 0, i.e. no CP violation. So the i-branch would need U₁ = i with a different weight or relation. Not computed here; it goes to the queue.
- Still assumed (P2 open), but the postulate is narrower and has falsifiers.
Mirror question (forward, next tick): if U₂ = (b₃/a⁰)/U₁ holds DURING inflation, U₂ moves with the inflaton. Derive the effective kinetic term (−ln Im U₂ is a modular image of −ln Im U₁, so it adds the same hyperbolic metric, i.e. α → α + 1?) and the change in n_s and r for SERAPIS-E. Alternatively, is the relation only imposed at the minimum (heavy U₂ direction)?
MAP: node=lepto_rho status=assumed touches=[lepto_i, serapis_e] ripple=no

## D765 (FORWARD, i-side; Jl tick 4; locked PREREG_D765 + DEVIATIONS D1–D2; results/flux_rel_inflation_d765.txt, run1 CRASH kept) — CORRECTION: if P2's flux relation ties U₂ to the inflaton, SERAPIS-E leaves its frozen bands (r doubles)
Derivation: with U₂ = c/U₁, −ln Im U₂ = −ln Im U₁ + (Kähler transformation), so K_eff = −2 ln Im U₁. The metric doubles and y = e^{φ} replaces e^{√2φ}.
Deviations: D1 corrected the solver's field map; D2 moved the start to y = 13 after run 1 overflowed (numerical only; both written before reruns).
Computed (same MS solver and grid as D692):
- C = 0: n_s 0.9615 / 0.9626, r 6.90 / 6.52e-4 at N* 48.4 / 49.9 (y* ≈ 10.1–10.2).
- C = 1.0e-6: n_s 0.9639 / 0.9651, r 7.36 / 6.98e-4.
- C = 1.3e-6: n_s 0.9647 / 0.9659, r 7.51 / 7.13e-4.
- vs D692 (single metric) at C = 1.3e-6: n_s 0.9731 / 0.9746, r 5.12 / 4.92e-4.
Analytic check: N ≈ ζ(4)y²/(2k²) and ε ≈ 1/(8k²N²), so k² = 2 → 1 doubles ε. Untilted r goes 3.75 → 6.90e-4 (×1.84; the tilt and the exact solver account for the rest), and y* 13.8 → 10.1 (√2 is 1.41; got 1.37). Consistent.
VERDICT (locked rule): CORRECTION.
- With the flux relation enforced during inflation, no natural C keeps both bands. The tilt moves n_s only ~2.5e3 per unit C (E is smaller at y* ≈ 10). Reaching n_s 0.970 needs C ≈ 3.4e-6, where r ≈ 8.5e-4, above the frozen r band (4.55–5.12e-4) and the 8.3e-4 cap.
- So P2 in its strong form ("U₁U₂ = b₃/a⁰ with U₁ the inflaton") CONFLICTS with SERAPIS-E. The frozen bands are untouched.
Viable P2 variant to test next (reverse): put the flux relation on two moduli that are NOT the inflaton (U₂U₃ = b₃/a⁰ with U₂ at its own fixed point), so U₁'s metric stays single.
Alternatively, the relation is lifted by a mass below H_inf, but then U₂ is light during inflation (isocurvature risk; F4).
MAP: node=serapis_e status=frozen touches=[lepto_rho] ripple=no

## D765a (correction to D765's MAP line)
D765's MAP line set node serapis_e to status=frozen, which changed it from "computed". That was a labelling error: SERAPIS-E's bands are locked (D693) but post-hoc, and the node's status was never "frozen". This note restores it; D765's physics is unchanged.
MAP: node=serapis_e status=computed touches=[] ripple=no

## D766 (REVERSE, ρ-side; Jl tick 5; locked PREREG_D766; results/p2_tadpole_d766.txt) — P2 on non-inflaton moduli works only with U₂ = ω, and it fits the tadpole only if SERAPIS's stuck branes drop from 5/5/5+1 to 3/3/3+1
Literature (2405.18813, fetched):
- n_flux = −2f·a⁰b₃ (eq 3.25), with bound n_flux = 32 − 2n_D3 − n_O3′ (eq 3.8).
- CP violation needs b₃ ∤ a⁰ and a⁰ ∤ b₃. The smallest such case is a⁰ = 2, b₃ = −3, f = 1, so n_flux = 12 (eq 4.14).
- Odd flux quanta need exotic O3′ planes (their App. A).
Computed:
- U₂ = i: U₃ = −(b₃/a⁰)/i = i·(b₃/a⁰) is purely imaginary, so j is real and s_CP = 0 for all 46 flux ratios. CP-conserving always [derived and computed; agrees with 2405.18813's weight-6 statement].
- U₂ = ω: 63% of ratios give s_CP > 0.1, median 0.77 (reproduces D764).
- Tadpole: n_flux = 12 ⇒ n_D3 ≤ 10. D698's 5/5/5 + 1 (16) does NOT fit. 3/3/3 + 1 = 10 saturates it exactly (12 + 20 = 32). At fixed C, Im S·Im ρ rescales to 225–732, which keeps weak coupling and moderate volume. 2/2/2(+1) fits with 150–488 only if extra flux or mobile branes fill the remainder.
VERDICT (locked rule): VIABLE, with conditions.
- P2 = the third torus's U₃ sits off the CP locus via U₂U₃ = b₃/a⁰ with U₂ = ω, and the heavy-ν couplings depend on U₃.
- The microscopic picture changes: 3/3/3 + 1 stuck D3s, replacing 5/5/5 + 1 (D698's tilt mechanism, the fixed-point asymmetry, is kept; only N changes).
- Caveats:
  - odd b₃ needs exotic O3′ planes, and n_O3′ > 0 would shrink the D3 room below 10;
  - the next even CP-violating option (a⁰ = 4, b₃ = −6, f = ½, n_flux = 24) leaves n_D3 ≤ 4, i.e. 1/1/1 + 1 with Im S·Im ρ 75–244 (marginal);
  - that U₁ can stay out of W_flux in this flux restriction is an estimate (torus-permutation symmetry), not checked in the paper.
- Applies to BOTH branches (U₁ = i or ρ is the inflaton; CP comes from U₃).
Tool fix: ladder.py now reads letter-suffixed correction notes (D765a); new test, 5/5 pass. Frozen nodes stay protected (by design), so D765a's manual map fix stands.
Mirror question (forward, next tick): with N = 3 instead of 5, does anything frozen move? Check D698/D692: C = 15N/(64π⁶ Im S Im ρ) is fixed by the band, so only the inferred Im S·Im ρ moves. Also the gravitino/wino chain (m₃/₂ depends on the volume, D732–D736): recompute the volume implied by Im S·Im ρ 225–732 and check that the wino window 0.67–0.80 TeV holds.
MAP: node=lepto_rho status=assumed touches=[lepto_i] ripple=no

## D766a (correction to D766's Im S·Im ρ)
D766 rescaled the summary range 375–1220 by N/5 and got 225–732. That was wrong. D696's tilt is set by N_eff = N − N0, not N, and 375–1220 was a union of the full- and half-unit cases. Correct (D767, computed): (N, N0) = (3, 1) gives N_eff = 2 and Im S·Im ρ = 375–488, or 188–244 if a stuck brane counts as half a D3 unit. Still weak coupling and moderate volume, but the half-unit case is getting low. D766's other statements (U₂ = ω only; n_flux = 12 saturates with 3/3/3 + 1) stand.
MAP: none

## D767 (FORWARD, i-side; Jl tick 6; locked PREREG_D767; results/n3_downstream_d767.txt) — 3/3/3 + 1 halves N_eff; the wino window and the frozen bands do not move
Computed:
- Tilt (D696 formula): K4 reproduces (5, 1) → 750–975. With (3, 1) + 6 flux units (n_flux = 12), N_eff = 2 and Im S·Im ρ = 375–488 (half-unit variant 188–244). This corrects D766 (see D766a).
- Wino chain: by inspection of the inputs, T_R comes from the heavy-ν sector (D725: M_H, c), m₃/₂ from the phenomenological window (gluino and wino bounds), and M₂ = 2.7e-3·m₃/₂ from anomaly mediation. None depends on N or Im S·Im ρ. Regression: D732 and D735 rerun unchanged, with outputs identical to the committed files.
VERDICT (locked rule): the wino window (0.67–0.80 TeV, Einasto, post-hoc) is UNCHANGED, and so are the frozen SERAPIS-E bands (C is fixed by the band; only the inferred Im S·Im ρ moves). D766a written.
Note for the paper/state doc: "Im S·Im ρ ≈ 375–1220" becomes 375–488 (or 188–244) if the P2 CP mechanism is adopted. That is a modelling choice to state, not a frozen change.
Mirror question (reverse, next tick): the stale wall plateau_origin (D760). Under the no-stop rule: deep research on non-perturbative or warped sources of a 1/E(τ,2) term. If none, write POSTULATE P3 for the plateau term with explicit falsifiers. Budget β3: P2 is open, so P3 would make 2 (allowed).
MAP: node=lepto_rho status=assumed touches=[] ripple=no

## D768 (REVERSE, ρ-side; Jl tick 7; literature, no computation) — the plateau wall: no string computation gives 1/E(τ,2), but the anti-D3 "geometric" framework can carry it; postulate P3
Deep research:
- 2408.05203 (Kallosh–Linde et al., SL(2,Z) cosmological attractors; fetched). Plateau potentials are built from j, Ê₁ = −π ln(Im τ|η|⁴) and G̃₂, with K = −3α ln(−i(τ − τ̄)). The minimum is at e^{2πi/3} (≅ ρ) and τ = i is a dS saddle for the j-based potentials. Predictions are α-attractor: n_s = 1 − 2/N, r = 12α/N².
  - The paper claims NO string derivation. Its supergravity embedding is D3̄-induced geometric inflation, i.e. a nilpotent field X whose metric G_XX̄(τ) is CHOSEN to give V.
  - It uses only Ê₁ (log η), never E(τ,s) with s ≠ 1, the same pattern as D760.
- 2411.07552 (Landscape of Modular Cosmology) and 2509.02632 (swampland review): listed, not fetched (budget).
- Anti-D3 / warped throat (2202.05344, 1707.07059 listed): the moduli dependence of the uplift is through warping and volume. I found no 1/E(U,2) dependence (search-only claim).
Wall status: no microscopic source of the 1/E(τ,2) plateau, consistent with D703–D757 and D760. Create (no-stop rule): POSTULATE P3 (theory/derivations/POSTULATES.md). The plateau is the anti-D3 nilpotent sector with K^{XX̄}(τ) ∝ V(τ) + 3|W0|².
- This is the SAME level of origin as the published SL(2,Z) attractors (chosen G_XX̄), so SERAPIS-E is no worse off than the literature, but not better.
- What SERAPIS-E adds beyond them: the E(τ,2) choice ties plateau and tilt to one function, and the tilt has a loop origin (BHK, D692).
Comparison: with SERAPIS-E's single −ln metric (y = e^{√2φ}, i.e. 3α = 1), 2408.05203's formula r = 12α/N² = 4/N² gives 1.6–1.7e-3. SERAPIS-E's exact r is 3.5–3.8e-4 untilted, because its plateau approach is 1/E ∝ y⁻² = e^{−2√2φ}, not e^{−√2φ}. So the E(τ,2) plateau sits a factor ~4.5 below the j/Ê₁ attractors in r: a distinguishing feature, consistent with the D700–D702 r-ladder.
Mirror question (forward, next tick): the axion Re τ is exponentially flat during inflation (x-dependence ∝ e^{−2πy}, y* ≈ 14, as 2408.05203 §7 also notes). Compute, with the 2-field metric, whether a trajectory starting at x₀ ≠ ½ ends at ρ, and the size of ∂N/∂x₀ near x₀ = ½ and at generic x₀. Then the induced ζ from δx ~ √2·y*·H/2π versus 5e-5 (isocurvature / f_NL test of P3).
MAP: node=plateau_origin status=assumed touches=[serapis_e] ripple=no

## D769 (FORWARD, i-side; Jl tick 8; locked PREREG_D769 + DEVIATIONS D1–D2; results/axion_two_field_d769.txt, run1 INVALID kept) — the light axion adds ζ ≲ 1e-7 (passes), but the locked verdict is FAIL on a mis-specified end criterion; the post-inflation relaxation to ρ is untested
Computed (two-field background, D692 plateau form, C = 1.15e-6, start y = 25):
- K4: N_total(x₀ = ½) = 109.0902263, equal to the single-field D692 background (109.0902263, checked separately with the D692 code). PASS.
- N_total(x₀) − N_total(½): +4.4e-8 (0.49/0.51), +1.1e-5 (0.45), +4.3e-4 (0.4), +1.6e-3 (0.3), +4.3e-3 (0.1). x hardly moves during inflation (0.1 → 0.1004), and y_end = 1.297–1.306.
- ∂N/∂x₀ = −4.3e-3 at 0.45 and −1.4e-2 at 0.3. With δx = √2·y*·H/2π = 7.4e-6: ζ_axion = 3.2e-8 at 0.45 and 1.0e-7 at 0.3, i.e. ≤ 0.2% of ζ in amplitude, ≤ 4e-6 of the power.
- At ½: ∂²N/∂x² = 0.088, so the second-order δN is 2.4e-12 (f_NL contribution negligible).
VERDICT (locked rule): FAIL. The ζ part PASSES by a factor ≥ 10 (1.0e-7 ≤ 1e-6), but the second criterion, "|x_end − ½| < 0.05 at the end of inflation", fails for x₀ ≤ 0.44, because the axion has not yet relaxed when ε = 1.
- The criterion was mis-specified: it tested x at ε = 1, while the question is where the field settles AFTER inflation. That is a design error in the lock, recorded here. The verdict is not changed, and the test is not rerun with a new rule.
- The post-inflation relaxation (does a trajectory ending at x ≈ 0.1–0.4, y ≈ 1.3 fall into ρ, or near the τ = i saddle?) is a NEW question, D770, with its own lock.
Physics so far: for SERAPIS-E the axion's curvature contribution is negligible across x₀ ∈ [0.1, 0.9]. This supports the paper's axion statement (made for τ = i), now for ρ.
MAP: node=serapis_e status=computed touches=[plateau_origin] ripple=no

## D770 (REVERSE, ρ-side; Jl tick 9; locked PREREG_D770; results/axion_relax_d770.txt) — PASS: after inflation every axion start settles at ρ (or an image); none sticks at the τ = i saddle
Computed (two-field, cosmic time, Hubble friction; final position read when the energy first falls below 1e-4·V_end):
- x₀ = 0.5, 0.45, 0.4, 0.3, 0.2, 0.1, 0.05, 0.02 → all RHO. The reduced final positions lie within 0.003 of ρ or ρ′ = −½ + i√3/2 (an image).
- K4: x₀ = ½ stays at x = ½ exactly.
- Its read-out point y = 0.288 is the ST-image of ρ's neighbourhood along x = ½ (½ + iy ↔ y′ = 1/(4y) = 0.869). The field oscillates through images of ρ on the line x = ½. Not LOST (bound y < 0.2).
- Even x₀ = 0.02, next to the i-saddle line x = 0, falls into a ρ image.
VERDICT (locked rule): PASS. Together with D769's ζ_axion ≤ 1.0e-7, P3's axion falsifier is cleared. The light Re τ neither spoils the curvature spectrum nor traps the field away from ρ, for any start x₀ ∈ [0.02, 0.98] (by x → 1 − x symmetry).
This closes the question D769 left open. The paper's axion paragraph can now cover SERAPIS-E as well as τ = i (one sentence).
Mirror question (forward, next tick): P3 at the β3 limit. Test or retire P2 or P3 next. Candidate: P2's falsifier "exotic O3′ planes needed for odd b₃ are inconsistent with the stuck-brane torsion model". Literature check on O3′ (exotic O3-plane) charges in T⁶/(Z₂×Z₂) with discrete torsion (hep-th/0602038, 2405.18813 App. A), plus the tadpole arithmetic with n_O3′ > 0.
MAP: node=serapis_e status=computed touches=[plateau_origin] ripple=no

## D766b (correction to D766's brane configuration)
D766 placed 3/3/3 + 1 stuck D3s with n_flux = 12 and no exotic planes. But odd flux quanta (b₃ = −3) need exotic O3′ planes (2405.18813 App. A), so that configuration is not allowed as stated. The allowed configuration is in D771: 2/2/2 + 0 with 8 O3′. N_eff = 2 in both, so D766a's Im S·Im ρ = 375–488 is unchanged.
MAP: none

## D771 (FORWARD, i-side; Jl tick 10; locked PREREG_D771; results/o3prime_d771.txt) — P2 survives in one configuration: odd flux n_flux = 12, 8 exotic O3′ planes spread evenly, stuck D3s 2/2/2 + 0
Literature (2405.18813 App. A, fetched): odd flux quanta need exotic O3′ planes, which enter as n_flux + 2n_D3 + n_O3′ = 32. The paper gives no O3′ charges, counts or compatibility with D3 branes. With only even quanta the non-divisibility condition is hard to meet under the bound.
Computed (enumeration; O3′ placed evenly over the inflaton torus's 4 fixed points, n_O3′ ≡ 0 mod 4, so they add no U-asymmetry; mobile D3s count in N0):
- n_flux = 12 with n_O3′ = 8: n_D3 = 6, the unique (N, N0) = (2, 0), N_eff = 2, Im S·Im ρ = 375–488 (half-unit 188–244). The ONLY allowed configuration.
- n_flux = 12 with n_O3′ = 4, 12, 16 or 20: no placement with N_eff ≥ 1.
- n_flux = 24 (all-even fluxes): no placement with N_eff ≥ 1 for any n_O3′. Even fluxes leave too little D3 room for a tilt.
VERDICT (locked rule): P2 SURVIVES, restricted to a single configuration: a⁰ = 2, b₃ = −3 (n_flux = 12), 8 exotic O3′ planes (two per fixed point of the inflaton torus), stuck D3s 2/2/2 at the half-periods with none at the origin, N_eff = 2.
Caveats (not checked):
- whether exotic-plane consistency (Frey–Polchinski-type: the exotic types are set by the flux's parity through each fixed point, from memory) allows exactly this even 8-plane placement for these fluxes;
- whether stuck D3s (hep-th/0602038) can sit at fixed points that carry an O3′;
- uneven O3′ placements would add their own U-asymmetry to the tilt (not computed).
These are P2's sharpest remaining falsifiers, recorded in POSTULATES.md.
Mirror question (reverse, next tick): source the exotic-plane rules. Deep research on O3-plane types (O3⁻, Õ3⁻, O3⁺, Õ3⁺), their D3 charges, and how odd H₃/F₃ quanta fix which fixed points carry exotic planes (Frey–Polchinski hep-th/0201029; Hanany–Kol; Witten "baryons and branes"). Then test whether "two exotic planes per inflaton fixed point" is consistent with a⁰ = 2, b₃ = −3. If yes, P2 stays; if no, P2 is retired (freeing β3), and ρ-leptogenesis falls back to P1-type explicit CP.
MAP: node=lepto_rho status=assumed touches=[] ripple=no

## D772 (REVERSE, ρ-side; Jl tick 11; literature + locked PREREG_D772; results/pure_ns_d772.txt) — P2 RETIRED: 2405.18813's Model I ties every complex-structure modulus (τ₁τ₂ = −3/2 AND τ₃ = S), leaving no free inflaton; new postulate P4 (pure-NS flux) keeps the inflaton free and has tadpole room
Literature:
- 2405.18813 Model I, full flux vector (fetched): F₃ = 2α₀ − 3β³, H₃ = −2α₃ − 3β⁰, so W_flux = (τ₃ − S)(2τ₁τ₂ + 3). The SUSY Minkowski conditions fix τ₁τ₂ = −3/2 AND τ₃ = S.
- Frey–Polchinski (hep-th/0201029, ar5iv, partly read): O3 planes with no discrete flux have D3 charge −¼; with discrete NS, RR or both, +¼. An odd flux through a 3-cycle needs an odd number of its fixed points to carry the matching discrete flux.
Derived:
- In Model I all three complex-structure moduli are in flux relations. Whichever is the inflaton (U₁ ∈ {τ₁, τ₂, τ₃}) sits in a relation: τ₁ or τ₂ through τ₁τ₂ = c (D765: metric doubles, r → 6.5–7.5e-4), or τ₃ through τ₃ = S (−ln Im S − ln Im τ₃ → −2 ln Im τ₃, the same doubling).
- So Model I, and with it P2 as stated, is INCOMPATIBLE with the frozen SERAPIS-E bands. D771's configuration is moot. P2 RETIRED (β3 slot freed).
Create (no-stop rule): POSTULATE P4.
- F₃ = 0 and an odd H₃ quantum give W = S·(a·U₂U₃ + b). At W = 0, D_S W = 0 enforces U₂U₃ = −b/a and leaves U₁ (the inflaton) free.
- S is flat at this order, so it needs separate stabilisation. SERAPIS already uses a supersymmetric racetrack for the dilaton (D586, D591).
- n_flux = ∫F₃∧H₃ = 0, so no flux tadpole cost. The odd NS quantum needs exotic O3 planes (+¼ each).
Computed (tadpole room, n_O3′ ≡ 0 mod 4 spread evenly):
- n_O3′ = 4: (N, N0) = (4, 2), N_eff = 2.
- n_O3′ = 8: (4, 0), N_eff = 4, Im S·Im ρ = 750–975 (the same as D696's original).
- n_O3′ = 12: (3, 1), N_eff = 2.
- n_O3′ = 20: (2, 0), N_eff = 2.
VERDICT (locked rule): VIABLE-ARITHMETIC. P4 keeps the inflaton's metric single and the frozen bands untouched, and has tadpole room (up to N_eff = 4).
Untested:
- the exotic-plane parity pattern for this H₃ (odd count per odd-flux cycle) together with even spreading on the inflaton torus;
- dilaton stabilisation compatible with W = 0 and the anti-D3 uplift;
- whether CP violation needs U₂ = ω (as in D766: U₂ = i is CP-even);
- H₃-only vacua with W = 0 may conflict with D693's W₀ ≠ 0 requirement in the covariant completion (Sec. VII: f² = 3|W₀|²) — to check.
The paper's CP paragraph is updated (unpublished v3.1).
MAP: node=lepto_rho status=assumed touches=[lepto_i] ripple=no

## D773 (FORWARD, i-side; Jl tick 12; locked PREREG_D773 + DEVIATIONS D1; results/p4_susy_d773.txt) — P4 RETIRED; in untwisted T⁶/(Z₂×Z₂) flux vacua no CP-violating flux relation leaves the inflaton torus free, so SERAPIS needs explicit CP (P1 reopened)
Computed (GVW superpotential, basis read off D772's Model I; K4 reproduces Model I's τ₁τ₂ = −3/2, τ₃ = S):
- P4, W = −S(2τ₂τ₃ + 3): the only SUSY Minkowski solution is S = 0. Not admissible (Im S > 0 fails); P4 RETIRED. Reason [derived]: W = S·g(τ) needs g = 0 AND S·∂g = 0, and ∂g ≠ 0 on g = 0.
- General τ₁-free fluxes (all 5.76e6 vectors with entries −3…3 on the 4+4 components not involving τ₁): 0 admissible vacua.
  - Exact reason (D1 reduction): stationarity in τ₂, τ₃ reduces W = ∂_S W = 0 to a double root of a real quadratic Q(S), so S is real.
  - This holds for ANY integer fluxes, not just the grid. The grid check agrees.
Consequence [derived]: in untwisted T⁶/(Z₂×Z₂) GVW vacua, a SUSY Minkowski point that fixes complex moduli off the CP locus needs S paired with a τ-dependent factor. Model I's (τ₃ − S) uses the third torus. So every such vacuum involves the inflaton torus, which D765 excludes (doubled metric, r out of band).
- Flux-relation CP sources are therefore incompatible with SERAPIS within this setup.
- Remaining CP routes: explicit CP in the heavy-ν couplings (P1, REOPENED); twisted complex-structure moduli (torsion models; not examined); a separate hidden sector.
VERDICT (locked rule): P4 RETIRED; reopen explicit CP (P1). D762's result stands: leptogenesis on both branches needs CP phases the CP-conserving vacua cannot provide, and SERAPIS has no in-model source for them. D762's statistics (P1 natural, P = 0.62–0.99) apply again.
The paper's CP paragraph is updated (unpublished v3.1).
MAP: node=lepto_rho status=assumed touches=[lepto_i] ripple=no

## D774 (REVERSE, ρ-side; Jl tick 13; literature, no computation) — twisted moduli as the CP source: in tension with SERAPIS-E's orbifold-point tilt; P1 stays the working assumption
Deep research (1 search, 1 fetch; 1702.08424, T⁶/(Z₂×Z₂) with discrete torsion, Hodge (3, 51)):
- There are 48 twisted complex-structure (deformation) moduli ε^{(i)}_{αβ}, one per Z₂ singularity. Non-zero values DEFORM the fixed loci: "an exceptional cycle with non-vanishing volume emerges".
- D-branes can obstruct deformations through FI D-terms, pinning the modulus at the orbifold point. Stuck branes have no open-string moduli. The paper treats IIA D6-branes, and says nothing about IIB D3s or fluxes.
- No source found on flux stabilisation of twisted moduli at complex values in the IIB O3 torsion model (search-only claim).
Derived/estimate:
- SERAPIS-E's tilt (D689–D696) is the BHK one-loop Kähler term evaluated AT the orbifold point, with stuck D3s at fixed points. A CP phase from twisted moduli needs ε ≠ 0 with a phase, which deforms exactly the singular points the stuck stacks sit at (or their images in the other tori).
- The orbifold point ε = 0 is CP-even. A small |ε| keeps the tilt formula approximately and gives a phase of O(|ε|) in couplings to the twisted sector. Whether the heavy-ν couplings are of that kind is unknown.
- Route status: possible in principle with |ε| ≳ 0.01 (D731's smallest sin δ), but it sits in tension with the stuck-brane picture. No in-model source. Recorded as a direction, not as a postulate (β3 kept for testable items).
VERDICT: the in-model CP chain is EXHAUSTED for now (D762–D774): untwisted flux relations are impossible without the inflaton (D773), and twisted moduli conflict with the orbifold-point tilt (estimate). P1 (explicit CP phases) stays the working assumption on both branches.
Next (forward): upgrade lepto_rho from the Davidson–Ibarra upper estimate (D731) to an actual CP-asymmetry computation for the 2⊕1 heavy-ν sector at ρ under P1 (random complex couplings), as D745 did for τ = i.
MAP: node=lepto_i status=assumed touches=[lepto_rho] ripple=no

## D775 (FORWARD, i-side; Jl tick 14; locked PREREG_D775; results/lepto_rho_ci_d775.txt) — ρ-leptogenesis computed: passes for c = 1 and 3 at the preferred M_H = 1e12 (29–70% of the grid), FAILS for c = 0.3; corrects D731's "pass in all cases"
Computed: Covi–Roulet–Vissani unflavoured ε (vertex + self-energy), Casas–Ibarra 27³ complex-R grid (P1), NO, m₁ = 1e-4 and 1e-3 eV, D731 yield conventions. The degenerate pair is aligned to Re H₁₂ = 0, so it has no mutual term. K4: c = 0.3 hierarchical, max|ε̄_pair|/ε_DI = 0.47, inside [0.3, 1.3]. PASS.
M_H = 1e12 (the gamma-ray-preferred scale, D733); pass fractions for m₁ = 1e-4 / 1e-3 eV:
- c = 0.3: pair 0.0 / 0.0%, single 0.0 / 0.0%. max|ε̄_pair| = 1.0e-5 = 0.48 ε_DI, so Y_B max ≈ 7.6e-11, a factor 1.15 short. FAIL.
- c = 1: pair 32.9 / 29.4%, single 56.2 / 54.0%. PASS.
- c = 3: single (the lighter state, 4.7e11) 70.2 / 68.0%, slightly above DI (ratio 1.1, self-energy enhancement); the pair (1e12) 0%. PASS.
M_H = 1e13 (gamma-ray-disfavoured): 78–91%, PASS.
Why D731 was too optimistic: the actual |ε| reaches only 0.03–0.8 of the DI bound for these spectra. For the heavy single state with c = 0.3 the ratio is only 0.03, because its loop partners (the light pair) are lighter (x < 1 suppresses f + g).
VERDICT (locked rule): not all M_H = 1e12 cases pass, so lepto_rho is not "computed" across the board. It is CORRECTED: ρ-leptogenesis (under P1) works for c ≳ 1, i.e. M_pair/M_H ≳ 0.5, and fails for the most hierarchical c = 0.3 sector at M_H = 1e12. Combined with D733, SERAPIS-E now points to M_H ≈ 1e12 GeV with an order-one doublet–singlet mixing c ≳ 1.
Other notes:
- The T_R for c = 1 and 3 (4.3e8, 9.5e8 GeV, D725) stays inside the frozen-band N* range (D725: n_s 0.9732–0.9739).
- The paper's D731 sentence is updated (unpublished v3.1).
- Mirror question (reverse, next tick): what fixes c? The doublet–singlet coupling through the weight-2 doublet (D724/D739) is a free O(1) coefficient. Is there a Γ₂ or weight argument, or a string selection rule, making c ~ 1 natural, or bounding it?
MAP: node=lepto_rho status=corrected touches=[gravitino_wino] ripple=no

## D776 (REVERSE, ρ-side; Jl tick 15; locked PREREG_D776; results/c_threshold_d776.txt) — c is a free O(1) ratio (the Kähler factors cancel); ρ-leptogenesis needs c ≥ 0.6, natural for ~61% of a log-uniform prior
Reasoning [derived]: with the consistent weights k_N = k_N3 = −1 (D724), the doublet–doublet and doublet–singlet Majorana terms are both weight-2 forms Y. Each carries the same canonical factor (2 Im τ)^{(k_i + k_j)/2}, so the factor cancels in c. Γ₂ ≅ S₃ allows the two invariants independently, so c is the ratio of two O(1) superpotential constants, not fixed by the symmetry. No literature search this tick (budget). I know of no selection rule fixing c, an honest statement of what was not checked.
Computed (D775 code path, M_H = 1e12, m₁ = 1e-3 eV, T_R(c) interpolated from D725; K4: c = 0.3 and 1.0 reproduce D775, 0% and 29.4/54.0%):
- Pass fraction (max of the pair and single channels): 0 / 0.5 / 2.2 / 8.2 / 12.1 / 14.3 / 25.5 / 54.0% for c = 0.3 / 0.35 / 0.4 / 0.5 / 0.6 / 0.7 / 0.85 / 1.0.
- So c* = 0.6.
- With a log-uniform prior on [0.1, 10], P(c ≥ 0.6) = 0.61. For c ≥ 3 the pass fraction is ~70% (D775).
VERDICT: c ≳ 0.6 is a MODEL REQUIREMENT for ρ-leptogenesis at M_H ≈ 1e12 (natural in ~60% of a broad prior). It is not load-bearing for the frozen predictions, so no new postulate is made (β3 kept). For the paper, the D775 sentence's "c ≳ 1" is refined to "c ≳ 0.6".
Mirror question (forward, next tick): the ρ-branch's neutrino predictions. With the 2⊕1 sector and c ≳ 0.6, does the light-neutrino texture at ρ give normal ordering and Σm_ν ≈ 0.059 eV (the frozen value)? D741 found a TENSION at ρ with the minimal Weinberg texture (no NO points). Recheck with the seesaw from this heavy sector (Casas–Ibarra is agnostic). Is there a modular-form Dirac Yukawa at ρ that, through the seesaw, gives NO with m₁ ≪ m₃?
MAP: node=lepto_rho status=corrected touches=[] ripple=no

## D777 (FORWARD, i-side; Jl tick 16; locked PREREG_D777; results/rho_seesaw_d777.txt) — FAIL: at ρ the weight-2 seesaw ALWAYS gives an exactly degenerate light pair, so no ordering matches oscillation data
Computed (M_R = [[A(Y), cY], [cYᵀ, 0]], M_D = [[A(Y), βY], [γYᵀ, 0]], Y ∝ (1, i) at ρ, L₃N₃ = 0 as no weight-2 singlet exists; 1764 complex (β, γ) per c ∈ {0.6, 1, 3}). K4: M_R's singular values are (c, c, √2), matching D725's pair/single ratio 0.7072c.
- NO = 0 and IO = 0 points for every c.
- A diagnostic after the locked run (labelled as such): the light singular values always contain an exactly degenerate pair, e.g. (1, 1, √2), (0.6, 0.6, √2), (√2, 7.07, 7.07). That holds in 243/243 sampled points.
- Reason [derived]: the residual Z₃ (ST) symmetry at ρ acts on the 2⊕1 sector, and with only weight-2 Y couplings both M_D and M_R are built from the same aligned objects, so the seesaw inherits the degeneracy. Charged-lepton mixing cannot help, because it does not change the eigenvalues of m_ν.
VERDICT (locked rule): FAIL. The ρ-branch's minimal (weight-2) lepton sector gives Δm²₂₁ = 0 or Δm²₃₂ = 0 exactly. This extends D741's tension (no NO with the Weinberg texture at ρ) to the full seesaw.
- The frozen Σm_ν (0.0587 eV, normal-ordering floor) stays as locked, but the ρ-branch has NO derived light-neutrino spectrum: it needs symmetry breaking beyond weight 2.
- Candidates:
  - (a) higher-weight forms that are non-zero and non-aligned at ρ: E6·Y (weight 8) lifts the null direction (D739), and E6(ρ) ≠ 0;
  - (b) an L₃N₃ singlet of weight 6 ∝ E6 (non-zero at ρ);
  - (c) τ displaced slightly from ρ (it sits exactly there, so no).
- The leptogenesis results (D775–D776) used Casas–Ibarra, which is agnostic about the texture, so they are unaffected only if a texture with the observed spectrum exists. That is now an open condition.
Mirror question (reverse, next tick): find the MINIMAL addition that splits the degenerate light pair at ρ. Test (b), a weight-6 singlet δ·E6 for L₃N₃ (and/or N₃N₃), and (a), a weight-8 doublet term. Lock a scan; report the NO fraction and Σm_ν. If a minimal addition works, ρ's neutrino sector is restored at that cost.
MAP: node=n_sector_rho status=corrected touches=[mnu, lepto_rho] ripple=no

## D778 (REVERSE, ρ-side; Jl tick 17; locked PREREG_D778; results/rho_weights_d778.txt) — NOT RESTORED: no Dirac-weight assignment with lepton doublets fixes the ρ spectrum; the residual Z₃ forbids it (theorem); the remedy is lepton SINGLETS
Computed: all 25 Dirac-weight assignments (w_d, w₃) ∈ {0, 2, 4, 6, 8}², with complex coefficients on the locked grid and c ∈ {0.6, 1, 3}. K4: (2, 2) reproduces D777. Result: zero NO and zero IO points for every assignment.
A diagnostic after the locked run shows either a degenerate pair, e.g. (4, 4) → (0.99, 0.99, 1.20) and (0, 6) → (0.71, 0.90, 0.90), or a singular M_D.
Reason (theorem) [derived]:
- At ρ the residual ST ≅ Z₃ assigns each field a charge q = (rep phase) + (weight phase).
- A Majorana mass entry m_ij can be non-zero only if q_i + q_j ≡ 0 (mod 3).
- The two components of a Γ₂ doublet carry DIFFERENT charges (ST has eigenvalues ω, ω² on the doublet, shifted equally by the weight phase).
- So a light-lepton doublet always yields either a (q, −q) pair, which gets a Dirac-type degenerate mass, or a state with no partner, which is massless. Three non-degenerate light masses need all three light leptons at q = 0, which a doublet cannot do.
- This holds for the seesaw too (m_ν inherits the light fields' charges).
- It is the reason modular-flavour fits at ω use τ slightly OFF the fixed point (2405.18813 quotes |τ − τ*| ~ 0.01–0.1). SERAPIS-E's vacuum sits exactly at ρ (a symmetry-fixed minimum).
Remedy (creation, testable): put the lepton doublets in Γ₂ SINGLETS, L ∈ 1 ⊕ 1 ⊕ 1′ (1 and 1′ both have Z₃ charge 0, plus the weight phase chosen so that q = 0).
- Then m_ν is unconstrained by Z₃, and three distinct masses are allowed.
- The heavy-ν doublet sector, needed for reheating and leptogenesis at ρ (D724–D776), is unaffected: the N masses may stay degenerate, since they are heavy.
- Cost: no Γ₂ predictivity for the PMNS structure (lepton flavour becomes generic).
VERDICT (locked rule): NOT RESTORED with lepton doublets. ρ-branch lepton doublets are EXCLUDED by the residual Z₃ (exact).
Next (forward): verify the singlet remedy. Seesaw with L = 1 ⊕ 1 ⊕ 1′ and the D724 heavy sector at ρ, singlet Dirac couplings (weight-0 constants and the weight-6 E6 entries allowed by q = 0). Find the NO fraction with Σm_ν ≤ 0.064 eV. Also check whether leptogenesis (D775) survives with this Dirac structure (Casas–Ibarra is agnostic; just confirm a fit exists).
MAP: node=n_sector_rho status=corrected touches=[mnu] ripple=no

## D779 (FORWARD, i-side; Jl tick 18; locked PREREG_D779 + DEVIATIONS D1–D2; results/rho_charges_d779.txt, run1 INVALID kept) — the singlet-lepton remedy alone gives rank(m_ν) = 1; the ρ branch needs two EXTRA Z₃-neutral heavy singlets
Computed (charge eigenbasis of the Γ₂ doublet at ρ: n = (1, −i)/√2 and Y = (1, i)/√2; K4: M_R's singular values (1, 1, √2) at c = 1, PASS after D1–D2):
- In that basis M_R has non-zero entries only at (n, N₃) and (Y, Y). So N_n and N₃ form a Dirac-type pair (charges q, −q; mass c), and N_Y is the only Z₃-neutral, pure Majorana state (mass √2).
- With light leptons as singlets of common charge q_L = −q_H, Dirac couplings are allowed only to q = 0 heavy states, i.e. N_Y alone. Then rank(m_ν) = 1 (1000/1000 random draws): two massless light neutrinos, FAIL.
- Adding Z₃-neutral heavy singlets with generic masses: rank 2 with one extra, rank 3 with two extra.
VERDICT (locked rule): the D778 remedy FAILS as stated. MINIMAL working extension: light leptons as Γ₂ singlets (q = −q_H) PLUS at least two extra Z₃-neutral heavy singlet neutrinos.
- The 2⊕1 sector keeps its role in reheating and leptogenesis (the Dirac pair N_n–N₃ and N_Y; D724–D776). The light masses come from N_Y and the two new singlets.
- Consequence: D775's leptogenesis assumed 3 heavy states with Casas–Ibarra Yukawas. With 5 heavy states and Z₃-restricted Yukawas (the N_n, N₃ pair has NO Dirac coupling to q = 0 leptons at ρ), the decaying Dirac-pair states cannot produce a lepton asymmetry at tree level, because they do not couple to leptons. Only N_Y and the new singlets can.
- This affects D775 (computed with the full Casas–Ibarra structure) and is a CORRECTION to check next.
MAP: node=n_sector_rho status=corrected touches=[lepto_rho, mnu] ripple=no

## D780 (REVERSE, ρ-side; Jl tick 19; derivation, no computation) — exact Z₃ at ρ: the inflaton is Z₃-charged, so its decay products carry Z₃ charge, and the charged heavy-ν pair cannot decay through renormalisable couplings; ρ reheating must be redone
Charge bookkeeping (lesson D778):
1. δτ at ρ transforms under the residual ST ≅ Z₃ with a non-trivial phase (weight −2 at a fixed point), so inflaton quanta carry Z₃ charge q_φ ≠ 0 [derived].
2. Heavy states (D779): N_Y (charge 0), Dirac pair N_n (q) / N₃ (−q), q ≠ 0, plus the neutral singlets S₁, S₂.
3. Inflaton decays φ → N_a N_b need q_a + q_b ≡ −q_φ ≠ 0, so EVERY channel contains at least one charged N_n or N₃ [derived]. This matches D725's open channels (LL pair and HL), all of which involve the pair.
4. Realistic light masses force a common lepton charge q_L = −q_H (D778). The renormalisable Dirac coupling L·N·H then needs q_N = 0, so N_n and N₃ cannot decay to L + H [derived]. D725's statement "light states decay via seesaw y_D 0.02–0.13" is WRONG at ρ.
5. Gauge-invariant SM bilinears (H_uH_d, constrained by the μ-term, and L H_u) are Z₃-neutral, so electroweak vevs do not break Z₃ in renormalisable couplings [derived].
6. Modular symmetry is a gauge symmetry in string theory, so Z₃ is exact: no gravitational breaking [literature-level statement, from memory].
Consequences:
- If no operator of any dimension carries the pair's charge, the lightest Z₃-charged state is STABLE. Produced with Y ~ (3/4)T_R/m_φ ~ 1e-5 at M ~ 1e11–1e12 GeV, it overcloses by ~1e14. FATAL.
- If a higher-dimension operator with charge q exists (SM fermion charges are partly free, fixed only by the Yukawas and anomalies), the pair decays through it: Γ ~ M⁵/Λ⁴. With Λ = M_P and M = 1e12, Γ ≈ 3e-14 GeV; the pair (which carries ALL the inflaton energy) then reheats a second time at T₂ ~ √(Γ M_P) ~ 300 GeV. With Λ = M_s ~ 1e16–1e17 GeV, T₂ ~ 3e4–3e6 GeV.
- Either way, D725's T_R = 3e8–3e9 GeV is NOT the final reheating temperature at ρ. The effective T_R is much lower, N* shifts, and the leptogenesis of D731/D775/D776 (produced before the second reheating) is diluted or reset.
VERDICT: CORRECTION. ρ-branch reheating (D725), and everything built on its T_R (leptogenesis D731/D775/D776, the gravitino/wino chain D732–D736), must be recomputed with Z₃ charge conservation. The frozen SERAPIS-E bands are locked and stay as frozen.
- Sign of the shift: a lower T_R lowers N* and n_s (D725: N* 49.7–50.5 at T_R 3e8–3e9). With T₂ ~ 300 GeV–3e6 GeV, N* is ~1.5–4 e-folds lower, and n_s may drop out of the band. That must be computed.
- The τ = i branch is NOT affected the same way: its residual Z₂ allows odd leptons with Majorana masses (2q ≡ 0 mod 2), so odd heavy states can decay to odd leptons.
Next (forward, locked): (a) the N* and n_s, r shift for T₂ ∈ {3e2, 3e4, 3e6} GeV, with an intermediate matter phase of the pair, using the D719/D725 N* code; (b) whether n_s stays in 0.970–0.975.
MAP: node=n_sector_rho status=corrected touches=[lepto_rho, gravitino_wino, serapis_e] ripple=no

## D781 (FORWARD, i-side; Jl tick 20; locked PREREG_D781; results/late_reheat_d781.txt) — the frozen SERAPIS-E bands survive the Z₃ late reheating only if T₂ ≳ 1e5–1e6 GeV (decay via string-scale operators); Planck-suppressed decay (T₂ ~ 300 GeV) puts SERAPIS-E outside its frozen r band
Computed (D725 N* code, matter-like until T₂; K4: C = 1.15e-6 at T₂ = 3.175e8 reproduces D725 exactly: N* 49.72, n_s 0.9732, r 4.697e-4):
| T₂ (GeV) | N* | n_s (C = 1.0 / 1.15 / 1.3e-6) | r (×1e-4) | frozen bands |
|---|---|---|---|---|
| 3.2e8 (D725) | 49.7 | 0.9716 / 0.9732 / 0.9748 | 4.52 / 4.70 / 4.89 | INSIDE (C ≥ 1.15) |
| 3e6 | 48.2 | 0.9701 / 0.9716 / 0.9732 | 4.73 / 4.90 / 5.09 | INSIDE (all C) |
| 3e4 | 46.6 | 0.9686 / 0.9700 / 0.9715 | 4.95 / 5.12 / 5.31 | OUTSIDE (r just above 5.12 where n_s is in band) |
| 3e2 | 45.1 | 0.9669 / 0.9683 / 0.9698 | 5.20 / 5.37 / 5.55 | OUTSIDE |
VERDICT (locked rule): INSIDE for T₂ = 3e6, OUTSIDE for T₂ ≤ 3e4.
- A lower T₂ lowers N* by ≈ 0.75 per decade of T₂, which lowers n_s and raises r. The frozen strip's r ceiling (5.12e-4) is crossed near T₂ ~ 1e5 GeV.
- Therefore the frozen D693 predictions hold at ρ ONLY IF the Z₃-charged heavy ν decay through operators suppressed by Λ ≲ M_s (T₂ ≳ 1e5–1e6 GeV). With M_P-suppressed decay (T₂ ~ 300 GeV) SERAPIS-E sits at r ≈ 5.2–5.5e-4, outside its frozen r band (but inside the family cap 8.3e-4 and the strip's broader range).
- The frozen bands are NOT changed. This is a conditional CORRECTION: the frozen ρ-branch numbers now carry an extra condition (T₂ ≳ 1e5 GeV).
- If that condition fails, the post-hoc SERAPIS-E prediction moves to r ≈ 5.2–5.5e-4, n_s ≈ 0.967–0.970, scored only on future data.
Next (reverse): what sets Λ? Which Z₃-allowed operator lets the charged pair decay, and at what scale? Candidates: string-scale (M_s) couplings to the twisted sector; operators with the dilaton or Kähler moduli that carry Z₃ charge; or decay into a light Z₃-charged hidden state (dark radiation). Deep research plus charge bookkeeping.
MAP: node=serapis_e status=computed touches=[n_sector_rho] ripple=no

## D782 (REVERSE, ρ-side; Jl tick 21; literature + derivation, no computation) — the residual Z₃ at ω exactly stabilises a heavy neutrino (literature: used as DM); SERAPIS-E at ρ needs a Z₃-allowed higher-dimension decay with Λ ≲ 3e16 GeV, and then baryogenesis must come from those late decays
Literature (2111.05674, modular A₄; fetched): "the Z₃ is restored at τ = ω. This is why N_R1 is stable". The heavy neutrino's only Yukawa is a form that vanishes at the fixed point. Decay happens only if τ deviates from the fixed point (lifetime estimates there). Their DM is TeV-scale with a B−L scalar for annihilation. They do not treat heavy states produced by inflaton decay.
- So D780's conclusion is the standard fixed-point result, applied to a case (inflaton → charged N at 1e11–1e12 GeV) where stability is fatal, not useful.
Charge bookkeeping, SERAPIS-E at ρ [derived]:
- Z₃-charged: δτ (the inflaton and axion), the N_n/N₃ pair. SM fields carry the charges their modular weights give, which are free up to Yukawa, μ-term and anomaly conditions.
- Z₃-neutral by construction: N_Y, S₁, S₂, the gauge-invariant bilinears H_uH_d and LH_u (D780).
- The stuck-D3 open strings and twisted states: unknown charges (not checked).
- A Z₃-allowed decay of the pair needs an SM operator O_SM with charge −q. Renormalisable LHN is excluded (D780). The lowest candidates are dim-6, e.g. N·u·d·d (B-violating) or N·L·Q·d (L-violating), allowed if the SM weights give q_O ≡ −q. That is a CHOICE of SM weights, available at the cost of fixing them.
Required scale (estimate): Γ ≈ M⁵/(192π³Λ⁴) (3-body) and T₂ ≈ √(ΓM_P)·(90/π²g*)^{1/4} ≳ 1e5 GeV (D781) ⇒ Λ ≲ 3e16 GeV for M = 1e12 (Λ ≲ 1e16 for M = 4e11). That is about the string scale for Im S·Im ρ ~ 1e2–1e3 (estimate; M_s not computed here).
Consequence for baryogenesis [derived]: the pair dominates the energy density until T₂, so any asymmetry made earlier (D731/D775/D776 at T_R1) is diluted by ~M·Y_N/T₂ ≳ 1e3–1e6. Baryogenesis at ρ must then come from the late, B- or L-violating, CP-violating pair decays themselves: Y_B ≈ (3/4)(T₂/M)·ε_late. With T₂ ~ 1e6 and M ~ 1e12 this needs ε_late ≳ 1e-4.
VERDICT: a REQUIREMENT, not a postulate (β3 kept): "R-Z₃ — the SM modular weights admit a dim-6 Z₃-charged operator coupling the heavy pair, suppressed by Λ ≲ 3e16 GeV." It restores the frozen ρ band (D781). ρ-leptogenesis via D775/D776 is SUPERSEDED (diluted), and late-decay baryogenesis becomes the ρ route (to compute).
Next (forward, locked): compute (a) T₂(Λ, M) with the 3-body width, giving the Λ window that keeps the frozen bands; (b) the late-decay ε needed, and whether a two-operator interference with P1 phases can reach ε ≳ 1e-4 (order of magnitude).
MAP: node=lepto_rho status=corrected touches=[n_sector_rho, serapis_e] ripple=no

## D783 (FORWARD, i-side; Jl tick 22; locked PREREG_D783; results/lambda_window_d783.txt) — the ρ band needs Λ ≲ 4e15–1e16 GeV, about the string scale (estimate 6e15–3e16); late-decay baryogenesis is plausible (ε ≈ 2e-5 – 3e-3)
Computed (Γ = M⁵/(192π³Λ⁴), T₂ = (90/π²g*)^{1/4}√(ΓM_P)):
- The largest Λ with T₂ ≥ 1e5 GeV (the D781 boundary): 3.6e15 / 6.8e15 / 1.05e16 for M = 4.3e11 / 7.1e11 / 1e12. For T₂ ≥ 3e6 (inside for all C): 0.67 / 1.2 / 1.9e15.
- M_s estimate (M_s ≈ g_s^{1/4}M_P/√(4πV), V = (Im ρ)^{3/2}, Im S·Im ρ = 375–975, g_s = 0.1–0.5): 5.6e15 – 2.6e16 GeV.
- So the decay operator must be suppressed by a scale AT or slightly BELOW M_s (Λ/M_s ≈ 0.15–1.9 across the grid). M_P suppression (T₂ ~ 1 GeV) is excluded, and the required window overlaps the string scale only at its low end.
- Late-decay baryogenesis: ε_req = 2e-5 – 1.2e-3 (B-violating) or 5e-5 – 3.3e-3 (L-violating), all ≤ 1/(8π). PLAUSIBLE.
VERDICT (locked rule): PLAUSIBLE, but TIGHT.
- The frozen ρ-branch predictions survive only if the Z₃-charged heavy neutrinos decay through string-scale operators with O(1) couplings (Λ ≲ M_s), and the SM weights admit such an operator (R-Z₃).
- Baryogenesis then comes from those late decays with ε ~ 1e-4 – 1e-3.
- If the operator is suppressed even mildly more (Λ ≳ 2M_s at M = 1e12), T₂ < 1e5 and the frozen r band is exceeded (D781).
- This is now the ρ branch's most fragile link.
ρ-branch status: viable only through R-Z₃ plus string-scale decay plus late-decay baryogenesis. The τ = i branch is untouched by Z₃ issues; its frozen predictions do not carry these conditions.
MAP: node=serapis_e status=computed touches=[lepto_rho] ripple=no

## D784 (REVERSE, ρ-side; Jl tick 23; locked PREREG_D784; results/wino_late_d784.txt) — after the Z₃ late reheating the SERAPIS-E wino is thermal: window WIDENS from 0.67–0.80 to 0.67–1.85 TeV (5–41% of DM)
Computed (K4: D732's Ω_total at M₂ = 0.66 TeV, T_R = 3.2e8, reproduced: 0.017):
- No thermal bath exists before T₂ (the inflaton decays to heavy N), so gravitinos are made only at T₂: Y₃/₂ = 1.9e-17 to 1.9e-15 for T₂ = 1e5–1e7. Their winos give Ω_nth = 4e-6 to 4e-4 at 0.7 TeV, negligible.
- T₂ ≫ T_f ≈ M₂/20, so winos freeze out thermally: f = (M₂/2.9 TeV)² = 0.053 at 0.67 TeV and 0.41 at 1.85 TeV.
- Einasto line limit (D735 method): allowed for M₂ ≤ 1.96–2.00 TeV. Combined with 2507.15934's stated exclusion of thermal sub-fractions from 1.85 TeV up, and the ATLAS 670 GeV floor: window 0.67–1.85 TeV.
VERDICT (locked rule): CHANGED. The sharp post-hoc 0.67–0.80 TeV window (D735, built on T_R = 3e8) is SUPERSEDED by the generic thermal-wino window 0.67–1.85 TeV (5–41% of DM).
- The prediction is less sharp: HL-LHC disappearing tracks (~1 TeV reach, D736) test only its lower half, and gamma-ray lines its upper end.
- The rest of the DM needs another component (as D713).
- The paper's table row, the SERAPIS-E text and the abstract were updated; 2507.15934 added to refs.
MAP: node=wino_window status=corrected touches=[gravitino_wino] ripple=no

## D785 (FORWARD, i-side; Jl tick 24; locked PREREG_D785; results/i_mirror_d785.txt) — mirror check PASSES: at τ = i every heavy state couples to leptons and the light spectrum is generically non-degenerate; D780's claim that τ = i is unaffected is confirmed
Computed (the S₃ q-series doublet; K4: Y₂/Y₁ = i at ρ to 2e-11, PASS; at i, Y ∝ (√3/2, ½), real):
- M_R = [[A(Y), cY], [cYᵀ, 0]] at i has NON-degenerate singular values: (0.28, 1, 1.28), (0.62, 1, 1.62), (1, 2.54, 3.54) for c = 0.6, 1, 3. Unlike ρ, there is no Dirac-type pair.
- Every heavy Takagi eigenstate couples to the leptons: min/max column-norm ratio 0.05–0.10 over the grid, never 0. No stable heavy state.
- Light spectrum: only 1–3% of grid points are degenerate (54/1764 at most). NO points exist (12–18 per c) and IO points too.
VERDICT (locked rule): τ = i UNAFFECTED.
- The residual symmetry at i is the Z₂ (Z₄ with the centre) generated by S, whose real representation lets every state have a Majorana mass. The Z₃ obstruction (D778–D780) is specific to ρ.
- The τ = i branch's post-inflationary chain (D727–D745) and its frozen predictions carry none of the ρ conditions.
- The weight-2-only seesaw at i also reproduces both orderings, consistent with D741/D742, where NO needed extra structure for Σm_ν. Here the Σ values were not evaluated; that is not part of this lock.
Note: the paper's ρ caveat says "the τ = i branch is not affected", which is now computed (was reasoning in D780).
MAP: node=n_sector_i status=computed touches=[lepto_i] ripple=no

## D786 (REVERSE, ρ-side; Jl tick 25; arithmetic in code, no model run) — the frozen Σm_ν = 0.0587 eV is now the NO floor of a range: m₁ is no longer forced to ≈ 0 on either branch
Reverse step from the frozen value (lock D605): Σ = 0.0587 eV ⇔ NO with m₁ ≲ 1e-4 eV (computed: Σ(m₁) = 0.0586 / 0.0587 / 0.0597 / 0.0622 / 0.0652 eV for m₁ = 0 / 1e-4 / 1e-3 / 3e-3 / 5e-3 eV, with Δm²₂₁ = 7.42e-5, Δm²₃₁ = 2.5e-3).
What each branch now requires:
- τ = i: m₁ ≈ 0 was needed only for Affleck–Dine (D646). D745 made inflaton-decay leptogenesis viable without AD, so m₁ is free. The D742 texture gives m₁/m₃ = 0.001–0.08, i.e. m₁ ≈ 5e-5 – 4e-3 eV and Σ = 0.059–0.064 eV.
- ρ: the light leptons must be Γ₂ singlets (D778–D779), so m_ν is generic and there is no m₁ prediction. Only Σ ≥ 0.0586 (NO) or ≥ ~0.10 (IO).
Status of the frozen number: the lock stays as written (Σ ≃ 0.059 eV if NO). Its physical basis is now "the NO floor, approached when m₁ ≪ 1e-3". The disfavouring condition (Σ > 0.07 eV) is unchanged, and the τ = i range 0.059–0.064 sits inside it.
- DESI DR2 + Lyα 95% bound 0.0592 eV ⇒ m₁ ≲ 5.6e-4 eV, which already cuts the upper part of the τ = i range. A post-hoc observation, scored only on future data.
Flags cleared (rechecked, status unchanged): plateau_origin (P3 open; the axion falsifier cleared in D769–D770), lepto_i (D785: unaffected), gravitino_wino (D784 superseded the ρ part), n_sector_rho (D779/D780 corrections stand).
MAP: node=mnu status=frozen touches=[] ripple=no
MAP: node=plateau_origin status=assumed touches=[] ripple=no
MAP: node=lepto_i status=assumed touches=[] ripple=no
MAP: node=gravitino_wino status=estimate touches=[] ripple=no
MAP: node=n_sector_rho status=corrected touches=[] ripple=no
MAP: node=lepto_rho status=corrected touches=[] ripple=no

## D787 (FORWARD, i-side; Jl tick 26; locked PREREG_D787; results/rz3_charges_d787.txt) — R-Z₃ is SATISFIABLE: if the Higgs carries Z₃ charge, the residual Z₃ acts on SM operators as BARYON TRIALITY; the heavy pair then decays via N·u^c d^c d^c (B-violating), and the proton is protected
Computed (charges mod 3 with the imposed Yukawas, μ, Weinberg and LH_uN_Y; 9 assignments, free (q_Q, q_Hu)):
- q_Hu = 0 (3 assignments): every SM operator is Z₃-neutral, so the pair has no allowed decay. STABLE RELIC (FAIL).
- q_Hu ≠ 0 (6 assignments): UDD and QQQL carry charge ±1 and are FORBIDDEN, while N·UDD (W) and N·QQQL are allowed for the two pair charges. QDL, LLE and LH_u are Z₃-neutral (allowed by Z₃; they need matter parity, which the centre supplies at ρ, D661).
VERDICT (locked rule): R-Z₃ SATISFIABLE, in 6/9 assignments, exactly those with q_Hu ≠ 0, in which Z₃ acts on gauge-invariant SM operators as a baryon-number triality.
Consequences [derived]:
- With the D661 matter parity also imposed (N odd, quarks/leptons odd): N·UDD is even, ALLOWED; N·QQQL is odd, forbidden.
  - The pair member with the matching charge decays via the superpotential operator N·u^c d^c d^c/Λ².
  - Its Dirac partner (opposite charge) decays via the Kähler conjugate N†·u^c d^c d^c/Λ², which is also dim-6, so both decay at the D783 rate.
- Proton: QQQL and UDD are both forbidden by Z₃ (baryon triality) and matter parity together, so there is NO dim-4 or dim-5 proton decay. ΔB = 1 needs an on-shell N, which is impossible. Proton stable.
- Baryogenesis: the late decays N → u d d violate B directly (κ = 1 in D783: ε ≈ 2e-5 – 1.2e-3 needed). With CP phases (P1) between the W and K operators, the asymmetry is B-violating, so there is no sphaleron dilution factor.
- Anomaly: baryon triality B₃ is anomaly-free with MSSM content (Ibáñez–Ross; from memory, estimate). The heavy N pair is vector-like under Z₃ (q, −q), adding no anomaly [derived].
ρ-branch status: the Z₃ chain closes consistently. ρ requires (i) q_Hu ≠ 0 (Z₃ = B₃ on the SM), (ii) Λ ≲ 0.4–1e16 GeV for N·udd (D783), and (iii) late B-violating baryogenesis, which also makes the proton exactly stable as a bonus.
MAP: node=n_sector_rho status=computed touches=[lepto_rho] ripple=no

## D788 (REVERSE, ρ-side; Jl tick 27; locked PREREG_D788; results/late_eps_d788.txt) — WALL: late N → udd decays through dim-6 operators give ε ≤ 2e-8 (Nanopoulos–Weinberg), far below ε_req ≥ 2e-5; create P5, a light Z₃-charged colour-triplet diquark mediator, which also removes the late phase
Literature (1310.0840, fetched): for a particle stable without the B-violating interaction, the CP asymmetry needs at least TWO powers of the B-violating coupling (Nanopoulos–Weinberg).
Computed:
- (a) dim-6 only: ε_max ≈ (M/Λ)²/(8π) = 3.6e-10 – 1.7e-8 across the D783 window, against ε_req = 1.7e-5 – 1.2e-3. FAIL in every case, by 3–6 orders of magnitude. Late-decay baryogenesis via string-scale operators is IMPOSSIBLE.
- (b) the mediator arithmetic (coupling y ≥ 0.02–0.17 for ε_req; M_X ≤ y·Λ_eff) was computed. CORRECTION to the lock's (b) formula: for M_X > M the loop needs a second off-shell X, so ε ~ (y²/8π)(M/M_X)² [estimate], which is again too small for M_X ≫ M. The mechanism works only with M_X < M (an on-shell N → u X*, with an unsuppressed ε ~ y²/8π).
WALL → CREATE (no-stop rule): POSTULATE P5 (theory/derivations/POSTULATES.md), a Z₃-charged colour-triplet diquark X with M_X < M_pair and renormalisable couplings N·u·X*, X·d·d. Consequences:
- the pair decays promptly (renormalisable), so there is NO late matter phase and T_R returns to D725 (3e8–3e9). The frozen ρ band holds WITHOUT the Λ condition of D781–D783.
- baryogenesis: B-violating, from N decays, with ε ~ y²/8π. y ~ 0.05–0.2 suffices (estimate; the dilution factor is now O(1) and needs recomputation).
- the proton is still protected (baryon triality, D787).
β3 FLAG: three open postulates (P1, P3, P5). The next tick must test or retire one. P5 also needs a Z₃-charge check for X (proton safety) and a reason for a coloured state at ~1e11 GeV.
MAP: node=lepto_rho status=assumed touches=[n_sector_rho, serapis_e] ripple=no

## D789 (FORWARD, i-side; Jl tick 28; locked PREREG_D789 + DEVIATIONS D1; results/p5_test_d789.txt, run1 INVALID kept) — P5 PASSES its consistency tests; but with P5 the N decays conserve B, so the asymmetry must come from the (Z₃-charged) inflaton's own decays
Computed (6 D787 assignments × 2 pair charges):
- (1) For every assignment exactly ONE of the two pair charges (q) gives a consistent X, X̄ with an allowed mass term M_X·XX̄. The Dirac pair decays through that member's coupling (one Dirac fermion), so this suffices.
- (2) The gauge-allowed renormalisable X-terms are X·U, X̄·Q·H_u and X̄·D·D. Z₃ forbids X·U and X̄·Q·H_u in all cases, so the only allowed one is P5's own X̄·D·D. No leptoquark or U-mixing couplings, hence no proton decay through X. (D1: run 1 counted X̄DD as an "extra" coupling; fixed before rerun.)
- (3) Matter parity: X and X̄ are even (Higgs-like); NUX and X̄DD are even. Consistent.
- (4) Γ(N → uX) = 3e6 – 8e8 GeV ≫ H(3e8 GeV) = 0.6 GeV. Prompt: no late phase, T_R back to D725.
VERDICT (locked rule): P5 PASSES.
New consequence [derived]: assign B(X̄) = +2/3 (from X̄DD), B(X) = −2/3 (mass), so B(N) = +1 (from NUX). All P5 couplings and the Dirac pair mass CONSERVE B, so N decays cannot make a baryon asymmetry (contradicting D788's "baryogenesis in those decays").
- B is violated only by the inflaton's own couplings, e.g. φ → N_nN_n (ΔB = 2) allowed by its Z₃ charge, versus φ → N_Y + N₃ (ΔB = −1).
- So the ρ asymmetry must come from CP violation in the Z₃-charged inflaton's decays: φ vs φ* give B = ±2.
- This is a correction to D788's text (recorded here, not a silent edit). It is the next computation.
β3: three open postulates remain (P1, P3, P5). P5 was tested this tick and passed. P1 cannot be retired (τ = i needs it) and neither can P3 (plateau). The flag stands; next tick continues the P5 line.
MAP: node=lepto_rho status=assumed touches=[] ripple=no
