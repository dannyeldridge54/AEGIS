# Janus formulas — one-page reference (state at D1467, 19 Nov 2026)

Written by the Janus derivation loop (D1468). Every number below is copied from the cited D-note or its result json.

## Potentials (what the exact MS pipelines integrate)
- **τ = i** (NA12, `theory/modular/running_d632.py`; D1447): V = I²/(I² + 1) + ε·I₁, with I = y − c, I₁ = I/2 (to 4e-15 at y 20–30), c = ln1728/2π = 1.18646, φ = ln y/√2.
- **ρ** (SERAPIS-E offset model; D1414–D1415): V = (1 − 1/E₁)(1 + C(E₁ − 1)), E₁ = 2ζ(4)y² + B + πζ(3)/y, B = 1 − E(ρ,2) = −4.78334, φ = ln y/√2.

## Derived running (second-order slow roll; D1442, D1448)
Recipe: 1609.04739 Eqs. 9–12 for n_s, r and ε_n(V); α_s to O(ε³) = dn_s/d ln k with d ln k = (1 − ε₁)dN and dε_n/dN = ε_nε_{n+1}.
- ρ: 7/7 exact audited-box points within 0.14 % (D1442–D1444); τ = i: 5/5 NA12 within 0.031 % (D1448).
- References predate D1417's estimator fix (~0.07–0.17 %), so agreement is at reference precision (D1444); PC job J4 would tighten it (D1450).
- Scripts: `field_tests/scripts/d1442/second_order.py` (ρ), `d1448/tau_i_exact.py` (τ = i), `d1449/vac_grid.py` (both; `solve`).

## Cross-check formulas (fits to the derived models)
| vacuum | formula | fitted on | accuracy vs derived model |
|---|---|---|---|
| ρ (band_e) | α_s = −2r[1.0373 − 0.947(n_s − 0.972)] | n_s 0.969–0.975, r 4.55–5.12e-4 | ≤ 0.021 % in, ≤ 0.019 % out (D1457) |
| τ = i (band_i) | α_s = LO½·[1.1244 − 1.765(n_s − 0.9725)], LO½ = −½(1−n_s)²ρ[1 + ½(ρ−1)], ρ = 2√2√(r/2)/(1−n_s) | n_s 0.970–0.975, r 4.8–5.7e-4 | ≤ 0.0071 % in, ≤ 0.0103 % out (D1462) |
- A −2r-type form fails for τ = i (2 %; D1460). Leading-order miss: τ = i +12.06 % (offset c +11.71 %, SR order +0.31 %); ρ +3.50 % (offset + plateau +5.58 %, SR order −1.96 %) (D1463).

## Running of the running (leading order; D1466)
β_s = −(1 + ε₁)[2ε₁ε₂(ε₂ + ε₃) + ε₂ε₃(ε₃ + ε₄)]: ρ (A1) −2.860e-5 (D1400's (1 − n_s)α_s is 11.9 % shallower), τ = i (NA12 centre) −3.126e-5.

## Key points
- ρ A1: n_s 0.974393, r 4.82095e-4, α_s −9.9814e-4 (exact, old estimator); derived −9.9796e-4.
- τ = i NA12 (ε 1.40e-4): n_s 0.97462, r 4.8335e-4, α_s −8.543e-4 (exact); audited τ = i window ε 1.378–1.440e-4 (D1461).
- Bands (ACT DR6 pulls, all PASS, theory negative vs data leaning positive): band_e_audited −1.26 … −1.39σ (D1452), band_i −1.24 … −1.39σ (D1453), band_e −1.26 … −1.40σ (D1454).

## Testability (funded surveys unless marked)
| observable | SERAPIS | best real σ | significance | note |
|---|---|---|---|---|
| n_s | 0.9744–0.9746 | SO 0.002 (1907.08284) | 3.1–3.2σ if CMB-only 0.9682 holds (D1441); SO + SPHEREx 7.7–8.0σ (D1440, 2212.04115-based) | first decider (~2027+) |
| r | 4.55–5.7e-4 | LiteBIRD δr = 1e-3 (2406.02724, JFY2032) | 0.46–0.57σ (D1440) | idealized 0.98e-4 forecast would give 7.6–11.4σ (D1438, corrected) |
| α_s | −8.4e-4 … −1.07e-3 | SO 3.3e-3 | ≤ 0.3σ; 3σ needs ~3e-4 (D1409, D1431) | exclude-only (positive running would kill) |
| Δα_s (ρ − τ = i) | −1.05 … −1.62e-4 | SO 3.3e-3 | ≤ 0.05σ (D1449) | vac_discriminant killed |
| β_s | ≈ −3e-5 | Planck 0.013; S4 0.0045 (hypothetical) | ≤ 0.007σ (D1467) | needs ~1e-5 |
CMB-S4 ended July 2025 (D1440). No newer n_s/α_s/r measurement than 2512.10613 / 2606.28502 as of 19 Nov 2026 (D1465).

## Open decisions (Danny; D1464)
(a) queue PC jobs J1–J4 (`docs/JANUS_PC_JOBS.md`); (b) add band_i_audited node (D1429/D1461); (c) band_i map-note ε wording (D1461); (d) optional janus title note (D1458).
