# PREREG S4c — probe on the D1015 6D vacuum: KK spectrum of a minimally coupled massless bulk scalar
Locked 2026-11-17 before any S4c number. Background: D1015 (Basile–Thomée 2209.10553 Eq. 3.11, D = 6, γ = 2, α_E = 1),
metric e^{2A(y)} η_{(D−1)} + e^{2B(y)} dy², B = −γφ/2 — note: the uncompactified space is (D−1) = 5-dimensional.
Mode equation (derived from √g g^{MN}∂χ∂χ): −(e^{(D−1)A−B} ψ′)′ = m² e^{(D−3)A+B} ψ, Neumann (flux-free) at both ends.
Method: finite differences (second-order, symmetric) on y ∈ [ε, y_end − ε], ε = 1e-3, 2e-4, 4e-5 × y_end; N = 2000, 4000
points; report the lowest 4 eigenvalues m²; zero mode expected (constant ψ). Tests: T1 lowest |m₀²| ≤ 1e-8 relative to m₁²
(zero mode present); T2 m₁² converged to 1e-3 relative across the ε and N refinements; T3 all m² ≥ 0 (no tachyon, as
required for a Sturm–Liouville operator with positive weights — a check of the code, not of physics).
Verdict: probe VALID iff T1–T3; then report m₁ in units of √α_E and the volume-weighted interval size.
