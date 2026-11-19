# PREREG D1505 — tilt plan T3b: is D1504's ξ̂/𝒱̂ ≫ 1 flag a convention artefact?

Locked 2026-11-19 ~13:44 UTC before computing. Read-only use of the P3 chat's D1486 (DERIVATION_LOG line 2871; weak_spots ~15356): ξ(τ) = −χ/(4(2π)³)·E(τ,3/2),
λ = c/(2𝒱 + cE_ρ), c = |χ|/(4(2π)³), E_ρ = 8.8927, y* = 23.25·a^{2/3}; benchmarks (|χ|, 𝒱) = (100,100), (200,1000), (400,1e4) with a = 2.0e3, 9.9e3, 5.0e4.
BBHL (hep-th/0412239 Eq. 3.1): K = −2 log[2𝒱e^{−3φ/2} + ξ(Im τ)^{3/2}], ξ = −χζ(3)/2, e^{−3φ/2} = g_s^{−3/2} = y^{3/2}.
Steps (python): (a) recompute a = 1/λ for each benchmark from c, 𝒱, E_ρ (check vs D1486); (b) at the DILMIX strip centre y_model 13.96 (D1497) → y_phys = 13.96·a^{2/3},
evaluate R = cE(y_phys)/𝒱 (P3 convention) and x* = λ(E(y_phys) − E_ρ) (should equal the λ = 1 value 118.3); (c) state which volume is held fixed in P3's form A
(Einstein-frame 𝒱̂ vs string-frame) by comparing with BBHL Eq. 3.1. Rule: if R ≫ 1 in P3's own conventions the flag stands (not an artefact); if R ≲ 1 retract D1504 item 4.
Fixes only via PREREG_D1505_DEVIATIONS.md first.
