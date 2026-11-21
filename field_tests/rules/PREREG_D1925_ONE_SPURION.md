# PREREG D1925 — one spurion for both quark sectors (locked 21 Nov 2026 before running; repo at 3b1d1256)
Question (D1923 point 8, KILL-FIRST): must the quark lock have two independent breaking sizes (u_u ≠ u_d)?
Test: theory/tests/d1925_onespurion.py. Same 7^6 charge grid and ×2/×3 filters as D1828; uu = ud = u with u = U(0.0457 e^{i49°}) (|u| = 0.0259, the existing down step, not re-tuned). Every surviving assignment gets the D1829 naturalness run (5,000 O(1) complex draws, seed 25).
PASS: the best assignment has f7 ≥ 0.05 AND fJ ≥ 0.20 (the D1829 bars). FIT-NOT-NATURAL: fits exist but miss the bars. NONE: no assignment passes the filters.
Report only (no verdict): the same scan at |u| = 0.0018 and |u| = 0.1 (power/stability).
If PASS: "two sizes needed" is withdrawn; one spurion suffices, and the single-modulus homes (U₃ near i, a single FN flavon) reopen. Trials: +1 (trials_rungstep.md).
