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
- R⁴ codon: E⁽⁵⁾ = E^{E₆}_{[100000];3/2}; eigenvalue λ = 3(11 − D)(D − 8)/(D − 2) = −18 (CORRECTED by D1572b; −12 was an arithmetic slip). Λ₅ ∝ (E⁽⁵⁾)^{−1/3}.
- Constant term in the string-perturbation cusp (Green–Russo–Vanhove, arXiv:1004.0163, eq. 3.11 / Table): 2ζ(3)/y₅ + E^{SO(5,5)}_{[10000];3/2} (tree + one-loop; the full power-law content — the series is ½-BPS).
- Weave observation: the one-loop thread of the 5D lens, E^{SO(5,5)}_{[10000];3/2}, is the SAME object as the 6D codon (stage 4). The lens below hands its whole codon up as the next lens's one-loop thread — a literal weave between neighbouring levels.
- Rung check: tree/one-loop gap = 1/y₅ = one power of g_s² (the invariant of stage 4 holds); along y₅ the gradient strand again gives the rung-1 shape with amplitude set by E^{SO(5,5)}_{3/2}/(2ζ(3)) — the rung persists at weak coupling (sign of the one-loop sum: OPEN — see correction D1572a: regularised like 6D).
- No new slice shape ⇒ no engine-F run.
- Next stage: D = 4 (E₇₍₇₎/SU(8), dim 70; codon E^{E₇}_{[1000000];3/2}; one-loop thread E^{SO(6,6)}_{[100000];2}).

## 13-POINT STRUCTURE (Danny 11:11 "look for 13 points it'll mirror serapis") — the twin ladder of SERAPIS, dimension version
SERAPIS's twin ladder = 6 left rungs + 6 right rungs + 1 centre balance (13). The dimension ladder has the same shape, because every
dimension D = 10 − d has TWO dual lenses (heterotic/type II duality):
- LEFT ladder (6 points) — maximal-SUSY lens, U-duality E_{d+1}: 9D SL(2)×R⁺, 8D SL(3)×SL(2), 7D SL(5), 6D SO(5,5), 5D E₆, 4D E₇.
  (= stages 1–6; stage 0, 10D IIB, is the left anchor.)
- RIGHT ladder (6 points) — heterotic lens, Narain O(16 + d, d)/(O(16 + d)×O(d)) with the 16 internal (lattice) directions — the
  "9 through 16" of Danny's 10:54 request: 9D O(17,1), 8D O(18,2), 7D O(19,3), 6D O(20,4), 5D O(21,5), 4D O(22,6). Codon: the heterotic
  R⁴/R² threshold integrals (Kiritsis–Obers–Pioline; Bachas–Fabre–Kiritsis–Obers–Vanhove) — one-loop modular integrals over Γ_{16+d,d}.
