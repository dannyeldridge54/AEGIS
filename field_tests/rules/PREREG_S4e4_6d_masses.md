# PREREG S4e4 — 6D subcritical scalar KK masses (large list 12b)

Locked 2026-11-17 before computing. Label: COMPUTED prediction of our own model (no external target).
Background: the 6D subcritical vacuum exactly as in theory/strings/s4e_scalar_masses.py (D=6, γ=(D+2)/(D−2), δ, w, interval ξ∈(0, π/2w)).
Solver: the same Prüfer shooting function `spectrum` (validated in ratio vs BTR; D1214 two solvers agree to 1e-7 on 10D). BC D (the BC that matched BTR's ratio).
Convention: C0 (warp as written, no shift), as fixed by D1216. Report m², L, m L/π for the lowest two modes and the ratio m₂/m₁.
Convergence check (fixed): endpoint cutoffs ε = 1e-4 and 1e-5 of the interval; result is STABLE if m₂/m₁ changes ≤ 0.5% and each m L/π ≤ 1%.
Verdicts: STABLE → record as COMPUTED (convention C0; absolute scale carries the unexplained ~4% convention offset seen in 10D, D1216); UNSTABLE → record as NOT CONVERGED, no rerun with other cutoffs except via a written DEVIATION.
Tachyon check: report whether the lowest m² is negative (instability) — a negative eigenvalue is a physics result, not a failure.
