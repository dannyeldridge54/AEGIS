# PREREG R2a — generic single-channel Sommerfeld solver (relic module, stage R2a) — locked 2026-11-17
Plan for R2, so the full Sommerfeld freeze-out is staged:
- R2a: a generic single-channel solver, for the Q=±2 S=0 (repulsive α + α₂c_W² Yukawa_Z), Q=±1 (attractive α₂ Yukawa_W) and Q=0 S=1 (attractive) channels of Hisano+ hep-ph/0610249 Eqs. 2–4.
- R2b: the Q=0 S=0 two-channel problem with BOTH channels open (thermal E ≫ 2δm).
- R2c: thermal average (their Eq. 13) and freeze-out.
- R2d: ratio tests against Beneke+2020: LO/Born 1.308 and NLO/Born 1.288, with the NLO √2 convention fixed in advance. That is the blind A1e test.
R2a code (written after this lock): sommerfeld.single_channel(M, v, V, alpha_tail). It solves u'' = M(V − E)u from small r, takes the amplitude with WKB-local k at large R (the method validated in A7b), and returns S = |ψ(0)|².
Tests (scored):
- T1: attractive Coulomb V = −α/r vs the analytic S = 2πη/(1 − e^{−2πη}), η = α/v.
- T2: repulsive Coulomb V = +α/r vs −2πη/(1 − e^{2πη}).
- T3: Yukawa with m = 1e-7 GeV vs the attractive Coulomb analytic.
For α ∈ {0.01, 0.0335}, v ∈ {0.01, 0.1, 0.3}, M = 2000 GeV: max relative error ≤ 1e-4 (T1, T2) and ≤ 1e-3 (T3).
R2a VALIDATED iff T1–T3 pass. Fixes only via DEVIATIONS.
