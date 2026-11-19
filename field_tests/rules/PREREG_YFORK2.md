# PREREG_YFORK2 — which exit does the thread take at the Y-fork? Two-field end-of-inflation dynamics (locked D1606, 2026-11-19 12:50 CT)
Model: L = ½R − (ẋ² + ẏ²)/(4y²) − V, V = V₀(x,y)[1 + C(E − E_ρ)], V₀ = (4/9)y²|∇ ln E(τ,3/2)|², C = 8e-7, units V∞ = M_P = 1.
EOM (hyperbolic sigma model, G = δ/(2y²)): ẍ − (2/y)ẋẏ + 3Hẋ + 2y²∂ₓV = 0; ÿ + (ẋ² − ẏ²)/y + 3Hẏ + 2y²∂ᵧV = 0; H² = [(ẋ² + ẏ²)/(4y²) + V]/3.
ln E is tabulated on x ∈ [−0.3, 1.3] × ln y ∈ [ln 0.6, ln 25] (241 × 400) and splined (quintic); V and ∇V come from spline derivatives. Validation: spline V₀ against direct values at 5 test points, |Δ| < 1e-5 (else INVALID).
Initial conditions: y₀ = 20 on the slow-roll attractor (ẏ from slow roll, ẋ = 0), x₀ = ½ + δx with δx ∈ {0, 1e-6, 1e-4, 1e-3, 1e-2, 3e-2} (sign + only; the problem is symmetric under x → 1 − x).
Integrate (Radau, rtol 1e-9) until t = 2000/√V∞ or until the kinetic energy has fallen below 1e-10 near a minimum.
Outcome per run: the final (x mod 1, y) and its classification: "ρ" if within 0.05 of (½, √3/2), "i" if within 0.05 of (0 or 1, 1), "other" otherwise. Also report N (e-folds) from y₀ to the end of inflation (ε = 1).
Report the δx threshold, if any, above which the thread exits to i. No reruns to change the δx list.
Script: field_tests/scripts/yfork/run2.py
