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
