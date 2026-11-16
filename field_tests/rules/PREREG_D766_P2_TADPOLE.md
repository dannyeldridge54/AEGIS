# PREREG D766: P2 on non-inflaton moduli — the CP test at U₂ ∈ {i, ω} and the tadpole budget
Locked 2026-11-16 before computing. Script: theory/modular/p2_tadpole_d766.py. Output: field_tests/results/p2_tadpole_d766.txt.
Inputs:
- 2405.18813: n_flux = −2f·a⁰b₃ (eq 3.25), bound n_flux = 32 − 2n_D3 − n_O3′ (eq 3.8), CP needs b₃ ∤ a⁰ and a⁰ ∤ b₃, minimum n_flux = 12 (a⁰ = 2, b₃ = −3, f = 1).
- D698: SERAPIS uses 5/5/5 stuck D3 + 1 at the origin (16 units), and C = 15N/(64π⁶ Im S Im ρ).
Computations:
(1) the j-test of D764 for U₃ = −(b₃/a⁰)/U₂ with U₂ = i and U₂ = ω, over the D764 flux grid;
(2) the largest n_D3 allowed with n_flux = 12 and n_O3′ = 0;
(3) per-point stuck-brane counts N ∈ {1..5} that fit, with three equal half-period stacks plus k ∈ {0, 1} at the origin, and the implied Im S·Im ρ range, rescaling D698's 375–1220 (N = 5) by N/5 at fixed C.
Decision:
- VIABLE if U₂ = ω gives CP violation, U₂ = i gives none (expected), and some N ≥ 2 fits with Im S·Im ρ ≥ 100 (weak coupling and moderate volume kept).
- Otherwise P2 conflicts with the tadpole.
