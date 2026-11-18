# PREREG U1b — compiled exact MS with the initial-condition ripple suppressed
Locked after the U1 D1 diagnostic (results field_tests/results/u1_d1_diag.txt): the exact-MS α_s scatter is NOT integrator noise (rtol 1e-10…1e-13 identical on a 21-point fit) but a deterministic ripple in P(k) from starting the modes at k/aH = 200 (amplitude ~ (aH/k)² ≈ 2.5e-5), amplified by 5-point second differences.
Change: bd = 4000 (ripple ~6e-8) and α_s/n_s from a 9-point ±0.1 grid (deg-4 fit) — spectra_msjit arguments only; no code change.
Tests at the four TK1 points (C 1.0/1.15e-6 at N* 50.7, and the TK1 e2e N*):
 T1 |Δn_s| vs TK1 exact MS ≤ 1e-5 (printed 5-digit references), |Δr/r| ≤ 2e-4.
 T2 time per 9-k spectrum ≤ 15 s (vs ~570 s for ms.spectra at 63 s per k).
 T3 α_s stable: 9-pt ±0.1 vs 9-pt ±0.05 differ by ≤ 2e-5; and bd 4000 vs bd 8000 differ by ≤ 2e-5.
 T4 |α_s − Janus core spectra3| ≤ 3e-5.
Adopt as the serapis_ms tool path if T1–T3 PASS. Results: field_tests/results/u1b_ms_ripple.txt.
