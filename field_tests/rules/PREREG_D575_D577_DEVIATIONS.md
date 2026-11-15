# Deviations for D575 and D577 (written BEFORE any rerun)

D1 (bug in the added "inflation broken" check):
- infl() tests eps(u) ≥ 1 at every integration step, including the first. At the first step u = u_end, where eps = 1 by construction (brentq root), so rounding can trip the check.
- Evidence:
  - D575 ε = 1e-3 reports "broken at y = 2.8", which equals y_end = 2.77.
  - D577 κ = 1e-3, Ñ₀ = 25 and κ = 0.1, Ñ₀ = 25 report "no viable inflation", while κ = 1e-2 (in between) works. That is non-monotonic, so a numerical artifact is suspected.
- Fix: apply the check only after the first step, and only when eps(u) > 1 + 1e-6. No other change.

D2 (D575 ε = 3e-3 gives nonsense, y* = 1.2e6 and n_s < 0):
- The end-of-inflation search found a crossing; then the N-integration ran to the u = 14 cap without reaching N*.
- Fix: if the cap is hit, report "N* not reached (no viable inflation)" instead of numbers.

Rerun: both scripts, once each, with D1 and D2 applied. The reruns replace the affected rows only. All other rows must reproduce unchanged; this is checked and reported.
