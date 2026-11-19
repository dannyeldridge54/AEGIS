# PREREG D1436 — do the three closed forms nest exactly? D640 (c → 0) = D635 = D1405 at κ = ½ (p = 2√2)

Locked 2026-11-19 (UTC) before computing (JANUS tick 32). Hand derivation (in the D-note): (i) c = 0 in D640 gives D635 term by term;
(ii) for D635's potential (p = 2√2, q = √2 ⇒ κ = ½), ρ = (1+x)/(1−x/2), (1+ρ)/2 = (1+x/4)/(1−x/2), so D1405's
α_s = −½(1−n_s)²ρ[1+κ(ρ−1)] equals D635's −(128/y⁴)(1+x/4)(1+x) exactly.
Numerical check: y ∈ [10, 30], x ∈ [0, 1] (41×41). From D635's (n_s, r) evaluate D1405 at κ = ½, p = 2√2 (exact √8) and compare
with D635's α_s; and D640 with c = 1e-12 vs D635. Rule: PASS if both max relative differences < 1e-10.
No reruns to chase results; fixes only via PREREG_D1436_DEVIATIONS.md written first.
