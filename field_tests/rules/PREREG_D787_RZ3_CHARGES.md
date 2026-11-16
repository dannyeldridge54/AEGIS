# PREREG D787: is requirement R-Z₃ satisfiable? MSSM Z₃ charges at ρ and the operators they allow
Locked 2026-11-16 before computing. Script: theory/modular/rz3_charges_d787.py. Output: field_tests/results/rz3_charges_d787.txt.
Fields (superpotential conventions): Q, U = u^c, D = d^c, L, E = e^c, H_u, H_d; charges mod 3.
Imposed (all allowed, since their coefficient forms are non-zero at ρ): QH_uU, QH_dD, LH_dE, H_uH_d (μ), LLH_uH_u (Weinberg, so q_L ≡ −q_Hu since 2 is invertible mod 3), and LH_uN_Y (N_Y neutral). This leaves free (q_Q, q_Hu) ∈ Z₃²: 9 assignments.
For each, compute the charge of the gauge-invariant operators:
- B/L-violating SM: UDD, QDL, LLE, QQQL, UUDE, LH_u;
- pair decays (heavy N of charge ±q, q ∈ {1, 2}): N·UDD, N·QDL, N·LLE, N·LH_u (renormalisable, expected forbidden), N·QQQL.
An operator is allowed iff its total charge is ≡ 0.
Report: for each assignment, (i) whether some dim-6 operator N·O is allowed for both q = 1 and q = 2 (N_n and N₃); (ii) which SM-only B/L-violating operators are allowed (proton safety); (iii) whether the assignment acts on gauge-invariant SM operators as a baryon-number triality (charge ∝ B mod 3).
Decision:
- R-Z₃ SATISFIABLE if some assignment allows a pair decay operator for both charges while forbidding QQQL and UDD at the SM level.
- If every assignment allowing a pair decay also allows QQQL or UDD, report CONFLICT with proton stability.
Anomaly cancellation (Ibáñez–Ross Z₃ conditions) is recorded from memory only (estimate).
