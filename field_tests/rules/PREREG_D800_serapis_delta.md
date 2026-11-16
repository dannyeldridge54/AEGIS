# PREREG D800: SERAPIS-Δ (post hoc, not frozen): the two-term DKL plateau at ρ (Jl tick 39)
Locked before computing, 2026-11-16.
CONVENTION (also corrects D798): the family uses K = −ln(−i(τ−τ̄)), i.e. kinetic |τ̇|²/(4y²), as in the D790 code (rho_tot = v²/(4y²)) and the paper (φ = ln y/√2). D798 used −3 ln by its lock, so its n_s/r/y* numbers do not belong to the family convention. Here ε = 0 is recomputed in the family convention (the D798a correction).
Model: V = Δ̃²/(Δ̃²+1) + ε Δ̃, Δ̃ = Δ − Δ(ρ), Δ = −ln(y|η|⁴), on the valley x = ½, y = e^{√2φ}.
Scan: ε ∈ {0, 1e-5, 2e-5, 4e-5, 6e-5, 8e-5, 1e-4, 1.5e-4}. End of inflation at ε_H = 1. At N* = 50 and 55, report second-order slow roll n_s, r, α_s (α_s = 16εη − 24ε² − 2ξ²) and y*. Then test the paper's consistency relation (eq. consistency): α_s^pred from (n_s, r) vs α_s; report the ratio.
Vacuum mass: m²/H²_end, with m² = 2y²V_yy at ρ and H²_end = V_end/2 (ε_H = 1).
Expectations (leading order: Δ̃ ≈ (π/3)y, so the model is the paper's two-term model in Y = (π/3)y):
- the window ε ≈ (0.3–0.8)e-4 gives n_s 0.965–0.975;
- (n_s, r) on the family strip; consistency-relation ratio within 0.8–1.25 (the ln y term adds bias);
- m²/H² ≪ 1 (a quartic-dominated start of oscillation, as for Chronos).
No reruns; fixes go in DEVIATIONS first.
