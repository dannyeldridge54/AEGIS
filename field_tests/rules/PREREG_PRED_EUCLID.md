# Euclid / Rubin: extra frozen predictions (frozen numbers)

**Status: LOCKED** on Danny's word (9 Nov 2026, 01:33 CT, "Start them"); time and fingerprint in the .sha256 file. Lensing S8 forecasts for Euclid/Rubin are already locked (PREREG_LENSING_FORECASTS.md).
This adds two numbers to be frozen, from `theory/v2_frozen_numbers.json` (computed 9 Nov from the stored fits, no data):

1. **Dark-matter mass change since recombination (Spiral):** -0.81% / -0.95% / -0.89% (P+ / Dovekie / Union3), i.e. dark matter today is ~0.8–0.95% lighter per particle than at z = 1100, read from the code's ρ_cdm a³. Note: an earlier theory audit (7 Nov) said the mass grows; the code says it shrinks. Sign settled 9 Nov in theory/DM_COUPLING_PICTURE.md: shrinks, for the fitted models (argued, not a direct solver run).
2. **S8-L small-scale step:** linear power halved-suppression point k ≈ 0.57 h/Mpc, suppression 44% at k = 10 h/Mpc relative to the Spiral (cold matter; S8-LNL D2). A Euclid/Rubin small-scale or Lyman-α measurement showing no suppression at k ≲ 1 h/Mpc would rule S8-L out.

Scoring rule to be written with the Euclid DR1 data products (mid-2027) and locked before their release.
