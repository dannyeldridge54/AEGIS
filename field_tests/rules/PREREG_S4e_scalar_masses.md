# PREREG S4e — scalar KK masses: solver validated on the 10D critical orientifold, then applied to our 6D subcritical vacuum
Locked 2026-11-17 before any S4e number. Sources [fetched, arXiv 2209.10553]: critical background (3.10) A = −[ξ²/2 − ln ξ]/(2(D−1)),
φ = φ₀ + (D−2)[ξ²/2 + ln ξ]/(4√(D−1)), ξ = √(2(D−1)/(D−2)) y, gauge B = −γφ/2, α_E = 1, φ₀ = 0; dz = e^{B−A}dy; Ω = A (§5.1–5.2, as read);
scalar operator H = b + 𝒜†𝒜 (5.5–5.9) ⇒ −Ψ'' + U Ψ = m²Ψ, U = b + W² + W′ (derived here from 𝒜 = −d/dz + W), W = ((D−2)/2)(3Ω′ − e^{2Ω}V₀′/(4φ₀′)),
b = 2(D−3)e^{2Ω}(V₀/(D−2) + (D−2)Ω′V₀′/(8φ₀′)), ′ = d/dz, V₀ = 2α_E e^{γφ} (the action's potential term — a CONVENTION ASSUMPTION; the validation tests it).
Target (2209.10553 Eq. 5.14, 10D critical orientifold, shooting): m₁ ≈ 0.97π/L, m₂ ≈ 2.13π/L, L = Einstein-frame proper length ∫e^B dy.
Method: Prüfer shooting in z on [z(ε₁), z(ε₂)] with cutoffs in ξ (ε₁ = 1e-4 near ξ = 0; upper end at ξ_max where the proper length has converged to 1e-6),
BC Dirichlet (Ψ = 0) and Neumann (Ψ′ = 0) at both ends, both reported.
V1 (validation): for one BC choice, m₁L/π and m₂L/π within 3% of 0.97 and 2.13 → SOLVER VALIDATED (that BC + V₀ convention adopted). Else S4e
NOT VALIDATED (report numbers; no 6D claim). Only if V1 passes: apply the same solver/BC/convention to the 6D subcritical vacuum (S4b) and report m₁, m₂,
m₂/m₁ in units of π/L (claim only m² > 0 for the lowest mode, consistent with D1140). Results: field_tests/results/s4e_scalar_masses.txt.
