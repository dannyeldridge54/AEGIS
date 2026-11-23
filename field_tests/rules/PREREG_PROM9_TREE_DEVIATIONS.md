# PROM-9 TREE DEVIATIONS (written before the rerun). Locked run: TREE FAIL, 5/9 layers (FAIL L1, L3, L4, L8).
Referee R92 (sonnet, read-only; scratch runs in /tmp; checked cfspopcon 9.0.1 source).
- DEV-1 (my error: stale goalposts) L1, L3, L8 were locked with values ALREADY corrected in PREREG_FUSION1_DEVIATIONS:
  L1 neutron share 0.7997 -> 0.7976 +- 0.001 (FUSION-1 DEV-1, the 14.07 shortcut); L8 5.9 keV at 15.7 MK -> 5.9 +- 3% at 15 MK and
  6.07 +- 3% at 15.7 MK (FUSION-1 DEV-2); L3 tau_E window 3.0-4.4 s -> 3.4 s +- 15% (FUSION-1 DEV-7). Relocked to the corrected values.
  The locked FAILs on L1/L3/L8 stay on the record. Same class of mistake the playbook already lists (goalposts copied, not re-derived).
- DEV-2 (source-faithful, L4) cfspopcon evaluates IPB98 with the VOLUME-averaged n_e and areal elongation
  kappa_A = V / (2 pi R^3 eps^2 (pi - (pi - 8/3) eps)); ours used line-averaged n_e and V/(2 pi^2 R a^2). R92: the two cancel (net ~0).
  Adopted for the SPARC node anyway (like-with-like). Plasma volume: Creely's 20.9 m^3 (INPUT) instead of the ITER-calibrated 21.4.
- Not done (tuning): lowering H98 until L4 passes. R92: H98 0.9 -> 150 MW / 7.9 keV, 0.8 -> 82 MW: the SPARC point is so steep in T that a
  10-20% confinement difference swings P_fus by x2. L4 stands or falls on the rerun.
One rerun.
