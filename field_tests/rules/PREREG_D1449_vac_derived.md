# PREREG D1449 — vacuum discriminant with both derived second-order α_s models

Locked 2026-11-19 (UTC) before computing (JANUS tick 45, node vac_discriminant, status killed since D1425).
Models (both derived, second-order SR): ρ = D1442 offset model (script d1442/second_order.py, solve (C_r, y*)); τ = i = D1448 exact
plateau (script d1448/tau_i_exact.py, solve (ε, I*)). dps 30.
Grid: n_s ∈ {0.9725, 0.9740, 0.9755} × r ∈ {4.6, 4.75, 4.9}e-4 (overlap region of the audited points). At each grid point solve each
model to (n_s, r) and compute Δα_s = α_ρ − α_τ=i.
Survey σ(α_s), 1σ, 2212.04115 via D1409: SO 3.3e-3 (funded, operating); 8.5e-4 best combination includes S4 ⇒ hypothetical (D1440).
Rule: vac_discriminant stays KILLED unless max |Δα_s|/σ_SO ≥ 3; also report |Δα_s|/8.5e-4 (hypothetical) and the ratio
|Δα_s| / (model accuracy 0.14 % × |α_s|) to show whether the models resolve the vacua from each other at all.
Grid points where a solve fails to converge are reported as such (no reruns). Fixes only via PREREG_D1449_DEVIATIONS.md first.
