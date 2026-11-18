# Janus-LHC — plan and status (started 2026-11-18, Danny: "collect data… compare exactly how they compute… make their toolkit better… make one for them")

## How the LHC community computes (the chain we are matching)
| Step | Their standard tool | What it does | Our route |
|---|---|---|---|
| Cross sections (SUSY) | Resummino (NLO+NLL / aNNLO+NNLL, Mellin-space PDFs), NNLL-fast | one run per mass point, minutes | `tools/lhc/xsec.py`: surrogate of the published tables, µs per call, own error bar; next: our own LO computation with a PDF set (needs Danny's OK to download one) |
| Event generation | MadGraph5_aMC@NLO + Pythia8 | parton → hadron events | later (heavy; PC job) |
| Detector | Delphes | fast detector response | later |
| Recasting | SModelS, CheckMATE, MadAnalysis 5, Rivet | compare a model to published limits | SModelS 3.2.1 installed (pip); its database download is blocked here; next: our own disappearing-track recast from HEPData tables |
| Statistics | pyhf (HistFactory), published likelihoods on HEPData | CLs limits | `tools/lhc/stats.py`: pyhf + an independent exact-Poisson CLs |

## v0 results (cloud, 2026-11-18)
- Reference data saved: wino-like χ̃₂⁰χ̃₁± and χ̃₁⁺χ̃₁⁻ cross sections at 13 and 13.6 TeV, 100–2000 GeV (arXiv:2304.11915 Table 6; label in the
  extracted text: aNNLO+NNLL — to verify against the PDF before scoring anything).
- Surrogate accuracy (leave-one-out over 54 interior points): median 0.02%, max 10.3% (the max is at 200 GeV where the curve is steepest;
  fix: denser reference points there or interpolate in ln m). 14 TeV values are an EXTRAPOLATION (log-linear in √s) and labelled so.
- Statistics cross-check: pyhf (asymptotic) vs exact Poisson CLs for counting experiments: b=0.5,n=0: 3.07 vs 3.00; b=3,n=3: 5.00 vs
  5.40; b=10,n=12: 9.51 vs 9.97 → asymptotics are off by up to ~8% at low counts. Improvement we can offer: use exact (or toy-based)
  CLs automatically when counts are small, and report both.

## Next (in order)
1. Verify the Resummino table against the PDF; add the higgsino table; fix the 200 GeV interpolation error.
2. Disappearing-track recast: ATLAS/CMS HEPData acceptance × efficiency maps (fetch as text) → our limit vs theirs (must reproduce the published limit before any use).
3. Our own LO cross section (Drell–Yan-like q q̄' → W*/Z*/γ* → χχ) with a PDF set — needs a PDF download (Danny's OK); K-factor vs Resummino as the validation.
4. pyhf with published full likelihoods (HEPData) for one SUSY analysis; speed + agreement benchmark.
5. Register each piece in the CubeMind/Janus registry and the web.
