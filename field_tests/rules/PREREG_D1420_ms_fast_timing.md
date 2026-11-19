# PREREG D1420 — one timed exact-MS evaluation (ms.spectra_fast) of the ρ offset model at D1415's first-order point

Locked 2026-11-19 (UTC) before computing (JANUS tick 17). Purpose: timing + a first exact look; NO solve, no verdict on the model.
Model as D1415/D1418 (E₁ = 2ζ(4)y² + B + πζ(3)/y, B = −4.7833; V = (1 − 1/E₁)(1 + C(E₁ − 1))), C = 1.255e-6, y* = 14.818, start φ* + 0.3,
engine apps/aegis_studio/engine/tools/serapis_calc/ms.py Background + spectra_fast (unchanged), Nstar = N_end − N(φ*).
Report: n_s, r, α_s, seconds, and the gaps to D1415's first-order (n_s, r) = A1's (0.974393, 4.82095e-4) — i.e. how far exact MS moves
the observables at this point. Cap 150 s. Outcome labels: "fast (< 20 s)" → a Newton solve may be locked next tick; "slow"; "no result".
ms.py says spectra_fast is to be used only under a lock written for it — this is that lock.
No reruns to chase results; fixes only via PREREG_D1420_DEVIATIONS.md written first.
