# PREREG D396 — Twist-2 open problem 1: does χ pin x at x_E without a moduli problem? (locked 13:30 CT 14 Nov 2026, before running)

Script: theory/twist2/pinning_d396.py (semi-analytic chain, estimate-grade; conventions stated in the docstring).
Inputs: crossing points from D367b (x_E = 29.21 / 29.45 / 29.60 at T = 3.9 / 2.4 / 1.5 ×10¹¹ GeV, dp = 2.5 / 1.5 / 0.93 ×10⁻²);
λ ∈ {0.004, 0.01, 0.033} (D377 window); condensate scale v = T_c ∈ {10⁵, 10⁶, 10⁷, 10⁹} GeV; g = λ x_E √(2/3) (canonical coupling;
the weight-3/2 e^{K/2} factor cancels); thermal trap frequency gT/2; condensate mass m_x = g v; decay Γ = m_x³/(8π M_P²).
Pass criteria for a scan point: (i) trapped (kinetic energy at crossing < barrier T⁴/4); (ii) T_d ≥ 5 MeV; (iii) dilution D ≤ 10³
(absorbable by leptogenesis, D394).
Reading: PASS if at least one point with λ in the window meets (i)–(iii) for ALL three λ values at the same (x_E, v) ("robust");
WEAK PASS if only some λ; FAIL if none. Report the D range, since D > 1 also dilutes gravity-only DM (its mass window would shift by D).
Limits: estimate-grade (O(1) factors in m_th, m_x, Γ unfixed); not a field-theory computation. No reruns; fixes via DEVIATIONS first.
