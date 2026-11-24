# PREREG D2231 — the "hole" is the dark sector (Danny 17:59 "a tiny hole in the right place to generate thrust", 18:00 "consider darker
# matter equivalent", "model like that", 18:02 "Run"). Written before computing, 23 Nov 2026.
Input (D2230 at rho = 3/2 + referee round 10, triangulated with the builder diagnostic tools/seed/z6p_diag_d2230.py): 36,864 visible
(a,b,c,d) choices pass F1 (tree split), Sym_a = 0, three chiral doublets and the right-handed quark filters; all die at the 12-component
tadpole. Bulk part is saturated; the miss is purely exceptional and small (closest: +-2 on four exceptional charges, doubled convention).
One extra brane cannot fill it (any brane carries positive bulk). Named levers (referee): 3 hidden stacks splitting the bulk budget, N > 4.
Test: for every distinct passing visible quadruple at rho = 3/2, search hidden sectors of 1, 2 or 3 stacks, each a SUSY fractional cycle of
any rho = 3/2 bulk class (|w| <= 6 variants), ranks N_i in 1..6, such that the full 12-component tadpole cancels exactly (bulk + exceptional).
Every hit is then scored as the dark sector:
  D1 massless hypercharge (F2, D2167 test) on the visible stacks;  D2 no chiral visible-hidden matter (T3 = 0: sum |I(v,h)| + |I(v,h')| = 0);
  D3 extra massless U(1)s (hidden + visible, beyond Y) <= 2 (Delta N_eff < 0.14 at 0.0195 per U(1), D2167 PER);
  D4 (reported, not filtered) hidden gauge groups U(N_i) for the dark-photon / SIDM step; tree split R and the visible content.
Reading fixed now: hits passing D1-D3 = "hole = dark sector" candidates -> next lock: their N=2 Delta b (tori 2, 3) for alpha_s and the SIDM
and wino checks. Zero hits with tadpole closed -> the hole cannot be filled by <= 3 hidden stacks of N <= 6 at rho = 3/2. Hits that close
the tadpole but fail D1-D3 are reported with the failing test. Cap 30 min (PARTIAL if hit). Referee after; DEVIATIONS before any fix; one rerun.
