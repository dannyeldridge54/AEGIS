# PREREG J7k — the 3 models still listed after J7h, rerun on Danny's PC with long limits
Locked 2026-11-17 before any J7k number. Models and parameters exactly as J7h (PREREG_J7h_pulse_fixups): RPQTI (10, 0.01, −0.01), HI ξ = 20000,
KMIII ν = 1e6 (α = 1e10, β = 1e4). Change: limits only — ASPIC driver timeout 3600 s (J7h: 300 s), per-model Janus/MS wall limit 2 h (J7h: 20 min).
ASPIC: the PC build (@75400d2, verified identical to the cloud build on the lfi check, max rel diff 0.0). Same method, claims and reporting as J7f
(pulse 1) and J7g (pulses 2–3); results in field_tests/results/janus_j7k_p1.part.jsonl / _p23.part.jsonl, reported on their own and merged into
the pulse totals stating they came from J7k. A model still without a result is LISTED with its reason; no further reruns for these three.
