# PREREG DIM3_7D — dimension ladder stage 3 (D = 7, SL(5)): the τ-slice of the R⁴ codon is E_{3/2}(τ) + c with c of EITHER sign

Locked 2026-11-19 (11:08 CT) before computing. Dimension-ladder loop.
[literature] GRV 1001.2535: E⁽⁷⁾ = E^{SL(5)}_{[1000];3/2} (eq. 6.5), eigenvalue −12/5; constant terms (B.71) r^{6/5}E^{SL(4)}_{[001];3/2} + 4ζ(2)r^{16/5};
(B.72) r^{12/5}(Ê^{SL(3)}_{3/2} + 2Ê^{SL(2)}_{[1];1} + 8π log r), with Ê^{SL(3)}_{3/2} = ν₂^{−1/2}E_{3/2}(Ω) + (4π/3) log ν₂ + ….
Derived before computing: along τ (= Ω) at fixed other moduli the codon is ∝ E_{3/2}(τ) + c, c = ν₂^{1/2}[(4π/3) log ν₂ + 2Ê₁(U) + 8π log r + …]
— unlike 9D (c = 4ζ(2)ν₁ > 0), the 7D c contains logarithms and can be NEGATIVE. c < 0 makes y∂ ln(E + c) = (y∂ ln E)·E/(E + c) > its
asymptote ⇒ the plateau is approached from ABOVE (overshoot/bump), c > 0 from below (the 9D warp toward k = 3/2).
Runs (script field_tests/scripts/dim/dim1_9d.py — same V₀ = (y∂ ln(E_{3/2} + c)/1.5)², engine F, untilted): c ∈ {−0.658, −6.58}
(9D runs cover c ≥ 0: D1568).
Expectation stated now: c < 0 ⇒ no inflation into ρ or a hilltop with n_s far from the band (INVALID as plateau); so the 7D lens keeps the
rung only on the c ≥ 0, small-|c| side (large r, ν₂ ≈ 1 region where the logs nearly cancel).
No reruns to chase results; fixes only via PREREG_DIM3_7D_DEVIATIONS.md written first.
