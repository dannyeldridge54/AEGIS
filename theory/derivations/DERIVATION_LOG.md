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
