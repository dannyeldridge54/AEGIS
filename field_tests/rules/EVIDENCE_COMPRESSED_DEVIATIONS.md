# EVIDENCE-COMPRESSED deviations (written before any rerun)

D1 (13 Nov 2026, before rerun). The first run crashed at its first checkpoint save (pickle cannot store the local
likelihood function `run.<locals>.ll`); no evidence value was produced or seen. Fix: run without the checkpoint
file. Sampler settings (nlive 300, rwalk, dlogz 0.1, seed 1), priors, data and the scoring rule are unchanged.
Only cost: a killed run restarts from zero instead of resuming.

D2 (13 Nov 2026 ~11:00, before rerun). The D1 rerun was stopped by the cloud's 2-hour background limit before LCDM finished;
no evidence value was produced or seen. Without a checkpoint each model restarts from zero, so the run can never finish here.
Fix: make the likelihood and prior transform module-level (picklable), restore the checkpoint file
(evidence/<M>.save, every 10 min) and resume with NestedSampler.restore in successive runs. Sampler settings (nlive 300, rwalk,
dlogz 0.1, seed 1 for a fresh start), priors, data and scoring unchanged. A resumed run continues the same sampler state.

## D3 (13 Nov 13:52) — stopped by choice, no result read
Stopped on Danny's instruction to drop runs not needed for the best current theory. The LCDM evidence run had not finished (only
evidence/LCDM.save exists); no evidence value was computed or read. The full-likelihood NS-SPA comparison (D157/D158) now
supersedes the compressed comparison for model choice. The run can resume from the checkpoint if wanted; nothing is scored.
