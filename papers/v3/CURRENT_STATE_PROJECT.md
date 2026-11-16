# AEGIS: current state (16 Nov 2026, 04:05 CT). Read before working.

## Active line: SERAPIS v3 / v3.1 (modular inflation)
- Paper: v3.1 PUBLISHED 16 Nov 2026, DOI 10.5281/zenodo.24281771 (v3: 24250733). Source papers/v3/serapis_v3.tex.
- Repo: github.com/dannyeldridge54/AEGIS, branch `unify-bg`. D-notes: theory/pending_docs/D72_D75_weak_spots.md (to D736; next number in NEXT_D.txt). Locks: field_tests/rules/PREREG_D*.
- Frozen SERAPIS (τ = i, ρ): n_s 0.970–0.975, r (4.6–5.7)e-4, α_s −(8.5–9.9)e-4, β_s −(3.0–4.6)e-5; caps n_s ≤ 0.985, r ≤ 8.3e-4; strip D679/D681. Prediction sheet: papers/v3/prediction_sheet.md.
- SERAPIS-E (loop-motivated branch, lock D693, frozen after the data): V = V0[1 − E(ρ,2)/E(τ,2)](1 + CÊ), Ê = E(τ,2) − E(ρ,2); tilt from Berg–Haack–Körs one-loop Kähler correction (hep-th/0508043). n_s 0.970–0.975, r (4.55–5.12)e-4, α_s −(9.4–10.6)e-4; m_φ ≈ 2.2e13 GeV; N* 48.4–49.9.
- Microscopic picture: stuck D3 branes at the three half-periods (no moduli, no twisted charge; Maiden–Shiu–Stefański); tadpole: 5/5/5 + 1 at origin; tilt = fixed-point asymmetry; Im S·Im ρ ≈ 375–1220 (natural). Plateau interior form irrelevant (D698).
- Epstein plateau r-ladder (D700–D702): e = 2 → r ≈ 4.7e-4; e = 2.5 → 3.4e-4; e = 3 → 2.5e-4. Casimir route needs negative codim-2 tension — obstructed in string settings (D703).
- Research front (D706): species-scale/Laplacian swampland may supply the 1/E(τ,2) term (next step); competitor 2607.00528 (r ~ 1e-5, n_s ≈ 0.961); flavour models near ω/ρ (2512.24804).
- Multi-scale test run (D710, Fig. 6): n_s consistent in every release (≤1.33σ from band); Σm_ν 0.0587 passes DESI DR2 <0.0642; nulls hold (μ, f_NL, PBH, PTA/LISA GW, 0νββ); Lyα: eBOSS-only tension (6–7σ) NOT seen in DESI DR1 P1D (<0.8σ, D711); S8, N_eff consistent. Paper now 13 pp.
- Reheating revision (D719–D736, 15 Nov evening):
  - τ = i: the inflaton is NOT sterile. The Γ2 doublet's opposite-sign masses give an axion-like coupling (D727, two methods agree to 1e-10), so T_R ≈ 1–3e6 GeV, not 1e3–1e5. The stiff phase is physical (D730).
  - The corrected Chronos history meets the frozen band only for ε ≈ 1.40–1.46e-4 (n_s ≈ 0.974–0.975). The frozen band is kept as locked.
  - Leptogenesis from inflaton decay at i now PASSES (D728). AD is optional.
