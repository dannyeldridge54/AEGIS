"""Offline Star Mapper anomaly reports. Never starts scanners, downloads data, or fits models."""
import argparse
import csv
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

SCHEMA_VERSION = 4
REPORT_VERSION = "3.4"
ROOT = Path(__file__).resolve().parents[2]
REFERENCE_TOOLS = (
    {"name": "Gaia Archive", "url": "https://gea.esac.esa.int/archive/", "use": "Query Gaia DR3 source records and archive documentation."},
    {"name": "Gaia Archive Visualisation Service", "url": "https://www.cosmos.esa.int/web/gaia-users/archive/visualisation", "use": "Explore catalogue data with linked visualisation tools, including Aladin Lite and JS9."},
    {"name": "VizieR", "url": "https://vizier.cds.unistra.fr/", "use": "Search published astronomical catalogues and surveys; compare source records and catalogue measurements."},
    {"name": "SIMBAD", "url": "https://simbad.cds.unistra.fr/", "use": "Check literature cross-identifications, bibliography and compiled object properties; it is a literature database, not the source catalog."},
    {"name": "TOPCAT", "url": "https://www.star.bristol.ac.uk/~mbt/topcat/", "use": "Inspect, filter, join and plot astronomical tables; supports formats including CSV, VOTable and FITS."},
    {"name": "Astropy", "url": "https://docs.astropy.org/en/stable/", "use": "Python astronomy tools for units, coordinates, tables, time, statistics and file formats."},
    {"name": "GaiaUnlimited", "url": "https://gaiaunlimited.readthedocs.io/en/latest/", "use": "Survey/subsample selection functions and worked completeness examples; not applied by this report."},
)
CRITERIA = {
    "high_velocity": {
        "rule": "vtan_kms > 400",
        "definition": "4.74047 * hypot(pmra, pmdec) * dist_pc / 1000; Bailer-Jones distance when available, otherwise inverse parallax.",
        "confirm": "Obtain radial velocity and an orbit; propagate proper-motion and distance uncertainties.",
    },
    "astrometric_excess": {
        "rule": "ruwe > 1.4",
        "definition": "Poor single-star astrometric fit; not a detection of a companion.",
        "confirm": "Check Gaia DR3 NSS tables, binarity, crowding and astrometric systematics.",
    },
    "distance_mismatch": {
        "rule": "abs(1000/parallax - r_med_geo) > 3 * (r_hi_geo - r_lo_geo), with 0 < r_lo_geo <= r_med_geo <= r_hi_geo and r_hi_geo > r_lo_geo",
        "definition": "Distance consistency heuristic, NOT a calibrated 3-sigma test.",
        "confirm": "Check parallax zero-point, crowding and the distance posterior.",
    },
}
RESEARCH_CHANNELS = (
    {
        "name": "Galactic dynamics and high-velocity stars",
        "question": "How did the Milky Way assemble, and which stars warrant orbit follow-up?",
        "inputs_needed": "Full astrometric covariance, corrected parallax/distance posterior, reliable radial velocity, solar frame and Galactic potential with sensitivity checks.",
        "not_inferred": "A tangential-speed threshold does not establish escape probability, Galactic-centre origin, dark matter or torsion.",
        "references": [{"name": "GaiaUnlimited selection functions", "url": "https://gaiaunlimited.readthedocs.io/en/latest/"}],
    },
    {
        "name": "Unresolved binaries and compact companions",
        "question": "Is excess astrometric motion a companion, crowding or a systematic?",
        "inputs_needed": "Sky/crowding-dependent RUWE context, NSS quality/orbit checks, spectroscopy and independent orbit/mass constraints.",
        "not_inferred": "RUWE > 1.4 is neither a universal binary classifier nor a companion-mass measurement.",
        "references": [
            {"name": "GaiaUnlimited binary detectability", "url": "https://gaiaunlimited.readthedocs.io/en/latest/notebooks/dr3-unresolved-binaries.html"},
            {"name": "Gaia DR3 known issues", "url": "https://www.cosmos.esa.int/web/gaia/dr3-known-issues"},
        ],
    },
    {
        "name": "Asteroids and comets",
        "question": "Which known objects or unconfirmed tracklets need follow-up?",
        "inputs_needed": "Time-tagged multi-epoch astrometry, observatory location, calibrated errors, known-object ephemeris matching and orbit-fit validation.",
        "not_inferred": "Gaia star rows cannot discover moving objects; close approach is not impact probability or an alert.",
        "references": [
            {"name": "Gaia DR3 Solar System objects", "url": "https://www.cosmos.esa.int/web/gaia/dr3-solar-system-objects"},
            {"name": "MPC NEO confirmation page", "url": "https://www.minorplanetcenter.net/iau/NEO/toconfirm_tabular.html"},
            {"name": "JPL close-approach API documentation", "url": "https://ssd-api.jpl.nasa.gov/doc/cad.html"},
        ],
    },
    {
        "name": "Meteors and fireballs",
        "question": "Which atmospheric events have trajectories or possible source associations?",
        "inputs_needed": "Calibrated, synchronized camera observations, preferably multiple stations, atmospheric/trajectory uncertainties and completeness.",
        "not_inferred": "Published fireball records are not local detections; missing velocities cannot be replaced with zero or used for interstellar claims.",
        "references": [
            {"name": "Global Meteor Network", "url": "https://globalmeteornetwork.org/"},
            {"name": "JPL fireball API documentation", "url": "https://ssd-api.jpl.nasa.gov/doc/fireball.html"},
        ],
    },
    {
        "name": "Interstellar small bodies",
        "question": "Does a well-constrained orbit support an origin outside the Solar System?",
        "inputs_needed": "Extended observation arc, validated orbit/covariance, original barycentric orbit and perturbation/non-gravitational sensitivity; authoritative classification.",
        "not_inferred": "Large speed or a nominal eccentricity above one alone is not an interstellar classification.",
        "references": [{"name": "MPC orbit services", "url": "https://www.minorplanetcenter.net/mpcops/orbits/"}],
    },
    {
        "name": "Exoplanets",
        "question": "Which host systems have reliable planet evidence or interesting architectures?",
        "inputs_needed": "Reference-consistent planet/host parameters with uncertainties and dispositions; transit light curves or RV time series for new candidates, blend/activity vetting and selection modeling.",
        "not_inferred": "Gaia RUWE is not planet detection; archive PS rows repeat planets by reference, and PSCompPars values need not be mutually self-consistent.",
        "references": [{"name": "NASA Exoplanet Archive table definitions", "url": "https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html"}],
    },
    {
        "name": "Pulsars and neutron stars",
        "question": "Which timing/kinematic systems can constrain compact-object physics?",
        "inputs_needed": "Radio/high-energy counterpart identification, timing data/ephemeris and epoch, period derivatives, distance model and kinematic corrections.",
        "not_inferred": "An optical positional association is not pulsar detection; dispersion-measure distances are model dependent.",
        "references": [{"name": "ATNF Pulsar Catalogue", "url": "https://www.atnf.csiro.au/research/pulsar/psrcat/"}],
    },
    {
        "name": "Black holes and high-energy counterparts",
        "question": "Which systems have evidence for a dark compact companion or accretion?",
        "inputs_needed": "Ambiguity-aware epoch/proper-motion crossmatches, spectroscopy/orbits/inclination and dynamical mass constraints; multiwavelength diagnostics and literature evidence.",
        "not_inferred": "X-ray emission, positional coincidence or excess RUWE alone does not establish a black hole.",
        "references": [
            {"name": "HEASARC catalogue access", "url": "https://heasarc.gsfc.nasa.gov/W3Browse/"},
            {"name": "SIMBAD literature checks", "url": "https://simbad.cds.unistra.fr/"},
        ],
    },
)
LIMITATIONS = [
    "Flagged sources are candidates for follow-up, not discoveries.",
    "Report generation did not fetch measurements; the scanner may update local inputs independently. File modification times are local filesystem times, not observation or release dates.",
    "Gaia DR3 and Bailer-Jones 2021 are catalog releases; their distances share Gaia astrometry and are not independent measurements.",
    "Sweep totals are sums of persisted per-tile row counters, not a row-by-row audit of the large tile archive. Flags overlap; do not sum them as unique stars.",
    "The legacy random-patch summary is a separate, periodically saved snapshot that can lag its catalog CSV; patch encounters may repeat source IDs.",
    "Catalog values (RUWE, proper motions) and derived distances/speeds are distinguished in candidate rows. Stored rounded values are not reclassified.",
    "New scanner rows retain parallax error, proper-motion errors and their pairwise correlation, plus Bailer-Jones 16-84% distance bounds. Older rows may not contain these fields; the full five-parameter astrometric covariance is not retained and uncertainties are not propagated into calibrated significance.",
    "No matched control sample, selection correction, multiple-testing correction, or old-vs-new test is performed here. Flag fractions are descriptive only.",
    "Selection: scanner requests parallax_over_error > 5. Legacy random patches capped at 2000 rows can be truncated; do not infer sky density.",
    "Legacy random-patch summary and systematic HEALPix sweep are separate snapshots and must not be added, compared as one run, or cited as one count.",
    "ESA spot checks compare saved per-tile row counts with fresh archive counts; they do not revalidate individual source values or candidate classifications.",
]


