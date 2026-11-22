# Loom auto round 6

**Decision:** CONTINUE. Null True (streak 5). Endpoint False (0/5).

**Field run** (20 s, seed 2032): FAIL; 2741.4 pulses/s; accuracy {'A1': True, 'A2_recall': False, 'A2_prec_fast': True, 'A2_prec_full': True, 'A3': True, 'A4': False, 'A5': True}
**Goalposts:** {'PASS (FIT)': 7, 'UNSCORED': 9, 'PASS': 18, 'PASS (bound)': 2, 'TRUST': 1, 'PASS (null)': 7, 'FAIL': 1, 'OPEN': 15, 'FAIL (FIT)': 1}. **Nodes DONE (s):** {1: 0.0, 2: 16.99, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0, 8: 0.0, 9: 0.0}. **STUCK:** {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}. **Fits spent:** ['TR', 'm32', 'split'].
**Battery:** {'B8': True, 'B1': True, 'B2': True, 'B3': True, 'B5': True, 'B6': True}. **PASS-label check:** ok. **Online FDR:** 10 tests, significant tensions ['A1'].

**Lock map:** {1: 'LOCKED', 2: 'LOCKED-BY-FIT', 3: 'TRUST (no margin; cannot lock, G-T5)', 4: 'NO LOCK', 5: 'LOCKED-BY-FIT', 6: 'LOCKED-BY-FIT', 7: 'LOCKED-BY-FIT', 8: 'LOCKED-BY-FIT', 9: 'TRUST (no margin; cannot lock, G-T5)'}

**Next actions:**
- derive L4: derive the 15.3 % lepton vs neutrino rung mismatch from the geometry (U3, fluxes (4,4,8)) with no new fit; L5-L9 may not move until L4 is locked or explicitly held
- test L5: wino verdict at the edge, no nudging of m3/2
- referee LNone: referee due this round (every 2nd round): fresh-context review of the board and of the last overclaims
- owed LNone: the prediction / FIT / TRUST ledger file (field_tests/loom/pft_ledger.json) with honest relabels
- explore LNone: null round: spend the exploration share on the loosest direction
