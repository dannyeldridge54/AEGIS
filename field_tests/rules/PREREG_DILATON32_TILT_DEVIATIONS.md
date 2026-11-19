# PREREG DILATON32_TILT — DEVIATIONS (written before any rerun)

## D1 (2026-11-19 04:42 CT): withdrawn as a duplicate — no rerun
The five cloud runs crashed at start (C = None) before any result: run.py's run-name parser had been changed (commit 890fd792,
PREREG DILATON32_CSCAN, locked 04:24 CT by the parallel helper session) to accept 'C<value>' runs, and this lock's 'AT<value>' names
no longer parse. DILATON32_CSCAN is the SAME scan (form A, C ∈ {1.5, 2, 2.5, 3, 4}e-6), locked two minutes earlier, so this lock is
withdrawn in its favour; its runs are the record. The helper's independent SR band map (D1481) forecasts: n_s enters the band at
C ≈ 1.78–3.46e-6 with r = 6.6–7.7e-4 > 5.7e-4 ⇒ not in band at any tested C.
