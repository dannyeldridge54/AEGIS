
## DEV (2026-11-22 20:41 CT). W Pantheon+ crashed before producing any fit result
- **What happened:** Cobaya's minimiser drew u_i = 0.26 from the reference range uniform(0.02, 0.3). That start is past the thread's collapse edge (u_i ≈ 0.22, the referee's RD-2 warning), so the log-likelihood was −inf and the run stopped with "Cannot reproduce log minimum".
- **Fix:** the reference range becomes uniform(0.02, 0.20), inside the physical region. The prior (1e-6, 0.6) is unchanged, so the fit can still explore the whole space. Nothing else changes.
- **Rerun:** W Pantheon+ once. W Union3 has not started yet; it picks up the fixed script.
- **Dovekie:** W converged with u_i → 0.0016, so its start was unaffected.
