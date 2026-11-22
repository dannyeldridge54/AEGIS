# PREREG D1994: referees report the size of every detected data change. Locked before code and runs.
- D1992 verdict: tests 1 and 2 PASS (60 s seed 2033, plus triangulation seed 2036; 20 s seed 2034, with 0 false alarms). Test 3, the replay on seed 2035, gave specificity 5/7 < 6/7: **FAIL, which stands.**
  - The two flags were α_s releases with real shifts of 0.17σ and 0.11σ. The CUSUM integrates persistent sub-σ steps.
- **Rule.** Every detector-C alarm on stream s carries a magnitude m = \|estimate at alarm − baseline before restart\| / σ_release. It is **MATERIAL** if m ≥ 0.5, otherwise **MINOR**. Both are logged; only MATERIAL counts as a data event for the referee's report. The alarms used by bars A1–A5 are unchanged.
- **Test** (new seed 2037, replay):
  - recall = 1 on the detectable releases (\|Δ\|/σ ≥ 1), counting MATERIAL detections within 2 s;
  - specificity ≥ 6/7: no MATERIAL detection within 2 s on the quiet-expected releases (\|Δ\|/σ < 0.25).
- **Also on new seeds:** a 60 s synthetic run (2038) and a 20 s synthetic run (2039), each with A1–A5.
- **PASS needs all three.**
