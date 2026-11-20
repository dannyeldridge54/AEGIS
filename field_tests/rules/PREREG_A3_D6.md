# PREREG_A3_D6 — the D = 6 one-loop R⁴ thread: its sign across a torus slice (locked D1680, 2026-11-20 00:40 UTC; Danny 18:34 "Derive it")
Object: the one-loop R⁴ coefficient at D = 6 is ∝ RN∫_F Γ_{4,4} dμ = 2E^{SO(4,4)}_{V;1} (Obers–Pioline hep-th/9903113; GRV 1001.2535, eq. 3.54, coefficient 2 > 0). Its sign relative to the positive tree term 2ζ(3)/y₆ decides plateau vs hilltop along the coupling.
Regularisation: Zagier's renormalised integral, RN∫ = lim_L [∫_{F_L} Γ dμ − L], since Γ_{4,4} → τ₂² at large τ₂. This is the canonical prescription, but any other scheme shifts the result by a constant (as at D = 8), and that shift is reported.
Slice: rectangular T⁴, B = 0, equal radii R ∈ [1, 3] (T-duality makes R → 1/R identical), so Γ_{4,4} = Γ_{1,1}(R)⁴ with Γ_{1,1} = √τ₂ Σ_{m,w} exp(−πτ₂(m²/R² + w²R²)) e^{2πiτ₁mw}.
Validation first (must pass, else STOP): the same code for d = 2 at T = U = i must reproduce the DKL result RN∫Γ_{2,2} = −log(T₂U₂|η(T)η(U)|⁴) − log(8π e^{1−γ}/(3√3)), with the log L subtraction, to within 2 × 10⁻³.
Outputs: I(R) = RN∫Γ_{4,4} at R = 1, 1.25, 1.5, 2, 3, and its minimum (expected at the self-dual R = 1).
Reading set in advance: if min I > 0, the D = 6 one-loop thread is POSITIVE on this slice (plateau holds) with margin min I. If min I < 0, the sign flips near the self-dual point (hilltop risk there), and the R at which it crosses zero is reported.
Script: field_tests/scripts/a3d6/run.py
