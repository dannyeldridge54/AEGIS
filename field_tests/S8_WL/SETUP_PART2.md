# S8-WL Part 2 setup (full DES Y3 cosmic shear) — rule: `rules/PREREG_S8_WL.md` (locked 7 Nov 2026)

Built 7 Nov 2026 (night). Code: `S8_WL/part2/` (`aegis_camb.py` CosmoSIS module, `run_part2.py` driver).

1. **Software:** CosmoSIS 3 (`pip install cosmosis`; needs liblapack-dev, libgsl-dev) + the CosmoSIS standard library
   (`git clone https://github.com/joezuntz/cosmosis-standard-library`, then `source cosmosis-configure; make` with
   `GSL_INC`/`GSL_LIB` set; the CLASS and WMAP parts may fail and are not needed). Python: fast-pt, astropy.
   The DES Y3 data vector, covariance and n(z) ship with the standard library (`likelihood/des-y3/`).
2. **Pipeline:** the standard DES Y3 cosmic-shear pipeline (TATT intrinsic alignments, photo-z shifts, shear
   calibration m, fiducial scale cuts `examples/des-y3-scale-cuts.ini`, Y3 nuisance priors), with the CAMB module
   replaced by `aegis_camb.py`, which puts in each stored best fit's dark energy (ΛCDM, the Locked Twist's
   EarlyQuintessence, or the UB-2 two-field module) and runs CAMB once (cosmology fixed).
3. **Fit:** CosmoSIS `maxlike` (Nelder–Mead) over the 13 nuisance parameters only; χ²_WL = −2 ln(posterior) at the
   optimum; the pure data χ² is reported beside it.
4. **Run:** `CSL_DIR=<standard library> python run_part2.py` → `S8_WL/results/part2_desy3.json`.

**Not covered yet: the Spiral pairs.** The Spiral needs the coupled-dark-matter matter power spectrum from the AxiCLASS
coupled build, which CAMB cannot produce. Plan: write P(k, z) and distances from AxiCLASS (PC, WSL) to files and load
them with a small CosmoSIS module in place of `aegis_camb.py`. Until then those rows are NO VERDICT, as the rule says.

**Fixes logged while building (no rule change):** CAMB's `get_BAO` re-initialises EarlyQuintessence (Fortran
"already allocated"); `aegis_camb.py` computes the same four BAO quantities from the existing background instead.
