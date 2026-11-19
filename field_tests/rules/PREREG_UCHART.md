# PREREG UCHART — universal (k, C) chart: where is the SERAPIS band for ANY plateau, as a function of approach exponent k and tilt C?

Locked 2026-11-19 (08:35 CT) before computing. Danny 08:24 "restart and do the calculations better" (after the review: every P3 route
reduces to two numbers — how fast the plateau approaches 1, and the tilt).
Family (pipeline path Re τ = ½, n = 1, φ = ln y/√2, λ = 1, T_R = 8.94e8): E_paper → y^k (pure power), so e = y^k − (√3/2)^k and
V = e/(e+1)·(1 + C·e) (the pipeline's own native tilt). 1 − V ∝ y^{−k} = exp(−√2 k φ): k = 2 is the SERAPIS-E leading term, k = 1.5 the
single-power E(τ,3/2) (form A), k = 3 the α′³ square (form B).
Grid: k ∈ {1.25, 1.5, 1.75, 1.9, 2.0, 2.25, 2.5, 3.0} × C ∈ {0, 0.5, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0}e-6 (64 points).
Start point: DILATON32 D1 bisection (N_end ∈ [100, 200]).
Engine F (fast, all 64): janus_calc.core third-order flow (spectra3) with self-consistent N* (pipeline.nstar), as in predict_fast stage 1.
Engine X (exact MS, pipeline.predict) at 4 check points: (2.0, 1.25e-6), (1.5, 0), (1.75, 1.5e-6), (2.5, 2.0e-6).
Rule E (engine): chart is valid at engine-F level if all 4 checks have |Δn_s| ≤ 5e-4 and |Δr|/r ≤ 3 %; else the chart may only be
quoted with the measured F→X offsets applied, stated as such.
Rule R (reduction, does "two numbers" hold?): compare chart (k = 2, C = 1.25e-6) with exact SERAPIS-E (real E(τ,2), same C, T_R), and
chart (k = 1.5, C = 0 / 1.25e-6) with exact DILATON32 A0 / A1 (field_tests/results/DILATON32). "Reduction holds" if |Δn_s| ≤ 0.002 and
|Δr|/r ≤ 15 %; else the subleading (non-power) terms matter and each route also needs its own k_eff(φ*) — report the size.
Output: n_s, r, α_s, N* per point; in band / near (PREREG_SMSCAN); the in-band region in (k, C) by linear interpolation on the grid;
field_tests/results/UCHART/. Expectation stated now: band at k ≈ 1.8–2.1, C ≈ 1–2e-6 (from D1490/D1495/D1513).
No reruns to chase results; fixes only via PREREG_UCHART_DEVIATIONS.md written first.