- SERAPIS-E at ρ (D720–D735):
  - The doublet-only N sector is KILLED by dark radiation (massless N2, D723).
  - Viable with a 2⊕1 sector mixing through the weight-2 doublet (D724). T_R 3e8–3e9 GeV, N* 49.7–50.5, n_s 0.9732–0.9739, r 4.6–4.7e-4, inside frozen bands (D725).
  - Leptogenesis passes (D731). Gravitino→wino plus gamma rays favour M_H ~ 1e12, T_R ~ 3e8 (D732–D733).
  - Post-hoc wino prediction: 0.67–1.85 TeV thermal, 5–41% of DM (D784, superseding D735's 0.67–0.80). ATLAS 2603.08315 excludes < 670 GeV; HL-LHC reaches ~1 TeV (D736).
  - Open: digitised wino sub-fraction limits (2507.15934 Fig. 6); N splitting/CP phases from a flavour model.
- Jl learning loop (22:30 on; D758–D769). Mirror-of-SERAPIS loop: forward/reverse sides, functions L1–L10, checks K1–K8, balances β1–β5. Plan in docs/UPDATE_LADDER_PLAN.md; checker tools/loop/jl_check.py; logs in theory/derivations/ (DERIVATION_LOG, LESSONS, POSTULATES).
  - D759: log-derivative Epstein plateau is a post-hoc CANDIDATE (n_s band at C 5–10e-7, r 2.1–3.1e-4). D760: no string coupling makes the species scale track E(τ,2), so it stays phenomenological.
  - D762–D763: both vacua and the inflaton line are CP-conserving, so leptogenesis on both branches needs high-energy CP phases. Under gCP there is no leptogenesis and δ_CP ∈ {0, π}. Leptonic CP violation discovered ⇒ gCP excluded.
  - D764–D772: postulate P2 (retired D772: the published flux model also ties τ₃ = S, no free inflaton) — then P4 (pure-NS flux) also retired D773: no untwisted flux vacuum leaves the inflaton torus free, so CP phases are explicit (P1 reopened). Earlier P2 notes: = CP from a second modulus via the flux relation U₂U₃ = b₃/a⁰ with U₂ = ω (2405.18813). With the inflaton in the relation, r doubles and leaves the band (D765 correction). Odd flux needs exotic O3′ planes; the one allowed placement is 8 O3′ with 2/2/2 stuck D3s, Im S·Im ρ = 375–488 (D766a, D766b, D771). Wino window unchanged (D767).
  - D768: plateau origin = postulate P3 (open): anti-D3 nilpotent metric, the same origin level as the SL(2,Z) attractors of 2408.05203. SERAPIS-E's r is ~4.5× below theirs.
  - D769 (running): the light-axion (Re τ) test of P3. A first, invalid run shows ∂N/∂x₀ ~1e-4, i.e. ζ_axion ~1e-9.
- ρ-branch residual-Z₃ chain (D774–D785, 16 Nov 00:45–02:45):
  - D775–D776: ρ-leptogenesis computed (CRV): needs c ≥ 0.6. Later superseded by dilution (D782).
  - D777–D779: at ρ, any lepton-doublet texture gives a degenerate light pair (Z₃ theorem). The light leptons must be Γ₂ singlets, plus 2 extra neutral heavy singlets.
  - D780–D783: the inflaton is Z₃-charged, so its decay products (the heavy Dirac pair) have no renormalisable SM decay. The frozen band holds only if they decay via string-scale operators (Λ ≲ 0.4–1e16 vs M_s ~ 0.6–3e16), giving T₂ ≳ 1e5 GeV. Baryogenesis comes from the late decays (ε ~ 1e-5–1e-3).
  - D784: the SERAPIS-E wino is thermal, 0.67–1.85 TeV (5–41% of DM).
  - D785: τ = i is unaffected (computed mirror check).
- Jl ticks 25–30 (D786–D791):
  - Σm_ν frozen value = NO floor; m₁ free (τ = i: 0.059–0.064).
  - R-Z₃ satisfiable (Z₃ = baryon triality on the SM, D787).
  - Late dim-6 decays can't make the asymmetry (Nanopoulos–Weinberg, D788).
  - P5 (light colour-triplet mediator) is consistent, but with it the N decays conserve B (D789).
  - The inflaton-AD orbit charge works, but Planck isocurvature forces ~3e4 over-production (D790–D791). ρ baryogenesis = OPEN PROBLEM.
  - Open postulates: P1 (explicit CP), P3 (plateau via the anti-D3 metric), P5 (mediator).
- Paper v3.1 (15 pp, new title "The Shape of the Torus Sets the Sky…") is staged; Zenodo package in /mnt/user-data/outputs/zenodo_v3.1 (session) and papers/v3/zenodo. Danny said "Publish"; it needs his Zenodo login in Chrome plus "go".
- Tests (D705): n_s at SO LAT + SPHEREx (~2030); r at LiteBIRD (launch 2032, results ≳ 2035, optimistic reach).
- Pending Danny actions: Zenodo v3.1 "Publish"; outreach emails (4 drafts in papers/v3/drafts/outreach/, not sent); arXiv endorsement/submission.

## Tools (work order, 15 Nov)
- Done: AION pre-registration kit (tools/aion), Inflation Scorecard + Janus (tools/scorecard), SERAPIS tracker (tools/tracker → docs/tracker), D-note index + claim script (tools/dnotes; next D in theory/pending_docs/NEXT_D.txt), docs/INVENTORY.md, CI (.github/workflows/tools.yml, green), TorsionΛ audit D715 (β ≡ Ω_m rescaling; H0=73 case fails Planck priors; README limits text in docs/torsionlambda/), sky-map plan approved; AEGIS Sky Map 1.0.0 built in apps/skymap (release zip via tools/package_release.py; AEGIS layers need export_from_sweep.py run on Danny's PC; public hosting needs his OK). Tools dual-licensed AGPL-3.0 or commercial ($500/$2,500/$10k+).
- Pre-SERAPIS material moved to archive/ (15 Nov).
- Pending Danny: run skymap export on PC; OK for public hosting (GitHub Pages); push access/consent to update torsion-lambda-toolkit README.

## Older line (Twist v5, 14 Nov) — kept for reference
Source of truth v5.3 on Zenodo (DOI 10.5281/zenodo.24226521). TWIST-I: N* 56.7, n_s 0.9648, r 0.0037 (D387); gaps n_s HIGH (3.0σ SPA+DESI), birefringence HIGH; next: D367 stiff integrator, D390 χ trapping.

## Rules
- Lock rules before running; fixes only via *_DEVIATIONS.md written first; no reruns to chase results.
- No Zenodo changes without Danny's explicit "Publish"; emails stay drafts until he says send; never type passwords.
- PC repo: don't touch its git. Keep cost low, integrity first. Honest labels (estimate/computed/literature; post-hoc models scored on future data only).
- 16 Nov deep projects (D828–D842): P3 (anti-D3 one-loop, κ, warped throat) — the E-ratio plateau has no identified string origin; P3 stays a postulate; an anti-D3 needs large small tori (v₄ ≳ 2e4·g_s) for the band. τ = i kept as a CONDITIONAL variant (D841). Frozen predictions unchanged.
