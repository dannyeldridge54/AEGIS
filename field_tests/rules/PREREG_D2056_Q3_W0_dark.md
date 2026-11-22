# PREREG D2056: Q3, can the dark condensate play the role of W₀ (flux W₀ = 0 at the symmetric point ρ)? Locked before computing.
**Referee pre-check (formula):** SUSY vacuum D_iW = ∂_iW + K_iW = 0 for i = T_v, T_d.
- Toy Kähler potential K = −2 ln(t_v^{3/2} + t_d^{3/2}), real parts only.
- W = A_v e^{−a_v t_v} + A_d e^{−a_d t_d}, with a_v = 2π/6, a_d = 2π/12, A_v = 0.54.

**Test:** scan A_d ∈ ±[0.01, 100]. Solve both F-flatness conditions numerically for (t_v, t_d) > 1.

**Verdict:**
- **PASS** if a solution exists with t_v within 10% of 20.15 and natural |A_d| ∈ [0.1, 10].
- **FAIL** if no solution exists with t_v and t_d > 1, or only with unnatural A_d.
