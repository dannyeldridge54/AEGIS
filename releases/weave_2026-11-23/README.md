# The Weave: predictions, postulates and pre-registered tests (supplement)

Author: Danny Eldridge (independent researcher, Oklahoma City, Oklahoma, USA). Posted 23 November 2026.
Companion to the preprint "The Weave: Predictions and Postulates" (PDF in this record). Builds on SERAPIS v3 (doi:10.5281/zenodo.24250733).
Status: preprint, not peer reviewed. Fits still running at posting time are listed as pending in the PDF; their results will be added in a later version.

## What is here
- `locks/` : every pre-registration (PREREG_*.md) with its SHA-256, and every DEVIATIONS note. Each lock was committed and pushed before the computation it governs.
- `code/engine/` : the calibrated Weave engine (own background solver, gated against CAMB at 8.3e-5), CubeMind v5 facts, the research-only vault and dial tools.
- `code/pc_runs/` : the exact scripts used for the Planck PR4 / CamSpec / ACT DR6 / SPT-3G fits (Cobaya 3.6.2, CAMB 2.0.5).
- `code/brane_z6prime/` : the Z6' (Z6-II) intersecting D6-brane builder, its positive controls against Gmeiner & Honecker (arXiv:0708.2285, 0806.3039) and the scan.
- `code/loom/` : the layer, negative-space ladder, node-equation and restructure scripts.
- `results/` : all result JSONs (fits, controls, ladders).
- `notes/D2110_onward.md` : the dated research log for this stretch, including every correction.

## How a result counts
One entry = one Weave fit and one LCDM fit on the same data. dchi2 = chi2(W) - chi2(L): < -2 preferred, <= +2 consistent, <= +6 mild tension, > +6 disfavoured (PREREG_D2132, D2153). Entries share data and are never summed.

## Licence
AEGIS Community License 1.0 (LICENSE, included). The Zenodo record's metadata licence is CC BY-NC-SA 4.0; where they differ for code, the included LICENSE file applies.
Repository: https://github.com/dannyeldridge54/AEGIS (branch unify-bg).
