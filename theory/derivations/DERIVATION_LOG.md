<!-- AEGIS-FP 3BKSOVH3WUVK3MAY · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
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

## D775 — ρ-leptogenesis CP asymmetry (forward side)
1. Casas–Ibarra: Y = i·U*·√m·R·√D/v, R complex orthogonal [literature] (Casas–Ibarra; D745 set-up).
2. H = Y†Y; the degenerate pair is rotated so Re H₁₂ = 0, making Im[(H₁₂)²] = 0 [derived] (D745 alignment).
3. ε_i = −(1/8π)Σ_j Im[(H_ij)²]/H_ii·[f(x) + g(x)], f = √x[1 − (1 + x)ln((1 + x)/x)], g = √x/(1 − x) [literature] (Covi–Roulet–Vissani 1996).
4. Spectrum at ρ: pair (0.212, 0.707, 1.0)·M_H and single (1, 1, 0.471)·M_H for c = (0.3, 1, 3) [derived] (D725, computed).
5. Y_B = (8/23)(3/4)(T_R/m_φ)·2·|ε̄| [estimate] (non-thermal yield, D731 conventions; no washout, M/T_R ≥ 500).
6. Pass fractions at M_H = 1e12: c = 0.3 → 0%, c = 1 → 29–56%, c = 3 → 68–70% [derived] (computed).
7. K4: hierarchical |ε|max/ε_DI = 0.47, consistent with DI as an upper bound [derived].
8. [derived] Consistency: D731 overestimated (it used ε_DI·sin δ). Its c = 0.3, M_H = 1e12 "PASS" is corrected to FAIL. D733's M_H preference is unchanged. The frozen bands are untouched.
Touches: lepto_rho (corrected), gravitino_wino.

