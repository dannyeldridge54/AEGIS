# PREREG D845 (C.3): can a CP-invariant racetrack fix a Kähler axion at a CP-odd value?
Locked before computing, 2026-11-16.
Model: T = s + i t, K = −3 ln(−i(T − T̄)) = −3 ln(2t); W = W0 + A e^{iαT} + B e^{iβT}, α = 2π/N1, β = 2π/N2, all of W0, A, B REAL (CP: T → −T̄, s → −s, is a symmetry).
V = e^K (K^{TT̄}|D_T W|² − 3|W|²), e^K = (2t)^{−3}, K_T = 3i/(2t), K^{TT̄} = 4t²/3.
Period in s: L = lcm(N1, N2). CP-fixed values: s ≡ 0 or L/2 (mod L).
Scan: (N1, N2) with 5 ≤ N1 < N2 ≤ 10; W0 ∈ {±1e-4, ±1e-3, ±1e-2}; A ∈ {1}; B ∈ {±0.5, ±1, ±2} (overall sign of A absorbed). For each, locate local minima on a grid s ∈ [0, L) (400 pts), t ∈ [1, 60] (400 pts), refine with scipy minimize (Nelder–Mead) from each grid local minimum; keep minima with positive-definite numerical Hessian, t ∈ (1, 60).
Classify a minimum as CP-ODD if its distance (mod L) from both 0 and L/2 exceeds 1e-3·L.
Verdict rule: option (ii) is VIABLE if at least one CP-odd minimum with t > 2 exists; report the count and fraction of parameter points that have one, and the depth (AdS) relative to the deepest CP-even minimum at the same parameters.
Prediction (pre-stated): none. With real coefficients the two exponentials can interfere destructively only along CP-fixed lines; CP-odd minima occur, if at all, only for sign choices where the CP-fixed points are saddles.
