# Improved compute route (17 Nov 2026)
1. Every batch job uses tools/calcq/sweep.py: resumable part file, one process per task, per-task wall limit (default 20 min), errors/timeouts recorded,
   never silently retried (test: tools/calcq/test_sweep.py PASS). No more DEVIATIONS notes for stuck single cases.
2. tools/calcq/pcjob.py packages a LOCKED job in one step (checks lock hash, committed and pushed) → .tgz + .job for the PC runner.
3. PC runner v2 (tools/calcq/pc_runner2.sh → Desktop\AEGIS_PCJOBS\pc_runner2.sh): 2–3 jobs at once, per-job wall limit, auto-unpack, status/heartbeat.
   Takes over when AEGIS_PC_RUNNER.bat is next started (bat now points to v2); v1 keeps running until then.
4. External references for the next validations (researched): multi-field — MultiModeCode (arXiv 1410.0685, exact multi-field MS) and PyTransport
   (arXiv 1609.00381, transport method incl. bispectrum) → validate Janus twofield δN (n_s, r, f_NL) against them like ASPIC for single field;
   task-runner prior art: pytaskfarmer, executorlib (comparison page), scitq — our sweep.py covers the needed subset with no new dependency.
5. Next: install ASPIC in WSL on the PC (so full Janus-vs-ASPIC pulses run there); pin one requirements file for cloud + PC with a start-up self-test.
