# theory/: scripts and outputs for the BI-supergravity theory note

Theory note: doi:[10.5281/zenodo.23899237](https://doi.org/10.5281/zenodo.23899237) (v2) · source in
[../papers/theory_note/](../papers/theory_note/).

| Script | What it computes | Output |
|---|---|---|
| `bi_kahler_lambda.py` | Kähler metric of the Gates–Ketov–Yunes BI superfield; λ = −2√(2/3) (sympy) | `bi_kahler_lambda.json` |
| `solar_lowz.py` | Solar-system gate (Cassini) for the BI dilaton | `solar_gate.json` |
| `bi_superpotential.py` | Supergravity potential for constant W | `bi_superpotential.json` |
| `ufe_checks.py` | Inflation from α = 1; dilaton as early field; LQG value | `ufe_er.json`, `ufe_in.json` |
| `spiral_w.py` | Two-field Spiral Twist solver; validation; Ramos-Hamud mirror; scans; matter-like angle | `spiral_*.json` |
| `spiral_class_mirror.py` | AxiCLASS effective spiral against the solver | `spiral_class_mirror.json` |
| `forward_predictions.py` | Frozen predictions from the stored best fits | `forward_predictions.json` |
| `lowz_split.py` | DES Y5 supernova χ² split at z = 0.1 | `lowz_split.json` |

**Rules written before computing:** `PREREGISTRATION_UFE_CHECKS.md`, `PREREGISTRATION_SOLAR_LOWZ.md`.
**Predictions locked before the data:** `PREDICTIONS_LOCKED_2026-11-02.md`, with its SHA-256 in the `.sha256` file.

**Paths:** scripts that rebuild fits read `TWIST_AXI` (default: this repository's `cmb-fit/axiclass` inside WSL) and
`TWIST_RESULTS`. The pure-Python ones (`bi_kahler_lambda.py`, `solar_lowz.py`, `bi_superpotential.py`,
`ufe_checks.py`, `spiral_w.py`) need only numpy, scipy and sympy.
