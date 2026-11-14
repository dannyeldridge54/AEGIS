# PREREG D406 — first centre (balance) check: pinning dilution (right ladder) vs N* and n_s (left ladder)
(locked 16:05 CT 14 Nov 2026, before running; Danny: "Yes … how would you set it" — two-ladder process)

Script: theory/twist2/balance_nstar_dilution_d406.py. Cross-effect: an entropy release D after reheating lowers N* by (1/3) ln D (standard
matching: a_end/a_0 falls by D^{-1/3}). Inputs: D from the locked D396 chain at the robust capture point x_E = 29.598, λ ∈ {0.004, 0.01, 0.033},
v ∈ {10⁹, 10¹⁰, 3×10¹⁰, 10¹¹} GeV; N* = 57.2 before dilution (D391); n_s from the Twist table (D403).
Centre rule: a (λ, v) point is BALANCED if it passes the right ladder (trapped, T_d ≥ 5 MeV, D ≤ 10³) AND costs the left ladder at most
0.5 e-fold of N* (|ΔN*| ≤ 0.5, i.e. D ≤ e^{1.5} ≈ 4.5). Report the balanced set, or "NO BALANCE" if empty (then the dilution must be reduced
by other means, or the left ladder must absorb the cost and the n_s distance is restated).
No reruns; fixes via a DEVIATIONS file written first.
