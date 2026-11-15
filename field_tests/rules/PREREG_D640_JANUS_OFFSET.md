# PREREG D640 (W1): removing the 11–13% bias of the Janus consistency relation
Locked before computation, 2026-11-15. Script theory/modular/janus_offset_d640.py; output field_tests/results/janus_offset_d640.txt.
Asymptotics (analytic, from |j−1728| ≈ e^{2πy}): I ≈ y − c, c = ln1728/(2π) = 1.1868; I1 ≈ y/2 − c/2 = I/2. So V ≈ V0[I²/(I²+1) + εI/2] with canonical φ = ln(I + c)/√2: the offset enters ONLY through the field map.
Test data: the 8 exact Mukhanov–Sasaki points in results/janus_analytic_d635.txt (n_s, r, α_exact), fixed, not recomputed.
Methods (both parameter-free given n_s, r):
- A (closed form, first order in c/I): slow-roll n_s, r, α_s of V = 1 − I^{-2} + εI/2 with dφ = dI/(√2(I + c)), expanded to leading order in 1/I at fixed x = εI³/4 and first order in c/I (sympy series). Invert (n_s, r) → (I*, x) numerically, predict α_s.
- B (full slow-roll map): the exact asymptotic V in terms of I with I = y − c, I1 = I/2 and exact field map; first-order slow-roll n_s = 1 − 6ε_V + 2η_V, r = 16ε_V, α_s = 16ε_Vη_V − 24ε_V² − 2ξ_V²; solve (I*, ε) from (n_s, r) numerically; predict α_s.
Report signed error vs α_exact for each point and the max |error|. PASS (bias removed) if max |err| ≤ 3% for B; A reported. Also report the D635 leading-order error for comparison. No tuning, no rerun; fixes via DEVIATIONS first.
