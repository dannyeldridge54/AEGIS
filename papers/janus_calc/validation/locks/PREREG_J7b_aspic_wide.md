<!-- AEGIS-FP PPAB7LSKSM7R3APG · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# PREREG J7b — Janus vs ASPIC widened to 17 models, with a resolved α_s reference

Locked 2026-11-17 before any J7b number. Same codes, pivot definition and claims as PREREG_J7a (ASPIC @75400d2,
driver theory/janus/aspic/j7b_aspic.f90 using each model's endinf / x_trajectory / epsilon_one..three and srflow).

## Points: J7a's 7 models + 10 new, each at N* = 50 and 60 (34 points)
New (ASPIC x convention → Janus field y rolling to smaller y):
MHI μ = 10 (V = 1 − sech(φ/μ)); KMII α = 2 (1 − αx e^{−x}); RGI α = 1 (x²/(α + x²)); DWI φ0 = 25 ((x²−1)², x = φ/φ0, y = φ0(1 − x));
SFI p = 2, μ = 20 (1 − (φ/μ)^p, y = μ − φ); LI α = 0.3 (1 + α ln x); ESI q = √2; NI f = 7; LFI p = 3; LFI p = 1.
Janus start: y0 stepped outward from ASPIC's x*(60) until Janus's background has ≥ 75 e-folds.

## α_s reference (fixes the J7a problem: 5 k-points over ±0.1 with bd = 200 gave α_s noise ~1e-3)
ms.spectra_fast with dlnk = 9 points uniformly on [−1, 1] (least-squares quartic, α_s = 2c₂) and bd = 1000.
Reference convergence check R0 (before scoring α_s): on LFI p = 2 and SI at N* = 60, the same with dlnk on
[−0.5, 0.5] and bd = 2000 must agree to |Δα_s| ≤ 2e-5. If R0 fails, C3 is reported UNRESOLVED (not scored).
n_s, r reference: same runs (pivot dlnk = 0 kept in the grid).

## Claims (as J7a): C1 n_s median ≥10× better and max better; C2 r median ≥3× better; C3 α_s median better (only if R0
passes); C4 Janus median time ≤ 100 ms. "JANUS MORE ACCURATE" iff C1, C2 TRUE and C3 TRUE or UNRESOLVED (stated).
Any model where ASPIC or Janus fails to produce a number is listed as such, not dropped.
