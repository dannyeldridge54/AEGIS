# PREREG D1937 — central-equation knob engine and targeting (locked 21 Nov 2026 before running; repo at 7a274cf0)
Engine: tools/weave_knobs.py. Knobs: K_S = g_s; K_T = (σ_vis, 𝒱, A), with N = 6; K_U = |u| (decoupled from these observables, I_TU = 0 in the current chain).
1. **Jacobian.** d ln O/d ln K, using central differences at steps of 2, 5 and 10 % (the three vectors). The centre is the median; the floor is max − min.
2. **Targeting.** Find the knob setting closest to α_s = 0.1180 ± 0.0009 with the wino at least 660 GeV. The search is a bisection on σ_vis to 1e-12.
   - BALANCED if the best |pull| is ≤ 2. Otherwise the verdict is "no knob setting balances", and the residual Δα_s sizes the missing S–T seam term.
