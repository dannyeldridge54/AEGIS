# PREREG J9 — running of the running β_s: Janus (spectra3, third order) vs the exact Mukhanov–Sasaki spectrum
Locked 2026-11-17 before any J9 number. Models: J7b indices 1, 4, 13 (built by j7b_wide.build), N* = 50, 60.
Exact β_s = d³ln P_R/d(ln k)³ at the pivot from a degree-5 polynomial fit of ln P_R (ms.spectra_fast, bd = 1000, new
return_lp option — no numerical change) on 15 points over ln(k/k*) ∈ [−1.5, 1.5] ("A"). Reference check "B": 11 points on [−1, 1],
degree 5. A point is INFORMATIVE if |β_A − β_B| ≤ 0.2 |β_A|.
Claims: C1 at least 4 of 6 points informative; C2 at every informative point |β_Janus − β_A| ≤ 0.1 |β_A| (β_s is ~ε³, so 10% is
the honest accuracy target). C1 fail → J9 UNINFORMATIVE (reference too noisy), recorded as is. C2 fail → Janus β_s NOT VALIDATED.
Results: field_tests/results/janus_j9_beta_s.txt.
