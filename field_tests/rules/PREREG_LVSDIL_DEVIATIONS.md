# PREREG LVSDIL — DEVIATIONS (written before any rerun)

## D1 (2026-11-19 04:38 CT)
All four PC runs (LVS1–4) crashed at the spline build ("y must contain only finite values") before any result: at large Im τ,
F(E) = E^{1/3}exp(−kE^{2/3}) underflows to 0 (E^{2/3} up to ~2.6e3 on the grid), so e = F(E_ρ)/F(E) − 1 = ∞. Fix: compute e in log
space, e = expm1(min(Δ, 700)), Δ = log F(E_ρ) − log F(E). Where Δ > 700 the plateau differs from 1 by < e^{−700} — no effect on any
observable. Model, k values, start rule, band and rule unchanged.
