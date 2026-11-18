# PREREG PW7 — web postulate 7: the string benchmark's own heavy-ν mass (σ = ½ instanton, M = 9.8e10 GeV, D861) in the ρ reheating + leptogenesis chain
Locked 2026-11-18 04:56Z before computing. Pattern: PW2's point uses M_H = 1e12 GeV (chosen), but the same string benchmark (g_s 0.232, Im S·Im ρ 781, C 1.25e-6) gives M_H = 9.8e10 from a σ = ½ instanton (D861). Postulate: the benchmark is self-consistent only if its own M_H also reheats and makes the baryon asymmetry.
Compute (scripts = NA6 copies, only M_H changed; c ∈ {0.3, 1, 3}):
 (1) T_R at M_H = 9.8e10 with tr_2p1 (m_φ 3.1746e13, n = 1), SM g* as in NA6, then ×0.82652 for MSSM g* (A1);
 (2) leptogenesis pass fractions (D775/NA6 grid, m1 = 1e-4, 1e-3 eV) at those T_R (SM-g* T_R as NA6 did for comparability);
 (3) for c = 1: N*, n_s, r, α_s with predict_fast (C 1.25e-6, MSSM g*, T_R(MSSM)).
Pre-stated expectation: T_R ∝ M_H ⇒ T_R(c=1) ≈ 8.8e7 (SM) / 7.2e7 (MSSM); ε ∝ M_H and Y_B ∝ T_R·ε ∝ M_H² ⇒ yields ×~1e-2 ⇒ leptogenesis FAILS the locked 10 % rule for every c (expectation: FAIL = tension). N* ≈ 50.18 − ⅓ln(10.2) ≈ 49.41, n_s ≈ 0.9736.
Reading: FAIL ⇒ node instanton_MH (status postulate, killed-or-tension) records that the benchmark's instanton M_H and thermal leptogenesis at ρ are incompatible — either a different instanton/σ or non-thermal leptogenesis is needed; PASS ⇒ benchmark self-consistent, point moves to the new N*.
Script field_tests/scripts/pw7.py. Results field_tests/results/pw7_instanton_MH.txt.
