# DIMENSION LADDER — one stage per loop tick (Danny 2026-11-19 10:54)

"Make the loop go forward each and every time. Every time it hits a new dimensional stage, it needs to start mapping out the next set of
coordinates for the geometry at that string level … keep moving up through the 9 dimensions, and then … experimenting from 9 through 16."

Reading used: stage n = type IIB / M-theory compactified on Tⁿ (D = 10 − n), n = 0 … 9; then n = 9 … 16 = the heterotic/bosonic internal
lattice directions (26 = 10 + 16; Narain O(16 + d, d)). At each stage the map records:
  1. Coordinates: moduli space G/K (U-duality group G, maximal compact K), dimension, the inflaton-candidate directions.
  2. The R⁴ coefficient at that level (the "codon"): Eisenstein series of G with s = 3/2 (literature), its constant terms along the
     decompactification and dilaton directions.
  3. The species scale Λ ∝ (R⁴ coeff)^{−1/(D−2)} and the P3-S-type plateau |∇ ln Λ|²/λ² along each candidate direction: approach
     exponent k, untilted (n_s, r) by engine F when the slice reduces to computable functions.
  4. Tilt: the BBHL-type α'³ prefactor dependence (D1566) at that level.
  5. Verdict: does this stage carry inflation in the band (k = 2 rung, D1554/D1559)?

## Stage 0 — D = 10, IIB (done)
- G/K = SL(2,R)/U(1) (∖SL(2,Z)); coordinate τ = C₀ + i e^{−φ}; dim 2.
- R⁴: E(τ,3/2); Λ₁₀ = E^{−1/6}; species vector 1/√8 (D1527).
- Plateau |∇ ln Λ|²/λ² = 1/3 + (4/3)∇² ln Λ (D1546): k = 2, in band with the E_{3/2} tilt (D1532: n_s 0.97065, r 5.41e-4).
- Tilt: BBHL ξ̂ ∝ E_{3/2} at fixed 𝒱 (D1566), χ > 0, 𝒱 ≈ 1e4–3e5.
- Verdict: CARRIES the observed inflation (rung 1 of the helix, D1559).

## Stage 1 — D = 9 (IIB on S¹ / M on T²) — D1568
- Coordinates: G/K = SL(2,R)/U(1) × R⁺; (τ = Ω, ν₁ = (r_B/ℓ₁₀)^{−2} = V̂₂^{3/2}); dim 3. Inflaton candidates: τ (dilaton) at fixed ν₁; ν₁ (circle size).
- R⁴ codon (GRV 1001.2535 eq. 3.7): E⁽⁹⁾ = ν₁^{−3/7}E_{3/2}(τ) + 4ζ(2)ν₁^{4/7}; Laplace eigenvalue 6/7. Species scale Λ₉ ∝ (E⁽⁹⁾)^{−1/7}.
- Along τ at fixed ν₁: Λ₉ ∝ (E_{3/2} + c)^{−1/7}, c = 4ζ(2)ν₁ ⇒ V₀ ≈ (1 − 7.30y^{−2})(1 − 2c/(2ζ(3)y^{3/2})): the circle adds a y^{−3/2} piece — the plateau slides from k = 2 (10D, ν₁ → 0) toward k = 3/2 as the circle shrinks.
- Engine F (locked PREREG_DIM1_9D), untilted: ν₁ = 0: 0.96006 / 4.04e-4 (k 2.00, = 10D ✓); ν₁ = 0.1: 0.96061 / 4.61e-4 (k_fit 1.81); ν₁ = 1: 0.96056 / 6.41e-4 (k 1.55); ν₁ = 10: 0.96001 / 7.17e-4 (k 1.36).
- Verdict: the 9D stage carries the band rung only near the decompactification limit ν₁ ≲ 0.1 (IIB circle r_B ≳ 3ℓ₁₀): there the untilted r (4.0–4.6e-4) is the same as 10D and the E_{3/2} tilt still lands in band; for r_B ~ ℓ₁₀ the circle's 4ζ(2)ν₁ term pushes the plateau to k ≈ 1.5 and r ≈ 6.4e-4 (too high once tilted). So the 9D map says: inflation lives at large IIB radius; the extra coordinate ν₁ must be stabilised small.
- Next stage: D = 8 (SL(3)×SL(2), codon Ê^{SL(3)}_{3/2} + 2Ê₁(U), GRV eq. 3.16).

