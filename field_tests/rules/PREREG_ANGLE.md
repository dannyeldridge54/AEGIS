# PREREG ANGLE — inflaton trajectory at an angle θ between the dilaton and the volume: does the angle supply the P3-S tilt?

Locked 2026-11-19 (10:28 CT) before computing. Danny 10:23: "the particles that split take the dark energy … the angle changes at each
dimension"; 10:24 "set up the calculation, on a free core local or cloud".
Model (straight-line reduction, stated as an approximation — orthogonal dynamics ignored):
  canonical dilaton φ₁ = ln y/√2 (K = −ln(2y)); canonical volume χ with K = −3 ln(T + T̄) ⇒ χ = √(3/2) ln(T + T̄);
  a dilaton-independent D7 D-term scale (D1549) V_D7 ∝ (T + T̄)^{−3} = e^{−√6 χ};
  trajectory φ₁ = ψ cos θ, χ = −ψ sin θ (the volume shrinks as y grows, θ ≥ 0), ψ canonical;
  V(ψ) = S(y(ψ)) · e^{√6 ψ sin θ}, y = e^{√2 ψ cos θ}, S = the P3-S species shape (2/3·y∂_y ln E(τ,3/2))² (D1546), no hand-put tilt.
  For small θ the volume factor is a multiplicative power tilt y^{p}, p = √3·tan θ.
Grid: θ ∈ {0, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1} rad. Engine F (T_R 8.94e8), D1 start rule, 5-point stencil.
Report: n_s, r, α_s, N*, y*; in band / near; θ interval in band by interpolation; effective p.
Expectation stated now: θ = 0 reproduces untilted P3-S (0.96006 / 4.04e-4); a band crossing may exist near θ ~ 0.01 (p ~ 0.02) but with r
rising fast — a multiplicative y^p tilt is between the log and y^{1/2} classes, which D1531 found 1 % short in r; so "no band" is likely.
No reruns to chase results; fixes only via PREREG_ANGLE_DEVIATIONS.md written first.
