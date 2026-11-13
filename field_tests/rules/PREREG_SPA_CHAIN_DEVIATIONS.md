# SPA-CHAIN deviations (PREREG_SPA_CHAIN.md locked and unchanged)
## D1 (13 Nov 14:42) — start-up crash, no sampling done
Both chains stopped at start-up: the shared config builder sets force: True and the script added resume: True, which Cobaya refuses.
Fix: drop "force" so the chains can resume across restarts. Code-only; likelihoods, priors and the stopping rule unchanged.
