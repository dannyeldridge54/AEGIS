# PREREG D2072: P8, W₀ from a second condensate on the same visible cycle (racetrack with flux W₀ = 0). Locked before computing.
**Referee pre-check (formula):**
- W = A e^{−aT} − B e^{−bT}, with a = 2π/6 (v4) and b = 2π/N′.
- K = −3 ln(T + T̄). The SUSY condition D_T W = 0 at real t reads −aA e^{−at} + bB e^{−bt} − (3/2t)(A e^{−at} − B e^{−bt}) = 0.
- A = 0.54 (v4).

**Test:** for N′ ∈ {5, 7, 8, 9, 10, 12}:
- solve for the B that puts the SUSY point at t = 20.15;
- check that the point is a minimum (V″ > 0 in the SUSY-AdS sense: d²|W|/dt² > 0 suffices as a proxy);
- compute W_min and compare with v4's |W₀| = 5.6e-9.

**Verdict:** **PASS** if some N′ gives a natural B/A ∈ [0.1, 10] and |W_min| within ×3 of 5.6e-9. Otherwise FAIL.
