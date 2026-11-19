# Janus lead queue — derivations from the geometry (planned 19 Nov 2026)

Danny 04:18 CT: "Can u have Janus still deriving nodes" / "Plan as many as u can based off the geometry predictions".
The geometry: inflation near the two SL(2,Z) fixed points — ρ = e^{2πi/3} (SERAPIS-E, V = (1 − 1/E₁)(1 + C(E₁ − 1)), B = 1 − E(ρ,2) = −4.78334) and τ = i (NA12, V = I²/(I² + 1) + ε·I₁, c = ln1728/2π) — with the modular Kähler field map φ = ln y/√2.
Scope: Janus nodes only (janus, band_e_audited, band_i, band_e, vac_discriminant). Each lead = one D-note through the full pipeline (lock first). No map status edits; status changes are Danny's.
Tools: field_tests/scripts/d1449/vac_grid.py solve(), d1442/second_order.py (ρ), d1448/tau_i_exact.py (τ = i), theory/modular/running_d632.py.
Order = queue order. Mark `[done D####]` when finished; add follow-ups at the end.

## A. Spectrum observables at the two fixed points
- [done D1480] L1 Pivot conversion: n_s, α_s at k = 0.002 Mpc⁻¹ from k = 0.05 (via α_s, β_s), both vacua; compare the pivot of 2609.35964 / BK.
- [done D1555] L2 Tensor tilt n_t to second order and the consistency-relation deviation n_t + r/8, both vacua.
- L3 N_* dependence: n_s, r, α_s across N_* = 50–60, both vacua; which N_* range D1478's data prefer.
- L4 μ-distortion from the derived P(k) (standard window, k ≈ 50–10⁴ Mpc⁻¹), both vacua vs no-running; PIXIE/PRISM σ_μ as [literature].
- L5 Joint n_s–α_s pull vs 2609.35964 if a correlation is readable; else NULL loud.
- L6 Tensor running α_t (second order), both vacua.
- L7 Truncation test: exact MS P(k) vs the (n_s, α_s, β_s) Taylor form over k = 1e-4…1 Mpc⁻¹ — where the expansion fails.
- L8 Small-scale power at k = 1–10 Mpc⁻¹ (Lyα range) relative to no-running; compare the eBOSS Lyα slope/curvature on file (2511.01612).
- L9 Single-field f_NL^local = (5/12)(1 − n_s), both vacua; SPHEREx σ(f_NL) as [literature] — a consistency number, not a test.

## B. Field-space geometry (φ = ln y/√2)
- L10 Field excursion Δφ from y_* to y_end and the Lyth-bound check against r, both vacua.
- L11 End of inflation: y_end where ε_V = 1 (and |η_V| = 1); N(y_* → y_end) vs the audited box N_* 50.07–51.22.
- L12 Scale of inflation: V_*^{1/4} and H_* from A_s (Planck 2018 value on file) and r, both vacua.
- L13 Inflaton mass at the minimum (canonical V'' at the vacuum), both vacua — input to reheating.
- L14 Reheating consistency: Liddle–Leach matching (w_reh = 0, 1/3) gives T_reh for N_* 50–51; compare with a gravitational-decay estimate Γ ~ m³/M_P² [estimate].
- L15 Falsifier map: if SO measures n_s = 0.968 (CMB-only centre), what N_* each vacuum would need, and whether reheating can supply it.

## C. Modular-geometry sensitivities
- L16 ρ: ∂(n_s, r, α_s)/∂B — how strongly the fixed-point Eisenstein value E(ρ,2) sets the predictions (error propagation of B).
- L17 τ = i: ∂(n_s, r, α_s)/∂c with c = ln1728/2π — same for the j(i) = 1728 offset.
- L18 Non-zero modes: size of the e^{−2πy} terms at y = 14–30 on n_s and α_s, both vacua (expected negligible; state the number).
- L19 ρ: α_s and β_s across the allowed C_r range of the audited box.
- L20 τ = i: n_s, α_s, β_s across the audited ε window 1.378–1.440e-4 (D1461), band_i edges.
- L21 Janus relation κ residual map: κ = α_s/(LO form) across both boxes — one table for the card.

