# PREREG D541 — SERAPIS-2: plateau log factor from the threshold/species function (locked 2026-11-14 22:32 CT before computing)
Model (D540 proposal): same as SERAPIS-1 (holomorphic form, c = 0) but the factor [ln(j/1728)+κ] in |H|² is replaced by the string-derived, modular-invariant threshold function L(τ) = −ln(2 Im τ |η(τ)|⁴) + κ′ (entering V directly, non-holomorphic):
V ∝ (2y)⁻¹ |η|⁻⁴ |j − 1728| |j|^(−7/6) · L, on the imaginary axis τ = iy.
Method: identical to PC job J4 (janus_j4.py infl(): canonical φ = ln y/√2, end at ε = 1, N* e-folds back, slow-roll n_s = 1 − 6ε + 2η, r = 16ε), δ = 0.
Grid: κ′ ∈ {0 (primary), 1, 2π (sensitivity)}; N* ∈ {52, 55.6}.
Report n_s, r and distance to CMB-SPA (0.9684 ± 0.0030) and SPA+DESI (0.9728 ± 0.0027). Verdict: VIABLE if the primary κ′ = 0 has |n_s − 0.9684| ≤ 2σ and r < 0.036 at both N*; else NOT VIABLE. Single run.
