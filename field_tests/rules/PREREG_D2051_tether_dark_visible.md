# PREREG D2051: the D2050 cross-check (gauge coupling). Can opposed tethers keep α_G⁻¹ = 28 and cancel mirage? Locked before computing.
**v4 facts used:**
- α_G⁻¹ = Re f_vis = σ_vis + 9·Re S = 20.15 + 9(√3/2) = 27.94 (v4 lists 28.0).
- The visible cycle: N = 6, x_v = 2πσ_vis/6 = 21.10.
- The dark cycle: SU(12), σ_d = 40.3, so x_d = 2πσ_d/12.

**Mutation:** f_vis' = T_d − T_v + 9S (the two boundaries tethered in opposition).
- Re f' = σ_d − σ_v + 9 Re S.
- Gaugino modulus piece ∝ |F_d/(2t_d) − F_v/(2t_v)| ≈ m₃/₂·|1/x_d − 1/x_v|.
- The KKLT condition per cycle gives x_i ≈ ln(A_i/W₀) + O(ln x). So x_d − x_v ≈ ln(A_d/A_v).

**Compute:**
- (a) α_G'⁻¹ from v4's σ values;
- (b) x_d vs x_v;
- (c) the allowed A_d/A_v window for leak_rel = |x_d − x_v|/x ≤ 0.0214 (the D2039 bound).

**Verdict:**
- **PASS(coupling)** if |α_G'⁻¹ − 27.94| ≤ 0.5;
- **PASS(leak)** if the allowed window contains A_d/A_v = 1 and is at least a factor ×1.3 wide (natural);
- otherwise FAIL.
- Holomorphy of the class [D_d] − [D_v] is **not** checked here. It is owed.
