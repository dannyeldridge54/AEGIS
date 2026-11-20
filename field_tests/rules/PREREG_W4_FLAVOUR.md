# PREREG_W4_FLAVOUR — Weave Control flavour level (locked 20 Nov 2026, before computing)
Item W4 (tools/weave_control/LOOP_STATE.md). The level DISPLAYS already-locked flavour results through the engine and adds one new comparison (the post-JUNO global sin²θ₁₂). No new model, no tuning.

## Inputs (sourced)
- sin²θ₁₃ = 0.02195 (NuFIT 6.0 NO IC19, arXiv:2410.05380, as used in D1667).
- sin²θ₂₃ cases: 0.561 (NuFIT IC19) and 0.470 (IC24); T2K+NOvA sin²θ₂₃ = 0.56 picks 0.561 (D1690).
- sin²θ₁₂ data: JUNO first data 0.3092 ± 0.0087 (arXiv:2511.14593); post-JUNO global 0.3085 ± 0.0073 (arXiv:2511.21650, NEW here); NuFIT 6.0 + JUNO combination 0.3084 ± 0.0070 (D1652).
- δ_CP data: NuFIT 6.0 NO (IC19 177 +19/−20, 3σ [96°, 422°]; IC24 212 +26/−41, 3σ [124°, 364°]); T2K+NOvA joint (Nature 2025): ordering-marginalised 1σ [214°, 313°], peak 275.4°, NO 3σ [−1.38π, 0.30π] (D1669, D1690).
- Lepton masses: PDG 2024 (already in the engine).

## Computations (formulas fixed now)
- TM1 (first TBM column kept): sin²θ₁₂ = 1 − 2/(3 cos²θ₁₃). Expected 0.3184 (D1667).
- TM1 δ_CP from the TM1 sum rule, as in D1667/D1669: both branches for each sin²θ₂₃ case (expected 74.3°/285.7° at 0.561; 97.6°/262.4° at 0.470). The engine must REPRODUCE these to ±0.5°, or the level is not shown.
- Exact TM2 sin²θ₁₂ = 1/(3 cos²θ₁₃) shown as the excluded reference (D1652: 0.3408).

## Tests and status
- sin²θ₁₂ pull of TM1 vs each data value: |pull| < 2 pass, 2–3 tension, ≥ 3 fail. The STATUS uses the post-JUNO global value (newest combination); the others are shown.
- δ_CP: each branch is 'inside' or 'outside' the T2K+NOvA marginalised 1σ and the NuFIT 3σ ranges; status pass if the lower branch for the T2K+NOvA-preferred θ₂₃ (0.561) is inside both.
- Koide Q and Brannen δ as already in the engine (Q pull from m_τ only; δ is a domain choice, stated).
Labels: TM1 and S₄ are ASSUMED (P-S4, register B5); δ = 2/9 has no mechanism (C-δ).
