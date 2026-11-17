# PREREG S4e2 — validate the S4e scalar-mass solver by an independent method (BTR's 2-sig-fig numbers kept as context only)
Locked 2026-11-17 before any S4e2 number. Same operator, background, cutoffs and Dirichlet BC as S4e (D1141). Method B: z(y) by cumulative quadrature on a
dense y-grid; U(z) interpolated onto a uniform z-grid; second-order finite differences with Dirichlet ends; lowest two eigenvalues by scipy eigh_tridiagonal;
N = 4000 and N = 8000 (Richardson-checked). Claim V2: method B and S4e's Prüfer m² (2.97956, 14.28653) agree within 0.5% for both modes, AND N=4000 vs 8000
agree within 0.2% → SOLVER VALIDATED (independent). Then run both methods on our 6D subcritical vacuum (S4b), same cutoffs as S4e, and report m₁, m₂ in π/L
and m₂/m₁ (claim only: lowest m² > 0 and the two methods agree ≤ 0.5%). BTR's 0.97/2.13 reported as context (D1141: −4%, 2 sig. figs, no stated method).
Results: field_tests/results/s4e2_independent.txt.
