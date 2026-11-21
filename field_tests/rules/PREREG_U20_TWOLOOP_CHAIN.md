# PREREG U20 — the chain at the two-loop unification point (locked 21 Nov 2026 before computing)
Input change: α⁻¹(M₁₂) = 27.94 at M₁₂ = 1.07e16 GeV (D1800, two-loop) replaces 28.9 at 6.6–7e15 (D1767, one-loop).
Fixed: g_s = 2/√3, flux part 9/g_s = 7.794, x·1.34e9 GeV reheating law (U11), master relation (D1772): M₂ = [√(g_s/2) M_P/375]·[4(2π)³C/(wχ)]·W₀, W₀ = exp[−(2π/N)(α⁻¹ − 9/g_s)], w = 2/3, C = 8e-7 (tilt), 𝒱 = wχ/(4(2π)³C), m₃/₂ = 375 M₂.
Compute: x, T_R, Re T_vis, W₀ (N = 6, 7, 8), M₂(χ) and the χ range putting M₂ in the wino window that weave_wino passes at the new T_R; 𝒱 for that χ.
Verdict:
- CLOSES if an integer pair (N, χ) with N ∈ {6,7,8} and χ ∈ [2, 300] (positive, tilt-compatible) gives M₂ inside the passing window AND 𝒱 ≥ 1e4 (control) — report all such pairs;
- STRAINED if only χ outside [2, 300] or 𝒱 < 1e4 works;
- BROKEN if none.
