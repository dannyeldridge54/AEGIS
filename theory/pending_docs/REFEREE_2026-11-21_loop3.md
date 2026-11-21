# Referee report, loop 3: D1790 to D1803 (21 Nov 2026)

Independent skeptical referee. Scope: notes D1790 to D1803 in theory/pending_docs/D72_D75_weak_spots.md, the 21 Nov locks in field_tests/rules, the scripts in theory/tests (z3_modes, y4_oddflux, y4b_optimise, y5_z2omega, l8c_crossterm, d1795_frozen, u20_chain), and weave_walls, weave_edm, weave_rg, weave_rg2 and weave_nuclear in tools/weave_cm/weave_tools.py. No existing file was edited. The flavour scripts were rerun in a scratch copy, so no result file was overwritten.

## 0. What was reproduced (all OK)

| quantity | note | rerun |
|---|---|---|
| Z3 multiplicities M = 3, 5, 7, 9 (1/6, 5/6) | D1790 | (1,1,1), (2,2,1), (3,2,2), (3,3,3), residual < 6e-15 |
| Y4 Haar fraction / verdict | D1790 | 0 in all 9 pairs, FAIL; best r23 = 0.196 |
| Y5 leptons, control | D1791 | both hit to 1e-13; frac 0; medians 0.43 / 0.64 |
| Y4b, all 9 pairs | D1792 | identical JSON (HOSTED, control HOSTED) |
| σ_Λ, σ_β, α_D | D1793 | 38.634; 36.378 to 40.089; 0.02182 |
| Kähler-type and M_P⁴ rows | D1794 | 34.5, 44.0 (m₃/₂ = 1.07e-13 M_P = 2.6e5 GeV, consistent) |
| m/H0, f for m = H0 | D1795 | 63.5; 1.425 M_P |
| one-loop M₁₂, α⁻¹, Δ₃, α_s | D1799 | 7.43e15, 28.77, −0.903, 0.1066 |
| two-loop M₁₂, α⁻¹, Δ₃, α_s | D1800 | 1.072e16, 27.935, −0.154, 0.11584 |
| x, T_R, Re T_vis, χ, 𝒱 | D1801 | 0.279, 3.74e8, 20.146, 119 to 124, 1.0e5 (identical JSON) |
| radius, α_s precision | D1802 | 5.18, 4.25e-4 (with the tool's b₀; see finding 10) |
| wall peak | D1798 | 6.84e-9 at 30.5 nHz |

All lock hashes (.sha256) match. Every lock commit comes before its result commit. weave_tools self-test passes.

Formulas checked and found correct:
- **KKLT cross term.** With K = −3 ln(T+T̄) and W = W0 + A e^{−aT}, the K^{TT̄}K_T K_T̄ = 3 cancellation is exact. V = e^K[(4σ²/3)a²A²e^{−2aσ} + 4aσ W0 A e^{−aσ} cos aθ + …]. The prefactor 4aσ is right, and it agrees with the LVS cross term 4 a_s τ_s W0 A e^{−aτ_s}/𝒱².
- **Two-loop matrices.** The SM and MSSM b_ij are correct. Wino Δb₂₂ = (16/3)C(G)² = 64/3 and gluino Δb₃₃ = 48 are correct. Adding higgsinos (49/6) gives the Giudice–Romanino values 106/3 and 22. The two-loop RGE form dα_i⁻¹/dt = −b_i/2π − Σ b_ij α_j/8π² is correct.
- **Walls template.** It matches arXiv:2306.16219 Eq. (54), (56) and (57), including the 3/(32π) prefactor, ε̃ = 0.7 and f_p = 1.14 nHz. The DW-SM posteriors (T* 110–275 MeV, α* 0.080–0.19) and the Bayes factor 14.8 are quoted correctly.
- **Λ_QCD sensitivity.** The form δlnΛ = 2π δα_s/(b₀α_s²) is right; the problem is the choice of b₀ (finding 10).
- **NANOGrav comparison.** h²Ω ≈ 3.6e-9 at 1/yr for A = 2.4e-15, consistent with "~4e-9".

## 1. Findings

### D1793 / D1795 (and the inherited D1760): axion decay constant mis-normalised · MAJOR
- **What is wrong.** f = √3/(2σ) M_P equals √K_{TT̄}. That drops both the canonical-normalisation √2 and the 1/a from the period of cos(2πθ).
- **Correct value.** With T = σ + iθ, the kinetic term K_{TT̄}(∂θ)² gives φ = √(2K_{TT̄}) θ. Then cos(2πθ) = cos(φ/f) with **f = √(3/2)/(2πσ) M_P**. That is smaller by a factor of √2·π = 4.44: at σ = 38.6, f = 5.05e-3 M_P, not 0.0224.
- **Corrected numbers:**
  - D1795: m = 4.1e-31 eV = **282 H0**, not 64. The FAIL is stronger. The field starts oscillating at z ≈ 30–60, not ~15.
  - D1795: the energy share at 1e-33 eV becomes 5.8e-6, not 1.1e-4, which is below Svrcek's 1.7e-5. The cap becomes m ≲ 4.1e-31 eV, not 9e-32.
  - D1793: σ_β becomes 36.86–40.57 (36.72–40.43 with two-loop W0 and 𝒱). σ_Λ = 38.6 is still inside, so the SHIFTED verdict stands.
  - D1794: "f ≈ 5.4 M_P/S" becomes 1.2 M_P/S.
  - The old D1760 window (20.3–22.1) and every use of "f_ℓ ≈ 0.04 M_P" carry the same error. Line 17341 (f_a of the visible QCD-like axion) does too, so f_a ≈ 1.5–3e16 GeV, not 6.6–13e16.
- **Effect on verdicts.** None changes, but every f-dependent number does.

### D1793 / D1794: the dark-cycle saxion is not stabilised by the potential used · MAJOR
- **KKLT.** A KKLT minimum at σ = 38.6 needs W0 ~ aA e^{−aσ} ~ 1e-104, not 1.4e-8.
- **LVS.** An LVS blow-up minimum with W0 = 5.9e-9 and 𝒱 = 4.2e4 sits at a_sτ_s ≈ 30, i.e. τ_s ≈ 5, not 38.6.
- **Consequence.** The cycle must be fixed by something else (D-terms, loops, a fibre modulus). Otherwise Re T_dark has a mass of order a·σ·m_axion ~ 1e-29 eV, which is a fifth-force and rolling problem. That other stabilisation would also have to leave the axion potential alone.
- **What D1794 overstates.** "σ_dark ≈ 34–44 under every standard scaling" assumes a stabilisation that none of the listed schemes provides.
- **Fix.** State σ_dark as an input that needs an unspecified stabilisation mechanism, and label it C.

### D1793: inconsistent e^K and understated prefactor error · MINOR
- **The mismatch.** The derivation uses a single-modulus K, but the code plugs in e^K = 1/(2ReS 𝒱²) = 3.3e-10. The single-modulus value would be (2σ)⁻³ = 2.2e-6. That moves σ_Λ by +1.4, well beyond the locked ±0.37.
- **Stated ratio.** "Subleading by ~10^48" should read 1.8e46 (3W0e^{aσ}/(aσ) at σ = 20.57). Still huge, so harmless.
- **Stale inputs.** L8c used one-loop W0 (5.9e-9) and 𝒱 (4.2e4). With the D1801 values (1.4e-8, 1.0e5), σ_Λ = 38.49 and α_D is unchanged at 0.0218. The joint is fine, but it should be noted.

### D1795 → C1, C2, A6 locks: α_D = 0.022 has lost its derivation · MAJOR
- **The broken chain.** α_D = 1/(σ_dark + running) came from σ_Λ = 38.6, which was fixed by requiring V = ρ_Λ. D1795 withdraws exactly that identification (U19 withdrawn), so σ_dark = 38.6 no longer follows from anything.
- **What could rescue it.** It survives only if the dark U(1) cycle is the same cycle as the birefringence-axion cycle (σ_β window, which gives α_D 0.021–0.023). That is a postulate, and it leans on a ~3σ hint (β = 0.28°).
- **Hidden assumption.** Including the visible-style flux term 9/g_s would give α_D = 0.0186. The note silently assumes that the dark cycle has no flux part.
- **Fix.** "SIDM now fully passes (U4 upgraded)" and the α_D in C1, C2 and A6 should be labelled conditional on that postulate.

### D1797 / B10 vs D1800–D1801: the proton-decay joint was not propagated · MAJOR
- **Where it moved.** At the two-loop point (1.07e16 GeV, α⁻¹ = 27.94), the same scaling gives **τ(p → e⁺π⁰) ≈ 1.6e35 yr** (×3: 0.5–5e35), not 2.5–3.2e34. That is ×6.
- **Not listed.** D1801's "what moved" table leaves proton decay out.
- **The lock now contradicts itself.** PREREG_B10 branch G still predicts 0.8e34–1e35 and says "τ > 1e35 kills G". The updated estimate itself predicts τ > 1e35.
- **Fix.** Write a dated DEVIATION or re-lock for B10 before any Hyper-K result. Branch G is now "beyond or at the edge of Hyper-K", not "at Super-K's bound". The headline of D1797 is obsolete.

### D1800: error budget incomplete; "0.2 %" is wrong · MAJOR (budget) / MINOR (number)
- **Spectrum sensitivity.** α_s,unif depends on the Weave's own spectrum inputs, and the note does not quote this:
  - scalars 0.25 / 0.47 / 0.7 PeV give 0.1175 / 0.1158 / 0.1148;
  - gluino 4.8 / 7 / 20 TeV (the lock says "gluino ≳ 4.8 TeV") gives 0.1140 / 0.1158 / 0.1213;
  - wino 0.3–1.5 TeV moves it only ±0.0003.
- **Effect on the verdict.** With gluino 4.8 TeV plus the stated Yukawa shift (−0.002 to −0.004), |Δα_s| = 0.006–0.008. That straddles the locked CONSISTENT/TENSION boundary at 0.007. The verdict is formally per lock, but it is not robust.
- **The 0.2 % figure.** The title's "unifies to 0.2 % in α⁻¹" is wrong. |Δ₃|/α⁻¹ = 0.154/27.94 = **0.55 %**; in α_s(M_Z) the miss is 1.9 %.
- **"Cleanest quantitative success".** This is generic split-SUSY unification (label S). The note admits this; the headline should not claim more.

### D1801: "CLOSES" is close to automatic; χ = 50 "survives" uses an information-only window · MAJOR (overclaim)
- **Why it is near-automatic.** χ is a free integer in [2, 300] and N ∈ {6, 7, 8}. With M₂ ∝ W0/χ, almost any W0 finds a χ. Indeed χ moved 50 → 120 without the verdict changing. This is a consistency check with a fitted integer, not a test.
- **The χ = 50 claim.** "Old χ = 50 survives" uses the ×2 window, which DEVIATIONS D1 labels "for information only". The strict result is χ = 119–124.
- **Typo.** "M₂ = 8.24e4 GeV·(50/χ)·W₀/1.4e-8" should read 8.24e4 GeV/χ, i.e. 1.65 TeV·(50/χ)·(W₀/1.4e-8). The code is right.
- **Small joint mismatch.** The RG spectrum (D1799/D1800) uses wino 0.70 TeV, which is just outside the strict window 0.66–0.694 TeV. Negligible for the running, but it should be stated.

### D1802 / E3: wrong b₀ in the Λ_QCD sensitivity · MINOR
- **The issue.** The tool uses b₀ = 23/3 (n_f = 5). The carbon window concerns the low-energy (n_f = 3) Λ at fixed quark masses. Matching through the thresholds gives δlnΛ₃ = (b₅/b₃) δlnΛ₅ with δlnΛ₅ = 2π δα_s/(b₅α_s²). So δlnΛ₃ = 2π δα_s/(b₃α_s²), with b₃ = 9.
- **Correct values.** δ(m_q/Λ) = **11.0 %** (not 13 %), radius **4.4** (not 5.2), and the needed precision is **|δα_s| ≲ 5.0e-4** (not 4.2e-4).
- **Effect on the verdict.** None.

### D1792: "the Koide/Z₃ reading at ρ survives" is an overclaim · MAJOR
- **The test.** With the Y4 tensors (pair (0,0)) and 20000 random Higgs directions, Koide Q has percentiles 0.34 / 0.37 / 0.46 (1, 50, 99 %). Not one direction is within 1e-3 of 2/3.
- **What that means.** The Z₃ Yukawas at ρ do not enforce Q = 2/3. Q is fixed by the two fitted ratios, so the Y4b fit satisfies Koide only because it is fitted to data.
- **Fix.** "Survives" must become "is not excluded, and is not produced by this sector". The B1 forecast (m_τ = 1776.969 MeV from Q = 2/3) rests on D1776, not on the orbifold Yukawas. Its status should say so.
- **Also.** "Fit any two mass ratios" is extrapolated from two targets (leptons and down quarks). Say "fit both tested target pairs".

### D1791 / D1792: the control does not discriminate · MINOR
- "The down-quark control is hit exactly (so the code is sound)" overclaims. A 5–6 complex-parameter optimiser on arbitrary 3×3×k tensors would hit any two ratios. The control shows the optimiser works; it does not show the physics code is right. The real validation is the gate residuals and the Z₃ multiplicities, and those are fine.

### D1790 · MINOR
- Best r₂₃ = 0.196 (×3.3), not "≥ 0.20 (×3.4)". This is near the ×3 threshold, so "near-democratic" is a slight exaggeration for the best direction (the medians are democratic).
- The verdict wording was corrected by D1792 (OK).

### D1798 / A9 · MINOR
- **What the SL(2,Z) statement covers.** It is correct only where the duality is a gauge redundancy of the full background. Fluxes and orbifolds usually break SL(2,Z) to a subgroup (Γ(N), or flux-preserving subgroups). Images under the broken cosets are then physically distinct vacua.
- **Where the reason really lies.** The operative reason for "no walls" is that one pre-inflationary patch settles in one minimum (plus the residual Z₃ at ρ being unbroken). The argument covers only modular-moduli walls. Axion walls (N_DW > 1) are absent for a different reason (PQ broken before inflation), and the note should say so.
- **Template simplifications.** The tool fixes b = c = 1, whereas NANOGrav marginalises b ∈ [0.5, 1] and c ∈ [0.3, 3]. _gstar jumps 17 → 62 between 150 and 200 MeV, which is coarse compared with lattice g*(T). Both are labelled approximate.
- **Wording.** "Has a reason, not just an estimate" should read "has a heuristic argument".

### B8/B9 EDM (weave_edm) · MINOR
- The one-loop scaling ∝ 1/m̃² misses the two-loop Barr–Zee chargino term, which dominates in split SUSY. Here μ is at the PeV scale, so it is also ~1e-33 and the prediction stands. The tool should mention it.

### A4 lock · MINOR
- The Maldacena (5/12)(1 − n_s) is removed by the consistency relation (a coordinate effect; Pajer–Schmidt–Zaldarriaga 2013), so the physical local f_NL is ≈ 0.
- (5/12)(1 − 0.965) = 0.0146; the value 0.012 needs n_s ≈ 0.971.
- The FAIL rule is unaffected.

### Integrity · MINOR (no breach found)
- **Order is right.** Every lock precedes its result in git. Y4 D1 was committed before the rerun (the result came 19 s later). The U20 D1 commit contains only the run-1 BROKEN JSON, so it came before the rerun. No threshold was loosened.
- **Run-1 code not preserved.** The U20 deviation flipped BROKEN → CLOSES through a post-hoc window definition. It is documented and reasonable (a zero-width window is an artefact). But the run-1 script was never committed (u20_chain.py first appears with D1801), so "artefact" cannot be audited.
- **Code not frozen at lock time.** Tool code is committed together with its result, 20–40 s after the lock (B11, B11b, E3, A9). Locks do not record a code hash, so git cannot show that the code was not run before the lock. Recommendation: commit the tool, or its sha256, inside the lock commit.
- **Timestamps.** The DEVIATIONS times in the text ("10:35" for U20, "10:27" for C1) are later than their commit times (10:31:58, 10:24:03 CT). Fix the clock or the labels.
- **Commit message.** "D1792 draft + Y4b script (run finishing)" is misleading: the full result JSON is in that commit. The rerun reproduces it exactly.

### Joints
| quantity | stated | check | status |
|---|---|---|---|
| α_D | 0.022 | 0.0218 (0.0186 if the dark cycle carries 9/g_s) | OK, but provenance is broken (see the α_D finding) |
| Re T_dark | 38.6 | 38.63 (one-loop W0, 𝒱); 38.49 (two-loop) | MINOR stale |
| α⁻¹ | 27.9 | 27.935 | OK |
| χ | ≈ 120 | 119–124 | OK |
| W0 | 1.4e-8 | 1.402e-8 | OK |
| T_R | 3.7e8 | 3.74e8 | OK |
| τ_p | 2.5–3.2e34 | 1.6e35 at the two-loop point | MAJOR (proton-decay finding) |
| wino | 0.70 TeV (RG input) | strict window 0.66–0.694 TeV | MINOR |

## 2. Overall verdict

- **No FATAL errors.**
- **The arithmetic reproduces exactly**, and the lock discipline holds: no threshold was loosened and no result was chased.
- **The headline verdicts stand:** Y4 FAIL, Y4b/Y5 HOSTED, L8c SHIFTED, D1795 FAIL, B11b CONSISTENT, U20 CLOSES.
- **But several stated numbers or readings are wrong or over-stated:**
  - one systematic normalisation error (the axion f, ×4.44);
  - one unpropagated joint that makes a live forecast lock self-contradictory (B10 proton decay, ×6);
  - an under-stated error budget on the "cleanest success" (α_s);
  - three overclaims: Koide "survives", the near-automatic chain closure, and α_D still treated as derived after U19 was withdrawn;
  - one unaddressed physics consistency problem: the dark-cycle saxion stabilisation.

## 3. Required fixes

1. Correct f = √(3/2)/(2πσ) M_P everywhere (D1760, D1793, D1794, D1795, line 17341). Restate σ_β = 36.9–40.6, m/H0 = 282, the energy share at 1e-33 eV = 5.8e-6 and the cap m ≲ 4e-31 eV.
2. Re-lock or add a DEVIATION for B10 at the two-loop point: τ(p → e⁺π⁰) ≈ 1.6e35 yr (0.5–5e35). Update D1797's headline and add proton decay to D1801's "what moved" table.
3. D1800: quote the spectrum sensitivity (α_s,unif = 0.114–0.121 over gluino 4.8–20 TeV; 0.1148–0.1175 over scalars), and say the CONSISTENT verdict is marginal at the gluino lower edge. Replace "0.2 % in α⁻¹" with 0.55 % (or 1.9 % in α_s).
4. D1795, C1, C2, A6: label α_D = 0.022 and "SIDM fully passes" as conditional on the postulate that the dark-gauge cycle is the photon-axion cycle. State the no-flux-term assumption (otherwise α_D = 0.0186).
5. D1793/D1794: state that σ_dark ≈ 38.6 is not a KKLT or LVS minimum of its own instanton. A separate saxion stabilisation is needed (label C), and "under every standard scaling" should be softened.
6. D1792: replace "Koide/Z₃ reading survives" with "not excluded, not produced". Random Higgs directions give Q ≈ 0.37, never 2/3. Note in B1 that the Koide forecast rests on D1776 alone.
7. D1801: call CLOSES a consistency check with a fitted integer χ. Drop "χ = 50 survives" (it uses an information-only window), and fix the M₂ prefactor typo.
8. weave_nuclear / D1802: use b₀ = 9 (n_f = 3) for low-energy Λ at fixed m_q. The results become 11 %, radius 4.4 and |δα_s| ≲ 5e-4.
9. D1793: record the e^K model choice. The single-modulus e^K would shift σ_Λ by +1.4, outside the locked ±0.37. Correct "10^48" to 1.8e46, and note σ_Λ = 38.49 with the two-loop W0 and 𝒱.
10. D1798/A9: restrict the SL(2,Z) argument to an unbroken duality group, name pre-inflationary selection as the operative reason, and mention axion walls separately.
11. D1790: best r₂₃ = 0.196 (×3.3). D1791/D1792: drop "so the code is sound" for the optimiser control.
12. Process: commit the tool code, or its hash, in the lock commit. Correct the DEVIATIONS time labels. Preserve run-1 scripts whenever a DEVIATION changes a verdict.
13. Minor: A4 f_NL ≈ 0 observable (consistency relation) and 0.0146 at n_s = 0.965; mention the two-loop Barr–Zee term in weave_edm.
