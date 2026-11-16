# Full derivations (one section per tick, appended by the DERIVE step)
Each section gives the chain from model assumptions to the tick's result, one equation per step:
- each step labelled [derived] / [literature] / [postulate Pn] / [estimate];
- the inputs that carry over from earlier D-notes;
- a consistency check against earlier derivations (signs, units, limits);
- what changed in the theory and which map nodes it touches.
A mismatch with an earlier derivation gets a correction note (D###a), never a silent edit.

## D762 — ρ-branch leptogenesis phase (reverse side)
1. The SERAPIS-E trajectory is Re τ = ½, y from ~18 down to √3/2, ending at ρ = ½ + i√3/2 [derived] (D693, D759 set-up).
2. Generalised CP acts as τ → −τ̄. For τ = ½ + iy, −τ̄ = −½ + iy = T⁻¹τ, so the point is CP-invariant up to a modular transformation [literature] (1905.11970 eq 4.19, §4.3).
3. With gCP imposed, all couplings in the symmetric basis are real (§4.1) [literature].
4. From 1–3: every quantity built from Y(τ) and real couplings along the trajectory is CP-even, so ε_CP = 0 at ρ and during reheating [derived].
5. D731 needs sin δ ≥ s_min ∈ [0.01, 0.56] [derived] (D731, DI-bound estimate).
6. Postulate P1: no gCP; δ uniform on [0, 2π) [postulate P1].
7. P(|sin δ| ≥ s) = 1 − (2/π) arcsin s [derived] (uniform δ; K4 checks: P(0) = 1, P(1/√2) = ½, P(1) = 0).
8. P across D731 cases: 0.62–0.99, median 0.95 [derived] (computed).
9. [derived] Consistency with earlier derivations: D731's ε used the DI bound with an unspecified δ, consistent with 5. No earlier note claimed a phase source, so no correction note is needed. It is a missing assumption, now explicit (P1).
Touches: lepto_rho (→ assumed), mirror to lepto_i.

## D763 — τ = i leptogenesis and δ_CP (forward side)
1. Casas–Ibarra: Y = i U*·√m·R·√D / v_u, with R complex orthogonal [literature] (D745 set-up).
2. H = Y†Y = √D R†·diag(m)·R √D / v_u², since U is unitary [derived].
3. The radiative ε ∝ Im H₂₁·Re[Y₃₁*Y₃₂] / [H_jj(H₂₂ − H₁₁)] [literature] (hep-ph/0507092).
4. For real R, H is real, so Im H₂₁ = 0 and ε = 0 for any δ_CP or Majorana phase [derived].
5. Check: numerical (B) gives 0/1728 passes and Y_B ≤ 2e-25 [derived] (computed; agrees with 4).
6. For complex R, the pass fraction is 67.5–71.3% across δ_CP ∈ {0, …, 270°} [derived] (computed; no δ dependence, consistent with 2).
7. τ = i lies on the CP-conserving imaginary axis, so gCP forces real couplings, real R and δ_CP ∈ {0, π} [literature] (1905.11970 §4.3).
8. From 4 + 7: SERAPIS + gCP has no leptogenesis at i; with D762 the same holds at ρ [derived].
9. P1 (high-energy phases) makes both branches viable and leaves δ_CP free [postulate P1].
10. Discriminator: leptonic CP violation discovered ⇒ gCP excluded ⇒ P1-type completion required [derived].
11. [derived] Consistency: D745's PASS (68%) is reproduced exactly at δ = 230°. D762's ρ statement is mirrored. No earlier result is contradicted. P1's falsifier wording is refined, recorded in POSTULATES.md (not a silent edit).
Touches: lepto_i (→ assumed), lepto_rho.

## D764 — a CP phase from the second modulus (reverse side)
1. Under CP, τ → −τ̄; for the j-invariant, j(−τ̄) = j(τ)* [literature] (q-expansion with integer coefficients).
2. So CP-conserving τ (up to SL(2,Z)) ⇔ j(τ) ∈ ℝ, a locus that includes the imaginary axis, Re τ = ±½ and the unit arc [derived] (consistent with 1905.11970 §4.3).
3. The flux superpotential plus matter couplings fix U₁U₂ = b₃/a⁰, with U₁ = ω ≅ ρ [literature] (2405.18813).
4. U₂ = −(b₃/a⁰)/ρ [derived].
5. s_CP = |Im j(U₂)|/|j(U₂)| measures the CP violation [derived] (vanishes exactly on the locus by 2).
6. Computed: 63% of 46 small flux ratios have s_CP > 0.1, median 0.77. Integer and 1/integer ratios give 0 [derived] (computed; matches the paper's b₃ ∤ a⁰ condition).
7. Heavy-ν couplings that depend on U₂ inherit O(s_CP) phases [postulate P2].
8. With 7, D731's requirement sin δ ≥ 0.01–0.56 is met for generic non-divisible fluxes [estimate] (the map from s_CP to δ is not computed; O(1) is assumed).
9. [derived] Consistency: D762 (τ on the CP locus ⇒ no phase from τ) holds, since the phase comes from U₂, not U₁. D763's need for high-energy phases is met by 7. No contradiction.
Touches: lepto_rho, lepto_i, serapis_e (flux relation during inflation, open).

## D765 — the flux relation during inflation (forward side)
1. K = −ln Im U₁ − ln Im U₂ [literature] (factorised T⁶ complex structure).
2. Impose U₂ = c/U₁ (c real), from the F-term relation of 2405.18813 [postulate P2].
3. Im U₂ = |c|·Im U₁/|U₁|², so −ln Im U₂ = −ln Im U₁ + ln U₁ + ln Ū₁ − ln|c| [derived].
4. ln U₁ + ln Ū₁ is a Kähler transformation, so K_eff ≅ −2 ln Im U₁ [derived].
5. Canonical field: dφ = √(n/2)·dy/y with n = 2, so y = e^{φ} (was e^{√2φ}) [derived].
6. The plateau 1 − V ≈ 1/E ≈ 1/(2ζ(4)y²) gives N ≈ ζ(4)y²/(2k²) and ε ≈ 1/(8k²N²) with y = e^{kφ} [derived].
7. k: √2 → 1 gives ε ×2, r ×2, y* ×1/√2 [derived].
8. Numerical (exact MS): r 6.5–7.5e-4, n_s 0.9615–0.9659 for C ≤ 1.3e-6 [derived] (computed; agrees with 7 within the tilt effect).
9. The frozen band needs n_s 0.970–0.975 with r 4.55–5.12e-4; no C ≤ 4e-6 meets both [derived].
10. [derived] Consistency: D692 is reproduced as the n = 1 limit (same code path). D764's CP result stands; only the assignment of the relation to the inflaton modulus fails.
Touches: serapis_e (frozen; unchanged), lepto_rho (P2 restricted).

## D766 — P2 on non-inflaton moduli; the tadpole (reverse side)
1. CP-conserving ⇔ j(τ) ∈ ℝ [derived] (D764 step 2).
2. Flux relation U₂U₃ = c, with c = b₃/a⁰ real [literature] (2405.18813 Model I, applied to tori 2 and 3).
3. U₂ = i ⇒ U₃ = −ic, purely imaginary ⇒ j(U₃) real ⇒ CP-conserving for every c [derived] (checked over 46 ratios: s_CP = 0).
4. U₂ = ω ⇒ U₃ = c/ω; CP-violating for 63% of small ratios [derived] (computed; = D764).
5. n_flux = −2f·a⁰b₃ ≥ 12 for any CP-violating choice [literature] (eqs 3.25, 4.31; minimum a⁰ = 2, b₃ = −3, f = 1).
6. n_flux + 2n_D3 + n_O3′ = 32 [literature] (eq 3.8).
7. With n_O3′ = 0: n_D3 ≤ 10, so 3/3/3 + 1 saturates [derived].
8. C = 15N/(64π⁶ Im S Im ρ) is fixed by the frozen band, so Im S·Im ρ ∝ N: 375–1220 → 225–732 for N = 5 → 3 [derived] (D698 formula).
9. Heavy-ν couplings ∝ modular forms of U₃ carry O(s_CP) phases [postulate P2].
10. [derived] Consistency: D765 is respected (U₁ is not in the relation, so its metric stays single). D698's tilt mechanism is unchanged; only N changes, and the frozen predictions do not move. The exotic-O3′ caveat is open.
Touches: lepto_rho, lepto_i; mirror to the gravitino/wino chain (volume).

## D767 — downstream of 3/3/3 + 1 (forward side)
1. Tilt C = (15/64π⁶)·N_eff/(Im S Im ρ), with N_eff = N − N0 [literature] (D696 derivation from BHK hep-th/0508043).
2. Tadpole 3N + N0 + N_flux = 16, with N_flux = n_flux/2 [literature] (hep-th/0602038 eq 4.10; 2405.18813 eq 3.8).
3. n_flux = 12 ⇒ N_flux = 6 ⇒ (N, N0) = (3, 1), N_eff = 2 [derived].
4. The band C = 1.0–1.3e-6 ⇒ Im S·Im ρ = 375–488 (half-unit 188–244) [derived] (computed; K4 reproduces D696's 750–975 for (5, 1)).
5. T_R = T_R(M_H, c), independent of N [derived] (D725 inputs).
6. M₂ = b₂g₂²m₃/₂/16π², with m₃/₂ in the phenomenological window [literature] (anomaly mediation; D649-block).
7. Ω_wino and f_max are unchanged; D732 and D735 regression outputs are identical [derived] (computed).
8. [derived] Consistency: D766's 225–732 is contradicted, so D766a is written. The frozen bands are untouched (C fixed by the band).
Touches: lepto_rho (P2 context); no change to serapis_e or the wino window.

## D768 — the plateau's origin (reverse side)
1. Every in-model loop, species, Casimir, threshold and metric route to V ∝ 1 − E(ρ)/E(τ) is closed [derived] (D703, D707–D709, D712, D717–D718, D747, D757, D760).
2. Nilpotent X with W = W0 + F·X gives V = |F|²K^{XX̄}(τ) − 3|W0|² [literature] (geometric inflation; 2408.05203 §9 and its refs [16, 17]).
3. Choosing K^{XX̄} = (V_inf(τ) + 3|W0|²)/|F|² realises any V_inf ≥ 0 [derived].
4. V_inf = V0[1 − E(ρ,2)/E(τ,2)] is ≥ 0 and modular invariant, so K^{XX̄} > 0 on the whole domain [derived] (E(τ,2) ≥ E(ρ,2), its minimum at ρ, D689).
5. The τ-dependence of K^{XX̄} as 1/E(τ,2) [postulate P3].
6. The published SL(2,Z) attractors use j and Ê₁ with r = 12α/N² [literature] (2408.05203 eq 2.7).
7. SERAPIS-E: 1 − V ∝ y⁻² = e^{−2√2φ}, so ε ∝ 1/(8k²N²)·…, giving r ≈ 3.5–3.8e-4 untilted vs 1.6–1.7e-3 for the j/Ê₁ attractors at the same metric [derived] (D692 computed; D765 step 6).
8. [derived] Consistency: the frozen bands are untouched (P3 only names the origin). D760's finding (only Ê₁/log η appears in string species functions) is repeated in 2408.05203. No contradiction.
Touches: plateau_origin (open → assumed, stale flag cleared), serapis_e.

## D769 — the light axion during inflation (forward side)
1. K = −ln Im τ, so L_kin = (ẋ² + ẏ²)/(4y²) and the field metric is G = δ/(2y²) [literature] (D692 convention).
2. The Christoffels of the conformally flat metric give the x and y equations of the PREREG [derived].
3. The x-dependence of E(x + iy, 2) enters only through the Bessel terms ∝ cos(2πnx)e^{−2πny} [literature] (Fourier expansion; D692 Ese).
4. At ½ the n = 1 term has cos = −1, so E is minimal in x there and V too, making x = ½ a valley [derived].
5. At x₀ = ½ the two-field background equals single-field D692, N = 109.0902263 [derived] (computed, K4).
6. The valley's pull is ∝ e^{−2πy}, negligible until y ≈ 2, so x is frozen through horizon exit and N(x₀) differs only through the last e-fold [derived] (computed: ΔN ≤ 4.3e-3 at x₀ = 0.1).
7. δx = √2·y*·H/2π from the canonical normalisation δχ = H/2π with √G = 1/(√2 y) [derived].
8. ζ_axion = |∂N/∂x₀|δx ≤ 1.0e-7 [derived] (computed).
9. [derived] Consistency: the paper's τ = i axion statement (isocurvature ~1e-8 of ζ, D587) is of the same order, now shown for the ρ branch. The lock's end-criterion defect is recorded, not fixed, and the relaxation goes to D770.
Touches: serapis_e (axion OK during inflation), plateau_origin (P3's axion falsifier: ζ part passed).

## D770 — post-inflation axion relaxation (reverse side)
1. Equations of motion in cosmic time for the metric G = δ/(2y²), with H² = ρ/3 [derived] (D769 step 2, time variable changed).
2. Near y ≈ 1 the n ≥ 1 Bessel terms make V depend on x, with minima at the images of ρ [literature] (E(τ,2)'s minimum is at ρ, D689).
3. τ = i is a saddle of E(τ,2), so V there is a saddle as well [literature] (D608 for L; for E: D689, global minimum at ρ only).
4. Hubble friction drains energy, and the field settles into a basin of a local minimum. Since the minima are all images of ρ, every non-measure-zero start settles at a ρ image [derived] (computed: 8/8 starts, x₀ down to 0.02).
5. The read-out is at ρ_tot = 1e-4·V_end, as the lock states (lesson D769) [derived].
6. ½ + iy and ½ + i/(4y) are equivalent under ST (on the line x = ½), so y = 0.288 ≅ 0.869 [derived].
7. [derived] Consistency: D769's ζ bound and D770's basin result together clear P3's axion falsifier. No earlier result is contradicted.
Touches: serapis_e (axion fully OK), plateau_origin (P3 falsifier 3 cleared).

## D771 — P2 with exotic O3′ planes (forward side)
1. n_flux + 2n_D3 + n_O3′ = 32 [literature] (2405.18813 eq 3.8).
2. A CP-violating (non-divisible) flux needs n_flux ≥ 12, and odd quanta need n_O3′ > 0 [literature] (2405.18813 eq 4.31 and App. A).
3. Tilt C ∝ N_eff = N − N0, with n_D3 = 3N + N0 (stuck stacks; mobile D3s roll to the origin) [literature] (D696, D694).
4. Exotic planes spread evenly over the inflaton torus's fixed points add no U-asymmetry, so n_O3′ ≡ 0 (mod 4) [estimate] (assumption stated in the lock).
5. Enumeration: the only solution with N_eff ≥ 1 is n_flux = 12, n_O3′ = 8, (N, N0) = (2, 0) [derived] (computed).
6. Im S·Im ρ = (750–975)·N_eff/4 = 375–488 [derived] (D696 scaling).
7. [derived] Consistency: D766's (3, 1) with no O3′ is not allowed with odd flux (D766b correction). D766a's Im S·Im ρ is unchanged because N_eff = 2 in both. The frozen bands are untouched.
Touches: lepto_rho (P2 restricted).

## D772 — P2 retired, P4 created (reverse side)
1. G₃ = F₃ − S·H₃, W = ∫G₃∧Ω [literature] (GVW; 2405.18813 eq 3.10).
2. Model I: F₃ = 2α₀ − 3β³, H₃ = −2α₃ − 3β⁰ ⇒ W = (τ₃ − S)(2τ₁τ₂ + 3) [literature] (fetched).
3. W = 0 = ∂W gives τ₁τ₂ = −3/2 and τ₃ = S [derived].
4. Any modulus in a holomorphic relation with another field doubles its effective metric (Kähler transformation argument) [derived] (D765 step 4; for τ₃ = S: −ln Im S − ln Im τ₃ → −2 ln Im τ₃).
5. Doubled metric ⇒ r ≈ 6.5–7.5e-4, outside the band [derived] (D765 computed).
6. So Model I is incompatible with SERAPIS-E, and P2 is retired [derived].
7. F₃ = 0: W = −S∫H₃∧Ω = S·(a·U₂U₃ + b) for an H₃ with α₁- and β¹-type components only [estimate] (form chosen; the component assignment is not checked against the symplectic basis).
8. Then W = 0 ⇒ U₂U₃ = −b/a and U₁ is absent [derived].
9. n_flux = ∫F₃∧H₃ = 0; 2n_D3 + n_O3′ = 32; enumeration gives N_eff ≤ 4 [derived] (computed).
10. [derived] Consistency: D764's CP test carries over unchanged (U₂ = ω needed, D766). D771's configuration is superseded. The frozen bands are untouched.
Touches: lepto_rho, lepto_i.

## D773 — no inflaton-free CP-violating flux vacuum (forward side)
1. GVW: W = P_F(τ) − S·P_H(τ), multilinear in τ₁, τ₂, τ₃ [literature] (basis from 2405.18813, D772).
2. SUSY Minkowski: W = ∂_S W = ∂_{τ_i} W = 0 [literature] (standard GVW).
3. A τ₁-free W gives P = A + Bτ₂ + Cτ₃ + Dτ₂τ₃, with A..D affine in S and integer coefficients [derived].
4. ∂_{τ₂}P = ∂_{τ₃}P = 0 ⇒ τ₂ = −C/D, τ₃ = −B/D, so P = Q(S)/D with Q = AD − BC [derived].
5. W = 0 and ∂_S W = 0 ⇒ Q(S₀) = Q′(S₀) = 0 ⇒ S₀ = −q₁/(2q₂) ∈ ℝ [derived].
6. So no admissible (Im S > 0) vacuum, for every integer flux [derived] (grid check: 0 of 5.76e6).
7. P4's special case W = −S(2τ₂τ₃ + 3) gives S = 0 [derived] (sympy).
8. CP-violating flux vacua therefore involve all three tori, including the inflaton's, and D765 excludes these [derived].
9. The CP phase for leptogenesis must be explicit (P1) [postulate P1].
10. [derived] Consistency: D762–D763 (both branches need high-energy CP) stand. D764's j-test result is still correct as a statement about U₃, but has no admissible vacuum to apply to. D771–D772 are superseded.
Touches: lepto_rho, lepto_i.

## D774 — the twisted-moduli CP route (reverse side)
1. T⁶/(Z₂×Z₂) with discrete torsion has 48 twisted complex-structure moduli ε, one per Z₂ singularity [literature] (1702.08424).
2. ε ≠ 0 deforms the singularity and opens an exceptional cycle [literature] (1702.08424).
3. SERAPIS-E's tilt uses BHK's one-loop K at the orbifold point with stuck D3s at fixed points [literature] (D689, D696).
4. ε = 0 is CP-even (real periods at the orbifold point, by the symmetry of the singular point) [estimate].
5. A CP phase needs arg ε ≠ 0, |ε| ≠ 0, which deforms the stuck-brane loci, so the tilt formula holds only for |ε| ≪ 1 [estimate].
6. Leptogenesis needs sin δ ≳ 0.01–0.56 (D731); with phases O(|ε|), |ε| ≳ 0.01 is needed [estimate].
7. [derived] Consistency: D773 (untwisted) stands. This adds a tension, not an exclusion. P1 is unchanged.
Touches: lepto_i, lepto_rho.
