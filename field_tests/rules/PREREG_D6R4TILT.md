# PREREG D6R4TILT — shape from R⁴, tilt from D⁶R⁴: the tilt as the ratio of the next string-derivative coefficient to the R⁴ one

Locked 2026-11-19 (10:40 CT) before computing. 1-min derivation loop (Danny 10:33 "loop 1 min till derivation").
[literature] 10D IIB D⁶R⁴ coefficient f(τ) (Green–Miller–Vanhove et al., arXiv:1404.2192): (Δ − 12)f = −(2ζ(3)E_{3/2})² (Δ = y²(∂ₓ² + ∂ᵧ²)),
zero mode f₀ = (2ζ(3)²/3)y³ + (4ζ(2)ζ(3)/3)y + 4ζ(4)/y + c₃/y³ (c₃ not quoted there — omitted; non-zero modes ~e^{−2πy} omitted: both
negligible for y ≳ 3, i.e. wherever the tilt matters).
Postulate (candidate): the tilt is the D⁶R⁴/R⁴ coefficient ratio, X = f₀/E(τ,3/2) → (ζ(3)/3)y^{3/2} at large y (a T3-class y^{3/2} tilt),
with C = κ·(H/M_s)⁶, κ an O(1) background factor (on-shell value of D⁶R⁴/R⁴ invariants — unknown, the Weyl obstacle of D1526 applies).
Run: P3-S shape (G32 lens code) × (1 + C·(X − X_ρ)), engine F, T_R 8.94e8; C on the quarter-decade grid 10^{k/4}, k = −28 … −16.
Report: band interval in C, r and α_s at n_s 0.9706; then the implied H/M_s = (C/κ)^{1/6} for κ ∈ {0.1, 1, 10}, and the implied
string scale M_s = H/(H/M_s) vs the D1528 window (H = 5.8e12 < M_s ≪ 2.2e15 GeV).
Expectation stated now: band at C ≈ 6·8e-7 ≈ 4.8e-6 (the T3 band rescaled by 2ζ(3)/(ζ(3)/3) = 6), r ≈ 5.4e-4; H/M_s ≈ 0.13 for κ = 1,
i.e. M_s ≈ 4e13 GeV — inside the window. Whether κ is O(1) (or zero on FRW) is the open link; this run checks consistency, not κ.
No reruns to chase results; fixes only via PREREG_D6R4TILT_DEVIATIONS.md written first.
