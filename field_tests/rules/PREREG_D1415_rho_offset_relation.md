# PREREG D1415 — ρ analogue of D640: does the offset model predict A1's exact α_s within 1 %?

Locked 2026-11-19 (UTC) before computing (JANUS tick 13, node janus).
Model (D691 asymptotics, D1414): V/V0 = P(1 + C·Ê), P = 1 − 1/(Ê + 1), Ê + 1 = A y² + B + D/y, A = 2ζ(4), B = 1 − E(ρ,2) = −4.7833,
D = π ζ(3) (Epstein E(τ,2) = 2ζ(4)y² + πζ(3)/y + exp. small, i.e. 2√π Γ(s−½)ζ(2s−1)/Γ(s) at s = 2). The D coefficient is first
CHECKED numerically: lattice sum of E(τ,2) at τ = −½ + iy, y = 2, 3, 4, against 2ζ(4)y² + πζ(3)/y + 1 − ... (residual must fall
like e^{−2πy}; require |residual| < 1e-3 at y = 3). Canonical field φ = ln y/√2.
Slow roll (first order, numerical derivatives in φ): ε = ½(V′/V)², η = V″/V, ξ² = V′V‴/V²; n_s = 1 − 6ε + 2η, r = 16ε,
α_s = 16εη − 24ε² − 2ξ². Solve (C, y*) so (n_s, r) = A1 (0.974393, 4.82095e-4); predict α_s.
Controls: the same solve with B = D = 0 (pure plateau) — reported, to separate the offset's effect from slow-roll order.
Rule: PASS if |α_s(model)/α_s(A1 exact) − 1| < 1 % with A1 exact α_s = −9.9814e-4 (D1262); FAIL otherwise.
No reruns to chase results; fixes only via PREREG_D1415_DEVIATIONS.md written first.
