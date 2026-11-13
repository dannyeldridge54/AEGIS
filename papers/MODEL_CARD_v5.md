# The Twist — model card v5 (13 Nov 2026, afternoon; corrected 13:20 after an independent referee review)

**This card is the single source of truth for every number.** Where REVIEW_GUIDE.md, COVERAGE.md or older notes differ, this card wins.

One page: the model as it now stands, every number we chose, every assumption we added, and what would prove it wrong.
Development numbers (D…) point to theory/pending_docs/D72_D75_weak_spots.md. Consistency pass: field_tests/results/consistency_v5.txt.

## The model — main construction: TWIST-K (adopted 13:56; D159)
- Kähler potential: K = −3 ln(T + T̄ − g E(T+T̄) SS̄ + ζ E(T+T̄)² (SS̄)²),  g = 1 + (T+T̄)/2μ,  E(u) = exp(2n(1 − e^{−πu/8}))
  (the cliff lives in S's metric; e^{−πx/4} = |q| is the form of a worldsheet-instanton correction)
- Superpotential: W = √3 m S T  (W = 0 at S = 0, so the gravitino is massless)
- Reheating field χ: W ⊃ (h/2)(1 − e^{−2π(T − T₀)})χ², decays through Planck-suppressed operators linear in χ   (D105, D110, D118)
- Standard Model: neutral under the isometries of the T-disk (the shield, D140–D142)
- Potential along real T identical to the earlier form (checked to 10 digits in full supergravity); every inflation and late-time
  observable is unchanged. The angle is +4H² everywhere (no cliff tachyon); matter is being recomputed (D160).

Alternative construction (kept on record): W = √3 m S T exp(−n(1 − e^{−πT/4})) with the cliff from a hidden SU(8) and a Z₂
racetrack of two G₂ groups (D119, D126, D148), K without E. Same potential along real T; needs a hidden gauge coupling linear in T,
which no known string setting provides together with a neutral Standard Model (D154).

## Numbers
| Number | Value | Status |
|---|---|---|
| n (cliff depth) | ≈ 125 (124.6 reproduces ρ_DE) | **chosen** — a tuning of today's dark energy (Δn ≈ 0.35 per factor 2 in ρ_DE); = 2πκ/N₂ in D126 |
| m (inflaton mass) | 2.1×10⁻⁵ M_P | fixed by A_s; **related** to a gauge coupling (e^{−b(f₀−κ)}, α₂ ≈ 0.005–0.03), at the cost of a ~7% cancellation between b f₀ ≈ 134 and n = 125 (D126, D136) |
| π/4 in the cliff | |q| = e^{−πx/4} (worldsheet-instanton form; alternatively 2π/8 from SU(8)) | **assumed** (SU(8) condensate form; the SU(8) coupling is strong, g² ~ 10²–10⁴, through all of inflation, so the formula is outside control — D136) |
| μ | 1 | chosen (constant term in S's metric, D127) |
| ζ | 3×10⁵ (was 3×10⁴) | chosen; raised for lumpy-start robustness (D217–D218): S stable for x > 1/(4ζ) = 8×10⁻⁷, 6.2 M_P of plateau beyond the CMB point; re-run: V unchanged to 10 digits, angle +4H², m_S²/H² 310–6×10⁵ along the path; no prediction changes |
| m_σ (hidden axion) | ≈ 6×10¹⁰ GeV (refit) | chosen to fit the matter amount; confirmation run pending (D124) |
| h, x₀ (χ mass) | h 0.2–1 M_P, x₀ 0.02–0.1 | chosen, matched to the 0.8% heat share (D118) |
| Heat share | ≈ 0.65–0.8% | derived from χ's decay (D105, D118) |

## Assumptions added beyond the original model (each is a place it could fail)
1. **No coupling between the tail field and the Standard Model** — now a named symmetry: the SM is neutral under both isometries of the T-disk (scaling and shift), broken only by the cliff's instanton (passes every test by ≥10¹⁹, D140–D142) and by perturbative leaks, which must fall as 1/x⁴ or faster (atomic clocks). Locked: PREREG_SHIELD. Previously: needs an unexplained symmetry. The D110 argument that lets χ decay also generically gives (φ/M_P)·O_SM couplings with β = O(1), excluded by Cassini. **The fifth force is the main open problem** (D135).
2. χ → −χ broken at the Planck scale (D110) — needed for χ to decay.
3. χ's mass saturates via a single instanton, or an SU(2) condensate with SM loops cut off below ~10¹⁶ GeV (D118, D128) — needed for the tail's quantum stability.
4. The cliff is a worldsheet-instanton correction to S's Kähler metric whose resummed size at small volume is 2n ≈ 250 (TWIST-K, D159, D161). (Alternative: the Z₂ racetrack of two hidden G₂ groups, D119/D126.)
5. **Where T lives** (D150–D152, D164, D184–D202): type IIB is excluded — its only rung-3 field is the overall volume, which sets M_s/M_P, so even sequestered D3 matter couples with β ≈ 0.61 (D192). Candidate home: **weakly coupled heterotic on a Z₃-type orbifold**, with (a) a Γ₀(9) duality group so the plateau and the tail are different cusps (D194); (b) the cliff built from the Γ₀(9) hauptmodul to the 9th power, so its leftover starts at degree 9 by symmetry; but the computed post-inflation roll leaves today at g_s ≈ 8 even at 50% reheating and ≈ 4400 at the Twist's 0.8% — weak coupling today is NOT reached (TWIST-M9, D196–D197, D204; locked PREREG_TWISTM9). No heterotic realisation tried is weakly coupled today; the string home is open. **Examined and failed (D205–D208): heterotic M-theory** (strong coupling, where the field actually is): symmetric vacua (c₂(V₁) = c₂(V₂) = ½c₂(TX), no five-branes) have no gauge thresholds and no matter-metric corrections, no exact T-duality, and membrane instantons as a cliff source — but the matter-neutral direction is rung 4, giving r ≈ 0.0046 and w0 −0.925 (locked PREREG_TWIST4) — but D208: that rung-4 path moves Re S and the SM coupling (d ln α/dφ ≈ 0.71), so it is not matter-neutral; CY shape moduli at fixed volume are neutral but give a steep tail (λ ≈ 1.15, w0 ≈ −0.79). No string home survives; the shield remains an effective-theory assumption; (c) the duality-invariant dilaton fixed by a pure hidden E₈ with BGW Kähler stabilisation (b_a = b), which keeps T flat under the hidden sector and the gauge couplings T-independent (D200; a condensate racetrack instead would make α drift, D198–D199); (d) the hidden sector decouples from the Twist at tree level, loops harmless (D201); m_3/2 ~ 10¹⁴ GeV in BGW's example — dilaton stable in inflation, no collider SUSY (D202). Not derivable there: n (instanton sums give ~10⁻⁴ of what is needed, D189; warping is IIB-only, D190–D191). Cost: TWIST-M9 lowers n_s to 0.957–0.965. Open: Γ₀(9) version of BGW; cliff form as an actual worldsheet computation.
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

## Known costs
- Strong CP is not solved (the angle would overproduce axion dark matter, D172); neutrino masses are assumed (seesaw scale fits the Twist's scales, D173).
- Late ISW 5% stronger than ΛCDM (D172b).
- Hubble tension: the Twist lowers the CMB-inferred H₀ to ≈ 65.7 km/s/Mpc (ΛCDM 67.4), moving away from local ~73 (D169).
- Growth: σ8 1.5% lower and f σ8 3% lower at z ≈ 0.4 than ΛCDM at fixed Ω_m (D168, locked PREREG_GROWTH) — helps the S8 tension slightly.

## Results today that went against the model (kept on record)
- **D157: NS-SPA INCONSISTENT** — n_s fixed at 0.964 costs Δχ² 11.7 vs CMB-SPA + DESI (ΛCDM 8.5); PURE-TWIST free fits this set +1.45 worse than ΛCDM.
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

## Separate model: TWIST-L (locked 13:59; PREREG_TWISTL.md)
TWIST-K plus a logarithmic factor in S's metric (an IR-free running coupling at a T-set scale, D163). Keeps rung 3. Predicts n_s 0.965–0.979 with r 0.0036–0.014 rising together (lower r than TWIST-P at the same n_s). Built after seeing the n_s data; scored only on future CMB results.
