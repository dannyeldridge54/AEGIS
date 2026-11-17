# DEVIATIONS R2c stage a — written after the run, before adding anything (2026-11-17)
D1: the lock said to include the closed side (v < v_th) if its Maxwell weight is > 1e-4. The weight is 0.8–2.6e-4 (above 1e-4 in 5 of 6 cases), but the script omitted the closed side. That is a script error against the lock.
- The open-side numbers stand as computed. They are now labelled "open-side part, normalised over [1.001 v_th, 2]".
- Fix, done exactly as the lock intends: add the closed-side contribution, with the normalisation over the full Maxwell weight:
  - R₀₀ = [∫_{open} S w + ∫_{closed} S w] / (2∫_0^∞ w).
  - Closed side: sommerfeld_nlo.wino_s_nlo(nlo=False), on a uniform v grid of 200 and 400 points over [1e-3 v_th, 0.999 v_th]. Converged iff the two agree within 1%.
  - The Rydberg tower in x ∈ [0.999, 1) is not resolved. Its weight is < band weight/100 ~ 1e-6, which is stated as a bound.
- The open-side grid S values are recomputed (the same deterministic calls, 40/80 points). No change to any parameter.
