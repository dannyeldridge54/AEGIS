# PREREG_TM1_DCP — BIG LOOP Q2: TM1 δ_CP versus NuFIT 6.0 (locked D1669, 2026-11-20 00:16 UTC)
Predictions (D1667, TM1 sum rule): s₂₃² = 0.561 → 74.3° or 285.7°; s₂₃² = 0.470 → 97.6° or 262.4°.
Data (NuFIT 6.0, arXiv:2410.05380, NO), each paired with its own s₂₃²:
- IC19 without SK-atm: s₂₃² = 0.561, δ = 177 (+19/−20), 3σ [96, 422].
- IC24 with SK-atm: s₂₃² = 0.470, δ = 212 (+26/−41), 3σ [124, 364].
Score: inside or outside the published 3σ range (angles mod 360, so 422 ≡ 62). Approximate pull: piecewise linear through the 1σ and 3σ points.
Rule: a branch SURVIVES if inside 3σ. The TM1 model survives if at least one branch does, for each dataset.
Script: field_tests/scripts/tm1dcp/run.py
