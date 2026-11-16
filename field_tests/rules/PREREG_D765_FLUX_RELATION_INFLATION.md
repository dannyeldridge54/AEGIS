# PREREG D765: SERAPIS-E n_s and r if the flux relation U₂ = c/U₁ holds during inflation
Locked 2026-11-16 before computing. Script: theory/modular/flux_rel_inflation_d765.py (the D692 script with y = e^{√2φ} replaced by y = e^{φ}; nothing else changed). Output: field_tests/results/flux_rel_inflation_d765.txt.
Derivation (fixed now):
- K = −ln Im U₁ − ln Im U₂. With U₂ = c/U₁ (c real), Im U₂ = |c|·Im U₁/|U₁|².
- −ln Im U₂ = −ln Im U₁ + ln U₁ + ln Ū₁ + const. The middle terms are a Kähler transformation.
- So K_eff = −2 ln Im U₁ up to a Kähler transformation, and the metric doubles: φ = (1/√2)·√2 ln y = ln y.
- Assumptions: the relation is enforced by a mass ≫ H_inf, and the potential's U₂ dependence along the relation is not included (only the kinetic change is tested).
Runs: C ∈ {0, 6e-7, 1e-6, 1.3e-6}, N* ∈ {48.4, 49.9}, the same as D692.
K4: the D692 script itself reproduces its committed results (C = 0, N* = 48.4: n_s 0.9606, r 3.752e-4). Checked by running the original first line only if time allows; otherwise accepted from the committed file.
Decision:
- Report the n_s, r shifts. If no C ≤ 4e-6 keeps n_s in 0.970–0.975 AND r in 4.55–5.12e-4, it is a CORRECTION: the flux-relation completion conflicts with the frozen SERAPIS-E bands and P2 must use the "relation only at the minimum" option, or be dropped.
- If the frozen bands still hold, it is CONSISTENT.
