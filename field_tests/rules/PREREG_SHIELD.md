LOCKED 2026-11-13 (time = lock commit) by the development driver on Danny's word ("construct this and start testing it",
13:26 CT) under STANDING_LOCK_AUTHORITY.md

# PREREG_SHIELD — the isometry shield against the fifth force: what it predicts for varying constants and free fall

## The construction (D140–D142)
The Standard Model is neutral under both isometries of the Twist's field disk (the scaling T → λT and the shift T → T + ic).
Any dependence of a Standard-Model constant on the dark-energy field then comes only from what breaks them:
d ln(constant) = c_q Re q(x) + c_p x^{−p},  q = e^{−πT/4} (the cliff's own instanton, c_q ~ 1), plus a possible perturbative leak.
Already-public limits (quasars, Oklo, BBN, clocks, MICROSCOPE, Cassini) were used to SIZE the leak (shield_tests_d142.txt):
the tightest is atomic clocks — a leak needs p ≥ 4 with c_p < 0.6, or p = 3 with c_p < 9×10⁻³. Those bounds are not evidence
for the shield; they are the space it must live in.

## Locked predictions (for results first public after this lock)
1. Instanton part: |Δα/α| < 10⁻²⁴ at any redshift, |α̇/α| < 10⁻³⁸ /yr, Eötvös η < 10⁻⁴⁰ — undetectable by any planned experiment.
2. The shield's signature if a leak exists: every varying-constant signal has one fixed redshift shape, set by how the field thaws
   (shield_fingerprint.txt): Δα/α(z) / Δα/α(z=1) = 0.22–0.23 at z = 0.14, 0.66–0.67 at z = 0.5, 1.23–1.25 at z = 2,
   1.30–1.33 at z = 3, 1.35–1.38 at BBN (p = 3–4). Almost all of the change happens at z < 2; nothing new above z ≈ 3.
   Clocks and quasars are tied: α̇/α (today, per yr) = −p × 2.5×10⁻¹¹ × (Δα/α at z=1) / (x(1)^{−p}/x₀^{−p} − 1) for the same p.
3. Equivalence principle: η = 2β² × (composition factor ~10⁻³) with β = p c_p x₀^{−p} √(2/3); for the allowed leak, η < 3×10⁻¹⁵ ×
   (current bound) — i.e. MICROSCOPE-class experiments see nothing unless the leak sits at its clock limit.

## Readings (first eligible new result of each kind)
- **CONSISTENT**: no detection; or a detection whose redshift shape matches item 2 within its errors.
- **DISFAVOURED (shield)**: a detected variation of α or μ = m_p/m_e at z > 3 larger than 1.5× the z = 1 value (at > 3σ); or a
  detected variation whose sign differs between z < 1 and z > 1 (at > 3σ); or a clock drift and a quasar signal that violate the
  tie in item 2 by more than 3σ.
- **DISFAVOURED (Twist dark energy as a whole)**: an equivalence-principle violation or Cassini-type γ − 1 detected at > 5σ.
Eligible: atomic or nuclear (Th-229) clock results, ELT/ANDES or ESPRESSO quasar results, MICROSCOPE-2 or other EP tests, first
public after this lock. Everything public before the lock is excluded (it was used to size the leak).

## Failure handling
No changes after the lock; corrections only in PREREG_SHIELD_DEVIATIONS.md, written before any scoring.
