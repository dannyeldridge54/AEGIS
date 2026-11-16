# PREREG D776: the minimum doublet–singlet mixing c* for ρ-leptogenesis, and its naturalness
Locked 2026-11-16 before computing. Script: theory/modular/c_threshold_d776.py (reuses the D775 code path). Output: field_tests/results/c_threshold_d776.txt.
Inputs:
- D725: the pair singular value is 0.2745·c and the single is 0.38817, independent of c. So M_pair/M_single = 0.7072·c for c < 1.4142.
- T_R(c) is interpolated log-linearly in log c through D725's points (0.3: 3.175e8; 1: 4.287e8; 3: 9.459e8) at M_H = 1e12.
Scan c ∈ {0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.85, 1.0}, m₁ = 1e-3 eV, with the D775 ε/yield and grid. K4: c = 0.3 and 1.0 reproduce D775 (0% and 29.4/54.0%).
c* = the smallest c with max(pass fraction) ≥ 10%.
Naturalness (stated reasoning, no fit): with k_N = k_N3 = −1, both the doublet–doublet and the doublet–singlet terms are weight-2 forms Y with the same Kähler factor (2 Im τ)^{(k_i + k_j)/2}, so c is a ratio of two O(1) constants. Prior: log-uniform on [0.1, 10]. Report P(c ≥ c*).
