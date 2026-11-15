> **SUPERSEDED (7 Nov 2026).** Older model notes; some numbers here are withdrawn or failed. Current model and results: [CURRENT_MODEL.md](CURRENT_MODEL.md).

# The AEGIS model, version 2 (reframed 26 October 2026)

Danny Lee Eldridge. Everything here is organised in two tiers, kept separate on purpose.

| Tier | What it holds | How it is judged |
|---|---|---|
| **1 · Physics** | The Twist and the Fingerprint | Telescope data, against the standard model, with a penalty for every extra setting |
| **2 · Framework** | The Sigil Model ("mechanism first") | Orbits, exoplanets and chance, against randomised data |

Beliefs and values are kept out of this model entirely; only what can be tested against data is listed.

---

## Tier 1 · The Twist (torsion-born early dark energy)

**Equations**

```
S = ∫ d⁴x √−g [ M_Pl² R/2 − ½(∂φ)² − V(φ) ] + S_matter
φ = √(3/2) M_Pl · arsinh(1/γ)                        (γ = Barbero–Immirzi parameter)
V(φ) = Λ⁴ [1 − cos((φ − φ₀)/F)]³ ,  φ₀ = 2.63 M_Pl  (rest point at γ₀ = 0.2375)
Fingerprint:  (φ − φ₀) → g(φ) = s[sinh(φ/s) − sinh(φ₀/s)]/cosh(φ₀/s),  s = √(3/2) M_Pl
```

**Coupling (decided 7 Nov 2026, hypothesis tier):** the Twist couples through the **Nieh–Yan** term, so the canonical
field is linear, φ = √(3/2) M_Pl β, and the predicted potential is the plain cosine in the displacement d (the form
every fit already uses), with F = (4/π)√(3/2) M_Pl at a Planck-length Nieh–Yan scale. The arsinh map and the
Fingerprint above are the **Holst** alternative; the Fingerprint's locked rule now also tests the choice. Details:
`theory/COUPLING_CHOICE_NIEH_YAN.md`.


