# Star Mapper: Gaia DR4 sweep plan (prepared 15 Nov 2026; DR4 due Wed 2 Dec 2026)

Source: ESA Gaia news 2026: "Gaia DR4 is planned for Wednesday, 2 December 2026"; it covers the first 5.5 years of observations. Contents are not confirmed here yet (source counts, column names).

## Principles
- The DR3 sweep (12,288 tiles, 192,208,838 stars, 200/200 ESA checks) stays frozen as the reference run. DR4 runs as a separate run: `AEGIS_RUN_ID=dr4` writes to `cosmos_map/runs/dr4/`.
- Lock the DR4 rules first: same tiling (HEALPix level 5 via source_id ranges, if DR4 keeps that encoding), same `parallax_over_error > 5` cut, and the same D716 discovery categories. Write a `PREREG_D###_STAR_MAPPER_DR4` lock before the first DR4 query.
- No coding blind. Code changes wait until the DR4 archive tables and documentation are public.

## Code changes needed on release day (all in ufe-v2/aegis)
1. Table names: `gaiadr3.gaia_source` appears in `sweep.py` (lines 36, 43), `star_scanner.py` (65–73) and `validation_collect.py` (41, 47). Make it a setting (`AEGIS_GAIA_TABLE`, default DR3).
2. Distances: the Bailer-Jones `external.gaiaedr3_distance` join has no DR4 counterpart at release. Use parallax-only distances, flagged as such, until a DR4 distance catalogue appears.
3. Columns: check every name in `COLS` against the DR4 data model (e.g. `radial_velocity`, `ruwe`, `nu_eff_used_in_astrometry`). Missing columns become NULL, never a guess.
4. ESA spot checks: point them at the DR4 table.
5. New in DR4 (expected: epoch astrometry and photometry, exoplanet and binary candidates): consider a new discovery category, written into a new lock before use.

## Load and cost
The DR3 sweep took weeks on Danny's PC. The DR4 query volume per tile will be larger, so it runs at the same polite rate (2 workers). Run it overnight. Fans: it will work the CPU, and it stops when the window is closed.

## Update 18 Nov 2026 (D1330; source: ESA Gaia news 2026)
- Date confirmed: ESA's 8 Oct 2026 notice says the archive is **offline 25 Nov to 2 Dec 2026** and comes back on 2 Dec with DR4.
  - Any DR3 query (Mapper top-ups, ESA spot checks) must finish before 25 Nov or wait until 2 Dec.
- Archive release (14 Oct 2026): **max 5 concurrent jobs per user**. The planned 2 workers fit.
  - DataLink structures are renamed: RAW → DATAMODEL_GAIA, INDIVIDUAL → DATAMODEL_STANDARD. The AEGIS cloud tree does not use DataLink; check the PC tree (ufe-v2/aegis) before any epoch-data pull.
- Still no public DR4 data model, so the rule "no coding blind" stands.
