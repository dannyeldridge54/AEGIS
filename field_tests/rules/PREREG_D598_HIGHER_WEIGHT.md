# PREREG D598: κ at τ = i for higher-weight Γ₂ doublets (route (b) of D597), locked before computing
- Doublet multiplication 2⊗2 → 2: (a, b) → (a₁b₂ + a₂b₁, a₁b₁ − a₂b₂).
- Weight-4 doublet: Y⁽⁴⁾ = Y⁽²⁾ ⊗ Y⁽²⁾ projected to 2. Weight-6 doublet: Y⁽⁶⁾ = Y⁽²⁾ ⊗ Y⁽⁴⁾ projected to 2. Weight-8 doublet: Y⁽⁸⁾ = Y⁽⁴⁾ ⊗ Y⁽⁴⁾ projected to 2.
- For each, compute κ = |(UᵀA(Y′)U)₁₂|/|s| at τ = i, exactly as in D597 (same code path).
- Y_B scales linearly with κ (D597 plateau), so Y_B,plateau(k) = 1.25e-11·κ_k/1.2635.
Verdict:
- PASS for weight k if Y_B,plateau ≥ 8.75e-11 (κ ≥ 8.85).
- If a doublet vanishes at i (s = 0), report "degenerate at i" (κ undefined).
