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
- V.4 [open] Independent referee pass on the diff only; report to Danny with the PDF.
