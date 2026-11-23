# Field-map rotation: the ping-pong engine on every toolkit

Started 2026-11-23 on Danny's word ("add the engine to all of them and have them start mapping out each one of their fields
completely"). Template: releases/nuclear_rung_2026-11-23 (README map + RESEARCH_LIMB).

Each loop tick takes the next toolkit and does ONE rung. PRIORITY FIRST (Danny, 08:54): speed it up with our engine.
0. Speed rung (before the map): profile the toolkit's slowest paths (time each locked test / main command), then redesign
   with what we have built where it helps: the Loom fast fitter (tools/fastcmb/loom_fast.py: parallel starts, warm starts,
   thread control), surrogate / emulator caches with locked accuracy, closed-form or analytic shortcuts (as Chronos'
   Bateman vs matrix exponential), vectorised numpy, a browser (JS) engine for instant interactive use.
   Rule: lock a speed prereg first (PREREG_SPEED_<tool>.md: which paths, the accuracy tolerance the fast path must keep
   against the old path, the timing protocol). The old path stays as the reference; the fast path is accepted only if it
   matches the reference within the locked tolerance on the locked test set. Record before/after timings in the ledger.
   If nothing can be sped up without losing accuracy, say so and move on.
1. Field map: the field's own big planning studies / reviews (2-4 searches, fetch the best 2-3), the Oklahoma people in it,
   what the field needs, what our toolkit already covers, the gaps, a cheapest-first build order. Lantern on top.
   File: releases/field_maps/<field>.md
2. Lock a short referee charge (field_tests/rules/PREREG_RR_<tool>.md + .sha256) before the round.
3. One independent referee round on the toolkit (code, tests, claims). Fixes only through a DEVIATIONS note written first;
   re-run its tests (CI and tools/gifts/pingpong_suite.py); ping-pong until NULL.
4. Record in tools/gifts/REFEREE_LEDGER.md; commit and push.

Order: 1 Spindle (quantum simulation / cold atoms) -> 2 Aion (neutrino mass) -> 3 Zurvan (SUSY / naturalness) ->
4 Hyperion (astrophysics: stars, BBN, neutron stars) -> 5 CERN+1 (collider physics) -> 6 Lattice Lab (lattice QCD) ->
7 Janus (astro / lt) -> 8 SERAPIS calc (cosmology) -> 9 chem -> 10 golden.
Done: 0 Chronos / nuclear (map + limb + referee R77, R78, R78b pending).
