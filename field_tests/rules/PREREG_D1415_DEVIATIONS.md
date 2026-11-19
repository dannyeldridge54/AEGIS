# PREREG D1415 — DEVIATIONS (written before the rerun; no result was seen — the first run crashed before printing)
D1. Crash: json cannot serialise numpy.bool_ (D_check_pass). Fix: cast to Python bool. No method change.
D2. fsolve warned "not making good progress" on one of the three solves. Fix: report each solve's residual
    (|Δn_s|, |Δr|/r) in the output; a solve with residual > 1e-8 (n_s) or > 1e-6 (relative r) is marked UNCONVERGED and
    the verdict for that case becomes "no result" (not PASS/FAIL). No change to the model, inputs, starting point or rule.
