# PREREG D1456 — predicted α_s window per vacuum once SO measures n_s to ±0.002

Locked 2026-11-19 (UTC) before computing (JANUS tick 52, node janus).
Chains (exact rows on file): ρ — the tilt line C 1.0/1.15/1.3e-6 at T_R 5.455e8 (a1_mssm_gstar.txt MSSM rows: n_s 0.971663/0.973232/0.974828,
r 4.52911/4.70877/4.89722e-4); τ = i — NA12 ε line (n_s 0.97368…0.97556, r 4.6846…4.9878e-4).
Method: linear fit r(n_s) per chain (report slope, max residual); centres A1 n_s 0.974393 (ρ) and NA12 ε 1.40e-4 n_s 0.97462 (τ = i);
evaluate n_s = centre − 0.002, centre, centre + 0.002 (SO 1σ, 1907.08284), r from the fit (mild extrapolation beyond the rows, stated),
α_s from each vacuum's derived second-order model (d1449/vac_grid.py solve, dps 30).
Report: α_s window per vacuum = [α(centre−0.002), α(centre+0.002)], its width relative to |α_s(centre)|, and whether the two
vacua's windows overlap. No pass/fail (forecast characterisation); verdict text: "windows overlap" or "windows separate".
No reruns; fixes only via PREREG_D1456_DEVIATIONS.md first.
