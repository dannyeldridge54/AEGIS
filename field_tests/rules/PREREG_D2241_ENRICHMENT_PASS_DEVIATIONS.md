# D2241 DEVIATIONS (written before rerun, 2026-11-23)
DEV-1 (BLOCKER, found in run 1): the main pass never moved eta off 3. Cause: for a no-burn state the breathing score is
-(c0/0.05)-10 where c0 is the divertor seeding from the FIRST iteration, computed before the core-argon floor c/eta
is applied, so the score is blind to eta and a step to eta=5/10 is never a strict improvement. Run-1 main = control
(uninformative), recorded as such.
Fix: run the breathing optimiser three times with eta FIXED at 3, 5 and 10 (eta removed from the ladder), same starts,
classes and other ladders. This is exactly the pre-registered report "smallest eta that works per start". Verdict
rules unchanged. One rerun.