def _utc(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()


def _source(path, root, content=None, hash_scope=None):
    stat = path.stat()
    result = {
        "path": str(path.relative_to(root)),
        "size_bytes": stat.st_size,
        "file_modified_utc": _utc(stat.st_mtime),
        "sha256": hashlib.sha256(content).hexdigest() if content is not None else None,
    }
    if content is None:
        result["hash_scope"] = hash_scope or "not hashed in full; only a bounded prefix is read"
    return result


def _json(content):
    def reject(value):
        raise ValueError(f"Non-finite JSON value: {value}")
    return json.loads(content, parse_constant=reject)


def _sweep_summary(content, out):
    state = _json(content)
    if not isinstance(state, dict):
        raise ValueError("Sweep state must be an object")
    level = state.get("level")
    if type(level) is not int or not 0 <= level <= 15:
        raise ValueError("Invalid sweep HEALPix level")
    done = state.get("done")
    if not isinstance(done, dict):
        raise ValueError("Sweep state done tiles must be an object")
    total_tiles = 12 * 4 ** level
    counts = {"stars": 0, "confirmed": 0, "flags": {}}
    tile_ids = set()
    for tile, data in done.items():
        try:
            tile_id = int(tile)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid sweep tile ID: {tile}") from None
        if str(tile_id) != str(tile) or not 0 <= tile_id < total_tiles or tile_id in tile_ids:
            raise ValueError(f"Invalid or duplicate sweep tile ID: {tile}")
        tile_ids.add(tile_id)
        if not isinstance(data, dict):
            raise ValueError(f"Invalid sweep tile record: {tile}")
        stars, confirmed = data.get("n"), data.get("conf")
        if type(stars) is not int or stars < 0 or type(confirmed) is not int or not 0 <= confirmed <= stars:
            raise ValueError(f"Invalid sweep tile counts: {tile}")
        flags = data.get("flags")
        if not isinstance(flags, dict):
            raise ValueError(f"Invalid sweep tile flags: {tile}")
        counts["stars"] += stars
        counts["confirmed"] += confirmed
        for flag, count in flags.items():
            if type(count) is not int or not 0 <= count <= stars:
                raise ValueError(f"Invalid sweep flag count: {tile}/{flag}")
            counts["flags"][flag] = counts["flags"].get(flag, 0) + count

    tiles_dir = out / "tiles" / f"L{level}"
    expected_files = {f"{tile:05d}.csv.gz" for tile in tile_ids}
    existing_files = {path.name for path in tiles_dir.glob("*.csv.gz")} if tiles_dir.is_dir() else set()
    latest = None
    recent_tiles = state.get("recent_tiles", [])
    if not isinstance(recent_tiles, list):
        raise ValueError("Sweep recent_tiles must be a list")
    timestamps = []
    for tile in recent_tiles:
        timestamp = tile.get("t") if isinstance(tile, dict) else None
        if type(timestamp) not in (int, float) or not math.isfinite(timestamp):
            raise ValueError("Invalid sweep tile timestamp")
        timestamps.append(timestamp)
    if timestamps:
        latest = _utc(max(timestamps))
    checks = state.get("checks", [])
    if not isinstance(checks, list):
        raise ValueError("Sweep spot checks must be a list")
    checked = []
    for check in checks:
        if not isinstance(check, dict):
            raise ValueError("Invalid sweep spot check")
        timestamp, tile_id = check.get("t"), check.get("tile")
        ours, esa, match = check.get("ours"), check.get("esa"), check.get("match")
        if type(timestamp) not in (int, float) or not math.isfinite(timestamp):
            raise ValueError("Invalid sweep spot-check timestamp")
        if type(tile_id) is not int or not 0 <= tile_id < total_tiles:
            raise ValueError("Invalid sweep spot-check tile")
        if type(ours) is not int or ours < 0 or type(esa) is not int or esa < 0:
            raise ValueError("Invalid sweep spot-check count")
        if type(match) is not bool or match != (ours == esa):
            raise ValueError("Inconsistent sweep spot-check result")
        checked.append({
            "checked_utc": _utc(timestamp), "tile": tile_id,
            "local_count": ours, "esa_count": esa, "match": match,
        })
    return {
        "status": "available",
        "mode": "systematic_healpix_sweep",
        "level": level,
        "tiles_done": len(tile_ids),
        "tiles_total": total_tiles,
        "complete": len(tile_ids) == total_tiles,
        "stars": counts["stars"],
        "confirmed": counts["confirmed"],
        "confirmed_frac": counts["confirmed"] / counts["stars"] if counts["stars"] else 0.0,
        "flags": counts["flags"],
        "latest_recorded_tile_utc": latest,
        "count_basis": (
            "Sum of persisted rows satisfying parallax_over_error > 5 in completed Gaia DR3 source_id HEALPix ranges. "
            "The ranges are non-overlapping; active tiles and incomplete work are excluded. "
            "Tile files are not fully reread by this report."
        ),
        "tile_files": {
            "expected_for_completed_tiles": len(expected_files),
            "present": len(expected_files & existing_files),
            "missing": len(expected_files - existing_files),
        },
        "spot_checks": {
            "retained": len(checked),
            "matched": sum(1 for check in checked if check["match"]),
            "mismatched": sum(1 for check in checked if not check["match"]),
            "latest_check_utc": checked[-1]["checked_utc"] if checked else None,
            "records": checked,
            "retention_basis": "All spot checks present in this run's sweep_state.json; older runs may retain only a bounded history.",
        },
    }


def _additional_local_datasets(root, sources, missing):
    impact_path = root / "research" / "impacts" / "craters.json"
    impact_result_path = impact_path.with_name("impact_result.json")
    impact = {"status": "unavailable", "input_path": str(impact_path.relative_to(root))}
    if impact_path.exists():
        impact_data = impact_path.read_bytes()
        sources.append(_source(impact_path, root, impact_data))
        rows = _json(impact_data)
        if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
            raise ValueError("Impact-structure catalog must be a list of records")
        impact.update(status="catalog_available", rows=len(rows))
        if impact_result_path.exists():
            result_data = impact_result_path.read_bytes()
            sources.append(_source(impact_result_path, root, result_data))
            result = _json(result_data)
            if not isinstance(result, dict) or result.get("n") != len(rows):
                raise ValueError("Impact analysis result does not match the local catalog")
            for key in ("Pbest", "R", "p"):
                value = result.get(key)
                if type(value) not in (int, float) or not math.isfinite(value):
                    raise ValueError(f"Invalid impact analysis result: {key}")
            impact.update(
                status="analysis_available",
                result={key: result[key] for key in ("n", "Pbest", "R", "p")},
            )
        else:
            missing.append(str(impact_result_path.relative_to(root)))
    else:
        missing.append(str(impact_path.relative_to(root)))

    exo_rows = root / "research" / "exoplanet_locks" / "exo_rows.json"
    exo_prereg = root / "research" / "exoplanet_locks" / "PREREG_EXO.md"
    exo_script = root / "research" / "exoplanet_locks" / "exo_test.py"
    for path in (exo_prereg, exo_script):
        if path.exists():
            sources.append(_source(path, root, path.read_bytes()))
    if exo_rows.exists():
        exo = {"status": "input_available", "input_path": str(exo_rows.relative_to(root))}
        sources.append(_source(exo_rows, root, exo_rows.read_bytes()))
    else:
        exo = {"status": "missing_input", "input_path": str(exo_rows.relative_to(root))}
        missing.append(str(exo_rows.relative_to(root)))
    return {
        "scope": "Separate local astronomy datasets; not merged into Gaia star classifications.",
        "impact_structures": impact,
        "exoplanet_periods": exo,
    }


def build_report(root=ROOT, max_rows=20000, outdir=None):
    """Inspect max_rows flag rows with one-row lookahead for truncation; preserve all inputs."""
    root = Path(root).resolve()
    if not 1 <= max_rows <= 20000:
        raise ValueError("max_rows must be between 1 and 20000")
    out = Path(outdir).resolve() if outdir is not None else root / "ufe-v2" / "cosmos_map"
    summary_path = out / "star_scan_summary.json"
    sweep_path = out / "sweep_state.json"
    catalog_path = out / "cosmos_map_stars.csv"
    summary = None
    sweep_summary = None
    sources, missing = [], []
    criteria_path = root / "ufe-v2" / "aegis" / "star_scanner.py"
    if criteria_path.exists():
        sources.append(_source(criteria_path, root, criteria_path.read_bytes()))
    else:
        missing.append(str(criteria_path.relative_to(root)))
    sweep_code_path = root / "ufe-v2" / "aegis" / "sweep.py"
    if sweep_code_path.exists():
        sources.append(_source(sweep_code_path, root, sweep_code_path.read_bytes()))
    else:
        missing.append(str(sweep_code_path.relative_to(root)))
    if summary_path.exists():
        content = summary_path.read_bytes()
        sources.append(_source(summary_path, root, content))
        summary = _json(content)
        if not isinstance(summary, dict):
            raise ValueError("Star summary must be an object")
        for key in ("stars", "confirmed", "patches"):
            if type(summary.get(key)) is not int or summary[key] < 0:
                raise ValueError(f"Invalid star summary count: {key}")
        if summary["confirmed"] > summary["stars"]:
            raise ValueError("Confirmed count exceeds star count")
        if not isinstance(summary.get("flags"), dict):
            raise ValueError("Star summary flags must be an object")
        for flag, count in summary["flags"].items():
            if type(count) is not int or not 0 <= count <= summary["stars"]:
                raise ValueError(f"Invalid star summary flag count: {flag}")
    else:
        missing.append(str(summary_path.relative_to(root)))

    if sweep_path.exists():
        content = sweep_path.read_bytes()
        sources.append(_source(sweep_path, root, content))
        sweep_summary = _sweep_summary(content, out)
    else:
        missing.append(str(sweep_path.relative_to(root)))

    catalog_source = None
    if catalog_path.exists():
        catalog_source = _source(catalog_path, root, hash_scope="metadata only; file contents were not read")
        sources.append(catalog_source)

    flags_path = out / "cosmos_map_flags.csv"
    candidates, counts = [], {}
    uncertainty_fields = ("parallax_error", "pmra_error", "pmdec_error", "pmra_pmdec_corr", "r_lo_geo", "r_hi_geo")
    uncertainty_rows = {field: 0 for field in uncertainty_fields}
    inspected, truncated = 0, False
    flag_source = None
    if flags_path.exists():
        flag_source = _source(flags_path, root)
        sources.append(flag_source)
        with flags_path.open(newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            required = {"source_id", "flags", "flag_notes"}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError("Mapper flags CSV requires source_id, flags and flag_notes")
            available_uncertainty_fields = sorted(set(uncertainty_fields) & set(reader.fieldnames or []))
            for row in reader:
                if inspected == max_rows:
                    truncated = True
                    break
                inspected += 1
                source_id = row.get("source_id") or ""
                if None in row or not source_id.isascii() or not source_id.isdigit() or row.get("flag_notes") is None:
                    raise ValueError(f"Malformed mapper flags row {inspected}")
                flags = list(dict.fromkeys(filter(None, (row.get("flags") or "").split(";"))))
                for flag in flags:
                    counts[flag] = counts.get(flag, 0) + 1
                for field in available_uncertainty_fields:
                    if row.get(field) not in (None, ""):
                        uncertainty_rows[field] += 1
                if flags and len(candidates) < 40:
                    candidates.append({
                        "source": "star", "id": row["source_id"], "time": None,
                        "flags": ";".join(flags), "flag_notes": row["flag_notes"],
                        "catalog_values": {k: row.get(k, "") for k in (
                            "ra", "dec", "l", "b", "ruwe", "pmra", "pmdec", "rv", "g_mag", "bp_rp",
                            "parallax_error", "pmra_error", "pmdec_error", "pmra_pmdec_corr",
                            "parallax", "ref_epoch", "astrometric_params_solved",
                            "nu_eff_used_in_astrometry", "pseudocolour", "ecl_lat",
                            "ra_error", "dec_error", "ra_dec_corr", "ra_parallax_corr",
                            "ra_pmra_corr", "ra_pmdec_corr", "dec_parallax_corr",
                            "dec_pmra_corr", "dec_pmdec_corr", "parallax_pmra_corr",
                            "parallax_pmdec_corr", "radial_velocity_error",
                        )},
                        "derived_values": {k: row.get(k, "") for k in (
                            "dist_pc", "dist_plx_pc", "dist_bj_pc", "r_lo_geo", "r_hi_geo", "vtan_kms", "l", "b",
                        )},
                        "uncertainty": "Raw Gaia parallax/proper-motion errors, pmRA-pmDec correlation and Bailer-Jones distance bounds are supplied when present. No full covariance propagation or calibrated significance is computed.",
                        "source_path": flag_source["path"],
                    })
    else:
        missing.append(str(flags_path.relative_to(root)))

    additional_local_datasets = _additional_local_datasets(root, sources, missing)
    patch_times = []
    for patch in (summary or {}).get("last_patches", []):
        timestamp = patch.get("t")
        if type(timestamp) not in (int, float) or not math.isfinite(timestamp):
            raise ValueError("Invalid recorded patch timestamp")
        patch_times.append(timestamp)
    latest = _utc(max(patch_times)) if patch_times else None
    stars = summary["stars"] if summary else None
    summary_source = next(
        (source for source in sources if source["path"] == str(summary_path.relative_to(root))),
        None,
    )
    legacy_snapshot = {
        "status": "available" if summary else "unavailable",
        "summary": summary,
        "count_basis": (
            "Legacy random-patch scanner's unique Gaia source IDs at its last summary save. "
            "The summary is written every 10 patches and can lag the catalog CSV; "
            "rechecked is attempted ID re-queries, not additional stars."
        ),
        "summary_file_modified_utc": summary_source["file_modified_utc"] if summary_source else None,
        "catalog_file_modified_utc": catalog_source["file_modified_utc"] if catalog_source else None,
        "catalog_newer_than_summary": (
            catalog_source["file_modified_utc"] > summary_source["file_modified_utc"]
            if catalog_source and summary_source else None
        ),
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "report_version": REPORT_VERSION,
        "run_id": out.name if out.parent.name == "runs" else "default",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "local_only_no_downloads_no_fits",
        "sources": sources,
        "missing_sources": missing,
        "freshness": {
            "catalog_versions": ["Gaia DR3", "Bailer-Jones et al. 2021 geometric distances"],
            "latest_recorded_patch_utc": latest,
            "latest_recorded_patch_scope": "Latest timestamp in saved last_patches only; not a catalog observation date or proof of a later full sweep.",
            "new_measurements_acquired": False,
            "status": "Report generation reads existing local files only; the scanner may update them independently. Latest recorded patch: " + (latest or "unknown"),
            "saved_summary_file_modified_utc": next(
                (source["file_modified_utc"] for source in sources if source["path"] == str(summary_path.relative_to(root))),
                None,
            ),
            "sweep_state_file_modified_utc": next(
                (source["file_modified_utc"] for source in sources if source["path"] == str(sweep_path.relative_to(root))),
                None,
            ),
        },
        "observational_evidence": {
            "status": "separate_sweep_and_legacy_snapshots" if sweep_summary and summary else (
                "sweep_state_available" if sweep_summary else (
                    "saved_summary_not_row_verified" if summary else "no_saved_summary"
                )
            ),
            "saved_star_summary": summary,
            "legacy_random_patch_snapshot": legacy_snapshot,
            "active_sweep_summary": sweep_summary,
            "flag_fractions_of_saved_stars": {
                flag: count / stars if stars else None for flag, count in (summary or {}).get("flags", {}).items()
            },
            "candidate_export": {
                "status": "available" if flag_source else "missing_not_zero_candidates",
                "rows_inspected": inspected, "row_limit": max_rows, "truncated": truncated,
                "flags_in_inspected_rows": counts, "rows": candidates,
                "uncertainty_fields": {
                    "available_in_csv": sorted(set(uncertainty_fields) & set(reader.fieldnames or []))
                    if flag_source else [],
                    "nonempty_rows_inspected": uncertainty_rows,
                    "count_basis": "Non-empty raw uncertainty fields among inspected flagged-export rows; blank legacy values are unavailable, not zero.",
                },
                "display_limit": 40, "order": "first flagged rows in file, not most recent or randomly sampled",
            },
        },
        "additional_local_datasets": additional_local_datasets,
        "reference_tools": REFERENCE_TOOLS,
        "research_channels": {
            "status": "reference_routes_only_no_catalog_ingestion_or_new_detection",
            "scope": "Research questions and follow-up requirements, not a survey of astronomer preferences. No object-type classifier, crossmatch, orbit fit, timing or light-curve analysis is performed.",
            "channels": RESEARCH_CHANNELS,
        },
        "anomaly_definitions_and_controls": {
            "criteria": CRITERIA,
            "criteria_source": "ufe-v2\\aegis\\star_scanner.py:assess",
            "controls": "No matched control sample, selection correction, multiple-testing correction, calibrated significance, or causal test is calculated.",
            "unknown_flags": sorted(
                set((summary or {}).get("flags", {}))
                .union((sweep_summary or {}).get("flags", {}), counts)
                - set(CRITERIA)
            ),
        },
        "limitations": LIMITATIONS,
    }


def to_markdown(report):
    obs = report["observational_evidence"]
    summary = obs["saved_star_summary"]
    sweep = obs.get("active_sweep_summary")
    legacy = obs.get("legacy_random_patch_snapshot", {})
    lines = [
        "# Local Star Mapper anomaly report", "",
        f"Generated: {report['generated_utc']} | run {report['run_id']} | "
        f"schema {report['schema_version']} | reporter {report['report_version']}",
        "", "## Dataset and freshness", "", report["freshness"]["status"], "",
        "Catalog inputs: Gaia DR3 source astrometry and Bailer-Jones et al. (2021) geometric-distance estimates. "
        "These estimates use Gaia astrometry and are not independent measurements.",
        f"Snapshot status: {obs['status']}. Sweep state file modified: "
        f"{report['freshness'].get('sweep_state_file_modified_utc') or 'unavailable'}.",
    ]
    if sweep is not None:
        lines += [
            "", "## Systematic HEALPix sweep snapshot", "",
            f"Completed tiles: {sweep['tiles_done']:,} / {sweep['tiles_total']:,}; "
            f"completed-tile source rows: {sweep['stars']:,}; "
            f"mapper distance-quality heuristic passed: {sweep['confirmed']:,}.",
            f"Count basis: {sweep['count_basis']}",
            f"Tile files present for completed tiles: {sweep['tile_files']['present']:,} / "
            f"{sweep['tile_files']['expected_for_completed_tiles']:,}; missing: {sweep['tile_files']['missing']:,}.",
            f"Latest recorded tile: {sweep['latest_recorded_tile_utc'] or 'unknown'}.",
            f"ESA tile-count checks retained: {sweep['spot_checks']['matched']:,} matched, "
            f"{sweep['spot_checks']['mismatched']:,} mismatched of {sweep['spot_checks']['retained']:,}; "
            f"latest check: {sweep['spot_checks']['latest_check_utc'] or 'none'}.",
            "Full check records are stored in the companion JSON and this run's sweep_state.json.",
        ]
        if sweep["flags"]:
            lines += [
                "", "Stored systematic-sweep flag counts (categories overlap; not unique stars):", "",
                "| Heuristic flag | Saved row count |", "| --- | ---: |",
            ]
            lines += [f"| {flag} | {count:,} |" for flag, count in sorted(sweep["flags"].items())]
    other = report["additional_local_datasets"]
    impact = other["impact_structures"]
    exo = other["exoplanet_periods"]
    lines += [
        "", "## Other local astronomy datasets (separate analyses)", "",
        f"Earth impact structures: {impact['status']}; records: {impact.get('rows', 'unavailable')}.",
    ]
    if impact.get("result"):
        result = impact["result"]
        lines.append(
            f"Pre-registered period scan summary: best period {result['Pbest']:.2f} Myr, "
            f"Rayleigh statistic {result['R']:.3f}, scan-corrected p={result['p']:.4f}; "
            "this is not evidence of a periodic impact signal."
        )
    lines += [
        f"Exoplanet period-ratio dataset: {exo['status']}; expected local input: `{exo['input_path']}`.",
        "These datasets are not merged with Gaia stars or plotted on the sky map; the exoplanet analysis is unavailable without its source rows.",
    ]
    if summary is not None:
        lines += ["", "## Legacy random-patch snapshot", "",
                  f"Unique source IDs at summary save: {summary['stars']:,}; mapper distance-quality heuristic passed: "
                  f"{summary['confirmed']:,}; patches: {summary['patches']:,}; rechecks attempted: "
                  f"{summary.get('rechecked', 'unavailable')}.",
                  f"Snapshot status: {legacy.get('status')}; catalog CSV newer than summary: "
                  f"{legacy.get('catalog_newer_than_summary')}.",
                  f"Count basis: {legacy.get('count_basis', 'Unavailable')}",
                  "This historical random-patch snapshot is a different scanner/data snapshot from the systematic sweep; do not compare or add the counts.",
                  "", "| Flag rule | Legacy saved count | Fraction of legacy saved stars |", "| --- | ---: | ---: |"]
        for flag, count in summary["flags"].items():
            fraction = obs["flag_fractions_of_saved_stars"][flag]
            lines.append(f"| {flag} | {count} | {fraction:.6%} |" if fraction is not None else f"| {flag} | {count} | unavailable |")
    elif sweep is None:
        lines += ["", "No saved scanner summary is available."]
    export = obs["candidate_export"]
    lines += ["", f"Candidate export: {export['status']}; rows inspected: {export['rows_inspected']}; truncated: {export['truncated']}.",
              "Candidate rows and recorded values are in the companion JSON (first 40, file order, not a random sample).",
              "", "## Anomaly definitions and controls", ""]
    for flag, criterion in report["anomaly_definitions_and_controls"]["criteria"].items():
        lines += [f"- **{flag}**: {criterion['rule']}. {criterion['definition']} Follow-up: {criterion['confirm']}"]
    lines += ["", report["anomaly_definitions_and_controls"]["controls"],
              "", "## Candidate rows", "",
              "Values below are copied from the first flagged rows in the local CSV, not a random sample. Stored flags are preserved and not recalculated."]
    uncertainty = export["uncertainty_fields"]
    lines += [
              "Uncertainty fields present in the inspected flagged export: "
              + (", ".join(uncertainty["available_in_csv"]) if uncertainty["available_in_csv"] else "none"),
              "Non-empty inspected rows by field: "
              + (", ".join(f"{key}={value}" for key, value in uncertainty["nonempty_rows_inspected"].items())
                 if uncertainty["nonempty_rows_inspected"] else "unavailable"),
              uncertainty["count_basis"],
    ]
    if export["rows"]:
              lines += ["", "| Gaia source ID | Flags | RA (deg) | Dec (deg) | RUWE | pmRA (mas/yr) | pmDec (mas/yr) | RV (km/s) | BJ distance (pc) | BJ 16-84% bounds (pc) | Parallax distance (pc) | Parallax error (mas) | Proper-motion errors (mas/yr) | pmRA-pmDec correlation | Tangential speed (km/s) |",
                        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
              for row in export["rows"]:
                  catalog, derived = row["catalog_values"], row["derived_values"]
                  lines.append("| " + " | ".join(
                      str("—" if value in (None, "") else value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")
                      for value in (
                      row["id"], row["flags"], catalog["ra"], catalog["dec"], catalog["ruwe"],
                      catalog["pmra"], catalog["pmdec"], catalog["rv"], derived["dist_bj_pc"],
                      f"{derived['r_lo_geo']}–{derived['r_hi_geo']}"
                      if derived["r_lo_geo"] not in (None, "") and derived["r_hi_geo"] not in (None, "") else "—",
                      derived["dist_plx_pc"], catalog["parallax_error"],
                      f"{catalog['pmra_error']} / {catalog['pmdec_error']}" if catalog["pmra_error"] not in (None, "") or catalog["pmdec_error"] not in (None, "") else "—",
                      catalog["pmra_pmdec_corr"], derived["vtan_kms"],
                  )) + " |")
              lines += ["", "Raw uncertainty inputs are for follow-up only; this report does not propagate them into a calibrated velocity interval, significance, or anomaly probability."]
    else:
        lines += ["", "No candidate rows are available in the local export."]
    lines += ["", "## Uncertainty and limitations", ""]
    lines += [f"- {text}" for text in report["limitations"]]
    lines += ["", "## Source provenance", "", "File times are not acquisition dates. SHA-256 identifies exact small source files; large candidate CSVs are not hashed in full.", ""]
    for source in report["sources"]:
        lines += [f"- `{source['path']}` | modified {source['file_modified_utc']} | {source['size_bytes']} bytes | SHA-256: {source['sha256'] or source.get('hash_scope', 'not computed')}"]
    lines += ["", "## Astronomy tools for independent follow-up", ""]
    lines += [f"- [{tool['name']}]({tool['url']}) — {tool['use']}" for tool in report["reference_tools"]]
    channels = report.get("research_channels")
    if channels:
        lines += ["", "## Research channels and missing evidence", "", channels["scope"]]
        for channel in channels["channels"]:
            lines += ["", f"### {channel['name']}", channel["question"],
                      f"Required inputs: {channel['inputs_needed']}",
                      f"Not inferred: {channel['not_inferred']}"]
            lines += [f"- [{item['name']}]({item['url']})" for item in channel["references"]]
    lines += ["", "Missing inputs (not zero results):"] + [f"- `{path}`" for path in report["missing_sources"]]
    return "\n".join(lines) + "\n"


def write_report(root=ROOT, max_rows=20000, outdir=None):
    """Create an immutable report pair; never update scanner evidence or a previous report."""
    root = Path(root).resolve()
    report = build_report(root, max_rows, outdir)
    out = Path(outdir).resolve() if outdir is not None else root / "ufe-v2" / "cosmos_map"
    reports = out / "anomaly_reports"
    reports.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    stem = f"anomaly_report_{stamp}_{uuid4().hex[:8]}"
    json_path, md_path = reports / (stem + ".json"), reports / (stem + ".md")
    with md_path.open("x", encoding="utf-8") as fh:
        fh.write(to_markdown(report))
    pending_path = json_path.with_suffix(".json.tmp")
    with pending_path.open("x", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, allow_nan=False)
        fh.write("\n")
    pending_path.rename(json_path)
    return json_path, md_path


def latest_report(outdir, markdown=False):
    """Read a completed report, without generating anything on an HTTP request."""
    paths = sorted(
        path for path in (Path(outdir) / "anomaly_reports").glob("anomaly_report_*.json")
        if path.with_suffix(".md").is_file()
    )
    if not paths:
        return None
    path = paths[-1].with_suffix(".md") if markdown else paths[-1]
    return path.read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-rows", type=int, default=20000, help="Bounded flag-row inspection (1..20000)")
    parser.add_argument("--outdir", default=os.environ.get("AEGIS_OUT_DIR"), help="Dataset run directory (defaults to cosmos_map)")
    args = parser.parse_args()
    for path in write_report(max_rows=args.max_rows, outdir=args.outdir):
        print(path)


if __name__ == "__main__":
    main()
