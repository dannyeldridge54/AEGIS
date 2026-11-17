# PREREG C7 — McMillan 2017 Milky Way vs the C2/C3/C4/C6 data (Djl C; follows D1108) — locked 2026-11-17
Potential: galpy.potential.mwpotentials.McMillan17 (DiskSCF + NFW + SCF), its own units (ro = 8.21 kpc, vo = 233.1 km/s). No rescaling.
Data and methods identical to the earlier locks:
- C3: M(<73) = 4.3 ± 0.95e11 (KG) and M(<52) = 4.1 ± 1.2e11 (BHB), via M ≈ r v_c²/G.
- C4: NFW-halo-only M200 (200 ρ_crit, H0 67.66) vs KG 0.55 (+0.15/−0.11) and BHB 1.00 (+0.67/−0.33) e12.
- C6: v_esc(8.3 kpc) to 2 r200 (Deason definition, D1108) vs 528 (+24/−25).
- C2: Jeans σ_r (galpy, tracer r^−3.5, β ∈ {0, 0.5, 0.8}) at 20/50/80/120 kpc vs 120/102/84/50 ± 22. Rule: |Δ| ≤ 20 km/s at the first three and 2σ at 120 kpc.
Scored per data set: CONSISTENT (≤ 2σ), TENSION (≤ 3σ), EXCLUDED, or for C2 per β as before.
Headline: whether one published Gaia-calibrated model passes all four without rescaling, unlike MWPotential2014, which needed s ≈ 1.1.
Script theory/wiring/c7_mcmillan17.py (written after this lock).
