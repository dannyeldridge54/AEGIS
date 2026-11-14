# PREREG D387 — the Twist's N* on the full TWIST-I/D367 trajectory (locked before running)

Locked 11:10 CT 14 Nov 2026, before any run. Script: theory/review/nstar_traj_d387.py (a copy of the locked
omegakin_d367.py with two changes only: it stores rho_end = 3H² at the end of inflation, and it prints
dN* = ¼ ln(rho_end/rho(N)) − (N − N_e) with Ω_rad at each half e-fold, stopping at N − N_e = 9). Same parameters as D367
(m_σ 5.8×10¹⁰ GeV, y 0.1, f_rh 0.008). The formula is the one of kination_Nstar.py (Development 84).

Statistic: dN*_traj = the printed value at N − N_e = 9.0. Convergence check: |value(9.0) − value(8.0)| < 0.02, else report
"NOT CONVERGED" (and Ω_rad at 9.0).
N*_traj = 55.70 + dN*_traj (55.70 = instant-reheating N*, kination_Nstar.txt). n_s by linear interpolation in that table:
n_s = 0.9642 + 0.00058 (N*_traj − 55.70).

Reading (reported, no pass/fail on the theory):
- Compare with kination_Nstar's value at the nearest heat share (+1.66 at 0.4%); report the difference.
- N*_traj ≥ 58: "reaches the refined-Starobinsky ACT 2σ region (arXiv:2504.20757)"; else "below it".
- N*_traj vs the CMB-SPA+DESI 68% lower edge 64.5 (arXiv:2609.19296, D385): report the shortfall.
Cross-sector: the matter (n_B/s) and DM yields are NOT re-derived here; the CMB-scale k is unchanged (same inflation).
No reruns to chase a value; fixes only via PREREG_D387_NSTAR_TRAJ_DEVIATIONS.md written before rerunning.