**Field convention (fixed 26 Oct after Copilot's review):** the code variable is the displacement d = φ_abs − φ₀, with φ₀ = 2.63 M_Pl at γ₀ = 0.2375. The implemented potential is V = Λ⁴[1 − cos(d/F)]ⁿ, minimum at d = 0. The Fingerprint maps d through g(d) = s[sinh((d + φ₀)/s) − sinh(φ₀/s)]/cosh(φ₀/s), s = √(3/2) M_Pl.

**Planck PR4 (corrected):** likelihood-only Δχ² = +0.09 (no improvement); the earlier −3.4 included Gaussian foreground priors and is withdrawn. H₀ 70.29 vs 67.63.

**Status (corrected 28 Oct 2026; Planck 2018 + DESI DR2 + Pantheon+, no SH0ES; one engine, CAMB 2.0.5 + Cobaya, converged):** against the best ΛCDM (χ² 2433.58, H₀ 68.33): free Twist Δχ² = −3.84, ΔAIC = +2.16, H₀ = 69.65, f_EDE ≈ 0.048; Locked Twist (best of 8) Δχ² = −3.96, ΔAIC = +0.04, ΔBIC = +11.2, H₀ = 69.93, f_EDE ≈ 0.057. A tie on AIC, disfavoured on BIC; no detection is claimed. The earlier Δχ² = −6.5 / H₀ = 70.60 / f_EDE = 0.078 came from a different engine and unconverged runs and is withdrawn.

**Theory review and evidence boundary (3 Nov 2026).** The current data support studying an EDE-shaped expansion history, not a torsion explanation or a robust victory over ΛCDM. The broader comparison in `cmb-fit/results/COMPARE.md` is dataset-dependent: the blind P-ACT fit has ΔAIC = −3.23 for the two-extra-parameter locked model, while the SPT-3G comparison has ΔAIC = +2.73; several supernova substitutions give modest AIC improvements but BIC penalties around +10. This is not a uniform preference, and a best-fit Δχ² is not evidence by itself. Independent recent AEDE analyses likewise report no statistically significant preference over ΛCDM from CMB-only data ([Khalife et al., Phys. Rev. D 113, 103546 (2026)](https://doi.org/10.1103/8jjr-7hpb)).

The torsion-to-potential step remains the decisive theoretical gap. `theory/bi_kahler_lambda.py` derives a field-space metric and kinetic coupling; it does not derive the cosine potential, its power n = 3, its period F, or the release redshift. The explicit constant-superpotential calculation in `theory/bi_superpotential.py` yields a negative potential at its GR point, V(ϕ = −1/2) ≈ −1626.93 W², rather than the positive EDE potential used in the fits. Its ϕ = −2/3 minimum is only local, the potential is unbounded below as ϕ → 0⁻, and its positive branch has negative signed slope s = −d ln V/dχ in the stated canonical-field orientation. It does not derive either the exponential uplift or the periodic Twist potential. The pre-registered torsion value F = √(3/2) M_Pl failed, so allowing F to vary makes the successful fit phenomenological EDE, not evidence for torsion.

**Improvement path (no data-driven retuning):** derive a positive, stable periodic potential from an explicit symmetry-breaking or non-perturbative sector, fixing F, n and the amplitude before cosmological fitting; show that the same action recovers the GR/solar-system limit and has stable perturbations; then compare against ΛCDM with converged, marginalized posteriors, the same nuisance treatment and independent CMB/SN/BAO/lensing combinations. Until those gates pass, retain the present model as a falsifiable EDE phenomenology and do not claim that it beats ΛCDM or that torsion is its established origin.

**Separate quantum-input/scalar-dynamics branch (new background calculation).** `theory/bi_qcd_axion.py` uses the leading low-energy QCD-anomaly potential \(V(\theta)=\chi_{\rm QCD}[1-\cos\theta]\), with the susceptibility supplied as an external effective input. `theory/bi_qcd_dynamics.py` now evolves the homogeneous \(n=1\) field from \(H=m/3\), includes its contribution to the Friedmann constraint and Hubble friction, and transitions to a WKB-averaged matter-like density once \(m/H\) is large. For the documented defaults, it solves for the initial angle that yields a requested 5% scalar fraction at equality. That target is normalization, not evidence from data. This branch is distinct from the phenomenological \(n=3\) Twist EDE model: it does not calculate the QCD susceptibility from quantum fields, evolve the dilaton, include scalar perturbations, or evaluate CMB/BAO/SN likelihoods. Since the oscillating field is CDM-like by equality, replacing an equal CDM density leaves the homogeneous background degenerate with ΛCDM; no \(\Delta\chi^2\) is reported. A genuine model-selection comparison requires implementing and validating this field's perturbations in the Boltzmann solver first.

**Decision tree, written before the results**

| Outcome | Verdict | Next |
|---|---|---|
| F fixed at 1.2247 M_Pl passes (Δχ² ≤ −4 vs ΛCDM) **and** the Fingerprint fits at least as well as the plain cosine | Torsion origin gains support | Write up for arXiv; ask for expert review |
| F fixed fails, free fit still improves | Survives as generic early dark energy | The torsion link needs a new derivation of F |
| Planck PR4 + ACT shows no improvement (Δχ² > −2) | Disfavoured | Say so on the page; keep the code public |

**Open problems (stated, not hidden)**
1. Derive V and its period from the Holst / Nieh–Yan terms. Lead: φ ∝ arsinh(1/γ) is a hyperbolic angle and γ weights the term mixing boosts and rotations; test whether Lorentz-group structure fixes the period.
2. Why the field switches on near matter–radiation equality: candidate trigger is its coupling to the axial (spin) current of fermions, −(3/4) ⋆J_A ∧ dγ̄.
3. The near-hilltop start.
4. **Stability: the bridge to Tier 2.** After z_c the field is a nonlinear oscillator (frequency ∝ amplitude² for n = 3). Floquet analysis of its fluctuations decides whether it locks into resonance and fragments (oscillons). That is the Sigil "Lock" inside the cosmology.

---

## Tier 2 · The Sigil Model, mechanism first

**Statement.** Order appears only where a physical mechanism acts long enough to lock it in. Where no mechanism acts, there is only chance.

**Definitions**
- A pair of cycles with periods P₁ < P₂ is *near-resonant* when the ratio r = P₂/P₁ lies just wide of a simple ratio p/q: 0 ≤ r/(p/q) − 1 ≤ 0.01. A true lock also needs the resonant angle φ_res = pλ₂ − qλ₁ − (p − q)ϖ to librate.
- **Lock excess** of a population: E = f_obs / f_null, where f is the fraction of near-resonant pairs and f_null comes from a smooth version of the same population (kernel-smoothed ln r, bandwidth 0.08).
- **Mechanism strength**: dissipation × time. Candidates: convergent migration in the birth disc, tidal dissipation, gas drag.

**Predictions and results**

| # | Prediction | Result | Status |
|---|---|---|---|
| A | Exoplanet pairs sit just wide of 2:1, 3:2, 4:3, 5:4 more than chance | 1,153 adjacent pairs in 1,067 systems (NASA Exoplanet Archive): E = 2.11, p < 0.0001; peaks just wide and troughs just inside each ratio | **Passed** |
| B | The excess is larger where tides are strongest (inner period < 10 days) | Compact E = 1.90, wide E = 2.42; difference −0.015 (95%: −0.043 to +0.015) | **Not supported**: tides alone are not the main mechanism |
| C | The golden ratio is not a general law of orbits | Planets p = 0.066, U-238 chain p = 0.84 | Supported |
| D | Systems with no mechanism show no order | Lottery: 105 tests, none survive correction; Moon on draws not reproduced | Supported |
| E | Our own Moon sets real rhythms | Tides (measured); Metonic 19-year cycle (exact to ~2 hours) | Established physics |

**Amendment from B.** The locking mechanism for planets is mainly **convergent migration while the planets were still in their birth disc**, with tides a smaller, later effect. Revised, pre-registered next prediction: near-resonant pairs in compact systems should sit *further* wide of exact resonance (tidal dissipation pushes them out). First look: median offsets 1.06% (compact) vs 1.00% (wide), too close to call; needs the proper test.

**What the model does not claim.** It does not claim planets steer human fate, lottery draws or emotions. Where it was tested on those, it found nothing, and says so.

---

## The solar-cycle question (Tier 2, open)

Mean period of solar minima 1755–2020: 11.070 yr; Venus–Earth–Jupiter tidal period: 11.07 yr. But 281 planet-made periods fall between 9 and 13 yr, nine within 0.05 yr of 11.07, and cycle lengths behave like a random walk (lag-1 r = +0.10). Only Mercury, Venus, Earth and Jupiter exert meaningful tides. Status: open; next test is the multi-millennial ¹⁴C / ¹⁰Be record.

---

## Guardrails (automatic, on the monitor page)

Fit numbers recomputed from checkpoints; pre-registration files hash-locked; theory self-checks; ESA spot-checks; geometry needs ≥ 3σ and ≥ 25% of sky, with the Galactic-Centre pull flagged as expected; sigil fingerprints.

## Still missing (as of this version)

1. Derivation of V and its period (Tier 1, top priority).
2. Floquet stability of the oscillating field (the Tier 1–2 bridge).
3. Full MCMC posteriors; weak-lensing likelihood for S₈; SPT; direct birefringence check.
4. A Milky Way model to subtract before reading any direction from the onion sweep.
5. Libration check (not just ratios) for the exoplanet locks, with N-body fits where data allow.
6. The millennial solar record.
7. Outside expert review; public GitHub and Zenodo DOI.
