# PREREG D1412 — is the 10.8 % τ = i Janus-relation miss (D1263) the leading-order offset bias that D640 removes?

Locked 2026-11-19 (UTC) before computing (JANUS tick 10, node janus).
D1263: at τ = i the own-κ (½) relation misses exact α_s by 10.8 %, and names the cause as the εI-tilt offset bias (D635/D672),
with the offset-corrected relation (D640) "not tested here". D640 (verbatim formulas, theory/pending_docs, c = ln1728/2π):
  1 − n_s = 8u²[(2 − x) + cu(5 − x)],  r = 64u⁴(1 + x)²(1 + 2cu),  α_s = −32u⁴(1 + x)[(4 + x) + cu(23 + 2x)],  u = 1/I*.
Method: for each NA12 exact τ = i point (field_tests/results/na12_band_i_audited.txt, five ε values), solve the n_s and r
equations for (u, x) with scipy fsolve from (u, x) = (0.06, 0.5), require residual < 1e-12, then predict α_s and compare
with the exact MS α_s. Also report the leading-order κ = ½ relation's error at the same points.
Rule: PASS (bias explained) if |α_s(D640)/α_s(exact) − 1| < 1 % at all five points; FAIL otherwise.
No reruns to chase results; fixes only via PREREG_D1412_DEVIATIONS.md written first.
