# PREREG N6-N8 TRANSPORT (23 Nov 2026 14:50 CT) — neutron ladder: slowing-down kernel, our own Monte Carlo, computed TBR
Plan tools/fusion/NEUTRON_LADDER.md; hints tools/fusion/hints/n6n8.json.
Build tools/fusion/mc.py: continuous-energy analog Monte Carlo (ENDF/B-VIII.0 HDF5, 294 K), concentric-sphere geometry; reactions sampled
from non-redundant partial cross sections; secondary neutrons from the evaluated distributions (elastic + discrete-level inelastic angular
tables, Kalbach-Mann continua incl. (n,2n), continuous tabular, evaporation; correlated if present); CM->lab per reaction flag; target at
rest (free-gas thermal motion neglected: stated approximation); photons not transported; collision estimator for tritium production (MT205).
## Goalposts (locked)
K1 (N6) elastic kernel with isotropic CM scattering: Monte Carlo mean lethargy gain within 1% of the analytic xi for A = 1, 12, 56, 208.
T1 (N7/N8 held-out: OpenMC workshop task 5, H8/H9) TBR within +-5% of 1.0266 (their stat 1.8%; library may differ), with >= 20,000 histories.
T2 leakage fraction within +-30% of 0.0437.
T3 Li-7 share of TBR between 0.1% and 1.5% (theirs 0.37%).
T4 can-fail: with Pb (n,2n) switched off (MT16 treated as absorption-free removal: no secondaries -> particle killed) TBR must drop > 10%.
Referee after; DEVIATIONS before any fix; one rerun.
