# PREREG A2q: wino window upper edge with the endpoint factor (ESTIMATE)
- Input: field_tests/results/a2o_upper_edge.txt (D1324, unchanged) and R(Δ=0.10) from A2p (D1337): 1.1174, 1.1415, 1.1622 at 1.0, 1.25, 1.5 TeV.
- Operation: f_max → f_max/R for every halo, LO and NLO bands. f_pred unchanged. Verdict rule as A2o: PASS if f_max,low ≥ f_pred,high; FAIL if f_max,high < f_pred,low; else BAND-DEP.
- Label: ESTIMATE (LL endpoint; inherits A2o assumptions). Reported as a sensitivity of the D1324 window, not a replacement until NLL endpoint is sourced.
- Script field_tests/scripts/a2q_endpoint_edge.py; output field_tests/results/a2q_endpoint_edge.txt.
