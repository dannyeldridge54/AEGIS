# DEVIATIONS — PREREG_GENESIS_DE (written before any rerun)
D1 (design error found on first run, crash before any output): the scan range A e^{-βφ_i} ∈ [0.01, 3] includes values > 1, where V = V_Λ(1 − amp) < 0 at the start — that is not "on the plateau", contradicting the lock's own stated intent. The shooting bracket V_Λ ∈ [0.5, 10] also cannot reach H₀ = 1 for amp near 1.
Fix: scan amp ∈ [0.01, 0.9] (40 log-spaced points, same count); bracket V_Λ by expanding the upper end ×2 until the sign changes (max 1e4). Physics, data, pass rule, ρ = −0.9 unchanged. No output had been seen.
