"""Audit a Reading-B zero-coupling overlay against completed local Gaia sweep tiles.

This is a null/pipeline check, not a stellar-scale prediction or a test of AEGIS.
It reads completed tile files only and writes a timestamped report beside the run.
"""
import argparse
import csv
import gzip
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RUN_ID = "gaia-full-20261104T025414Z"
REQUIRED_FIELDS = {
    "source_id", "ra", "dec", "dist_pc", "dist_plx_pc", "dist_bj_pc",
    "pmra", "pmdec", "vtan_kms", "confirmed", "flags",
}


def _atomic_json(path, value):
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(value, fh, indent=2, sort_keys=True)
        fh.write("\n")
    os.replace(tmp, path)


def _tile_counts(path):
    counts = {"rows": 0, "confirmed": 0, "flags": {}}
    with gzip.open(path, "rt", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fields = set(reader.fieldnames or ())
        if not REQUIRED_FIELDS.issubset(fields):
            raise ValueError(f"{path.name}: missing required columns {sorted(REQUIRED_FIELDS - fields)}")
        for line, row in enumerate(reader, start=2):
            if None in row or not row.get("source_id"):
                raise ValueError(f"{path.name}: malformed CSV row {line}")
            counts["rows"] += 1
            counts["confirmed"] += row.get("confirmed") == "True"
            for flag in filter(None, (row.get("flags") or "").split(";")):
                counts["flags"][flag] = counts["flags"].get(flag, 0) + 1
    return counts


def _markdown(report):
    obs = report["gaia_snapshot"]
    verify = report["validation"]
    lines = [
        "# AEGIS Reading-B / Gaia side-by-side null overlay",
        "",
        f"Generated: {report['generated_utc']}",
        f"Gaia run: `{report['run_id']}` | state SHA-256: `{report['sweep_state_sha256']}`",
        "",
        "> **Interpretation:** this is a zero-coupling null/pipeline check, not a stellar-scale prediction, "
        "not a test of AEGIS, and not evidence for torsion or theory preference.",
        "",
        "## Side-by-side",
        "",
        "| Gaia Star Mapper baseline | AEGIS Reading-B overlay |",
        "| --- | --- |",
        "| Gaia DR3 astrometry, Bailer–Jones geometric distances, and existing catalog flags | "
        "Matter is blind to the dilaton by assumption; direct matter-force correction is exactly zero |",
        "| Measured catalog coordinates, distances, and proper motions remain the observations | "
        "No local stellar field profile or orbit equation is implemented, so the overlay makes no independent "
        "stellar prediction |",
        "| Existing heuristic flags are unchanged | "
        "Null overlay is identical to the baseline by construction; no Gaia values are changed |",
        "",
        "## Verified completed-tile snapshot",
        "",
        f"- Completed tiles in the captured sweep state: {obs['tiles_verified']:,} / {obs['tiles_total']:,} "
        f"({obs['sky_fraction']:.3%}).",
        f"- Gaia rows read and accounted for: {obs['rows_verified']:,}; distance-quality-pass heuristic rows: "
        f"{obs['confirmed_rows']:,}.",
        f"- Tile CSV row/count/flag mismatches: {verify['mismatched_tiles']:,}; "
        f"missing or unreadable completed tiles: {verify['failed_tiles']:,}.",
        f"- Sweep-state file modified: {obs['sweep_state_modified_utc']}.",
        "- Only tiles listed as completed in one atomic `sweep_state.json` snapshot were read. "
        "Active tiles were excluded; the live scanner and its catalog were not modified.",
        "",
        "Stored flag counts (categories overlap; not unique stars):",
        "",
        "| Heuristic flag | Verified rows |",
        "| --- | ---: |",
    ]
    lines.extend(f"| {name} | {count:,} |" for name, count in sorted(obs["flag_counts"].items()))
    lines.extend([
        "",
        "## Scientific boundary",
        "",
        "AEGIS `Reading B` sets matter coupling to zero by construction. The resulting zero direct-force correction "
        "is an assumption of that branch, not an observational result. Reading A has a separate scalar coupling "
        "and Cassini gate, but this repository does not provide a validated local field solution sourced by a star "
        "or a stellar-orbit prediction. Accordingly, no nonzero force, acceleration, orbit, or anomaly explanation "
        "is inferred here.",
        "",
        "The Gaia flags are candidate-screening heuristics. They do not measure torsion, validate the cosmological "
        "model, or establish that AEGIS outperforms another model.",
        "",
    ])
    return "\n".join(lines)


def build_report(run_id=DEFAULT_RUN_ID):
    run_dir = ROOT / "ufe-v2" / "cosmos_map" / "runs" / run_id
    state_path = run_dir / "sweep_state.json"
    state_bytes = state_path.read_bytes()
    state = json.loads(state_bytes)
    if not isinstance(state.get("done"), dict) or type(state.get("level")) is not int:
        raise ValueError("Sweep state must contain an integer level and completed-tile map")
    level = state["level"]
    done = state["done"]
    tile_dir = run_dir / "tiles" / f"L{level}"
    mismatches, failures, tile_rows = [], [], []
    totals = {"rows": 0, "confirmed": 0, "flags": {}}

    for tile_key, expected in sorted(done.items(), key=lambda item: int(item[0])):
        tile = int(tile_key)
        path = tile_dir / f"{tile:05d}.csv.gz"
        if not path.is_file():
            failures.append({"tile": tile, "reason": "completed tile file is missing"})
            continue
        try:
            actual = _tile_counts(path)
        except (OSError, EOFError, csv.Error, UnicodeError, ValueError) as exc:
            failures.append({"tile": tile, "reason": f"{type(exc).__name__}: {exc}"})
            continue

        expected_flags = expected.get("flags", {})
        differences = {}
        if actual["rows"] != expected.get("n"):
            differences["rows"] = {"state": expected.get("n"), "file": actual["rows"]}
        if actual["confirmed"] != expected.get("conf"):
            differences["confirmed"] = {"state": expected.get("conf"), "file": actual["confirmed"]}
        if actual["flags"] != expected_flags:
            differences["flags"] = {"state": expected_flags, "file": actual["flags"]}
        if differences:
            mismatches.append({"tile": tile, "differences": differences})

        totals["rows"] += actual["rows"]
        totals["confirmed"] += actual["confirmed"]
        for flag, count in actual["flags"].items():
            totals["flags"][flag] = totals["flags"].get(flag, 0) + count
        tile_rows.append({
            "tile": tile,
            "rows_verified": actual["rows"],
            "reading_b_direct_force_correction": "0 by assumption",
            "gaia_catalog_values_changed": 0,
            "state_mismatch": bool(differences),
        })

    tile_total = 12 * 32**2
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%S%fZ")
    report_dir = run_dir / "theory_null_overlay"
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / f"reading_b_null_overlay_{stamp}.json"
    md_path = report_dir / f"reading_b_null_overlay_{stamp}.md"
    report = {
        "schema_version": 1,
        "analysis": "AEGIS Reading-B zero-coupling Gaia null overlay",
        "run_id": run_id,
        "generated_utc": now.isoformat(),
        "mode": "offline_read_only_completed_tiles",
        "sweep_state_sha256": hashlib.sha256(state_bytes).hexdigest(),
        "theory": {
            "branch": "Spiral Twist Reading B",
            "matter_dilaton_coupling": 0.0,
            "direct_matter_force_correction": 0.0,
            "status": "zero by construction; assumption/null check, not a stellar-scale test",
            "validated_local_stellar_field_solution": False,
            "validated_stellar_orbit_prediction": False,
        },
        "gaia_snapshot": {
            "catalog": "Gaia DR3; Bailer-Jones et al. (2021) geometric distances",
            "selection": "Completed non-overlapping Gaia DR3 source_id HEALPix tile files only",
            "tiles_total": tile_total,
            "tiles_in_sweep_state": len(done),
            "tiles_verified": len(tile_rows),
            "sky_fraction": len(done) / tile_total,
            "rows_verified": totals["rows"],
            "confirmed_rows": totals["confirmed"],
            "flag_counts": totals["flags"],
            "sweep_state_modified_utc": datetime.fromtimestamp(
                state_path.stat().st_mtime, timezone.utc
            ).isoformat(),
        },
        "comparison": {
            "baseline": "Observed Gaia catalog values and existing heuristic flags",
            "reading_b_overlay": "Same catalog values; no direct matter-force correction",
            "per_star_catalog_changes": 0,
            "interpretation": "Identical output follows from the zero-coupling assumption and is not independent predictive agreement.",
        },
        "validation": {
            "mismatched_tiles": len(mismatches),
            "failed_tiles": len(failures),
            "mismatches": mismatches,
            "failures": failures,
            "tiles": tile_rows,
        },
        "limitations": [
            "Reading B sets the direct matter coupling to zero by assumption.",
            "No validated local stellar field profile or stellar-orbit equation is supplied by this repository.",
            "Anomaly flags are catalog-screening heuristics and are not torsion detections.",
            "Completed-tile counts are not a full-sky result; active tiles were excluded.",
        ],
    }
    _atomic_json(json_path, report)
    md_path.write_text(_markdown(report), encoding="utf-8", newline="\n")
    return report, json_path, md_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    args = parser.parse_args()
    report, json_path, md_path = build_report(args.run_id)
    print(json.dumps({
        "run_id": report["run_id"],
        "rows_verified": report["gaia_snapshot"]["rows_verified"],
        "tiles_verified": report["gaia_snapshot"]["tiles_verified"],
        "mismatched_tiles": report["validation"]["mismatched_tiles"],
        "failed_tiles": report["validation"]["failed_tiles"],
        "json_report": str(json_path.relative_to(ROOT)),
        "markdown_report": str(md_path.relative_to(ROOT)),
    }, indent=2))
    if report["validation"]["mismatched_tiles"] or report["validation"]["failed_tiles"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
