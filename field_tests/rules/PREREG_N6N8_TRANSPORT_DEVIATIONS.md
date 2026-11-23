# N6-N8 DEVIATIONS (written before the rerun). Locked run: K1, T1-T4 PASS (TBR 1.0226+-0.0063).
Referee R96 (sonnet; scratch runs in /tmp):
- DEV-1 (BUG, mine; also in hint H5) Kalbach-Mann branches swapped: the e^{a mu} (precompound) branch must be taken with probability r, the
  cosh branch with 1-r (OpenMC: cosh if prn > r). Affects angles of every Pb (n,2n) and continuum secondary. R96 scratch with the fix:
  TBR 1.0193+-0.008, leakage 0.0395 (within noise) -> TBR is blind to it; angular sampling is NOT validated by T1.
  Fix: swap the branches. (KM r, a taken at bin k instead of interpolated: minor, unchanged.)
- DEV-2 (test design) T4 killed the neutron on (n,2n) (a strawman: -64%). Replaced by MT16 yield forced to 1 (multiplication off, neutron kept);
  R96 scratch: TBR 0.838 (-18%). New T4: TBR must drop by > 10% with yield 1.
- DEV-3 (statistics/wording) 8 batches -> 16 batches x 2500 histories in the rerun; T1 (+-5%) is ~2.7x OpenMC's own error and cannot separate
  libraries: the result is reported as "consistent with" the workshop value, not "validated".
- Noted, no change: target at rest / no free-gas thermal motion is the likeliest hidden compensating effect (resonance capture in Pb/Fe,
  Li-6 1/v region); the non-redundant sum vs MT1 was not checkable (MT1 absent from the HDF5).
Checked correct by R96: collision estimator (unbiased, consistent Sigma_t), yields, correlated layout, elastic/CM->lab, level inelastic, geometry.
