# MATTER deviations (logged before the run)
- **D1 (12 Nov 2026, before any number):** the code (`theory/matter/boltzmann_leptogenesis.py`) was written before the
  lock (the rule said "after"); it is unchanged by the lock. It integrates from T_RH down to 10¹¹ GeV, not to the
  electroweak scale, using the single equilibrium coefficient μ_ℓ/μ_A = 0.5227 (the set valid above 10¹² GeV) instead of
  recomputing it in each lower band. Below ~10¹² GeV the Weinberg rate is far below the expansion rate, so the
  asymmetry is already frozen; the readings are taken as computed and this simplification is reported with them.
- **D2 (12 Nov 2026, 18:2x CT):** the first run computed all rows but crashed when saving (a numpy boolean in
  K_KIN_flag is not JSON-serialisable). Fix: wrap it in bool(). No input, rate or reading changed; rerun once.

## D-refit (13 Nov 12:30): matter_refit_check.py killed by the session's 30-min background limit before printing
The D124 confirmation run (locked 11:55, prediction 0.6–1.6× at m_σ = 5.8×10¹⁰) was stopped by the tool's background time limit,
not by the code, and wrote no result. Rerun unchanged with a 2-hour limit, followed by D129 (matter_d127_form.py, also unchanged).
No result had been seen, so this is not a rerun to chase a result.

## D-PC (13 Nov 14:07): the four locked matter checks moved to Danny's PC — no result had been produced or read
At m_σ = 5.8×10¹⁰ GeV the hidden field oscillates ~10× faster than at 6×10⁹, so each run needs several hours; the cloud session kills
background jobs at 2 hours (the refit was already killed once). The refit (D124), new-form (D129), TWIST-K (D160) and yield-sensitivity
(D137) checks were stopped here without output and started in parallel on the PC runner (field_tests/matter_pc/run_matter_pc.sh,
14:05:47). Scripts are unchanged except that absolute paths became paths relative to the script; predictions and readings unchanged.
