# PREREG D1932 — pulse ring 0: the rung step (rule 6h, 7 nulls in a row; locked 21 Nov 2026 before running; repo at e8040ceb)
Script: theory/tests/d1932_ring0_rungstep.py. It uses the D1925 filters unchanged and the helper tools/loom/triangulate.py.
1. **Edges.** Bracket the edges of the one-spurion fit window around 0.027, starting from [0.0234, 0.027] and [0.027, 0.0311]. Each round takes three readings at the quarter points. Resolution is 1e-6, and the run stops after 7 null rounds in a row. VOID if the start brackets do not straddle the edges.
2. **Inside the window.** Three points at the quarter points, three seeds each (2,000 draws). The window is natural if the median over seeds has f7 ≥ 0.05 and fJ ≥ 0.20 at all three points.
3. **Three vectors on the rung step.** The one-spurion window's geometric centre, the D1832 lepton slip 0.0253, and the neutrino θ-step e^{−9π/8}. Report their median ± spread and the offset from the six-sector median 0.027.
This is a measurement of existing results, not a new postulate, so the flavour cap is untouched. No PASS/FAIL. Report whether the window contains 0.027, 0.02587 and 0.0253.
