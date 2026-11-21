# PREREG_RW2_SEQUESTER — DEVIATIONS
## D1 (21 Nov 2026, before any RW2 result was produced)
- What happened: the tool self-test (tools/weave_cm/weave_reverse.py __main__) stopped with an AssertionError
  before theory/tests/rw2_sequester.py was run, so no RW2 number exists from the bad code. Captured output:
  `AssertionError: (0.15635249018669128, 0.16964110845474456)` (numeric δK/δφ vs the leading-order formula).
- Cause (coding/numerical): K_dd was taken by central finite differences with h = 1e-4 on K ≈ −23. Roundoff
  ≈ 2e-16·23/h² ≈ 5e-7 is comparable to K_dd ≈ 1.2e-6·4, so the second derivative was wrong at the ~10 % level.
  The same issue affects G_matrix and the swiss branch of saxion_mass_over_H0.
- Fix: analytic derivatives of K = −2 ln 𝒱, 𝒱 = τ_b^{3/2} − τ_v^{3/2} − τ_d^{3/2}:
  K_i = 3√τ_i/𝒱 (small cycles), K_ii = 3/(2√τ_i 𝒱) + 9τ_i/𝒱², K_vd = 9√(τ_v τ_d)/𝒱².
  The self-test tolerance against the leading-order √(12 τ^{3/2}/𝒱) is set to 3 % (the exact subleading term
  9τ/𝒱² is 1.4 % of K_dd here); the check is now that numeric = analytic to 1e-9.
- Nothing else changes: inputs, channels, thresholds and the verdict rule are as locked.

## D2 (21 Nov 2026, still before any RW2 result) — correction to D1's formula text
- D1 wrote K_ii = 3/(2√τ_i 𝒱) + 9τ_i/𝒱² and K_vd = 9√(τ_v τ_d)/𝒱². The correct second derivatives of
  K = −2 ln 𝒱 are K_ii = 3/(2√τ_i 𝒱) + 9τ_i/(2𝒱²) and K_vd = 9√(τ_v τ_d)/(2𝒱²) (factor ½ on the 𝒱⁻² terms).
  Found while coding the D1 fix; the code uses the correct forms and the self-test now checks them against
  40-digit mpmath derivatives (relative 1e-9). D1 is kept as written.
