# The Twist — model card v5 (13 Nov 2026, afternoon)

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
| n (cliff depth) | ≈ 125 | **chosen** — sets today's dark energy (plays Λ's role); = 2πκ/N₂ in D126 |
| m (inflaton mass) | 2.1×10⁻⁵ M_P | fixed by A_s; **explained** as e^{−b(f₀−κ)} from a weak coupling α₂ ≈ 0.005–0.03 (D126) |
| 4/π in the cliff | 2π/8 | **derived** from SU(8) |
| μ | 1 | chosen (constant term in S's metric, D127) |
| ζ | ≳ 3×10⁴ | chosen (lower bound from S stability) |
| m_σ (hidden axion) | ≈ 6×10¹⁰ GeV (refit) | chosen to fit the matter amount; confirmation run pending (D124) |
| h, x₀ (χ mass) | h 0.2–1 M_P, x₀ 0.02–0.1 | chosen, matched to the 0.8% heat share (D118) |
| Heat share | ≈ 0.65–0.8% | derived from χ's decay (D105, D118) |

## Assumptions added beyond the original model (each is a place it could fail)
1. SM outside SUGRA, minimally coupled (D104) — needed for the fifth force.
2. χ → −χ broken at the Planck scale (D110) — needed for χ to decay.
3. χ's mass saturates via a single instanton, or an SU(2) condensate with SM loops cut off below ~10¹⁶ GeV (D118, D128) — needed for the tail's quantum stability.
4. The Z₂ racetrack of two hidden G₂ groups with the operator Tr W₈² Tr W₂²/M_P³, coefficient ~20 N₂ (D119, D126).
5. T behaves like a volume-type modulus for the distance conjecture (D123) — passes, but floors the plateau at x ≈ 6×10⁻⁶.
6. γ is the self-dual value for black-hole entropy (D120) — a choice; LQG link is motivation only.
7. Dark matter is a gravity-only fermion; its 100–500 TeV mass needs χ̃ to decay to SM fermions (D112).

## Predictions (falsifiers)
| Observable | Twist | Kills it |
|---|---|---|
| Dark energy | w0 ≈ −0.90, wa ≈ −0.14, insensitive to heat share (D125) | w0, wa pinned at ΛCDM (−1, 0) by DESI/Euclid |
| n_s, r | n_s ≈ 0.965 (0.965–0.968 with loops), r ≈ 0.0035 | n_s ≥ 0.974 (D108); r ≫ 0.004 or no r at ~0.003 by LiteBIRD/CMB-S4 |
| GW propagation | Ξ₀ = 1, no birefringence (locked: PREREG_GW_FRICTION) | Ξ₀ ≠ 1 measured |
| Dark matter | no direct-detection signal | a WIMP-like signal |
| Extra radiation | ΔN_eff ~ 3×10⁻⁸ | — |

## Results today that went against the model (kept on record)
- TAIL-F: full tail disfavoured (Δχ² +29) with the old cliff → cliff reshaped (post hoc, labelled).
- D102: y = 4 / γ = 1/4 hypothesis FAILS.
- D109: n ≈ 124 leads fail.
- D124: matter at 0.8% heat 7.53× (prediction 2–3× MISSED).

## Open
n not derived · inhomogeneous starts only by analogy · SU(8) strongly coupled on the far plateau · m_σ confirmation pending.

## Consistency pass (final form, one run)
V identical to the old form for real T · N* 55.7 (instant), n_s 0.9642, r 0.0038 · tail at 0.8%: x frozen 73, today 89, w0 −0.902, wa −0.142 ·
angle mass +8H² at the CMB point and today · S mass 30 H² (CMB point), 2600 H² (today). All pass.

## Companion model: TWIST-P (locked 12:23 and 12:25; PREREG_TWISTP.md, PREREG_TWISTP_L.md)
Same model plus one Kähler term β/(T + T̄) that reshapes only the deep plateau (a polynomial attractor there); V along real T is
unchanged. Built after seeing the n_s data, so only post-lock CMB results can score it. Prediction: n_s 0.965–0.971 (+ loops
≤ 0.974) with r 0.0036–0.011 rising together; it does not reach n_s = 0.974 at tree level. Isocurvature safe (D134).
