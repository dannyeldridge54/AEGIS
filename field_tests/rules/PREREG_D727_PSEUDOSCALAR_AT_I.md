# PREREG D727: is the imaginary (pseudoscalar) inflaton–N coupling at τ = i physical, and what T_R does it give?
Locked 2026-11-16 before computing. Script: theory/modular/pseudo_i_d727.py. Output: field_tests/results/pseudo_i_d727.txt.
## Claim to test (from D726)
A(Y) is real symmetric and traceless along the imaginary axis, eigenvalues +s, −s. A real rotation θ(y) of its eigenvectors gives, in the Takagi (positive-mass) basis, an off-diagonal coupling of size (λ₁ − λ₂)θ′ = 2sθ′, not (|λ₁| − |λ₂|)θ′ = 0. Analytic argument (written now): with ψ = (N₁+iN₂)/√2, χ = (N₁−iN₂)/√2 the mass term is s(e^{−2iθ}ψψ + e^{2iθ}χχ) + h.c.; removing θ(φ) by a field rotation leaves θ′∂φ·(J_ψ − J_χ), whose on-shell matrix element is ∝ 2s (axion-like decay to a massive Majorana pair). So it is physical.
## Checks (decide NULL)
1. Method A (Takagi, as D726): |P₁₂| at i.
2. Method B (independent): real eigenvectors of A(Y(iy)) by numpy eigh at y = 1 ± h; θ′ from their rotation; compare 2sθ′ with |P₁₂| (2y-factor stripped consistently). Agreement to 1% → PHYSICAL; disagreement → NULL, loop stops.
3. Same ratio κ = |P₁₂|/s must reproduce D597's κ = 1.26 (consistency with the earlier number).
## T_R (if physical)
D597/D589 conventions at τ = i: λ = √2κ (NO ΔM factor), pseudoscalar width Γ = (Mλ/M_P)² m (1 − 4x²)^{1/2}/(8π), x = M/m ∈ {0.1, 0.2, 0.33, 0.45}, m = 1.9e11 GeV, g* = 106.75 (also 228.75). T_R as before.
## Consequences (estimates, labelled)
ΔN* ≈ 0.76 per decade of T_R relative to the frozen bracket's T_R = 1e3–1e5 GeV (D682); Δn_s ≈ +0.0008 per e-fold (D644); y* growth ≈ 0.3 per e-fold (D602 rows). Report whether the τ = i frozen band edges (n_s ≤ 0.975, y* ≤ 25) are at risk. AD: required m_ν1 scales ∝ T_R (D646).
## Decision rule
- PHYSICAL + T_R ≫ 1e5 → correction note to D597/D601/D602 and the paper's reheating section (frozen bands not retuned; status of the τ = i history changes).
- Fixes only via D727_DEVIATIONS.md.
