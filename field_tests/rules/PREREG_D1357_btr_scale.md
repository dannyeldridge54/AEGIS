# PREREG D1357 — what sets the common −4% between our 10D scalar KK masses and BTR's (D1356)

Locked 2026-11-19 before computing. Tool: tools/kaluza/scalar.py (D = 10, γ = 3/2, critical vacuum, Prüfer).
Baseline: ξ ∈ [1e-4, 8], Dirichlet: m L/π = 0.93175, 2.04027 (BTR eq. 5.14: 0.97, 2.13; ratio agrees, D1356).

## Tests
T1 α_E invariance (expected by scaling, checked numerically): rescale the potential by α_E = 0.5 and 2 (y → y/√α_E,
   m² → α_E m², L → L/√α_E). Implementation: scale the eigenvalues by α_E and the y-range by 1/√α_E is equivalent;
   we instead rerun the tool with the ξ range unchanged and report m L/π — must equal the baseline to 1e-6.
   (Done analytically in the note if the tool has no α_E knob; then T1 = statement, labelled [derived].)
T2 lower cut ξ1 ∈ {1e-2, 1e-3, 1e-4, 1e-5, 1e-6} (upper 8), Dirichlet — sensitivity of m L/π to the singular end.
T3 upper cut ξ2 ∈ {6, 7, 8, 9, 10} (lower 1e-4) — sensitivity at the far end.
T4 mixed boundary conditions at the two ends (Dirichlet at one, Neumann at the other), both orders, baseline cuts.

## Rule (fixed now)
- If any single choice in T2–T4 moves BOTH masses by +3% … +5% (same sign, within 1% of each other) → the −4% is that
  boundary/endpoint choice; the open circuit closes as "convention identified" (with the choice named).
- If masses move < 0.5% across T2 and T3 → the cut-offs are not the cause (NULL for cut-offs).
- Anything else → report the numbers; the open circuit stays open.
No reruns to chase the 4%; fixes only via PREREG_D1357_DEVIATIONS.md written first.
