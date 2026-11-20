# PREREG Q4 — DEVIATIONS (written before any code change or recomputation)
## D1 (20 Nov 2026, joint audit D1750/D1751)
The lock fixed N* = 55 in Δn_s = 2ΔN*/N*². The inflation level the Weave actually uses (serapis_10d) has N* = 50.37
(serapis_6d 50.57). Change: the τ_q tools (engine quark level, weave_tauq) take N* from the inflation model in use
(engine: J.predict(model, Nstar)['Nstar']; weave_tauq: argument Nstar, default 50.37) instead of the constant 55.
Nothing else changes: same filters (T_dec ≥ 5 MeV, D ≤ 1e3, |Δn_s| ≤ 0.003), same formulas, no tolerance loosened.
The locked Q4 result file stays as recorded (computed with N* = 55). The recomputed window is reported beside it,
whatever it is; Q4's verdict is not re-graded upward by this change.
