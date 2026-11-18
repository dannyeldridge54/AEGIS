# Referee response — Janus-LHC / CERN+1 cross sections (doi:10.5281/zenodo.24342227)

## 18 Nov pass
Verdict on v1: MINOR-TO-MAJOR REVISION (every number reproduced; error-bar scope, attribution and prior art needed fixing). All fixes applied in the .tex (v2); rebuilt twice with pdflatex, no undefined references.

Numbers checked from the repo root with python3 (field_tests/lhc1_scaling.py, tools/lhc/xsec.py, tools/lhc/stats.py, D1299):
- P1: +0.454…+0.997%, +0.472…+1.001%, +0.469…+0.961% (≤1.0%): reproduced.
- P2: κ = −0.165/−0.163/−0.161, max dev 0.291/0.263/0.260%: reproduced.
- P3: 0.71–0.96% at m = 500, 1000, 1100, 1500, 1800 GeV: reproduced.
- Route 1 LOO: median 0.0153% (13 TeV), 0.0160% (13.6 TeV); max 0.30% / 0.15%; n = 54; ln σ–m spline 10.3% at 200 GeV: reproduced.
- Example: 0.7869 fb, spread 0.81% at m = 1.1 TeV, 14 TeV: reproduced.
- CLs pairs 3.07/3.00, 5.00/5.40, 9.51/9.97 (pyhf/exact): reproduced; the largest difference is 7.9% relative to pyhf.
- Reference table spot-checked against arXiv:2304.11915 Table 6 (aNNLO+NNLL, mass-degenerate winos): 100 and 1000 GeV rows at 13 and 13.6 TeV match the json.

### Required issues and changes
1. **Toolkit name**: title, abstract and footnote now say CERN+1 (formerly Janus-LHC), with an independence disclaimer (not affiliated with, sponsored by or endorsed by CERN or any LHC experiment).
2. **Error-bar scope (required by editor)**: the abstract, Route 1, the example and the limitations now say that the quoted errors are interpolation/route spread only and exclude the reference tables' PDF and scale uncertainties, which must be added from Resummino.
3. **"Uses no PDF file"**: clarified. No PDF file is called, but the PDFs enter through the 13 TeV reference table.
4. **"Single, process-independent signature of parton evolution" (overclaim)**: now "nearly the same for the three channels, as expected for q q̄′ channels sharing luminosities; absorbs mainly the scale evolution of the PDFs", and κ also absorbs α_s running in higher orders and M_W,Z effects. Title "Universal" changed to "Common". Two-energy lever arm (4.6%) and the assumption that κ stays constant are stated.
5. **Scaling derivation incomplete**: the conditions are now stated: σ̂ = f(4m²/ŝ)/ŝ (m the only scale; W/Z masses and squark exchange neglected) and a scale-independent luminosity. The μ ~ m argument for why κ ≠ 0 is given.
6. **P2 is in-sample**: now says κ is least-squares fitted to the same 13.6 TeV entries (19 masses, 200–2000 GeV), so this is a fit, not a prediction.
7. **P3 independence**: both routes are two-point extrapolations from the same tables, and the scaling route is lower at every point. The spread is therefore labelled extrapolation ambiguity, not an independent error. The five tested masses are now listed.
8. **"All tests were pre-registered"**: false for the CLs comparison (no PREREG file covers pyhf vs exact). Now "the three cross-section tests were pre-registered", and the statistics section says the comparisons were not locked.
9. **CLs comparison conflates effects**: the exact route uses n as the test statistic with no background uncertainty, and pyhf uses asymptotic q̃_μ. Both differences are now stated; "8%" is given relative to pyhf.
10. **Prior art**: Drell–Yan (1970) cited for the scaling; Quigg (arXiv:0908.3660) cited for parton-luminosity rescaling between energies; the novelty is restricted to a calibrated one-parameter version on the Resummino tables.
11. **Median LOO**: "0.016%" made precise as 0.015% (13 TeV) / 0.016% (13.6 TeV); the 54 points are explained (18 interior masses × 3 channels).
12. **Bibliography**: Resummino now has full authors and EPJC 83, 707 (2023). Added Drell–Yan, Quigg, Junk, Read, Cowan–Cranmer–Gross–Vitells, pyhf (JOSS 6, 2823) and the full P4 title. Archive URL wrapped in \url.

### Headline-claim flags
- "One universal evolution exponent / process-independent signature" is downgraded to "one common exponent for these three channels" (title changed).
- The 14 TeV error bar is explicitly restricted to route spread (no PDF/scale); the numbers are unchanged.
- "All tests were pre-registered" is narrowed to the cross-section tests.
