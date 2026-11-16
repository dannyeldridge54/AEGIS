# Loop lessons (read FIRST every tick; append after every tick's DERIVE step)
Each line: date, D-number, the lesson, and how it changes the next steps. Keep it short; condense when it grows past ~60 lines.

- 2026-11-15 D720/D724/D725: eigen- or Takagi methods fail on degenerate or nilpotent blocks. Use a symmetric square root, and check residuals before trusting a coupling.
- 2026-11-15 D727: opposite-sign mass eigenvalues give an axion-like coupling 2sθ′. Never assume λ ∝ ΔM.
- 2026-11-15 D728→D738: check the assumed ratio ranges (ΔM/M) against the model's own output before calling something a "natural" pass.
- 2026-11-15 D759: nested finite differences make n_s noisy. Use analytic or mpmath derivatives, and check C = 0 against the earlier untilted result.
- 2026-11-15 D760: a fetched paper's species function was log η (F₁), not E(τ,2). Check which modular function a source actually uses before building on it.
- 2026-11-16 D762: check whether a vacuum or trajectory sits on a CP-conserving locus (imaginary axis, Re τ = ±½, the unit arc) before claiming any CP-violating result. Our two vacua and the inflaton line all do, so every CP effect needs an explicit phase source.
- 2026-11-16 D762: a PASS that leaves a parameter "unspecified" (here δ) hides an assumption. Make it a postulate at once, so the derived:assumed count stays honest.
- 2026-11-16 D763: before claiming a low-energy prediction from a high-energy mechanism, check whether the low-energy parameter cancels out of the formula (here U drops out of H = Y†Y). Run a real-parameter control grid as the K4 regression.
- 2026-11-16 D763: write a postulate's falsifier as "what result would favour the ALTERNATIVE". It is sharper than "what would disfavour the postulate".
- 2026-11-16 D764: "j(τ) real ⇔ CP-conserving" is a one-line, modular-invariant CP test. Use it instead of basis-dependent coupling phases.
- 2026-11-16 D764: when a mechanism ties a new field to the inflaton (here U₂ = c/U₁), check at once whether it changes the inflaton's kinetic term. Queue a forward check before trusting the old n_s and r.
- 2026-11-16 D765: an imported vacuum relation that involves the inflaton changes the kinetic term, here doubling the Kähler metric and r. Check every new constraint against the inflaton direction before using it for other sectors.
- 2026-11-16 D765: when reusing a solver under a new field map, grep it for hard-coded maps (s2, start values) and write the DEVIATIONS before the first run, not after a crash.
- 2026-11-16 D766: every new flux or brane ingredient must be booked against the tadpole (32 = n_flux + 2n_D3 + n_O3′) the moment it is proposed. Here it forced 5/5/5+1 → 3/3/3+1.
- 2026-11-16 D766: a frozen map node can't be changed by a MAP line, by design. A label slip on a frozen node needs a manual, documented edit, which is what D765a did.
- 2026-11-16 D767: rescale from the actual formula, not from a summary range. D766 scaled a union range by N and missed that the tilt depends on N − N0. The forward DERIVE step caught it, which is the design working.
- 2026-11-16 D768: when every derivation route is closed, check how the leading published models handle the same gap. If they also choose the function (e.g. a nilpotent metric), the honest status is "postulated at the field's standard". Record what still distinguishes us (here r is ~4.5× lower).
- 2026-11-16 D769: a lock's success criterion must test the physical question at the right moment. "Ends in the valley" had to be judged after reheating-era relaxation, not at ε = 1. When writing a PREREG, state WHEN each quantity is evaluated.
- 2026-11-16 D769: write the plateau in the exact form the solver uses. The shorthand 1 − E(ρ)/E and the code's Ê/(Ê + 1) give the same n_s and r but different N(y) (D769 run 1 was invalid for this reason).
- 2026-11-16 D770: in modular field spaces, judge "where it settled" after reducing to the fundamental domain. A raw final point like ½ + 0.29i is ρ in disguise.
