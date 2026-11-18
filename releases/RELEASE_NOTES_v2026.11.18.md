## AEGIS release 2026.11.18: public toolkits

**Quick start**
```
git clone https://github.com/dannyeldridge54/AEGIS && cd AEGIS
pip install -r requirements-tools.txt
python tools/release_smoketest.py      # 11/11 checks against published values, about 2 s
```

**Included**
- **CERN+1** (`tools/lhc`): an independent wino LHC toolkit, not affiliated with or endorsed by CERN.
  - Cross sections at any energy, by two routes that agree to 1%.
  - A mass-dependent chargino lifetime engine.
  - A disappearing-track recast with a computed boost distribution: 661.5 ± 10 GeV vs ATLAS 660 GeV (136 fb⁻¹); 446.6 GeV vs 460 GeV (36 fb⁻¹).
  - Exact-Poisson and pyhf CLs.
  - Theory bands.
  - HL-LHC, HE-LHC and FCC-hh reach.
  - Self-tests.
- **Lattice Lab** (`tools/lattice/lattice_lab.py`): Gaussian and Epstein energies, duality flips, theta series and modular forms, and hexagonal and square planes, from d=2 to d=24 (E8, BW16, Leech).
- **Janus calculator** (`tools/janus_calc`): exact numerical n_s, r and α_s for any potential. It is also released on its own as [janus-string-calculator v1.3](https://github.com/dannyeldridge54/janus-string-calculator).
- **Hyperion** (`tools/janus_astro`): Big Bang helium and deuterium (PRIMAT tables; `aegis hyperion bbn`), 3-billion-year Milky Way star orbits in McMillan17 or MWPotential2014 (`aegis hyperion orbit`), and the Star Mapper orbit feed.
- **Inflation Scorecard** (`tools/scorecard`): scores any (n_s, r, α_s) against every current CMB and large-scale-structure constraint, with sources (`aegis scorecard`).
- **One program for everything**: `aegis` (menu when double-clicked; Windows, macOS and Linux builds attached to this release). Plain-language errors for bad input. Tests for every toolkit run on each push (CERN+1 21, Lattice Lab 5, smoke test 11).
- **Papers**, all refereed on 18 Nov: CERN+1 v2, Lattice Champions, Shape–Scale–Duality, SERAPIS-E v2, Twist-2 v2, CubeMind interim evaluation, Lock v2. Each lists its pre-registered tests and its failures.

**License (new from this release):** the AEGIS Community License.
- Free for individuals, scientists, students, schools, nonprofits and public research.
- Any business or for-profit use, including internal R&D, needs the AEGIS Commercial License (`licensing/COMMERCIAL_LICENSE.md`): a yearly minimum or a share of group profit, plus an executive-pay surcharge above $50M revenue.
- No military or mass-surveillance use.
- Earlier releases keep their original licenses.

**Support:** all of this is built by one person, Danny Eldridge, with the help of AI. To donate, email dannyeldridge54@gmail.com.
