# Level S plan: string one-loop masses for Project H (started 16 Nov 2026)
Goal: decide, by computation, whether a gauge-charged scalar χ on the anti-D5 branes of the ADS T⁴/Z₂ orientifold (hep-th/9908023) gets a POSITIVE one-loop mass² ∝ E(U,2)/A on a T² factor (Project H's open condition, D964–D968, D983).
Rule: each stage must reproduce an independent route before it is used; results go through locks as usual.
- S0 DONE: theta/eta; abstruse identity θ₃⁴ − θ₄⁴ − θ₂⁴ = 0 (selftest).
- S1 DONE: field-theory one-loop potential on R⁴ × T² for a bulk boson with a Wilson line/position shift: KK proper-time sum = Poisson winding sum (1e-8 on four tori), curvature = E_paper(U,2)/(π³A) (1e-4). Sign rule: fermions enter with weight −1, so m² ∝ +(N_B − N_F)E(U,2)/A (D983).
- S2 DONE (16 Nov 20:20 CT): open-string annulus for a D-brane stack on T² with a Wilson line: A(a) = ∫dt/t³ · [oscillator theta/eta ratio] · Σ_p e^{−πt α′|p+a|²}. Tests: (i) supersymmetric ratio vanishes identically (S0); (ii) massless-level truncation reproduces S1 exactly; (iii) Kitazawa 0805.0824 9-brane-on-circle result (sign opposite to the vacuum amplitude).
- S3 DONE (D985, PASS): Möbius strip + the BSB (anti-D5) projection: oscillator content of the anti-D5 sector (bosonic excess +128, D968); compute d²A/dχ² for a gauge-charged position/charged scalar; extract sign and U-dependence; compare with S1's E(U,2) form and with the field-theory sign rule. Lock before running.
- S4: write-up; if positive with E(U,2), Project H's sign condition moves from derived (field theory) to computed (string).
Parallel: outreach email to string theorists (draft only, papers/outreach/STRING_EXPERT_DRAFT.md) — sent only on Danny's "Send".

## S3 input data (ADS hep-th/9908023, extracted 16 Nov 20:05 CT) [literature]
- Direct annulus eq. (9): A = ¼{(Q_o+Q_v)(N²P + D²W) + 2ND(Q_s′+Q_c′)(η/θ₄)² + (R_N²+R_D²)(Q_o−Q_v)(2η/θ₂)² + 2R_N R_D(−O₄S₄ − C₄O₄ + V₄C₄ + S₄V₄)(η/θ₃)²}; Q_o = V₄O₄ − C₄C₄, Q_v = O₄V₄ − S₄S₄ (each a boson−fermion supersymmetric pair): the annulus is supersymmetric.
- Direct Möbius eq. (12): M = −¼{NP(Ô₄V̂₄ + V̂₄Ô₄ − Ŝ₄Ŝ₄ − Ĉ₄Ĉ₄) − DW(Ô₄V̂₄ + V̂₄Ô₄ + Ŝ₄Ŝ₄ + Ĉ₄Ĉ₄) − …}: in the D̄5 term bosons and fermions enter with the SAME sign (the O5 charge reversed), so supersymmetry is broken by the Möbius amplitude in the D̄5 sector only.
- Tadpoles: N = D = 32, R_N = R_D = 0; D̄5 gauge group USp(16)×USp(16). Massless D̄5 spectrum: USp vectors (adjoint = symmetric 136), scalars in (16,16) quartets, fermions in antisymmetric 120's and (16,16): NO gauginos. Per USp(16): boson adjoint 136 vs fermion antisymmetric 120 → mismatch 16 per factor.
- D̄5 vacuum energy positive, V = c e^{−φ₁₀} = c/g²_YM, c > 0 (eq. 18).
S3 task (next, lock first): add a Wilson line / position shift a for a χ charged under USp(16) on the D̄5 stack wrapping the T² (P → P(a) for charged states; the Möbius only sees states mapped to themselves, i.e. shift 2a); compute d²(A + M)/da² at a = 0 from the full theta-function amplitudes (S2 machinery, Ô/V̂/Ŝ/Ĉ in the "hatted" Möbius basis), sign and U-dependence; field-theory cross-check: massless level = (adjoint 136 − antisym 120) mismatch × S1's E(U,2)/A form.
S2 result: superstring degeneracies 8/128/1152/7680/42112 exact (NS = R); Wilson-line potential with the full tower by two routes (level sum with Bessel K₃ vs theta-trace proper-time integral) agrees to 1e-5–1.5e-4 (L = 10–16); massive-state share 7.7% (L=10), 1.05% (L=12), 0.036% (L=16) → S1 recovered at large torus. Two bugs found by the two-route rule: proper-time peak missed by the integrator for large windings; NS trace underflow at large t (fixed with expm1). Convergence needs |w| above the Hagedorn length 2π√2 √α′.
- S3b positivity shortcut FAILED (D987: Ĥ oscillates for t ≲ 0.027); S3b proper (next, larger): relax D985's heavy-T⁴-winding assumption. For χ moving along a T⁴ circle of radius R, the Möbius strings stretch over 2y + 2πRn; the n ≠ 0 images enter m² with (2t − 4t²R²n²)e^{−tR²n²}, which can carry either sign, and the (w_T², n) = (0, n) terms need the closed-string (transverse) channel to be finite (tadpole region). Needs the transverse Möbius amplitude (ADS eq. 11) and a Poisson resummation in n; lock before running; target: sign of m² for R down to ~√α′.
- Local-mass sign (D988) literature check [literature, 2107.02814 Basile review §6.3]: probe Dp-branes in the backreacted Dudas–Mourad geometry (9D, 8-branes) are repelled for p < 3, attracted for p > 4, unstable equilibria for p = 3, 4; at large separation repulsive for p < 5 and attractive for p > 5, with p = 5 "needing subleading terms" (undetermined); branes "cannot be described as isolated objects" because of the dilaton potential. No computation for D̄5 position scalars in the 6D T⁴/Z₂ BSB model found; the D988 sign stays open. A real computation would need the 6D backreacted solution plus probe/annulus analysis: research-level, not a toolkit stage.
- S4a DONE (D996). S4 (path for the D988 local-mass sign): build the backreacted background ourselves. S4a: reproduce the Dudas–Mourad 9D tadpole solution (dilaton + warp + metric ODEs with the exponential tadpole potential) two ways (shooting vs relaxation); S4b: the 6D anti-D5 (T⁴/Z₂ BSB) analogue; S4c: probe-brane / annulus in that background → sign of χ's U-independent mass. Each stage locked, each reproducing the previous limit.

## S4b research note (17 Nov, 05:12Z) — 6D tadpole action
[literature] hep-th/0503204 (Eq. 6, Eq. 13): string-frame action ∝ e^{−2φ}[R + 4(∂φ)² − H²/12]; the BSB tadpole is
disk-level, V_φ ~ T ∫ √G e^{−φ} (brane tension ∝ 1/g_s); T⁴/Z₂ with brane SUSY breaking is in its Secs. 2.3, 4.2.3.
[derived] (frame algebra, to be checked symbolically under the S4b lock): in D dimensions, g_s = e^{4φ/(D−2)} g_E turns
√g_s e^{−φ} into √g_E e^{(D+2)φ/(D−2)}; with the kinetic term (4/(D−2))(∂φ)², the canonical field is φ_c = φ√(8/(D−2)),
so the Einstein-frame exponent is γ_D = (D+2)/√(8(D−2)). Check: D = 10 → γ = 3/2 (Dudas–Mourad, D996 ✓). D = 6 (anti-D5
filling 6D, T⁴ volume frozen, φ_6 = φ − ¼ ln Vol₄ reduces the brane term to e^{−φ_6}) → γ_6 = 8/√32 = √2.
S4b DONE (D1014 exponent, D1015 6D vacuum: subcritical, finite interval, two routes). Next S4c: χ probe on the 6D background.
S4a solver (two routes); (c) note that the frozen-volume assumption must later be lifted (the T⁴ breathing mode also
feels the tadpole).

## Track R research note (17 Nov 06:35Z) — type IIB one-loop Kähler terms (lead, not a result)
[literature] Berg–Haack–Körs hep-th/0508043 (fetched, partial): one-loop K ⊃ −c Σ_i E₂(A_i, U)/[(S−S̄)(S′−S̄′)] inside the log
(Eq. 2.77, T⁴/Z₂×T²), c = 1/(128π⁶) (Sec. 2.6, App. D); Z₂×Z₂ form in Sec. 3.4 / Eq. 3.30 (not yet read). These carry a
naturally SMALL coefficient (unlike heterotic GS, D1021/D1024). They are weight-2-type (E₂) in U, the same family as
Project H's BHK term (D975), not the log L.
Idea to test (lock first): the Kronecker limit of the non-holomorphic Eisenstein series E(U, s) at s → 1 contains
−ln(Im U |η(U)|⁴) = L (+ pole + constant) — fetch the exact Kronecker first limit formula before using it. If a one-loop
amplitude is evaluated at (or regularised near) s = 1 rather than s = 2, its finite part is L with the small 1/(128π⁶)-type
coefficient: a candidate natural origin for ε L. Read Eq. 3.30 and check which s the amplitudes carry.
- S4c3 DONE (D1036): KK masses converged, m1² = 0.778184 α_E, m2/m1 1.780, m3/m1 2.546. Next: derive q≈0.84 from endpoint exponents; dilaton/metric fluctuations.
- D1038: convergence order q=(D−2)/((D−1)(1+δ)) derived; y=0 is log-type (p~u): state the regular-branch BC as an input.
- R: BHK IIB one-loop lead CLOSED (D1040, s=2). Next R step: DKL threshold corrections (s=1 log) in the gauge kinetic function (fetch source, lock first).
- R source pinned (fetched, hep-th/9506178 Eq. 1, 15): (4π)²/g_a² = (4π)²k_a/g_X² + 2b_a ln(μ/M_X) + Δ̃_a, Δ_a^(m) = Σ_i b̃'_a^i ln[(T_i+T̄_i)|η(T_i)|⁴],
  b̃'_a^i = b'_a^i − k_a δ_GS^i; one-loop dilaton S+S̄ → S+S̄ + Σ_i 2δ_GS^i/(4π)² ln(T_i+T̄_i). Next R step (lock first): hidden-vs-visible
  asymmetry of b̃' (non-universal part b'_a) in a Z_N orbifold with N=2 sectors (Z3 has none → no asymmetry) → does it change R?
