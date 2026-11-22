# Loom auto round 12

**Decision:** STALL. Null True (streak 11). Endpoint False (1/5).

**Field run** (60 s, seed 2038): PASS; 4225.9 pulses/s; accuracy {'A1': True, 'A2_recall': True, 'A2_prec_fast': True, 'A2_prec_full': True, 'A3': True, 'A4': True, 'A5': True}
**Goalposts:** {'PASS (FIT)': 8, 'UNSCORED': 9, 'PASS': 18, 'PASS (bound)': 2, 'TRUST': 1, 'PASS (null)': 7, 'FAIL': 1, 'OPEN': 15}. **Nodes DONE (s):** {'1': 0.0, '2': 57.0, '3': 0.0, '4': 0.0, '5': 0.0, '6': 0.0, '7': 0.0, '8': 0.0, '9': 0.0}. **STUCK:** {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}. **Fits spent:** ['TR', 'm32', 'split'].
**Battery:** {'B8': True, 'B1': True, 'B2': True, 'B3': True, 'B5': True, 'B6': True}. **PASS-label check:** ok. **Online FDR:** 40 tests, significant tensions [].

**Lock map:** {1: 'LOCKED', 2: 'LOCKED-BY-FIT', 3: 'TRUST (no margin; cannot lock, G-T5)', 4: 'NO LOCK', 5: 'LOCKED-BY-FIT', 6: 'LOCKED-BY-FIT', 7: 'LOCKED-BY-FIT', 8: 'LOCKED-BY-FIT', 9: 'TRUST (no margin; cannot lock, G-T5)'}

**Next actions:**
- derive L4: derive the 15.3 % lepton vs neutrino rung mismatch from the geometry (U3, fluxes (4,4,8)) with no new fit; L5-L9 may not move until L4 is locked or explicitly held
- test L5: wino verdict at the edge, no nudging of m3/2
- referee LNone: referee due this round (every 2nd round): fresh-context review of the board and of the last overclaims
- explore LNone: 7 null rounds without balance is a STALL, not the endpoint: change the approach (broad then narrow; mine the loose still-point directions; a tournament of competing explanations for the strained layer)
- owed LNone: the prediction / FIT / TRUST ledger file (field_tests/loom/pft_ledger.json) with honest relabels
