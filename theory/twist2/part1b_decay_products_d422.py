"""D422 (locked PREREG_D422_PART1B): second pass, Part 1 condition (ii). On the Higgs branch of W = λ(T−T_E)χχ̄ + y χ ψ ψ̄' (U(1)_X D-flat,
|χ| = |χ̄| = v), δT pairs with the neutral radial mode into a chiral multiplet of mass m_S = √2 λ' v (λ' = canonical λ x_E √(2/3), D396).
Its fast decay needs a coupling to lighter states; the Yukawa y gives Γ = y² m_S/(8π) (κ = (y/g_X)² in D407's notation) AND a mass m_ψ = y v
to the products. Kinematics: m_ψ < m_S/2 ⇒ y < λ'/√2. If ψ-number is conserved the ψ are stable: thermal relic estimate
Ωh² ≈ 2.1×10⁻¹⁰ GeV⁻² / ⟨σv⟩ with ⟨σv⟩ = π α_X² / m_ψ² (α_X = g_X²/4π, g_X = 0.5). AI-assisted."""
import math
gX = 0.5; aX = gX**2 / (4 * math.pi)
for lam in (0.004, 0.01, 0.033):
    lp = lam * 29.6 * math.sqrt(2 / 3)
    for v in (1e9, 1e11):
        mS = math.sqrt(2) * lp * v; ymax = lp / math.sqrt(2); ymin = gX * 1e-3   # κ ≥ 1e-6 ⇔ y ≥ g_X 1e-3
        for y in (ymin, min(1e-2, 0.9 * ymax)):
            mpsi = y * v; sv = math.pi * aX**2 / mpsi**2; Oh2 = 2.1e-10 / sv
            print(f"λ {lam:5.3f} v {v:.0e}: m_S {mS:.2e} GeV, y {y:.1e} (allowed {ymin:.1e}–{ymax:.2e}), m_ψ {mpsi:.2e} GeV, stable-ψ Ωh² ≈ {Oh2:.1e}")
