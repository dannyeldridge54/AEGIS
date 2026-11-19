"""Which Gaia release the Mapper queries (DR4 prep, Danny 18 Nov 2026: "full development now").

Defaults reproduce the frozen DR3 reference run byte for byte. Every DR4 setting below is an ASSUMPTION until the
DR4 data model is public (2 Dec 2026); see field_tests/rules/PREREG_STAR_MAPPER_DR4_DEVIATIONS.md.

  AEGIS_GAIA_TABLE    main source table          default gaiadr3.gaia_source   (DR4 guess: gaiadr4.gaia_source)
  AEGIS_DIST_TABLE    distance catalogue to join default external.gaiaedr3_distance; "none" = parallax-only
  AEGIS_GAIA_MISSING  comma list of columns the release lacks -> selected as NULL (never guessed)
  AEGIS_GAIA_LABEL    release name used in flag text, default "Gaia DR3"
"""
import os

DIST_COLS = ("r_med_geo", "r_lo_geo", "r_hi_geo")


def table():
    return os.environ.get("AEGIS_GAIA_TABLE", "gaiadr3.gaia_source")


def label():
    return os.environ.get("AEGIS_GAIA_LABEL", "Gaia DR3")


def dist_table():
    t = os.environ.get("AEGIS_DIST_TABLE", "external.gaiaedr3_distance").strip()
    return None if t.lower() in ("", "none", "off") else t


def missing():
    return {c.strip() for c in os.environ.get("AEGIS_GAIA_MISSING", "").split(",") if c.strip()}


def col(name, prefix="g."):
    """One source column, or NULL AS name when the release lacks it."""
    return f"NULL AS {name}" if name in missing() else f"{prefix}{name}"


def select(fields, prefix="g."):
    return ", ".join(col(f, prefix) for f in fields)


def dist_select():
    if dist_table():
        return ", ".join(f"d.{c}" for c in DIST_COLS)
    return ", ".join(f"NULL AS {c}" for c in DIST_COLS)


def dist_join():
    t = dist_table()
    return f"LEFT OUTER JOIN {t} AS d ON g.source_id = d.source_id " if t else ""


def parallax_only():
    return dist_table() is None
