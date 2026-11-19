# PREREG_YFORK — the Y-fork ("Genesis split") test on the Weave potential (locked D1605, 2026-11-19 12:46 CT)
Postulates recorded (Danny 12:41–12:42): P-X, a reverse-tied X (axion/twist) strand; P-Y, a Y-formation where the single thread splits into two branches ("destruction, then expansion; fission/fusion; Genesis").
Concrete test: the inflaton runs down the line x = ½. If the transverse curvature ∂²V₀/∂x² on x = ½ changes sign at some y_c, the valley turns into a ridge there and the thread forks into two mirror branches x = ½ ± δ(y). The branches are CP conjugates, so the fork itself is a spontaneous CP split.
Compute V₀(x, y) = (4/9) y² |∇ ln E(τ, 3/2)|² (Euclidean ∇ in x, y; the Zhinü factor) with the repo's E. Curvature by central differences (h = 1e-4) on x = ½ at 60 log-spaced y ∈ [0.87, 6].
Report: the sign pattern, any y_c (bisection to 1e-5), and if a fork exists the branch offset δ(y) (minimise V₀ in x at fixed y) at 10 points below y_c, plus where the branches end.
Pass/fail: "FORK EXISTS" if the sign changes with |curvature| above 1e-10 on both sides; else "NO FORK on x = ½".
Script: field_tests/scripts/yfork/run.py
