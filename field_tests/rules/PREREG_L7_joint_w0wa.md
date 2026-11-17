# PREREG L7 — Janus-LT joint DESI DR2 BAO + CMB(θ*, ω_b, ω_bc) + Pantheon+ w0waCDM fit
Locked 2026-11-17 before any L7 number. Likelihood = L4's (BAO DR2 Table IV + compressed CMB, same grid of z*, z_d, same mν = 0.06)
+ L6's Pantheon+ SN term (zHD > 0.01, STAT+SYS cov, M marginalised analytically). SN distances: D_M from E(z) on a 600-point
z grid with cubic-spline integration; checked against Cosmo.DM quad at 3 cosmologies × 3 z (must be ≤ 1e-5 relative, else
recorded TOO LARGE and the fit is not claimed). Same optimiser starts, same Fisher step sizes as L4.
Target [literature, fetched arXiv 2503.14738 Table V]: DESI+CMB+Pantheon+ w0 = −0.838 ± 0.055, wa = −0.62 (+0.22/−0.19).
Claim: Janus-LT MAP w0 within 0.055 and wa within 0.22 of those values → CONSISTENT, else INCONSISTENT. (Caveat stated up front:
DESI quotes posterior means with full Planck likelihood; ours is MAP + Fisher with a compressed CMB, so 1σ is the honest bar.)
Δχ² vs ΛCDM reported, not tested. Results: field_tests/results/janus_lt_l7_joint.txt.