## D776 — the mixing threshold c* (reverse side)
1. Weights k_N = k_N3 = −1, so the NN and NN₃ terms both need weight-2 forms, i.e. Y [derived] (D724).
2. The canonical factor (2 Im τ)^{(k_i + k_j)/2} is equal for both entries, so it cancels in c [derived].
3. Γ₂ ≅ S₃ allows both invariants independently, so c = β/α is a ratio of free constants [derived].
4. Spectrum: M_pair/M_single = 0.7072c (c < √2) [derived] (D725 singular values).
5. CP asymmetry and yield as D775 [literature] (CRV) / [estimate] (non-thermal yield).
6. c* = 0.6 for ≥ 10% of the grid passing [derived] (computed).
7. Log-uniform prior on [0.1, 10] ⇒ P(c ≥ c*) = log(10/c*)/log 100 = 0.61 [derived].
8. [derived] Consistency: D775 is reproduced at c = 0.3 and 1. The frozen bands are untouched (T_R(c) stays inside D725's range).
Touches: lepto_rho.

## D777 — the ρ seesaw degeneracy (forward side)
1. At ρ the weight-2 doublet is Y ∝ (1, i), and A(Y) is nilpotent [derived] (D720, D739).
2. M_R = [[A, cY], [cYᵀ, 0]] has singular values (c, c, √2) [derived] (computed; matches D725).
3. With weight-2-only Dirac couplings, M_D = [[A, βY], [γYᵀ, 0]] [estimate] (the weight assignment is assumed to allow all three terms).
4. m_ν = −M_D M_R⁻¹ M_Dᵀ has an exactly degenerate pair for all β, γ, c [derived] (computed: 243/243 and the full grid).
5. The eigenvalues of m_ν are basis-independent, so the charged-lepton sector cannot lift the pair [derived].
6. So the minimal ρ lepton sector gives Δm²₂₁ = 0 or Δm²₃₂ = 0, i.e. FAIL [derived].
7. [derived] Consistency: this extends D741 (Weinberg texture at ρ, no NO). The frozen Σm_ν is unchanged (locked), but now lacks a derived spectrum at ρ. Leptogenesis (D775) assumed only a Casas–Ibarra-compatible texture exists, which is now conditional.
Touches: n_sector_rho (computed → corrected), mnu, lepto_rho.

## D778 — the Z₃ obstruction at ρ (reverse side)
1. ρ is fixed by ST (order 3), so at τ = ρ the residual symmetry is Z₃ [literature] (standard; 1905.11970 and the modular-flavour literature).
2. A field of weight k in rep r transforms under the residual Z₃ by (cρ + d)^{−k}·ρ_r(ST) [literature] (modular-form transformation).
3. In the Γ₂ ≅ S₃ doublet, ρ_2(ST) has eigenvalues ω and ω², so the two components have charges differing by 1 [derived].
4. Majorana mass entries need q_i + q_j ≡ 0 mod 3 [derived] (Z₃ invariance of the mass term).
5. A light-lepton doublet therefore gives a degenerate (q, −q) pair or a massless state, and the doublet-based ρ lepton sector is excluded [derived] (consistent with D741, D777 and D778's 0/25 assignments).
6. Singlets 1 and 1′ of S₃ have ST-charge 0 (ST is a 3-cycle, trivial on both 1-dim reps); with suitable weights, q = 0 for all three [derived].
7. [derived] Consistency: D777's degeneracy is now explained. The heavy-ν doublet results (D724–D776) are unaffected, since only light-mass degeneracy is excluded. The frozen Σm_ν is untouched (locked).
Touches: n_sector_rho (corrected), mnu.

## D779 — Z₃ bookkeeping of the ρ seesaw (forward side)
1. In the basis (n, Y, N₃), M_R = [[0, 0, c], [0, √2·i, 0], [c, 0, 0]], up to the normalisation of A [derived] (computed; K4 SVs (c, c, √2)).
2. So N_n–N₃ is a Dirac pair (charges q, −q) and N_Y has charge 0 [derived] (Z₃ invariance of each non-zero entry).
3. A Weinberg mass for leptons needs a common lepton charge q_L = −q_H [derived] (D778).
4. Dirac couplings need q_N = −q_L − q_H = 0, i.e. N_Y only [derived].
5. So rank(m_ν) = 1 [derived] (computed: 1000/1000).
6. Each extra q = 0 heavy singlet raises the rank by 1, so two are needed [derived] (computed).
7. The N_n–N₃ pair has no tree-level coupling to q = 0 leptons, so its decays cannot make a lepton asymmetry [derived].
8. [derived] Consistency: D775's Casas–Ibarra assumption (all N couple to all L) is violated at ρ, so D775 must be re-examined (correction pending). The reheating result D725 (inflaton → N pairs) is unaffected.
Touches: n_sector_rho, lepto_rho, mnu.

## D780 — Z₃ charge conservation in ρ reheating (reverse side)
1. Under ST, δτ → (cρ + d)^{−2}δτ, a non-trivial cube root of unity at ρ, so q_φ ≠ 0 [derived].
2. Decay amplitudes are Z₃-invariant, so φ's products have total charge q_φ [derived].
3. Heavy-ν charges: N_Y 0, N_n q, N₃ −q (D779) [derived].
4. So every φ → NN channel contains a charged N [derived].
5. L·N·H needs q_N = 0 when q_L = −q_H (D778) [derived].
6. Charged N have no renormalisable decay to SM [derived].
7. Higher-dimension decay Γ ~ M⁵/Λ⁴ ⇒ T₂ ~ √(ΓM_P) ≈ 300 GeV (Λ = M_P, M = 1e12) [estimate].
8. A stable relic, if no charged operator exists: Ωh² ~ 2.7e8·M·Y ~ 1e14·0.12 [estimate].
9. [derived] Consistency: this contradicts D725's statement that light states decay via the seesaw y_D (it ignored Z₃), so D725 and everything downstream is corrected. The frozen bands are locked and unchanged. τ = i is unaffected (Z₂ allows Majorana odd leptons).
Touches: n_sector_rho, lepto_rho, gravitino_wino, serapis_e.

## D781 — late reheating and the frozen bands (forward side)
1. N* = 67 − ln(k/a₀H₀) + ¼ ln(V*²/(M_P⁴ρ_end)) + (1/12)ln(ρ_th/ρ_end) − (1/12)ln g* for a w = 0 phase down to T₂ [literature] (Liddle–Leach; Planck 2018 X; D719 code).
2. Both the inflaton and the heavy-N phases are matter-like, so only T₂ enters [derived].
3. dN*/d log₁₀T₂ = (1/12)·4·ln 10 ≈ 0.77 [derived] (computed: 49.7 → 48.2 → 46.6 → 45.1 per two decades ✓).
4. Exact spectra (first-order slow roll on the D692 potential) give n_s and r per (C, T₂) [derived] (computed).
5. The frozen bands hold for T₂ ≥ 3e6 and fail for T₂ ≤ 3e4 [derived] (computed).
6. The required T₂ ≳ 1e5 GeV implies Λ ≲ (M⁵M_P/T₂⁴)^{1/4}·…, i.e. roughly the string scale for M ~ 1e12 [estimate] (from Γ ~ M⁵/Λ⁴ and T₂ ~ √(ΓM_P)).
7. [derived] Consistency: K4 reproduces D725. D780's estimate T₂ ~ 300 GeV (Λ = M_P) is now quantified as OUTSIDE. The frozen bands are unchanged (locked); a condition is added.
Touches: serapis_e, n_sector_rho.

## D782 — the decay scale of the Z₃-charged pair (reverse side)
1. At τ = ω the residual Z₃ is exact, and states whose couplings vanish there are stable [literature] (2111.05674).
2. The N_n/N₃ pair is Z₃-charged with no renormalisable SM decay [derived] (D779, D780).
3. A decay needs an SM operator with the opposite Z₃ charge; dim-6 candidates exist for suitable SM weights [estimate] (weights are free up to the Yukawa, μ and anomaly constraints; not enumerated).
4. Γ ≈ M⁵/(192π³Λ⁴) for 3-body decay [estimate] (dimensional analysis).
5. T₂ ≈ √(ΓM_P)(90/π²g*)^{1/4} ≳ 1e5 GeV ⇒ Λ ≲ 3e16 GeV (M = 1e12) [estimate].
6. Earlier asymmetries are diluted by the pair's domination, so baryogenesis must come from the late decays: Y_B ≈ (3/4)(T₂/M)ε [derived] (standard late-decay yield).
7. [derived] Consistency: D781's condition T₂ ≳ 1e5 is translated into Λ. D775/D776 are superseded for ρ (dilution). The frozen bands are untouched (conditional on R-Z₃).
Touches: lepto_rho, n_sector_rho, serapis_e.

## D783 — the Λ window (forward side)
1. Γ = M⁵/(192π³Λ⁴) for a dim-6 three-body decay [estimate] (dimensional analysis, standard phase space).
2. T₂ = (90/π²g*)^{1/4}√(ΓM_P) (sudden decay) [literature] (standard).
3. T₂ ≥ 1e5 ⇔ Λ ≤ (pref²·M_P·M⁵/(192π³·1e10))^{1/4} = 3.6e15–1.05e16 [derived] (computed).
4. M_s ≈ g_s^{1/4}M_P/√(4πV) [estimate] (IIB convention, isotropic V = (Im ρ)^{3/2}; not computed for the actual orientifold).
5. M_s = 5.6e15–2.6e16 for the D696/D766a moduli range [derived] (from 4).
6. Y_B = κ(3/4)(T₂/M)ε ⇒ ε_req = 2e-5 – 3e-3 [derived] (computed; κ = 28/79 or 1).
7. ε ≤ 1/(8π) for one-loop interference, so this is plausible [estimate].
8. [derived] Consistency: D781's T₂ boundary is translated; D782's estimate "Λ ≲ 3e16" is refined DOWN to ≲ 1e16 (it neglected the 192π³ phase space). The frozen bands are unchanged (conditional).
Touches: serapis_e, lepto_rho.

## D784 — the wino after late reheating (reverse side)
1. φ → NN with no SM channel, so there is no thermal bath before T₂ [derived] (D780).
2. Thermal gravitino yield Y₃/₂ = 1.9e-12·T₂/1e10 [literature] (D732 formula; Bolz–Brandenburg–Buchmüller-type).
3. Ω_nth = 2.74e8·M₂·Y₃/₂ ≤ 4e-4 [derived] (computed).
4. T₂ ≫ M₂/20, so the thermal freeze-out relic is f = (M₂/2.9 TeV)² [literature] (thermal wino mass 2.9 TeV, D732 convention).
5. f_max = √(L/σ_line) with Einasto L ∝ M² [estimate] (D735 method), giving M₂ ≤ 1.96–2.0 TeV [derived] (computed).
6. 2507.15934 excludes thermal sub-fractions from 1.85 TeV [literature] (D761), so the window is 0.67–1.85 TeV [derived].
7. [derived] Consistency: K4 reproduces D732. D735/D736's narrow window depended on T_R = 3e8 (now superseded by D780). The τ = i branch's wino window (0.66–2.9 TeV, paper Sec. VII) is unaffected.
Touches: wino_window (corrected), gravitino_wino.

## D785 — the τ = i mirror check (forward side)
1. S₃ weight-2 doublet q-series [literature] (1803.10391 S₃ basis; from memory, validated by K4 at ρ).
2. At i, Y ∝ (√3/2, ½), real [derived] (computed).
3. M_R at i has three distinct singular values for c ∈ {0.6, 1, 3} [derived] (computed).
4. A real Y at a Z₂ fixed point keeps the symmetric matrices diagonalisable into Majorana states, so there is no protected Dirac pairing [derived] (S has real eigenvalues ±1; q_i + q_j ≡ 0 mod 2 allows self-pairing).
5. Every heavy eigenstate has a non-zero lepton coupling, so no stable relic [derived] (computed).
6. The light spectrum is generically non-degenerate, with NO and IO points [derived] (computed).
7. [derived] Consistency: D780 (reasoning) is confirmed. D727's ±s doublet pair is lifted by the c-mixing (D738). D741/D742 are consistent.
Touches: n_sector_i, lepto_i.

## D786 — the meaning of the frozen Σm_ν (reverse side)
1. NO: Σ = m₁ + √(m₁² + Δm²₂₁) + √(m₁² + Δm²₃₁) [literature] (standard).
2. Σ(0) = 0.0586 eV, and Σ = 0.0587 at m₁ = 1e-4 [derived] (computed).
3. At τ = i, m₁ ≈ 0 came only from AD (D646); D745 removes that need [derived].
4. The D742 texture gives m₁/m₃ = 0.001–0.08, so Σ = 0.059–0.064 [derived] (D742 computed).
5. At ρ, singlet leptons give a generic m_ν, so there is no m₁ prediction [derived] (D778–D779).
6. The DESI DR2 + Lyα bound 0.0592 ⇒ m₁ ≲ 5.6e-4 eV [derived] (computed; bound from the paper's ref arXiv:2607.27410).
7. [derived] Consistency: the frozen lock is unchanged, and its condition Σ > 0.07 still disfavours. The interpretation is updated, not the number.
Touches: mnu (frozen; flag cleared), plus flag clears for plateau_origin, lepto_i, gravitino_wino, n_sector_rho, lepto_rho.

## D787 — Z₃ = baryon triality at ρ (forward side)
1. The charges must allow QH_uU, QH_dD, LH_dE, H_uH_d, LLH_uH_u and LH_uN_Y [derived] (D778, D779 and the paper's chain).
2. Solving mod 3: H_d = L = −H_u, E = 2H_u, U = −Q − H_u, D = −Q + H_u [derived].
3. Charge(UDD) = −3Q + H_u ≡ H_u; charge(QQQL) = 3Q − H_u ≡ −H_u [derived] (computed for all 9).
4. So for H_u ≠ 0 the B-violating operators carry charge ∝ B mod 3, i.e. baryon triality [derived].
5. The pair (charges ±q) can decay via N·UDD (W) and N†·UDD (K), both dim-6 [derived] (computed).
6. Matter parity forbids N·QQQL (odd) and allows N·UDD (even) [derived] (D661 matter parity).
7. B₃ is anomaly-free with MSSM content [estimate] (Ibáñez–Ross, from memory).
8. [derived] Consistency: D782's R-Z₃ is satisfied. D783's κ = 1 case applies. The proton is stable. The frozen bands remain conditional on Λ (D781–D783).
Touches: n_sector_rho (corrected → computed), lepto_rho.

## D788 — the late-decay CP asymmetry (reverse side)
1. N_pair is stable without B-violating operators, so ε = O((B-violating coupling)²) [literature] (Nanopoulos–Weinberg via 1310.0840).
2. With dim-6 c/Λ²: ε ≲ (1/8π)(M/Λ)² [estimate].
3. Over the D783 window: ε ≤ 1.7e-8 < ε_req,min = 1.7e-5 [derived] (computed), so it is a WALL.
4. Heavy mediator M_X > M: ε ~ (y²/8π)(M/M_X)², still small [estimate].
5. Light mediator M_X < M: N → uX* on shell, ε ~ y²/8π, y ≳ 0.02–0.17 [estimate].
6. A renormalisable N decay means the pair does not dominate: T_R back to D725's 3e8–3e9 [derived] (D725 rates apply if the N → uX* rate exceeds H at production, Γ ~ y²M/16π ≫ H(T_R)).
7. Postulate P5 (X with M_X < M) [postulate P5].
8. [derived] Consistency: D782/D783's late-decay route is closed (ε). D781's frozen-band condition becomes moot under P5. D787 baryon triality is kept.
Touches: lepto_rho (assumed), n_sector_rho, serapis_e.

## D789 — P5 consistency and the B bookkeeping (forward side)
1. X ~ (3, 2/3), X̄ ~ (3̄, −2/3); NUX and X̄DD are gauge-invariant [derived] (computed hypercharge and colour).
2. Z₃: q_X = −q − q_U, q_X̄ = −2q_D; M_X XX̄ is allowed for exactly one pair charge per assignment [derived] (computed).
3. Gauge-allowed X-terms with SM fields: XU, X̄QH_u, X̄DD; Z₃ allows only X̄DD [derived] (computed).
4. Matter parity: X, X̄ even [derived].
5. Γ(N → uX) ≫ H(T_R), so the decay is prompt [derived] (computed).
6. B charges: X̄ +2/3, X −2/3, N +1 make all P5 terms and the Dirac mass B-conserving [derived].
7. So the N decays conserve B, and B violation sits in the inflaton couplings (φNN with ΔB = ±2, ±1) [derived].
8. [derived] Consistency: D788's statement "baryogenesis in N decays" is corrected (B conserved there). P5 is still useful (it removes the late phase). Baryogenesis moves to φ decays.
Touches: lepto_rho.

## D790 — inflaton Affleck–Dine at ρ (reverse side)
1. ε_φ ≤ g²/8π for interference at order g² [estimate] (Nanopoulos–Weinberg counting; D725 couplings).
2. ε_φ ≤ 3e-13 ≪ 4e-6, a WALL [derived] (computed).
3. Near ρ, Z₃ forbids δτ² terms, so the quadratic potential is isotropic, with an approximate U(1) on the disk coordinate w [derived] (the charge of δτ² is 2q_φ ≢ 0).
4. Cubic δτ³ terms (Z₃-allowed) break the U(1), so an off-axis start gives an orbit charge n = Im(w*ẇ) [derived] (AD mechanism structure).
5. η = n/(ρ/m): 0 at x₀ = ½; |η| ≈ 0.1–0.2 at |Δx| = 0.05–0.1 [derived] (computed; read-outs at ρ only).
6. Inflaton quanta carry B-triality, so decays transfer η into B: Y_B = (3/4)(T_R/m_φ)·⟨ΔB⟩·η [estimate].
7. Requirement η ≈ 4.3e-6 ⇒ |Δx| ≈ 2e-6; isocurvature safety needs |Δx| ≥ 7e-5, hence ~35× over-production [derived] (computed arithmetic).
8. [derived] Consistency: the CP violation here is spontaneous (the initial x₀), so P1 is not needed at ρ in this route. The D788/D789 picture (P5 for prompt N decay) is kept. The 0.499/0.49 read-outs are flagged unreliable.
Touches: lepto_rho.

## D791 — the Planck bound on the inflaton-AD offset (forward side)
1. Uncorrelated axion-type CDI: β_iso < 0.038 (95%, k = 0.05) [literature] (Planck 2018 X, Table 14).
2. A baryon isocurvature mode is equivalent to CDI with S_c = (Ω_b/Ω_c)S_b [literature] (standard; Ω_b/Ω_c ≈ 0.186 as an estimate).
3. S_b = δη/η = δx/|Δx| for η ∝ Δx [derived] (D790 linear read-outs).
4. β < 0.038 ⇒ |Δx| ≥ 0.15 [derived] (computed).
5. Y_B(Δx = 0.15) = 2.3e-6 ⇒ dilution ~2.7e4 needed [derived] (computed).
6. [derived] Consistency: D790's verdict is corrected (loose allowance). D769's δx is reused. The τ = i branch is unaffected.
Touches: lepto_rho.

## D792 — the self-diluted ρ history (reverse side)
1. Inflaton quanta carry B-triality; φ → N_nN_n gives ΔB = 2 [derived] (D780, D787).
2. Orbit charge η = (n_φ − n_φ*)/n_φ = 2|Δx|, with |Δx| ≥ 0.15 [derived] (D790, D791).
3. B per N = η; the N dominate until T₂ [derived].
4. Y_B = (28/79)(3/4)(T₂/M)·η [derived] (entropy from N decay, s = (4/3)ρ/T₂; sphaleron conversion of B with L = 0).
5. Y_B = 8.75e-11 ⇒ T₂ = 142–1097 GeV [derived] (computed).
6. Λ = (M⁵/(192π³Γ))^{1/4}, Γ from T₂, gives 5e16–2e17 GeV [derived] (computed).
7. N*(T₂) from D781 (0.77 per decade) gives n_s 0.967–0.970, r 5.1–5.6e-4 [derived] (interpolation of computed rows).
8. [derived] Consistency: D781's frozen-band condition is violated by construction (T₂ < 1e5), so this is an alternative, not a confirmation. The P5 mediator is unnecessary (retired). P1 is not needed at ρ (spontaneous CP).
Touches: lepto_rho (assumed → computed), serapis_e.

## D793 — exact self-diluted ρ spectra (forward side)
1. Matter-like phase to T₂, with N* from the matching equation [literature] (D781 step 1).
2. T₂ ∈ {150, 330, 1100} gives N* 44.9–45.6 [derived] (computed).
3. Exact first-order slow-roll spectra on the D692 potential give n_s 0.9667–0.9703, r 5.13–5.59e-4 [derived] (computed; K4 passes).
4. D792's interpolation agrees to ≤ 1% [derived].
5. Wino T_f = M₂/20 ≤ 92.5 GeV < T₂, so the thermal relic is unchanged [derived].
6. [derived] Consistency: D784's wino window holds. The frozen band is unchanged (this is an alternative). The family strip and cap (D678–D681) contain these points.
Touches: serapis_e, lepto_rho.

## D794: τ = i mirror of the inflaton-AD mechanism (reverse side)
1. Stabiliser of i in PSL(2,Z) is ⟨S⟩ ≅ Z₂; on z = (τ−i)/(τ+i), S: z → −z [derived] (dτ'/dτ = τ⁻² = −1 at i).
2. Stabiliser of ρ is ⟨ST⟩ ≅ Z₃, acting as z → ωz [literature] (standard; used in D777).
3. A real quadratic form invariant under a rotation by 2π/3 is ∝|z|² [derived]. Under z → −z, every quadratic form is invariant [derived].
4. Hence at ρ the U(1) charge Q = i(z̄ż − zż̄) is conserved to quadratic order. At i it is not, unless the masses are accidentally equal [derived]; Δm ≠ 0 in our potential [estimate].
5. An asymmetry needs an additive charge carried by the decay products. At ρ that is Z₃ (baryon triality, D787) [derived, D787–D792]. At i the only residual is a parity, Z₂ (or Z₄, whose charge −1 states are Z₂-like) [derived].
6. So there is no inflaton-AD asymmetry at i, and D745 stands as the only τ = i baryogenesis route, needing explicit CP in the heavy-ν couplings [derived].
Touches: lepto_i, lepto_rho.

## D795: isotropy at τ = i (forward side)
1. S fixes i and acts as z → −z; j ∘ S = j, so j − 1728 is even in z with a double zero: j − 1728 = c z²(1 + b z² + O(z⁴)) [derived].
2. |j − 1728| = |c||z|²(1 + Re(b z²) + …) [derived]. Hence V = F(|j − 1728|) has U(1) symmetry at O(|z|²), broken at O(|z|⁴) [derived].
3. The metric −3 ln(2y) is conformally flat (isotropic) [derived]. So the canonical masses are equal, R = 1 [derived]; numerically 1 − 1.3e-7 [derived] (computed).
4. So the orbit charge is approximately conserved at i too, and D794 step 4 is corrected [derived].
5. The asymmetry needs a conserved carrier among the decay products. At ρ that is the Z₃-charged Dirac-like pair [derived, D777–D792]; at i the products are Majorana parity eigenstates (D785), so there is no carrier [derived].
6. A Kähler-connection chemical potential exists, but L-violation is out of equilibrium at T_R ~ 1e6 GeV [estimate].
Touches: lepto_i, lepto_rho.

## D796: Z₃ structure of the SERAPIS-E potential at ρ (reverse side)
1. ST fixes ρ and acts as z → ω z on z = (τ−ρ)/(τ−ρ̄) [literature] (D777).
2. Z₃ forces the quadratic form to be ∝|z|² [derived] (D794 step 3); computed R = 1 ± 1e-8 [derived] (computed).
3. Smooth Z₃-invariant terms: |z|²ⁿ, Re(e^{iφ} z³)|z|²ᵐ, Re z⁶ …. So the angular modes are k ≡ 0 mod 3, with relative orders r (k = 3) and r⁴ (k = 6) [derived]; confirmed numerically [derived] (computed).
4. The CP line Re τ = ½ is a reflection axis, so the cos 3θ term is aligned with it (no sin 3θ about θ_CP) [derived].
5. Torque ∝ |z|³ sin 3(θ−θ_CP); Q freezes after O(1) oscillations [derived] (standard AD scaling).
6. η ∝ Δx at small offsets [derived]; coefficient O(1–10) [estimate], compatible with D790's 2 [derived] (D790, computed).
Touches: lepto_rho, lepto_i, serapis_e.

## D797: can P3's 1/E goldstino metric be derived? (forward side)
1. Tree level: anti-D3 uplift ∝ e^{4A}/(T+T̄)³, no torus-τ dependence without warping [literature] (1707.07059).
2. One loop: annulus KK/winding sums give Epstein E(τ,s) [literature] (BHK; D756).
3. Required: K^{XX̄} = a − b/E [derived] (P3 form rearranged).
4. Additive k₁E in K_XX̄ gives a hilltop (k₁ > 0) or negative metric (k₁ < 0) [derived].
5. A Casimir term −cE is unbounded below [derived].
6. No standard route gives the needed denominator; P3 remains a postulate [postulate P3].
Touches: plateau_origin, serapis_e.

## D798: DKL-threshold plateau at ρ (reverse side)
1. Δ = −ln(y|η|⁴) is modular invariant, the s → 1 Kronecker limit [literature].
2. Its minimum is at ρ [literature] (confirmed numerically here).
3. Z₃ gives Δ̃ ∝ |z|², so p = 1 is massive and isotropic (R = 1), p = 2 is quartic [derived] (computed).
4. Δ ~ πy/3 gives an α-attractor with α = 1/p² [derived]; the log correction lowers r by 37–55% versus leading order [derived] (computed).
5. p = 1 violates y* ≲ 25 [derived]; p = 2: n_s 0.963–0.966, r 5.4–6.5e-4 [derived] (computed).
6. A massive p = 2 version needs the ε Δ̃ term, the ρ analogue of the two-term model [derived].
Touches: plateau_origin, serapis_e.

## D799: can a gaugino condensate place Δ for P3? (forward side)
1. W = Ω(S)H/η⁶, with weight −3 [literature] (2212.03876).
2. H is polynomial in j (× G₄, G₆ powers) [literature].
3. e^K|W|² ≳ y⁻³e^{πy}, growing at the cusp [derived].
4. Uplift − condensate is unbounded below; uplift + condensate is a wall [derived].
5. GS mixing: e^{K_S} = 1/(2 Re S − δ_GS Δ) also grows [derived].
6. A plateau requires saturation at the cusp, i.e. inverse-metric placement [postulate P3].
Touches: plateau_origin, serapis_e.

## D800: SERAPIS-Δ (reverse side)
1. Δ̃ ≈ (π/3)y − ln y − c′ on the cusp [derived].
2. In Y = Δ̃ the model is the two-term form, but φ = ln y/√2 [derived].
3. The log term slows Y, so y* ≈ 28–30 and r ≈ 2.3–3.4e-4 [derived] (computed).
4. Log offset → consistency-relation bias −25% [derived] (computed).
5. y* exceeds the 25 cut [derived]; disfavoured.
6. m²/H² ~ 1e-4 → quartic start [derived] (computed).
Touches: plateau_origin, serapis_e.

## D801: lattice sums select ρ (forward side)
1. E(τ,s) is uniquely minimised at ρ for all s > 0 [literature] (Rankin, Cassels, Ennola, Diananda; 1504.01153).
2. The theta function behaves the same [literature] (Montgomery 1988).
3. Positive combinations (one-loop integrals) are minimised at ρ [derived].
4. i is a saddle: minimum along the axis, maximum along the arc [derived] (computed for E(τ,2) and Δ).
5. A vacuum at i requires a non-lattice function [derived]; the caveat on mixed-sign sums is [estimate].
Touches: plateau_origin, serapis_e.

## D802: BHK term at the τ = i vacuum (reverse side)
1. V = P(τ)[1 + C(E − E_ref)] [literature] (BHK; D689).
2. At a vacuum with P = ∇P = 0, Hess V = (1 + CẼ)·Hess P [derived].
3. Additive remnant from no-scale breaking, ∝ C·E_xx·|W₀|² [estimate].
4. C_crit ~ 1e-4 versus a natural C ~ 1e-6 [derived] (arithmetic on locked outputs).
5. The τ = i vacuum is stable [derived].
Touches: serapis_e, plateau_origin.

## D803: mixed-sign one-loop sums (forward side)
1. Scherk–Schwarz: one-loop energy = difference of shifted lattice sums [literature] (2504.19364).
2. The reduced group (index 3) has ε₂ = 1, ε₃ = 0 [literature].
3. The image of i is enforced critical; ρ is not [derived].
4. The computed minimum is at 1 + i [literature].
5. D801 holds only for positive sums [derived].
6. The SERAPIS-E sector is SUSY-like, so the BHK picture applies [estimate].
Touches: plateau_origin, serapis_e.

## D804: flavour under the reduced group (reverse side)
1. Γ⁰(2)/Γ(2) ≅ Z₂ [literature].
2. It is generated by TST⁻¹ (b even, order 2, fixes 1 + i) [derived] (checked).
3. The S₃ doublet → 1 ⊕ 1′ with free couplings, and the doublet predictions are lost [derived].
4. The Z₂ residual at 1 + i keeps the parity-eigenstate structure [derived].
5. ε₃ = 0: ρ has a trivial stabiliser, losing Z₃, isotropy and the critical point [derived].
6. SERAPIS-E needs the full SL(2,Z) [derived].
Touches: serapis_e, n_sector_rho, lepto_i.

## D805: data check (forward side)
1. New n_s values [literature] (2512.05108).
2. σ-distances [derived] (computed).
3. Shifts are 0.30–0.33σ, below the flag threshold [derived].
4. With DESI, the frozen band is centred and the post-hoc ρ alternative is at −1.5 … −2.7σ [derived].
Touches: serapis_e.

## D806: α_s reach (reverse side)
1. Best 2030 combination σ(α_s) ≈ 8.7e-4 at 1σ [literature] (2212.04115).
2. SERAPIS signal 1.0–1.2σ [derived].
3. 3σ enhancement needs σ ≈ 1.8e-4 [derived].
4. The α_s leg is post-2030s [derived]; candidate probes (21-cm, distortions) are [estimate].
Touches: serapis_e.

## D807: referee merge (accuracy track)
1. Referee findings checked against the D-notes [derived] (each fix cites its source note).
2. Completely monotone f → hexagonal minimum (Montgomery + Bernstein) [literature] (referee; 1504.01153).
3. Half-period character sums are invariant only under index-3 subgroups; the equal-brane total restores SL(2,Z) [derived] (referee's identity Σ_k E₂(φ_k) = −¾E).
4. No frozen prediction changed [derived].
Touches: serapis_e, band_e, wino_window.

## D808: referee deferrals (accuracy track)
1. Wino window 0.67–1.85 TeV [derived] (D784).
2. m₃/₂ ∝ M₂ and m_gluino ∝ M₂ under anomaly mediation [literature] (D650).
3. So m₃/₂ ≤ 1.1e6 × 1.85/2.9 = 7.0e5 GeV and gluino ≤ 21 × 1.85/2.9 = 13.4 TeV [derived].
4. τ = i Σm_ν = 0.059–0.064 eV with m₁ free [derived] (D786).
Touches: wino_window.

## D809: gravitino → wino, full yield (accuracy track)
1. Y₃/₂ = Σ yᵢgᵢ²(1 + Mᵢ²/3m₃/₂²) ln(kᵢ/gᵢ)(T/1e10) [literature] (Pradler–Steffen hep-ph/0612291).
2. One-loop MSSM couplings [estimate].
3. K4 at 1e10: identical to the old fit [derived] (computed).
4. Ω_nth = 2.74e8·M₂·Y ≤ 2.6e-4 in all histories [derived] (computed).
5. Dilution by T₂/T_R [estimate]; the margin of ≥40× covers it [derived].
6. Wino window unchanged; D732's 1e13 restriction is moot after D780–D783 [derived].
Touches: gravitino_wino, wino_window.

## D810: orbit-charge coefficient (accuracy track)
1. The charge read-out must be centred on the settling image [derived] (lesson D790).
2. The Möbius-invariant normalisation χ = √2|w| holds for any centre [derived].
3. |η|/Δx = 1.74–2.05 [derived] (computed).
4. CP mirror: η(1 − x₀) = −η(x₀) [derived] (computed exactly).
5. The sign alternates with the offset (winding), so the sign of Y_B is an initial-condition choice [derived].
6. D796's 9Δx estimate is corrected to ≈2Δx [derived].
Touches: lepto_rho, serapis_e.

## D811: BHK remnant at τ = i (accuracy track)
1. V_τ ∝ 4y²|∂_τL|² [literature] (D684).
2. δK = CE gives ∂_τL + C∂_τE [derived].
3. Same-sign x-curvatures, so g_xx = 2(L_xx + CE_xx)² ≥ 0 [derived] (computed).
4. Linear coefficient +4L_xxE_xx [derived] (computed 4.09).
5. C_crit = ∞; D802's estimate corrected (D802a) [derived].
Touches: serapis_e.

## D812: exactness audit (accuracy track)
1. MS is exact to all orders in slow roll; first-order SR carries O(ε, η²) errors of ~1e-3 in n_s on these plateaus [literature] (standard; cf. D635's 11–13% bias of the closed form).
2. Script inspection decides each number's method [derived].
3. D781/D793 use SR1, not MS [derived] (late_reheat_d781.py line 15).
4. Six numbers are flagged for MS [derived].
Touches: serapis_e.

## D813: exact self-diluted spectra (accuracy track)
1. MS solver verbatim from D632/D692 [derived] (K4 passes).
2. N* from D793 (late-matter phase to T₂) [derived] (D781).
3. MS gives n_s 0.9664–0.9699, r 5.20–5.66e-4, α_s −(1.08–1.18)e-3 [derived] (computed).
4. SR1 error: Δn_s ≈ −0.0004, Δr ≈ +1.5% [derived].
5. Versus CMB-SPA+DESI: −3.1 … −1.5σ [derived].
Touches: lepto_rho, serapis_e.

## D814: exact 2⊕1 band (accuracy track)
1. N* from the D725 matching [derived] (read from results).
2. MS gives n_s 0.9729–0.9736, r 4.66–4.75e-4 [derived] (computed).
3. SR1 offset −0.0003 / +1.2% [derived].
4. Still inside the frozen D693 band [derived].
Touches: n_sector_rho, serapis_e.

## D815: exact Chronos at the corrected T_R (accuracy track)
1. D632 MS code, K4 against D642 [derived] (passes).
2. MS rows agree with D729 to ≤ 0.0001 in n_s; r is +1.5% [derived] (computed).
3. Exact ε window for the actual (stiff, N* ≈ 50.3) history: 1.40–1.45e-4 [derived] (computed).
4. The frozen τ = i band is unchanged (it is frozen); only the "meets the band" statement is refined [derived].
Touches: nstar_i, band_i.

## D816: exact check of the frozen ρ band (accuracy track)
1. D634 MS code, K4 passes [derived].
2. MS gives n_s 0.9691–0.9722, r 4.67–5.16e-4, α_s −(8.7–9.9)e-4 [derived] (computed).
3. Versus frozen 0.969–0.972 / 4.6–5.1e-4: r top +1.2% [derived].
4. The excess equals the SR1 r bias (~+1.5%) [derived]. Frozen numbers are kept per the lock rule [derived].
Touches: band_i.

## D817: D722 exact and the τ = i band line (accuracy track)
1. MS at the D722 N* gives n_s 0.9731–0.9746 [derived] (computed; K4 passes).
2. The τ = i frozen band versus MS (D642, D815) is the same to rounding [derived].
3. Across D813–D817 the SR1 bias is uniform: n_s +0.0003, r −1.3% [derived].
Touches: n_sector_rho.

## D819: published-papers merge (accuracy track, A0)
1. MICROSCOPE final σ_η = 2.75e-15 [literature] (2209.15487).
2. η ≈ 1e-3 ζ² gives ζ ≲ 1.66e-6 [literature] (Martins 2204.02930; arithmetic [derived]).
3. Suppression 2.0–3.4e3 (MICROSCOPE), ~1e5 (combined, 2105.09746) [derived].
4. Clock relation R = ζ gives 1 + w₀ ≲ (2–6)e-13 [derived].
5. The Twist and Twist-2 corrections are taken from D387–D475, as listed in the addenda [derived].
Touches: none.

## D820: r detectability (accuracy track)
1. LiteBIRD δr = 1e-3 total; σ_stat = 6e-4 [literature] (2406.02724).
2. SERAPIS r = (4.6–5.7)e-4 is < 1σ [derived].
3. The live r test is exclusion at r ≳ 1e-3 [derived].
Touches: none.

## D821: error budgets (accuracy track)
1. MS slopes in N* [derived] (from D642, D692, D815).
2. Convention ±0.5 e-fold [estimate].
3. SR bias [derived] (D817).
4. Two-loop Kähler ≲ 1e-4 [estimate].
5. Edge uncertainty ±0.0005–0.0006 in n_s, well below the data σ; the dominant risks are conditional [derived].
Touches: band_e, band_i.

## D822: pruning (accuracy track)
1. Keep rule: a source, or a unique test within reach [derived] (A4).
2. Log-derivative plateau: no source (D760); r below LiteBIRD 1σ (D820); retired [derived].
3. SERAPIS-Δ: fails the y* cut (D800); retired [derived].
Touches: logderiv_plateau, serapis_e.

## D823: BHK tilt on the τ = i plateau (accuracy track)
1. Multiplicative BHK factor [literature] (D689).
2. E ∝ y²: κ = 1 ramp [derived].
3. MS: band at C ≈ 3.4–6.5e-7 (natural) [derived] (computed).
4. Different r(n_s) and α_s (−1.0 to −1.2e-3) from the frozen ε-model [derived] (computed).
5. The vacuum stays massless, so ε is not derived [derived].
Touches: eps_tilt, band_i.

## D824: Σm_ν status (accuracy track)
1. Bounds < 0.064 / < 0.0592 eV [literature] (2503.14744; 2607.27410).
2. Frozen 0.0587 survives by 0.0005 eV [derived].
3. Below 0.0586, NO + ΛCDM fails generally [derived]; a forecast 3σ rejection is possible with SO + DR3 [literature] (2610.20977).
4. The Σm_ν entry is not SERAPIS-specific [derived].
Touches: mnu.

## D825: flags and consistency sweep (accuracy track)
1. Flag justifications [derived] (D822, D823).
2. Stale values in non-paper documents replaced by the v3.1 values [derived] (D784, D786, D807, D808).
Touches: none.

## D826: τ = i vacuum-mass sources (accuracy track)
1. Needed m²/H² ≈ 2e-3 [derived] (D795).
2. Covariant F-term: 3R·2y²g_xx ≈ 1.6e-15 – 1.3e-14 [derived].
3. BHK factors cannot help (multiplicative; remnant ×1.0003) [derived].
4. Holomorphic h(τ) destroys the plateau [derived] (D685).
5. The only candidate is the anti-D3 log correction [postulate P3] (D686).
Touches: eps_tilt, band_i.

## D827: manifest and status (accuracy track)
1. Lock order from git first-commit times: no K1 failures [derived] (computed in a short script; the listing has no results file).
2. Status summary compiled from D807–D826 [derived].
Touches: none.

## D828: P3.1 literature (P3 deep project)
1. Tree-level anti-D3 has no U dependence [literature] (1707.07059).
2. One-loop vacuum energies are additive lattice sums E(U,s) with characters [literature] (2512.20570; hep-ph/0004091).
3. Additive ±E is a wall or unbounded below, not a plateau [derived].
4. In V_up = |F|²K^{XX̄}, additive means E in the numerator; P3 needs it in the denominator [derived].
5. P3 is not supported at one loop; P3.2 sets up the actual amplitude [derived].
Touches: plateau_origin, serapis_e.

## D829: P3.2 anti-D3 amplitude (P3 deep project)
1. Anti-D3–D3/O3 interaction on T² is the torus Green's function, closed-channel s = 1 shifted lattice sums [literature] (Polchinski §7.2; D828).
2. Half-period sum S(U) = −2 ln 2 for all U (θ₂θ₃θ₄ = 2η³) [derived] (computed, PREREG_D829).
3. Case A V ∝ Δ(U) = −ln(y|η|⁴), linear in y at the cusp [derived].
4. Case B V ∝ 5Δ + 5S − 4G(½), non-monotone [derived].
5. Enters V additively; K_XX̄ unchanged at this order [derived].
6. P3's inverted form does not arise at one loop [derived].
Touches: plateau_origin, serapis_e, eps_tilt.

## D830: P3.3 anti-D3 placement (P3 deep project)
1. Tadpole with one anti-D3 needs 17 D3 units: (5, 2), N_eff = 3 [derived] (D696).
2. Anti-D3 on top of D3s annihilates [literature] (hep-th/9805170).
3. Mobile anti-D3 on T² falls into a D3 stack [derived] (D829).
4. Stable placement: stuck at an empty O3 point, displaced in T⁴ [derived] (hep-th/0602038).
5. Shape dependence stays additive E-type sums [derived] (D828, D829).
Touches: plateau_origin, serapis_e, eps_tilt.

## D831: P3.4 anti-D3 size and shape (P3 deep project)
1. T⁴-displaced coincidence regularises to Δ(U) + const [derived] (D830).
2. Weights +2 per D3, −2 per O3 unit, (5, 2) stacks [derived] (D696, D830).
3. V = −2κB; slope dB/dy → −2π/3, a rising wall [derived] (computed, PREREG_D831).
4. V(ρ) − V(i) < 0 in both placements [derived].
5. Opposite large-y behaviour to P3's 1 − b/E [derived].
6. Size bound κ/V0 ≲ 2.9e-3/y*; κ's normalisation open [estimate].
Touches: plateau_origin, serapis_e, eps_tilt.

## D832: P3.5 verdict (P3 deep project)
1. Anti-D3 one-loop is additive; K_XX̄ unchanged [derived] (D828, D829).
2. Stable placement and (5, 2) tadpole [derived] (D830).
3. Rising wall, opposite asymptotics to P3 [derived] (D831).
4. P3 kept as a postulate, downgraded: no one-loop origin [derived].
5. Remaining routes: warped throat, non-perturbative, other origin [estimate].
6. Side: anti-D3 term as decompactification wall and τ = i mass candidate, pending κ [estimate].
Touches: plateau_origin, serapis_e.

## D833: K.1 κ normalisation (κ deep project)
1. Per-sector D3–D3 exchange |V| = 2κ₁₀²T₃²G₆ [literature] (Polchinski §13.3).
2. 2κ₁₀²T₃² = 2π [derived] (checked in code, PREREG_D833).
3. T⁴ zero mode gives κ = 1/(2Vol₄) [derived] (D829, D831).
4. κ/V0 = g_s/(8πv₄) with V0 = 2T₃ [derived].
5. Slope bound needs v₄ ≳ 190–200 g_s [derived] (computed, PREREG_D833).
6. O(1) sector factors, warping and twisted sectors not included [estimate].
Touches: plateau_origin, serapis_e, eps_tilt.

## D834: K.3 τ = i mass from the anti-D3 term (κ deep project)
1. B from D831 with stacks (5, 2) and O3 weight 4 [derived] (D830, D831).
2. Canonical masses at y = 1: d²V/dφ² = 2V_yy, d²V/dχ² = 2V_xx [derived] (family K = −ln).
3. z_a = 0: extremum, saddle, m²/H² = −1.48e-3 (x), +6.45e-3 (y) at κ_max [derived] (computed, PREREG_D834).
4. z_a = ½: not an extremum [derived].
5. Not the τ = i mass source; destabilises τ = i along x; ρ unaffected [derived] (D691, D826).
Touches: band_i, eps_tilt, plateau_origin.

## D835: K.4 anti-D3 term in SERAPIS-E (κ deep project)
1. On x = ½ with z_a = 0, B = −2Δ + S, V_add/V0 = 4k[Δ − Δ(ρ)] [derived] (D829, D831).
2. Exact MS with C = 1e-6: k = 5e-5 gives n_s 0.994–0.997, r ≈ 1e-3 [derived] (computed, PREREG_D835, DEVIATIONS D1).
3. Harmless rule fails; k_max run fails to bracket [derived].
4. D831/D833 slope criterion too loose; revised k ≲ 2e-6, v₄ ≳ 2e4 g_s [estimate].
5. (C, k) degeneracy noted, post-hoc, not claimed [estimate].
Touches: serapis_e, eps_tilt, plateau_origin.

## D836: K.5 κ verdict (κ deep project)
1. κ/V0 = g_s/(8πv₄) [derived] (D833).
2. τ = i saddle, not the mass source [derived] (D834).
3. Exact MS: harmless needs k ≲ 2e-6, v₄ ≳ 2e4 g_s [estimate] (D835).
4. P3 consistent with the band only for a large T⁴ (or a post-hoc C share, not claimed) [derived].
5. ρ safe; τ = i variant weakened [derived].
Touches: plateau_origin, serapis_e, band_i.

## D837: W.1 warped-throat literature (warped-throat project)
1. Conifold modulus S has GVW W and s_KS ≃ Λ₀³e^{−2πK/g_sM} [literature] (1809.06861).
2. S couples to bulk Z^I only indirectly (τ, volume) [literature] (1809.06861).
3. Warping couples S to the volume; anti-D3 energy grows with |S| [literature] (2105.03370; 1809.06618).
4. U enters V_up only via Λ₀(U): multiplicative f(U) [derived].
5. T⁶/(Z₂×Z₂) has no conifold, so route (a) leaves the toroidal model [derived].
6. P3 via (a) needs |Λ₀(U)|⁴ ∝ 1 − E(ρ)/E(U) [derived].
Touches: plateau_origin, serapis_e.

## D838: W.2 throat-cutoff shape (warped-throat project)
1. Invariant f from holomorphic data is Σ c_i y^{w_i}|h_i|², w_i ≥ 0 [literature] (Diamond–Shurman).
2. Non-cusp terms grow as y^{w}; cusp forms decay exponentially [derived].
3. f → constant needs weight-0 constant plus cusp forms: exponential approach [derived].
4. SERAPIS-E's plateau approaches as a power law 1 − c/y² [derived] (D691).
5. Route (a) cannot give P3 in any modular-invariant completion [derived].
6. P3's E-ratio has no identified string origin [derived] (D828–D837).
Touches: plateau_origin, serapis_e.

## D839: W.5 warped verdict (warped-throat project)
1. Warped uplift couples to U multiplicatively; torus has no conifold [derived] (D837).
2. Holomorphic invariant factors give exponential plateau approach only [derived] (D838).
3. Route (a) closed for P3; W.3, W.4 moot [derived].
4. P3 has no identified string origin; predictions unaffected [derived] (D828–D838).
Touches: plateau_origin, serapis_e.

## D840: T.1 τ = i evidence table (τ = i verdict project)
1. Fifteen items collected and checked against their notes [derived] (D664a–D839).
2. Correction D834a: the anti-D3 term does not destabilise τ = i at band-allowed k [derived] (D795, D834, D835).
3. Tally + 4, − 6, 0 5; minuses concern motivation and origin, not data [derived].
Touches: band_i, eps_tilt.

## D841: T.2 τ = i decision (τ = i verdict project)
1. Decision rule committed before applying [derived] (DECISION_RULE_D841).
2. R1 not met: frozen band overlaps current n_s, r, Σm_ν bounds [literature] (D824; CMB-SPA, SPA+DESI).
3. R2 not met: stable vacuum, frozen band reproduced in exact MS [derived] (D811, D815, D834a).
4. C1 and C3 met; C2 ambiguous in units, outcome independent of it [derived].
5. Outcome: keep as conditional variant [derived].
Touches: band_i, eps_tilt.

## D842: T.3 τ = i consequences (τ = i verdict project)
1. Status note added to the prediction sheet; frozen numbers unchanged [derived] (D841).
2. MANIFEST addendum: six locks, commit order checked in git, no K1 failures [derived].
3. Current-state summary updated and synced [derived].
4. Stale-wording sweep clean [derived] (D834a).
Touches: none.

## D843: C.1 CP sources literature (P1 deep project)
1. CP is an outer automorphism of the symplectic modular group in IIB orientifolds [literature] (2010.10782).
2. CP violation is spontaneous, via axion vevs [literature] (2010.10782; 1901.03251).
3. Toroidal prepotentials give no spontaneous CPV in flux vacua; Kähler axions not studied [literature] (2010.10782).
4. P1's independent coupling phases conflict with the generic string expectation [derived].
5. Remaining sources in our setup: Kähler axions, brane/Wilson-line moduli [derived].
6. P1 not falsified; must be reformulated with a named breaking modulus [derived].
Touches: none.

## D844: C.2 CP-odd fields in our setup (P1 deep project)
1. CP swaps the U/2 and (1+U)/2 stacks at ρ; equal stacks are CP-invariant [derived] (D696, D830).
2. Stuck D3 Wilson lines are Z₂, CP-even [derived].
3. Kähler axions are flat in our V; single-exponential stabilisation is CP-conserving [derived]; real racetracks generically too [estimate].
4. S, U₂, U₃ flux-stabilised in a toroidal prepotential: no spontaneous CPV [literature] (2010.10782).
5. No spontaneous CP source in the specified configuration; δ = 0 unless extended [derived].
Touches: none.

## D845: C.3 racetrack CP scan (P1 deep project)
1. CP-invariant racetrack W = W0 + e^{2πiT/N1} + B e^{2πiT/N2} with real coefficients [derived] (PREREG_D845).
2. 90% of 540 points have CP-odd local minima in mirror pairs [derived] (computed).
3. Often metastable or near-degenerate with CP-even minima [derived].
4. Competing axion cosines give spontaneous CPV with CP-invariant inputs [derived].
5. Vacuum selection, uplift and the three-modulus structure not included [estimate].
6. P1 can be reformulated with a named source (Kähler-axion racetrack) [derived].
Touches: none.

## D846: C.4 P1 verdict (P1 deep project)
1. CP is a string symmetry; specified config has no CP source; racetrack gives CP-odd axion minima [derived] (D843–D845).
2. P1 replaced by P1′: spontaneous CPV by a Kähler-axion racetrack [derived].
3. δ becomes vacuum-dependent, not a uniform prior [derived].
4. New ingredients and open vacuum selection [derived].
5. No frozen prediction changes [derived].
6. New falsifiers stated [derived].
Touches: none.

## D847: V.1 v3.2 draft accuracy edits
1. Draft file copied from v3.1; published file untouched [derived].
2. D822, D823, D824, D826 applied with D-note numbers [derived] (D822–D826).
3. 2610.20977 bib entry checked online [literature].
4. Draft compiles, 16 pages, no undefined references [derived].
Touches: none.

## D848: V.2 v3.2 draft P3, tadpole, τ = i, P1′ edits
1. Tadpole (5, 2) with anti-D3 added [derived] (D830, D831).
2. P3 caveat rewritten: no identified string origin, large-tori requirement [derived] (D828–D839).
3. τ = i conditional-variant bullet [derived] (D841).
4. CP paragraph and bullet rewritten for P1′; stale P2 clause removed [derived] (D843–D846, D772).
5. 16 pages, no undefined references, no overfull boxes; v3.1 file unchanged [derived].
Touches: none.

## D849: V.3 v3.2 checks and changelog
1. Every new number checked against its D-note by script; one rounding (563 → 560) noted [derived].
2. Two abstract contradictions fixed (CP, plateau origin) [derived] (D839, D846).
3. Changelog written, PDF built, 16 pages, clean log [derived].
Touches: none.

## D850: V.4 referee on the v3.2 diff
1. Internal labels (P1′, N_eff, v₄) undefined in the paper: removed or defined [derived].
2. Holomorphic-factor claim narrowed to D838's scope [derived] (D838).
3. Racetrack figure scoped; D823 bullet clarified [derived] (D823, D845).
4. Rebuilt clean, 16 pages [derived].
Touches: none.

## D851: Q.1 P1′ phase distribution (P1′ follow-up)
1. Same racetrack model and grid as D845, new locked script [derived] (PREREG_D851).
2. θ₁ generic: |sin θ₁| > 0.1 in 100%, > 0.5 in 84% [derived] (computed).
3. θ₂ less generic: > 0.1 in 51% [derived].
4. Deepest minimum CP-odd in 41% of points; otherwise near-degenerate (median ratio 0.95) [derived].
5. Grid robustness 54/54 [derived].
6. P1′ passes the locked phase-support rule for θ₁; depends on which exponential the heavy ν carry [derived].
Touches: none.

## D852: Q.2 instanton phase (P1′ follow-up)
1. Heavy-ν Majorana masses from D-instantons, M ∝ e^{2πinT} [literature] (hep-th/0609191; IIB mirror, estimate).
2. Kähler normalisation and Dirac Yukawas carry no phase [derived] (D844).
3. A common phase is removable; CPV needs Δn ≠ 0, Δ = 2πΔn⟨Re T⟩ [derived].
4. |sin Δ₁| > 0.1 in 80.3% of CP-odd vacua; 19.7% near zero [derived] (computed, PREREG_D852).
5. P1′ gains a two-sector condition; draft updated [derived].
Touches: none.

## D853: Q.3 P1′ verdict (P1′ follow-up)
1. D762 per-case thresholds re-weighted with the D852 phase histogram [derived] (arithmetic on locked outputs).
2. Given a CP-odd vacuum: median 0.84, min 0.48 (P1: 0.95, 0.62) [derived].
3. Deepest-vacuum selection: unconditional median ≈ 0.34 [estimate].
4. P1′ final form: racetrack axion plus two instanton sectors [derived] (D845–D852).
Touches: none.

## D854: R.1 τ = i phase map (P1′ at τ = i)
1. Instanton charge scales with wrapping, so n_ij ∝ q_i + q_j on one cycle class [derived] (hep-th/0609191 zero-mode counting).
2. Doublet members share charge, hence phase [derived] (D664a, D690).
3. Singlet mixing transmits no relative phase on one cycle class [derived].
4. τ = i resonant ε = 0 under single-modulus P1′; D763's 68–71% becomes 0% [derived] (D763).
5. Escape: two cycle classes with CP-odd axions [derived].
Touches: lepto_i, band_i.

## D855: R.2 ρ charge check (P1′ at ρ)
1. ρ's frozen band has no baryogenesis mechanism; the AD history needs no phase [derived] (D780, D789, D792).
2. D853's ρ re-weighting is moot; D854's ρ charge claim unsupported (D853a) [derived].
3. P1′ matters only for τ = i, which needs two CP-odd axions [derived] (D854).
4. Brane placement of ρ's heavy states undetermined [estimate].
Touches: lepto_i, lepto_rho.

## D856: V.5 draft update for D854/D855
1. τ = i two-cycle-class condition added to the CP paragraph and both caveat bullets [derived] (D854).
2. ρ branch stated not to use the phase [derived] (D792, D855).
3. Rebuilt clean, changelog and PDF updated [derived].
Touches: none.

## D857: M.1 moduli requirements (moduli-consistency project)
1. Untwisted 4-cycle moduli Im T_i ≈ A_jA_k/g_s; v₄ = A₂A₃ [derived] (standard IIB O3/O7; O(2π) factors estimate).
2. Requirements from D696, D835, D845, D852, D783 tabulated [derived].
3. Conflict A: no untwisted 4-cycle can host the CP-odd racetrack if BHK and the anti-D3 bound both hold [derived].
4. Conflict B: E3 masses on the racetrack cycle scale as W0^N; need W0 ≈ 0.07–0.3, outside the D845 scan [derived].
5. D689's Im S convention (1.13 at g_s = 0.1) unexplained; flagged [estimate].
6. Escapes: twisted blow-up cycles, no anti-D3, fractional instantons [estimate].
Touches: lepto_i, serapis_e, plateau_origin.

## D858: V.6 full referee fixes
1. Independent referee found 10 major consistency issues, mostly stale v3.0/v3.1 text [derived] (REFEREE_v3.2_full.md).
2. All majors and three minors fixed as wording/table changes; frozen numbers unchanged [derived].
3. Rebuilt clean, 16 pages; twelve minors deferred [derived].
Touches: none.

## D859: M.2 conventions and escapes (moduli-consistency)
1. D689 uses Im S = 1/(2√2π g_s) (BHK normalisation) [derived] (bhk_tilt_d689.py).
2. ρ-to-area conversion carries up to 4π² [estimate].
3. With discrete torsion (needed for rigid branes) h¹¹ = 3: no twisted Kähler moduli [literature] (0902.1694; hep-th/0602038).
4. Twisted-cycle racetrack escape closed [derived].
5. Fractional rigid instantons S = σ[T + …] remain [literature] (0902.1694).
6. No-anti-D3 escape remains [derived].
Touches: lepto_i, serapis_e.

## D860: M.3 moduli feasibility scan (moduli-consistency)
1. Constraints C1–C5 from D696, D835, D845, D852, D783 on (g_s, A₁, A₂, A₃) [derived] (D857, D859).
2. Anti-D3 on: no passing point in any convention or σ [derived] (computed, PREREG_D860).
3. Anti-D3 off: passing points for σ ≤ ½, all at A₂ = A₃ = 1 [derived] (computed).
4. P3's anti-D3 and P1′'s racetrack are incompatible in our configuration [derived].
5. O(1) factors, grid edge and assumed σ [estimate].
Touches: lepto_i, plateau_origin, band_i.

## D861: M.4 benchmark and M.5 verdict (moduli-consistency)
1. Benchmark g_s = 0.232, A = (40.8, 1, 1): C = 1.25e-6, M_s = 7.5e16 GeV, Im T₁ = 4.31, M = 9.8e10 GeV [derived] (arithmetic on locked formulas).
2. Benchmark has string-size small tori, so it is not under geometric control [estimate].
3. Under DECISION_RULE_D841, R2 is not met: the conflict is between postulated ingredients and is removable [derived].
4. τ = i stays conditional with a further condition (no natural-size anti-D3; string-size T⁴) [derived] (D860).
5. ρ branch unaffected [derived] (D855).
Touches: band_i, lepto_i, plateau_origin.

## D862: α′ control at string-size tori
1. BBHL correction at the benchmark is 0.29% (χ = −96) [derived] (computed, PREREG_D862).
2. Worldsheet-instanton-type terms e^{−2πA} are sub-percent for A ≥ 1 [derived].
3. With A_i ≥ 2 only one edge point survives; none at A_i ≥ 3 [derived] (computed).
4. Locked verdict formally "controlled", in practice marginal [derived].
5. Loop corrections to K for T₁ (∝ 1/(Im S·Im T₁) ≈ 0.5) not computed, likely the weak point [estimate].
Touches: lepto_i, band_i.

## D863: loop correction to the racetrack modulus
1. BHK one-loop δK = c′/t with c′ ≈ 0.008 at the benchmark [derived] (D689 normalisation).
2. CP-odd minima unchanged in 24/24 cases at ×1, ×10, ×100 [derived] (computed, PREREG_D863, DEVIATIONS D1).
3. D862's "≈ 0.5" estimate omitted 1/256π⁶; withdrawn (D862a) [derived].
4. Remaining control issues: string-size tori, assumed σ [estimate].
Touches: lepto_i, band_i.

## D864: D7 stacks for the racetrack
1. The orientifold has O3 and three O7 sets [literature] (hep-th/0602038).
2. 11 D7₁ fit the tadpole of 16 [estimate].
3. Torsion requires rigid D7s at T²₁ fixed points for pure-SYM condensation [estimate].
4. Flavour counting forces SU(5) at the origin, SU(6) at a half-period [derived] (D830 stacks).
5. Asymmetric D7 placement adds O(10–50%) to the tilt; benchmark must be re-fitted [estimate] (D689, D861).
Touches: lepto_i, serapis_e, eps_tilt.

## D865: D7 contribution to the tilt
1. D864's half-period placement breaks SL(2,Z); both stacks must sit at the origin (D864a) [derived].
2. Origin D7s reduce N_eff by 11·r·Im S/Im T₁ [estimate] (BHK structure, r = O(1)).
3. At the benchmark this is 0.6–2.5, rescaling Im S·Im ρ₁ by ×0.38–0.85 [derived] (arithmetic).
4. Symmetric placement keeps SL(2,Z), ρ vacuum and tilt shape [derived].
5. Benchmark re-fit: A₁ ≈ 16–35 at fixed g_s [estimate].
Touches: serapis_e, eps_tilt, lepto_i.

## D866: BHK D7 term and modulus mapping
1. BHK (3.30): D3-type term ℰ₂(A,U^I)/((S−S̄)(T^I−T̄^I)); D7-type term ℰ₂(0,U^I)/((T^J−T̄^J)(T^K−T̄^K)) [literature] (hep-th/0508043).
2. After T-duality T^I is the 4-cycle transverse to T²_I [literature] (hep-th/0508043 §5).
3. D7 term is position-independent; D865 arithmetic withdrawn [derived].
4. D689's ρ is the T⁴ modulus, not A₁; D857–D865 mapping superseded (D857a) [derived].
5. Racetrack on T₁ excluded; on T₂/T₃ reopened [derived].
Touches: serapis_e, lepto_i, eps_tilt.

## D867: corrected moduli scan
1. v₄ = A₂A₃ is geometric, independent of the BHK mapping [derived] (D833).
2. Anti-D3 bound and BHK tilt are incompatible for g_s < 3.1 [derived] (computed, PREREG_D867).
3. At the tilt's moduli the anti-D3 would shift n_s by ≈ +0.005 to +0.06 [estimate] (D835 scaling).
4. Racetrack on T₂/T₃ passes for σ ≤ ½, only at string-size tori and g_s ≈ 0.4–0.5 [derived] (computed).
5. D857–D861 mixed branches: BHK belongs to ρ, P1′ to τ = i; D861's τ = i condition withdrawn (D861a) [derived].
Touches: plateau_origin, serapis_e, band_i, lepto_i.

## D868: SERAPIS-E uplift alternatives
1. Distant sequestered anti-D3 avoids the U₁ term but needs a throat outside the torus [estimate] (D837, D838).
2. T-brane D-term on the T⁴ cycle adds only an E(U₁,2) piece to C [literature] (1512.04558; D866).
3. Complex-structure F-term uplift couples to U₁ and is hard to control [literature] (2512.17995).
4. Kähler/hidden-sector uplift is U₁-independent at leading order [literature] (hep-th/0611332, 0707.2671).
5. P3's wording must move from "anti-D3 sector" to "uplift sector" [derived] (D867).
Touches: plateau_origin, serapis_e.

## D869: throat anti-D3 residual coupling
1. The throat anti-D3's Coulomb term carries an extra a₀⁴ relative to its uplift [literature] (KKLMMT structure, from memory).
2. k_warped ≈ (g_s/8πv₄)·a₀⁴ [derived].
3. a₀⁴ ~ 1e-6–1e-2 for the plateau height [estimate].
4. k ≤ 1e-8 for a₀⁴ ≤ 1e-4, well under 2e-6 [derived] (D835, D867).
5. Needs a throat outside the torus; plateau shape still postulated [estimate] (D837, D838).
Touches: plateau_origin, serapis_e.

## D870: P3 wording
1. P3 restated as an uplift-sector postulate [derived] (D867–D869).
2. Draft caveat names the throat and T-brane options [derived] (D868, D869).
3. Nilpotent-field wording kept, valid for the throat option [derived].
Touches: plateau_origin, serapis_e.

## D871: referee minors batch 1
1. Six wording/table fixes applied, numbers from existing notes [derived] (REFEREE_v3.2_full.md).
2. α_s testing scale stated as 2e-4 (Janus vs attractor) and 2e-5 (2% relation) [derived] (2% of 9e-4).
3. Rebuilt clean, 17 pages [derived].
Touches: none.

## D872: referee minors batch 2
1. Repository URL, ε_CP rename, constant-W₀ label and abstract trim applied [derived] (REFEREE_v3.2_full.md).
2. All referee items applied or answered [derived].
3. Rebuilt, 16 pages; two cosmetic 2.9 pt float overflows [derived].
Touches: none.

## D873: size of the D7 piece of the tilt
1. BHK (3.30): D3 and D7 terms share c; both E(U₁,2)-shaped [literature] (hep-th/0508043).
2. Moduli ratio (Im S·Im T₁)/(Im T₂·Im T₃) = 1/(2√2π A₁²) [derived].
3. D7/D3 ≈ q/(8.89 A₁²), < 10% unless A₁ ≈ 1 and q ≳ 1 [derived] (arithmetic).
4. Lattice-coefficient ratio q not computed [estimate].
Touches: serapis_e, eps_tilt.

## D874: checkpoint
1. Day summary of D828–D873 written and synced [derived].
2. Open items ranked; ρ baryogenesis inside the frozen band chosen next [derived] (D780, D789, D792).
Touches: none.

## D875: B.1 ρ baryogenesis inventory
1. Binding Z₃ rules collected [derived] (D778–D780, D787).
2. Seven routes tabulated with outcomes [derived] (D725–D793).
3. Tension: frozen band needs fast late decay (T₂ ≳ 1e5 GeV), the working AD route needs slow decay (T₂ ~ 1e2–1e3 GeV) [derived] (D781, D792).
4. Targets for B.2: asymmetry produced at or after T₂ ≳ 1e5 GeV, or a smaller early asymmetry [derived].
Touches: lepto_rho, band_e, n_sector_rho.

## D876: B.2 ρ baryogenesis literature
1. Late re-annihilation baryogenesis needs low T_reh [literature] (1803.00820).
2. Axiogenesis converts a rotation charge partially, via sphalerons [literature] (PRL 124, 111602).
3. Light-mediator CP sources evade Nanopoulos–Weinberg [literature] (2312.08327).
4. Top candidate: suppressed transfer f of the inflaton-AD charge instead of strong dilution [estimate] (D790–D792, D787).
Touches: lepto_rho, band_e.

## D877: B.3 AD transfer fraction
1. Two Z₃-allowed inflaton channels carry ΔB = +2 and −1 [derived] (D780, D787, D789).
2. f = |3b − 1| with b = BR(φ → N_nN_n) [derived].
3. Band-safe T₂ needs f = 1.4e-4–1.1e-2, |b − 1/3| = 5e-5–4e-3 [derived] (arithmetic on D792's formula).
4. A tuning unless a symmetry fixes b = 1/3 [estimate].
Touches: lepto_rho, band_e, n_sector_rho.

## D878: B.3b channel ratio
1. LL = N_nN_n and HL = N_Y N₃ identified by Z₃ charge [derived] (D780).
2. D725 couplings give b = 0.10–0.95 across open cases [derived] (computed, PREREG_D878).
3. f never reaches the required 1.4e-4–1.1e-2 without tuning c [derived].
4. Suppressed-transfer route not natural; ranks 2–3 remain [derived] (D876).
Touches: lepto_rho, band_e, n_sector_rho.

## D879: B.4 verdict and Z₃ flat directions
1. Suppressed-transfer route tuned [derived] (D877, D878).
2. UDD and QQQL forbidden, QDL, LLE, LH_u allowed by Z₃ at ρ [derived] (D780, D787).
3. LH_u AD was missing from the ρ inventory [derived] (D875).
4. LH_u AD at T₂ = 1e5–1e6 GeV needs m_ν₁ ≈ 1e-10–1e-9 eV [estimate] (standard formula, from memory).
5. ρ gains a candidate mechanism inside the frozen band, pending a locked check [derived].
Touches: lepto_rho, band_e, mnu.

## D880: B.5 LH_u AD at ρ
1. n_B/s ≃ 1e-11 δ_eff (m_ν₁/1e-8 eV)^{−3/2}(m_{3/2}|a_m|/TeV), mild T_R^{1/3} below 1e8 GeV [literature] (hep-ph/0102187).
2. At ρ, T_R → T₂ = 1e5–1e6 GeV and m_{3/2} = 2.5e5–7e5 GeV [derived] (D781, covariant completion).
3. Required m_ν₁ = 4e-9–7e-8 eV [derived] (computed, PREREG_D880).
4. ρ has a post-hoc baryogenesis route inside the frozen band [derived].
5. Realistic ρ lepton sector and the condensate's CP phase still open [estimate].
Touches: lepto_rho, band_e, mnu, n_sector_rho.

## D881: B.6 draft update for ρ baryogenesis
1. Abstract and Sec. VII updated to the LH_u AD route at ρ [derived] (D880).
2. Σm_ν footnote now covers both vacua [derived].
3. Rebuilt clean, 17 pages [derived].
Touches: none.

## D882: B.7 ρ lepton sector for tiny m_ν₁
1. D779's minimal extension (Γ₂-singlet leptons plus two neutral singlets) gives rank 3 [derived] (D778, D779).
2. m_ν₁ ≈ y₂²v_u²/M₂ ≈ 1e-8 eV needs y₂²/M₂ ≈ 3e-22 GeV⁻¹ [derived].
3. E₄(ρ) = 0 can protect the lightest direction exactly [derived].
4. Planck-suppressed (LH_u)² must be ≲ 1e-3 of natural size for the lightest direction [estimate] (hep-ph/0008041, title level).
5. Structure exists; no oscillation fit yet [derived].
Touches: n_sector_rho, lepto_rho, mnu.

## D883: B.8 ρ oscillation fit
1. ρ lepton sector: Γ₂-singlet leptons, N_Y, S₁, and S₂ with an E₄-protected coupling ε·y₂ [derived] (D779, D882).
2. 3.5% of random draws give NO with both splittings in 3σ [derived] (computed, PREREG_D883).
3. ε ≈ 1.8e-3 (3e-4–1.1e-2) gives m_ν₁ ≈ 1.7e-8 eV [derived] (computed).
4. Natural by the locked rule; origin of ε open [estimate].
Touches: n_sector_rho, lepto_rho, mnu.

## D884: draft and board update; next project
1. ρ lepton-sector result added to the draft caveat [derived] (D882, D883).
2. Theory Map ρ heavy-ν box updated [derived].
3. Next deep project: origin of τ = i's ε [derived] (D826).
Touches: none.

## D885: E.1 ε reverse path
1. Required term: V_up·(1 + εI₁), weight 0, log of |j − 1728|, double zero at i [derived] (D689a, D826).
2. Nine routes tabulated with their failures [derived] (D576–D834).
3. |j − 1728|^{2q} ≈ 1 + 2q ln|j − 1728| reproduces εI₁ with q ~ 1e-5, linear at y* [derived].
4. A throat cutoff Λ₀(U) ∝ (j − 1728)^{q′} gives it via V_up ∝ |Λ₀|⁴ [estimate] (D837).
5. Small q′ fits a one-loop U-dependence of the throat's UV data [estimate].
Touches: eps_tilt, band_i.

## D886: E.2 throat cutoff literature
1. |z_cf| = (1/2π)exp(−2πK′/n g_s M) with a pure-number prefactor [literature] (2009.03312 eq. 3.22).
2. Bulk dependence only via fluxes and e^{2πiτ}-suppressed corrections [literature] (2009.03312).
3. Exponentially small corrections cannot give the linear-in-y εI₁ ramp [derived].
4. No one-loop log in the throat cutoff found; ε stays fitted [derived].
Touches: eps_tilt, band_i.

## D887: E.4 ε verdict
1. Target form |j−1728|^{2q}, q~1e-5, from D885 [derived].
2. No throat source at leading order [literature] (2009.03312, via D886).
3. Project closes negative; ε stays fitted; D841 rule unchanged [derived].
Touches: eps_tilt, band_i, serapis_e.

## D887: E.4 ε verdict
1. Target form |j−1728|^{2q}, q~1e-5, from D885 [derived].
2. No throat source at leading order [literature] (2009.03312, via D886).
3. Project closes negative; ε stays fitted; D841 rule unchanged [derived].
Touches: eps_tilt, band_i, serapis_e.

## D888: L.1 ρ lift reverse path
1. ε = 1.8e-3 (3.1e-4 to 1.1e-2) on S₂'s coupling [derived] (D883).
2. E₄ is the unique weight-4 form and E₄(ρ) = 0, so no holomorphic lift at fixed weight [derived].
3. Displacement needs |τ−ρ| ≈ 6e-4 but ρ is a fixed point, so zero without explicit breaking [derived].
4. Loops cannot lift a zero superpotential coupling [literature] (non-renormalisation theorem).
5. Instanton: Im T/N = 1.01 (0.72–1.29) [derived] (arithmetic).
6. Operator: Λ = 4.4e15 GeV (7.6e14 to 2.7e16) [derived] (arithmetic).
Touches: n_sector_rho, lepto_rho, mnu.

## D889: L.2 ρ lift literature (with D888a)
1. Residual Z₃ at ρ is exact for all U-modular-invariant terms, so the instanton and Kähler routes also vanish (corrects D888) [derived].
2. Entries scale as |u|^l, l = residual charge, with ε free in the literature [literature] (2102.07488).
3. Weight ≥ 3 polyharmonic Maass forms are holomorphic, so there is no non-holomorphic lift [literature] (2406.02527).
4. ε = 1.8e-3 ⇔ |τ−ρ| = 3.1e-3 (l = 1) [derived] (arithmetic).
5. No in-model source; ε at ρ is a post hoc residual-Z₃ breaking [derived].
Touches: n_sector_rho, lepto_rho, mnu.

## D890: L.4 ρ lift verdict
1. All U-modular-invariant contributions to the charged coupling vanish at ρ [derived] (D888a).
2. ε ≈ 1.8e-3 ⇔ |u| ≈ 2e-3 residual-Z₃ breaking [literature] (2102.07488, via D889).
3. Project closes negative; ε at ρ is post hoc, like ε at τ = i [derived].
Touches: n_sector_rho, lepto_rho, mnu.

## D891: W2.1 Weinberg selection rule at ρ
1. Light leptons share q_L = −q_{H_u}, so LH_u is Z₃-neutral [derived] (D778, D787).
2. Every Weinberg entry is then Z₃-neutral and generically non-zero at ρ [derived].
3. m_W = v_u²/Λ = 1.2e-5 eV (reduced M_P), 1e-3–5e-3 eV (M_s) [derived] (arithmetic).
4. Needed c ≲ 1e-3 (M_P) or ≲ 1e-5 (M_s); c = 1 at M_P gives AD yield ~1e-13 [derived] (arithmetic).
Touches: lepto_rho, n_sector_rho, mnu.

## D892: W2.2 Weinberg origin literature
1. Perturbative U(1)s conserve lepton number; Weinberg term instanton-only, C/𝓜 ~ e^{−S}/M_s [literature] (1112.5992).
2. M_m = x M_s e^{−2πVol/ℓ_s³g_s} [literature] (hep-th/0609191 eq. 2).
3. Bound needs S_W ≳ 9.5–14; heavy-ν instantons have S_N ≈ 6.4–12.6 [derived] (arithmetic).
4. Natural for M_N ≲ 1e12 GeV if S_W ≥ S_N [estimate].
Touches: lepto_rho, n_sector_rho, mnu.

## D893: W2.3 Weinberg verdict
1. Weinberg term allowed by Z₃ at ρ; bound c ≲ 1e-3 (M_P) or 1e-5 (M_s) [derived] (D891).
2. Instanton-only under perturbative lepton number [literature] (1112.5992, hep-th/0609191, via D892).
3. Bound met for M_N ≲ 1e12 GeV with S_W ≥ S_N [estimate].
Touches: lepto_rho, n_sector_rho, mnu.

## D894: R2.1 referee pass
1. τ = i AD (D646) gives m_ν₁ ≤ 9e-11 eV at T_R = 1e5 GeV [derived] (D646).
2. ρ AD (D880, FHY) gives m_ν₁ ≥ 4.4e-9 eV at T₂ = 1e5 GeV [literature] (hep-ph/0102187, via D880).
3. Ratio ≈ 49 in m_ν₁, ≈ 340 in yield [derived] (arithmetic).
4. Four text minors listed in REFEREE_v3.2_R2.md [derived].
Touches: lepto_rho, n_sector_rho, mnu.

## D895: R2.2a AD yield at ρ (with D880a)
1. Thermal effects negligible at H_osc ~ m_soft ~ 1e5–1e6 GeV [derived] (D653).
2. n_B/s = (8/23)T₂(2v_u²/m_ν₁)Q/(4M_P²), Q = 0.020–0.087 [derived] (D646, D646a).
3. m_ν₁ = 2.0e-11–8.9e-10 eV for T₂ = 1e5–1e6 GeV [derived] (locked run D895).
4. FHY extrapolation exceeds the no-thermal ceiling by 4 at D880's point [derived] (check K).
5. Lift target ε ≈ 1.6e-4; Weinberg bound c ≲ 1e-5 (M_P) / 1e-7 (M_s) [estimate].
Touches: lepto_rho, n_sector_rho, mnu.

## D896: R2.2b ρ lift recomputed
1. Same model and draws as D883; target m_ν₁ = 1.34e-10 eV from D895 [derived].
2. Pass fraction 3.50%; ε median 1.62e-4 (2.8e-5 to 1.0e-3) [derived] (locked run D896).
3. Window ends: ε = 6.3e-5 to 4.2e-4 [derived] (locked run D896).
4. |τ−ρ| ≈ √3·ε ≈ 2.8e-4 for l = 1 [derived] (arithmetic).
Touches: n_sector_rho, lepto_rho, mnu.

## D897: Weinberg numbers redone
1. Window m_ν₁ = 2e-11–9e-10 eV [derived] (D895).
2. c ≲ 1.7e-6–7.6e-5 (reduced M_P), 4e-9–9e-7 (M_s) [derived] (arithmetic).
3. S_W ≳ 13.9–19.3 vs S_N = 6.4–12.6 [derived] (arithmetic).
4. D892's natural claim withdrawn; shared M ≫ M_P condition with τ = i [derived] (D646a).
Touches: lepto_rho, n_sector_rho, mnu.

## D898: R2.2c text pass
1. Draft numbers replaced by D895–D897 values [derived] (D895, D896, D897).
2. Referee R2 minors 2–5 fixed [derived].
3. No new physics; frozen predictions unchanged [derived].
Touches: none.

## D899: R3.1 full referee pass
1. τ = i AD window quoted at T_R = 1e3–1e5 GeV [derived] (D646).
2. Corrected τ = i T_R ≈ (0.8–3)e6 GeV [derived] (D727, D815).
3. Same yield gives m_ν₁ ≈ 1.6e-10–2.7e-9 eV [derived] (arithmetic).
4. Three text minors (D690 stale, two superseded-route pointers) [derived].
Touches: lepto_i, mnu.

## D900: τ = i AD window at corrected T_R
1. Corrected τ = i T_R = (0.8–3)e6 GeV [derived] (D727, D815).
2. Same yield as D646/D646a [derived] (D646).
3. m_ν₁ = 1.6e-10–2.7e-9 eV; thermal check passes (φ/T ≥ 4.9e4) [derived] (locked run D900).
4. Overlap with ρ's window at 1.6e-10–9e-10 eV [derived] (D895).
Touches: lepto_i, mnu.

## D901: R3.2 text pass
1. Draft numbers updated to D900 [derived] (D900).
2. R3 minors fixed (D727 T_R; superseded-route pointers) [derived].
3. No new physics; frozen predictions unchanged [derived].
Touches: none.

## D902: DC.1 newest-data check
1. Σm_ν < 0.052 eV (zero prior), < 0.092 eV (hierarchy prior) [literature] (2606.17994).
2. ATLAS Run 2 disappearing tracks: 720 GeV at 1 ns [literature] (ATLAS briefing, 10 Mar 2026).
3. NO floor 0.0587 eV below one zero-prior bound, inside the physical-prior bound [derived].
Touches: mnu.

## D903: W3.1 Weinberg at τ = i
1. Singlet Weinberg (E₄η^{-2}) non-zero at i; Planck-size m ~ 1.8e-5 eV [derived] (D654a; arithmetic).
2. AD window needs S ≳ 13–17 (Λ = M_s) [derived] (arithmetic, D900 window).
3. Minimal texture m₁ ≈ 5e-5–4e-3 eV, far above the window [derived] (D786, D742).
4. AD at i conditional; inflaton-decay leptogenesis remains τ = i's route [derived] (D745).
Touches: lepto_i, mnu.

## D904: W4.1 lepton number and instanton actions
1. Anomalous U(1) may survive as an exact perturbative global symmetry [literature] (hep-ph/9908305).
2. E(-1) action S = 2π/g_s [literature] (standard D-instanton action).
3. g_s = 0.23–0.5 gives S = 12.6–27.1 [derived] (arithmetic).
4. Meets S ≳ 13–19 for g_s ≲ 0.33–0.48 [derived] (D897, D903).
Touches: lepto_rho, lepto_i, mnu.

## D905: per-branch conditions table
1. Table assembled from existing D-notes only [derived].
2. No new physics; frozen predictions unchanged [derived].
Touches: none.

## D906: ladder flag recheck
1. Fourteen flags traced to D887, D895, D897, D904a [derived].
2. D895 changed only m_ν₁; reheating chain T₂ unchanged [derived] (D781, D895).
3. All 14 nodes keep their statuses; no new work [derived].
Touches: none.

## D907: v3.2 readiness check
1. Build, references and citations checked by script [derived].
2. Locks verified by sha256 and commit order [derived].
3. Two mechanical gaps fixed; no substantive blocker [derived].
Touches: none.

## D908: v3.2 published
1. Published on Danny's explicit "Publish" [derived].
2. Uploaded files verified by md5 against the local build [derived].
Touches: none.

## D909: N1.1 protected light direction at τ = i
1. Non-zero at i iff Σk ≡ 0 mod 4 (trivial character) [derived] (D654a).
2. L₁SH_u with k_S ≡ 1 mod 4 vanishes at i [derived].
3. S's Majorana mass also vanishes (2k_S ≡ 2 mod 4) [derived] (D663).
4. A Dirac partner S′ (k_S + k_S′ ≡ 0 mod 4) restores the mass and keeps the protection [derived].
5. Cost: two extra fields plus a post hoc lift, as at ρ [derived] (D779, D888a).
Touches: lepto_i, mnu.

## D910: P3 literature tick (null)
1. Loop blow-up plateau 1 − c/φ^{2/3} is from a blow-up Kähler modulus [literature] (2604.07288, 2403.04831).
2. No modular power-law plateau source in 2026 literature found [literature] (2604.16281).
3. P3 unchanged [derived].
Touches: plateau_origin.

## D911: P3.L1 Eisenstein Kähler potentials
1. E_s in K with positivity windows [literature] (2510.19927).
2. e^K ∝ E^{−c} gives a 1/E plateau approach for c = 1 with an uplift [derived].
3. K = −log E(τ,2): 4y²g = −2 at ρ and i (ghost) [derived] (computed).
4. K = −k log 2y − c log E: ghost-free at ρ if k > 2c; plateau approach needs k + 2c = 2 [estimate].
5. No known string term −c log E(U,2) [literature] (BHK is additive).
Touches: plateau_origin, serapis_e.

## D912: P3.K1 Eisenstein-Kähler scan (with D911a)
1. Invariant V needs W ∝ η^{−2k}; e^G = (2y|η|⁴)^{−k}E^{−c} grows as e^{kπy/3} [derived] (D911a).
2. Positivity holds for k > 2c [derived] (locked run D912).
3. ρ is a maximum; no plateau for any w tested [derived] (locked run D912).
4. With k = 0 the metric has a ghost at the fixed points [derived] (D911).
5. P3.K route closed; P3 unchanged [derived].
Touches: plateau_origin, serapis_e.

## D913: reproducibility of the published v3.2 archive
1. 22 scripts run from a clean unpack of the published zip [derived].
2. 21 byte-identical, 1 identical up to wrapper timing lines [derived].
3. README gap (v3.2 rows) fixed in the repo [derived].
Touches: none.

## D914: T-brane uplift U-dependence
1. V_up = C_up/V^{8/3}, C_up ∝ g_s ∫|Ĝ|² [literature] (1512.04558 eq. 3.24).
2. U enters only via the flux norm, not analysed there [literature] (1512.04558).
3. Torus flux norm |m + nU|²/Im U is one lattice term, not E(U,2) [estimate].
4. P3 unchanged; both uplift carriers shape-blind for the E-ratio [derived] (D886).
Touches: plateau_origin.

## D915: audit M.1
1. Duality as residual gauge symmetry protected from explicit breaking (d = 1) [literature] (hep-th/9401139 §2.6.1).
2. W multilinear in T^i, 1/Im factors in the norm [literature] (hep-th/0303016 eqs. 3.8, 3.12, 4.19).
3. Per-factor |a + bU|²/Im U form inferred, not quoted [estimate].
Touches: none.

## D916: audit M.2 (with D657a)
1. Proton hexality is an anomaly-free non-R symmetry forbidding the dangerous operators [literature] (1102.3595).
2. Non-R Z_M cannot address the μ problem [literature] (1102.3595).
3. The modular centre cannot supply a Z₆; D656/D657 numbers stand [derived].
4. CMB-S4 support ended 10 July 2025 [literature] (Scientific American).
Touches: none.

## D917: audit M.3
1. Heterotic one-loop K has −δ_GS/8π² log(T + T̄) inside the dilaton log; η only in f [literature] (1009.3931 eq. 3.11).
2. D754's L-in-K lead unsupported as written [derived].
3. D760's pattern consistent [literature] (1009.3931, hep-th/0508043).
4. No published sentence affected [derived].
Touches: none.

## D918: audit M.4, audit closed
1. O3 types and flux parity [literature] (hep-th/0201029).
2. D752 conversion unused in the paper; stays an estimate [derived].
3. Audit summary: 1 published error (D657a), 1 lead weakened, 5 supported, 1 estimate [derived].
Touches: none.

## D919: letter novelty re-check
1. Uplifted α-attractors give n_s, r numerically, no running relation [literature] (2608.12819).
2. α_s given in model parameters, not eliminated [literature] (2602.01327).
3. Relation still not found; cite 2608.12819 as closest [derived].
Touches: none.

## D920: paper 1 published
1. Letter compiled from locked notes only [derived] (D640, D666, D669, D670, D671, D919).
2. Published with full metadata; md5 verified [derived].
Touches: none.

## D921: paper 2 published
1. Three no-go results compiled from locked notes only [derived] (D867, D912, D886, D914).
2. Published with full metadata; md5 verified [derived].
Touches: none.

## D922: paper 3 published
1. SERAPIS-E compiled from the published v3.2 section and locked notes [derived].
2. Published with full metadata; md5 verified [derived].
Touches: none.

## D923: paper 4 published
1. Methods note compiled from the public record; counts checked by script [derived].
2. Published with full metadata; md5 verified [derived].
Touches: none.

## D924: Zenodo record audit
- [derived] (md5 comparison) 12/12 posted files identical to local release files.
- [literature] none.
- Result: v3.2 page completed (68 refs, 19 keywords, related works to papers 1–4); all five records fully filled.

## D925: completion literature tick
- [literature] arXiv:2605.10197 (boundary complex-structure plateau, n_s ≈ 0.9643), arXiv:2604.19250 (pLVS fibre inflation).
- [derived] (arithmetic) 2605.10197 n_s is 3.1σ below SPA+DESI.
- Result: NULL for the SERAPIS completion.

## D926: completion tick 2
- [literature] arXiv:1412.5537: inflation near infinite-order special points only; no plateau, no LG points.
- [estimate] Lead: quintic-mirror LG (Z5) point plus LCS point as the CY analogue of fixed point plus cusp.
- Result: NULL for existing completion; lead recorded.

## D927: novelty check of the LG+LCS lead
- [literature] arXiv:1605.03974: conifold-to-orbifold multi-field inflation on the mirror quintic (2016).
- [literature] arXiv:2404.12422: W=0 vacua on symmetric loci, no inflation.
- Result: lead partly prior art; narrower pairing stays an unclaimed estimate.

## D928: LCS ray attractor index
- [derived] (sympy) K = −log t³ gives φ = √(3/2) ln t, p = k√(2/3), α = 1/k².
- [derived] (arithmetic) α = 1: n_s 0.960–0.967, r 3.3–4.8e-3 for N = 50–60; 2.3–4.7σ below SPA+DESI.
- [estimate] Power k of the leading correction assumed, not computed.
- Result: CY LCS analogue is a sibling (α = 1), not SERAPIS (α = 1/12).

## D929: p = 2√2 selects n = 1
- [derived] p = k√(2/n) for K = −n log y, V ≈ V₀(1 − c/y^k); SERAPIS needs k² = 4n.
- [derived] (arithmetic) integer k only for n = 1 (k = 2, the E(τ,2) power).
- Result: completion must keep a T²-type U modulus; open problem narrowed.

## D930: T²-factor completion search
- [literature] arXiv:2405.06738, 2505.01246: U fixed by fluxes first, volume inflates.
- Result: NULL; obstacle stated (SERAPIS needs one U left flat by the fluxes).

## D931: flux-flat U directions lead
- [literature] arXiv:2209.02720: tree-level flat directions in T⁶/Z₂ flux vacua, include S and U_i, lifted by loops/α′/instantons.
- [estimate] Could supply SERAPIS's unfixed U; checks pending (single U vs S–U ray; Re U free).
- Result: lead recorded.

## D932: flat directions are diagonal
- [literature] arXiv:2209.02720 toroidal section: all flat directions lock partners (one-flat ray includes the dilaton).
- [derived] SL(2,R)-invariant metric → n = 2 or 4 along the flat direction.
- [derived] (arithmetic) p = k√(2/n): only n = 4, k = 4 matches 2√2.
- [estimate] that ray sends g_s → 0, shrinking the BHK tilt.
- Result: D931 lead closed; no flux justification for single-U SERAPIS.

## D933: no identically flat single U
- [derived] ∂W/∂U₃ ≡ 0 ⇔ F, H ∝ dy³ ⇒ N_flux = 0 (enumeration: 0 nonzero wedges) ⇒ G = 0 for ISD flux.
- [derived] point-wise flatness: 16 real linear conditions on 16 flux integers; one determinant condition on P.
- [estimate] 5-parameter candidate family; integrality untested.
- Result: partial no-go; locked integer search queued.

## D934: flat single-U flux search (locked)
- [computed] nullity 0 at 512/512 grid points (run 2, DEVIATIONS D1 speed-only).
- [estimate] determinant may vanish nowhere; untested.
- Result: FAIL on grid; extended lock (ρ points + symbolic det) next.

## D935: F1 killed
- [computed] ρ grid nullity 0 (343 points); continuous min σ ratio 1.5e-3 at domain corners (> 1e-4 rule).
- [derived] with D933: no identically or point-wise flat single U in the sampled domain.
- Result: Project F switches to the sibling catalogue; candidate fourth no-go.

## D936: sibling catalogue (locked)
- [computed] n_s 0.960–0.967, α_s −(5.6–8.0)e-4 for all; r(N=55): 4.0e-3, 1.3e-3, 6.6e-4, 1.7e-4, 3.3e-4 for α = 1, 1/3, 1/6, 1/24, 1/12.
- [derived] all need a ramp for SPA+DESI n_s; D669 p listed per member.
- Result: catalogue recorded; Project F closed pending a new idea.

## D937: D929 log loophole
- [derived] k_eff = k − 1/ln y for a y^{−k} ln y approach.
- [derived] (arithmetic) n=3,k=4 needs y≈6.5 (drift 0.015); n=2,k=3 needs y≈340 (drift 0.002).
- [estimate] no source for such leading terms computed.
- Result: D929 holds only without tuning.

## D938: Weinberg instanton literature
- [literature] arXiv:1001.3148 (e^{−S} LHLH/M_s; M_s/e^{−S} ≈ 1e14 GeV for realistic ν masses); arXiv:2606.11346 (radiative, no instantons).
- [derived] (arithmetic) S ≳ 13–19 ↔ e^{−S} ≲ 2e-6–6e-9.
- Result: form confirmed; open part NULL.

## D939: v3.3 draft modulus paragraph
- [derived] summary of D928–D937 in the draft; no new numbers.
- [literature] 2209.02720, 1605.03974 added.
- Result: draft builds clean (18 pp).

## D940: P3 literature tick 2
- [literature] arXiv:1902.04625: level-N hauptmodul inflation, no plateau, no bounded ratio.
- Result: NULL; plan queue complete.

## D941: P3 as a heavy-field series combination
- [derived] (sympy) min_χ [Aχ² + B(1−χ)²] = AB/(A+B); A = μ²Ê, B = μ² gives P3.
- [derived] (sympy) m_χ²/H² = 6(A+B)²/(AB M²) ≥ 24/M².
- [literature] E(U,2) = T² lattice sum.
- [estimate] mass² ∝ E(U,2) from the KK tower, offset tuned; not computed.
- Result: P3 reformulated; novelty check and locked two-field check next.

## D942: D941 novelty check
- [literature] 1702.00420 (one-loop Pfaffians), 2508.11206 (KK tower potential): different uses; no Eisenstein-ratio plateau.
- Result: not found in this check; locked two-field check next.

## D943: two-field P3 check not completed
- [computed] run 1 invalid (normalisation 2/ξ vs 4/ξ; start near ρ).
- [derived] (sympy) dV₁/dÊ > 0 everywhere: no turnaround; D2's start rule inapplicable.
- Result: no observables; new lock D944 needed.

## D944: two-field P3 check (locked) PASS
- [computed] Δn_s = −4.7e-6/−1.8e-5, Δr/r = +0.01%/+0.05% for M = 0.1/0.2; m²/H² = 2.9e5/7.3e4; 1 − c_s² ≲ 4e-14.
- [derived] m²/H² ≈ 6Ê/M² on the plateau.
- Result: D941 realises P3 with no observable cost; mass source still assumed.

## D945: one-loop mass from T² images
- [literature] T² one-loop potentials are lattice sums; no E(U,2) mass for a plateau found.
- [derived] δm² = λ Σ′ G_D(|w|) = λ·2ζ(2s)E(U,s)/A^s·Γ(D/2−1)/(4π^{D/2}), s = (D−2)/2.
- [derived] D = 6 ⇒ s = 2 ⇒ p = 2√2; positive for boson loops.
- [estimate] offset at ρ is a one-number tuning.
- Result: H2 analytic pass; H3 tuning recorded; H4 open.

## D946: H4 ratio is free
- [derived] (sympy) general A = aÊ, B = b gives b·P3(λÊ; C/λ), λ = a/b exactly.
- [derived] λ ↔ field shift on the plateau; enters only via the vacuum mass.
- Result: H4 passes; P3 derived up to one tuned offset (H3) and model-building assumptions.

## D947: H3 offset = CC subtraction
- [derived] (sympy) V_min(E) − V_min(E_ρ) = N·P3(λ′Ê), λ′ = λ/(λE_ρ+1), exact.
- [derived] ramp leftover absorbed into C; residual O(1e-6).
- Result: Project H closes positive analytically; P3 derived up to model-building assumptions.

## D948: D941/D945 vs earlier no-gos
- [derived] (sympy) E-term share of V_min is 1/(λÊ+1) ≈ 1e-3–1e-4, not D709's 50%.
- [derived] no tension competition, so D712/D703's sign wall does not apply.
- [estimate] new assumptions: tree mass of χ accidentally small (loop ≫ tree); area stabilised with m_A ≫ H.
- Result: Project H's close stands with two added conditions.

## D949: v3.3 draft Project H caveat
- [derived] summary of D941–D948; no new numbers.
- Result: draft builds clean, 18 pp.

## D950: Project H needs a non-SUSY tower
- [literature] 0805.1874: SUSY orbifold N=2 sectors give log(T₂U₂|η|⁴) Kähler corrections, no masses.
- [derived] soft breaking: m_soft² ∂G/∂m² ∝ L^{−(D−4)} → s = 1 for D = 6 → p = √2, α = 1/3.
- [estimate] Scherk–Schwarz on the same T² conflicts with low m_{3/2}; a sequestered non-BPS sector remains.
- Result: Project H stands with a stricter requirement; draft updated.

## D951: brane SUSY breaking class
- [literature] hep-th/0601158: BSB keeps bulk SUSY at tree level; T² Wilson-line one-loop masses take both signs (14/16 saddles).
- [estimate] Project H needs n_B > n_F among χ's partners and T² ≫ l_s.
- Result: realisation class named; sign is a condition, not a guarantee.

## D952: Project H scale window
- [derived] δm² = 0.01745 g E M_s²/A₁² (λ₆ = g/M_s²).
- [derived] (arithmetic) 17g–175g ≲ A₁ ≲ 2.6e6–6.6e7.
- [estimate] benchmark small T⁴ fits D945a.
- Result: no scale conflict; toolkit with 11/11 self-checks added.

## D953: independent reproduction of SERAPIS-E
- [computed] new MS code, paper convention: n_s 0.9700–0.9746, r (4.55–5.12)e-4; C = 0: 0.9612, 3.64e-4 — matches v3.2.
- [computed] α_s −(8.2–11.5)e-4, one corner outside ±10% → locked FAIL; [estimate] new-code α_s noise ~1.5e-4.
- Result: n_s, r confirmed; α_s not confirmed (tool limitation).

## D954: α_s reproduction (locked) PASS
- [computed] α_s −(8.5–11.1)e-4 vs published −(9.4–10.6)e-4; relation −(9.1–10.2)e-4.
- [estimate] residual solver scatter ~1e-4.
- Result: SERAPIS-E n_s, r, α_s independently reproduced (α_s to ~10%).

## D955: Sugimoto spectrum sign check
- [literature] 1711.11494: USp(32) bosons, fermions in antisymmetric 495 + singlet goldstino.
- [derived] (arithmetic) 528 − 496 = +32 bosonic excess.
- [estimate] Project H sign condition met at the massless level; massive levels and couplings unchecked.

## D956: vacuum-mass shift of N* (Project H)
- [derived] λ′ < 1/E_ρ = 0.173; m_φ² ∝ λ′.
- [estimate] Γ ∝ m³ ⇒ ΔN* = ¼ ln λ′ = −0.44 to −1.15; Δn_s ≈ −(3.5–9.2)e-4.
- Result: tolerable (<1e-3) for λ′ ≳ 0.01, but a real downward shift; locked exact check needed before any claim.

## D957: Sugimoto massive levels
- [literature] 1711.11494: only the V₈ sign in the Möbius amplitude differs from SO(32).
- [derived] n_B − n_F = ε_l 𝒩 d_l per level; +32 at the massless level.
- [literature, unverified here] ε_l = (−1)^l from hatted characters.
- [estimate] massive levels suppressed for A₁ ≳ 20; sign condition holds there.

## D958: α_s Bunch–Davies start artifact
- [computed] α_s −1.035e-3 (bd 200) vs −0.902e-3 (bd 1000); n_s identical.
- [estimate] mechanism: residual negative-frequency oscillation ~2/bd².
- Result: published α_s may carry ~10% bias; locked convergence test queued.

## D959: Chronos/Kairos reproduction (locked) PASS
- [computed] Chronos n_s 0.9696–0.9752, r 4.86–5.77e-4, y* 23.2–24.3; Kairos n_s 0.9586–0.9611, r 3.28–3.70e-4 — match v3.2.
- Result: main-branch n_s, r, y* independently reproduced; α_s to ~10%.

## D960: Möbius phase verified
- [literature] hep-th/0503204 eq. 1.83: hatted characters carry (−1)^k per level.
- Result: D957's flagged step sourced; Project H sign condition sourced.

## D961: ADS anti-D5 embedding for Project H
- [literature] hep-th/9908023: T⁴/Z₂, 32 anti-D5, SUSY broken only on them, tachyon-free.
- [derived] (arithmetic) 5̄5̄ massless: 2112 boson vs 1984 fermion d.o.f., excess +128.
- [estimate] 6D anti-D5 worldvolume on R⁴ × T² matches D945a; χ coupling and stabilisation open.

## D962: SERAPIS-ρ reproduction; map links
- [computed] ρ n_s 0.96909/0.97224, r 5.160/4.672e-4 match D816 exactly; α_s −13.6%/+8% (locked FAIL, D958 artifact).
- Result: n_s, r independently reproduced on all three branches; α_s pending D960.

## D963: correction: BSB scalar mass sign
- [literature] hep-ph/0004091: Wilson-line scalar one-loop mass² negative in the anti-D5 sector.
- [derived] sign depends on the coupling (quartic tadpole vs mass shift), not only on n_B − n_F.
- Result: D955/D957/D961 sign verdicts withdrawn; Project H sign condition open.

## D964: negative-mass branch of Project H
- [derived] (sympy) A = −aE: stable only for aE < B; V_min/B = X/(X−1) → −∞ as X → 1.
- Result: Project H needs the positive sign strictly; D963's question is decisive.

## D965: gauge-loop sign positive
- [literature] hep-ph/9810410 eq. 3.14: brane scalars from bulk gauge towers, m² > 0, finite.
- [derived] (mpmath) Δm²(0) − Δm²(½) = (7/4)ζ(3) = 2.1036 (checked).
- Result: gauge → +, Yukawa → −, Wilson line → −; Project H needs a gauge-charged localised χ.

## D966: T² gauge-loop mass structure
- [derived] (mpmath) ADPQ's Li₃ difference = circle image sum, 2.103599581 = (7/4)ζ(3).
- [derived] T²: bosonic windings Σ′|w|⁻⁴ = 2ζ(4)E(U,2)/A²; no light gauginos in ADS 5̄5̄ → positive.
- [estimate] loop normalisation c₆, massive levels not computed.
- Result: Project H sign condition met in structure.

## D967: gauge-invariant pinning
- [derived] charged χ forbids the −2Bχ tadpole.
- [derived] (sympy) D-term: flat top at finite Ê, not P3; mixing B|χ−φ₀|²: P3 exactly, breaks the gauge group.
- [estimate] need gφ₀ ≪ T² KK scale to keep E(U,2).
- Result: new condition on Project H.

## D968: gauge-mass correction to the E(U,2) mass
- [derived] (mpmath-checked) G₆(L;m) ≈ G₆(L;0)[1 − (mL)²/4].
- [derived] correction = weight-1 sum −(m_V²/4A)E_reg(U,1).
- [estimate] need g φ₀ ≲ 0.1 M_KK to keep the p = 2√2 approach to ~1%.

## D969: ADS ND doublets as (χ, φ₀)
- [literature] hep-th/9908023: ND scalar doublets in (16,1,1,16)+(1,16,16,1); no potential/vevs/masses; ND annulus vanishes.
- [estimate] same-rep pair available; doublet symmetry vs mixing open; ND scalar mass uncomputed.
- Result: ingredients present; Project H's top open item is the one-loop ND-scalar mass.

## D970: Project H loop coefficient
- [derived] (mpmath) 5D calibration against ADPQ: κ = 4C = (D−1)C exactly.
- [estimate] 6D, κ = 5C: m_χ² = (5ζ(4)/2π³) g²C E(U,2)/A = 0.0873 g²C E(U,2)/A.
- Result: explicit coefficient; open items unchanged.

## D971: correction to D970's coefficient
- [literature] hep-th/0502093: 6D brane-scalar mass from bulk gauge KK modes, positive, finite.
- [derived] (Poisson resummation, numeric check) Lee = (2ζ(4)/π³) g²Q² E/A exactly (ratio 1.0000); D970's 5ζ(4)/2π³ was 1.25× too large.
- Result: c₆ = 0.0698; κ = 4C in 5D and 6D; finiteness needs bulk-like breaking on the T².

## D972: Project H null observables
- [derived] (arithmetic) m/H = 108–539 → e^{−πm/H} = 10^{−147}–10^{−735}; 1 − c_s² ≲ 1e-12 (D944).
- Result: no collider/sound-speed signature; only the N* shift distinguishes Project H.

## D973: Project H selects ρ
- [computed] E(U,2) Hessian: saddle at i (−6.85, +30.96), isotropic minimum at ρ (11.57, 11.57).
- Result: Project H applies to the ρ/E branch only; τ = i plateau stays postulated.

## D974: α_s convergence (locked) NOT CONVERGED
- [computed] bd 200/1000/5000: SERAPIS-E α_s −10.35/−9.02/−9.34 e-4; Chronos −8.69/−9.35/−9.75 e-4; n_s, r converged.
- Result: published α_s consistent at ~5%; new method (exact dS start) needs a new lock.

## D975: Project H implies a smaller physical tilt coefficient
- [derived] C = λ′C₀ ≤ 2.0e-7; Im S Im T ≥ 4904 (vs 750–975).
- Result: Project H version of SERAPIS-E needs ~6× larger Im S Im T; D961's fixed-C rows test the stronger-ramp regime; refit-C version needs a new lock.

## D976: correction to D956
- [derived] Γ ∝ m (D722 channel) ⇒ ΔN* = (1/12) ln λ′ = −0.146 at λ′ = 0.173; Δn_s ≈ −1.2e-4 (D956 overstated by 3×).

## D977: Project H refit-C (locked) FAIL
- [computed] λ′ = 0.173: Δn_s = −2.69e-3, Δr/r = +8.5% at ΔN* = −0.06 (C = λ′C₀).
- [derived] λ′Ê is not a pure field shift of Ê beyond the y² term.
- Result: Project H gives a sibling of SERAPIS-E (n_s ≈ 0.9714, r ≈ 5.0e-4), still inside the frozen band.

## D978: Project H fixed-C (locked) — too few e-folds
- [computed] λ′ = 0.173, C fixed: Ntot = 40.6 < 58.5; scenario excluded; refit-C (D977) is the consistent one.

## D979: N* reproduction (locked D958) — FAIL by constant +0.171, traced
- [computed] Exact N* = 46.46–51.04 for T_R = 1e4–1e10 GeV, vs D719 +0.17 at every T_R.
- [derived] (arithmetic) ΔN* = (1/3) ln(V*/V_end exact 2.267 / slow-roll 1.357) = 0.171; diagnostic reproduces it to ±0.004.
- Result: D719's N* bracket is 0.17 low (slow-roll end of inflation); Δn_s ≈ +1.5e-4, inside the frozen band.

## D980: α_s de Sitter start (locked D975) — NOT CONVERGED
- [computed] α_s scatter 21% (SERAPIS-E), 12% (Chronos) across bd = 200/1000/5000; n_s, r converged to ≤3e-6.
- [derived] Start transient removed but scatter remains → not a start effect (D974's estimate not supported).
- [estimate] Readout noise ~1e-6 in ln P amplified by the ±0.1 stencil; next: wide-grid quadratic fit (new lock).

## D981: prep of five open nodes
- [literature] 1105.0591: brane adjoint one-loop mass matrix traceless → tachyonic direction (sign warning for Project H).
- [literature] 2311.05824: Boltzmann system for inflaton-decay leptogenesis; locked check PREREG_D982 queued.
- ε origin and halo profile: no new calculable input.

## D982: second prep pass
- [literature] 0805.0824: brane-scalar mass² sign tracks the one-loop vacuum amplitude; [estimate] bosonic-excess sector → positive χ mass (Project H's need).
- [literature] 2605.16994: Gaia DR3 prefers Einasto/cored halos → halo node literature.
- [literature] 1707.07059: no U-dependence of the anti-D3 uplift at leading order.

## D983: third prep pass
- [derived] (structure) brane scalar with positive quartics: δm² ∝ +(N_B−N_F)E(U,2)/A², V ∝ −(N_B−N_F)·(weight s+1): bosonic excess → V<0, m²>0 (Kitazawa's opposite-sign rule in field theory; holds for ADS +128).
- D982 OOM crash → DEVIATIONS D1, rerun D982b.

## D984: Project H n_s-matched (locked D979, PC)
- [computed] C = 1.238 λ′C₀ restores n_s = 0.97403; r = 5.331e-4 vs 4.607e-4 (+15.7%).
- [estimate] Δr ≈ 7e-5 needs σ(r) ≲ 2.4e-5 for 3σ: beyond funded missions; locked "LiteBIRD-class" label overstates feasibility.

## D985: Level S3 (locked D985) PASS
- [computed] anti-D5 position scalar, Möbius amplitude with full tower: m² > 0 at all 9 grid points; shape = E(U,2)/A² to 1.1% (L=10), 0.02% (L=16); two routes agree to ~1e-5.
- Project H's decisive sign condition (D964) met at string level in the ADS sector; other conditions remain.

## D986: leptogenesis Boltzmann (locked D982)
- [computed] κ = 0.9391 on all rows: instantaneous yields stand (×0.94); c = 0.3, M_H = 1e12 fails by ×1.22.

## D987: S3b positivity (locked D986) — SIGN CHANGE
- [computed] Ĥ(t) oscillates in sign for t ≲ 0.027 (|Ĥ| ~ e^{π²/2t}), positive for t ≥ 0.03.
- D985 (large T², heavy T⁴ windings) unaffected; all-radius positivity fails; small-R needs the transverse channel.

## D988: Project H local χ mass
- [derived] winding-zero term = local, string-scale, tadpole-dominated (D987 region); [estimate] exceeds the E(U,2) part by ~A ≳ 100.
- [derived] positive A₀ → absorbed into λ′ (needs larger Im S Im T); negative A₀ → fatal (D964). Sign needs dilaton backreaction.

## D989: Janus calculator battery A (locked D990) VALIDATED
- [computed] 24/24 SERAPIS points: |Δn_s| ≤ 2.4e-5, |Δr/r| ≤ 0.013%; stress set inside envelope; ~4e4× faster.

## D991: ρ tilt origin (estimate)
- [derived] εL has the weight-1 soft-threshold form (D950). [estimate] Hubble-induced soft masses: ε ≈ N c² M_KK²/(48π² M_P²) = 4.6e-6 (N=128, c=1, M_KK=1e16); fitted 6e-5 needs M_KK ≈ 3.6e16 or c ≈ 3.6.

## D991a: correction to D991
- [derived+computed] soft-split vacuum energy is weight 2 (E(U,2)), verified to 1e-4 on 5 tori; the log is the m_s⁴ term. D991 withdrawn; ρ tilt origin open.

## D993: eternal inflation + swampland (EZ1)
- [computed] tilted branches max P_R ≈ 1.6–2× A_s → non-eternal; Kairos 0.13 in range (eternal further up). [derived] the tilt ramp makes ε_V → 4 (E) or 1 (Chronos/ρ) asymptotically.
- Scorecard: dS and TCC violated (plateau-generic); Δφ ≈ 1.8 M_P.

## D994: Janus J3 third order (locked PREREG_J3) IMPROVED
- [computed] n_s median error 1.7e-5 → 1.6e-6 (max 2.9e-6) on 24 points; β_s ≈ −3e-5.

## D995: Janus J2/J4/J5 (locked PREREG_J4) VALIDATED
- [computed] N* exact to 1e-3, n_s within error bar, 5 T_R.

## D996: S4a Dudas-Mourad 9D reproduced
- [computed] symbolic residuals 0; numerical 1e-10; first lock NOT VALIDATED (FD floor), second (symbolic) VALIDATED.

## D997: Janus-LT L0a VALIDATED
- [computed] H 5e-11, D_M 3e-6 vs CAMB, 50 cosmologies.

## D999: Janus J6 two-field δN NOT VALIDATED as locked
- [computed] T2–T4 pass (VW analytic f_NL to 0.6 %); T1 r off 1.2 % = second-order term (1 + Cε₂) missing from lowest-order δN; J6b planned.

## D1000: Janus J6b NLO δN r VALIDATED; two-field module
- [computed] r_NLO vs calculator 9e-5; equal-mass angle-independent; twofield.observe_multi added.

## D1001: Janus large-f_NL δN VALIDATED on slow-roll slices (J6d); J6c at ε=1 NOT VALIDATED
- [computed] f_NL −0.26…−81 vs Byrnes–Choi–Hall Eq. 21 within 0.4–6 % on 9 slices; transient f_NL decays by ε_H = 1.

## D1002: Janus vs real ASPIC (J7a): n_s ~200×, r ~330× more accurate vs exact MS on 14 points; α_s comparison uninformative
- [computed] medians dn_s 3.8e-6 vs 7.7e-4; dr/r 7.5e-5 vs 2.5e-2; ASPIC 0.1 µs/pt, Janus 1.2 ms/pt any V.

## D1003: Battery B (D989) VALIDATED 8/8, α_s ≤ 0.3 %; D981c replicates the α_s convergence verdict
- [computed] Janus α_s vs exact solver ≤ 0.30 % at ~1.5e5× speed; independent PC rerun matches the other session to 2e-6.

## D1004: Janus vs ASPIC on 17 models (J7b): n_s ~350×, r ~320×, α_s ~50× more accurate vs exact MS
- [computed] 32/32 points Janus better on n_s; α_s reference convergence-checked (R0).

## D1006: Janus-LT L0b r_d integral VALIDATED (1.9e-6 vs CAMB); EH98 z_d fit off 3.7 % (definition mismatch)
- [computed] needs own recombination for z_d (L0b2).

## D1007: track R candidate — gaugino-condensation potential carries e^{3L} at leading order; linearised gives the ρ tilt εL (not yet computed)
- [literature] 1812.06520 Eqs. 2.7, 4.1, 4.2; [derived] (Im T|η|⁴)^{-3} = 8e^{3L}.

## D1007a: correction — e^{3L} gaugino-condensation source fails as an εL tilt on the inflaton (ΔL ≈ 19 over 50 e-folds)
- [computed] L(y) along SERAPIS-ρ: 24.0 (N=60) → 2.5 (N=1); linearisation valid only over ≲ 0.1 e-fold.

## D1008: Janus vs ASPIC reheating route (J7c2): n_s ~260×, r ~260×, α_s ~35× more accurate; ASPIC pivot off 0.16 e-fold
- [computed] 32/32; J7c VOID (lock slip ½ ln H*) kept on record.

## D1009: track R — Green–Schwarz Kähler term −ln(2ReS − δ_GS L) gives +εL with ε = δ_GS/(2ReS); curvature ≤ 2e-6
- [literature] 2212.03876 Eq. 2.21; [derived] linear over the inflationary range; needs Re S ~ δ_GS·8e3.

## D1010: R1 — Green–Schwarz multiplicative tilt κ = ε reproduces SERAPIS-ρ (Δn_s ≤ 5e-5); A(S,S̄) factor next
- [computed] κ*/ε = 0.996.

## D1011: R2 — GS term with full Kähler structure keeps the tilt linear in L (kinetic change 4e-5 const; Ã depends on T only via Y)
- [computed] sympy identities K1, K2, K4; K3 numbers.

## D1012: Janus-LT L0b2 own recombination VALIDATED — z_d 6.7e-4, r_d 4.4e-4 vs CAMB (50/50)
- [computed] minimal RECFAST, 2.5 s/cosmology.

## D1013: D984 wide-grid α_s — SERAPIS-ρ −9.863e-4 / −8.694e-4 converged, published stands; Kairos 0.93×(−2/N²)
- [computed] PC run; Janus agrees to 0.16 %.

## D1014: S4b(a) γ_D = (D+2)/√(8(D−2)) verified (k = 4/(D−2)); γ₆ = √2, γ₁₀ = 3/2
- [computed] sympy Christoffel-level check, D = 4, 6, 10.

## D1015: S4b(b) — 6D tadpole subcritical (γ_o = 2 < √5): trigonometric vacuum on a finite interval, two routes agree (≤ 4e-11)
- [literature] 2209.10553 Eqs. 3.1–3.17; [computed] analytic residual 2e-36, numeric 3e-12.

## D1016: R3 — single condensate flips the GS tilt sign at weak coupling (R → −1); need δ_GS < 0 or racetrack
- [derived] R = (v − 2 − a²Y²)/(a²Y² + 2aY + v − 2).

## D1017: R4 — at a SUSY dilaton minimum (F_S = 0) the GS tilt is exactly the e^K one (R = 1) for any Ω(S)
- [derived] stationarity: d ln(Ω²/Y)/ds = 2F_S/Ω; [computed] racetrack point R = 1.0000.

## D1018: J7d two-parameter models — Janus n_s ~360×, r ~540×, α_s ~40× better than ASPIC (8/8); PSNI start-finder failure listed
- [computed] TI, SFI; J1b bisection start-finder needed.

## D1019: Janus-LT L0c massive ν VALIDATED (H, D_M ≤ 4.6e-5 vs CAMB, 150 cases)
- [computed] Komatsu 2011 Eq. 25 by quadrature.

## D1020: J7d2 — PSNI unscored: Janus background integrator stalls at the log-singular end (J1c fix path)
- [computed] bisection added; N_tot = ∞ for all starts.

## D1021: R5 — realistic heterotic δ_GS (−9…−24), Re S ≈ 2 ⇒ GS tilt 0.03–0.08, ~500–1300× too large (normalisation to confirm)
- [literature] hep-ph/0209061; [estimate] ε = |δ_GS|/(16π² Re S).

## D1022: J1c — Radau fallback does not rescue PSNI; diagnose trajectory next (J1d)
- [computed] guard PASS; PSNI unscored.

## D1023: J1d — PSNI scored with a field-value end (exact ε_H never reaches 1 before the singularity); Janus n_s ~1000× better
- [computed] end_y option added; 42/42 fixed-N* points Janus better.

## D1024: R6 — GS coefficient C/8π² = 0.380 (E₈), sign OK; ε = 6e-5 needs Re S ≈ 3200 (cf. D975 Im S Im T ≳ 4900)
- [literature] hep-th/9202059 Eqs. 1.1, 1.4, 3.9, 3.13, 4.15, 4.19.

## D1025: L1 — TorsionΛ D715 audit with first-principles Janus-LT: (b) R +6.8σ, l_A −186σ; D715 verdict strengthened
- [computed] V vs CAMB ΛCDM: z* 5e-4, l_A 3.4e-4.

## D1015a: correction — the 6D vacuum is 5D Minkowski × interval (not 4D)
## D1026: S4c KK probe NOT VALID (ill-conditioned FD eigenproblem at singular ends); Liouville/shooting next

## D1027: Janus-LT L2 growth VALIDATED — σ8 ratio 4e-6, f 6e-5 vs CAMB (20 cosmologies)
- [computed] scale-independent growth ODE (2602.08207 Eq. 5).

## D1028: Janus-LT L3 DESI DR2 BAO likelihood reproduces DESI ΛCDM (Ω_m 0.2970 vs 0.2975; h r_d 101.56 vs 101.54); TorsionΛ (b) χ² 123/13
- [computed] Table IV, 13 points.

## D1029: L4 — Janus-LT w0wa (BAO + compressed CMB): w0 −0.455±0.22, wa −1.62±0.65 matches DESI+CMB; Δχ² −8.0 vs −12.5 → locked INCONSISTENT on Δχ²
- [computed] 242 s, own recombination.

## D1030: R7 — heterotic M-theory gives no ~10³ hidden/visible coupling asymmetry in its controlled regime (1811.08892)

## D1031: R8 — L = finite part of E(τ, s → 1) (Kronecker): E = π/(s−1) + πL + 2πγ − π ln 2 + O(s−1)

## D1032: L5 — SERAPIS ΛCDM + Σm_ν 0.0587 eV: Δχ² = 2.37 vs Σm_ν = 0 (BAO + compressed CMB); consistency check only

## D1033: S4c2 — Prüfer KK probe validated on flat interval; 6D zero mode + positive tower, m₁² 0.82→0.78 not yet converged (locked NOT VALID)

## D1034: J8 — ASPIC (w, ρ_reh) route: Janus n_s ~230×, r ~230×, α_s ~35× better (32/32); ASPIC pivot 0.22 e-fold off
## D1035: J7f pulse 1 — 32 ASPIC models at once: Janus n_s better 64/64 (median ~560×), r ~430×; DI outlier; 10 listed
## D1036: S4c3 — 6D KK masses converged (Aitken, q≈0.84): m1² 0.778184, m2/m1 1.780, m3/m1 2.546; VALID
## D1037: correction to D1035 — kmii is an ASPIC failure, not my parser; my bugs among listed = 3 (gmlfi, ncli, fi)
## D1038: S4c3 convergence order derived: q = (D−2)/((D−1)(1+δ)) = 0.8446 vs measured 0.8442; p ~ u exactly at y=0
## D1039: J9 — Janus β_s vs exact MS: 6/6 within 1–4% (reference noise ≤ 7%) → VALIDATED at ~5%
## D1040: R track — BHK IIB one-loop Kähler term is E₂ (s=2), not s=1 → cannot give the GS-type log tilt; lead closed; next: DKL thresholds
## D1041: L6 — Janus-LT Pantheon+ SN-only Ω_m = 0.3315 ± 0.018 vs published 0.334 ± 0.018 → REPRODUCED
## D1042: L7 — joint BAO+CMB+Pantheon+ w0wa: w0 −0.853 ± 0.053, wa −0.518 ± 0.200 vs DESI −0.838/−0.62 → CONSISTENT; Δχ² −7.7
## D1043: R — hidden condensate gives an L-term ∝ (δ_GS/16π² + b_a): tilt size is a difference of two O(1e-2) terms; 6e-5 needs ~0.5% cancellation [estimate]
## D1044: correction to D1043 — condensate η-exponent is absorbed by the dilaton shift S'=S+δ ln η² (LRW 2212.03876 Eqs. 2.12–2.21): no free cancellation; size problem stands
## D1045: R5 — with the consistent S'-frame tilt variable ln(2 Im T) no κ reproduces SERAPIS-ρ n_s → FAILS; D1010/D1017 used an inconsistent K/W pair
## D1046: R5b — fine κ scan: only crossing κ*=−9.7e-3 sits at the breakdown edge with r ×4 → ℓ-tilt FAILS CONFIRMED; GS route closed unless S (not S') is stabilised
## D1047: L8 — distance priors fit exactly (χ²=0) but the lock was degenerate (3 params/3 data); informative part: implied h 0.675–0.676, Ω_m 0.3155; own z* 1090.30
## D1048: R — BGW (hep-th/9605170): GS term cancels all T-dependence at fixed ℓ; with D1044–D1046 the GS route for the ρ tilt is CLOSED
## D1049: R lead — AGNT Eq. 20: matter wave function Y_j = 2γ̃_j ln[|η|⁴(T+T̄)] with N=2 coefficient (not GS) → candidate non-GS source of the ρ tilt
## D1050: L8b — CHW priors + DESI BAO ΛCDM: χ² 14.05/13, h 0.6864 vs 0.6842 (L4) → ROBUST to CMB compression
## D1051: R — AGNT matter-log tilt κ = 2g²γ̃; natural size 1.6e-3–1.6e-2 (30–300× too big); ε needs near-finite N=2 sector (γ̃ ≈ 0) [estimate]
## D1065: L9a — EH98 no-wiggle T(k) vs CAMB: rms 1.3–1.4%, max ≤ 4.0% (BAO wiggles) → VALIDATED
## D1127: J7g pulses 2–3 — 31 models × 2 reheating routes: Janus n_s better 124/124 (~390×); ASPIC pivot off 0.16–0.33 e-folds; with J7f, 188/188
## D1130: L9 — Janus-LT fσ8 reproduces DESI fiducial to 0.16%; L8b ΛCDM vs DR1 full-shape χ² 3.81/6 → CONSISTENT (σ8 amplitude from CAMB, stated)
## D1132: L9b — own σ8 ratio to CAMB 0.902–0.917 (constant ~9% low) → NOT VALIDATED; points at D normalisation with radiation at a=1e-3
## D1133: L9c — own σ8 (A_s → P(k), EH98, MD-normalised D) vs CAMB: +1.0–1.4% → VALIDATED; confirms D1132's diagnosis
## D1134: L9v2 — fσ8 with own σ8: χ² 3.81/6 (unchanged) → CONSISTENT; Janus-LT growth chain self-contained
## D1135: R — Z6-II-b abelian N=2 sector: b̃_U(1) = 0 exactly (hep-th/0001062, after Eqs. 50–51) → small γ̃ = small correction to an exact zero
## D1137: R — Wilson lines (hep-th/0001062 Eqs. 29–51) don't lift the Z6-II-b U(1) zero; U(1) instead gets log(ω(T)−ω(U)), not L. Line paused.
## D1138: S4d prep — BMS 1811.11448: DM tadpole vacua (9D × interval) perturbatively stable in all sectors; template + expectation for our 6D S4d
## D1140: S4d — subcritical 6D vacuum scalar sector: A′/P′ ∈ [−0.2236, +0.2236] ≥ −1/4 → b ≥ 0 → STABLE (BTR 2209.10553 Eq. 5.10)
## D1141: S4e — Dirichlet m L/π 0.932, 2.040 vs BTR 0.97, 2.13 (−4%) → NOT VALIDATED; ratio m₂/m₁ 2.190 vs 2.196 matches
## D1146: J9b (PC) — β_s 24/32 informative, median err 3.1%, max 10.6% → VALIDATED; steep LFI p=3,4 show resolved −6 to −10% truncation systematic
## D1148: J10 (PC) — 48 new-pivot points: medians dns 1.7e-6, dr/r 7.6e-5, das 4.5e-7 → accuracy holds at N* 45/55/65
## D1149: J11 (PC) — β_s rel. error ∝ ε* (slope 1.14, ≈5ε*) → third-order truncation confirmed; ≤5% for ε* ≲ 0.01
## D1160: toolkits — KALUZA v0.1 REGRESSION PASS (4/4), LOCKBENCH v0.1 (ledger flagged D1039 precision), MultiModeCode built/running for JANUS-MF
## D1161: JMF1 — two-field δN vs MultiModeCode: r ≤ 2e-4 vs exact; n_s δN error 1.3e-4/7.6e-4/1.7e-3 for R=1/3/9; C1 FAILS (mismatched δN definitions)
## D1162: JMF2 — Janus-MF exact multi-field MS vs MultiModeCode: |Δn_s| ≤ 6.3e-6, r ≤ 1.2e-4, α_s ≤ 0.6% → VALIDATED; δN error at R=9 1.7e-3 → 4.7e-6
## D1163: LOCKBENCH L-1 — machine-readable claims + evaluator, tests PASS
## D1164: LOCKBENCH L-2 — lock linter; flags L8, D1039, JMF1, J7h patterns; clean lock passes
## D1165: LOCKBENCH L-4 — provenance stamps (sha256 of results/lock/code/data, versions, machine); tests PASS
## D1166: JMF3 — Janus-MF matches MultiModeCode on quartic and axion 2-field models (|Δn_s| ≤ 2.4e-6, r ≤ 4e-5); VALIDATED
## D1167: LOCKBENCH L-3 — blind mode (seal until the D-note states the verdict); tests PASS
## D1168: J7h — 3 more ASPIC models scored on the PC; pulses now 206/206 Janus better; 3 listed (ASPIC timeouts, wall limit)
## D1169: JMF4 non-separable NOT VALIDATED vs MMC; JMF4b shows the gap is MMC's inconsistent derivative code (cases 8, 11, 12)
## D1171: LOCKBENCH L-5 verification kit (GCI/order/MMS); KALUZA FD operator verified 2nd order on an exact case
## D1172: LOCKBENCH L-6 — deviation command + rerun guard in pcjob; tests PASS
## D1174: JMF5 — with MMC's derivative code fixed, Janus-MF matches on both non-separable models (|Δn_s| ≤ 9.4e-6)
## D1175: LOCKBENCH L-8 — ENV.lock pin + selftest (8/8 PASS on cloud)
## D1176: J13 — Janus accuracy holds at N* 45/55/65 on 32 ASPIC models (96 pts; median dns 1.4e-6)
## D1177: LOCKBENCH L-7 — results ledger dashboard (D1160–D1176 verdicts + CubeMind arms); LOCKBENCH L-1…L-8 complete
## D1195: JMF6 — Janus-MF matches PyTransport (independent, symbolic V) on 3 quadratic + 2 non-separable models, |Δn_s| ≤ 9.3e-5; VALIDATED
## D1200: L10 — w0–wa profile likelihood matches L7 (min 1 step from MAP, ΔχΛCDM 7.69 vs 7.70); DESI best fit inside 68%
## D1205: L11 — Cobaya MCMC on L7's likelihood: w0 −0.842±0.053, wa −0.565±0.213 vs L7 −0.853±0.053, −0.518±0.200 → CONFIRMED
## D1206: JMF7 — P_R frozen by ε=1 in Q9, N2', N1 (last-e-fold change ≤ 4.5e-9) → multi-field results final
## D1207: JMF8 — Janus-MF matches PyTransport for 3 fields (separable and coupled), |Δn_s| ≤ 8.9e-5; VALIDATED
## D1213: L12 — adding DESI DR1 fσ8 + Planck A_s prior leaves w0wa unchanged (w0 −0.852, wa −0.530), fσ8 χ² 3.76/6, ΔχΛCDM 7.87
## D1214: S4e2 NOT RUN (2-h limit); its V2 part (printed before the limit, informational) shows FD and Prüfer agree to 1.3e-7 — S4e's −4% vs BTR is not a solver error
## D1215: J7k — HI scored (Janus better 2/2, ~1000×); RPQTI listed (ASPIC Fortran crash), KMIII listed (2-h limit); pulses 208/208
## D1216: S4e3 — four locked warp normalisations (as-is, warp max, midpoint, Planck-weighted) give m L/π 0.93–1.01 / 2.04–2.21; none matches BTR's 0.97/2.13 → NOT EXPLAINED (post-hoc)
## D1217: JMF9 — Janus-MF-NC (covariant MS, curved field space) matches PyTransport NC on DoubleQuadNC: n_s 0.925024 vs 0.925023 (|d| 8.1e-7); VALIDATED
## D1218: J7m — 12 new two-parameter points (TI, SFI scored; PSNI ×3 and SFI p=1 listed): Janus better on 16/16, median |Δn_s| 2.9e-6 vs ASPIC 7.5e-4 → JANUS MORE ACCURATE
## D1219: N3 — N3LO n_s beats second order at 16/16 points (median 2.87e-6 vs 8.27e-6) but misses the locked ×3 margin (2.88) → NOT CONFIRMED; residual looks like fourth order (post-hoc)
## D1220: JMF10 — Janus-MF fast (one ODE for all k) ×3.9 at |Δn_s| ≤ 5e-8; quick mode (bd 300) ×11.2 at ≤ 2.5e-7 → both adopted (labelled)
## D1221: JMF11 — compiled Janus-MF (numba DP5(4)) matches spectra_mf to ≤ 5.3e-8 in n_s at median ×36 speed (quick mode ×121) → adopted as PC default
## D1222: JMF12 — compiled Janus-MF-NC matches on DoubleQuadNC and flat (|Δn_s| ≤ 6.5e-8, ×36–39) but the R=2 sphere case is unphysical in both codes (n_s 3.49 vs 85.9) → NOT ADOPTED; JMF12b with a sanity gate next
## D1223: JMF12b — nc-jit matches at R=1 (×34, |Δ| 1.8e-7) but R≠1 spheres are unphysical in both codes → INCONCLUSIVE; suspect a shared R-scaling issue in mfms_nc (item 25), pole hypothesis refuted
## D1224: JMF13 — Janus-MF codes normalised a = e^N, so long runs dropped mode amplitudes below the ODE atol (garbage at R ≥ 1.5); fixed with a = e^(N−N_p): unchanged ≤ 1e-7 where it worked, R = 1.5/2 now match PyTransport to 4e-5 → adopted
## D1225: MSJ1 — compiled exact single-field MS reference matches spectra_fast on 16/16 points (|Δn_s| ≤ 2e-8) at median ×23 → adopted (ms-jit)
## D1226: JSJ1 — compiled single-field Janus: same answers (≤1e-7), per point 0.225 ms vs ASPIC 0.468 ms (faster, ~250× more accurate), but ×19 vs core (<×20 locked) → not adopted yet; build step is the bottleneck
## D1227: JSJ2 — janus-jit adopted: same answers, ×29 vs core, per point 0.150 ms vs ASPIC 0.244 ms (faster); per model with the build still 2.8 vs 0.49 ms
## D1228: JSJ3 — janus-jit with compiled DOP853: same answers (≤1e-7), per point 0.095 vs ASPIC 0.404 ms, per model 0.58 vs 0.81 ms → faster than ASPIC both ways, ~250× more accurate; adopted
## D1229: web-guided tick — top web conflict = SERAPIS-E plateau's string home; 2026 literature NULL for a new home; r separates SERAPIS-E (4.6–5.1e-4) from loop blow-up (1.8e-5) and Casas–Ibáñez (1–3e-3)
## D1230: web tick 2 — Chronos/Hyperion added to the web; top conflict = wino window; our relic uses constant g_* = 106.75, and the SM EOS shifts WIMP abundances 5–10 % (2005.03544) ≈ our +5.4 % mass offset → needs the EOS table ("yes table")
## D1231: J7m2 — bisection start fails for all three listed PSNI points (e-fold window unreachable) → 5b BLOCKED; J7m totals unchanged
## D1233: NA1 — SERAPIS-E chain recomputed live in the Janus app: frozen band consistent (9/9 inside), caps consistent; corrected N* 50.5 pushes two box corners just outside (r −1.7 %, n_s +2.5e-4) → flag band_e
## D1234: NA2 — mnu Σ = 0.05878 eV from NuFIT 6.0 PASS; Janus relation off by 3–4 % (not D689's 13–16 %) FAIL-as-locked; nstar_e node still pre-D979: corrected 49.88–50.64 (FAIL-as-locked); D1233a correction
## D1235: NA3 — reheat_rho: m_φ = 3.17e13 (not 2.2e13); D725 couplings normalised for K = −3 ln while SERAPIS-E's inflaton has n = 1 → T_R ×2.1, N* 50.1–51.3; flag reheat_rho, nstar_e, lepto_rho
## D1236: NA4 — lepto_rho rescaled by NA3: Y_B ×1.44–1.98; c = 0.3 M_H = 1e12 → 1.03e-10 (passes, conditional on NA3 caveat); κ recheck needed where M/T_R < 500; wino window BLOCKED (EOS table host refused by proxy)
## D1237: NA5 — the ρ decays are the inflaton's (flavour modulus = inflaton); D721/D722 scripts used n = 1 for V and n = 3 for couplings → NA3 correction stands; taint list D720–D982 queued for one rerun lock
## D1239: NA6 — ρ chain rerun (n = 1, m_φ 3.17e13): T_R confirmed to 0.15 %, c = 3 M_H = 1e13 newly open (1.43e9); lepto pass fractions c = 1: 41–64 %, c = 3: 75 %, c = 0.3 @1e12: 2.2 % → still FAIL (D1236a correction)
## D1240: NA7 — darkrad_rho PASS at corrected T_R (×55–376 margin); caps CONSISTENT (cap falls with N*); τ = i scripts n = 1 except NULL D726; reheat_i m_φ 1.9e11 vs 2.3–2.7e11 (D730) → ΔN* +0.03–0.16 flag
## D1241: NA8 — τ = i chain with D730's m (2.28/2.65e11): T_R ×1.31/1.65 → 1.3–5.0e6 GeV, N* +0.09/+0.17; lepto_i verdicts unchanged
## D1242: NA9 — gravitino → wino at audited T_R: max Ω_nth 4.4e-4 (τ = i, M2 1.85 TeV) < 0.01 PASS; label ≤ 3e-4 → ≤ 5e-4; diluted SERAPIS-E case T_R-insensitive; C_lepto PASS
## D1243: NA10 — D745 radiative resonant leptogenesis rerun with D730 m_φ: pass 38–86 % / 42–86 % (was 34–86 %), PASS; eta_n, lepto_i unchanged
## D1245: PW1 (web postulate 1) — audited SERAPIS-E box n_s 0.9717–0.9760, r 4.38–4.90e-4 (live Janus scan); 4/9 corners inside frozen band; pre-stated ranges FAIL (5/9)
## D1246: NA11 — SERAPIS-E core arithmetic all PASS (lattice E(ρ,2) = 5.7833592, isotropic minimum, 2ζ(4)y² plateau, BHK C per tadpole row, tadpole = 16); D1234a: D689's 13–16 % belonged to the predecessor model, janus consistent with D693's ≤ 6 %
## D1247: NA12 — τ = i with audited reheating (N* 50.40–50.45): ε window narrows to ≈ 1.39–1.44e-4 (only ε = 1.40e-4 in band on the grid; n_s 0.97462, r 4.83e-4); D861 arithmetic PASS
## D1248: NA13 — tests_cmb: D751 reproduced; audited n_s edges separate SERAPIS-E 3.1σ (att60) / 2.5σ (kination cap), τ = i 5.0σ / 4.3σ with SO+SPHEREx; r 8.8–9.7σ only for optimistic LiteBIRD
## D1249: NA14 sweep — vac/n_sector/halo arithmetic all PASS (D785 rerun identical); tests_lhc corrected: HL-LHC wino reach 0.9–1.1 TeV (1812.07831) cannot close 0.67–1.85 TeV; HE-LHC 1.5–2.1 TeV would
## D1250: NA15 — theory-lane audit complete (wino_window BLOCKED on g*(T)); matter parity and covariant bounds PASS; eps_tilt → 1.39–1.44e-4 (τ = i); audit summary of all corrections
## D1251: PW2 — SERAPIS-E point prediction (c = 1, M_H 1e12 → T_R 8.94e8 → N* 50.24; C 1.25e-6): n_s 0.97445, r 4.81e-4, α_s −9.97e-4; expectation PASS; inside frozen band; live Janus app
## D1252: NA16 — B1/B2 bridges fail 10/10 on SERAPIS-E (Twist-era nulls, r/(1−n_s)² 0.57–0.83 vs 3); relabelled; SERAPIS null = Janus relation; R_w0wa ΛCDM pulls −2.8σ/+2.6σ (1-D); C_nstar updated
## D1254: TK1 (partial) — Janus core vs exact MS |Δn_s| ≤ 1.5e-6, r 0.01 % (4 rows); α_s bar fails on 2 rows because the exact-MS α_s is step-dependent noise (D2: −8.0/−7.6/−2.2e-4 for 3 step sets); remaining rows + CAMB → upgraded MS (U1)
## D1255: U1/U1b — compiled exact MS for SERAPIS-E: ×600 faster (0.9 s / 9 k); α_s noise traced to the BD-start ripple at k/aH = 200 (not the integrator); bd 4000 + 9-pt fit → α_s stable 2e-5, Janus core α_s confirmed to ≤ 4e-6; ADOPTED
## D1256: TK1 complete — 9/9 SERAPIS-E box points; Janus core = exact MS (U1b) to Δn_s ≤ 1.1e-6, Δr/r 0.011 %, Δα ≤ 3.3e-6; CAMB BB(80) 2.7–3.0e-5 μK²; pulls SPA +1.5–2.5σ, SPA+DESI 0–1.2σ
## D1257: U2 predict_fast ADOPTED (exact to TK1, 23–26 s vs ≥ 15 min); W1 measured wave: tilt link 0.394σ > N* link 0.343σ > T_R decade 0.261σ (heuristic ordering REVERSED), all linear (≤ 3 % asymmetry); C and N* separate in r
## D1258: W2 — reheating-chain waves at the PW2 point: m_φ ±10 % 0.016σ, g* SM→MSSM 0.021σ (ΔN* −0.063), Kähler √3 0.061σ; all linear, as pre-stated; flag: SERAPIS should use MSSM g* = 228.75
## D1260: U4 — Hyperion/Janus-LT recombination vectorised: ×72 faster (6.6 → 0.09 s), z*, z_d, χ² identical; ADOPTED
## D1261: TK2 — SERAPIS late universe (ΛCDM, Σm_ν 0.05878) χ² 15.32; w0wa preferred Δχ² −7.98 (2.4σ, 2 dof); fit in 19 s with U4
## D1262: A1 — MSSM g* = 228.75 applied to SERAPIS reheating: point N* 50.181, n_s 0.974393, r 4.821e-4; box n_s 0.97166–0.97596, r 4.389–4.897e-4, N* 50.07–51.22 (expectation band FAIL by 5e-7 on one corner)
## D1263: PW3 KILLED — Janus κ does not separate the ρ/τ = i vacua (τ = i own-κ 10.8 %, crossed 13.2 %); vacua differ by Δα_s 1.4e-4 only (≤ 0.09σ) — vacuum choice not decidable from CMB inflation data
## D1264: PW4 PASSES — SERAPIS-E covariant m3/2 bound at its own y (14.6–16.6): < 2.0e9 / 6.7e8 GeV, ×960 above the AMSB wino need (≤ 7e5); Chronos-range bound (y 23–30) was marginal
## D1265: PW5 PASSES (forecast) — CMB as a string meter: SO n_s → Im S·Im ρ ±14 % (T_R known); + LiteBIRD r (optimistic) → ±19 % and T_R to 2.8 decades; response slopes match the audited box edges (2–8 %)
## D1267: papers 5 (SERAPIS-E audited, doi 10.5281/zenodo.24330316) and 6 (MS start-condition ripple, doi 10.5281/zenodo.24330318) published, files md5-verified
## D1268: PW6 PASSES — inverse string meter at T_R 7.39e8: n_s 0.972/0.974/0.976 → Im S·Im ρ 953/804/697 (exact); PW5 linear inverse ≤ 0.4–2.4 % inside, 3.5–7 % at 0.970/0.978
## D1270: PW7 KILLED — benchmark instanton M_H 9.8e10 → T_R ≈ 7e7 GeV, leptogenesis 0 % (Y_B ×12 short); point's M_H = 1e12 is a choice, not a benchmark output; would-be point N* 49.41, n_s 0.97362 (still in frozen band)
- D1272 (2026-11-18): SERAPIS-E tool cross-check — PT1 emulator |Δn_s|≤3.2e-5 vs exact across C∈[1.0,1.6]e-6; PW6 meter C,P consistent (~1%). Trajectory reproduced. [tool/numerics]

## D1272: SERAPIS-E tool cross-check: the PT1 emulator and PW6 inverse meter reproduce the EXACT point across the C band (2026-11-18)
1. Computed the exact SERAPIS-E point (n_s, r, alpha_s, N*) via Janus core spectra3 + N* self-consistency at T_R=7.389e8 GeV, g*=228.75, N_eff=4, Nmax=4000, for C in {1.0,1.15,1.30,1.60}e-6. [derived]
2. Computed the PT1 emulator at the same C and differenced: |Δn_s| ≤ 3.2e-5 across the band, r to ~1e-6, alpha_s to ~1e-5. [derived]
3. Inverse meter (PW6 log-interp table) at n_s=0.97439 -> C=1.248e-6, P=782 (=15·N_eff/64π⁶C); exact pipeline C≈1.26e-6, agree ~1%. [derived]
4. Recorded point n_s=0.97439 <-> C≈1.25e-6, r≈4.8e-4, alpha_s≈-9.9e-4, N*=50.18 reproduced; trajectory consistent. No new physics claim. [derived]

## D1273: Where SERAPIS-E sits against the CMB: +2.0σ vs CMB-SPA, +0.6σ vs CMB-SPA+DESI; the Janus α_s relation is ~3% approximate (2026-11-18)
1. Took the exact SERAPIS-E point n_s=0.97439, r=4.82e-4, α_s=−9.98e-4, N*=50.18 (pipeline, D1272-verified). [derived]
2. Differenced n_s against the published constraints: +2.00σ vs CMB-SPA 0.9684±0.0030; +0.59σ vs CMB-SPA+DESI 0.9728±0.0027. [literature]
3. Compared r=4.82e-4 to the r<0.036 bound: 75× below, so r is not a near-term discriminator. [literature]
4. Evaluated the analytic Janus relation α_s(n_s,r,p=2√2,κ=1) = −9.640e-4 vs pipeline −9.980e-4 → 3.4% approximation; use the pipeline value for scoring. [derived]

## D1274: n_s error budget: σ_theory = 0.0133 × (fractional moduli uncertainty); pinning Im S·Im ρ to ≲5% is the highest-value next target (2026-11-18)
1. Took the D1272-verified exact table n_s(C) and formed the local slope at C0=1.25e-6 from the 1.15–1.30e-6 bracket: dn_s/dC = 1.067e4 per unit C. [derived]
2. Converted to a fractional form: C0·dn_s/dC = 0.01333, so σ_theory(n_s) = 0.01333 × (δC/C). [derived]
3. Used C = 15·N_eff/(64π⁶·Im S·Im ρ) to map δC/C onto the moduli product: 5% → 6.7e-4, 10% → 1.33e-3, 20% → 2.67e-3. [derived]
4. Combined theory and data errors in quadrature against the CMB offsets; tension vs CMB-SPA falls only 2.00σ→1.82σ at 10% moduli, so the tension is not an artefact of our uncertainty. [derived]

## D1275: Im S·Im ρ: the construction (560–975) CONTAINS the CMB-meter value (804), but is wider than the data — SERAPIS-E is currently a meter, not a predictor (2026-11-18)
1. Took the construction range Im S·Im ρ = 560–975 (stacks (5,2)) and formed its central value and width: 768 ± 208 (±27%). [derived] (D696/D830)
2. Compared the PW6 inverse-meter value at n_s=0.974, Im S·Im ρ = 804: it lies inside the range, +4.8% from central — an independent consistency pass. [derived] (D1268)
3. Propagated the construction width through D1274's slope: σ_theory(n_s)=0.01333×0.27=3.6e-3, i.e. 1.2× the CMB-SPA error and 1.3× the +DESI error. [derived]
4. Concluded the branch currently operates as a meter (data→moduli, ±14%, D1265) not a predictor, and identified the heavy-ν/leptogenesis sector as an independent cross-scale constraint on the same product. [derived]

## D1276: Shape selection in d=2: hexagonal (τ=ρ) beats square (τ=i) at equal covolume, and the margin grows with the exponent (2026-11-18)
1. Built unit-covolume Gram forms for the square (τ=i) and hexagonal (τ=ρ) lattices and checked det(Gram)=1 for both, so the comparison is at fixed covolume. [derived]
2. Summed the Epstein zeta over 400 shells at s=2,3,4: hexagonal is lower by 4.04%, 11.11%, 19.80% respectively. [derived]
3. Noted the margin grows with s — shorter-range lattice sums select the shape more sharply. [derived]
4. Identified these two forms as the modular domain's elliptic fixed points, which are exactly our n_sector_i and n_sector_rho; recorded as a selection argument only, since the sector is actually fixed by the flux/stack construction. [derived]
5. Recorded the dimension chain A2/FCC/D4/E8/Leech and the nesting A2 ⊂ D4 ⊂ E8 ⊂ Λ24, with E8 and Leech universally optimal. [literature]

## D1265a: CORRECTION to D1265 (PW5): the n_s response at the benchmark is 0.0135, not 0.0117 — the CMB meter is ±12% on Im S·Im ρ, not ±14% (2026-11-18)
1. Fitted n_s vs ln C quadratically through the four D1272 exact points (max residual 9e-6). [derived]
2. Evaluated the response at the D861 benchmark C=1.249e-6: dn_s/dlnC = 0.01352, versus 0.01171 used in D1265 (13.4% low; that value matches C≈1.12e-6). [derived]
3. Re-derived the n_s-only meter: σ(ln C) = 0.0016/0.01352 = 0.118, so Im S·Im ρ to ±12% instead of ±14%; PW5's PASS is unchanged. [derived]

## D1275a: CORRECTION to D1275: the heavy-ν sector is NOT a clean independent handle on Im S·Im ρ₁ (2026-11-18)
1. Read the heavy-ν mass formula M = x·M_s·e^{−2πn Im T} with the instanton on a rigid cycle distinct from the gauge branes. [literature] (D852, hep-th/0609191)
2. Read M_s ≈ g_s^{1/4}M_P/√(4πV), V=(Im ρ)^{3/2}, and Im S = 1/(2√2π g_s). [derived] (D783, D689)
3. Concluded M constrains Im S·Im ρ₁ only jointly with Im T_inst, x and V, and that M_H is itself a choice (D1270); the ν handle is useful only if the construction fixes Im T_inst and x. [derived]

## D1277: Shape selection vs scale: in 2D hexagonal wins at every scale; in 3D BCC and FCC swap exactly at the self-dual scale (2026-11-18)
1. Built unit-covolume bases for square, hexagonal, SC, BCC and FCC and verified det = 1 for each. [derived]
2. Summed the Gaussian energy Σ e^{−πα|v|²} over 14 shells (2D) and 7 shells (3D) for α = 0.25…4. [derived]
3. 2D: hexagonal is lowest at every α; 3D: BCC lowest for α<1, FCC for α>1, exact tie at α=1, SC never lowest. [derived]
4. Explained the swap by Poisson duality θ_L(α)=α^{−d/2}θ_{L*}(1/α) with FCC* ~ BCC; self-dual lattices cannot flip. [literature]
5. Concluded the ρ-sector (hexagonal) preference of D1276 holds at all scales in d=2. [derived]

## D1278: Going up in dimension: the winning shape flips with scale if and only if it is not self-dual (tested d = 2, 3, 4, 5, 8) (2026-11-18)
1. Computed unit-covolume Gaussian energies for Zⁿ, Dₙ, Dₙ*, E8 with exact Jacobi theta formulas (θ₃ⁿ; (θ₃ⁿ+θ₄ⁿ)/2; θ₃ⁿ+θ₂ⁿ; (θ₂⁸+θ₃⁸+θ₄⁸)/2), rescaled to covolume 1. [derived]
2. Computed Aₙ and Aₙ* by brute force on the Cartan Gram matrix and its inverse, normalised to determinant 1. [derived]
3. Checked d=3 against D1277 (exact reproduction) and found: d=4 D4 at all α; d=5 D5*/D5 swap with an exact tie at α=1; d=8 E8 at all α. [derived]
4. Stated the rule (flip iff the winner is not self-dual) and its prediction for E6, E7 (flip) and Leech (no flip) — an extrapolation from the tested cases, not a derivation. [estimate]

## D1279: Running it backwards: a torus started at any shape slides to the hexagon; the square is a saddle held only by mirror symmetry (2026-11-18)
1. Wrote the d=2 torus shape as τ=x+iy with basis (1,τ) at unit covolume and the Gaussian lattice energy E(τ)=Σ' exp(−π|m+nτ|²/y). [derived]
2. Ran hyperbolic gradient descent from τ=3i, 0.02+3i and 0.30+2i, reducing to the fundamental domain to classify shapes; all paths end hexagonal with E decreasing monotonically. [derived]
3. Computed Hessians: τ=i has eigenvalues −0.295, +1.118 (saddle); τ=ρ has +0.635, +0.635 (isotropic minimum). [derived]
4. Noted τ=i and τ=ρ are critical points of any modular-invariant function, with min/saddle character set by the function. [literature]
5. Counted torus shape moduli d(d+1)/2−1 = 0, 2, 5, 9, 14, 35, 299 for d = 1, 2, 3, 4, 5, 8, 24. [derived]

## D1273a: CORRECTION to D1273: the 2σ tension belongs to the benchmark point, not the model; and the data inputs were unsourced (2026-11-18)
1. Checked the n_s inputs against primary sources: SPT-3G D1 CMB-SPA 0.9679±0.0033; published CMB-SPA 0.9679–0.9693 and CMB-SPA+DESI 0.9728–0.9737; BK18 r₀.₀₅<0.036. [literature] (2506.20707, 2512.10613, 2512.05108, 2110.00483)
2. Read D861: the benchmark's g_s and A₁ are chosen so C lands inside the frozen band 1.0–1.3e-6. [literature] (D861)
3. Computed the band's n_s span 0.97176–0.97493 and its σ offsets for every analysis: CMB-SPA +0.85…+2.18σ, +DESI −0.78…+0.79σ. [derived]
4. Concluded the 2σ figure belongs to the benchmark point and the band reaches ~1σ at its low edge. [derived]

## D1274a: CORRECTION to D1274: verdict (1) had a void premise — the moduli are fitted, not independently known (2026-11-18)
1. Confirmed the slope with a fresh symmetric difference: 0.01334 vs the 0.01333 used. [derived]
2. Noted verdict (1) assumes an independent moduli value with an error bar, which D1275b shows does not exist; verdicts (2) and (3) are unaffected. [derived]

## D1275b: CORRECTION to D1275: the "independent consistency pass" was circular; Im S·Im ρ is currently an input fitted to n_s (2026-11-18)
1. Read D689, D830 and DERIVATION_LOG: Im S·Im ρ is computed from the C that fits the n_s band, and C is "fixed by the frozen band". [literature] (D689, D830)
2. Concluded the 560–975 range is the n_s band mapped through the same formula over N_eff=3,4, so the meter value lying inside it is not an independent test. [derived]
3. Listed what the construction does fix (N_eff, the sector, the formula for C, naturalness) and what it does not (Im S·Im ρ; D861's g_s and A₁ are choices). [derived]

## D1265b: REFINEMENT of D1265a: the n_s response at the benchmark is 0.0133 (fresh symmetric difference), not 0.0135 (2026-11-18)
1. Ran exact points at C=1.249e-6×(0.97, 1, 1.03) and formed the symmetric log-slope 0.01334, versus D1265a's wide-fit 0.01352. [derived]
2. Recomputed the meter: σ(ln C)=0.120, Im S·Im ρ to ±12% (unchanged). [derived]

## D1280: τ = i is a SADDLE of the actual SERAPIS-E potential (unstable only along the axion); any potential monotone in E(τ,2) has its vacuum only at ρ (2026-11-18)
1. Took the model V/V0 = P3(Ê), Ê = E(τ,2) − E(ρ,2), from tools/serapis_calc/potentials.py, with C = 1.25e-6. [derived]
2. Used the repo's symbolic slope dP3/dE = (CE²+2CE+1)/(E+1)² > 0 to note that V is monotone in E(τ,2), so Hess V = P3′·Hess E at critical points. [derived]
3. Computed central-difference Hessians with the model's own E_fourier: τ=i [−1.2792, +5.7786] (saddle, negative mode along x), τ=ρ [+3.5623, +3.5623] (minimum); h = 1e-3 and 1e-4 agree. [derived]
4. Checked the eigenvalue ratio at i (−0.2214) against the bare Epstein s=2 ratio (−0.2215). [derived]
5. Concluded a τ = i vacuum needs an extra ingredient (pinned axion or a non-monotone building block), as in SERAPIS-1's j-based form; Kallosh–Linde likewise have i as a saddle. [literature] (D530/SERAPIS-1 history, arXiv:2212.03876 context)

## D1282: E6 and E7 flip against their duals at the self-dual scale α=1; E8 does not (D1278 prediction confirmed) (2026-11-18)
1. [derived] Poisson summation at unit covolume: θ_L(α) = α^{−d/2} θ_{L*}(1/α); hence θ_L(1) = θ_{L*}(1) for every lattice.
2. [derived] So if θ_L(α) < θ_{L*}(α) for all α > 1, then θ_{L*}(α) < θ_L(α) for all α < 1: a lattice that is not isometric to its dual must swap with it exactly at α=1.
3. [derived] Exact enumeration (|x|² ≤ 12, converged ≤3e-11): E6 beats E6* for α>1 (Δθ=−1.60e-3 at α=1.25), E7 beats E7* (Δθ=−2.59e-3); ties at α=1 to 1e-13.
4. [derived] E8 = E8* (unimodular): Δθ ≤ 7e-15 at every α → no flip.
5. [literature] Universal optimality is proven only in d=8 (E8) and d=24 (Leech) (Cohn–Kumar–Miller–Radchenko–Viazovska 2022); in d=6,7 the comparison here is Eₙ vs its own dual only.

## D1283: Optimal Narain (string) lattices match our shape results on the shape, not on the size (2026-11-18)
1. [literature] Angelinos–Chakraborty–Dymarsky, arXiv:2206.14825: toroidal compactifications ↔ even self-dual lattices in R^{c,c}; max spectral gap c=1: 1/2 (self-dual radius), c=2: 2/3 at SU(3)₁ with t = b = (1+i√3)/2.
2. [derived] t=(1+i√3)/2 is SL(2,Z)-equivalent to ρ=e^{2πi/3}: the c=2 optimum has the hexagonal shape — the SERAPIS-E vacuum point (D1280) and the lattice-energy winner (D1277).
3. [derived] T-duality R→1/R is the Poisson map α→1/α at unit covolume; a self-dual lattice is invariant, so by D1278 it never flips (D1282: E8 ties its dual to 7e-15).
4. [derived] The c=2 optimum also fixes the Kähler modulus at the hexagonal point (string-scale volume), whereas SERAPIS-E needs Im S·Im ρ ≈ 780; so the match is on the shape only.
5. [postulate P1] If some dynamics selects max-gap points, the shape half of the SERAPIS-E vacuum would be derived rather than chosen — open, needs a literature search.

## D1285: Moduli trapping selects enhanced-symmetry points dynamically, but shape and size together — not SERAPIS-E's shape-only match (2026-11-18)
1. [literature] Kofman et al., hep-th/0403001: particle production near extra-species points traps moduli there; Hubble friction makes it permanent; self-dual radius is the toroidal example.
2. [estimate] The c=2 maximum-gap point (SU(3), D1283) is an enhanced-symmetry point with extra light states.
3. [derived] Those states are light only when shape AND complexified size sit at the special point; at Im S·Im ρ ≈ 780 they are heavy for every shape, so τ=ρ alone is not a trapping point.
4. [derived] Trapping would therefore pull the torus to string-scale volume, opposite to SERAPIS-E; the shape preference remains the D1280 result (V monotone in E(τ,2)).
5. [postulate P1] A shape-only selector at large volume would need light states whose masses depend on τ alone (brane or flux sector on the inflaton torus) — open.

## D1286: In d=6,7 the E-lattices win against all standard families at every scale, handing over to their duals at α=1 (2026-11-18)
1. [derived] Locked predictions P1–P4 (PREREG_D1286) before computing.
2. [derived] Exact enumeration (|v|²≤12) of Zⁿ, Dₙ, Dₙ*, Aₙ, Aₙ*, Eₙ, Eₙ*, n=6,7, unit covolume: E has the lowest Gaussian energy for all α>1 (d=6 α=1.25: E .10458, E* .10618, D .11870, A .14604).
3. [derived] By Poisson, Eₙ* has the lowest energy for all α<1; every L/L* pair ties at α=1 to ≤9e-14.
4. [derived] Zⁿ is last at every α; the order E > E* > D > (A, D*) > A* > Z holds at every α>1 tested.
5. [derived] Champion chain d=2…8: hex, FCC/BCC, D4, D5/D5*, E6/E6*, E7/E7*, E8 — self-dual champions never hand over; the others hand over to their own dual exactly at α=1.

## D1287: CORRECTION — lattice notes D1276–D1286 belong to the serapis_e map node, not n_sector_rho (heavy-ν sector) (2026-11-18)
1. [derived] n_sector_rho is the heavy-neutrino sector node; the lattice results concern the inflaton torus shape and vacuum.
2. [derived] Re-map them to serapis_e; no numbers change; future lattice notes use node=serapis_e.

## D1288: The heterotic lattices E8⊕E8 and D16⁺ have identical shells and identical energy at every scale (isospectral tori) (2026-11-18)
1. [derived] Locked predictions P1–P4 (PREREG_D1288) before computing; one basis error fixed via DEVIATIONS (det 64 → 1).
2. [derived] Exact enumeration |v|² ≤ 6: both have shells 1, 480, 61920, 1050240.
3. [derived] Gaussian energies agree to ≤2.5e-14 at α = 1–3; both beat D16 and Z¹⁶.
4. [literature] Equal theta series ⇒ isospectral flat tori (Milnor 1964); both are even unimodular, so self-dual and never flip.
5. [derived] d=16 is a tie between two distinct champion shapes — lattice energy cannot choose between the E8×E8 and Spin(32)/Z2 heterotic lattices.

## D1289: The Leech lattice (d=24) verified from scratch — rootless, 196560 minimal vectors, self-dual, beats E8³ at every scale (2026-11-18)
1. [derived] Locked P0–P3 (PREREG_D1289). Built from Golay-code generators + LLL; det 1, even.
2. [derived] P0 partly failed: the code step gave the 11-dim even subcode (506 octads), not the 12-dim Golay code.
3. [derived] Enumeration |v|²≤4: no norm-2 vectors, 196560 of norm 4.
4. [literature] Even unimodular, rootless, d=24 ⇒ unique ⇒ Λ24 (Conway); shells 16773120 (norm 6), 398034000 (norm 8).
5. [derived] Self-dual ⇒ no flip; Gaussian energy below E8³ at all α≥1 (α=2: 2.39e-6 vs 2.51e-3) and, by Poisson, at all α<1.

## D1291: Self-dual champions' energies are modular forms (E4, E4², E4³−720Δ); the flip rule is modularity; E(τ,2) is the scale-integral of the lattice energy (2026-11-18)
1. [derived] Locked P1–P4 (PREREG_D1291).
2. [derived] E8 enumerated shells = 240σ3(n) (n≤6): θ_E8 = E4. E8⊕E8 = D16⁺ shells = E4² coefficients; Leech shells = E4³ − 720Δ.
3. [literature] Weight-8 modular forms are one-dimensional ⇒ every even unimodular 16-lattice has θ = E4² ⇒ the D1288 tie is forced.
4. [derived] Non-self-dual champions violate θ(α) = α^{−d/2}θ(1/α) by their L−L* gap; self-dual ones satisfy it (≤2e-11). The flip rule = modularity under τ → −1/τ with τ = iα.
5. [derived] Z_Λ(s) = π^s/Γ(s)∫₀^∞(θ_Λ−1)α^{s−1}dα reproduces D1276 (hex 5.783359, square 6.026812 at s=2): E(τ,2) is the all-scale integral of the Gaussian energy, so the hexagon's win at every scale (D1277) implies its win for every s.

## D1292: The 2D lattice energy has only two critical points (τ=i saddle, τ=ρ minimum) at every scale tested (2026-11-18)
1. [derived] Locked P1–P2 (PREREG_D1292).
2. [derived] Grid + Nelder–Mead refinement of the hyperbolic gradient over the fundamental domain at α = 0.5, 1, 2: only (0,1) saddle and (½, √3/2) minimum, |∇| ≤ 2e-11.
3. [derived] So the τ=i and τ=ρ sectors are the complete list of stationary torus shapes in d=2.

## D1293: For Epstein energies the dual handover sits at the exponent s=d/4, the exact analogue of the self-dual scale α=1 (2026-11-18)
1. [derived] Locked P1–P4 (PREREG_D1293); Z_L(s) analytically continued via Mellin + Poisson.
2. [derived] FCC/BCC, D5/D5*, E6/E6*, E7/E7*: Z_L − Z_{L*} changes sign at s=d/4 with a tie ≤1e-14; the large-scale winner has the lower Z for s>d/4.
3. [derived] Self-dual hex, D4, E8: Z_L = Z_{L*} for all s.
4. [derived] Functional equation s ↔ d/2−s is the Mellin image of Poisson α ↔ 1/α; s=d/4 is its fixed point.
5. [derived] SERAPIS-E: d=2, s=2, hexagon self-dual ⇒ no handover at any s; same selection as at every scale.

## D1294: The hexagonal torus (τ=ρ) is the repeated tile inside every higher champion: 16 (D4), 120 (E6), 336 (E7), 1120 (E8), 75,348,000 (Leech) (2026-11-18)
1. [derived] Locked counts (PREREG_D1294) = (#min vectors)(#at 120° per vector)/12.
2. [derived] Exact enumeration: D4 24·8/12 = 16, E6 72·20/12 = 120, E7 126·32/12 = 336, E8 240·56/12 = 1120.
3. [derived] Leech: 196560 minimal vectors, 4600 at 120° to each of 6 sampled ones → 75,348,000 ([literature] transitivity of Co0).
4. [derived] Each such plane has Gram ∝ [[2,−1],[−1,2]], i.e. shape τ=ρ — the SERAPIS-E vacuum.

## D1295: τ=i and τ=ρ are forced: they are Z[i] and Z[ω], the only 2D lattices with extra rotations, and symmetry makes every shape-energy stationary there (2026-11-18)
1. [derived] Locked P1–P3 (PREREG_D1295).
2. [derived] Automorphism orders: oblique 2, rectangle 4, rhombus 4, square 8, hexagon 12.
3. [literature] Z[i] and Z[ω] are the only imaginary-quadratic rings with units beyond ±1 (4 and 6 units); 8 = 2·4, 12 = 2·6.
4. [derived] A shape-fixing rotation acts on the tangent plane, so ∇E = 0 at τ=i, ρ for any shape-energy; checked ≤4.5e-10 (vs 0.14–0.32 at τ=2i).
5. [derived] Hence the two SERAPIS sectors are forced by symmetry; which is the minimum (hexagon) is set by the energy.

## D1296: Square (τ=i) planes inside the champions: 18 (D4), 270 (E6), 945 (E7), 3780 (E8), 2,288,695,500 (Leech) — outnumbering hexagons increasingly with d (2026-11-18)
1. [derived] Locked counts (PREREG_D1296) = (#min)(#orthogonal per vector)/8.
2. [derived] Exact enumeration: D4 18, E6 270, E7 945, E8 3780; Leech 196560·93150/8 from 6 sampled vectors ([literature] Co0 transitive).
3. [derived] Square/hex plane ratio 1.125, 2.25, 2.81, 3.375, 30.4 — rising with dimension.

## D1297: In d=3 every torus flows to FCC above the self-dual scale and to BCC below it; the cube is never a resting shape (2026-11-18)
1. [derived] Locked P1–P3 (PREREG_D1297).
2. [derived] 16 minimisations over the 5-dim shape space (8 random starts × α = 1.6, 0.6): all end at FCC (α=1.6, E = 0.02133827) or BCC (α=0.6, E = 1.18691409), matching the reference energies to 8 digits.
3. [derived] The cube Z³ is never reached; the destination switches at α=1 exactly as the flip rule (D1278) requires for the dual pair FCC/BCC.

## D1298: Barnes–Wall BW16 is the d=16 champion over E8⊕E8 = D16⁺ at every scale; similar to its dual, so it never flips (2026-11-18)
1. [derived] Locked P1–P4 (PREREG_D1298). BW16 by Construction D (RM(1,4) + 2·RM(3,4) + 4Z¹⁶) and LLL.
2. [derived] Minimal norm 8, kissing 4320; BW16 and BW16* at unit covolume have identical shells and energies (2-modular ⇒ no flip).
3. [derived] Gaussian energy below E8⊕E8 at α = 1–2 (e.g. 8.28e-5 vs 1.67e-3 at α=2) and, by self-duality, at α < 1.
4. [derived] 280 hexagonal partners per minimal vector → 100,800 τ=ρ planes inside BW16.
5. [derived] Refines D1288: the heterotic pair ties with each other, but BW16 is the d=16 champion.

## D1299: LHC wino cross sections from Drell–Yan scaling — one universal exponent κ ≈ −0.163 reproduces the 13.6 TeV table to 0.3% (2026-11-18)
1. [literature] Resummino aNNLO+NNLL wino cross sections at 13 and 13.6 TeV (arXiv:2304.11915, Table 6).
2. [derived] At LO without PDF evolution, s·σ is a function of τ₀ = 4m²/s only; built Φ(τ₀) from the 13 TeV table.
3. [derived] Pure scaling predicts the 13.6 TeV table to ≤1.0%; a factor (√s/13)^κ with κ = −0.161…−0.165 (same for all three processes) brings it to ≤0.29%.
4. [derived] At 14 TeV the scaling and log-linear routes agree to ≤1%; their mean and spread are the tool's estimate and error.

## D1300: Wino chargino lifetime engine — δm(1 TeV) = 164.1 MeV, cτ = 5.83 cm, BR(π) = 97.9% (2026-11-18)
1. [literature] Two-loop δm fit and the π, eν width formulas of arXiv:1212.5989 (Eqs. 17, 21, 22); PDG constants.
2. [derived] Added the μν mode with the exact muon-decay phase-space factor.
3. [derived] δm rises from 149.5 MeV (100 GeV) to 164.5 MeV (3 TeV); cτ falls from 11.3 to 5.75 cm; τ(δm=160 MeV) = 0.226 ns.
4. [derived] Locked P1 partly failed (δm(1 TeV) = 164.1, not ≤163 MeV); P2–P4 passed.

## D1301: Disappearing-track recast reproduces the ATLAS wino limit (666.6 vs 660 GeV) and projects HL-LHC to ≈975 GeV (2026-11-18)
1. [literature] ATLAS 136 fb⁻¹ EW signal region: σ_vis < 0.037 fb (N₉₅ = 5.03), benchmark 8.6 events at 600 GeV, τ = 0.2 ns.
2. [derived] N_sig(m) scaled from the benchmark with Janus-LHC cross sections and the decay probability between 122.5 and 299 mm using the LHC2 lifetime.
3. [derived] Limit 666.6 GeV (observed N₉₅), 657.7 GeV (n = b); βγ 0.3–0.8 moves it by ≤ 2 GeV.
4. [estimate] HL-LHC like-for-like (14 TeV, 3000 fb⁻¹, Run-2 efficiency): N₉₅ = 17.6 on b = 66 → ≈ 975 GeV.

## D1303: The CERN+1 recast reproduces a second ATLAS search (36.1 fb⁻¹): 447.8 vs 460 GeV without retuning (2026-11-18)
1. [literature] ATLAS 36.1 fb⁻¹ EW SR: N₉₅ = 0.22 fb × 36.1 fb⁻¹ = 7.94; benchmark 13.5 events at 400 GeV, τ = 0.2 ns.
2. [derived] Same benchmark-anchored recast as D1301: limit 447.8 GeV (−2.7%); the 136 fb⁻¹ search stays at 666.6 GeV (+1.0%).
3. [derived] Boost assumption βγ = 0.3–0.8 changes either limit by ≤ 5 GeV.

## D1304: Model vs collider — the SERAPIS wino window begins at the LHC limit and HL-LHC tests its lower 26% (2026-11-18)
1. [literature] Model window 0.67–1.85 TeV (thermal wino, D784; read-only).
2. [derived] CERN+1 Run-2 limit 666.6 GeV (D1301) sits 3.4 GeV below the lower edge.
3. [estimate] HL-LHC like-for-like reach ≈ 975 GeV ⇒ 25.9% of the window testable; 975–1850 GeV needs other probes.

## D1305: CERN+1 symmetry self-tests — ratios scale with τ₀ to 0.1%; the u/d charge asymmetry turns over above 1.5 TeV (2026-11-18)
1. [derived] Locked T1–T4 (PREREG_LHC6).
2. [derived] Charge asymmetry σ(χ̃₂⁰χ̃₁⁺)/σ(χ̃₂⁰χ̃₁⁻): 1.58 → 3.36 up to 1.5 TeV, then down to 3.28 at 2 TeV — the locked monotonic rise FAILS; the turnover coincides with the PDF-limited region.
3. [derived] At equal τ₀ the asymmetry and the charged/neutral ratio agree between 13 and 13.6 TeV to 0.093% and 0.050%.

## D1306: Future colliders — CERN+1 matches the published HL-LHC and HE-LHC wino reaches; FCC-hh comes out short; FCC-hh covers the whole SERAPIS window (2026-11-18)
1. [literature] Published disappearing-track wino reaches (arXiv:1805.00015): HL-LHC 0.9/0.5, HE-LHC 2.1/1.5, FCC-hh 6.5/4.5 TeV.
2. [estimate] CERN+1: Drell–Yan-scaled cross sections (κ extrapolated), Run-2 efficiency and decay window, background × luminosity × R_bkg (1 or 10).
3. [derived] HL-LHC 0.974/0.801, HE-LHC 1.684/1.360, FCC-hh 3.741/2.876 TeV; FCC-hh high-background variant 36% short (locked 25% fails); κ = 0 gives 4.03/3.11 TeV.
4. [derived] Every FCC-hh variant exceeds 1.85 TeV, so the full SERAPIS wino window is testable there.

## D1307: CERN+1 kinematic boost distribution
1. [derived] Φ(τ₀)=∫dτ/τ L(τ) g(τ₀/τ), g=β(3−β²)/2 for an s-wave fermion pair through a vector current.
2. [estimate] L(τ) shape N τ^(−a)(1−√τ)^b fitted to Resummino 13 TeV table: max deviation 3.2%.
3. [derived] transverse βγ = p sinθ/m, cosθ from 1+cos²θ; decay window average replaces fixed βγ.
4. [estimate] ATLAS recasts 661.5 / 446.6 GeV vs published 660 / 460.

## D1308: registry access to the computed boost
1. [derived] lhc_dt_limit(search, boost="kinematic") calls kinematics.limit_search; values identical to D1307 (661.5 / 446.6 GeV).

## D1309: theory band on CERN+1 recasts
1. [literature] per-channel scale and PDF uncertainties from arXiv:2304.11915 Table 6 (13.0 TeV).
2. [estimate] channels fully correlated, σ-weighted; scale and PDF in quadrature.
3. [derived] N(m)=N_b(1±ε(m))σ(m)/σ(m_b)·P(m)/P(m_b); δm ±0.4 MeV enters through P.
4. [derived] 661.5 ± 10.0 GeV (136 fb⁻¹); 446.4 ± 5.5 GeV (36.1 fb⁻¹).

## D1310: registry access to the theory band
1. [derived] lhc_dt_limit(search, band=true) returns theory_band.band(search); values identical to D1309.

## D1311: ATLAS 36 fb⁻¹ residual
1. [literature] acceptance 0.09 (400 GeV) and 0.12 (600 GeV) at τ = 0.2 ns, arXiv:1712.02118 Table 2; limit at fixed τ = 0.2 ns; window 122.5–295 mm.
2. [estimate] acceptance taken linear in mass between the two points.
3. [derived] recast with kinematic boost and these inputs: 457.2 GeV vs published 460 GeV.

## D1312: gamma-line link in the CERN+1 panel
1. [literature] verdicts taken as recorded in D1126, D1150 and D1153 (Hyperion track); no recomputation.

## D1313: CERN+1 higgsino cross sections
1. [literature] Resummino aNNLO+NNLL higgsino tables, arXiv:2304.11915 Table 4.
2. [derived] Drell–Yan scaling s·σ = Φ(τ₀)(√s/13)^κ with the wino κ predicts the 13.6 TeV higgsino tables to ≤ 0.34%.

## D1342: MAP-line backfill (metadata only)
1. [derived] 20 notes lacked MAP lines; each gets the parent's node/status (ripple=no) or `MAP: none`; ladder applied-set unchanged, so the map is unchanged.

## D1343: τ = i α_s recheck (ripple-free exact MS)
1. [derived] D632 potential compiled with ms_jit; 9-point ln k fit at bd = 4000 gives α_s = −8.5498e-4 (ε = 1.40e-4) vs −8.543e-4 before: Δ = −7e-7.
2. [derived] Lock rule: |Δα_s| ≤ 2e-5 → D1247 confirmed; no correction note.

## D1344: node sync pass 1
1. [derived] Out-of-sync pairs found by comparing each node's last D-note with its inputs' last D-notes (19 nodes).
2. [derived] vac_i: D1280 (τ = i is a saddle of SERAPIS-E) implies the τ = i vacuum needs a pinned axion → status assumed.
3. [derived] 17 pairs reviewed as no effect or already in sync (reasons recorded in theory/map/sync.yaml); tests_lhc left to the wino track.

## D1345: CubeMind verifier pass
1. [derived] 8 proposals checked against D1280, D1275b, D1272, D1262; 6 rejected with reasons, 2 answered (1 tool-grounded, 1 estimate).
2. [estimate] dN*/d ln T_R ≈ 0.34 from the audited box (D1262), giving the T_R → n_s answer.

## D1346: D1255 recheck closed
1. [derived] Janus-vs-exact α_s agreement of 3–6e-7 (D1148, D1176, D1218) excludes a 1e-4 reference ripple; verdicts stand.

## D1347: CubeMind learn-loop upgrade
1. [derived] Hash-embed cosine: same-topic pairs median 0.60 vs different-topic 90th percentile 0.65 → too weak for duplicate detection; rule-based pre-gate used instead.

## D1348: CubeMind embedder/proposer + literature data
1. [derived] 1,801/1,831 learner cycles were 'holding' → verification, not model speed, limited proposals.
2. [literature] 2601.09542: τ = i, ω extrema only for tuned parameters, generally not minima.

## D1349: τ = i axion pin
1. [derived] ΔV = A V0(1 − cos 2πx) vanishes with ∂ₓ on x = 0 → inflation along x = 0 unchanged.
2. [derived] Stability needs A ≥ −∂²ₓV/(4π²) = 5.61e-2 V0 (maximum at τ = i); ∂²ᵧV(i) = +10.0 V0.
3. [derived] V(i) = 0.196 V0 > 0 = V(ρ): the pinned τ = i of SERAPIS-E's potential is a false vacuum.

## D1350: tests_lhc sync
1. [derived] Window 0.67–1.25 TeV vs CERN+1 reaches: HL-LHC 0.80–0.97 TeV → 23–52 % covered; HE-LHC 1.36–1.68 TeV → 100 %.

## D1351: τ = i variant vacuum
1. [derived] V depends on τ via |j − 1728| (double zero at i) → V(i) = 0; scan minimum at i.
2. [derived] ∂²ₓV > 0 along x = 0 for y = 1.02–3 and ∂²ᵧV(i) > 0 → true vacuum, no pin; D1280/D1349 apply to SERAPIS-E's E(τ,2) potential only.

## D1352: lattice-geometry α-attractor configs
1. [postulate P6] One Poincaré disk per complex dimension of lattice L: 3α = d/2 (A2 1, D4 2, E6 3, E8 4, BW16 8, Leech 12).
2. [literature] 3α = 1…7 disk family (Ferrara–Kallosh 2016; Kallosh–Linde–Wrase–Yamada 2017).
3. [derived] Exact T-model: sinh²y_e = 4/(3α), cosh y* = cosh y_e + 4N/(3α), r = 64/(3α sinh²y*); numerics agree to 3.5e-4 (r).
4. [derived] n_s = 0.9608 (N*=50.7) / 0.9639 (N*=55) for every lattice; r = 1.5e-3 (A2) … 1.6e-2 (Leech). Lattice shows only in r; below the SERAPIS n_s band; plateau_origin stays assumed.

## D1354: SERAPIS circuit + two corrections
1. [derived] Six A2 triangle laws (n_s, n_s-MS, N*, α_s, C, r) close within tolerances fixed before the run; spreads 2.5e-5 … 3.6%.
2. [derived] dN*/dln T_R = (1−3w)/(3(1+w)) = 1/3 at w = 0 (ρ ∝ T⁴); the first-run bound 1/12 was the per-ρ coefficient (my error).
3. [derived] r/3(1−n_s)² = 0.245: SERAPIS-E sits below the Starobinsky line; B1 is not a law for this model (my misapplication).

## D1355: SUSY shell of the circuit
1. [literature] One-loop AMSB M_i = b_i g_i²/(16π²) m3/2, b = (33/5, 1, −3); g_i² at 1 TeV = 0.212, 0.420, 1.118.
2. [derived] m3/2(M2 = 1.85 TeV) = 6.96e5 GeV (record 7e5); |M3|/M2 = 7.99 (D809: 7.0); M1/M2 = 3.33 → wino LSP; bino card "M2/2" corrected.
3. [derived] HL-LHC covers 52.9% / 26.1% of the 1.25 / 1.85 TeV windows (records 52% / 26%); window upper edge 1.25 vs 1.85 TeV across records is an open inconsistency.

## D1356: BTR gap = common scale
1. [literature] BTR eq. 5.14: m₁ ≈ 0.97 π/L, m₂ ≈ 2.13 π/L, L = Einstein-frame proper length; Dirichlet or Neumann BCs.
2. [derived] Our m₂/m₁ = 2.190 lies inside BTR's rounding range 2.179–2.212 → the spectrum shape agrees; the −4% is a common length/mass scale.
3. [estimate] Neumann BCs do not reproduce 0.97/2.13 (exploratory); candidates left: dilaton-normalisation convention, α_E normalisation, rounding.

## D1357: BTR scale recheck
1. [derived] m L/π is independent of α_E (y → y/√α_E, m² → α_E m², L → L/√α_E).
2. [estimate] Singular-end cut ξ₁ → 0: m L/π → ≈0.9384, 2.0543 (+0.7% vs ξ₁ = 1e-4); gap to BTR ≈ −3.3%/−3.6%, ratio still 2.189.
3. [derived] Far-end cut and far-end BC have no effect (< 1e-5); Neumann at the singular end −0.3%/−0.4%; no single choice gives +4% → open.

## D1358: extension route closed
1. [literature] 2305.09587: scalar perturbations have μ = μ̃ = 1 at both ends → unique square-integrable BCs; their spectrum M² ≃ (π/z_m)²[n(n+1) − 7/8] is an estimate.
2. [derived] Our ξ₁ → 0 limit is that unique solution; the ≈3.4% common gap to BTR's two-figure "≈" values is not a boundary-condition choice.

## D1359: Moonshine layer
1. [derived] Exact j series: c₀ = 744 = 3·(240 + 8) = 3 dim E8; c₁ − 196560 (Leech kissing) = 324.
2. [literature] McKay/Thompson: 196884 = 1 + 196883; 21493760 = 1 + 196883 + 21296876 (Monster representations).
3. [derived] Heterotic 16 = rank E8⊕E8 = rank D16⁺ (isospectral to 2.7e-13); bosonic 24 = Leech rank (no roots); j(i) = 1728 from the series ties the layer to the τ = i vacuum.

## D1360: Hyperion full run
1. [derived] 24,522,893 stars integrated in MWPotential2014 (3 Gyr) on the PC; every tile sane (0 bad), median ecc 0.164, z_max 0.58 kpc, r_peri 6.73, r_apo 8.86 kpc.
2. [derived] A8d M1–M4 PASS on the parallel code; McMillan17 full run still open (CPU-bound, ~10 days).

## D1361: P3 candidate source
1. [literature] Green–Russo–Vanhove 2010 eq. (4.10): the 8D D⁴R⁴ coefficient contains −4 E^{SL(3)}_{−1/2}·E₂(U), U the T² complex structure.
2. [derived] Eigenvalue check: (Δ − 10/3)E = 0 with s(s−1) = 2 for E₂(U) and 4/3 for E^{SL(3)}_{−1/2} → 10/3; E₂(U) is forced, not inserted.
3. [postulate P3] Turning this curvature term into the SERAPIS plateau (mechanism, sign at ρ, magnitude vs V0, 8D → 4D) is not yet computed; P3 stays open.

## D1362: P3 step 1
1. [literature] GRV eq. (4.10) verified; E_s normalisation = ours; U₂ = r₂/r₁ is the T² shape (complex structure).
2. [derived] Weak coupling: E^{SL(3)}_{−1/2} < 0 (constant term eq. 4.14) → the E₂(U) term enters with a positive coefficient, lowest at the hexagon ρ, saddle at i.
3. [postulate P3] Curvature-term → potential map, plateau shape and magnitude not yet computed.

## D1363: P3 step 2
1. [literature] Casas–Ibáñez 2407.12081: log|η|/G̃₂ species-scale potential, vacuum at i, origin not derived → our E(τ,2)/ρ route is distinct.
2. [literature] Ciupke–Louis–Westphal 1505.03092: four-derivative terms give V₁ = −e^{2K}T|DW|⁴; a minimum needs a negative operator sign.
3. [derived] Leading U-shape is Ê₁(U) = −log(U₂|η|⁴) (from R⁴); E₂(U) is next order (D⁴R⁴); both minimal at ρ; sign of the operator decides min vs max.

## D1365: P3 escape via universal thresholds
1. [literature] Petropoulos–Rizos hep-th/9601037 eqs. (2), (23), (31): Δ_α = −b̂_α log(T₂U₂|η|⁴) − k_α Y(T,U); Y = 6πT₂ + 90κ/(πT₂) + … at U = i.
2. [derived] κ = E(i,2)/π² (to 4e-10): Y's 1/T₂ term is (90/π³)E(U,2)/T₂ at U = i.
3. [estimate] Same term for general U (unfolding argument; unchecked).
4. [postulate P3] Plateau from E(U,2) via a b̂ = 0 condensing factor — model, sign and ratio form not computed.

## D1366: general-U E(U,2)/T₂ term in Y
1. [literature] DKL degenerate-orbit unfolding of Γ₂,₂ onto the strip.
2. [derived] ∫(dτ₂/τ₂)(T₂/τ₂)(90/πτ₂)e^{−πT₂|j+pU|²/(U₂τ₂)} summed → (90/π³)E(U,2)/T₂ for all U; matches κ = E(i,2)/π² at U = i.
3. [postulate P3] Plateau via a b̂ = 0 condensing factor — model, sign, ratio form not computed.

## D1367: b̂ = 0 candidate
1. [literature] K3 instantons (k, 24−k): E7 with (k/2 − 2)×56; N=2 b̂ = 2(ΣT(R_hyp) − T(adj)).
2. [derived] k = 10: 3×56, b̂ = 2(18 − 18) = 0; only split with an N=2-conformal E7.
3. [derived] That factor's threshold U-dependence is −Y ⊃ −(90/π³)E(U,2)/T₂ (no s = 1 term).
4. [postulate P3] 4D N=1 embedding, condensation and the plateau ratio form not shown.

## D1368: condensate sign and shape
1. [literature] 16π²/g² = k·16π²/g_s² + Δ, Δ ⊃ −kY; Λ³ ∝ exp(−24π²/(|b|g²)).
2. [derived] Λ³ ∝ exp(c·E(U,2)/T₂), c > 0 → |W|² minimal at ρ: vacuum at the hexagon.
3. [estimate] Leading shape exp(cE) has no plateau; SERAPIS ratio form not reproduced (SUGRA terms neglected).
4. [postulate P3] Saturation mechanism for the plateau still assumed.

## D1369: sources for −a/E(U,2)
1. [literature] D699: plateau = V_up(1 − E(ρ,2)/E(U,2)); cf. loop blow-up inflation 2403.04831.
2. [derived] D-term ∝ +1/E (max at ρ, wrong sign); condensate ∝ exp(cE) (no plateau).
3. [estimate] F-term −3e^K|W|² with K ⊃ −log E(U,2) gives the right sign; BHK δK is additive (∝ +E), not 1/E.
4. [postulate P3] Source of the −a/E term still assumed.

## D1370: no-scale with BHK δK, exact
1. [derived] K = −3 log T₂ + εE/T₂, W₀ const: V = e^K|W₀|² u²/(2u+3), u = εE/T₂ (sympy-checked).
2. [derived] Near ρ V ∝ E(U,2)² (min at ρ, no plateau); matches LVS V_loop ∝ (C^{KK})².
3. [postulate P3] A genuine −a/E(U,2) term still assumed.

## D1371: plateau via threshold-shifted dilaton
1. [literature] f = S − kY/16π², Y ⊃ (90/π³)E(U,2)/T₂; condensate fixes f.
2. [estimate] Re S* = s₀ + εE(U,2), ε = 90k/(16π⁵T₂).
3. [derived] V = b/A − b/(s₀ + εE) = (b/A)·x/(1+x), x = (ε/A)(E − E_ρ): the SERAPIS-E plateau (sympy-checked).
4. [postulate P3] Modular-weight/GS bookkeeping (s = 1 multiplier) and λ value unchecked.

## D1372: modular-weight condition for the plateau
1. [literature] 2411.06516 eqs. (32–36): W = e^{−3f/b}, f ⊃ (b − δ_GS)log η²; V ∝ 1/((T+T̄)³|η|¹²) diverges at large T.
2. [derived] U-multiplier [U₂|η(U)|⁴]^p destroys the plateau unless p = 0.
3. [estimate] p = 0 ⇔ b′_U = kδ^U_GS (no log in the GS-corrected threshold).
4. [postulate P3] δ^U_GS for the b̂ = 0 E7 plane unknown.

## D1373: λ free, C slope missing
1. [literature] D698: a = 1/λ absorbed into C → C·a; λ unconstrained.
2. [derived] D1371 route has C = 0; a second condensate gives slope 2c′/T₂, c′ = 4.354k′/|b′|; needs T₂|b′|/k′ ≈ 7e4–7e6.
3. [estimate] Unnaturally large T₂: C slope not explained.
4. [postulate P3] Origin of C still assumed.

## D1374 (D1373a): C slope origin
1. [literature] D689/D696: C = (15/64π⁶)N_eff/(Im S·Im ρ) from the BHK tilt (IIB stuck D3s).
2. [derived] e^{δK} multiplies a nonzero plateau height → linear (1 + C·E); D1370's cancellation needed V ≡ 0.
3. [estimate] Heterotic lead: K_S ⊃ −log(S + S̄ + const·Y) would give e^K ∝ 1/(s + c′E/T₂).
4. [postulate P3] One framework carrying plateau + tilt not yet built.

## D1375: one-loop K_S contains Y
1. [literature] KKPR hep-th/9608034 App. A: K = −log(Im S + (Δ^GS + Y)/16π²) + K⁽⁰⁾.
2. [derived] Y ⊃ (90/π³)E(U,2)/T₂ → e^K ∝ 1/(s + εE), ε = 90/(16π⁵T₂) = 0.01838/T₂; uplift tuned at ρ → (b/A)x/(1+x).
3. [estimate] Needs δ^U_GS = 0 and b′_U = 0 on the inflaton plane (else s = 1 log re-enters).
4. [postulate P3] Concrete orbifold plane with those properties not yet found.

## D1376: δ^U_GS = 0 realised, Γ₀(N) caveat
1. [literature] 1009.3931 eqs. (4.4), (4.13): δ³_GS = 0 on the U-plane; U enters via η(U/4), η(U/2) with nonzero exponents (b′ ≠ 0).
2. [derived] δ^U_GS = 0 is realisable; b′_U = 0 is not met by those condensing factors.
3. [estimate] η(U/N) ⇒ Γ₀(N) U-plane: Eisenstein minimum need not be ρ; need an SL(2,Z) plane.
4. [postulate P3] SL(2,Z) U-plane with b′_U = δ^U_GS = 0 not yet found.

## D1377: chamber T₂ > U₂*
1. [literature] P–R: Y's expansion valid for T₂ > U₂; log|j(T) − j(U)| diverges at T = U.
2. [derived] U₂* = 14.58 (Ê* ≈ 460); corrections 1.3e-4 at T₂ = 16, 1.6e-15 at T₂ = 20; εE* = 0.53–0.28.
3. [estimate] T₂ ≳ 16–20 heterotic large-volume tension unchecked.
4. [postulate P3] Model with SL(2,Z) U-plane, b′_U = δ^U_GS = 0 still needed.

## D1378: large-volume control
1. [literature] P–R eq. 2 thresholds; Y lowers the unification scale; heterotic decompactification problem.
2. [derived] Universal Δα⁻¹ = 1.5kT₂ = 24–30 at T₂ = 16–20; non-universal 1.11–1.43 per unit Δb′.
3. [estimate] One-loop ≈ tree: marginal perturbative control of Y.
4. [postulate P3] Model and control still open.

## D1379: control vs symmetry
1. [literature] hep-th/9606087: spontaneous N=4→N=2 breaking suppresses linear threshold growth (withdrawn arXiv version; published form unchecked).
2. [derived] The shift turns the D1366 sum into a parity-shifted (Γ₀(2)-type) Epstein series.
3. [estimate] Either SL(2,Z)+ρ with one-loop ≈ tree, or control with a different shape/vacuum.
4. [postulate P3] Resolution open; next: locked minima of shifted Epstein sums.

## D1380: shifted Epstein sums (locked)
1. [derived] Control E(U,2): min at an SL(2,Z) image of ρ, 5.78330 (gate pass on value; location wording note N1).
2. [derived] Σ′(−1)^m, Σ′(−1)^n, Σ′(−1)^{m+n}, half-shifted sum: no interior minimum; run to cusps.
3. [estimate] Mixed sector combinations untested.
4. [postulate P3] Option (ii) loses the vacuum for simple shifts; option (i) remains with marginal control.
