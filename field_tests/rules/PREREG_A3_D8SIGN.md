# PREREG_A3_D8SIGN — BIG LOOP Q5 (partial): sign of the regularised one-loop R⁴ term in the D = 8 analogue (locked D1672, 2026-11-20 00:20 UTC)
GRV (1001.2535, eqs. 3.20–3.21, 3.30): at D = 8 the s = 1 pole cancels and leaves the moduli-dependent term L(U) = −π log(U₂|η(U)|⁴), plus a scheme constant c that we do not have.
Compute: the minimum of L over the SL(2,Z) fundamental domain (|U₁| ≤ ½, |U| ≥ 1, U₂ ≤ 6), on a 200 × 400 grid plus a local refinement; also L at i and ρ.
Reading set in advance: if min L > 0, the one-loop thread is positive everywhere up to the constant, so the D = 8 plateau is a plateau (not a hilltop) whenever c > −min L. Report min L as the margin. D ≤ 6 is still open (a different series).
Script: field_tests/scripts/a3/run.py