## D. Data confrontations (locked rules, as D1471/D1478)
- L22 Gaussian Δχ² of each vacuum point vs the ΛCDM+α_s best fits of 2609.35964 Table III (marginal, correlation caveat).
- L23 Pivot-matched rerun of D1471/D1478 pulls if L1 shows a pivot mismatch > 0.1σ.
- L24 SO + LiteBIRD joint forecast for (n_s, r) at both vacua with the official δr = 1e-3 and SO σ(n_s) = 0.002 (D1440/D1441 inputs) — 2D separation from CMB-only centre.
- L25 What σ(α_s) a future survey needs to see the ρ − τ = i gap at 2σ (update of D1449's 0.05σ).

## E. Upkeep
- L26 Card refresh: add A–D results to docs/JANUS_FORMULAS.md and machine-check against jsons (as D1469/D1473) — after every ~5 leads.
- L27 Console sync: update chains/{rho,tau_i,bands,tests} stages with new results.
- L28 (from D1480) r at k = 0.002: compare r_0.002 = 4.46–4.47e-4 with any bound quoted at 0.002 (check which pivot BK18 / LiteBIRD forecasts use) — read the pivot from the papers.

## F. Genesis pathways (added 19 Nov 2026 16:20 CT — Danny: "use the newest Serapis calculation … with both the dark energy and scalar field or matter genesis … update Janus with the right pathways")
Source chain (all on file, nothing new assumed here):
SERAPIS FINAL EQUATION v3 (scalar field ψ = string coupling; D = 10 default; theory/pending_docs/SERAPIS_FINAL_EQUATION.md)
→ reheating (T_R ≈ 9e8 GeV Weave; 7.389e8 GeV exact-pipeline point)
→ matter genesis P-M (one asymmetry, ADM, m_DM = 5.03 GeV at equal sharing; D1631–D1632)
→ light elements (BBN v3, all 5 locked rules PASS; D1633–D1634) → recombination (Saha toy, D1632)
→ reverse thread / late dark energy P-G (V = V_Λ(1 − 7.30 e^{−βφ}); D1626–D1630, published 10.5281/zenodo.24380387).
Scope guard: D1636 (full-likelihood DE fit, other session) is NOT a Janus lead — read its result when it lands, never redo it.
Cycle per lead (one lead per tick): Research → Development → Postulation → Derivation → Postulation check → Referee → Review.

- [done D1637] G1 Reheating from the final equation: inflaton mass at ρ (V'' of the D = 10 potential, canonical ψ) and T_R from Γ ~ m³/M_P² [estimate] vs the 7.389e8 / 9e8 GeV on file — is the number that feeds P-M actually derived from v3?
- [done D1638] G2 Thread continuity: is the late thread's coefficient (7.30) and slope β = √(D−2) the SAME function as v3's plateau (V ≈ V∞[1 − 7.30 e^{−β_D ψ}]) — derive, or flag P-G as a separate field.
- [deferred: other chat queued C2 "C-start" (WEAVE_POSTULATES.md, D1639) — Janus reads it, does not redo] G3 Starting height: can the ~1 % tuned start (D1628) be set by inflation-era dynamics (frozen field + Hubble friction since reheating)? Postulate check, then compute the frozen value if a mechanism exists; else NULL loud.
- [deferred: other chat queued C3] G4 Z₃ at ρ and the sharing factor n_DM/n_B (D1631's next step): does the residual Z₃ fix it? Literature first; locked test only if a concrete rule exists.
- [deferred: other chat queued C4] G5 Asymmetry source at T_R: Davidson–Ibarra bound vs T_R from G1 [literature + estimate]; which non-thermal route survives.
- [done D1646] G6 Mirror-sector temperature ξ from reheating branching (inflaton → mirror vs visible) and the ξ < 0.45 bound (D1632 T4).
- [taken by other chat: D1639 rung R-Li, D1640 lock] G7 BBN v3 + Li-7 (known gap): add ⁷Be/⁷Li channels under a new lock; report the lithium value honestly (the standard model's own Li problem expected).
- [taken by other chat: D1640 R-Li includes weak-rate corrections] G8 BBN weak-rate corrections: the stated −0.005 Y_p bias — lock, add Coulomb/radiative/finite-mass terms, re-score.
- [done D1644] G9 Future oscillation of the thread: thread mass m ~ √V''(min) vs H₀; when (if ever) it becomes matter-like and what fraction — art/lens claim vs physics stated separately.
- [done D1647] G10 Genesis budget table: Ω_DM/Ω_b, η, Y_p, D/H, ³He/H, w₀/w_a — every number from its json, one card (machine-checked as D1469/D1473).
- [done D1650] G11 Console sync: chains/genesis stages updated with G1–G10 results.
- [done D1650 PASS] G12 REFEREE (whole genesis chain, fresh read of every json): pass → loop stops and reports to Danny; fail → the failures become new G-leads.
- [done D1641] G1b (from D1637) Derive why V''/V∞ = 1/4 exactly at ρ (expected (f')² = 1/8 = λ_sp², the species-scale slope) — analytic, no data.
- [done D1644] G2b (from D1638) The thread at ρ: oscillation about V = 0 with V'' = V_Λ/4 (D1637's 1/4) ⇒ m_DE ~ H₀ — when it reaches ρ in the future, how fast it becomes matter-like (merge with G9). G3 must use the EXACT v3 shape (D1638).
- [done D1653 ROBUST] G9b (from D1644) The thread's end point in the full τ plane (x and y): does it still settle at an image of i, or at ρ, once the axion direction is free? Needs the 2D kinetic metric (dτdτ̄/(2y²)·(D−2)/… — read the kinetic normalisation from SERAPIS_FINAL_EQUATION step 1 first).
- [done D1654: minimal sector EXCLUDED; D1646a] G6b (from D1646) Replace A-dem: channel-by-channel gravitational decay of the inflaton at ρ (scalars vs helicity-suppressed fermions vs conformal gauge bosons) — does the dark side still start at ξ ≈ 1? Then read the current N_eff bound and the next-CMB σ(N_eff) from papers (lock).
- [done D1655: i 9/10, ρ 1/10] G9c (from D1653) Larger axion kicks (δx ~ 0.1–0.5) and starts off the x = ½ line: is there a basin boundary where the thread ends at ρ instead of i? Map the basin.
- [done D1657 OPEN] G6c (from D1654) Massive dark photon rescue: what dark-photon mass range (non-relativistic before recombination, decays/kinetic mixing bounds as [literature]) keeps P-M alive — lock with sourced bounds.
- [done D1659: OPEN 0.3–5 GeV, ε 1e-11–1e-7] G6d (from D1657) Lab limits on the dark photon (beam dump, BaBar/LHCb/NA64 etc.) over 1 MeV–5 GeV vs the BBN floor ε ≳ 1e-10 — fetch the current exclusion summary, lock, state the open strip.
- [done D1658] G9d (from D1636) Rerun the thread's future (D1644 acceleration end, D1655 end point) from D1636's full-likelihood best starts (u_i 0.150 / 0.184 / 0.179 in field_tests/results/D1636/rt10_*.json — read D1636's u_i definition first): does acceleration still end, when, and where does it settle?
- [done D1661] G13 (from D1660) Sourced scope note for D1632 T4, D1648 Q2, D1649: recompute with ΔN_eff ≤ 0.086 (2σ, 2603.13226) — full-mirror ξ_max, ξ⁴, the visible-favoured decay ratio, D1648's m_DM under symmetric decay, and D1649 version (b) with a massive dark photon (D1659). Then G12c: re-run g12b_referee.py source audit; PASS if only nits remain.
