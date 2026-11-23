# PREREG N3+N4 (23 Nov 2026 14:05 CT) — neutron ladder: nuclear data in hand, then resonances rebuilt from their parameters
Plan tools/fusion/NEUTRON_LADDER.md; hints tools/fusion/hints/n3n4.json.
## N3 nuclear data (tools/fusion/ndata.py reads OpenMC HDF5, ENDF/B-VIII.0, 294 K) — DATA-access check against held-out Atlas values
D1 thermal (0.0253 eV): Li-6(n,t) MT105 940 b +-2%; H-1(n,g) 0.3326 b +-2%; Li-7(n,g) 0.0454 b +-5%; Fe-56(n,g) 2.59 b +-3%; Mn-55(n,g) 13.3 b +-3%.
D2 14.1 MeV: Be-9(n,2n) 0.5 b +-20%; Pb-208(n,2n) 2.2 b +-15%; Li-7 triton-producing (n,n't) 0.3 b +-30%.
## N4 resonances (tools/fusion/resonance.py: our own MLBW and Reich-Moore from ENDF-102 App. D, H3-H9) on the raw ENDF tapes
R1 Mn-55 (Reich-Moore), 1e-5 eV-125 keV, at the HDF5 0 K energy points: elastic and capture, median |rel diff| <= 0.5% and 95th percentile <= 3%.
R2 Zr-90 (MLBW), 1e-5 eV-200 keV, same metric.
R3 Mn-55 largest s-wave resonance: peak energy within 1 eV of 336 eV; our peak elastic within 2% of the 0 K evaluated peak.
R4 can-fail: Zr-90 with single-level Breit-Wigner (no interference between resonances) must fail R2's elastic median (> 0.5%).
Referee after; DEVIATIONS before any fix; one rerun.
