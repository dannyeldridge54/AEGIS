# PREREG D789: P5 consistency (the colour-triplet mediator X, X̄)
Locked 2026-11-16 before computing. Script: theory/modular/p5_test_d789.py. Output: field_tests/results/p5_test_d789.txt.
Superfields: X ~ (3, 1, +2/3) and X̄ ~ (3̄, 1, −2/3), with mass M_X·XX̄. P5 couplings: y₁·N·U·X and y₂·X̄·D·D (U = u^c (3̄, −2/3), D = d^c (3̄, +1/3)).
(1) Z₃: for D787's six q_Hu ≠ 0 assignments, and N charge q ∈ {1, 2}, set q_X = −q − q_U and q_X̄ = −2q_D. Check that M_X·XX̄ is allowed (q_X + q_X̄ ≡ 0).
(2) Enumerate every renormalisable gauge-invariant superpotential term with one X or X̄ and SM fields (bilinears and trilinears from {Q, U, D, L, E, H_u, H_d}), using SU(3) singlet and hypercharge checks in code. Report which are gauge-allowed, then Z₃-allowed. Dangerous = any that, with X̄DD or NUX, gives proton decay without N (e.g. X̄QH_u, XQQ, XUE, XLD …).
(3) Matter parity (D661: SM matter odd, Higgs and N's partner structure as in the paper): X and X̄ even; check NUX and X̄DD are even.
(4) Prompt decay: Γ = y²M/(16π) for y ∈ {0.02, 0.2}, M ∈ {4.3e11, 1e12}, against H(T_R = 3e8) = 1.66√g*·T²/M_P.
Decision: P5 PASSES if (1) is consistent for some assignment, (2) has no Z₃-allowed dangerous coupling, (3) holds, and (4) gives Γ ≫ H.
