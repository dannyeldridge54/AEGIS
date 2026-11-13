LOCKED 2026-11-13 (time = lock commit) by the development driver under STANDING_LOCK_AUTHORITY.md

# PREREG_SN_SWAP — the same test on Union3 and DES-Dovekie

Identical to PREREG_DESY5_SWAP.md in likelihood, models, fitting, readings and failure handling, with the supernova
block replaced by, in turn:
- **UNION3**: Union3 binned magnitudes (cobaya_packages sn_data/Union3/lcparam_full.txt, 22 points, columns zcmb, mb;
  zhel = zcmb as in Cobaya's union3.py), covariance mag_covmat.txt (total).
- **DOVEKIE**: DES-Dovekie (sn_data/DES-Dovekie/DES-Dovekie_HD.csv, 1820 SNe, zHD, zHEL, MU), inverse total covariance
  covtot_inv_000.npz unpacked as Cobaya does (upper triangle, reflected).
Gate per set: the expected number of points loads (22 / 1820), the LCDM chi2 is finite, and the W0WA fit gives
w_a < -0.40. Readings per set: TWIST HOLDS ON <SET> / STRAINED / FAILS ON <SET> with the DESY5-SWAP bands.
Code: field_tests/missing_piece/sn_swap.py (SNSET=UNION3|DOVEKIE). Runs after DESY5-SWAP finishes (CPU).
