<!-- AEGIS-FP MMQCIWXAXLJ2G4RC · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# PREREG D990: Janus String Calculator test battery A — n_s and r on 32 points (written before running)
Janus (tools/janus_calc, as committed with this lock): second-order Hubble-flow n_s, r. Reference: base toolkit tools/serapis_calc ms.spectra_fast (validated in the base selftest for n_s and r), default stencil, bd = 200.
Points: SERAPIS-E C ∈ {1.0, 1.15, 1.3}e-6 × N* ∈ {44, 47, 50, 53} (12); Chronos ε ∈ {1.3, 1.45}e-4 × N* ∈ {44, 47, 50} (6); SERAPIS-ρ ε = 6e-5 × N* ∈ {44, 46.09, 49.49, 52} (4); Kairos (ε = 0) × N* ∈ {46, 50} (2) → 24 SERAPIS-family points.
Stress set (textbook potentials, larger ε, outside the SERAPIS regime): m²φ², φ⁴, Starobinsky (1 − e^{−√(2/3)φ})², natural 1 + cos(φ/5), each at N* ∈ {50, 60} → 8 points.
Pass (fixed now): SERAPIS family: |Δn_s| ≤ 1e-4 and |Δr/r| ≤ 0.5% per point; battery verdict VALIDATED (all 24 pass) / PARTIAL (≥ 20) / NOT VALIDATED. Stress set: reported against a looser envelope |Δn_s| ≤ 5e-4, |Δr/r| ≤ 2% (expected to degrade as ε grows; that is the point of the stress set); no family verdict from it.
Also reported: per-point Janus and reference wall times; max and median errors.
Resumable: points already in the output file are not recomputed (protects against container restarts; not a rerun of a finished point). Two worker processes split the points by index parity.
Script theory/janus/battery_a_d990.py; output field_tests/results/janus_battery_a_d990.txt.
