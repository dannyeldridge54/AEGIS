# PREREG_REALDATA_EXACT — real-data refit with the EXACT perturbative SERAPIS curve (locked D1696, 2026-11-20 01:24 UTC)
Shape: V/V_Λ = g(y) = [(2/3)(3/2 − 2c u/(1 + c u))]², with u = y⁻², c = 2ζ(2)/ζ(3) = 2.737 and y = e^{βφ/2}, β = 2√2. This is the perturbative part of E(τ,3/2) only (no e^{−2πy} terms). It reduces to 1 − 7.30u at small u, has a floor V = 0 at y² = c/3, and is never negative. The start is parametrised as amp ≡ 7.30/y_i² (same meaning as before), frozen at a = 10⁻³.
Fits: (a) BAO + SN as PREREG_REALDATA_NEG (compare with leading order −7.01); (b) BAO + SN + CMB as PREREG_REALDATA_CMB (compare with −4.84).
Reading: "leading order is adequate" if |Δχ²(exact) − Δχ²(leading)| ≤ 1 in both.
Script: field_tests/scripts/realdata/exact.py
