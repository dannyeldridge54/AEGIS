# PREREG D612: selection rule at the ρ vacuum (SERAPIS-ρ) for the D529 parity assignments (locked before computing)
At ρ, the residual order-3 element (ST) fixes ρ. A level-1 modular form of weight k is non-zero at ρ only if k ≡ 0 (mod 6): E₄(ρ) = 0, E₆(ρ) ≠ 0, E₄²(ρ) = 0, …
Check numerically: |E₄(ρ)| < 1e-12, |E₆(ρ)| > 0.1, |E₄²(ρ)| < 1e-12, and |E₆²(ρ)| > 0.1.
Same as D551 otherwise:
- W weight −1, so k_Y = Σk_i − 1;
- required couplings QHuU, QHdD, LHdE, HuHd, LHuLHu;
- the D529-passing assignments for Z₄^R and Z₈^R.
Each k_i may be lifted by {0, 2, 4} (because the condition is mod 6), giving 3⁷ lifts. Require every k_Y to be an even integer ≥ 0 with k_Y ≡ 0 (mod 6).
Report: the count of assignments that admit such a lift, and an example. PASS if ≥ 1 for at least one of Z₄^R and Z₈^R.
