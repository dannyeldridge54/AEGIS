# PREREG D635: analytic derivation of the Janus pair (Kairos x = 0, Chronos x > 0) from the two-term potential, checked against the exact numerics (locked before computing)

Cusp form (p = 2, α = 1/3, φ = ln(y)/√2): V ≈ 1 − y⁻² + (ε/2)y, using I ≈ y and I₁ ≈ y/2 to leading order. Tilt fraction x ≡ εy*³/4.

Derived (leading slow-roll):
- N = ∫ y dy/(4 + εy³), so y*² = 8N at x = 0.
- 1 − n_s = (16/y²)(1 − x/2).
- r = (64/y⁴)(1 + x)².
- α_s = −(128/y⁴)(1 + x/4)(1 + x).

Consequences:
- (i) Kairos (x = 0): r = (1 − n_s)²/4 and α_s = −(1 − n_s)²/2.
- (ii) Running ratio versus an attractor at the same n_s: R(x) = (1 + x/4)(1 + x)/(1 − x/2)².
- (iii) JANUS CONSISTENCY RELATION, from (n_s, r) to α_s:
  - ρ = 2√r/(1 − n_s), x = (ρ − 1)/(1 + ρ/2), A = (1 − n_s)/(1 − x/2);
  - α_s = −(A²/2)(1 + x/4)(1 + x).

Check (code):
- Evaluate (iii) on the exact D588/D632 (n_s, r, α_s) triples. For the D632 rows, r comes from the same MS run, via spectra(…)[1]/[0] at s = 0.
- PASS if the predicted α_s matches the exact value within 20% for every row (HS-Kairos and two-term ε = 1.0–1.6e-4, N* = 47, 50).
Report x, R(x) and the percentage errors.
