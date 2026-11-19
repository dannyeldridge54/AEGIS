# PREREG D1457 — band_e running formula with an n_s term, fitted to the derived ρ grid

Locked 2026-11-19 (UTC) before fitting (JANUS tick 53, node band_e).
Form: α_s = −2r·(a + b(n_s − 0.972)) — the κ = 1 leading-order −2r (D1399) times a linear n_s correction (D1454 found 0.55 % n_s
dependence at fixed r that D1421's r-only −k·p²r/4 lacks).
Fit: least squares in relative residual over the 9 D1454 grid points (field_tests/results/D1454_band_e_derived.json; no new solves).
Out-of-sample check: the derived model's A1 value (D1442 json, n_s 0.974393, r 4.82095e-4, α_s −9.97963e-4) and the D1443/D1444
corners K3, K4 (inside band_e's r span: r 4.529e-4 is below 4.55e-4, so only K4 r 4.709e-4 and A1 are in-band; K3 reported, flagged).
Rule: ADOPTED (as a cross-check formula, D1421 stays the frozen-band reference) if max in-sample |rel. residual| ≤ 0.1 % AND
out-of-sample |rel. error| ≤ 0.1 % at A1 and K4; otherwise NOT ADOPTED. Report a, b.
No refits to chase results; fixes only via PREREG_D1457_DEVIATIONS.md first.
