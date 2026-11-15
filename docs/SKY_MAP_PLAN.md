# Plan: one interactive AEGIS sky map (Job 9 — for Danny's approval)

**Goal:** a free web map that anyone (students, people at home) can open in a browser to explore the sky that
AEGIS has surveyed, see what the Star Mapper flagged, and help check it. Plan only; nothing gets built until you approve.

## What we already have (from docs/INVENTORY.md)
| Piece | Where | What it gives the map |
|---|---|---|
| Star Mapper sweep | `ufe-v2/` (runs on your PC) | 192,208,838 Gaia DR3 stars in 12,288 HEALPix level-5 tiles, every tile verified against ESA (STAR_AUDIT.md), plus anomaly flags |
| Cosmos Atlas | `apps/cosmos_atlas/index.html` | A working browser sky viewer (planets and Moon via astronomy-engine), "hunt" target lists, SIMBAD/VizieR fetchers |
| Sky Pointer | `apps/cosmos_atlas/sky_pointer.html` | Point-your-phone sky finder |
| CosmoExplorer | separate repo | Cosmology model explorer, a "how the universe expands" side panel, not a sky layer |

## Design
1. **One static web app, no server.** It loads as plain files, so it can be hosted free (GitHub Pages) and works offline once loaded.
2. **Sky engine: Aladin Lite v3** (CDS Strasbourg; open source, used by ESA and NASA archives). It draws the whole sky
   from HiPS tiles and already serves Gaia, 2MASS, Planck and other surveys, so we don't host imagery ourselves.
3. **Our layers, built from the Star Mapper data:**
   - a star-density map of the AEGIS sweep (a HEALPix map: a few MB, not the 192 million rows);
   - the anomaly flags as a small catalogue (position, flag type, status: candidate / rechecked / explained);
   - the hunt targets from Cosmos Atlas;
   - planets and Moon for tonight (astronomy-engine, already in Cosmos Atlas).
4. **Citizen-science view:** click a flag and you see the Gaia data, the reason it was flagged and the known
   explanations, then mark it "looks real / looks like an artefact". Votes are stored per flag (an artifact database or a
   small free backend). Flags stay labelled **candidates** until rechecked — nothing is presented as a discovery.
5. **Learn panel:** short pages on what Gaia measures, what a parallax is, and how AEGIS checks its own work (AION locks).

## Phases (each with a done-when)
| Phase | Work | Done when |
|---|---|---|
| A. Export | Script on your PC: Gaia tiles → HEALPix density map + flags catalogue (CSV/JSON) | Two files under 50 MB, counts match STAR_AUDIT.md |
| B. Prototype | Aladin Lite page with the density and flags layers, plus planets from Cosmos Atlas | Opens on a phone and a laptop; a flag click shows its data |
| C. Merge | Bring the Cosmos Atlas hunts and the Sky Pointer in as tabs; retire the nine fetch scripts into one | One page, one code path |
| D. Citizen review | Vote buttons + per-flag tallies; moderation by you | 20 test flags reviewed end to end |
| E. Release | Host on GitHub Pages; cite Gaia/ESA and CDS; your licence | Public link works; credits page complete |

## Decisions for you
- **Approve the plan** (or change the scope).
- **Hosting:** GitHub Pages (free, public) is the default.
- **Publishing flags:** OK to show the anomaly candidates publicly, clearly labelled as unconfirmed?
- **Licence** for the map code (same choice as the other tools).

## Costs and limits
Free hosting; Aladin Lite and astronomy-engine are free and open source. Phase A needs your PC (the raw tiles live
there). Gaia data use requires the standard ESA acknowledgement.
