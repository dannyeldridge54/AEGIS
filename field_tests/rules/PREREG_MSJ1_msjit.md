# PREREG MSJ1 — compiled exact single-field MS reference (numba) vs ms.spectra_fast
Locked 2026-11-17 19:20 CT before the equivalence run (one probe on TI α=0.1 μ=10 while writing: Δn_s 1.6e-9 at rtol 1e-11, 10.1 s → 0.60 s).
Code: tools/serapis_calc/ms_jit.py (spectra_fast's equations; background + all k in one compiled ODE; DP5(4); analytic dV from sympy instead of the 1e-6 central difference).
Setting: rtol 1e-11. Models: the 12 scored J7m points' models (TI ×6, SFI p=3 ×2 parameter sets) at N* = 50 and 60 with J7b settings (9 k on [−1, 1], bd 1000),
start y0 as built by j7m_grid.build (16 comparisons).
Claim M1: |Δn_s| ≤ 1e-7, |Δr/r| ≤ 1e-6, |Δα_s| ≤ 1e-7 on all 16, AND median speed-up ≥ 10× (compile excluded). Pass → ms_jit adopted as the exact reference ("ms-jit")
for new locks; fail → not adopted.
