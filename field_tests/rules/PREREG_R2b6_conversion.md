# PREREG R2b6 — Gailitis total: ⟨S_ann⟩_below vs S_ann + S_conv above — locked 2026-11-17, before any code or run
Basis: the sourced expectation in the D-note citing arXiv:1607.07649 §3.3 (Gailitis' theorem for the total reaction).
- New script function copying two_channel_open's integration (the validated module is not modified).
  - It returns, for incoming χ⁰χ⁰ (channel 0, incoming amplitude −1/(2ik₀)), the OUTGOING amplitude a₁ in channel 1 at R, with WKB-local k and Coulomb tail as in two_channel_open.
  - P_conv = k₁|a₁|² / (k₀·|1/(2k₀)|²). Unitarity check: P_conv ≤ 1. Also report the elastic |S₀₀| for information.
- M = 2000, x = 1.01, full α, tails = (0, ALPHA).
- S_conv = σ_conv v / (πα₂²/M²), with σ_conv = (π/k₀²)P_conv (convention A, distinguishable) and v = 2k₀/M. So S_conv = 2 P_conv M / (k₀ α₂²).
  - Convention B (identical χ⁰χ⁰, ×2) is reported, not scored.
- Below: ⟨S⟩ = 107.61 (D1170, fixed). Above: S_ann = 36.20 at x = 1.01 (D1170), plus S_conv(A).
- Self-check (scored): S_ann from the new function's s must equal 36.20 within 1e-3; otherwise the copy is wrong → STOP.
- Score: PASS iff |⟨S⟩/(S_ann + S_conv(A)) − 1| ≤ 0.20. If only convention B passes → "convention-dependent", not a PASS.
