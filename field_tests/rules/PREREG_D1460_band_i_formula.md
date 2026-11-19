# PREREG D1460 — band_i running formula of D1457's form, fitted to the derived τ = i grid

Locked 2026-11-19 (UTC) before fitting (JANUS tick 56, node band_i).
Form (same as D1457 so the vacua compare directly): α_s = −2r·(a + b(n_s − 0.9725)).
Fit: least squares in relative residual over the 9 D1453 grid points (field_tests/results/D1453_band_i_derived.json; no new solves).
Out-of-sample: D1448's five derived NA12 values (field_tests/results/D1448_tau_i_exact_plateau.json, alpha at NA12 (n_s, r)).
Rule: ADOPTED if max in-sample |rel. residual| ≤ 0.1 % AND max out-of-sample ≤ 0.1 %; otherwise NOT ADOPTED.
Expectation stated before fitting: at κ = ½ the leading-order running is not proportional to r (D1405: −½(1−n_s)²ρ[1 + ½(ρ − 1)]),
and band_i spans r 4.8–5.7e-4 with α_s/(−2r) varying widely — a FAIL is plausible and will be reported as such, no refit.
No refits to chase results; fixes only via PREREG_D1460_DEVIATIONS.md first.
