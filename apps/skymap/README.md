# AEGIS Sky Map

A free, interactive map of the whole sky for classrooms and curious people. Open it in a browser and you can:

- **Look at real telescope surveys** of the entire sky — visible light, infrared, microwaves (Planck), gamma rays (Fermi), and the
  Gaia map of 1.8 billion stars — and switch between them on the same patch of sky.
- **Find things**: 88 constellations with their figures and names, 378 named stars, all 110 Messier galaxies, nebulae and
  clusters, and the Sun, Moon and planets where they are right now (or at any date you choose).
- **See tonight's sky** for your town: which planets are up, when they rise and set, how full the Moon is.
- **Take a 10-stop guided tour** (Orion, a star nursery, the galactic centre in infrared, Andromeda, the microwave sky…).
- **Learn**: six short lessons and three ready-to-run classroom activities.
- **Help check real data**: the AEGIS Star Mapper re-verified 192,208,838 Gaia stars against ESA's archive and flags unusual
  ones. Students open a flagged star, read why it was flagged, and record their own review (kept on the device; exportable as CSV).

No accounts, no tracking, no ads. Works on Chromebooks, Windows, Mac, iPad and phones, and installs as an app.

![Whole-sky view with constellations, named stars, Messier objects and planets (telescope imagery streams in underneath when online)](docs/screenshot-wholesky.png)

## Start it
- **Quickest:** double-click `START_SKY_MAP.bat` (Windows) or run `sh start_sky_map.sh` (Mac/Linux). Needs Python 3, nothing else.
- **For a whole school:** put this folder on any web server or school intranet, or host it free on GitHub Pages. See [INSTALL.md](INSTALL.md).
- Teachers: see [TEACHERS.md](TEACHERS.md).

The app itself works offline once loaded. The telescope pictures stream from the CDS archive in Strasbourg, so they need internet;
without it, the drawn layers (constellations, stars, Messier objects, planets, AEGIS stars), Tonight, Tour and Learn still work.

## Adding the AEGIS survey layers
On the computer that runs the Star Mapper:
```
python apps/skymap/tools/export_from_sweep.py --cosmos-map ufe-v2/cosmos_map --out apps/skymap/data
```
This writes `data/aegis_coverage.json` (sky coverage and density) and `data/aegis_flags.json` (all high-velocity and
distance-mismatch stars and the strongest RUWE stars, with the criteria). Flags are always shown as candidates, not discoveries.

## For developers
Plain HTML, CSS and ES modules, no build step. `vendor/` holds Aladin Lite 3.8.2 (CDS, LGPL-3) and astronomy-engine 2.1.19 (MIT);
`tools/build_reference_data.py` rebuilds the constellation/star/Messier files from d3-celestial (BSD-3).
Tests: `pytest apps/skymap/tests` (the browser test needs Playwright). Release zip: `python tools/package_release.py`.

## Licence
AGPL-3.0-or-later — free for schools, students and everyone ([LICENSE](LICENSE)); commercial licence for organisations that
don't want the AGPL's obligations ([COMMERCIAL.md](COMMERCIAL.md)). Third-party parts: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
© 2026 Danny Lee Eldridge. Built with AI assistance (Claude, Anthropic).
