# PREREG D2260 — UFE engine stages 5-6: layered pulse and gate work orders (locked 25 Nov 2026)

**Script.** `tools/field_engine/ufe_pulse.py`, written after this lock, run once. Output `field_tests/results/d2260_ufe_pulse.json` and
`bridge/UFE_GATE_WORK_ORDERS.md`.

## Stage 5 — layered pulse (centre outward)
Five layers, run in order each pulse. A layer runs only if every layer inside it is SOLID.
| Layer | Content | SOLID when |
|---|---|---|
| L0 mathematics | stage-2 numbers N1-N9 (ufe_stages.stage2) | all PASS |
| L1 sectors | ufe_pack tools whose model is a single sector or mathematics, each fitter vs its independent tester on 50 random inputs per ring, rings 0-2 | all pass |
| L2 bridges | ufe_pack bridge tools (loop_det, flux_mass, hessian, thread) the same way, plus combine() on all sector pairs | all pass; combine(weave_v4, serapis_e) is OPEN |
| L3 consistency | stage-3 symbolic steps and the stage-4 finder | all REPRODUCE; finder lists every disagreement in the lock D2259 list |
| L4 perturbations | gated: not run (Danny's direction: no testing until he says) | reported GATED |
Each layer also runs the Loom checks that apply: C3 VALIDATION (a reference value reproduced before use: E_2(rho) by two methods) and C1
INDEPENDENCE (no two tools in a layer return values that move together exactly under random input changes).
**Pass rule.** Three pulses with seeds 1, 2, 3 give the same layer states. A layer that is SOLID in one pulse and not another is reported UNSTABLE.

## Stage 6 — gate work orders
Every OPEN or BLOCKED gate in ufe_pack.GATES becomes a work order: what input would close it, who can supply it, what file would count.
**Closing rule.** A gate is CLOSED only when a named file at a named commit contains the derivation or the source record. No gate is closed by
relabelling. One gate is proposed for closing in this run, on a record that already exists:
- gauge convention: D2257 (commit e5811a95, 24 Nov) states the D2051 numbers use 1/g_s = Im S and the notation should read sigma + 9 Im S.
  This is the project's own source record, written in response to the agents' earlier flag. It closes the gate as RESOLVED-BY-RECORD; the
  agents may reopen it if D2257 does not cover the full transformed K, W, f and theta term (their stated requirement).
All other gates stay OPEN or BLOCKED.
