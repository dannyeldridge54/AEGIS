# The Twist — model card v5 (13 Nov 2026, afternoon; corrected 13:20 after an independent referee review)

**This card is the single source of truth for every number.** Where REVIEW_GUIDE.md, COVERAGE.md or older notes differ, this card wins.

One page: the model as it now stands, every number we chose, every assumption we added, and what would prove it wrong.
Development numbers (D…) point to theory/pending_docs/D72_D75_weak_spots.md. Consistency pass: field_tests/results/consistency_v5.txt.

## The model
- Kähler potential: K = −3 ln(T + T̄ − SS̄(1 + (T + T̄)/2μ) + ζ(SS̄)²)   (D72, D81, D127)
- Superpotential: W = √3 m S T exp(−n(1 − e^{−πT/4}))   (D79 cliff, D126 origin)
- Reheating field χ: W ⊃ (h/2)(1 − e^{−2π(T − T₀)})χ², decays through Planck-suppressed operators linear in χ   (D105, D110, D118)
- Standard Model: non-supersymmetric, outside the supergravity sector, minimally coupled in the Einstein frame   (D104)
- Hidden sectors: SU(8) (gives e^{−πT/4}); two copies of G₂ swapped by Z₂ (S → −S) form the racetrack that gives W   (D119, D126)

## Numbers
| Number | Value | Status |
|---|---|---|
| n (cliff depth) | ≈ 125 (124.6 reproduces ρ_DE) | **chosen** — a tuning of today's dark energy (Δn ≈ 0.35 per factor 2 in ρ_DE); = 2πκ/N₂ in D126 |
| m (inflaton mass) | 2.1×10⁻⁵ M_P | fixed by A_s; **related** to a gauge coupling (e^{−b(f₀−κ)}, α₂ ≈ 0.005–0.03), at the cost of a ~7% cancellation between b f₀ ≈ 134 and n = 125 (D126, D136) |
| 4/π in the cliff | 2π/8 | **assumed** (SU(8) condensate form; the SU(8) coupling is strong, g² ~ 10²–10⁴, through all of inflation, so the formula is outside control — D136) |
| μ | 1 | chosen (constant term in S's metric, D127) |
| ζ | ≳ 3×10⁴ | chosen (lower bound from S stability) |
| m_σ (hidden axion) | ≈ 6×10¹⁰ GeV (refit) | chosen to fit the matter amount; confirmation run pending (D124) |
| h, x₀ (χ mass) | h 0.2–1 M_P, x₀ 0.02–0.1 | chosen, matched to the 0.8% heat share (D118) |
| Heat share | ≈ 0.65–0.8% | derived from χ's decay (D105, D118) |

## Assumptions added beyond the original model (each is a place it could fail)
1. **No coupling between the tail field and the Standard Model** — now a named symmetry: the SM is neutral under both isometries of the T-disk (scaling and shift), broken only by the cliff's instanton (passes every test by ≥10¹⁹, D140–D142) and by perturbative leaks, which must fall as 1/x⁴ or faster (atomic clocks). Locked: PREREG_SHIELD. Previously: needs an unexplained symmetry. The D110 argument that lets χ decay also generically gives (φ/M_P)·O_SM couplings with β = O(1), excluded by Cassini. **The fifth force is the main open problem** (D135).
2. χ → −χ broken at the Planck scale (D110) — needed for χ to decay.
3. χ's mass saturates via a single instanton, or an SU(2) condensate with SM loops cut off below ~10¹⁶ GeV (D118, D128) — needed for the tail's quantum stability.
4. The Z₂ racetrack of two hidden G₂ groups with the operator Tr W₈² Tr W₂²/M_P³, coefficient ~20 N₂ (D119, D126).
5. **Where T lives** (D150–D152): in type IIB a rung-3 volume modulus moves the string scale and couples to matter at Planck strength (excluded). Working candidate: the heterotic string on the Z₃ orbifold, where T is the overall modulus (K = −3 ln, rung 3) but the string scale is set by the dilaton, Z₃ has no T-dependent gauge thresholds, untwisted Yukawas are T-independent and twisted ones instanton-suppressed — matter is neutral as the shield needs. Open: dilaton stabilisation, the cliff's form in heterotic language, higher-order Kähler corrections (must fall as 1/x⁴).
6. γ is the self-dual value for black-hole entropy (D120) — a choice; LQG link is motivation only.
7. Dark matter is a gravity-only fermion; its 100–500 TeV mass needs χ̃ to decay to SM fermions (D112).

## Predictions (falsifiers)
Matter (m_σ) and dark-matter (100–500 TeV) numbers are left out until they stop moving. The late-time test is generic thawing
quintessence with λ = √(2/3): the supergravity structure plays no role in it. DR3 is cumulative with DR2, so it is a weaker
out-of-sample test than a new survey.
| Observable | Twist | Kills it |
|---|---|---|
| Dark energy | w0 ≈ −0.90, wa ≈ −0.14, insensitive to heat share (D125) | w0, wa pinned at ΛCDM (−1, 0) by DESI/Euclid |
| n_s, r | n_s ≈ 0.964–0.965 (loop shift negligible with the saturating χ, D156), r ≈ 0.0036 | n_s ≥ 0.973 at > 3σ (D108); r > 0.0112 detected at > 3σ, or r < 0.0030 at 95% |
| GW propagation | Ξ₀ = 1, no birefringence (locked: PREREG_GW_FRICTION) | Ξ₀ ≠ 1 measured |
| Extra radiation | ΔN_eff ~ 3×10⁻⁸ | — |

## Results today that went against the model (kept on record)
- TAIL-F: full tail disfavoured (Δχ² +29) with the old cliff → cliff reshaped (post hoc, labelled).
- D102: y = 4 / γ = 1/4 hypothesis FAILS.
- D109: n ≈ 124 leads fail.
- D124: matter at 0.8% heat 7.53× (prediction 2–3× MISSED).

## Open
The fifth force (main open problem, D135) · isocurvature unverified until D137 · initial conditions: only near-rest starts at
x ≈ 10⁻⁵–10⁻⁴ (fast starts sit where S is tachyonic, D136) · n not derived · inhomogeneous starts only by analogy · SU(8) strongly coupled on the far plateau · m_σ confirmation pending.

## Consistency pass (final form, one run)
V identical to the old form for real T · N* 55.7 (instant), n_s 0.9642, r 0.0038 · tail at 0.8%: x frozen 73, today 89, w0 −0.902, wa −0.142 ·
angle mass +8H² at the CMB point and today · S mass 30 H² (CMB point), 2600 H² (today). All pass.

## Separate model: TWIST-P (locked 12:23 and 12:25; PREREG_TWISTP.md, PREREG_TWISTP_L.md, deviation D1)
A DIFFERENT model, built after seeing the n_s data — D108 says the Twist's own Kähler potential cannot reach n_s ≈ 0.973;
TWIST-P changes it. Construction: the Twist plus one Kähler term β/(T + T̄) that reshapes only the deep plateau (a polynomial attractor there); V along real T is
unchanged. Built after seeing the n_s data, so only post-lock CMB results can score it. Prediction: n_s 0.965–0.971 (+ loops
≤ 0.974) with r 0.0036–0.011 rising together; it does not reach n_s = 0.974 at tree level. Isocurvature: estimated safe (D134), unverified until D137; if D137 fails for the angle, only the β ≤ 2.2×10⁻³ segment stands.
