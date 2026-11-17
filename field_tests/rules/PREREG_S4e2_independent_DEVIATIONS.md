# S4e2 DEVIATIONS
D1 (2026-11-17 ~19:12Z, no S4e2 number exists — the cloud run hit my 3400 s shell limit before writing any output): one rerun of the unchanged script on
Danny's PC (runner, 2 h limit). If it times out again, S4e2 is recorded NOT RUN (compute-limited) and the 6D Prüfer step gets its own lock.
D2 (2026-11-17 19:43Z, still no S4e2 number): the PC run of D1 died at import — the PC's WSL python has no sympy. Install sympy there
(pip --user) and run the unchanged script once more on the PC. Environment fix only; D1's rule (one timeout → NOT RUN) still applies.
