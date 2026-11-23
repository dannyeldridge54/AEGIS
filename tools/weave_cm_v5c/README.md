# CubeMind v5c (22 Nov 2026, 22:17-22:25 CT)
Danny: "tell it to run the engine alongside itself and/or postulate to it and then use the engine and it will check itself."
- patch_selfcheck.py patches mindmem/learn_loop.py step_derive (backup .bak_v5c_22nov on the PC):
  postulate (formula as one expression) -> engine evaluates it exactly alongside the model (formula_ok, graded apart from arithmetic)
  -> on a miss, a self-check call names the first wrong step + class (formula/units/arithmetic/reading) + one rule, stored per tool
  (kind derivation_rule) and fed back into the next prompt for that tool. Safe evaluator: math names + task inputs only, no builtins.
- WEAVE_FACTS.txt gained a v5c section with the self-check procedure and the definitions it kept missing (rung size, Rydberg MeV->eV,
  tau_q decay, cube root, D2132 verdict rule). Note for grading honesty: these definitions are now TAUGHT, so later scores on those
  tools are not blind-from-scratch; the formula/arithmetic split is the new measure.
- Grade before v5c (9,568 derivations, qwen3:8b): 64% overall, 68% recent; A: rung_of 99, koide 98, proton 96, rladder 95;
  F: weave_tauq 0/150, weave_atomic 17%, weave_rung 18%. Needs a CubeMind restart to load the patch.

## Fix found while grading (22:25 CT)
CubeMind's derivations stopped at 21:02 because the queued `weave_verdict` item hit the registry's 10 s tool timeout while 15 PC fits load the CPU; a failing queue item was never marked done, so it blocked the queue every cycle ("derive: tool error"). Fixes on the PC: registry timeout for weave_verdict 10 -> 90 s (backup registry.py.bak_v5c_22nov); step_derive now logs tool errors to weave_data/calc_errors.txt and parks a queue item after 3 failures. No restart needed: learn_loop re-execs itself when its code changes.
