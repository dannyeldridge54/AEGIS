# Inflation Scorecard (+ Janus calculator)

Give it an inflation model's predictions; it scores them against every current dataset, one row per dataset,
with the pull in σ, a verdict and the arXiv source. All data live in one file,
[`inflation_scorecard/data/constraints.yaml`](inflation_scorecard/data/constraints.yaml): updating to a new release is a one-line edit.

Probes: n_s in every CMB release since WMAP9; the running α_s (CMB and Lyman-α); r limits; Σm_ν; N_eff; f_NL;
and with `--camb`, the linear power at z = 3 compared with the eBOSS and DESI Lyman-α forest, plus S8.

## Install
```bash
pip install ./tools/scorecard            # add [camb] for the Lyman-alpha and S8 rows
```

## Use
```bash
inflation-scorecard --label SERAPIS --ns 0.970 0.975 --r 5e-4 --alpha-s=-1.0e-3 --beta-s=-3.8e-5 \
    --sum-mnu 0.0587 --camb --out scorecard.md --figure ns_history.png
```
(Write negative numbers with `=`, e.g. `--alpha-s=-1e-3`.) Verdicts per dataset: |pull| < 2 consistent, 2–3 tension, > 3 fail.
The datasets are correlated, so the pulls are not to be combined.

## Janus calculator
For plateau models with a tilt, V ≈ 1 − A e^{−pφ} + δ e^{qφ} (κ = q/p), the running follows from (n_s, r) alone:
ϱ = p√(r/2)/(1−n_s), x = (ϱ−1)/(1+κϱ), α_s = −½(1−n_s)²(1+x)(1+κ²x)/(1−κx)², and a closed β_s.
```bash
janus 0.9725 4.65e-4 --class "SERAPIS-E (Epstein E(tau,2))"    # or --p 0.8165 --kappa 0
janus 0.972 5.2e-4 --serapis-offset                            # offset-corrected SERAPIS tau = i form
```
Accuracy against exact numerics (tests): SERAPIS-E 3.5–5%; α-attractor T-model (α = 1, no tilt) 1.2–1.5%;
offset-corrected SERAPIS τ = i form 0.2–0.4% (AEGIS D640).

## Tests
`pytest tools/scorecard/tests` reproduces the published SERAPIS scorecard (AEGIS notes D710, D711) and the Janus checks.

## Licence
Dual-licensed: **AGPL-3.0-or-later** (free for everyone; see [LICENSE](LICENSE)) or a **commercial licence** for organisations that do not want the AGPL's obligations — tiers and contact in [COMMERCIAL.md](COMMERCIAL.md). © 2026 Danny Lee Eldridge.
