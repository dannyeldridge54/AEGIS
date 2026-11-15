# PREREG D490 — design and test a duality-symmetric ("as above, so below") Twist (Danny 20:29 CT "Design one that does"), locked before computing.
DESIGN. With K = −3 ln(T+T̄) and W = S·F(T), V = |F|²/(T+T̄)³. Take G = the Twist's F (μ = 1, m₂ = 4/π, ε) and define
  F_sym(x) = G(x) + x³ G(1/x).
Then F_sym(1/x) = x^{−3} F_sym(x), so V_sym(1/x) = V_sym(x) exactly (T-duality / modular-type symmetry on the real line). Inflation runs on the small-x plateau,
its mirror sits at large x, and the self-dual point x = 1 is the fixed point where both meet. There the capture root is symmetry-enforced (the two brane phases
are swapped by the duality, so their difference vanishes at x = 1), and Λ = V_sym(1).
TESTS (numerical, slow roll in canonical φ = √(3/2) ln x):
 (0) Control: the original Twist (G alone, n = 124.1, ε = 0 and ε = 3.04e-7) must reproduce n_s ≈ 0.9651 / 0.9736 at N* = 57.2 within ±0.002, else the code is wrong (report and stop).
 (i) Check V_sym(1/x) = V_sym(x) numerically to 1e-10 relative.
 (ii) Fix n by Λ: V_sym(1)/V_sym(x*) = 6e-111 (Λ = 2.5e-47 GeV⁴ over V_inf ≈ 4e63 GeV⁴), x* = the N* = 57.2 point (iterate).
 (iii) With that n (ε = 0 and 3.04e-7): n_s, r at N* = 57.2. PASS if |n_s − 0.9728| ≤ 2×0.0027 and r < 0.036.
Verdicts: "SYMMETRIC TWIST VIABLE" if (i)–(iii) pass for at least one ε; "SYMMETRY KILLS INFLATION FIT" otherwise. No reruns; fixes via _DEVIATIONS first.
