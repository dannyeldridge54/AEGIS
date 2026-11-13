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
