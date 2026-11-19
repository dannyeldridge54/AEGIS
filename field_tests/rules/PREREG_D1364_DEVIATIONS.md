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

## D3 (2026-11-18 18:51 CT, execution only)
Danny: "Run it through the pc loop". The same locked bundle (tools/serapis_calc, tools/janus_calc, scripts/d1364; tgz md5 871eb825)
was queued on the PC runner (job D1364MIX). First attempt failed at import (the run script called system python3 without
numpy/scipy; no computation happened). Resubmitted as D1364MIX2 with the runner's aegis env python (PYBIN). The cloud parallel run
continues as an identical-code cross-check. Model, w list, C, T_R, λ, gate, band and rule unchanged.
