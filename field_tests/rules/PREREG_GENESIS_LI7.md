# PREREG_GENESIS_LI7 — rung R-Li: lithium (locked D1640, 2026-11-19 16:30 CT)
Method: BBN v3 (D1634) plus ⁷Be and ⁷Li: ³He(α,γ)⁷Be, t(α,γ)⁷Li, ⁷Be(n,p)⁷Li, ⁷Li(p,α)⁴He. Rates: SKM-1993/CF88 fits (tools/genesis/li7rates.py), cross-checked BEFORE this lock against the PArthENoPE fits (astro-ph/0408076 App. E) at T₉ = 0.1–1.0: all ratios 0.96–1.05. Final Li/H = (⁷Li + ⁷Be)/H, since ⁷Be later decays to ⁷Li.
Change of plan (not a deviation from any lock): the weak-rate corrections are moved to a separate rung, so this rung is lithium only.
Pass rules:
L1 Li/H ∈ [3, 7] × 10⁻¹⁰ (standard prediction ≈ 5 × 10⁻¹⁰). The observed Spite plateau, 1.6 ± 0.3 × 10⁻¹⁰, is the PROBLEM, not the target.
L2 Y_p and D/H within 0.5% of v3 (the A = 7 chain is a trace and must not feed back).
L3 ⁷Be fraction of final Li ≥ 0.5 (at Planck η most lithium is made as ⁷Be).
P-M tests (reported, with the reading fixed in advance):
M1 Li/H at ΔN_eff = 0.3. If |Δ| < 10%, the mirror sector does NOT solve the lithium problem (it needs a factor ≈ 3).
M2 ρ_DM/ρ_rad at T = 0.07 MeV for the observed DM density (5 GeV dark baryons have only a gravitational effect in BBN). Reading: < 10⁻³ means negligible.
Script: field_tests/scripts/genesis_matter/li7_run.py
