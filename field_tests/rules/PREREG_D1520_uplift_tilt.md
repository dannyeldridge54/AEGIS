# PREREG D1520 — tilt plan T4: can the uplift's τ-dependence be the plateau tilt?

Locked 2026-11-19 ~14:51 UTC before computing. Our own file and D-number.
[literature, read this tick] 2010.15903 Eq. (2.14) e^{4A₀} ≃ e^{−8πK/(3g_sM)}; Eq. (2.17) V_D̄3 ≃ e^{4A₀}M_p⁴/𝒱^{4/3}; Eq. (2.20) V_up = M_p⁴ g_s|η|²/𝒱^{4/3} = M_p⁴ c″|Z|^{4/3}/(π g_s M² 𝒱^{4/3}).
Test (sympy/python): along the inflaton y = 1/g_s at fixed 𝒱 and fixed throat data, the needed tilt is a POSITIVE term growing with the plateau variable g (∝ E(τ,3/2) ∝ y^{3/2}).
Shapes: (i) anti-D3 with warp: V_up ∝ e^{−(8πK/3M)y} (fixed Z) or ∝ y·|Z|^{4/3} (Eq. 2.20 form with Z held fixed); (ii) D-term uplift ∝ g_s^p/𝒱² = y^{−p} (p > 0 as generic) — sign and growth of each relative to the plateau.
Rule: a candidate can be the tilt only if it grows with y at least as fast as y^{3/2}·(small coefficient) with positive sign; otherwise "wrong shape/sign". Also report what the uplift's y-dependence does to the plateau height between ρ (y_ρ = 0.866) and horizon exit (y_phys ≈ 3.1e3).
Plus a P3 exact-row check: DILTR A1 at T_R 1e8 vs D1489 (AGREE if |Δn_s| ≤ 5e-4, |Δr/r| ≤ 2 %).
Fixes only via PREREG_D1520_DEVIATIONS.md first.
