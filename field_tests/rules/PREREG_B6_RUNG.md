# PREREG B6 — which up-quark rung do the quark data prefer, and does the preference survive narrower couplings? (D1757 item 2)
Locked BEFORE computing. Model w864 (weight 8/6/4, as PREREG_Q12), down quarks on rung 1, up quarks on rung u ∈ {2,…,10}; τ_u from the computed minima where available (1, 8, 9, 10, 13) else the ladder formula at arg 50° (label E), exactly as weave_sweep._tau_for.
Targets and tolerances: identical to PREREG_Q8/Q12 (×/÷ TOL: masses 1.5, V_us 1.1, V_cb 1.2, V_ub 1.3, J 1.5); score = Σ (ln(o/T)/ln TOL)².
Two coupling boxes (12 parameters: r1, r2, |g|, arg g, |f|, arg f for each sector):
- BOX-3: moduli in [1/3, 3] (the Q8/Q12 box, CubeMind's box);
- BOX-2: moduli in [1/2, 2] (closer to equal coefficients).
Procedure per (u, box): start from 400 random points (seed = 100·u + box), keep the best 5, Nelder–Mead polish each (maxiter 4000) with clipping to the box; report the best score, its fails, and the 8 observables. One run, no reruns.
Equal-coefficient check (no fit): g_u/g_d = (1 + 1/16)/(u + 1/16) vs data 0.1276 ± 0.0060 (D1741).
Readings decided now:
- "CKM prefers low rungs" CONFIRMED if, in BOX-3, the best passing (0 fails) rung is < 8 and rung 8 has ≥ 1 fail.
- "Preference survives narrower couplings" if the same holds in BOX-2.
- Joint verdict: a rung is JOINTLY VIABLE if it has 0 fails in BOX-2 AND its equal-coefficient g_u/g_d is within 3σ of data. If no rung is jointly viable ⇒ the ladder's quark placement is in tension (mass-ratio scaling and mixing pick different rungs) — recorded as such.
Caveat stated in advance: 12 parameters vs 8 observables — a pass is consistency, never evidence.
Code: theory/quarks/b6_rung.py.