- R (D1043): cancellation route found (K-term vs condensate W-term, coefficient δ_GS/16π² + b_a). Next: fetch explicit f(T) (FILQ/Cvetič), sympy total L-coefficient (lock first).
- R (D1044): D1043 withdrawn (redefinition, not cancellation). Next R: in the S' frame the GS tilt variable is ln(2 Im T), not L — re-test D1010's ρ match with ln Im T (lock first).
- R (D1045): GS route NOT reproduced in the consistent frame (S' fixed → tilt variable ln 2ImT). Options: finer κ scan (lock), or a non-condensate dilaton stabilisation fixing S.
- R (D1048): GS route CLOSED (LRW S' frame + BGW linear multiplet). Tilt origin back to open; remaining idea: non-GS s→1 Eisenstein source (D1031).
- R (D1049): NEW LEAD — matter wave function log (AGNT hep-th/9301033 Eq. 20, N=2 coefficient). Plan: matter F-term plateau? size γ̃ ↔ 6e-5? S'-shift independence?
- R (D1051): matter-log lead size: κ = 2g²γ̃, natural 30–300× too big; needs near-finite N=2 sector. Next: find an orbifold with small γ̃ (literature: N=2 finite sectors).
- R search (17 Nov): arXiv 1410.6147 checked — its N=2 sectors have b^{N=2} = −2C(E8) etc. (Eq. 5.21, 5.28), not small; it uses N=4 restoration instead. No near-finite N=2 example found yet; next candidates: hep-th/0001062, 1001.1480 (b'_a tables).
- R (D1135): exact-zero example found (Z6-II-b U(1), hep-th/0001062). Next: Wilson-line lift of the zero (same paper treats Wilson lines).
- R (D1137): Wilson-line lift: none at O(BC). Lead paused; R effort → S4d.
- S4d prep (D1138): BMS 1811.11448 template; next: fetch §5.3 tensor equations, cross-check S4c2 at D=10, then lock S4d scalars.
- S4d source map (ar5iv 1811.11448, 1.12M chars): offset 500k–600k = §4.3 scalars + §5 DM backgrounds (5.1–5.5); 600k–700k = §5.2 DM scalar sector (Eqs. 5.20–5.33: C = −7A, φ = −(8/φ′)(A′ + 7AΩ′), D Stückelberg, single physical scalar, eigen-eq. 5.33); tensor §5.3 is past 700k. S4d lock should transcribe Eqs. 5.20–5.33 at D=10, then generalise to D=6.
- S4d source (fetched verbatim LaTeX, ar5iv 1811.11448 Eq. 5.33, D=10, conformal frame ds² = e^{2Ω(z)}[η+h]):
  A'' + A'(24Ω' − (2/φ')e^{2Ω}V_φ) + A(m² − (7/4)e^{2Ω}V − 14 e^{2Ω}Ω' V_φ/φ') = 0, with C = −7A (5.31), φ = −(8/φ')(A' + 7AΩ') (5.32), D Stückelberg.
  Prime presumably d/dz (inference). BCs not in the fetched chunk. Next S4d step (lock first): sympy re-derivation of the scalar system for general D from the
  linearised Einstein–dilaton equations; PASS if at D=10 it reproduces 5.31–5.33 exactly (24 = ?(D), 7/4, 14 → identify D-dependence); then apply at D=6
  with our background (S4b/S4c2) and BCs from regularity, matching how S4c2 handled the tensor tower.
