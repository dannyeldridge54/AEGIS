<!-- AEGIS-FP 6W7UZA3WEU26LZHK · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# PREREG J7d — Janus vs ASPIC on two-parameter models (fixed N*), same method and claims as PREREG_J7b
Locked 2026-11-17 before any J7d number. ASPIC @75400d2, srflow second order at foo_x_trajectory(−N*, x_end, params).
Reference: exact MS, J7b settings (9 k-points on [−1, 1], bd = 1000; R0 passed in J7b). Janus: core.spectra3.
Models (ASPIC x convention → Janus field y rolling to smaller y):
- TI α = 0.1, μ = 10 and α = 0.2, μ = 8: V = 1 + cos x + α sin²x, x = φ/μ, y = μ(π − x) (top at y = μπ).
- PSNI α = 1e-3, f = 5: V = 1 + α ln|cos(x)|, x = φ/f (ASPIC's x), y = f(π/2 − x)… if ASPIC's convention differs,
  the point is listed as "convention not matched" and not scored.
- SFI p = 4, μ = 15 and p = 2, μ = 10: V = 1 − x^p, x = φ/μ, y = μ(1 − x).
N* = 50, 60 (10 points). Claims C1–C4 and verdict rule exactly as PREREG_J7b. Any model where ASPIC or Janus gives no
number (no end of inflation, slow-roll violation) is listed, not dropped.
