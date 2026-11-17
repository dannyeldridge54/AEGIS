# PREREG J9b — sharper β_s test (D1039 was reference-limited at ~5%): denser exact-MS reference over all J7b models — PC job
Locked 2026-11-17 before any J9b number. Models: all 16 J7b models (indices 1–17 except 9, built by j7b_wide.build), N* = 50, 60 (32 points).
Exact β_s = 6·c₃ of a degree-7 polynomial fit to ln P_R (ms.spectra_fast, bd = 1000, return_lp): A = 41 points on ln(k/k*) ∈ [−1.5, 1.5], B = 31 points on [−1, 1].
INFORMATIVE if |β_A − β_B| ≤ 0.05|β_A| (sharper than J9's 20%). Claims: C1 ≥ 20 of 32 informative; C2 at informative points median |β_Janus/β_A − 1| ≤ 5%
and max ≤ 15% → VALIDATED at the reference's precision (report the median reference spread). C1 fail → UNINFORMATIVE. Runs on Danny's PC (device VM),
code copied unchanged from the cloud repo at the lock commit. Results: field_tests/results/janus_j9b_beta_s.txt (copied back).
