# S8-WL setup (PC), after the rule is locked

1. **Lock the rule:** edit `DRAFT_PREREG_S8_WL.md`, rename it `PREREG_S8_WL.md`, write its SHA-256 and the time to
   `PREREG_S8_WL.md.sha256`, commit. Only then continue.
2. **CosmoSIS:** in the TWIST environment, `pip install cosmosis cosmosis-build-standard-library` and build the
   standard library (gives the DES Y3 shear likelihood and the CAMB module with HMCode2020).
3. **KiDS-Legacy:** clone `https://github.com/AngusWright/CosmoPipe` and fetch the released KiDS-Legacy COSEBIs data
   vector, covariance and n(z) as its README describes.
4. **Twist matter power:** the CAMB module must be given `dark_energy_model = EarlyQuintessence`, `n = 3`,
   `use_zc = T` and the stored f_EDE, z_c, θ_i from `cmp_edelockP.json`; ΛCDM uses `cmp_lcdmP.json`. Check first that
   CAMB alone reproduces the stored H₀ and σ₈ of both points to 0.1% (log it); if not, stop.
5. **Run:** for each survey and model, minimise over the survey's nuisance parameters only (cosmology fixed), and save
   χ²_WL to `field_tests/S8_WL/results/<survey>_<model>.json`.
6. **Score:** apply the locked rule; add the result to `field_tests/STATUS.md`.
