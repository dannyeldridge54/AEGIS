# PREREG A2d-line — NLL-resummed wino line (Ovanesyan–Slatyer–Stewart 2014) at 0.66 and 1 TeV (Djl A) — locked 2026-11-17
Source (fetched, arXiv:1409.8294):
- σ(χ⁰χ⁰ → X) = σ_tree(χ⁺χ⁻ → X) |s₀₀(Σ₁ − Σ₂) + √2 s₀± Σ₁|². At tree level Σ = 1.
- Σ₁ = (e^{Ω+D}/3)(2z^{−4ψ/b₀} + z^{2ψ/b₀}); Σ₁ − Σ₂ = (2e^{Ω+D}/3)(z^{−4ψ/b₀} − z^{2ψ/b₀}); ψ = 1 − iπ.
- z = α₂(μ_Z)/α₂(μ_mχ); D = (α₂(μ_Z)/2π) ln(4m²/μ_Z²) ln(m_W²/μ_Z²).
- Ω (Eq. 24) = −2πΓ₀(z ln z + 1 − z)/(b₀²α₂(μ_Z)) − Γ₀b₁(ln z − z − ln²z/2 + 1)/(2b₀³) − (ln z/2b₀)[8(ln(4m²/μ_m²) − 1) − 2b₀] − Γ₁(z − ln z − 1)/(2b₀²).
- b₀ = 19/6, b₁ = −35/6, Γ₀ = 8, Γ₁ = 8(70/9 − 2π²/3). Scales μ_m = 2m, μ_Z = m_Z.
Inputs:
- α₂(m_Z) MS-bar = 0.00780372/0.232486 (2009.00640, quoted).
- ASSUMPTION (labelled): one-loop running α₂⁻¹(μ) = α₂⁻¹(m_Z) + (b₀/2π) ln(μ/m_Z).
- s from sommerfeld_nlo at LO and NLO (√2 post hoc), v = 1e-3. Our s convention: s = (s₀₀, s₀±), free s = (1, 0).
Output: R = |s₀₀(Σ₁−Σ₂) + √2 s₀±Σ₁|² / |√2 s₀±|² (resummed/tree-SE line ratio), and f_max_resummed = f_max_tree(D1118/D1119)/√R for the three haloes.
Sanity checks (reported, not scored):
- (a) R < 1 (Sudakov suppression).
- (b) R decreases from 0.66 to 1 TeV.
- (c) R at 1 TeV is compared with the "×3–4 one-loop reduction" of 1307.4082.
Verdicts vs SERAPIS-E (f = 0.26 at 1 TeV, 0.14 at 0.66 TeV): PASS if f_max ≥ f.
Script theory/wiring/a2d_line_nll.py (written after this lock).
