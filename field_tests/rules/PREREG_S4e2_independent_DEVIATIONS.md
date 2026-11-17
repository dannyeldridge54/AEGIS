# S4e2 DEVIATIONS
D1 (2026-11-17 ~19:12Z, no S4e2 number exists — the cloud run hit my 3400 s shell limit before writing any output): one rerun of the unchanged script on
Danny's PC (runner, 2 h limit). If it times out again, S4e2 is recorded NOT RUN (compute-limited) and the 6D Prüfer step gets its own lock.
D2 (2026-11-17 19:43Z, still no S4e2 number): the PC run of D1 died at import — the PC's WSL python has no sympy. Install sympy there
(pip --user) and run the unchanged script once more on the PC. Environment fix only; D1's rule (one timeout → NOT RUN) still applies.
D3 (2026-11-17 21:21Z): D3 (2026-11-17 21:20Z, still no S4e2 number): the v1 PC runner had no time limit, so the D2 run went past D1's 2-h limit (13:45-15:20 CT, no output) and was stopped when the runner window was closed to restart the queue. The restarted v2 runner picked the job up again with a real 2-h limit (until ~17:20 CT). Per D1 the overrun counts as the one timeout already; this restarted run is reported as a separate, labelled attempt: if it finishes inside 2 h its numbers are recorded as 'S4e2 (attempt after D3)', otherwise S4e2 is NOT RUN (compute-limited) and the 6D Pruefer step gets its own lock.
