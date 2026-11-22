# PREREG D2107: sonar-magnet v2 (Danny 08:54–08:55). A best-first search steered by a goalpost "pull", with sonar pings from every node. Locked before running.

**Space and filters:** as in D2103/D2106 (T⁶/Z₂×Z₂ tilted T₃; PS 3 + 3; tadpole + K completion; fitted-K confinement; α_s within 2σ, M_s ≥ 4e15).

**Nodes:** (χ, A, B, C), visible PS stacks.

**Seeds:** every PS model in the existing catalogues (D2103 near list, D2105 outward, the torus catalogues).

**Pull score** (lower = stronger pull):
score = |α_s − 0.118|/0.0018 + w_exo·[not exotic-safe] + w_ms·[M_s < 4e15] + w_fit·[no physical fit]

**Sonar ping** (expansion of a node):
- every single ±1 change of one visible wrapping integer (keeping SUSY at χ and the PS conditions);
- every move of one χ_i to its neighbours on the rational ladder {p/q : q ≤ Q_ladder, in [1/Q_ladder, Q_ladder]} that keeps all three visible stacks SUSY.

**Best-first:** always expand the lowest-score unexpanded node.

**Echo removal:** canonical dedupe; completions memoised by (χ, residual, parity).

**Archive (quality-diversity):** the best node per direction cell (ln χ rounded to 0.25 per axis).

**Knobs** (live-tunable in tools/seed/sonar/knobs.json; every change is logged with a time stamp): w_exo, w_ms, w_fit, Q_ladder, brane pool L, and a per-node time cap.

**Verdict:** PASS on any hit; the hits/near/0.09 look-elsewhere count is reported.

**Tuning is search steering only.** It never changes the filters or the goalposts (no loosening).
