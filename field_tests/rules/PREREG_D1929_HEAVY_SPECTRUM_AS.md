# PREREG D1929 — α_s with the S-at-i spectrum (locked 21 Nov 2026 before running; repo at 15feaecb)
Script theory/tests/d1929_heavy_spectrum_as.py, two-loop weave_rg2 unchanged.
- Validation: the baseline spectrum (wino 0.69 TeV, gluino 4.93 TeV, scalars 4.7e5 GeV) must reproduce α_s(unif) = 0.1147 to 5e-4. If not, the run is VOID.
- Heavy spectrum: wino 2.0 TeV, gluino 14.5 TeV, scalars ×(7.6e5/2.58e5) = 1.38e6 GeV.
- PASS if α_s(M_Z) for exact unification lies within 2σ of 0.1180 ± 0.0009; otherwise FAIL.
- Report only: the heavy spectrum with the scalars held at 4.7e5 GeV.
Expectation: none stated. Trials +1 (trials_alpha_s.md).
