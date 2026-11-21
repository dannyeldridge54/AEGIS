# PREREG_RW7_UPLADDER — the dark-dimension "up-ladder" against the Weave's own scales (plan item 3)
Locked 21 Nov 2026 before computing. AI-assisted. Script theory/tests/rw7_upladder.py; result field_tests/results/rw7_upladder.json.

## Inputs
Dark dimension radius R ∈ {1, 2, 5, 7.4, 10} μm (2205.12293 window; 7.4 μm = the Casimir value of D1622).
m_KK = 1/R; species scale Λ_sp = m_KK^{1/3} M_P^{2/3} (D1622 convention) and the 2π variant
Λ_sp' = (m_KK/2π)^{1/3} M_P^{2/3} (report). ħc = 1.9733e-16 GeV·m, M_P = 2.435e18 GeV.
Weave scales: H_inf = 5.8e12 GeV, M_N ≥ 4.5e10 GeV, T_R = 3.74e8 GeV (D1801), scalars 4.7e5 GeV, m₃/₂ = 2.5e5 GeV.

## Checks (each: OK if the scale is below Λ_sp, i.e. inside the 4D+1 EFT)
- C1 H_inf < Λ_sp; C2 M_N < Λ_sp; C3 T_R < Λ_sp; C4 scalars < Λ_sp; C5 m₃/₂ < Λ_sp.
- C6 KK-graviton overproduction if the dimension is already open at reheating: the D1625 measure
  X = (T_R R)·T_R/M_P (number of accessible KK modes × the per-mode gravitational production rate relative
  to Hubble). OK if X < 1.
## Verdict
- HARD CONFLICT if C1, C2 or C6 fails at every R in the window (any one of them).
- CONSISTENT if all pass at some R.
- TENSION otherwise.
If HARD CONFLICT, the up-ladder can only be a late (post-reheating) opening, which D1625 already found needs
≥ 28 e-folds of radion kination, so row 3 of the mirror table would stay "≈ (direction only)".
