# PREREG CH1b — hydrogen 21 cm hyperfine frequency in the wavelength tool (18 Nov 2026, written before computing)
Problem: tools/chem/wavelength.py hydrogen_21cm() (Fermi formula, reduced-mass factor) gives 1418.84 MHz vs the measured 1420.405751768 MHz (Hellwig et al. 1970; Essen et al. 1971): −1.1e-3 relative, so CH1 was not adopted.
Change (one factor, standard textbook physics): multiply by (1 + a_e), the electron anomalous magnetic moment (CODATA via scipy 'electron mag. mom. anomaly').
Not included (stated, not fitted): Breit relativistic factor (+3/2 α² ≈ +8e-5), higher QED, recoil and proton-structure (Zemach ≈ −4e-5) terms. These partly cancel.
Expectation (rough mental estimate before running, stated for honesty): residual ≈ +6e-5.
PASS: |ν/1420.405751768 MHz − 1| < 1e-4. FAIL otherwise; on FAIL the tool keeps the 21 cm line marked "not adopted".
Single run; no further factors added to chase the number. The tool label stays "standard atomic physics".
