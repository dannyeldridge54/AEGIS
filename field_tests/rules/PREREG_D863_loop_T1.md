# PREREG D863: does the BHK-type one-loop Kähler correction destroy the CP-odd racetrack minima at the D861 benchmark?
Locked before computing, 2026-11-16.
Estimate of the coefficient [derivation, to be recorded]: BHK normalisation K⁽¹⁾ = (1/256π⁶) Σℰ₂/((S − S̄)(T − T̄)), Σℰ₂ ~ 128·N·E(U,2) per stack (D689), N ≈ 5, E(U,2) ≈ 6 → Σℰ₂ ≈ 3.8e3; with (S − S̄)(T − T̄) = −4 Im S·Im T and Im S = 0.485 (g_s = 0.232): δK = c′/t, c′ ≈ 3.8e3/(256π⁶·4·0.485) ≈ 0.008 (magnitude; sign scanned).
Model: K = −3 ln(2t) + c′/t, t = Im T; W = W0 + e^{2πiT/5} + B e^{2πiT/6}; V = e^K(K^{TT̄}|W_T + K_T W|² − 3|W|²), K_T = K′(t)/(2i), K_TT̄ = K″(t)/4.
Scan: W0 ∈ {+4e-3, −4e-3}; B ∈ {±0.5, ±1, ±2}; c′ ∈ {0, ±0.008, ±0.08, ±0.8} (×1, ×10, ×100 safety). Minima found as in D845 (400×400 grid s ∈ [0, 30), t ∈ [1, 60], Nelder–Mead, positive-definite Hessian).
Per (W0, B): number of CP-odd minima (t > 2) and their positions, versus c′ = 0.
Verdict: racetrack CP-odd minima SURVIVE if, for c′ = ±0.008, every (W0, B) keeps the same number of CP-odd minima with positions shifted by < 1% in s and t; "fragile" if they survive at ×1 but not at ×10.
Prediction (pre-stated): survive at ×1 and ×10 (relative correction to K_TT̄ ≈ 2c′/3t ≈ 1e-3 at t ≈ 4–10); changes appear only at ×100.
