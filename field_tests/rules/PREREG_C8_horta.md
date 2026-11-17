# PREREG C8 — Galaxy potentials vs Horta+2026 at the Sun — locked 2026-11-17, before code or run
Data: arXiv:2601.18876 abstract, as recorded in D1193.
- v_c☉ = 235.3 +2.8/−3.7 km/s; Ω☉ = 28.5 +0.4/−0.1 km/s/kpc; κ☉ = 36.9 +0.8/−1.0 km/s/kpc.
- The side of the asymmetric error is chosen by the sign of the residual.
Models (galpy):
- MWPotential2014 (natural units; multiply by ro = 8, vo = 220).
- McMillan17 (physical output ON: no extra ×vo, per DEVIATIONS_C7 D1).
Evaluated at R = 8.178 kpc (our IGS convention; labelled) and also at Horta's implied R0 = v_c/Ω = 8.256 kpc (reported).
- v_c = vcirc; Ω = v_c/R; κ = galpy epifreq.
Gaia NFW + McMillan17 baryons: skipped. galpy's McMillan17 does not separate cleanly into baryons and halo without editing its component list, which is out of scope this tick (labelled).
Score per model:
- PASS iff |pull| ≤ 2 for both v_c and Ω at R = 8.178;
- κ reported, not scored.
