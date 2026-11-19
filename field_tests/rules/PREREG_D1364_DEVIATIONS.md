# PREREG D1364 — DEVIATIONS (written before any rerun)

## D1 (2026-11-18, before rerun)
The first run (started ~00:15 UTC) crashed after computing w = 1: `json.dumps(row)` raised
"Object of type bool is not JSON serializable" because `in_band` was a numpy bool. No row was printed or saved, so NO result
was seen. Fix: wrap `in_band` in `bool(...)` and cast n_s, r, α_s, N* to float. Nothing else changes (same model, w list, C, T_R,
λ, gate, band and rule). This is a crash fix, not a rerun to chase a result.

## D2 (2026-11-18 18:38 CT, before restarting)
The D1 rerun was killed by a container restart before printing any row (no result seen). Restart change, execution only:
the script accepts an optional w on the command line and writes one row file per w (field_tests/results/D1364_rows/w_<w>.json);
the five w run as five parallel processes; a final merge writes D1364_p3_mix.json in the original format. Model, w list, C, T_R,
λ, gate, band and rule unchanged.
