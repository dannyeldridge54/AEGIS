# EVIDENCE-COMPRESSED deviations (written before any rerun)

D1 (13 Nov 2026, before rerun). The first run crashed at its first checkpoint save (pickle cannot store the local
likelihood function `run.<locals>.ll`); no evidence value was produced or seen. Fix: run without the checkpoint
file. Sampler settings (nlive 300, rwalk, dlogz 0.1, seed 1), priors, data and the scoring rule are unchanged.
Only cost: a killed run restarts from zero instead of resuming.
