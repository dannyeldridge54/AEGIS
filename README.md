# AEGIS — SERAPIS modular inflation, and tools for honest computational research

Independent research by Danny Lee Eldridge (Oklahoma City), carried out with substantial AI assistance (Claude, Anthropic).
Every computation is pre-registered: the rule is written, hashed and committed before anything runs.

## The science: SERAPIS
A modular-invariant inflation model in which the inflaton is the shape modulus τ of a string-theory torus, with its
vacuum at a symmetric point (τ = i or the hexagonal point ρ). Frozen predictions: n_s = 0.970–0.975,
r ≈ (4.6–5.7)×10⁻⁴, α_s ≈ −(8.5–10.6)×10⁻⁴, plus a parameter-free consistency relation (the Janus relation).

- Paper: [papers/v3/serapis_v3.pdf](papers/v3/serapis_v3.pdf) · Zenodo v3.1: doi:10.5281/zenodo.24281771 (v3: 10.5281/zenodo.24250733)
- One-page prediction sheet: [papers/v3/prediction_sheet.md](papers/v3/prediction_sheet.md)
- Research notes (D-notes): [theory/pending_docs/D72_D75_weak_spots.md](theory/pending_docs/D72_D75_weak_spots.md); index: docs/D_INDEX.md
- Locked rules: [field_tests/rules/](field_tests/rules/) · results: [field_tests/results/](field_tests/results/)
- Current state: [papers/v3/CURRENT_STATE_PROJECT.md](papers/v3/CURRENT_STATE_PROJECT.md)

## Tools (see [TOOLS.md](TOOLS.md))
- **AION** — pre-registration kit: `aion new / lock / deviate / check` ([tools/aion](tools/aion)). Audit of this repo: [docs/AION_AUDIT.md](docs/AION_AUDIT.md).
- **Star Mapper** — Gaia DR3 sweeps and anomaly scanning ([ufe-v2](ufe-v2)); **Cosmos Atlas** sky viewer ([apps/cosmos_atlas](apps/cosmos_atlas)).
- **CMB-fit pipeline** — CAMB/AxiCLASS fits used for the earlier Twist tests ([cmb-fit](cmb-fit)).
- More in progress: Inflation Scorecard, Janus Calculator, SERAPIS prediction tracker.

## Check the work
`sh check_my_work.sh` (Mac/Linux) or `CHECK_MY_WORK.bat` (Windows) re-derives the numbers; `aion check` verifies lock order.

## Earlier work
The Twist / torsion-cosmology tests (2025–Nov 2026) and the TypeScript agent are in [archive/](archive/README.md).
The clean Twist release: [the-twist-torsion-cosmology](https://github.com/dannyeldridge54/the-twist-torsion-cosmology).

Licence: see [LICENSE](LICENSE) (Hippocratic License 3.0, HL3-MIL-SV, for this repository).
