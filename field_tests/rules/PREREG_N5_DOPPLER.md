# PREREG N5 DOPPLER (23 Nov 2026 14:25 CT) — neutron ladder: resonances at temperature (exact free-gas kernel)
Plan tools/fusion/NEUTRON_LADDER.md; hints tools/fusion/hints/n5.json.
Build tools/fusion/doppler.py: Solbrig kernel (H1) applied to OUR N4 0 K reconstruction (elastic and capture) on the NJOY 0 K grid.
Goalposts (held-out: NJOY BROADR curves in the ENDF/B-VIII.0 HDF5), evaluated on the HDF5 temperature grid, 1 eV to the top of the
resolved range (Mn-55 125 keV, Zr-90 200 keV):
P1 Mn-55 (RM) elastic and capture at 294 K and 900 K: median |rel diff| <= 0.2%, p95 <= 1%.
P2 Zr-90 (MLBW) same.
P3 can-fail: our unbroadened 0 K capture vs the 900 K evaluation must have median > 2% for Mn-55.
P4 1/v check: Mn-55 capture at 0.0253 eV at 900 K within 0.5% of the 0 K value.
Referee after; DEVIATIONS before any fix; one rerun.
