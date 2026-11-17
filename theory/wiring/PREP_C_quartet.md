# PREP (C) Mapper quartet: orbits + dust + distances + halo (Djl C, 17 Nov 2026 13:18 UTC)
## State
- dustmaps installs from pip here. The module is tools/janus_astro/mapper_dust.py: SFD 2D or Bayestar19 3D, giving E(B−V) and then A_G.
- Maps are NOT reachable from the cloud workspace. dataverse.harvard.edu, IRSA and zenodo.org all time out through the allowlist. They must be fetched on Danny's PC.
- Approximate sizes: SFD about 0.1 GB, Bayestar19 about 0.7 GB (estimate; check on download). This needs Danny's download OK.
- Real Mapper per-star output is not in the repo. ufe-v2/cosmos_map has only star_scan_summary.json (patch counts), so W3 can't run yet. Its inputs would be the per-star (l, b, parallax, G, RV) list from the PC Mapper run.
## To source before locking C1
- R_G = A_G/E(B−V) for Gaia G, e.g. Casagrande & VandenBerg 2018 or the Gaia EDR3 extinction law (colour-dependent). Fetch it; don't use a remembered value.
- Bayestar19 unit conversion to E(B−V) (Green+2019 paper).
## C1 plan (lock when the maps and per-star data exist)
- T1: our SFD query vs dustmaps' own test values / the IRSA DUST service at a handful of (l, b).
- T2: A_G-corrected abs_mag_G feeds orbit_params unchanged (lossless).
- R: how much dust moves the Mapper's HR-diagram selection and its z_max medians (W2 observable).
## Sourced 13:40 UTC (Djl C)
- R_G (Casagrande & VandenBerg 2018, arXiv:1806.01953, Table 2):
  - mean ⟨R_G⟩ = 2.740 (⟨R_BP⟩ 3.374, ⟨R_RP⟩ 2.035)
  - fit R = a0 + T4(a1 + a2 T4) + a3[Fe/H], T4 = 1e-4 T_eff, valid 5250–7000 K
  - G coefficients: 1.4013, 3.1406, −1.5626, −0.0101
  - Coded as mapper_dust.R_cv18; outside the T_eff range it falls back to the mean.
- Still to settle in C1: which E(B−V) scale CV18 assumes vs the SFD map's (SFD vs the Schlafly & Finkbeiner 2011 recalibration). Fetch that, don't assume it.
- Remaining blocker: the maps and per-star data on Danny's PC.
