# Deviation from docs/STAR_MAPPER_DR4_PLAN.md — DR4 code written before the DR4 data model is public

Date: 18 Nov 2026 (CT). Decision: Danny, "Mapper = full development now" (overrides the plan's "no coding blind" line).

What changed (ufe-v2/aegis): plan steps 1–3 implemented as settings in `gaia_release.py`, wired into
`sweep.py`, `star_scanner.py`, `validation_collect.py`.
- Step 1 table: `AEGIS_GAIA_TABLE` (default `gaiadr3.gaia_source`).
- Step 2 distances: `AEGIS_DIST_TABLE=none` → no Bailer-Jones join, `r_*_geo` selected as NULL, every star flagged
  `distance_parallax_only`.
- Step 3 columns: `AEGIS_GAIA_MISSING` → those columns selected as NULL, never guessed.

Guarantees, tested (ufe-v2/tests/test_gaia_release.py):
- With no settings, every query is byte-identical to the frozen DR3 reference run (checked against a snapshot).
- DR4 mode contains no `gaiadr3`/`gaiaedr3` reference.

Still assumptions until 2 Dec 2026 (ESA archive offline 25 Nov – 2 Dec):
- The DR4 table name `gaiadr4.gaia_source`, the column names, and whether `source_id` keeps the HEALPix-5 encoding
  the tiling relies on. Check all three against the published DR4 data model before the first DR4 query.
- No DR4 query is run and no DR4 result is claimed from this code before then. Steps 4–5 (ESA spot checks, new
  discovery category) still wait for the data model and need their own lock.
