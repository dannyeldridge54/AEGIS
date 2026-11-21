# PREREG D1928 — single FN flavon, |u| free (new postulate U32 candidate; locked 21 Nov 2026 before running; repo at a3c41be2)
Lock rules from the D1927 referee. Script theory/tests/d1928_flavon_sweep.py reuses the D1925 scan and naturalness code unchanged.
- Grid: 25 log-spaced |u| from 0.01 to 0.3 (factor 1.152 per step). Phase fixed at arg U(0.0457 e^{i49°}).
- Per point: every assignment passing the D1828 ×2/×3 filters gets 2,000 O(1) complex draws (seed 28). A point is natural if its best fit has f7 ≥ 0.05 and fJ ≥ 0.20.
- PASS: a contiguous natural window spanning a factor ≥ 1.5 in |u| (at least 4 grid points). Otherwise FAIL.
- Penalty for the one free size: report the prior fraction P (window width over the 0.01–0.3 log range). The postulate is weighed against D1828 (two fitted sizes) by P, not by best-point naturalness.
- If PASS, U32 = "one flavon, |u| in the window" enters as PHENOMENOLOGICAL. It is not counted as a new scoreboard pass, and it does not yet have a geometric home.
Trials +1 (trials_rungstep.md).
