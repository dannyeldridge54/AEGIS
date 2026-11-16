# Accuracy queue (Jl accuracy track; top open item first). Status: open / in progress / done (D###) / retired (D###)

1. [done D807] Referee merge: papers/v3/REFEREE_v3.1_round7_independent.md (agent running since 06:17 CT). Fix valid items via correction notes; add the D806 qualifier (the α_s leg is beyond 2030s reach) to the title/abstract framing. Rebuild. (A0)
1b. [done D808] Referee deferrals: split the ~900-word SERAPIS-E paragraph (minor 10); covariant m₃/₂ window to match wino 0.67–1.85 TeV; extend tab:repro beyond D639 or point to MANIFEST.md; τ = i Σm_ν range 0.059–0.064 clause (minor 9).
2. [done D808] Map hygiene: wino_window title is stale (says 0.67–0.80 TeV, ~15%; current 0.67–1.85 TeV thermal, D784). Fix the map title only (no physics).
3. [done D809] gravitino_wino (estimate) → compute the gravitino→wino yield with the current T_R and m₃/₂ windows, locked. (A1)
4. [done D810] D796 orbit-charge coefficient: the estimate gives ~9Δx, the D790 simulation ~2Δx. Compute η/Δx from the D790 code at 3 small offsets, locked, and settle which is right. (A1)
5. [done D811] D802 additive remnant: compute the no-scale-breaking curvature term at i explicitly (the covariant-completion W₀), locked. (A1)
6. [done D812] Exactness audit: list every n_s/r/α_s in serapis_v3.tex with its source (exact MS / frozen pipeline / slow roll). Recompute any paper number that is slow-roll only, exactly. (A2)
6a. [done D813–D817] MS recomputation: done for D725, D729 (+interpolation), D613 consistency, D722 method; one per tick, locked, via spectra() from exact_ns_d588.py.
6b. [done D820] Literature check: LiteBIRD/SO forecast σ(r) for r ≈ 5e-4 (paper says ~1e-4 needed, beyond plans; sheet says 5e-5 optimistic). Fix whichever is wrong.
7. [done D821] Error budget for the frozen τ = i band and SERAPIS-E band: N* (reheating range), exact vs SR, parameter window, convention. Table in the prediction sheet. (A3)
8. [done D822] Prune: logderiv_plateau (no string source, D760) → retire unless a unique prediction is found; SERAPIS-Δ (D800, disfavoured) → record as retired. (A4)
9. [done D823] eps_tilt at τ = i: state that it is fitted; check whether a BHK-type tilt can exist on the τ = i branch (D802 says multiplicative, so no vacuum mass, but a tilt?). Derive or record "not derivable". (A1)
10. [deep, needs Danny's OK] P3 anti-D3 annulus computation.
Not derivable (tests only): P1 CP phases (DUNE/Hyper-K), halo_profile (astrophysics).

## Round 2 (added 16 Nov 2026 after D823; the round-1 queue is done except item 10)
11. [done D824] Σm_ν: check the frozen 0.0587 eV and the τ = i range 0.059–0.064 eV against the newest DESI/Euclid bounds (2026). If the bound has tightened below 0.059, record the falsification status honestly. (A1/L1)
12. [done D825] Ladder flags: clear any open rechecks with a one-line justification each.
13. [done D825] Cross-document consistency sweep: README, prediction_sheet, CURRENT_STATE, MANIFEST and the v3.1 paper must quote the same frozen numbers, DOIs and windows. List and fix mismatches outside the published paper; paper fixes go to V32_TODO. (A0)
14. [done D826] The τ = i vacuum-mass source: the ε I₁ term is the only mass term. List the candidate loop sources (D685–D687, D802) and state in one D-note which remain open. Derivation only.
15. [done D827] MANIFEST.md: make sure every PREREG from D759–D823 is listed with its sha256 and result file (the referee's minor 11).

## P3 DEEP PROJECT (approved by Danny 16 Nov 2026, 08:13 CT: "Start P3")
Goal: decide from a string computation whether the anti-D3 (nilpotent goldstino) sector's τ-dependence can give K^{XX̄} = a − b/E(τ,2) (P3), and whether a log correction (D686) supplies the τ = i tilt and mass.
Steps (one per tick; lock before any computation; honest labels):
- P3.1 [done D828] Literature: one-loop open-string vacuum amplitudes (annulus/Möbius) for D3/anti-D3/O3 systems on T⁶/(Z₂×Z₂) or T²-factorised orientifolds; brane supersymmetry breaking (Sugimoto; Antoniadis–Dudas–Sagnotti; Angelantonj–Sagnotti review). How does the vacuum energy (or goldstino metric) depend on the complex structure U? Which lattice sums appear (E(U,s), with characters for brane positions)?
- P3.2 [done D829] Set up the anti-D3 + D3/O3 annulus + Möbius amplitude for our configuration (5/5/5 + 1 stuck D3s; anti-D3 at a fixed point). Write the U-dependence as lattice sums with characters (as BHK, D689). Derive its sign and its large-y behaviour.
- P3.3 [done D830] Placement: does it enter V additively (Casimir-like), multiply V, or renormalise K_XX̄? Compare with the required a − b/E form (D797).
- P3.4 [done D831] Compute it numerically (locked) and compare its shape with 1 − E(ρ)/E(τ) and with the τ = i εI₁ log form.
- P3.5 [done D832] Verdict on P3 (retire / keep / replace), with a paper note for v3.2.

## κ deep project (anti-D3 term normalisation; started 2026-11-16 on Danny's choice)
- K.1 [done D833] Fix κ: anti-D3–D3 force normalisation (T₃², string-frame → Einstein-frame, Vol₄, g_s) in the same units as the SERAPIS-E plateau V0 (D689 conventions).
- K.2 [done D833; bound SUPERSEDED by D835: v₄ ≳ 2e4 g_s] Locked numerics: κ/V0 for the D696/D830 moduli (Im S·Im ρ ≈ 560–975) vs the slope bound 2.9e-3/y* (D831).
- K.3 [done D834: saddle, tachyonic along x] τ = i vacuum mass from the anti-D3 term vs the needed m²/H² ≈ 2e-3 (D826).
- K.4 [done D835: NOT harmless; k ≲ 2e-6 needed] Decompactification wall: does it bound V at large y without spoiling the band?
- K.5 [done D836] Verdict and v3.2 note.

## Warped-throat project (P3 route a; started 2026-11-16 on Danny's choice)
- W.1 [done D837] Literature: anti-D3 at the tip of a KS throat in a compact torus orientifold; how the warp factor e^{4A₀} and the uplift depend on the bulk complex structure U (throat moduli vs bulk moduli; 1707.07059, KKLMMT, Bena et al., Gautason et al.).
- W.2 [done D838: cannot give the power-law plateau] Derive the U-dependence of the warped uplift V_up = 2T₃e^{4A₀(U)}/(...) for our configuration; additive or inverted (1/E) form?
- W.3 [skipped: moot after D838] Warped κ: interaction vs tension in the throat (redo D833's ratio with warping).
- W.4 [skipped: moot after D838] Locked numerics if W.2 gives a candidate; compare with V0[1 − E(ρ)/E(τ)].
- W.5 [done D839] Verdict and v3.2 note.

## τ = i verdict project (started 2026-11-16 on Danny's choice)
- T.1 [done D840 (+ D834a)] Collect every τ = i strike and support (D795, D802, D811, D815, D823, D826, D834) into one table; check each against its source note.
- T.2 [done D841: keep as conditional variant] Decide by a stated rule, written before deciding (retire / keep as conditional / keep): the rule must not depend on new data.
- T.3 [done D842] Consequences: frozen τ = i predictions stay frozen (never change); paper wording for v3.2; MANIFEST and prediction sheet.

## P1 deep project (CP phases; started 2026-11-16 on Danny's choice)
- C.1 [done D843] Literature: CP phases in string orientifold flavour models at CP-conserving τ (ρ, i): sources from Kähler moduli, axion-dilaton S, Wilson lines/brane positions, twisted sectors; status of gCP in Type IIB orientifolds (is gCP generic or not?).
- C.2 [done D844: no spontaneous CP source as specified] For our configuration (D696/D830: stacks (5, 2), anti-D3?, BHK), list which fields can carry a phase: Im S axion, Kähler axions Re ρ_i, Wilson-line/position moduli of the stacks. Derive whether any is CP-odd at its vacuum.
- C.3 [done D845: CP-odd racetrack minima exist (90% of scan)] If a source exists: compute (locked) the induced leptogenesis phase δ and compare with P1's uniform prior.
- C.4 [done D846: P1 → P1′] Verdict (derive / keep / replace P1) and v3.2 note.

## v3.2 draft (started 2026-11-16 on Danny's choice; NO Zenodo upload without his word)
- V.1 [done D847] Copy papers/v3/serapis_v3.tex (v3.1, published) to papers/v3/serapis_v3.2_draft.tex; apply V32_TODO items D822–D826 (accuracy-track edits).
- V.2 [done D848] Apply V32_TODO items D830, D832, D836, D839 (P3, tadpole), D841 (τ = i conditional), D846 (P1′).
- V.3 [done D849] Build the PDF, check page count and overfull boxes, grep every changed number against its D-note; write CHANGELOG_v3.2.md.
- V.4 [done D850] Independent referee pass on the diff only; report to Danny with the PDF.

## P1′ follow-up (queued 2026-11-16 after v3.2 draft; draft held, "Not yet" on Zenodo)
- Q.1 [done D851: θ₁ generic; 41% deepest CP-odd] Distribution of the axion vev over CP-odd racetrack minima (D845 rerun with fixed seeds is NOT allowed; new lock): fraction with |sin(2π⟨Re T⟩/L·k)| > 0.1 for the phase that enters the heavy-ν couplings.
- Q.2 [done D852: two-sector condition; 80% generic] How the heavy-ν couplings depend on T (Kähler normalisation vs holomorphic), and the resulting leptogenesis phase δ.
- Q.3 [done D853] Verdict: does P1′ reproduce the D762/D763 pass fractions?

## τ = i phase map (queued 2026-11-16 on Danny's choice)
- R.1 [done D854: ε = 0 at τ = i under single-modulus P1′] Redo D763's τ = i radiative leptogenesis pass fraction with the complex-R phases drawn from P1′ (instanton phase Δ = 2πΔn⟨Re T⟩, D852 distribution) instead of uniform; locked run on the D745/D763 set-up; compare 68–71%.
- V.5 [done D856] D854/D855 folded into the draft.

## Moduli-consistency deep project (planned 2026-11-16, "Plan next deep jl")
Why: today's results each demand values of the same moduli (g_s, Im ρ₁, Im ρ₂, Im ρ₃, v₄) from different places. Nobody has checked they can hold at once. A conflict here would be a real internal inconsistency (rule R2 of D841); agreement would turn several estimates into one consistent point.
- M.1 [done D857: conflicts A, B flagged] Requirements table: every constraint on (g_s, Im S, Im ρ_i, v₄ = Im ρ₂·Im ρ₃ in string units, M_s) from D689/D696 (BHK tilt: Im S·Im ρ₁ ≈ 560–975 with stacks (5,2)), D833/D835 (anti-D3 safe: v₄ ≳ 2e4 g_s), D845/D851 (racetrack CP-odd minima at t ≈ 10 in units of e^{2πiT/N}), D852/D854 (heavy-ν masses M ≈ 1e11–1e13 GeV from e^{−2πn Im T}·M_s; two cycle classes at τ = i), D783 (Λ, M_s ≈ 6e15–3e16 GeV), D692 (T_R, N*). Derivation; normalisations checked between notes (Kähler conventions differ: K = −3 ln vs −Σ ln ρ_i).
- M.2 [done D859: twisted escape closed; fractional instantons, no-anti-D3 open] Map each requirement onto the three untwisted Kähler moduli of T⁶/(Z₂×Z₂): which ρ_i is the inflaton torus's, which carry the racetrack(s) and instantons, which make up v₄.
- M.3 [done D860: anti-D3 on → inconsistent; off → only at string-size tori] Locked feasibility scan: is there a common point satisfying all M.1 constraints (with ranges)? Report the allowed region or the first conflict.
- M.4 [done D861] If allowed: one benchmark point (all moduli values) with every derived quantity recomputed from it; if not: which constraint must give, and what that does to the frozen predictions (they never change; the variant would).
- M.5 [done D861: τ = i conditional, R2 not met] Verdict, status/postulate updates, v3.2 note.
- V.6 [done D858] Full independent referee; ten majors fixed, twelve minors deferred.
- V.7 [done] D861 folded into the draft τ = i bullet; rebuilt clean.
- α′ control [done D862]: leading corrections sub-percent at the benchmark; consistent P1′ region is a thin sliver near the string scale; loop corrections to T₁'s K (≈ 1/(Im S·Im T₁) ≈ 0.5) open.
- Loop correction to T₁ [done D863]: CP-odd racetrack minima survive even ×100; D862's weak-point estimate withdrawn (D862a).
- D7 tadpole [done D864: allowed with conditions; D7 stacks feed the tilt]. Next: D865 compute the D7 contribution to C (BHK D7 normalisation) and re-fit the benchmark.
- D7 tilt [done D865 (+D864a)]: both stacks at the origin; N_eff reduced by 0.6–2.5; benchmark A₁ ≈ 16–35. Open: BHK D7 coefficient r.
- BHK D7 coefficient [done D866]: D7 term position-independent, ∝ E(U₁,2)/(Im T₂ Im T₃); D689's ρ is the T⁴ modulus (D857a). Next: corrected M.3 scan (D867).
- Corrected scan [done D867 + D861a]: anti-D3 incompatible with SERAPIS-E's BHK tilt (g_s ≥ 3.1 needed); BHK + P1′ was a cross-branch combination.
- Uplift alternatives [done D868]: rank 1 distant sequestered anti-D3, rank 2 T-brane on T⁴ cycle. Next: residual U₁ coupling of a throat anti-D3 vs k ≲ 2e-6 (D869).
- Throat anti-D3 [done D869]: sequestered (k ≲ 1e-8). Next: D870 P3 wording 'uplift sector' in POSTULATES/status/draft.
- P3 wording [done D870]. Next: deferred referee minors batch 1 (D871).
- Referee minors batch 1 [done D871]. Next: batch 2 (#1, #2, #12, #14, #15) as D872.
- Referee minors batch 2 [done D872]; all referee items handled.
- D7 tilt piece [done D873]: ≤ 0.11q at A₁ = 1, negligible for A₁ ≳ 3.

## ρ-baryogenesis deep project (picked 2026-11-16 as the top open item, autonomous mode)
Why: the better-motivated vacuum ρ has no baryogenesis mechanism inside its frozen band (residual Z₃ makes the inflaton's decay products long-lived; D780, D789, D792); the only consistent history is post hoc and just outside the band.
- B.1 [done D875] Inventory: every ρ route tried (D725, D731, D780–D793) and why each failed or left the band; list the Z₃ selection rules that bind.
- B.2 [done D876: top = suppressed AD-charge transfer] Literature: baryogenesis mechanisms compatible with an exact discrete symmetry and a long-lived Z₃-charged state (e.g. late-decay baryogenesis through dim-6 operators, spontaneous baryogenesis from a rolling axion, Z₃-allowed Affleck–Dine directions, gravitational/thermal leptogenesis at low T_R).
- B.3 [done D877: needs b = 1/3 to 0.005–0.4%; tuning unless symmetric] Pick the best candidate; locked computation of Y_B and of its effect on N* (does it stay inside the frozen band?).
- B.4 [done D879: LH_u AD candidate at ρ found] Verdict and v3.2 note.
- B.3b [done D878: needs tuning]. Next: B.4 verdict (D879) and choose rank 2 or 3 as follow-up.
- B.5 [done D880: FITS, m_ν₁ ≈ 4e-9–7e-8 eV] Locked LH_u AD computation at ρ (T₂ = 1e5–1e6 GeV, m_ν₁, soft masses; ρ lepton-sector compatibility).
- B.6 [done D881] Fold D880 into status, POSTULATES (none new), and the v3.2 draft (abstract + Sec. VII ρ baryogenesis statement; label post hoc).
- B.7 [done D882: structure exists (E₄-protected); fit open] Realistic ρ lepton sector with m_ν₁ ≈ 4e-9–7e-8 eV (beyond the weight-two doublet alone).
- B.8 [done D883: natural, 3.5%, ε ≈ 2e-3] Locked oscillation fit at ρ: Γ₂-singlet leptons + N_Y + S₁ + S₂(weight-4, ∝E₄) + small lift; NO splittings and m_ν₁ ≈ 1e-8 eV.

## ε-origin deep project (τ = i; picked 2026-11-16 under the autonomy rule)
- E.1 [done D885: target = |j−1728|^{~1e-5} from a throat cutoff] Reverse path: from the required εI₁ term (m²/H² ≈ 2e-3 at i, ε ≈ 1.40–1.45e-4) write the needed term's form in K or W and its modular weight; list every route tried (D576–D618, D684–D687, D823, D826, D834) with the factor it missed by.
- E.2 [done D886: negative] Literature: threshold/one-loop corrections that are logarithmic in |j − 1728| or vanish quadratically at i (Harvey–Moore, DKL with Wilson lines, species scale at enhanced-symmetry points).
- E.3 [skipped: no candidate after D886] Locked computation of the best candidate's ε.
- E.4 [done D887: closed negative, ε fitted] Verdict and v3.2 note.

## ρ-lift project L (picked 2026-11-16 under the autonomy rule)
- L.1 [done D888: instanton Im T/N≈1 or Λ≈M_GUT alive; displacement and loops closed] Reverse path: from D883's lift ε ≈ 1.8e-3 of the E₄-protected S₂ mass, write the needed term (weight, field content) and its size in units of natural scales (Λ/M_P, one-loop, instanton e^{-2π Im T/N}).
- L.2 [done D889: ε = residual-Z₃ breaking |u|≈2e-3, no in-model source; D888a corrects D888] Literature: lifting of E₄(ρ)=0 zeros (Planck-suppressed operators, non-holomorphic Kähler corrections, weight-shift terms).
- L.3 [skipped: no candidate] Locked computation if a candidate exists.
- L.4 [done D890: closed negative; draft updated] Verdict and v3.2 note.

## ρ-lift project L (picked 2026-11-16 under the autonomy rule)
- L.1 [done D888: instanton Im T/N≈1 or Λ≈M_GUT alive; displacement and loops closed] Reverse path: from D883's lift ε ≈ 1.8e-3 of the E₄-protected S₂ mass, write the needed term (weight, field content) and its size in natural units (Λ/M_P, one-loop, instanton e^{-2π Im T/N}).
- L.2 [done D889: ε = residual-Z₃ breaking |u|≈2e-3, no in-model source; D888a corrects D888] Literature: lifting of E₄(ρ)=0 zeros (Planck-suppressed operators, non-holomorphic Kähler corrections, weight-shift terms).
- L.3 [skipped: no candidate] Locked computation if a candidate exists.
- L.4 [done D890: closed negative; draft updated] Verdict and v3.2 note.

## Weinberg-bound project W2 (picked 2026-11-16 under the autonomy rule; D882 point 4)
- W2.1 [done D891: not protected; c ≲ 1e-3 (M_P) or ≲ 1e-5 (M_s)] Selection rule: at ρ, does the residual Z₃ (charges q_L = −q_H, q_{H_u} ≠ 0 per D783) forbid the Planck-suppressed (LH_u)²/M_P entry along the lightest direction, or only allow it ∝ E₄? Derivation from the notes.
- W2.2 [done D892: instanton-only Weinberg term (perturbative lepton number) natural for M_N ≲ 1e12 GeV]
- W2.3 [done D893: conditional pass (perturbative lepton number); draft updated] Verdict and v3.2 note.

## Referee pass R2 (picked 2026-11-16 under the autonomy rule)
- R2.1 [done D894: 1 major (two AD yields differ ×49 in m_ν₁), 4 minors; REFEREE_v3.2_R2.md]
- R2.2a [done D895 + D880a: ρ AD window 2e-11–9e-10 eV; D880 corrected ×~100]
- R2.2b [done D896: ε ≈ 1.6e-4, natural at lower edge]
- R2.2c [done D897–D898: Weinberg redone, draft and sheet updated, R2 closed]

## Full referee pass R3 (picked 2026-11-16 under the autonomy rule)
- R3.1 [done D899: 1 major (τ = i AD window at old T_R), 3 minors; REFEREE_v3.2_R3.md]
- R3.2 [done D900–D901: τ = i AD window at corrected T_R; R3 closed]

## Data check DC (picked 2026-11-16 under the autonomy rule)
- DC.1 [done D902: one zero-prior Σm_ν bound below the NO floor (2606.17994); wino and n_s unchanged]

## Weinberg at τ = i project W3 (picked 2026-11-16 under the autonomy rule)
- W3.1 [done D903: AD at τ = i conditional (instanton-only Weinberg; light seesaw direction missing in minimal texture); draft sentence added]

## Lepton-number origin project W4 (picked 2026-11-16 under the autonomy rule)
- W4.1 [done D904: E(-1) action 2π/g_s ≈ 13–27 meets the bound for g_s ≲ 0.33–0.48; quiver charges not derived; W4 closed at estimate level; D904a: possible at ρ (g_s free), marginal at τ = i (racetrack g_s 0.4–0.5 → S 12.6–15.7 vs 13–17)]

## v3.2 readiness check RD (picked 2026-11-16 under the autonomy rule; no Zenodo action)
- RD.1 [done D907: ready; manifest and changelog gaps fixed; decision with Danny]

## τ = i light-direction project N1 (picked 2026-11-16 under the autonomy rule)
- N1.1 [done D909: possible with a heavy Dirac pair (S, S′) plus a post hoc lift; no fit run (would repeat D883/D896); N1 closed]

## P3 lead (queued 2026-11-16, D910)
- P3.L1 [done D911: LEAD: Eisenstein term in K gives 1/E approach; pure −log E(τ,2) ghost at fixed points; mixture k > 2c, k + 2c = 2 untested]
- P3.K1 [done D912 + D911a: FAILS (η factor makes e^G grow exponentially; ρ a maximum); P3.K route closed]

## Reproducibility project RP (planned 2026-11-16 13:35 CT on Danny's "Pl")
- RP.1 [done D913: 22/22 reproduce]
- RP.2 [done D913: README lacked v3.2 rows]
- RP.3 [done D913: rows added in repo; no v3.2.1 needed]

## Memory-claim audit M (started 2026-11-16, D915)
- M.1 [done D915: D780 gauge-symmetry claim supported; D914 flux-norm structure supported]
- M.2 [done D916 + D657a: D657 corrected (proton hexality exists, Z₆); CMB-S4 cancellation confirmed; v3.3 draft opened with the fix]
- M.3 [done D917: GS term is log(T+T̄) in K, η only in f; D754 lead weakened; no published text affected]
- M.4 [done D918: D771 confirmed; D752 unused, estimate; audit M closed]

## Project F: a flux-and-loop origin for SERAPIS (queued 16 Nov 2026, after D925–D934)
Goal: replace postulate P3 (the Ê/(Ê+1) plateau) and the bare "U rolls" assumption with a chain computed from a T⁶/(Z₂×Z₂) flux vacuum: fluxes fix S, U₁, U₂ and leave U₃ flat (D933–D934); one-loop (BHK) and α′/instanton terms lift U₃; the lift's shape is computed, not postulated.
Stages (each locked before computing; one D-note each):
- F1 flux vacuum: D934 result. If PASS, take the smallest-|N_flux| solution; if FAIL on grid, extend the grid once (ρ points, Q(√3)) via a new lock. Kill: no solution with ρ points either → record "no flat single U in T⁶/(Z₂×Z₂) at small flux", project stops at F1.
- F2 masses: compute the U₁, U₂, S masses and the Kähler-moduli stabilisation scale at that vacuum; check H_inf < every fixed mass (else they roll too). Kill: any fixed modulus lighter than H_inf.
- F3 the lift: write the full one-loop V(U₃) for that vacuum (BHK KK + winding terms, E(U₃,2) and E(U₃·…) pieces with their actual coefficients from the D-brane/O-plane content), plus the leading α′ term. Compare its shape with Ê/(Ê+1)(1+CÊ). Pass: same plateau index p = 2√2 and an approach within 10% of P3 over the observable e-folds. Kill: a different p (then SERAPIS becomes a sibling, D928/D932).
- F4 predictions: if F3 passes, n_s, r, α_s from the computed V (exact Mukhanov–Sasaki), scored only against FUTURE data; compare with the frozen SERAPIS numbers (frozen predictions never change).
- F5 write-up: a standalone paper ("a flux vacuum with one flat torus modulus and its loop-lifted plateau"), posted on Zenodo when Danny says so.
Side product (any outcome): a sibling catalogue (α = 1, 1/3, 1/6, 1/24 from D928/D932) with consistency-relation predictions (D669 with each p).
Cost: about 6–10 ticks; one locked script per stage; no subagents.
