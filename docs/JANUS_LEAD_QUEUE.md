# Janus lead queue — derivations from the geometry (planned 19 Nov 2026)

Danny 04:18 CT: "Can u have Janus still deriving nodes" / "Plan as many as u can based off the geometry predictions".
The geometry: inflation near the two SL(2,Z) fixed points — ρ = e^{2πi/3} (SERAPIS-E, V = (1 − 1/E₁)(1 + C(E₁ − 1)), B = 1 − E(ρ,2) = −4.78334) and τ = i (NA12, V = I²/(I² + 1) + ε·I₁, c = ln1728/2π) — with the modular Kähler field map φ = ln y/√2.
Scope: Janus nodes only (janus, band_e_audited, band_i, band_e, vac_discriminant). Each lead = one D-note through the full pipeline (lock first). No map status edits; status changes are Danny's.
Tools: field_tests/scripts/d1449/vac_grid.py solve(), d1442/second_order.py (ρ), d1448/tau_i_exact.py (τ = i), theory/modular/running_d632.py.
Order = queue order. Mark `[done D####]` when finished; add follow-ups at the end.

## A. Spectrum observables at the two fixed points
- L1 Pivot conversion: n_s, α_s at k = 0.002 Mpc⁻¹ from k = 0.05 (via α_s, β_s), both vacua; compare the pivot of 2609.35964 / BK.
- L2 Tensor tilt n_t to second order and the consistency-relation deviation n_t + r/8, both vacua.
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
