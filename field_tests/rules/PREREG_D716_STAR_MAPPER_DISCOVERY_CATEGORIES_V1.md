# PREREG D716: Star Mapper discovery categories v1
Locked 2026-11-15 before computing. Script: ufe-v2/aegis/discoveries.py. Output: apps/skymap/data/aegis_discoveries.json.

## Question
Fix, before they are run on the real 192-million-star sweep, the rules that sort Star Mapper stars into 'interesting' categories for the AEGIS Sky Map and for follow-up. This is a classification, not a hypothesis test: no category is a claim of discovery; every entry is a candidate.

## Inputs (fixed now)
- Rules (per star, from the Star Mapper tile columns; M_G = g_mag + 5 − 5 log10(dist_pc), no extinction correction; only stars with astrometric_quality_pass = True unless stated):
  1. nearby: dist_pc ≤ 20.
  2. white_dwarf_candidate: bp_rp < 1.2 and M_G > 3.3·bp_rp + 9.5 (below the main sequence).
  3. luminous_giant: M_G < −2.0 (bright giants and supergiant candidates; extinction makes this a lower bound on luminosity).
  4. fast_mover: total proper motion √(pmra² + pmdec²) > 1000 mas/yr.
  5. hypervelocity_candidate: heliocentric speed > 600 km/s, using √(vtan² + rv²) when rv exists, else vtan (labelled 'tangential only').
  6. strong_wobble: RUWE > 10 (all stars, quality flag ignored, since a large RUWE fails the quality cut by construction).
  7. very_red: bp_rp > 4.0.
  Ranking for the map (top 5,000 per category): nearby by distance; white dwarfs by M_G − (3.3·bp_rp + 9.5) descending; giants by M_G ascending; fast movers and hypervelocity by speed; strong_wobble by RUWE; very_red by bp_rp.
- Data: AEGIS Star Mapper tiles (ufe-v2 cosmos_map/tiles/L5/*.csv.gz), Gaia DR3 with Bailer-Jones distances; columns as in ufe-v2/aegis/star_scanner.py STAR_FIELDS.

## Method
Stream every tile once; count every category; keep the top 5,000 per category by the ranking above; write per-category counts and lists to apps/skymap/data/aegis_discoveries.json. Unit tests on synthetic rows check every rule boundary before the real run.

## Decision rule (written before running)
- PASS (sanity, not science) if: on the real sweep, nearby ≥ 1 known neighbour (e.g. Gaia DR3 counterparts of Barnard's Star or Proxima if in the swept tiles) is recovered; counts are reported in full whatever they are.
- FAIL if: a rule produces > 10% of all stars in any category except strong_wobble's quality-free definition (would mean a coding error).
- What happens if the run crashes or times out: fixes only through D716_DEVIATIONS.md, written before any rerun.

## Labels
Mark every number in the write-up as computed / estimate / literature / from memory.
