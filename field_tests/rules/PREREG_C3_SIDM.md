# PREREG C3 — dark-matter self-interaction of the Weave's dark particle (test plan C3). Locked BEFORE computing.
Inputs (earlier Weave notes): m_χ = 12.8 GeV (D1676), asymmetric (only particles: χχ → χχ, repulsive Yukawa via the dark photon), m_A′ ∈ [0.3, 12.8] GeV (D1685/D1688), α_D ≥ 4.7e-4 (D1677). α_D above the minimum is free ⇒ report α_D = 4.7e-4 (minimum) and 4.7e-3 (×10).
Formula (Born regime, valid when α_D m_χ/m_A′ < 1, checked in code): transfer cross-section for a Yukawa potential,
σ_T = (8π α_D² / (m_χ² v⁴)) · [ ln(1 + R²) − R²/(1 + R²) ], R = m_χ v / m_A′ (v = relative velocity, c = 1); arXiv:1403.1077 / Feng-Kaplinghat-Yu.
Velocities: dwarfs 30 km/s, galaxies 200 km/s, clusters 1000 km/s. Units: 1 GeV⁻² = 3.894e-28 cm², 1 GeV = 1.783e-24 g.
Pass/fail (decided now): PASS (consistent) if σ_T/m_χ < 0.1 cm²/g at 1000 km/s over the whole window at α_D = 4.7e-4 (cluster bounds ~0.1–1). Also REPORT (label E, no pass/fail) whether σ_T/m_χ ≥ 0.5 cm²/g at 30 km/s anywhere (would make cores). One run.
