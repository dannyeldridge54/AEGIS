# D1982 DEVIATIONS (before the one rerun, 22 Nov 2026 ~01:00Z)
1. **B5 harness bug.** It counted any line containing "FAIL" as a failure. test_check.py prints the *expected* FLAG verdicts with text such as "verdict always FAIL". **Fix:** compare the first two tokens with loomd.EXPECT, as loomd's self-test does. No expectation changed.
2. **B4 control added (strengthening).** A crash counts as a kill, so a runner that always crashed would score 100 %. **Added:** the unmutated copy must come out PASS through the same runner. If it does not, B4 is VOID.
