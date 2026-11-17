# PREREG L10 — Janus-LT w0–wa profile-likelihood grid (BAO + CMB compressed + Pantheon+), the shape behind L7's Gaussian errors
Locked 2026-11-17 before any L10 number. Likelihood: exactly L7's chi2 (theory/janus_lt/l7_joint.py, D1042), reused by import of its definitions.
Grid: w0 ∈ [−1.20, −0.50] step 0.05 (15), wa ∈ [−1.40, +0.40] step 0.1286 (15) = 225 points; at each point χ² is minimised over (h, ω_b, ω_bc)
(Nelder–Mead, 2 starts). Profile Δχ² = χ²(w0, wa) − min over grid and L7 MAP.
Claims: C1 grid minimum within one grid step of L7's MAP (w0 −0.853, wa −0.518); C2 Δχ² at (−1, 0) vs the overall minimum = L7's 7.70 ± 0.30;
C3 (reported, decisive for the label only) DESI Table V best fit (−0.838, −0.62) lies inside our Δχ² = 2.30 region.
C1 and C2 → PROFILE CONSISTENT WITH L7; C3 adds "contains DESI". Also reported: 68%/95% (Δχ² 2.30/6.18) region extents vs L7's Gaussian ±σ.
Runs on the cloud box (background, ~30 min). Results: field_tests/results/janus_lt_l10_profile.txt (+ grid .npz, + stamp).
