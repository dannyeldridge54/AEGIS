# PREREG DUAL — "circuit switch" test: do the 10D (R⁴, E(τ,3/2), species-gradient) and 8D (E(τ,2), ratio) plateaus give the same inflation once their asymptotics are matched?

Locked 2026-11-19 (10:05 CT) before computing. Danny 09:59: "create a dual serendipitous equation that takes the parts that work in both and
interweaves the calculations … at every dimensional level the theory switches … see if that is a working, capable thing."
Dual equation (derived before computing): V = V∞·[1 − D(τ)]·[1 + C·X(τ)], with two representations of the plateau defect D:
  10D (R⁴ level):  1 − D₁₀ = |∇ ln Λ₁₀|²/λ_sp² = 1/3 + (4/3)∇² ln Λ₁₀,  Λ₁₀ = E(τ,3/2)^{−1/6}   (P3-S; D1546)  ⇒ D₁₀ ≈ (16ζ(2)/3ζ(3))·y^{−2}
  8D (T², E₂ level): 1 − D₈ = e/(e + 1), e = λ₈(E(τ,2) − E(ρ,2))  (SERAPIS-E form)               ⇒ D₈ ≈ 1/(2ζ(4)λ₈ y²)
Switch rule (asymptotic matching): D₁₀ ≃ D₈ at large y ⇔ λ₈ = 3ζ(3)/(32ζ(2)ζ(4)) = 0.063298. Both vanish at ρ (V = 0 there). The Eisenstein
order switches s = 3/2 → 2 between levels by the map s_ratio = 2s_grad − 1 (log-gradient of E_s approaches as y^{1−2s}, the ratio of E_{s'}
as y^{−s'}).
Runs (engine F, T_R 8.94e8, D1 start rule):
  R1: 10D untilted (C = 0)        R2: 8D untilted, λ₈ = 0.063298, C = 0
  R3: 10D with its own R⁴ tilt C·(E_{3/2} − E_{3/2,ρ}), C = 8e-7 (D1532 centre)
  R4: 8D with its own pipeline tilt C·(E₂ − E₂,ρ) at λ₈ = 0.063298, C ∈ {2e-7, 4e-7, 6e-7, 8e-7} (scan to bracket n_s 0.9706)
Rule ("dual holds"): R1 vs R2 |Δn_s| ≤ 1e-3 and |Δr|/r ≤ 5 % (untilted observables set by the matched asymptotics, not by the level);
report R4's r at n_s 0.9706 vs R3 (expected different: the tilt powers differ, y² vs y^{3/2}; D1529 ordering predicts R4 r < R3 r).
Expectation stated now: dual holds at C = 0 (both k = 2, same amplitude); near-ρ differences shift N* by < 0.5.
No reruns to chase results; fixes only via PREREG_DUAL_DEVIATIONS.md written first.
