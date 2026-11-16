# AEGIS: current state (15 Nov 2026, 23:30 CT). Read before working.

## Active line: SERAPIS v3 / v3.1 (modular inflation)
- Paper: repo `papers/v3/serapis_v3.tex` (13 pp; v3.1 draft adds SERAPIS-E + D719–D736 corrections). Zenodo v3 published, DOI 10.5281/zenodo.24250733; v3.1 NOT yet uploaded (needs Danny's "Publish").
- Repo: github.com/dannyeldridge54/AEGIS, branch `unify-bg`. D-notes: theory/pending_docs/D72_D75_weak_spots.md (to D736; next number in NEXT_D.txt). Locks: field_tests/rules/PREREG_D*.
- Frozen SERAPIS (τ = i, ρ): n_s 0.970–0.975, r (4.6–5.7)e-4, α_s −(8.5–9.9)e-4, β_s −(3.0–4.6)e-5; caps n_s ≤ 0.985, r ≤ 8.3e-4; strip D679/D681. Prediction sheet: papers/v3/prediction_sheet.md.
- SERAPIS-E (derived branch, lock D693, post-hoc): V = V0[1 − E(ρ,2)/E(τ,2)](1 + CÊ), Ê = E(τ,2) − E(ρ,2); tilt from Berg–Haack–Körs one-loop Kähler correction (hep-th/0508043). n_s 0.970–0.975, r (4.55–5.12)e-4, α_s −(9.4–10.6)e-4; m_φ ≈ 2.2e13 GeV; N* 48.4–49.9.
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
  - Post-hoc wino prediction: 0.67–0.80 TeV for a cuspy halo, ~15% of DM (D735). ATLAS 2603.08315 already excludes < 670 GeV, so Run 3/HL-LHC will test it (D736).
  - Open: digitised wino sub-fraction limits (2507.15934 Fig. 6); N splitting/CP phases from a flavour model.
- Jl learning loop (22:30 on; D758–D769). Mirror-of-SERAPIS loop: forward/reverse sides, functions L1–L10, checks K1–K8, balances β1–β5. Plan in docs/UPDATE_LADDER_PLAN.md; checker tools/loop/jl_check.py; logs in theory/derivations/ (DERIVATION_LOG, LESSONS, POSTULATES).
  - D759: log-derivative Epstein plateau is a post-hoc CANDIDATE (n_s band at C 5–10e-7, r 2.1–3.1e-4). D760: no string coupling makes the species scale track E(τ,2), so it stays phenomenological.
  - D762–D763: both vacua and the inflaton line are CP-conserving, so leptogenesis on both branches needs high-energy CP phases. Under gCP there is no leptogenesis and δ_CP ∈ {0, π}. Leptonic CP violation discovered ⇒ gCP excluded.
  - D764–D772: postulate P2 (retired D772: the published flux model also ties τ₃ = S, no free inflaton) — replaced by P4 (open, pure-NS flux on non-inflaton tori). Earlier P2 notes: = CP from a second modulus via the flux relation U₂U₃ = b₃/a⁰ with U₂ = ω (2405.18813). With the inflaton in the relation, r doubles and leaves the band (D765 correction). Odd flux needs exotic O3′ planes; the one allowed placement is 8 O3′ with 2/2/2 stuck D3s, Im S·Im ρ = 375–488 (D766a, D766b, D771). Wino window unchanged (D767).
  - D768: plateau origin = postulate P3 (open): anti-D3 nilpotent metric, the same origin level as the SL(2,Z) attractors of 2408.05203. SERAPIS-E's r is ~4.5× below theirs.
  - D769 (running): the light-axion (Re τ) test of P3. A first, invalid run shows ∂N/∂x₀ ~1e-4, i.e. ζ_axion ~1e-9.
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
