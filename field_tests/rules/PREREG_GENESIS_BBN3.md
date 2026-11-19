# PREREG_GENESIS_BBN3 — "fix deuterium": real D-burning network (locked D1634, 2026-11-19 15:50 CT)
Context: BBN v2 (D1633) got Y_p = 0.2466 but D/H = 2.9 × 10⁻⁶ (≈9× too low) from a single lumped D + D step, and failed its rate-systematic rule. That result stands.
Method (tools/genesis/bbn3.py): the v2 background, weak rates and Saha start (T_sw = 0.2 MeV) unchanged. Network n, p, d, t, ³He, ⁴He with:
- p(n,γ)d (+ photodissociation by detailed balance), d(p,γ)³He, d(d,n)³He, d(d,p)t, ³He(n,p)t, t(d,n)⁴He, ³He(d,p)⁴He.
- Rates: Smith–Kawano–Malaney (1993) N_A⟨σv⟩(T₉) fits. These were checked BEFORE this lock against the PArthENoPE fits (astro-ph/0408076, App. E) at T₉ = 0.1–1.0: ratios 0.94–1.08 for all six shared reactions (d(p,γ) not compared, as the extracted fit was garbled).
- Reverse rates other than D photodissociation are neglected (Q ≥ 5.5 MeV).
Pass rules:
P1 Y_p ∈ [0.235, 0.260].
P2 D/H ∈ [1.5, 4.0] × 10⁻⁵ (observed 2.53 ± 0.03 × 10⁻⁵; toy window).
P3 ³He/H ∈ [0.5, 2.0] × 10⁻⁵ (standard prediction ≈ 1.0 × 10⁻⁵).
P4 Rate systematic: all charged-particle rates ×0.8 and ×1.2 together. PASS if the Y_p spread ≤ 0.003; report the D/H spread.
P5 D/H slope d ln(D/H)/d ln η from η ± 10% ∈ [−1.9, −1.3] (standard ≈ −1.6).
Plus, reported with no rule: dY_p/dΔN_eff, and the P-M mirror bound effect at ΔN_eff = 0.3 on D/H.
Script: field_tests/scripts/genesis_matter/bbn3_run.py
