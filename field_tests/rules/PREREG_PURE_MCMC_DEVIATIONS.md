# PREREG_PURE_MCMC deviations

D1 (2026-11-13 06:12 CT, written before resuming; no result read). Both chains stopped at the first 500-step
checkpoint: the status file write failed (numpy int64 not JSON-serialisable). Fix: cast to int/float. Code-only;
sampler, priors, likelihood and readings unchanged. The chains RESUME from their saved HDF5 state (the 500 steps
already taken are kept), so this is a continuation, not a rerun.
