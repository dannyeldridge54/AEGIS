# PREREG SPECIES32 — the IIB species-scale plateau: V ∝ G^{ττ̄}|∂_τ ln E(τ,3/2)|² (Λ_QG = E_{3/2}^{-1/6})

Locked 2026-11-19 (09:05 CT) before computing. Danny 08:53 "research online look for papers and hints".
Source [literature]: van de Heisteeg, Vafa, Wiesner, Wu, arXiv:2310.07708 eq. (3.15): global 10D IIB species scale Λ_QG = (E_{3/2}(τ))^{-1/6},
absolute maximum at τ = ρ (the "desert point"). Casas–Ibáñez arXiv:2407.12081: inflaton potential V ∝ G^{ij̄}∂_iΛ ∂_j̄Λ/Λ² (species
convex-hull generator), proposed (no derivation). Our D758/D759 did this with E(τ,2) (approach y^{−3}, retired D822 for "no source").
New here: with the IIB R⁴ function E(τ,3/2) the source is the literature species scale, and the approach is derived now:
E(τ,3/2) ≈ 2ζ(3)y^{3/2} + 4ζ(2)y^{−1/2} ⇒ y∂_y ln E = 3/2 − 2u + O(u²), u = 2ζ(2)/(ζ(3)y²) ⇒ 1 − V/V∞ ≈ (8/3)u ∝ y^{−2}, i.e. k = 2,
the exponent D1516 found the band needs (pure-power family). ∂E = 0 at ρ ⇒ V(ρ) = 0 (Minkowski vacuum at the desert point).
Model: along Re τ = ½, V₀ = (2/3·y ∂_y ln E(τ,3/2))² (normalised V₀ → 1), tilt T1: V = V₀·(1 + C·(E − E(ρ))) (the D759 convention:
tilt in the modular variable itself). Kinetic K = −ln(−i(τ − τ̄)) ⇒ φ = ln y/√2 (pipeline n = 1). T_R 8.94e8, engine F (third-order
flow + self-consistent N*; D1521: exact to ~1e-6 in n_s), start by the D1 bisection rule.
Grid: C ∈ {0, 0.5, 1, 1.5, 2, 3, 4, 6}e-6.
Checks: V(ρ) = 0 to < 1e-10; fitted approach exponent over y ∈ [20, 200] equals 2 within 0.05.
Rule: "in band" / "near" as PREREG_SMSCAN; report the in-band C interval by linear interpolation. Any in-band point ⇒ exact-MS
confirmation run at the interval centre (locked by this file) before it is quoted. Expectation stated now: untilted n_s ≈ 0.960,
r ≈ 3–5e-4; in band for some C in 1–4e-6 (the tilt grows as y^{3/2}, slower than SERAPIS's y²).
No reruns to chase results; fixes only via PREREG_SPECIES32_DEVIATIONS.md written first.
