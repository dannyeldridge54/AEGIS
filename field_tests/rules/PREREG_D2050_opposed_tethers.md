# PREREG D2050: Danny 02:17, "tethered to negative space and future space … up to 9 orientations … two boundaries tethered together in opposition". A toy test, locked before computing.
**Idea in model form:** the visible gauge kinetic function couples to n cycles with opposite orientations:
- f_vis = Σ_i s_i T_i + 9S, with s_i = ±1 and Σ s_i = 0 (balanced, "in opposition"), n = 2, 4, 6, 8. (9 is odd and cannot balance, so it is reported as unbalanced.)
- Each cycle is KKLT-stabilised with its own prefactor A_i: x_i = a_i t_i solves the KKLT condition. To good accuracy x_i ≈ x + ln(A_i/A), with x = 21.10.
- Its F-term is F_i/(2t_i) ≈ m₃/₂/x_i.
- Gaugino modulus piece: M₀ = m₃/₂·|Σ_i s_i/x_i| / (Σ_i 1/x_i)·(n/x)… The leak used is defined as the **ratio to the single-cycle case**: leak_rel = |Σ s_i/x_i| / (1/x).

**Test:** draw ln A_i uniformly in [ln 0.1, ln 10] (natural prefactors, 20,000 draws). Report:
- the fraction with leak_rel ≤ 1.2e-3 × 17.8 ≈ 0.0214, the D2039 bound converted (sq ≤ 1.2e-3 of a ×17.8 leak means leak_rel ≤ 0.0214);
- the median leak_rel.

**Verdict:**
- **PROMISING** if the fraction is ≥ 5% for some n.
- **SYMMETRY-ONLY** if the bound is met only with exactly equal A_i (a Z₂ / mirror symmetry would then be the thing to derive).
- **NULL** otherwise.

**Stated caveat:** a D7 wrapping a difference of divisors is not automatically holomorphic. The geometric realisation is not claimed.
