# PREREG D1829 — CP violation from the D1828 quark lock (locked 21 Nov 2026 before computing; repo at 1c20dc5a)
Finding before the computation (stated): with c_ij = 1 the texture M_ij = u^{q_i + q_j} is rank 1, and the modular phases (n·arg u) factorise and can be rephased away. So both the light masses and CP require generic complex O(1) coefficients. D1828's fit was a scaling estimate; this test makes it a matrix test.
Model: M_u = c^u_ij u_u^{q_{Qi} + q_{uj}}, M_d = c^d_ij u_d^{q_{Qi} + q_{dj}}, with the D1828 charges; c_ij = r e^{iθ}, r log-uniform in [0.5, 2], θ uniform; 20000 draws (seed 21). The complex u (arg from τ − ρ = ε at 50°/49°) is included.
Outputs per draw: mass ratios, |V_us|, |V_cb|, |V_ub|, J = Im(V_us V_cb V_ub* V_cs*), δ (PDG convention).
Verdicts:
(1) MATRIX CONSISTENCY: the fraction of draws with all 4 mass ratios within ×3 and all 3 |V| within ×3 = f₇; PASS if f₇ ≥ 5 %.
(2) CP: among those draws, the fraction with J within ×3 of 3.08e-5 = f_J; PASS if f_J ≥ 20 %, and report the median δ.
