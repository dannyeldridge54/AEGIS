# PREREG D1849 — do the families sit on the turnover's corners? (locked 21 Nov 2026 before computing; repo at 98a0aa3e)
T²/Z₃ at τ = ρ (lattice 1, ω = e^{2πi/3} as in z3_modes.py), flux M = 9, SS phase (1/6, 1/6). Z₃ classes ℓ = 0, 1, 2 (3 modes each, D1790). Class density P_ℓ(z) = Σ_a |ψ_a(z)|² over an orthonormalised basis of the class (Gram matrix on a 120 × 120 grid of the cell), with the Gaussian factor included.
Fixed points of z → ωz: z_k = (m + nω)/(ω − 1) reduced mod the lattice (3 points).
Verdict: CORNERS if each class's global maximum lies within 0.08 (cell units) of a DISTINCT fixed point; PARTIAL if all maxima sit on fixed points but not distinct; NO otherwise. Also report the density at each fixed point per class.
