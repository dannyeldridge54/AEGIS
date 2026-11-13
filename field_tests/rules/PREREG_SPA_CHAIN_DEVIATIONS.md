# SPA-CHAIN deviations (PREREG_SPA_CHAIN.md locked and unchanged)
## D1 (13 Nov 14:42) — start-up crash, no sampling done
Both chains stopped at start-up: the shared config builder sets force: True and the script added resume: True, which Cobaya refuses.
Fix: drop "force" so the chains can resume across restarts. Code-only; likelihoods, priors and the stopping rule unchanged.
D1 add (14:45): the key alone was not enough (force is also set at call level); now force=False and resume=True are passed to run() directly. Still no sampling done.
## D2 (13 Nov 16:55) — chains stuck at "Getting initial point" for 2 h; LCDM segfaulted at 16:31; still no sampling done
Diagnosis (field_tests/spa_chain/diag_spa.py, PC, results/spa_diag.txt): the LCDM posterior at the NS-SPA best-fit start point is finite
(logpost −1169.8, one evaluation 24 s, 3 GB). The start-point code only re-centred parameters that already had a "ref" entry; sampled
parameters without one were drawn from their full priors, which makes most candidate starts fail (up to max_tries = 100000 × ~24 s), and a
far-out draw is the likely cause of the segfault. Fix: re-centre EVERY sampled parameter present in the best-fit file (scale = its existing
ref scale, else 10⁻³·max(|value|, 10⁻³)), and max_tries 1000. Also the job log printed "exit 0" for every chain because $? was read after
$(date) — logging only; fixed to capture the exit code first. Code-only; likelihoods, priors, data and the stopping rule are unchanged; the
chains are estimation-only and have produced no samples, so nothing is being re-run to chase a result.
