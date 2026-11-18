# CERN+1 — an independent, validated toolkit that redoes the LHC chain and checks itself

*Independent work by Danny Eldridge (AEGIS project), built with Claude (Anthropic). Not affiliated with, produced by, or endorsed by
CERN or any LHC experiment; "CERN+1" is our working name for "the CERN chain, plus one more independent check at every step".*
Code path: `tools/lhc/` (registry tools `lhc_xsec`, `lhc_ul`, `lhc_lifetime`, `lhc_dt_limit`).

## What the LHC chain does, and what CERN+1 does at each step
| Step | Standard practice | CERN+1 | Measured result |
|---|---|---|---|
| Production cross section | Resummino / Prospino: one heavy run per mass and energy, tables at 13 and 13.6 TeV | Two independent routes: (1) ln σ–ln m spline of the reference tables; (2) Drell–Yan scaling with one universal evolution exponent — needs no PDF file | Route 1 reproduces left-out table points to 0.016% median, 0.30% max. Route 2 predicts the 13.6 TeV table from 13 TeV alone to ≤1.0%, ≤0.29% with κ = −0.163 (same for all three wino channels). At 14 TeV the routes agree to ≤1%; the spread is quoted as the error. Microseconds per call. |
| Particle lifetime | A single benchmark lifetime (τ ≈ 0.2 ns) | Mass-dependent pure-wino lifetime from the two-loop mass splitting, with π, eν and μν widths (μν phase space added) | δm(1 TeV) = 164.1 MeV, cτ = 5.83 cm, BR(π) = 97.9%; τ at the ATLAS limit 0.197 ns |
| Statistics | pyhf asymptotic CLs | pyhf AND exact Poisson CLs side by side; the exact value is used at low counts | Asymptotics are off by up to 8% at low counts (5.00 vs 5.40 events for b = n = 3) |
| Reinterpretation (recast) | SModelS / CheckMATE / full experiment likelihoods | Benchmark-anchored recast that combines our cross sections, our lifetimes and the published signal-region numbers | Two ATLAS disappearing-track searches reproduced with ONE method, no retuning: 136 fb⁻¹ → 666.6 GeV vs 660 (+1.0%); 36.1 fb⁻¹ → 447.8 GeV vs 460 (−2.7%); with the computed boost distribution (kinematics.py, D1307) they become 661.5 GeV (+0.2%) and 446.6 GeV (−2.9%); with the Resummino scale+PDF and δm theory band (theory_band.py, D1309) 661.5 ± 10 GeV (660 inside) and 446.4 ± 5.5 GeV (460 outside — an open residual); HL-LHC like-for-like ≈ 975 GeV |
| Symmetry self-tests | — (not standard) | Charge asymmetry (u/d), Drell–Yan scaling of ratios, SU(2) charged/neutral ratio checked on every table | Ratios scale with τ₀ to 0.1% / 0.05%; the charge asymmetry turns over above 1.5 TeV — flagged as the PDF-limited region (our locked monotonic prediction failed there) |
| Model vs collider | — (experiments test generic models) | Reads the SERAPIS wino window from the theory map and overlays CERN+1 reach | Window 0.67–1.85 TeV begins at the Run-2 limit (666.6 GeV); HL-LHC tests 26% (to ≈975 GeV); the rest needs other probes |
| Future colliders | Dedicated projection studies (one per collider) | One module for any √s and luminosity, anchored on the Run-2 recast | HL-LHC 0.97 TeV vs published 0.9; HE-LHC 1.36–1.68 vs 1.5–2.1; FCC-hh 2.9–3.7 vs 4.5–6.5 TeV (short — cross-section extrapolation to 100 TeV is the weak link); FCC-hh covers the whole SERAPIS window |
| Event generation, detector simulation | MadGraph5_aMC@NLO, Pythia8, Delphes | Not yet (planned, heavy) | — |
| Parton distributions | LHAPDF global sets | Pending (one PDF file to fetch) — then an independent LO calculation as a third cross-section route | — |

## Our process (how we work, and why it is more accurate)
1. **Lock before computing.** Every prediction (what a check should give, and what counts as a pass) is written down, hashed (SHA-256)
   and published to the repository BEFORE the calculation runs (field_tests/rules/PREREG_LHC*.md). Failures are reported as failures —
   e.g. LHC2's first prediction of the wino mass splitting was 1 MeV too low and is recorded as a partial FAIL.
2. **Two independent routes for every number.** A number is only trusted when two methods that share no shortcut agree, and the
   disagreement becomes the quoted error (cross sections: table spline vs physical scaling; limits: pyhf vs exact Poisson).
3. **Reproduce the experiment before predicting.** A recast is only used after it reproduces the experiment's own published limit
   (ATLAS 660 GeV → ours 666.6 GeV) — only then is it extrapolated (HL-LHC).
4. **Replace fixed benchmarks with computed physics.** Where the standard chain uses one benchmark value (a single lifetime), we compute
   it as a function of the model parameters from the published formulas.
5. **Everything is checked, logged and connected.** Each result has a derivation note (D1299–D1301), runs in the shared registry used by
   the Janus app and by the CubeMind learning system, and appears as a node in the AEGIS web.

## Why it is better — stated precisely
- **Faster:** µs–seconds per answer vs minutes–hours per point for the reference codes, with the error bar attached.
- **More honest errors:** every answer carries a measured interpolation or route-spread error instead of an implicit one.
- **More accurate where the standard shortcut is weak:** exact CLs at low counts (up to 8% better than asymptotics); mass-dependent
  lifetimes instead of one benchmark.
- **Not yet better at:** full event simulation and detector response — CERN+1 currently relies on the experiments' published
  efficiencies and on the reference cross-section tables. These are the next steps.

## How we came up with it
It grew out of the AEGIS/SERAPIS research, which predicts wino dark matter with a mass window that LHC searches can test. To score that
prediction honestly we needed the same numbers the experiments use, fast and with errors. The cross-section download was blocked, so we
asked what the physics alone fixes: Drell–Yan scaling says s·σ depends only on 4m²/s, which turned one energy's table into a predictor
for every energy — and the leftover correction came out identical for all three channels, showing it is parton evolution, not a fudge.
The same habits that built the Janus calculator (lock first, two routes, reproduce before predicting) were applied to each LHC step.

## References
Resummino 13.6 TeV tables: arXiv:2304.11915 · Wino mass splitting and widths: arXiv:1212.5989 · ATLAS disappearing tracks (136 fb⁻¹):
arXiv:2201.02472 · CERN+1 cross-section note: doi:10.5281/zenodo.24342227 · Lock workflow: doi:10.5281/zenodo.24291026.
