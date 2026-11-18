# PREREG D1352 — lattice-geometry inflation configs (new models, [postulate])

Locked 2026-11-18 before any computation. Danny: "new configs based on our geometry", "remember the lattices".

## Model (postulate)
For each lattice L of the weave (A2, D4, E6, E8, BW16, Leech; even dimension d), one Poincaré disk per complex
dimension of L's ambient space gives an α-attractor T-model
  V = V0 tanh²(φ/√(6α)),  3α = d/2.
Configs: A2 → 3α=1, D4 → 2, E6 → 3, E8 → 4, BW16 → 8, Leech → 12.
(E7 has odd d and is not a config; dual lattices have the same d, so a duality flip makes no new config.)
Literature anchor: 3α = 1…7 from seven disks (Ferrara–Kallosh 2016, Kallosh–Linde–Wrase–Yamada 2017). The lattice→disk count rule is ours.

## Computation
Exact slow-roll numerics (no large-N formula): φ_end from ε = 1; N(φ) by quadrature; n_s = 1 − 6ε + 2η, r = 16ε at N*.
N* = 50.7 (SERAPIS matching, primary) and N* = 55 (reported).
Check: 3α=1 must match the Starobinsky-class limit n_s ≈ 1 − 2/N*, r ≈ 12α/N*² within 1e-3 relative on r at N*=55.

## Scoring (fixed now)
Pull vs CMB-SPA n_s = 0.9684 ± 0.0030 and CMB-SPA+DESI 0.9728 ± 0.0027; r < 0.036.
Config "alive" if |pull| < 2 on at least one n_s dataset AND r < 0.036; else "out".
These are post-data models: current pulls are context only. The scored prediction is r per config,
tested by LiteBIRD / SO / CMB-S4 (σ(r) ~ 1e-3). Recorded in the tracker as forecasts, not claims.

## No reruns to chase results; fixes only via PREREG_D1352_DEVIATIONS.md written first.
