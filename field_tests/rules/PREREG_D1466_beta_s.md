# PREREG D1466 — β_s (running of the running) from both derived models

Locked 2026-11-19 (UTC) before computing (JANUS tick 62, node janus).
[derived, before computing] From 1609.04739 Eq. 1 (dε_n/dN = ε_nε_{n+1}) and Eq. 11 (α_S = −2ε1ε2 − ε2ε3 + O(ε³)), with d ln k = (1 − ε1)dN:
β_s = dα_S/d ln k = −(1 + ε1)[2ε1ε2(ε2 + ε3) + ε2ε3(ε3 + ε4)] + O(ε⁴) — leading order only (stated; the next order would need the
O(ε³) α_S terms of D1442 differentiated, not done here).
Points: ρ at A1 (solve the D1442 model at n_s 0.974393, r 4.82095e-4) and τ = i at the NA12 centre (D1448 model at n_s 0.97462,
r 4.8335e-4); ε_n from the 1609.04739 Eq. 12 map of the potential flow parameters (as in the D1442/D1448 scripts).
Comparison: D1400's κ = 1 closed form β_s = (1 − n_s)α_s, with α_s = the derived model's value at the same point.
Rule: for ρ, D1400 CONFIRMED if |β_derived/β_D1400 − 1| < 10 %, else NOT CONFIRMED. For τ = i (κ = ½, D1400 not derived for it)
report β_derived/((1 − n_s)α_s) as a characterisation only.
No reruns; fixes only via PREREG_D1466_DEVIATIONS.md first.
