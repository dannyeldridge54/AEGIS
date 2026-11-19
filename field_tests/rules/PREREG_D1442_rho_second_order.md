# PREREG D1442 — D1415's ρ offset model at second-order slow roll: does it reach A1's exact α_s within 1 %?

Locked 2026-11-19 (UTC) before computing (JANUS tick 38, node janus).
[literature] arXiv:1609.04739 (Martin et al.) Eqs. 1, 9–12, read in full this tick: ε_{n+1} = d ln|ε_n|/dN;
n_S = 1 − 2ε1 − ε2 − (3 + 2C)ε1ε2 − 2ε1² − Cε2ε3 + O(ε³); r = 16ε1(1 + Cε2) + O(ε³); C = γ_E + ln2 − 2;
ε1 = εv1(1 − εv2/3), ε2 = εv2(1 − εv2/6 − εv3/3), ε3 = εv3(1 − εv2/3 − εv4/3) + O(εv³);
εv1 = ½(V′/V)², εv2 = 2[(V′/V)² − V″/V], εv2εv3 = −εv2′V′/V, εv3εv4 = −εv3′V′/V (M_P = 1).
[derived] α_S to O(ε³) from the complete second-order n_S: α_S = dn_S/d ln k, d ln k = (1 − ε1)dN, dε_n/dN = ε_nε_{n+1}:
α_S = −(1 + ε1)[2ε1ε2 + ε2ε3] − (3 + 2C)ε1ε2(ε2 + ε3) − 4ε1²ε2 − Cε2ε3(ε3 + ε4) + O(ε⁴), with ε4 = εv4 at this order.
(Leading part reproduces the paper's Eq. 11.) Sign convention: larger k exits later (larger N).
Model: D1415 full model V/V0 = (1 − 1/E1)(1 + C_r(E1 − 1)), E1 = A y² + B + D/y, A = 2ζ(4), B = −4.78334, D = πζ(3), φ = ln y/√2.
Derivatives analytic-precision via mpmath (dps 40). Solve (C_r, y*) so second-order (n_S, r) = A1 (0.974393, 4.82095e-4).
Rule: PASS if |α_S/α_A1 − 1| < 1 % (α_A1 = −9.9814e-4); FAIL otherwise. Also report the first-order value at the same solve
(must reproduce D1415's −1.0114e-3 within 0.1 % as an implementation check; if not, verdict "no result").
No reruns to chase results; fixes only via PREREG_D1442_DEVIATIONS.md first.
