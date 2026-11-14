# PREREG D327: inflation test of D326's loophole (IIB U-modulus, twisted-moduli GS) — locked before computing

Locked 14 Nov 2026, ~06:20 CT (cloud). AI-assisted.

Setup: K ⊃ −3 ln(U+Ū) + ½(M+M̄ − δ ln(U+Ū))², with f_a ⊃ s_a M. D-flatness holds M+M̄ = δ ln(U+Ū), so K_UŪ gains δ²/(U+Ū)², i.e. α = 1 + δ²/3
(the first-order term vanishes at the D-flat point; the sign is fixed). Cancelling the Kaplunovsky–Louis −b_a ln u needs s_a δ = b_a/8π². With
the largest |b_a| (U(1)_Y, 33/5) at s = 1: δ = 0.0836, α = 1.00233. At s = 2: δ = 0.0418, α = 1.00058. At s = 1/2: δ = 0.167, α = 1.00931.
Computation: same code and conventions as PREREG_D325 (theory/review/gs_alpha_ns_d325.py: TWIST-K, n = 125, μ = 1, N* = 57), run for
α = 1.00233, 1.00058, 1.00931. Script: theory/review/twisted_gs_ns_d327.py.
Rule: |Δn_s| ≤ 0.004 at s = 1 → the loophole survives inflation at natural normalisation. The s = 2 and s = 1/2 values are reported as a
range; they are not scored. n_s values are post-data and NOT counted as evidence even if they move toward ACT.
No reruns; fixes go in PREREG_D327_TWISTED_GS_DEVIATIONS.md.
