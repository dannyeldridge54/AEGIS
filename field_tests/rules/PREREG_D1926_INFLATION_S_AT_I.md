# PREREG D1926 — inflation with S ending at i (locked 21 Nov 2026 before running; repo at 634ca10e)
Model: the P3-S plateau V ∝ G^{SS̄}|∂_S ln E(S,3/2)|² (D1523), Green–Gutperle normalisation; path Re S = 0 ending at S = i, vs the standard Re S = ½ ending at ρ.
Script: theory/tests/d1926_inflation_S_at_i.py. Validation first: E(ρ) must reproduce 8.893 (D1622) to 1e-3, and S-invariance must hold to 1e-10; if either fails the run is VOID.
PASS requires all three: (1) S = i is a strict minimum (both canonical m² > 0); (2) V rises monotonically along Re S = 0 from y = 1.05 to 20.95 (no barrier); (3) |Δn_s| < 1e-3 from the reheating shift ΔN* = ½ ln(m_i/m_ρ) (T_R ∝ m^{3/2}, w = 0), with N* = 50.3. Otherwise FAIL.
Report only: the plateau difference V(0, 55.6)/V(½, 55.6) − 1 (expected ~e^{−2π·55.6}); m²(i), m²(ρ).
Expectation (written before running): n_s and r are unchanged up to e^{−2πy*}; only the endpoint mass and T_R shift. D762 (CP-conserving inflaton line) carries over, since Re S = 0 is also a CP-symmetric line.
