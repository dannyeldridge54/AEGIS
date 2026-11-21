# PREREG_RW3_PLATEAU — (a) can the dark-cycle saxion be the thread? (b) what hosts the plateau 1 − A e^{−βφ}?
Locked 21 Nov 2026 before computing. AI-assisted. Script theory/tests/rw3_plateau.py (tool tools/weave_cm/weave_reverse.py).
Result: field_tests/results/rw3_plateau.json. Units M_P = 1, H₀ = 1 in the ODE.

## R1 — the 285 H₀ check (main session 10:36, not locked until now)
Saxion of the dark cycle with V = c σ e^{−aσ} (D1793 cross term), a = 2π, σ = 38.6, height ρ_Λ = 3H₀²Ω_Λ,
Ω_Λ = 0.685. m² = (dτ/dφ)² V_ττ + (d²τ/dφ²) V_τ. Two geometries: (i) K = −3 ln(T+T̄) (closed form
m²/H₀² = 2Ω_Λ[(aσ)² − 3aσ + 1]); (ii) swiss-cheese small cycle, 𝒱 = 1e5 (analytic metric).
Rule: the saxion CAN be the thread only if m/H₀ ≤ 3 in either geometry; otherwise FAIL (cannot be the thread).
Also report (derived): whether V = cσe^{−aσ} has a minimum in σ for aσ > 1.

## R2 — plateau exponents of known mechanisms
β = n√(2/k) for K = −k ln(T+T̄) with a 1/τⁿ correction (k = 1, 3; n = 1, 2); β = 2m/√3 for a fibre modulus at
fixed 𝒱 with τ₁^{−m} (m = ½, 1, 3/2, 2). A mechanism MATCHES a tested tilt if within 5 % of √2, 2 or 2√2.

## R3 — can a small-β plateau thaw to the data's region? (forecast-type; the data are known, so this counts
only on future data)
Thread V = V_L(1 − x), x = A e^{−βφ} (A is absorbed into the start value x_i; see R4). Ω_m = 0.31, Ω_r = 9e-5,
field frozen at a = 1e-3, V_L shot so that H(a=1) = 1; 300 log-spaced x_i ∈ [1e-3, 0.999]; viable if V > 0 at a = 1.
Report w₀ = w(a=1) and a CPL least-squares fit w = w₀ + w_a(1−a) on a ∈ [1/3, 1].
- Validation gate: β = 2√2 must reach a viable point with w₀ within ±0.03 of −0.79 and w_a within ±0.15 of −0.36
  (D1628 best point). If the gate fails, R3 is INVALID (no rerun to chase it; a DEVIATIONS file first).
- For β = 1/√3 (fibre, m = ½) and β = √(2/3) (K = −3 ln, n = 1): VIABLE if some viable x_i gives
  −0.82 ≤ w₀ ≤ −0.76 (the D1628/D1692 region); report its w_a.

## R4 — A degeneracy (derived, reported)
For the leading-order form, φ → φ + c maps A → A e^{−βc}, so background data see only x_i = A e^{−βφ_i}.

## R5 — natural height at the Weave's SUSY scale (estimate, reported)
For a fibre-type thread the potential is V_sub ~ m₃/₂⁴ (Cicoli–Pedro–Tasinato, arXiv:1203.6655).
Report V_sub/ρ_Λ, the implied m ~ m₃/₂²/M_P in units of H₀ at m₃/₂ = 2.5e5 GeV, and the m₃/₂ that would make
V_sub = ρ_Λ.

## Decision rule (one word)
- DERIVED: a Weave-internal mechanism fixes β to a tested tilt and A = 7.30 with no new input.
- HOSTED: some R2 mechanism is R3-VIABLE (or matches a tested tilt) AND its R5 natural mass at the Weave's
  m₃/₂ is ≤ 3 H₀.
- OPEN: otherwise (shape available, height/mass not natural at the Weave's SUSY scale).
