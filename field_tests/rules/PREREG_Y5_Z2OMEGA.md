# PREREG Y5 — lepton hierarchy on magnetised T²/Z2 at tau = omega, fluxes (4,4,8), multi-Higgs direction
Locked 21 Nov 2026 before computing. Motivation: Y4 (D1790) FAIL on T²/Z3 at omega; arXiv:2112.01680 gets the QUARK hierarchy on T²/Z2 (4-4-8) at tau = omega with tuned Higgs angles (~0.08–0.14 rad), and leaves leptons open. 1806.10369 says charged leptons fail for Z2 at Re tau = 0 (not at omega).

## Setup
- Z2-even zero modes: psi_even^j = (psi^j + psi^{M-j})/√2 (j = 1..M/2-1), psi^0, psi^{M/2}; no SS phase. L: M=4 (3 modes), R: M=4 (3), H: M=8 (5 modes, 5 complex Higgs directions).
- Gate: product psi_L psi_R expands in the M=8 even basis with residual < 1e-8; else NULL.
- Yukawa Y_ij = sum_k c_ijk h_k (common normalisation; ratios only).
## Observables, thresholds
Target r12 = m_e/m_mu = 4.84e-3, r23 = m_mu/m_tau = 5.95e-2. Also report the same for the down quarks (6.86e-4·... use m_d/m_s = 0.050, m_s/m_b = 0.0137... as a CONTROL: the control must succeed, else the code is suspect and the result is NULL).
- (i) Haar fraction: 50000 random h (seed 11) with both ratios within ×3 of target.
- (ii) Best fit: Nelder–Mead on the 10 real Higgs parameters, 40 starts (seed 12), loss = (ln r12/t12)² + (ln r23/t23)².
- PASS (natural): fraction ≥ 1 %. HOSTED (tuned fit): fraction < 1 % but the best fit within 10 % on both ratios. FAIL: best fit worse than ×2 on either ratio.
No rerun with other fluxes, tau or seeds.
