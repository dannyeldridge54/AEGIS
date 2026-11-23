# PREREG CM-FUSION — hand the fusion work to CubeMind (locked before building), 2026-11-23 14:45 CT
Danny 12:14: "give CubeMind that instead of you and have it do it ... tell it exactly how you've gotten to this point and have it run it."
Build: (1) tools/fusion/fusion_cm.py dispatcher (like chronos_cm) exposing the validated fusion engine as registry tools fusion_* and
element/nuclide lookups; (2) the PC registry gains these tools and a WORKER branch (backup first); (3) 30+ derivation tasks appended
to CubeMind's calc_queue.jsonl (CubeMind derives blind, then the tool grades it — its existing learn loop, step_derive); (4)
CUBEMIND_FUSION_PLAYBOOK.md (the method, the results, the rules) placed in the CubeMind folder and stored as a MEANING record.
Tests: K1 every fusion_* tool runs on its own example in the cloud copy and returns its queued result key; K2 every queued task's tool
returns a finite number for its key; K3 the dispatcher's numbers equal the engine's (rel 1e-12) for 5 spot checks; K4 on the PC the
registry imports and one fusion_* call returns (run in the Linux shell against the deployed files).
Guards: CubeMind's results land as derivations (graded) and HYPOTHESIS proposals; nothing it writes changes the engine; locks,
referee rounds and adoption decisions stay with the cloud session and Danny.
