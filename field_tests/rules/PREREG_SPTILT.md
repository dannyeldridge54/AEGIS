# PREREG SPTILT — which tilt powers can put the species-scale plateau (P3-S) in band? Tilts = powers of the species scale itself

Locked 2026-11-19 (09:15 CT) before computing. Danny 09:09 "Again" (DpL cycle 3, postulation).
Base: P3-S (PREREG_SPECIES32 + DEVIATIONS D1 code path, 5-point stencil): V₀ = (2/3·y∂_y ln E(τ,3/2))², Re τ = ½, φ = ln y/√2, engine F,
T_R 8.94e8, start by the D1 bisection rule.
Postulated tilt families (candidate sources in brackets; none derived):
  T1: V₀(1 + C(X − X_ρ)), X = E^{1/3} = Λ_QG^{−2} ~ y^{1/2}   [a (H/Λ_sp)²-type correction]
  T2: X = E^{2/3} = Λ_QG^{−4} ~ y              [(H/Λ_sp)⁴-type]
  T3: X = E = Λ_QG^{−6} ~ y^{3/2}              [R⁴-coefficient; = the D1523 tilt, rerun here as control]
  T5: X = E(τ,5/2) ~ y^{5/2}                    [D⁴R⁴ coefficient]
C grid per family: C = f·C₀, C₀ = 8e-4/(X(y = 55.64) − X_ρ) (same tilt fraction as D1523's centre at its y*), f ∈ {0, 0.25, 0.5, 0.75, 1,
1.25, 1.5, 2}.
Report n_s, r, α_s per point; in-band C interval by linear interpolation (band n_s 0.969–0.975, r 4.55–5.7e-4) and r at the band centre.
Control: T3 at f = 1 must reproduce D1523's centre (n_s 0.97065, r 5.41e-4) to 1e-4.
Expectation stated now: all four families can reach n_s 0.969–0.975 (any rising term raises n_s); r at band differs — slower tilts
(T1) give smaller r, faster (T5) larger. Which family lands with r inside 4.55–5.7e-4 is the result.
No reruns to chase results; fixes only via PREREG_SPTILT_DEVIATIONS.md written first.
