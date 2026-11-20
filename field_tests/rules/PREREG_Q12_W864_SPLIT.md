# PREREG Q12 — the paper's own modified model (forms of weight 8, 6, 4; arXiv:2212.13336 §4.5 Eqs. 55–56) on the split ladder (locked 2026-11-20, before computing)
LABEL: second model, chosen AFTER Q8 failed (it is the paper's own suggested fix). Its single-modulus fit needs f_u ≈ 30 (not O(1)).
Question: on the split ladder (down rung 1, up rung 8/9/10/13) can it fit with ALL couplings O(1)?
(Rung 13 is added because the paper's own two-moduli fit has |ε_u| = 0.00192 ≈ rung 13; that choice is post-hoc and labelled.)
M_q = diag(α,β,γ)·[[Ỹ₁⁽⁸⁾, Ỹ₃⁽⁸⁾, Ỹ₂⁽⁸⁾],[Ỹ₂⁽⁶⁾, Ỹ₁⁽⁶⁾, Ỹ₃⁽⁶⁾],[Y₃⁽⁴⁾, Y₂⁽⁴⁾, Y₁⁽⁴⁾]], Ỹ⁽⁸⁾ = Y⁽⁸⁾ + f Y′⁽⁸⁾, Ỹ⁽⁶⁾ = Y⁽⁶⁾ + g Y′⁽⁶⁾.
Y⁽⁸⁾ = (Y1²+2Y2Y3)(Y1²−Y2Y3, Y3²−Y1Y2, Y2²−Y1Y3); Y′⁽⁸⁾ = (Y3²+2Y1Y2)(Y2²−Y1Y3, Y1²−Y2Y3, Y3²−Y1Y2) (paper App. B); weight 6, 4 as in Q8.
VALIDATION: rank 1 at τ = ω (σ₂/σ₁ < 1e-10) for random couplings. If it fails, the assignment is wrong: stop, record.
O(1) box per sector: β/α, γ/α ∈ [1/3, 3]; |g|, |f| ∈ [1/3, 3], any phases. Same search, targets and tolerances as Q8. Same CONTROL (both at rung 1).
PASS for a rung if a point inside the box meets every Q8 tolerance. No reruns; no new box.
