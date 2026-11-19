# PREREG D1510 — tilt plan T3e: fine grid of the physical-frame DILMIX sliver

Locked 2026-11-19 ~14:07 UTC before computing. Model and method exactly as D1509 (physical frame λ = 1/9930.9, V = P(1 + C g), fast SR, T_R 8.94e8).
Grid: α ∈ {0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2} (7) × C ∈ {1.3, 1.4, …, 2.0}e-6 (8) = 56 points.
Output: in-band set (n_s 0.969–0.975, r 4.55–5.7e-4); if non-empty, the best-centred point (closest to n_s 0.972 with r in band) becomes the exact-MS spot check (T3f).
Rule: "sliver confirmed" if ≥ 1 grid point in band; else "sliver killed — DILMIX has no physical-frame in-band region at this grid resolution".
Fixes only via PREREG_D1510_DEVIATIONS.md first. No reruns to chase.
