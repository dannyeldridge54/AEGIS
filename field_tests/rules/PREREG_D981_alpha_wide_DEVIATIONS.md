# DEVIATIONS for PREREG_D981 (written before the rerun)
D1 (infrastructure, 16 Nov ~19:45 CT): the cloud queue runner reached the session's background-process time limit and was stopped; its child job (this run) was killed after 7 of 8 locked runs (only Chronos grid M remained). No results file was written.
Disclosure: the partial log was visible: SERAPIS-E W bd 200/1000/5000 = −9.8689/−9.8793/−9.8782e-4, M = −9.8688e-4; Chronos W = −9.9467/−9.9406/−9.9405e-4.
Fix: none to the method or script; the full locked script is rerun once (D981b) under a runner restarted with the maximum background time (2 h). The verdict is read only from the rerun's results file.
