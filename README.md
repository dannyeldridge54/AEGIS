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

## Quick start: the public toolkits (release 2026.11.18)
```
git clone https://github.com/dannyeldridge54/AEGIS && cd AEGIS
pip install -r requirements-tools.txt        # Python 3.10+
python tools/release_smoketest.py            # 9 checks against published values, ~2 s
```
- **CERN+1** ([tools/lhc](tools/lhc), [README](tools/lhc/README.md), [user guide](tools/lhc/USER_GUIDE.md)) — independent wino LHC toolkit: cross sections at any energy, mass-dependent lifetimes, a disappearing-track recast that reproduces two ATLAS limits, exact-Poisson and pyhf CLs, theory bands, future-collider reach. Not affiliated with or endorsed by CERN.
- **Lattice Lab** ([tools/lattice/lattice_lab.py](tools/lattice/lattice_lab.py)) — lattice energies, duality flips, theta series, Epstein zeta, hexagonal/square planes from d=2 to d=24 (E8, BW16, Leech). Run `python -m tools.lattice.lattice_lab` for commands.
- **Janus calculator** ([tools/janus_calc](tools/janus_calc)) — exact numerical inflation observables (n_s, r, α_s) for any potential; also released at [janus-string-calculator](https://github.com/dannyeldridge54/janus-string-calculator).

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

## License
**AEGIS Community License** ([LICENSE](LICENSE)): free for individuals, scientists, students, schools, nonprofits and public research.
Any business or for-profit use, including internal R&D, needs the **AEGIS Commercial License** ([licensing/COMMERCIAL_LICENSE.md](licensing/COMMERCIAL_LICENSE.md)): a yearly minimum or a share of group profit, rising with company size. No military, mass-surveillance or organized-religion use at any price.
Versions released before 18 November 2026 keep the license they were released under (HL3-MIL-SV).

## Support this work

> In a world of painted walls and borrowed light,
> where lies wear crowns and illusions call themselves the sky,
> this work is a lantern, not a throne.
> It belongs to the one who asks, who measures, who will not kneel:
> take it, test it, and see for yourself.
> It was made for freedom, the quiet kind, the kind no one can sell you.

All of this (the research, the toolkits and the papers) is built by one person, Danny Eldridge, an independent, self-taught researcher in Oklahoma City, working with the help of AI. He is trying to change his circumstances in life, and he promises to keep doing what he is doing now: releasing the work openly, free to individuals, scientists and students, and using it to try to make the world a better place. If it helps you, a donation of any size keeps it going: **email dannyeldridge54@gmail.com to donate** (a direct donation link is coming). Businesses: please license through the AEGIS Commercial License instead.
