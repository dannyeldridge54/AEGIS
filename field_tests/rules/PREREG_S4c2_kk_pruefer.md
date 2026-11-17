# PREREG S4c2 — KK spectrum on the D1015 6D vacuum by Prüfer-angle shooting (replaces S4c's FD method, D1026)
Locked 2026-11-17 before any S4c2 number.
Same operator as S4c: −(pψ′)′ = m² wψ, p = e^{(D−1)A−B}, w = e^{(D−3)A+B}, flux-free (pψ′ = 0) at both ends.
Prüfer angle: ψ = ρ sin θ, pψ′ = ρ cos θ ⇒ θ′ = cos²θ/p + m² w sin²θ (only θ is integrated: no overflow in ρ).
Flux-free ends ⇒ θ(a) = π/2 and θ(b) = π/2 + nπ for the n-th eigenvalue (n = 0 zero mode, n = 1 first massive).
Root-find m² on [θ(b) − π/2 − nπ]. Interval [ε, y_end − ε], ε ∈ {1e-3, 1e-4, 1e-5}·y_end (Radau, rtol 1e-10).
Validation V (must pass first): flat interval p = w = 1, L = 2: m_n² = (nπ/L)² for n = 1, 2, 3 to 1e-6 relative.
Tests on the 6D vacuum: T1 n = 0 gives m² ≈ 0 (|m₀²| ≤ 1e-6 m₁²); T2 m₁² converged across ε to 1e-3; T3 m₁² > 0.
Verdict VALID iff V, T1–T3; report m₁, m₂/m₁, m₃/m₁ in units of √α_E.
