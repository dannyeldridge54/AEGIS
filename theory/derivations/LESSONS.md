# Loop lessons (read FIRST every tick; append after every tick's DERIVE step)
Each line: date, D-number, the lesson, and how it changes the next steps. Keep it short; condense when it grows past ~60 lines.

- 2026-11-15 D720/D724/D725: eigen- or Takagi methods fail on degenerate or nilpotent blocks. Use a symmetric square root, and check residuals before trusting a coupling.
- 2026-11-15 D727: opposite-sign mass eigenvalues give an axion-like coupling 2sθ′. Never assume λ ∝ ΔM.
- 2026-11-15 D728→D738: check the assumed ratio ranges (ΔM/M) against the model's own output before calling something a "natural" pass.
- 2026-11-15 D759: nested finite differences make n_s noisy. Use analytic or mpmath derivatives, and check C = 0 against the earlier untilted result.
- 2026-11-15 D760: a fetched paper's species function was log η (F₁), not E(τ,2). Check which modular function a source actually uses before building on it.
- 2026-11-16 D762: check whether a vacuum or trajectory sits on a CP-conserving locus (imaginary axis, Re τ = ±½, the unit arc) before claiming any CP-violating result. Our two vacua and the inflaton line all do, so every CP effect needs an explicit phase source.
- 2026-11-16 D762: a PASS that leaves a parameter "unspecified" (here δ) hides an assumption. Make it a postulate at once, so the derived:assumed count stays honest.
