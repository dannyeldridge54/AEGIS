# Weak lensing: options 3 and 4 worked through on paper (8 Nov 2026)

AI-assisted working note, not a test and not a rule. The question for each: can the Twist lower S8 **without a new
free parameter**? If not, a test is still possible, but it adds a parameter and is scored with ΔAIC beside it.

## Why the Spiral raises S8
In the Spiral, dark matter's mass follows the dilaton, m_c ∝ e^{β_eff φ} (`cmb-fit/axiclass/coupled/patch_coupling.py`).
Its perturbation equation gets a fifth-force term (+β_eff k² δφ in θ_c'), which pulls matter together faster than
gravity alone. β_eff ≈ 0.04–0.05 at the best fits, and SF2 shows the supernova fit needs it. The cost is S8 ≈
0.833–0.840 against ≈ 0.817 for ΛCDM on the same data.

## Option 3: a coupling that moves momentum instead of energy
Momentum-only couplings ("dark scattering", Pourtsidou et al. 2013 type 3) slow clumping instead of speeding it up.
- The Nieh–Yan term couples the BI angle to torsion: θ d(e^a ∧ T_a) → after integrating by parts, ∂_μθ times the axial
  torsion. Solving for torsion with matter present gives a coupling ∂_μθ J5^μ to the **axial (spin) current** of
  fermions.
- For cold, non-relativistic, unpolarised dark matter, J5 averages to zero, and scalar dark matter has no J5 at all.
  So this route gives **no momentum exchange with dark matter** on cosmological scales. The Holst route behaves the
  same way.
- **Conclusion:** not produced by the theory. A momentum coupling would be an added assumption with its own strength
  parameter (+1). Possible to test, but it would be fitting a fix rather than deriving one. Not recommended as next.
  (Our derivation; worth checking against Mercuri 2009 and Taveras & Yunes 2008 before relying on it.)

## Option 4: the angle's share of dark matter is light and smooths small clumps
If the matter-like angle (share f = β_eff/0.816 ≈ 5–6%) is an ultralight field, it does not clump below its Jeans
length. That lowers small-scale power and S8. With f ≈ 5% and mass around 10⁻²⁶–10⁻²⁵ eV the drop in σ8 is a few
percent, which is the size of the Spiral's excess, and is near the edge of what CMB data allow for that fraction
(Hlozek et al.; Rogers et al. 2023).
- Can the early role fix that mass? No. The early angle uses (1 − cos)³, which near its minimum is ∝ θ⁶: it oscillates
  like a fluid with w = 1/2 and fades as a^{−4.5}. That is why the early boost dies away, and it also means the early
  oscillation cannot be the dark-matter share.
- The late share's mass is set by its own potential height and starting angle, neither fixed by λ or F.
- **Conclusion:** physically natural and literature-backed, but the mass is **one new free parameter**. A test needs a
  second field in the engine (AxiCLASS ultralight-axion module beside the coupled dilaton), which is a real build.

## Where this leaves things
- Option 1 (joint fit, `DRAFT_PREREG_S8_JOINT.md`) adds no physics and is ready to lock.
- Option 2 (survey split, done, reported only): `results/s8_survey_split.json`.
- Options 3 and 4 each cost a parameter. Option 4 is the stronger candidate if one is tried.
