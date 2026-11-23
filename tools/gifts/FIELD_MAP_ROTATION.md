# Field-map rotation: the ping-pong engine on every toolkit

Started 2026-11-23 on Danny's word ("add the engine to all of them and have them start mapping out each one of their fields
completely"). Template: releases/nuclear_rung_2026-11-23 (README map + RESEARCH_LIMB).

Each loop tick takes the next toolkit and does ONE rung:
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
