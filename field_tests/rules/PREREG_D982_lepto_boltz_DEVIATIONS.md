# DEVIATIONS for PREREG_D982 (written before the rerun)
D1 (crash, 16 Nov 19:16 CT): the run was killed by the container's memory limit (exit 137, OOM: python3 at 6.0 GB) after 22 of the locked rows; no results file was written. Cause: solve_ivp kept every solver step of each stiff integration in memory (dense output arrays), and the arrays accumulated.
Disclosure: the partial log (tools/calcq/logs/D982-leptoboltz.log) was seen before this file: sanity line and the completed rows all show kappa = 0.9391.
Fix: pass t_eval=[x_end] to solve_ivp so only the end point is stored. Physics, equations, inputs, tolerances, verdict rules unchanged. One rerun (D982b). The verdict is read only from the rerun's results file.
D2 (infrastructure, 16 Nov ~19:45 CT): the D982b rerun was killed with the cloud queue runner (session background time limit) before writing its results file; same disclosure as D1 (all logged rows κ = 0.9391). No change; one more full rerun (D982c) under the restarted runner.
