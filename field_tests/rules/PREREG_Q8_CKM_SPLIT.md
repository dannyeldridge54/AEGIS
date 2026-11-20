# PREREG Q8 — CKM from the split ladder: down quarks on rung 1, up quarks on rung 8/9/10 (locked 2026-11-20, before computing)
Model: arXiv:2212.13336 Eq. 23 (A4, level 3; Q triplet weight 2; singlets 1,1″,1′ weights 4,2,0), RL convention, CKM = U_uL† U_dL,
U_qL diagonalises M_q†M_q. M_q = diag(α, β, γ)·[[Ỹ₁⁽⁶⁾, Ỹ₃⁽⁶⁾, Ỹ₂⁽⁶⁾],[Y₂⁽⁴⁾, Y₁⁽⁴⁾, Y₃⁽⁴⁾],[Y₃⁽²⁾, Y₂⁽²⁾, Y₁⁽²⁾]], Ỹ⁽⁶⁾ = Y⁽⁶⁾ + g Y′⁽⁶⁾.
Forms: weight-2 triplet from Dedekind η (Feruglio 1706.08749, our run.py); Y⁽⁴⁾ = (Y1²−Y2Y3, Y3²−Y1Y2, Y2²−Y1Y3);
Y⁽⁶⁾ = (Y1³+2Y1Y2Y3, Y1²Y2+2Y2²Y3, Y1²Y3+2Y3²Y2); Y′⁽⁶⁾ = (Y3³+2Y1Y2Y3, Y3²Y1+2Y1²Y2, Y3²Y2+2Y2²Y1).
VALIDATION (must pass): at τ = ω the matrix has rank 1 with rows ∝ (1, −2ω², −2ω), (−ω/2, 1, ω²), (−ω²/2, ω, 1) (paper Eq. 25), to 1e-10.
Moduli (Q11 computed minima): τ_d = −0.484440+0.884238i (rung 1); τ_u ∈ {rung 8 −0.497988+0.868420i, rung 9 −0.498207+0.868153i, rung 10 −0.498421+0.867971i}.
O(1) couplings per sector: β/α, γ/α real in [1/3, 3]; g complex, |g| ∈ [1/3, 3], any phase. (Canonical-normalisation factors absorbed.)
Search: 2e5 random points per rung, then Nelder–Mead from the best 20 on a log-χ², parameters clipped to the O(1) box.
Targets (M_Z): m_s/m_b 0.0199, m_d/m_b 1.00e-3, m_c/m_t 3.72e-3, m_u/m_t 7.6e-6, |V_us| 0.2250, |V_cb| 0.0418, |V_ub| 0.00369, J 3.08e-5.
PASS for a rung if a point inside the O(1) box reproduces: mass ratios within ×/÷1.5, |V_us| ±10%, |V_cb| ±20%, |V_ub| ±30%, J ±50%.
Report the best point and which observables fail. Also report the SAME search with ONE shared modulus (both at rung 1) as the control.
No reruns; no new box or tolerances afterwards.
