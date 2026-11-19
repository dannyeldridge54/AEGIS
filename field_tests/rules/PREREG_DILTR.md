# PREREG DILTR — reheating sensitivity of the axio-dilaton near-band point (D1479 A1) and its untilted twin (A0)

Locked 2026-11-19 before computing (Danny 04:31 "any more").
Same code path as PREREG_DILATON32 + D1 (form A, E(τ,3/2), λ = 1), C ∈ {0, 1.25e-6}, T_R ∈ {1e8, 1e10} GeV (the D1479 runs used 8.94e8).
Question: how far do n_s and r move with the reheating temperature (via N*)? Report Δn_s, Δr vs the T_R = 8.94e8 values.
Rule: "robust" if |Δn_s| ≤ 0.002 and |Δr|/r ≤ 10% across the T_R range; else "reheating-sensitive" (then T_R becomes a parameter the
dilaton route must predict). Also report whether any of the four points lands in band (in band / near as PREREG_SMSCAN).
No reruns to chase results; fixes only via PREREG_DILTR_DEVIATIONS.md written first.
