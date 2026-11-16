# PREREG D730: does the octic (stiff) phase end before the inflaton decays at τ = i with the D727 width?
Locked 2026-11-16 before computing. Script: theory/modular/octic_decay_d730.py (imports chronos_tr_d729.py's functions). Output: field_tests/results/octic_decay_d730.txt.
## Code reading (done before locking)
In nstarT, 'w=3/5' means: stiff phase from ρ_end to ρ_A = max(min(ρ_x, ρ_end), ρ_R), then matter to ρ_R. 'w=0' means matter-like throughout (the conservative bracket).
## Computation (fixed now)
For ε ∈ {1.3e-4, 1.6e-4}: ρ_x, H_x = √(ρ_x/3)/M_P, and m (the vacuum mass from the same code). Compare H_x with Γ = 1.44e-6 – 1.30e-5 GeV (D727, M/m 0.1–0.45). During the octic phase ω/H ∝ ρ^{-1/8} (ω ∝ ρ^{3/8}), so decay during the octic phase is negligible if Γ(m) ≪ H_x (estimate, stated).
## Decision rule
- If Γ ≪ H_x for all rows: the physical history is octic → matter → radiation, i.e. the D729 'w=3/5' rows are physical and the 'w=0' rows are only a conservative bound. Then the τ = i frozen band is matched only partly (per D729), recorded as a correction.
- If Γ ≳ H_x: decay during the octic phase; the history is nearer 'w = 3/5 to ρ_R' and the analysis must be redone.
- Fixes only via D730_DEVIATIONS.md.
