# PREREG D770: after inflation, where does SERAPIS-E settle for x₀ ≠ ½?
Locked 2026-11-16 before computing. Script: theory/modular/axion_relax_d770.py. Output: field_tests/results/axion_relax_d770.txt. A NEW question (not a rerun of D769).
Model: as D769 after DEVIATIONS D1 (V = Ê/(Ê + 1)(1 + CÊ), C = 1.15e-6, E via D692's Ese with 30 Bessel terms; metric G = 1/(2y²)).
Equations in cosmic time (V0 = 1, M_P = 1):
- ẍ − (2/y)ẋẏ + 3Hẋ + 2y²V_x = 0
- ÿ + (ẋ² − ẏ²)/y + 3Hẏ + 2y²V_y = 0
- H² = [(ẋ² + ẏ²)/(4y²) + V]/3
Start: late in inflation at y = 3 with x = x₀ and the slow-roll velocity. D769 shows x is frozen until y ≈ 2, so this is equivalent to D769's trajectories.
x₀ ∈ {0.5, 0.45, 0.4, 0.3, 0.2, 0.1, 0.05, 0.02}.
WHEN judged: the final position is read when the total energy density first falls below 1e-4 × V(end of inflation). Stop with flag LOST if y < 0.2 (series accuracy) or t exceeds 5e4.
Final τ is reduced to the fundamental domain. Outcome per run:
- RHO if |τ_red − ρ| < 0.05 or |τ_red − ρ̄'| < 0.05, with ρ' = −½ + i√3/2;
- I if |τ_red − i| < 0.05;
- OTHER otherwise.
K4: x₀ = ½ must give RHO with x_final = ½ to 1e-6.
Decision: P3 PASSES the relaxation test if all runs with x₀ ∈ [0.05, 0.5] give RHO (the measure ≥ 0.9 of [0, ½], by the x → 1 − x symmetry). Otherwise FAIL, recording the basin edge.
