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
