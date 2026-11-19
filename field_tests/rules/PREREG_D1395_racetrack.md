# PREREG D1395 — can a racetrack stabilise S with W_S/W ≈ −2e-3 (the D1394 tilt condition)?

Locked 2026-11-18 before computing (Danny "Djl", P3 hunt).

Toy (real slice, axion ignored): s = Im S, L = s + δ (δ = Y/16π² ≈ 0.5, fixed), K = −log L,
W(s) = A e^{−a s} − B e^{−b s}, a = 2π/N, b = 2π/M (SU(N) × SU(M) condensates), A = 1.
V(s) = L·W_s² − 2W·W_s + (c − 2W²)/L (D1394; real W, W_s), c ≥ 0 an extra positive F-term (scan).
Scan: (N, M) ∈ {(5,6), (6,7), (8,9), (9,10), (10,12)}, B ∈ {0.5, 1, 1.5, 2, 3}, c/A² ∈ {0, 1e-6, 1e-4, 1e-2} × e^{−2a s_typ} … 
  (c is scanned as c = κ·W(s)² at the candidate point, κ ∈ {0, 0.5, 1, 1.5, 1.9}), s ∈ (0.5, 60) grid of 20000 points.
Question: does any setting have a LOCAL MINIMUM of V(s) (V' = 0, V'' > 0, interior) at which W_s/W ∈ [−1e-2, −1e-3]
and B_eff = 2W² − c > 0 (plateau sign) and A₀ = −2WW_s > 0 (uplift sign)?
Report: number of settings with such a minimum; for each, (N, M, B, κ, s*, W_s/W). Also report the distribution of W_s/W over
ALL local minima found. Rule: "condition realisable (toy)" if ≥ 1 setting qualifies; else "not realisable in this racetrack toy".
No reruns to chase results; fixes only via PREREG_D1395_DEVIATIONS.md written first.
