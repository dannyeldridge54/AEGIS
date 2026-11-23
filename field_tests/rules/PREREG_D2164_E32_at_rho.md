# PREREG D2164: is A = 7.30 protected at strong coupling? (locked 22 Nov 2026 ~23:20 CT, before computing)
Danny 23:16 "how do we derive them" / "get that done". Biggest hole (D2150a): g_s >= 1 at the knot, but A = (8/3)·2ζ(2)/ζ(3) = 7.298 comes from the first two (weak-coupling) terms of E(S, 3/2).
Compute the exact E(S, 3/2) = 2ζ(3) y^{3/2} + 4ζ(2) y^{-1/2} + I(S), with the D-instanton sum (Green–Gutperle)
  I(S) = 8π y^{1/2} Σ_{m≠0} Σ_{n≥1} |m/n| e^{2πi m n x} K_1(2π |m n| y),  S = x + i y,
at the knot S = ρ = e^{iπ/3} (x = 1/2, y = √3/2), and at S = i for comparison.
Validation before scoring: SL(2,Z) invariance E(S) = E(-1/S) at a generic point to 1e-10.
Measure: δ = I(ρ) / (4ζ(2) y^{-1/2}) = the instanton part relative to the term that carries A. A_eff = A (1 + δ) if A rides on the subleading term.
Rule: |δ| < 0.05 -> A is PROTECTED at the knot to within |δ| (the ~14 D2150a items keep their numbers within that); 0.05 <= |δ| < 0.3 -> SHIFTED (re-derive with A_eff); |δ| >= 0.3 -> NOT PROTECTED (weak-coupling A has no meaning at the knot).
Caveat stated now: this tests only whether the exact function stays close to its two-term form at ρ; it does not supply the dynamical mechanism (the F-theory constant-coupling reading stays OPEN).
