# AEGIS: current state (15 Nov 2026, 15:45 CT). Read before working.

## Active line: SERAPIS v3 / v3.1 (modular inflation)
- Paper: repo `papers/v3/serapis_v3.tex` (12 pp; v3.1 draft adds Sec. X SERAPIS-E). Zenodo v3 published, DOI 10.5281/zenodo.24250733; v3.1 NOT yet uploaded (needs Danny's "Publish").
- Repo: github.com/dannyeldridge54/AEGIS, branch `unify-bg`. D-notes: theory/pending_docs/D72_D75_weak_spots.md (to D715). Locks: field_tests/rules/PREREG_D*.
- Frozen SERAPIS (τ = i, ρ): n_s 0.970–0.975, r (4.6–5.7)e-4, α_s −(8.5–9.9)e-4, β_s −(3.0–4.6)e-5; caps n_s ≤ 0.985, r ≤ 8.3e-4; strip D679/D681. Prediction sheet: papers/v3/prediction_sheet.md.
- SERAPIS-E (derived branch, lock D693, post-hoc): V = V0[1 − E(ρ,2)/E(τ,2)](1 + CÊ), Ê = E(τ,2) − E(ρ,2); tilt from Berg–Haack–Körs one-loop Kähler correction (hep-th/0508043). n_s 0.970–0.975, r (4.55–5.12)e-4, α_s −(9.4–10.6)e-4; m_φ ≈ 2.2e13 GeV; N* 48.4–49.9.
- Microscopic picture: stuck D3 branes at the three half-periods (no moduli, no twisted charge; Maiden–Shiu–Stefański); tadpole: 5/5/5 + 1 at origin; tilt = fixed-point asymmetry; Im S·Im ρ ≈ 375–1220 (natural). Plateau interior form irrelevant (D698).
- Epstein plateau r-ladder (D700–D702): e = 2 → r ≈ 4.7e-4; e = 2.5 → 3.4e-4; e = 3 → 2.5e-4. Casimir route needs negative codim-2 tension — obstructed in string settings (D703).
- Research front (D706): species-scale/Laplacian swampland may supply the 1/E(τ,2) term (next step); competitor 2607.00528 (r ~ 1e-5, n_s ≈ 0.961); flavour models near ω/ρ (2512.24804).
- Multi-scale test run (D710, Fig. 6): n_s consistent in every release (≤1.33σ from band); Σm_ν 0.0587 passes DESI DR2 <0.0642; nulls hold (μ, f_NL, PBH, PTA/LISA GW, 0νββ); Lyα: eBOSS-only tension (6–7σ) NOT seen in DESI DR1 P1D (<0.8σ, D711); S8, N_eff consistent. Paper now 13 pp.
- Tests (D705): n_s at SO LAT + SPHEREx (~2030); r at LiteBIRD (launch 2032, results ≳ 2035, optimistic reach).
- Pending Danny actions: Zenodo v3.1 "Publish"; outreach emails (4 drafts in papers/v3/drafts/outreach/, not sent); arXiv endorsement/submission.

## Tools (work order, 15 Nov)
- Done: AION pre-registration kit (tools/aion), Inflation Scorecard + Janus (tools/scorecard), SERAPIS tracker (tools/tracker → docs/tracker), D-note index + claim script (tools/dnotes; next D in theory/pending_docs/NEXT_D.txt), docs/INVENTORY.md, CI (.github/workflows/tools.yml, green), TorsionΛ audit D715 (β ≡ Ω_m rescaling; H0=73 case fails Planck priors; README limits text in docs/torsionlambda/), sky-map plan docs/SKY_MAP_PLAN.md (awaiting approval).
- Pre-SERAPIS material moved to archive/ (15 Nov).
- Pending Danny: licence for tools; approve sky-map plan; push access/consent to update torsion-lambda-toolkit README.

## Older line (Twist v5, 14 Nov) — kept for reference
Source of truth v5.3 on Zenodo (DOI 10.5281/zenodo.24226521). TWIST-I: N* 56.7, n_s 0.9648, r 0.0037 (D387); gaps n_s HIGH (3.0σ SPA+DESI), birefringence HIGH; next: D367 stiff integrator, D390 χ trapping.

## Rules
- Lock rules before running; fixes only via *_DEVIATIONS.md written first; no reruns to chase results.
- No Zenodo changes without Danny's explicit "Publish"; emails stay drafts until he says send; never type passwords.
- PC repo: don't touch its git. Keep cost low, integrity first. Honest labels (estimate/computed/literature; post-hoc models scored on future data only).
