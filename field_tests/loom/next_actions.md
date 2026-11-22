# Loom planner, round 3

**Mission:** Derive and test the Weave unified field equation: one central equation whose three fields (S, T, U) balance every node with real predictions, not fits.

**Endpoint:** not reached (0/5 conditions met). Progress this round: False.
**Blocking:** layer 2 LOCKED-BY-FIT; layer 3 TRUST (no margin; cannot lock, G-T5); layer 4 NO LOCK; layer 5 LOCKED-BY-FIT; layer 6 LOCKED-BY-FIT; layer 7 LOCKED-BY-FIT; layer 8 LOCKED-BY-FIT; layer 9 TRUST (no margin; cannot lock, G-T5); 4 fits spent: MN, m32, TR, split; no prediction/FIT/TRUST ledger yet

## Next actions (in order)
1. **derive** L4: derive the 15.3 % lepton vs neutrino rung mismatch from the geometry (U3, fluxes (4,4,8)) with no new fit; L5-L9 may not move until L4 is locked or explicitly held. Guard: N0 inside-out; G-T3; LOCK. Tools: weave_rung, weave_rung_of, theory/tests/d1932_ring0_rungstep.py, theory/tests/d1925_onespurion.py. **Lock first.**
2. **test** L5: wino verdict at the edge, no nudging of m3/2. Guard: N0 inside-out; G-T3; LOCK. Tools: weave_W0, weave_wino, lhc_dt_limit, lhc_lifetime. **Lock first.**
3. **owed**: automated check: every PASS in a verdict file carries FIT / NO-POWER / CONDITIONAL where one applies. Guard: HONEST. Tools: tools/loom/lensing.py, tools/loom/check.py, tools/loom/method_tests_3axis.py.
4. **explore**: null round: spend the exploration share on the loosest direction. Guard: G-T6 null rounds count only with every node balanced. Tools: tools/loom/still_point.py, tools/loom/compass.py.

## Agents to wake
- N0 centre referee: always
- node agents: none (no inputs changed)
- axis agents: S = dilaton S (ln T_R, n_s, reheating); T = volumes T (ln m3/2, KKLT, spectrum); U = complex structure U (ln u, flavour rungs)
- edge agents: edge_out = outside layer 9: what the late-universe and collider data push back toward the centre; edge_in = inside layer 1: what the rung step / knot geometry pushes outward
- referee: False
