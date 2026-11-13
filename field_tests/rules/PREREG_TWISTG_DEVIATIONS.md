# PREREG_TWISTG deviations (append-only)
## D1 (13 Nov 17:55, after running the locked grid, before any eligible data)
The locked grid (γ ≥ 0) was run as written (results/twistg_scan.txt): n_s FALLS with γ (0.9642 → 0.9315 at γ = 0.02, N* = 55.7) — the
opposite of the intended effect. Cause: a sign error in translating arXiv:2606.24131's u^{−δ√α} (their u → 0 on the plateau at φ → +∞)
into the Twist's variable (the Twist's u = T + T̄ → 0 on the plateau at φ → −∞): the literature factor corresponds to γ = −δ/2 < 0, not +δ/2.
The γ ≥ 0 results stand as recorded (that branch of TWIST-G lowers n_s and is disfavoured by any n_s above 0.965). The γ < 0 branch is a
DIFFERENT locked model, PREREG_TWISTGN, locked before it is computed. Also: the "TCC VIOLATED" flag at γ = 0 is a finite-x artefact — at
x = 89 the g-term gives slope √(2/3)·u/(2 + u) = 0.807; the TCC bound is asymptotic (u → ∞), where the γ = 0 slope → √(2/3).
