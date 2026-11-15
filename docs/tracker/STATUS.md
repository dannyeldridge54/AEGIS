# SERAPIS prediction tracker — status 2026-11-15

Predictions frozen 2026-11-15 (locks in field_tests/rules). Data file version 2026-11-15. Only data dated after the freeze count as tests; earlier data show consistency only.

| Prediction | Frozen value | Kill condition | Status |
|---|---|---|---|
| Spectral index n_s | 0.969 – 0.975 | measured n_s more than 3σ outside the band | **alive** |
| Tensor ratio r | 0.000455 – 0.00057 | r < 2.4e-4 at 95% CL, or r detected > 1.1e-3 | **alive** |
| Running α_s | -0.00106 – -0.00085 | α_s > -3e-4 at 3σ, or violates the Janus relation | **tension** |
| Family caps (any ε) | 0 – 0.985 | n_s > 0.985 or r > 8.3e-4 at 3σ | **alive** |
| Σm_ν (normal ordering, m1≈0) | 0.0587 | Σm_ν > 0.07 eV measured, or a robust bound below 0.0587 eV | **tension** |
| f_NL local | 0.0115 | abs(f_NL) > 5 | **alive** |

## Spectral index n_s (D605, D615, D693)

| Dataset | Comparison | Status | Counts as |
|---|---|---|---|
| WMAP9 | 0.972 ± 0.013 → 0.00σ from band | consistent | pre-freeze (consistency) |
| Planck 2013 | 0.9603 ± 0.0073 → 1.19σ from band | consistent | pre-freeze (consistency) |
| Planck 2015 | 0.9655 ± 0.0062 → 0.56σ from band | consistent | pre-freeze (consistency) |
| Planck 2018 | 0.9649 ± 0.0042 → 0.98σ from band | consistent | pre-freeze (consistency) |
| P-ACT-LB (ACT DR6) | 0.974 ± 0.003 → 0.00σ from band | consistent | pre-freeze (consistency) |
| SPA (SPT+Planck+ACT) | 0.9682 ± 0.0032 → 0.25σ from band | consistent | pre-freeze (consistency) |
| SPA + DESI BAO | 0.9728 ± 0.0029 → 0.00σ from band | consistent | pre-freeze (consistency) |

## Tensor ratio r (D605, D615)

| Dataset | Comparison | Status | Counts as |
|---|---|---|---|
| BICEP/Keck 2018 + Planck | r < 0.036 (95%) vs band 4.6e-04–5.7e-04: not yet sensitive | consistent | pre-freeze (consistency) |
| Planck+SPT+ACT+BK | r < 0.034 (95%) vs band 4.6e-04–5.7e-04: not yet sensitive | consistent | pre-freeze (consistency) |

## Running α_s (D633, D693)

| Dataset | Comparison | Status | Counts as |
|---|---|---|---|
| Planck 2018 | -0.0045 ± 0.0067 → +0.53σ | consistent | pre-freeze (consistency) |
| ACT DR6 (P-ACT-LB) | 0.0062 ± 0.0052 → -1.38σ | consistent | pre-freeze (consistency) |
| ACT+Planck+SPT | 0.008 ± 0.0057 → -1.57σ | consistent | pre-freeze (consistency) |
| DESI DR1 Lya P1D + BAO + CMB | 0.0014 ± 0.0041 → -0.57σ | consistent | pre-freeze (consistency) |
| Planck + eBOSS Lya (Rogers & Poulin) | -0.0108 ± 0.0022 → +4.48σ | fail | pre-freeze (consistency) |

## Family caps (any ε) (D675, D677)

| Dataset | Comparison | Status | Counts as |
|---|---|---|---|
| WMAP9 | n_s 0.972 vs cap 0.985 | consistent | pre-freeze (consistency) |
| Planck 2013 | n_s 0.9603 vs cap 0.985 | consistent | pre-freeze (consistency) |
| Planck 2015 | n_s 0.9655 vs cap 0.985 | consistent | pre-freeze (consistency) |
| Planck 2018 | n_s 0.9649 vs cap 0.985 | consistent | pre-freeze (consistency) |
| P-ACT-LB (ACT DR6) | n_s 0.974 vs cap 0.985 | consistent | pre-freeze (consistency) |
| SPA (SPT+Planck+ACT) | n_s 0.9682 vs cap 0.985 | consistent | pre-freeze (consistency) |
| SPA + DESI BAO | n_s 0.9728 vs cap 0.985 | consistent | pre-freeze (consistency) |

## Σm_ν (normal ordering, m1≈0) (D605)

| Dataset | Comparison | Status | Counts as |
|---|---|---|---|
| Planck 2018 | < 0.12 eV vs 0.0587 | consistent | pre-freeze (consistency) |
| DESI DR1 + CMB | < 0.072 eV vs 0.0587 | consistent | pre-freeze (consistency) |
| DESI DR2 + CMB | < 0.0642 eV vs 0.0587 | consistent | pre-freeze (consistency) |
| DESI DR2 + CMB (Feldman-Cousins) | < 0.053 eV vs 0.0587 | pressure (excludes the NO floor) | pre-freeze (consistency) |

## f_NL local (D605)

| Dataset | Comparison | Status | Counts as |
|---|---|---|---|
| Planck 2018 | -0.9 ± 5.1 vs 0.0115 | consistent | pre-freeze (consistency) |
