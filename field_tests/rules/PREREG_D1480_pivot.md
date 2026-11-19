# PREREG D1480 — L1: n_s, α_s, r at k = 0.002 Mpc⁻¹ for both vacua (from the k = 0.05 pivot)

Locked 2026-11-19 ~10:31 UTC before computing (JANUS tick 89; lead L1 of docs/JANUS_LEAD_QUEUE.md).
Points: ρ A1 (n_s 0.974393, r 4.82095e-4) and τ = i NA12 centre (n_s 0.97462, r 4.8335e-4) at k_* = 0.05 Mpc⁻¹, solved with field_tests/scripts/d1449/vac_grid.py solve().
Method (two routes):
 (a) exact model: follow the slow-roll trajectory dφ/dN = V′/V back from φ_* until ∫(1 − ε₁)dN = ln(0.05/0.002) = 3.2189, and evaluate the second-order obs() there;
 (b) Taylor: n_s(k) = n_s + α_s L + ½β_s L², α_s(k) = α_s + β_s L, L = ln(0.002/0.05), β_s from D1466.
Rule: report both; agreement |Δn_s(a − b)| < 5e-5 ⇒ CONSISTENT, else report the gap as the Taylor truncation (no pass/fail on physics — this is a conversion). Script: field_tests/scripts/d1480/pivot.py → field_tests/results/D1480_pivot.json. No reruns; fixes via PREREG_D1480_DEVIATIONS.md first.
