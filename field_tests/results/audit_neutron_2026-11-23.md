# Back-end audit, neutron side (R99, sonnet, read-only; scratch /tmp/audit_n) — 23 Nov 2026, requested by Danny 13:48-13:49
Verdict: no remaining sampling bug moves TBR or dpa; both open discrepancies explained; weak points are test design and latent paths.
Verified: KM sampler, evaporation/maxwell u, level inelastic (no sub-threshold), yields, rotation, geometry, collision vs track-length within 1%,
penetrability/shift/phase incl. l=3, NAPS/APL, negative ER.
1 TBR 0.69 vs 0.84: yield override keyed on MT only also removed Fe (n,2n) (Fe56 0.42 b) and Li-7 MT16. Pb-only yield 1: 0.831+-0.008 (-18%);
  all-MT16: 0.687 -> override now keyed (MT, nuclide prefix); N6-N8 T4 restated as Pb-only (correction D2207a); DEV-2 text quoting 0.838 was right for Pb-only.
2 front-cm dpa: repo 7.1 is right (track-length 7.19); the scratch 10.7 had a normalisation slip. Front face ~30% below the ~10 rule of thumb;
  D1 passed on the 10 cm average (5.54 vs edge 5) and D2 only after the post-hoc Fe-only switch (7.38 vs edge 7) -> both reported as weak passes (D2207a).
3 doppler.py zeroed sigma below the grid (left=0): Zr-90 294 K capture -0.45% at 1.03e-5 eV (the unexplained N5 max) -> 1/v extension below the grid.
4 mc._sample_table discrete-line index off by one (inclusive cdf) - dormant (no neutron table with discrete lines in the 25 nuclides) -> fixed.
5 Correlated: no scaled E_out interpolation, lower-point mu (<=0.5% on <E_out>) -> noted (approximation).
6 source 14.0 MeV vs normalisation 14.06 in N9/N10: M low by 0.43% -> corrected M = 1.161 (D2207a); test normalises by the source energy from now on.
7 test design: K1 tests a copy of the kinematics, no neutron balance, E2 54% vs 3% margin, R1/R2 four orders of slack (only R4 discriminates), R3 relocked,
  P4 self-referential, N3 D2 references unsourced and suspiciously close -> listed; next locks: end-to-end kernel test via run(), neutron balance,
  tighter bands, sourced references.
8 N1 DEVIATIONS seed spreads (1.5/0.45/0.27%) contradict n1_rerun.json (2.4/1.6/0.95%) -> correction D2204a; single-run noise ~2%, B1 weakly informative.
9 resonance.py: MLBW with I>0 and two channel spins untested; GF/GX, extra ranges/isotopes silently ignored; tests suppress warnings -> noted.
