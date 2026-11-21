# PREREG Y4 — odd-flux |M| = 9 (SS phase 1/6) Z3 Yukawa hierarchy at tau = omega
Locked 21 Nov 2026 before any Yukawa is computed. Validation of the zero-mode Z3 action is DONE and recorded (theory/tests/z3_modes.py, least-squares C_k from 400 points, residual < 1e-14): multiplicities M=3:(1,1,1), 5:(2,2,1), 7:(3,2,2), 9 at (1/6,1/6):(3,3,3), (5/6,5/6):(3,3,3), (1/2,1/2):(4,3,2) — matches 1309.4925 Table 6 for odd M.

## Setup
- L on M=9, phase (1/6,1/6); R on M=9, phase (1/6,1/6); H on M=18, phase (1/3,1/3) (phases add under the product).
- Step 0 (gate): the product psi_L^i psi_R^j must expand in the M=18 (1/3,1/3) basis with relative residual < 1e-8; the Z3 action on that basis must close (residual < 1e-8). If either fails: record NULL (wrong phase bookkeeping), no rerun with other phases.
- Yukawa: c_ijk from the least-squares expansion psi_L^i psi_R^j = sum_k c_ijk psi_H^k(z) (common normalisation per flux; ratios only).
- Rotate L, R, H to Z3 eigenbases. Families: L = one 3-dim class, R = one 3-dim class; H in the class making the coupling Z3-invariant (determined numerically as the class where the projected coupling is nonzero). All 9 (class_L, class_R) pairs are examined.
- Higgs direction: 20000 Haar-random unit vectors in that H class (seed 7).

## Observable and threshold
Singular values y1 ≤ y2 ≤ y3 of Y_ij = sum_k c_ijk h_k. Target: charged leptons r12 = m_e/m_mu = 4.84e-3, r23 = m_mu/m_tau = 5.95e-2.
- PASS (natural hosting): for some class pair, ≥ 1 % of Higgs directions give both r12 and r23 within a factor 3 of target.
- WEAK (fit only): fraction > 0 but < 1 %.
- FAIL: no direction in 20000 for any pair. Reported either way with the best direction's ratios and the median ratios.
No rerun with other seeds, fluxes or phases to chase a result.