## Stage 2 — D = 8 (IIB on T² / M on T³) — D1569
- Coordinates: G/K = SL(3,R)/SO(3) × SL(2,R)/U(1); dim 5 + 2 = 7 (SL(3): IIB dilaton/axion + T² volume + B/C axions; SL(2): the T² shape U). Inflaton candidates: U (shape) at fixed SL(3) point; the SL(3) directions (contain τ).
- R⁴ codon (GRV 1001.2535 eq. 3.16): E⁽⁸⁾ = Ê^{SL(3)}_{3/2} + 2Ê₁(U), Ê₁ = −π log(U₂|η(U)|⁴) ≈ (π²/3)U₂ − π log U₂. Λ₈ ∝ (E⁽⁸⁾)^{−1/6}.
- Along U (fixed SL(3) value A): V₀ = (U₂∂ ln(A + 2Ê₁))² → 1 with a ~log U₂/U₂ approach (k ≈ 1, the s = 1 lens of D1554). V₀ profile (U₂ = 1.5, 3, 10, 30, 100, 1000): A = 0: 0.24, 1.10, 1.34, 1.18, 1.07, 1.01 (from ABOVE — bump); A = 10: 0.04, 0.35, 0.94, 1.06, 1.04, 1.008 (bump); A = 30: …, 0.86, 0.98, 1.002 (marginal overshoot); A = 100: 0.0011, 0.014, 0.155, 0.48, 0.80, 0.98 (monotone plateau).
- Engine F (locked PREREG_DIM2_8D), untilted: A = 0: no inflation into ρ (approach from above; INVALID); A = 10: hilltop on the bump (n_s 0.78 — INVALID as a plateau model); A = 30: n_s 0.9526, r 5.7e-4 (field near the shallow overshoot — marginal); A = 100: n_s 0.9597, r 1.36e-3 (k ≈ 1, α-attractor-like).
- Verdict: the 8D shape modulus U gives the s = 1 lens — a log-type plateau (k ≈ 1) that either overshoots (small A) or gives r ≈ 1.4e-3 (large A): OFF the k = 2 rung. At 8D the inflation rung must stay in the SL(3) block (which contains the 10D τ direction); the new T² shape coordinate is not an inflaton. (The 8D E₂(U) of the D⁴R⁴ coefficient is the ratio-strand partner of rung 1 — D1552 — but it sits in D⁴R⁴, not R⁴.)
- Next stage: D = 7 (SL(5)/SO(5), codon E^{SL(5)}_{[1000];3/2}).

