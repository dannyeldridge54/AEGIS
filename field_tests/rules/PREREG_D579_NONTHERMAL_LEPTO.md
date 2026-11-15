# PREREG D579: non-thermal leptogenesis from inflaton decay for the D578 models, locked before computing

Formula (Ding et al., arXiv:2411.18603, eq. 4.29):
- Y_B = (8/23)(3/4)(T_RH/m)·ε₁·2·Br(φ → N₁N₁).
- Upper bound by Davidson–Ibarra (hierarchical N): ε₁ ≤ 3M₁m₃/(16πv²), with m₃ = 0.05 eV and v = 174 GeV.
- Cases: Br = 1, with M₁ = m/3 (allowed by phase space) and M₁ = m/2 (the kinematic edge, giving the absolute maximum).

Inputs: m and T_RH from results/osc_nstar_d578.txt (all 12 rows), as printed. No recomputation.
Target: Y_B ≥ 8.75e-11.
Report per row: Y_B,max for both M₁ choices, and the pass/fail flag.
Also report the analytic threshold T_RH,min that this bound implies, which is independent of m: T_RH,min = Y_B / [(6/23)·2·(3/16π)·(M₁/m)·m₃/v²].
Caveat (stated now): the T_RH convention (90/π²g*)^{1/4} differs from the paper's √(2/π)(10/g*)^{1/4} by about 20%. Resonant leptogenesis (quasi-degenerate N) can exceed the Davidson–Ibarra bound; it is noted, not used.
Fixes go in PREREG_D579_DEVIATIONS.md, written first.
