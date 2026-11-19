# PREREG_GENESIS_DE2 — re-score the reverse thread with a SOURCED calibration (locked D1627, 2026-11-19 15:20 CT)
Why: D1626 used an ASSUMED w₀–w_a correlation ρ = −0.9. DESI DR2 (arXiv:2503.14738, Table VI) gives the w₀w_aCDM preference over ΛCDM: Δχ²_MAP = 10.7 (Pantheon+), 17.4 (Union3), 21.0 (DESY5). DESY5 point (Table V): w₀ = −0.752 ± 0.057, w_a = −0.86 (+0.23/−0.20).
Method: for each dataset, choose ρ ∈ (−0.99, 0.99) so that the Gaussian approximation gives Δχ²(ΛCDM point −1, 0) equal to that Δχ²_MAP (if none does, use the ρ that comes closest, and report it). Model grid: identical to PREREG_GENESIS_DE after DEVIATIONS D1–D2 (same physics, β set, 40 amps in [0.01, 0.9]).
Pass rule unchanged: CONSISTENT if min Δχ² ≤ 6.18, else TENSION. These scores REPLACE the D1626 scores whichever way they move.
Script: field_tests/scripts/genesis_de/rescore.py
