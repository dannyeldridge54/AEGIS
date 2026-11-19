# PREREG D1364 — P3 hunt step 4: can the string-order mix of shape functions give the SERAPIS plateau?

Locked 2026-11-19 before computing (Danny 18:10 "Djl" on the P3 hunt).

## Model family (everything else exactly SERAPIS-E: tools/serapis_calc/pipeline.py, path Re U = ½, kinetic n = 1,
V = e/(e+1)·(1 + C e/λ), e = λ[F(U) − F(ρ)], BHK tilt C, self-consistent N* with reheating):
  F_w(U) = (1 − w)·k·Ê₁(U) + w·E(U,2),   Ê₁(U) = −log(U₂|η(U)|⁴)  (tools/serapis_calc/shapes.py)
  k = [E(½+10i,2) − E(ρ,2)] / [Ê₁(½+10i) − Ê₁(ρ)]   (both pieces contribute equally between ρ and U₂ = 10; fixed now)
  w ∈ {0, 0.25, 0.5, 0.75, 1}; w = 1 is SERAPIS-E exactly (E_paper ≡ E(U,2), checked to 1e-15).
  Point: C = 1.25e-6, T_R = 8.94e8 GeV (the serapis_point arguments), λ = 1. Engine: pipeline.predict (exact spectra).

## Gate
G0: w = 1 must reproduce serapis_point (n_s = 0.97446 ± 2e-4, r = 4.81e-4 ± 2%). If G0 fails, nothing else is read.

## Locked questions and rule
(a) Which w give n_s ∈ [0.969, 0.975] AND r ∈ [4.55e-4, 5.7e-4] (the frozen band)?
(b) String weight: Ê₁ comes from R⁴ (order α'³), E(U,2) from D⁴R⁴ (order α'⁵), so in the controlled regime the physical
    E₂ share is suppressed, w_phys ~ (α'/R²)² ≪ 1 (stated now, before seeing (a)).
Rule: P3 → "derived (candidate)" only if the band admits w_phys ≪ 1 (i.e. small w passes (a)). If only w near 1 passes,
the verdict is: "the SERAPIS plateau needs the s = 2 term to dominate, which the controlled string expansion does not give —
P3 stays a postulate; blocker = order of the expansion" (unless a cancellation of the s = 1 piece is found later).
Expectation stated now: pure s = 1 (w = 0) approaches the plateau as U₂⁻¹ instead of U₂⁻², so it should give a smaller
r-steepness / different n_s than SERAPIS-E.
No reruns to chase results; fixes only via PREREG_D1364_DEVIATIONS.md written first.
