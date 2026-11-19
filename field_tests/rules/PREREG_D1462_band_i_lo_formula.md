# PREREG D1462 — band_i running formula built on D1405's κ = ½ leading order

Locked 2026-11-19 (UTC) before fitting (JANUS tick 58, node band_i).
Form: α_s = LO(n_s, r)·(a + b(n_s − 0.9725)), LO = −½(1 − n_s)²ρ[1 + ½(ρ − 1)], ρ = 2√2·√(r/2)/(1 − n_s) (D1405 with κ = ½,
p = 2√2 for the τ = i potential, D1436).
Fit: least squares in relative residual over the 9 D1453 grid points (no new solves). Out-of-sample: D1448's five derived NA12 values.
Rule: ADOPTED if max in-sample and out-of-sample |rel. residual| ≤ 0.1 %; otherwise NOT ADOPTED (no refit, no third parameter).
Expectation: LO is 10.8 % low at τ = i (D1263/D1412), so a ≈ 1.1 with an n_s-dependent part from the offset c (D640) is expected.
No refits to chase results; fixes only via PREREG_D1462_DEVIATIONS.md first.