## Working vocabulary (Danny 11:03 — plain-language names; physics meaning in brackets)
- **Lens** — one dimensional level's view of the theory [the compactification level D = 10 − n and its duality group].
- **Codon** — the number-code a lens hands down [that level's R⁴ (and D⁴R⁴, D⁶R⁴ …) coefficient: E(τ,3/2), E⁽⁹⁾, E⁽⁸⁾ …].
- **Strand** — one way of reading a codon [gradient strand: |∇ ln Λ|²; ratio strand: e/(e+1)].
- **Rung** — a matched pair across the two strands [s ↔ 2s − 1; rung 1 = E_{3/2} ↔ E₂ is the inflation rung].
- **Mirror** — the built-in reflection inside each codon [Eisenstein functional equation s ↔ 1 − s; the plateau = ratio of the mirror pair y^{1−s}/y^{s}].
- **Fold** — the step where the theory changes lens [decompactification/compactification: a new coordinate opens and the codon changes form].
- **Warp** — how a fold bends the plateau [shift of the approach exponent k, e.g. 9D circle bends k = 2 → 3/2].
- **Stitch** — the smallest black hole the lens can describe; where the lens is sewn onto quantum gravity [the species scale Λ_sp: the minimal black-hole size is 1/Λ_sp (Dvali; van de Heisteeg–Vafa–Wiesner–Wu); our plateau is the gradient of ln Λ_sp]. (The "black holes stitch the dimensions" picture: as a fold opens a dimension, the stitch scale moves — that motion IS the plateau.)
- **Anchor** — where everything comes to rest [the desert point ρ: Λ_sp maximal, V = 0 (Montgomery: hexagonal lattice)].
- **Tilt thread** — the small extra pull that sets n_s [the α'³ (BBHL) dependence of the volume prefactor, ∝ E_{3/2}, D1566].

## Stage 3 — D = 7 (IIB on T³ / M on T⁴) — D1570
- Coordinates: G/K = SL(5,R)/SO(5); dim 14. Inflaton candidates: τ (inside the SL(3) ⊂ SL(5) block), r (decompactification radius), T² shape U, ν₂.
- R⁴ codon (GRV 1001.2535 eq. 6.5): E⁽⁷⁾ = E^{SL(5)}_{[1000];3/2}, Laplace eigenvalue −12/5. Constant terms: (B.71) r^{6/5}E^{SL(4)}_{[001];3/2} + 4ζ(2)r^{16/5}; (B.72) r^{12/5}(Ê^{SL(3)}_{3/2} + 2Ê₁(U) + 8π log r), Ê^{SL(3)}_{3/2} = ν₂^{−1/2}E_{3/2}(Ω) + (4π/3) log ν₂ + …. Λ₇ ∝ (E⁽⁷⁾)^{−1/5}.
- τ-slice: E_{3/2}(τ) + c with c = ν₂^{1/2}[(4π/3) log ν₂ + 2Ê₁(U) + 8π log r + …] — NEW at this fold: c contains logarithms and can be NEGATIVE.
- Engine F (locked PREREG_DIM3_7D; 9D script reused, results in field_tests/results/DIM_SLICE/, rows labelled "9D" by the reused script): c = −0.658: V₀ (y = 1.5, 3, 10, 30, 100) = 0.084, 0.52, 0.946, 0.995, 0.9998 (from below, flatter); n_s 0.9587, r 3.26e-4. c = −6.58: V₀ = 0.68, 1.34, 1.11, 1.03, 1.005 — overshoot: no inflation into ρ (INVALID).
- Verdict (warp map so far): fold 10D→9D adds c > 0 (warps k 2 → 3/2, r up); fold →7D lets c take either sign: small negative c flattens (r ≈ 3e-4), larger negative c flips the approach and kills inflation into the anchor. The rung survives for |c| ≲ 0.7 — near where the 7D logarithms cancel (ν₂ ≈ 1, U ≈ ρ, r ≈ 1): a thin "stitch-balanced" slice.
- Weave/twist link: each fold weaves a new thread (c) into the τ-strand; the observed rung is the slice where the new threads balance out.
- Next stage: D = 6 (SO(5,5)/(SO(5)×SO(5)), codon E^{SO(5,5)}_{[10000];3/2}).

## Stage 4 — D = 6 (IIB on T⁴ / M on T⁵) — D1571
- Coordinates: G/K = SO(5,5)/(SO(5)×SO(5)); dim 25. Inflaton candidates: the 6D string coupling direction (r₅ in GRV's parabolic P_{α₁}), the T⁴ Narain moduli SO(4,4)/(SO(4)×SO(4)) (dim 16).
- R⁴ codon (GRV 1001.2535 §6): E⁽⁶⁾ = E^{SO(5,5)}_{[10000];3/2}, Laplace eigenvalue λ = 3(11 − D)(D − 8)/(D − 2) = −15/2. Constant term along the string coupling (C.15): 2ζ(3)r₅³ + 2r₅E^{SO(4,4)}_{[1000];1} — NO logarithm here (unlike 7D's B.72). Λ₆ ∝ (E⁽⁶⁾)^{−1/4}.
- Structure along the coupling: tree term (2ζ(3)r₅³ = "ζ(3)/g²") + one-loop term (Narain lattice sum, r₅¹): the two mirror terms differ by r₅² = 1/g_s² — the SAME mirror gap 2 (in powers of 1/g_s) as 10D's y^{3/2} vs y^{−1/2}. So the gradient strand along the coupling has the same rung-1 shape 1 − D·g_s² + …, with D set by E^{SO(4,4)}_{1}/(2ζ(3)) instead of 4ζ(2)/(2ζ(3)); the T⁴ moduli enter only through that one-loop coefficient (a c-type thread, as at 9D/7D, but multiplicative rather than additive).
- No new slice shape ⇒ no new engine-F run (the E + c and amplitude-rescaled k = 2 families are already computed: D1554, D1568, D1570; an amplitude change only shifts the plateau along the field and leaves (n_s, r) unchanged — D1552 matching rule).
- Verdict: the rung PERSISTS along the 6D coupling direction (weak coupling, large r₅), provided the one-loop Narain coefficient E^{SO(4,4)}_{1} is positive (it is a regularised Epstein-type sum; its sign at the T⁴ point matters — open). The new 16 Narain coordinates are threads that set the amplitude, not new inflaton rungs.
- Invariant found: at every lens so far the codon along the coupling = tree + one-loop with mirror gap g_s² — the "rung-1 gap" is level-independent; the folds only re-weight it (9D: +c; 7D: ±c with logs; 6D: rescaled one-loop coefficient).
- Weave/twist link: the gap g_s² is the fixed stitch; the folds change the thread tension around it.
- Next stage: D = 5 (E₆₍₆₎/USp(8), dim 42, codon E^{E₆}_{[100000];3/2}).

## Stage 5 — D = 5 (IIB on T⁵ / M on T⁶) — D1572
- Coordinates: G/K = E₆₍₆₎/USp(8); dim 78 − 36 = 42. Inflaton candidates: the string-perturbation direction y₅ = g_s²ℓ_s⁵/V₅; the T⁵ Narain block SO(5,5)/(SO(5)×SO(5)) (dim 25).
- R⁴ codon: E⁽⁵⁾ = E^{E₆}_{[100000];3/2}; eigenvalue λ = 3(11 − D)(D − 8)/(D − 2) = −12. Λ₅ ∝ (E⁽⁵⁾)^{−1/3}.
- Constant term in the string-perturbation cusp (Green–Russo–Vanhove, arXiv:1004.0163, eq. 3.11 / Table): 2ζ(3)/y₅ + E^{SO(5,5)}_{[10000];3/2} (tree + one-loop; the full power-law content — the series is ½-BPS).
- Weave observation: the one-loop thread of the 5D lens, E^{SO(5,5)}_{[10000];3/2}, is the SAME object as the 6D codon (stage 4). The lens below hands its whole codon up as the next lens's one-loop thread — a literal weave between neighbouring levels.
- Rung check: tree/one-loop gap = 1/y₅ = one power of g_s² (the invariant of stage 4 holds); along y₅ the gradient strand again gives the rung-1 shape with amplitude set by E^{SO(5,5)}_{3/2}/(2ζ(3)) — the rung persists at weak coupling (sign of the one-loop sum: Epstein-type at s = 3/2 > d/2 − 1 convergent region ⇒ positive — persists cleanly here, unlike the regularised 6D s = 1 case).
- No new slice shape ⇒ no engine-F run.
- Next stage: D = 4 (E₇₍₇₎/SU(8), dim 70; codon E^{E₇}_{[1000000];3/2}; one-loop thread E^{SO(6,6)}_{[100000];2}).