- CENTRE (1 point) — 4D, where both ladders must hand across the SAME inflation (shared quantities: n_s, r, the k = 2 rung, the species
  stitch). Balance rule (as SERAPIS's centre): a lens result is CONFIRMED only if the dual lens at the same D agrees.
Points beyond the twin ladder (3D E₈, 2D E₉, 1D E₁₀) are kept as an extension after the centre (E₈: golden-ratio check).

## L6/13 — D = 4 (IIB on T⁶ / M on T⁷), E₇₍₇₎/SU(8) — D1573 (left ladder top)
- Coordinates: dim 133 − 63 = 70. Inflaton candidates: string-perturbation direction y₄ = g_s²ℓ_s⁶/V₆ (the 4D dilaton); T⁶ Narain block SO(6,6)/(SO(6)×SO(6)) (dim 36).
- R⁴ codon: E⁽⁴⁾ = E^{E₇}_{[1000000];3/2}; eigenvalue λ = 3(11 − D)(D − 8)/(D − 2) = −42 (computed; the earlier working figure −21/2 was wrong and never filed). Λ₄ ∝ (E⁽⁴⁾)^{−1/2}.
- String-cusp constant term (GRV arXiv:1004.0163): 2ζ(3)/y₄ + E^{SO(6,6)}_{[100000];2}. Tree/one-loop gap = 1/y₄ = g_s² — the invariant holds at the top of the left ladder.
- Weave: the one-loop thread is the SO(6,6) vector series at s = 2 — the 4D analogue of stage 5 handing E^{SO(5,5)}_{3/2} up. (s = 2 > d/2 − 1 = 2 is the boundary value: the Epstein sum sits exactly at the edge of its convergence region, so it needs the same regularisation as 6D's s = 1 — sign of the coefficient open, as at 6D.)
- Rung: along y₄ the gradient strand again gives 1 − D₄·y₄ + …, the rung-1 shape (k = 2). No new slice shape ⇒ no engine-F run.
- Hand-across to CENTRE: left lens delivers {rung k = 2, mirror gap g_s², one-loop amplitude E^{SO(6,6)}_{2}/(2ζ(3)), species stitch Λ₄ ∝ E^{−1/2}}.

## R1/13 — 9D heterotic, O(17,1)/O(17) (dim 17) — D1573 (right ladder bottom)
- Coordinates: radius R + 16 Wilson lines on S¹ (the "9 through 16" internal directions), plus the 9D dilaton.
- Codon [literature, schematic]: tree ζ(3)/g² R⁴ (t₈t₈R⁴, as in type II) + one-loop modular integral ∫_F d²τ/τ₂² Γ_{17,1}(R, Y) × (elliptic-genus factor ∝ Ē₄-polynomials/η̄²⁴) for the t₈ tr R⁴ / (tr R²)² structures (Kiritsis–Obers–Pioline hep-th/0001083; Bachas–Fabre–Kiritsis–Obers–Vanhove hep-th/9707126). The heterotic one-loop F⁴/R⁴-type terms are believed one-loop exact (KOP).
- Mirror gap: tree 1/g² vs one-loop g⁰ ⇒ gap g_s² — SAME invariant as the left ladder. The twin structure holds at the bottom rung.
- Difference from the left lens: the one-loop thread is NOT a pure Eisenstein series at generic Wilson lines (the 1/η̄²⁴ insertion makes it a theta lift of a weakly holomorphic form; at large R it grows ∝ R plus constant plus e^{−R} — an s = 1-type thread, like 8D's U-direction). So along R the right lens gives a log/linear (s = 1) shape, OFF the rung; along the dilaton it gives the rung (gap g_s²).
- Verdict: R1 agrees with L1 along the coupling direction (rung k = 2, gap g_s²) and differs along the circle (s = 1 thread) — exactly the 8D pattern. Balance at 9D: PASS along the dilaton.
- MAP: node=plateau_origin status=postulate touches=[] ripple=no

## R2/13 — 8D heterotic, O(18,2)/(O(18)×O(2)) (dim 36) — D1574
- Codon [literature]: tree ζ(3)/g² + one-loop ∫_F Γ_{18,2} × elliptic-genus factor; Foerger–Stieberger hep-th/9901020 evaluate it in closed form at 8D — log|η(T)η(U)|-type terms plus polylogarithms (Borcherds-type products) in (T, U, Wilson lines).
- Mirror gap along the 8D dilaton: g_s² (holds). Along T, U: log / s = 1 thread — OFF the rung, the SAME as L2 (8D U-direction s = 1 log plateau, D1569).
- Balance at 8D: PASS (both lenses: rung along the coupling, s = 1 log in the torus moduli).

## R3/13 — 7D heterotic, O(19,3)/(O(19)×O(3)) (dim 57) — D1575
- Codon [literature, schematic]: Obers–Pioline hep-th/9903113 — the Γ_{d,d} one-loop integral is the SO(d,d) vector Eisenstein series at s = d/2 − 1; Angelantonj–Florakis–Pioline 1110.5318 extend this to Γ_{d+16,d} × weakly holomorphic forms (Niebur–Poincaré theta lift). At d = 3 the index s = 1/2 is the edge value ⇒ regularised, with a log.
- Mirror gap along the coupling: g_s² (holds). The log/edge term mirrors L3's ±c with logs (7D anomaly, D1570).
- Balance at 7D: PASS structurally [estimate].

## R4/13 — 6D heterotic, O(20,4) (dim 80) — D1576
- Heterotic on T⁴ ↔ IIA on K3: the heterotic tree/one-loop pair maps to IIA one-loop/tree (string–string duality flips g_s → 1/g_s in 6D). One-loop thread: Γ_{20,4} theta lift, s = d/2 − 1 = 1 (edge; regularised like L4's SO(5,5) s = 1 / SO(4,4) case).
- Gap g_s² along the 6D coupling (holds); the sign of the regularised one-loop coefficient is open — the SAME open sign as L4 (D1571).
- Balance at 6D: PASS with the same open sign on both sides.

## R5/13 — 5D heterotic, O(21,5) (dim 105) — D1577
- One-loop thread: Γ_{21,5} theta lift, s = d/2 − 1 = 3/2 (regularised, sign open — D1577a). Gap g_s² holds; rung persists along the coupling. Mirrors L5.
- Balance at 5D: PASS.

## R6/13 — 4D heterotic N = 4, SL(2)_S × O(22,6) (dim 2 + 132) — D1578
- R⁴: tree ζ(3)S₂ + one-loop Γ_{22,6} theta lift at s = d/2 − 1 = 2 (edge, regularised) — same edge as L6's SO(6,6) s = 2.
- Extra 4D feature [literature]: the heterotic N = 4 R² coupling is exact in S, ∝ −log(S₂|η(S)|⁴) (Harvey–Moore) — along the 4D dilaton the R² strand is an s = 1 log thread (tree S₂ + log S₂), while the R⁴ strand keeps the tree/one-loop gap g_s².
- Gap g_s² along S for R⁴: holds.

## CENTRE/13 — 4D balance (L6 vs R6) — D1579
- Shared quantities handed across: rung k = 2 (gradient strand along the coupling), mirror gap g_s², one-loop amplitude at the edge s = 2 (regularised on BOTH sides), species stitch Λ₄ ∝ E^{−1/2}.
- Balance rule: CONFIRMED only where both lenses agree.
  - Along the 4D string coupling (y₄ on the left, S₂ on the right): BOTH give the k = 2 rung with gap g_s² ⇒ CONFIRMED [estimate-level, structural].
  - Along the torus/Narain moduli: BOTH give s = 1 log-type or edge-regularised threads ⇒ consistent, but OFF the rung (not inflaton candidates).
  - The one-loop amplitude sign at the edge s = 2: open on BOTH sides ⇒ the one item sent back (to L6/R6).
- Result: across all 13 points the ONLY direction that carries the rung in every lens, on both ladders, is the string-coupling (species) direction — the same direction P3-S already uses (y, species plateau). The dimension twin ladder therefore singles out the P3-S inflaton direction rather than adding a new one.
- Status: P3-L/P3-S stay postulates (no ladder entry without Danny's yes). Next: extension 3D E₈ (golden-ratio check via H₄ ⊂ E₈), 2D E₉, 1D E₁₀.
- MAP: node=plateau_origin status=postulate touches=[] ripple=no

## EXTENSION (after the centre)

## E1 — 3D, E₈₍₈₎/SO(16) (dim 128) — D1580
- R⁴ codon: E^{E₈}_{[10000000];3/2}; eigenvalue 3(11 − D)(D − 8)/(D − 2) = −120 (computed). String cusp (GRV 1004.0163): 2ζ(3)/y₃ + E^{SO(7,7)}_{[1000000];5/2} — s = 5/2 = d/2 − 1 at d = 7, the edge value again (as at 6D and 4D).
- Gap g_s² holds; rung along the 3D coupling persists (structural).
- GOLDEN-RATIO CHECK (Danny's question): φ = 1.618… DOES appear in E₈'s geometry — the 240 E₈ roots project onto two copies of the H₄ 600-cell whose sizes differ by exactly φ (E₈ ≅ icosians over Z[φ]). φ does NOT appear in any codon coefficient (all are rational × ζ-values: 2ζ(3), ζ(5), …) nor in any rung ratio (the gap stays g_s², k = 2). Verdict: golden ratio = a property of the E₈ lens's shape (its folding pattern), not of the inflation numbers. Honest negative for "φ sets n_s or r"; positive for "φ lives in the 3D fold".
- Silver ratio (1 + √2): not found at any point (the B/C-type √2 structures appear only as SO(d,d) normalisations, not as 1 + √2).

## E2 — 2D, E₉ (affine Ê₈, loop group) — D1581
- The Laplace eigenvalue formula 3(11 − D)(D − 8)/(D − 2) DIVERGES at D = 2: the 2D codon cannot be fixed by the same Laplace rule — 2D gravity has no propagating graviton and the symmetry becomes infinite-dimensional (affine). Fleig–Kleinschmidt (arXiv:1204.3043) construct E₉ Eisenstein series and find the ½-BPS (s = 3/2) series still has a finite set of constant terms in the string cusp, consistent with tree + one-loop.
- Gap g_s² structure survives (as far as the constant terms go); the extra feature is the central charge/loop parameter — a new "spectral" thread with no finite-D analogue.
- Weave reading: at 2D the stitch (species scale) ceases to be a point-like black hole and becomes a string-like (loop) object — the fold turns into a loop.

## E3 — 1D, E₁₀ (hyperbolic Kac–Moody) — D1582
- E₁₀ Eisenstein series (Fleig–Kleinschmidt 1204.3043) are defined formally; constant terms of the s = 3/2 series reproduce the expected perturbative structure, but convergence/completeness is conjectural. E₁₀ is the symmetry of the cosmological-billiard (BKL) picture near a spacelike singularity (Damour–Henneaux–Nicolai).
- Rung/gap: no inflaton direction exists in 1D (time only); the ladder ends here. The last point maps to the BKL "billiard" — the universe's earliest chaotic oscillation — not to inflation.
- LADDER END: 10D anchor → 6 left + 6 right + centre (4D) → 3D E₈ (φ in shape) → 2D E₉ (loop) → 1D E₁₀ (billiard). The only rung shared by every lens is the species/coupling direction (D1579).
- MAP: node=plateau_origin status=postulate touches=[] ripple=no

## OBSERVER NODES (D1590) — r at n_s ≈ 0.9706 by dimension at horizon exit (10D, 6D computed; others scaled 8/(D−2))
| D | 10 | 9 | 8 | 7 | 6 | 5 | 4 |
|---|---|---|---|---|---|---|---|
| r | 5.41e-4 | 6.18e-4 | 7.21e-4 | 8.66e-4 | 1.07e-3 | 1.44e-3 | 2.16e-3 |
| parent (all circles T-dualised) | IIB | IIA | IIB | IIA | IIB | IIA | IIB |
| prefactor push q_D | −1 | −¾ | −½ | −¼ | 0 | +¼ | +½ |
