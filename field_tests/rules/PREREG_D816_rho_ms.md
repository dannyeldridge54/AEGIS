# PREREG D816: exact MS consistency check of the frozen SERAPIS-ρ band (accuracy queue 6a; Jl tick 55)
Locked before computing, 2026-11-16. The frozen numbers (lock D615: n_s 0.969–0.972, r 4.6–5.1e-4) are NOT changed.
Code: rho_running_d634.py (MS, same ρ-path potential), with everything above its scan exec'd unchanged. K4: ε = 6e-5, N* = 47 gives n_s 0.9700 (D634).
Run ε = 6e-5 at N* = 46.09, 47.61, 47.96, 49.49 (read from results/rho_nstar_d613.txt). Report n_s, r, α_s and their distance from the frozen band edges.
Rule: if MS lies outside the frozen band, the paper says so in one sentence ("exact spectra give …"); the frozen band stays.
