"""Offline matched-control summaries for completed Star Mapper Gaia DR3 sweeps.

This module reads archived tile CSVs only. It never queries the Gaia Archive,
starts a scanner, or fits the AEGIS cosmology model.
"""
import argparse
import csv
import gzip
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from aegis.anomaly_report import _sweep_summary
from aegis.star_scanner import ASTROMETRY_FIELDS

ROOT = Path(__file__).resolve().parents[2]
FLAGS = ("astrometric_excess", "high_velocity", "distance_mismatch")
REQUIRED_FIELDS = {
    "source_id", "g_mag", "bp_rp", "parallax_error", "dist_plx_pc",
    "dist_pc", "dist_bj_pc", "r_lo_geo", "r_hi_geo", "vtan_kms", "ruwe", "flags",
}
MAG_BIN = 0.5
COLOR_BIN = 0.5
SNR_EDGES = (5, 10, 20, 50, 100)
DISTANCE_DEX_BIN = 0.25


def _finite(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _fixed_bin(value, width):
    number = _finite(value)
    return None if number is None else math.floor(number / width)


def _log_bin(value, dex_width=DISTANCE_DEX_BIN):
    number = _finite(value)
    if number is None or number <= 0:
        return None
    return math.floor(math.log10(number) / dex_width)


def _snr_bin(row):
    distance = _finite(row.get("dist_plx_pc"))
    error = _finite(row.get("parallax_error"))
    if distance is None or distance <= 0 or error is None or error <= 0:
        return None
    snr = 1000.0 / distance / error
    if not math.isfinite(snr) or snr < 5:
        return None
    for index, edge in enumerate(SNR_EDGES[1:]):
        if snr < edge:
            return index
    return len(SNR_EDGES) - 1


def _stratum(flag, row, tile_id):
    g_bin = _fixed_bin(row.get("g_mag"), MAG_BIN)
    color_bin = _fixed_bin(row.get("bp_rp"), COLOR_BIN)
    snr_bin = _snr_bin(row)
    if None in (g_bin, color_bin, snr_bin):
        return None
    parts = [tile_id, g_bin, color_bin, snr_bin]
    if flag == "high_velocity":
        distance_bin = _log_bin(row.get("dist_pc"))
        if distance_bin is None:
            return None
        parts.append(distance_bin)
    elif flag == "distance_mismatch":
        distance_bin = _log_bin(row.get("dist_bj_pc"))
        lower = _finite(row.get("r_lo_geo"))
        upper = _finite(row.get("r_hi_geo"))
        median = _finite(row.get("dist_bj_pc"))
        if (distance_bin is None or lower is None or upper is None or median is None
                or lower <= 0 or upper <= lower or not lower <= median <= upper):
            return None
        width_bin = _fixed_bin((upper - lower) / median, 0.1)
        parts.extend((distance_bin, width_bin))
    return tuple(parts)


def _hash_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def build_summary(run_dir, allow_partial=False):
    """Build deterministic matched-stratum counts from one archived sweep.

    Controls are rows with no scanner flag of any kind. Each target flag is
    compared only within the same tile and fixed photometry/SNR strata. This
    returns descriptive matched counts, not significance or corrected rates.
    """
    run_dir = Path(run_dir).resolve()
    state_path = run_dir / "sweep_state.json"
    if not state_path.is_file():
        raise ValueError(f"Missing sweep state: {state_path}")
    state_bytes = state_path.read_bytes()
    state = json.loads(state_bytes, parse_constant=lambda value: (_ for _ in ()).throw(
        ValueError(f"Non-finite JSON value: {value}")))
    if not isinstance(state, dict):
        raise ValueError("Sweep state must be an object")
    level = state.get("level")
    if type(level) is not int or not 0 <= level <= 15:
        raise ValueError("Invalid sweep HEALPix level")
    total_tiles = 12 * 4 ** level
    done = state.get("done")
    if not isinstance(done, dict):
        raise ValueError("Sweep state done tiles must be an object")
    _sweep_summary(state_bytes, run_dir)
    tile_ids = []
    for raw_id in done:
        try:
            tile_id = int(raw_id)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid tile ID: {raw_id}") from None
        if str(tile_id) != str(raw_id) or not 0 <= tile_id < total_tiles:
            raise ValueError(f"Invalid tile ID: {raw_id}")
        tile_ids.append(tile_id)
    tile_ids.sort()
    if not allow_partial and len(tile_ids) != total_tiles:
        raise ValueError(
            f"Scientific matched-control run requires a complete sweep: {len(tile_ids)} of {total_tiles} tiles"
        )
    if not tile_ids:
        raise ValueError("Sweep has no completed tiles")

    tile_root = run_dir / "tiles" / f"L{level}"
    for tile_id in tile_ids:
        tile_path = tile_root / f"{tile_id:05d}.csv.gz"
        if not tile_path.is_file():
            raise ValueError(f"Missing completed tile file: {tile_path}")
        with gzip.open(tile_path, "rt", newline="", encoding="utf-8") as stream:
            fields = next(csv.reader(stream), [])
        missing = REQUIRED_FIELDS - set(fields)
        if missing:
            raise ValueError(f"Tile {tile_id} is missing required fields: {', '.join(sorted(missing))}")
        missing = set(ASTROMETRY_FIELDS) - set(fields)
        if missing:
            raise ValueError(
                f"Matched controls are on hold: tile {tile_id} lacks schema-complete Gaia inputs: "
                f"{', '.join(sorted(missing))}"
            )
    strata = {flag: {} for flag in FLAGS}
    exclusions = {flag: 0 for flag in FLAGS}
    tile_inputs = []
    rows_read = 0
    rows_without_flags = 0
    for tile_id in tile_ids:
        tile_path = tile_root / f"{tile_id:05d}.csv.gz"
        if not tile_path.is_file():
            raise ValueError(f"Missing completed tile file: {tile_path}")
        tile_inputs.append({
            "path": str(tile_path.relative_to(run_dir)),
            "size_bytes": tile_path.stat().st_size,
            "sha256": _hash_file(tile_path),
        })
        with gzip.open(tile_path, "rt", newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            missing = REQUIRED_FIELDS - set(reader.fieldnames or ())
            if missing:
                raise ValueError(
                    f"Tile {tile_id} is missing required fields: {', '.join(sorted(missing))}"
                )
            tile_rows = 0
            for line, row in enumerate(reader, start=2):
                if None in row or any(value is None for value in row.values()) or not row["source_id"].isdigit():
                    raise ValueError(f"Tile {tile_id}: malformed CSV row {line}")
                tile_rows += 1
                rows_read += 1
                raw_flags = row.get("flags", "")
                row_flags = set(filter(None, raw_flags.split(";")))
                if not row_flags:
                    rows_without_flags += 1
                for flag in FLAGS:
                    key = _stratum(flag, row, tile_id)
                    if key is None:
                        exclusions[flag] += 1
                        continue
                    bucket = strata[flag].setdefault(key, [0, 0])
                    if flag in row_flags:
                        bucket[0] += 1
                    elif not row_flags:
                        bucket[1] += 1
        if tile_rows != done[str(tile_id)]["n"]:
            raise ValueError(f"Tile {tile_id}: row count differs from sweep state")
        if _hash_file(tile_path) != tile_inputs[-1]["sha256"]:
            raise ValueError(f"Tile {tile_id} changed during capture")

    # Refuse to publish a report if the scanner changed the state during the
    # read; tile files are immutable after their state entry is committed.
    if state_path.read_bytes() != state_bytes:
        raise ValueError("Sweep state changed during capture; retry after the scanner settles")

    comparisons = {}
    for flag in FLAGS:
        groups = []
        totals = {"case_rows": 0, "clean_control_rows": 0, "matched_pairs": 0, "unmatched_case_rows": 0}
        for key, (cases, controls) in sorted(strata[flag].items()):
            matched = min(cases, controls)
            totals["case_rows"] += cases
            totals["clean_control_rows"] += controls
            totals["matched_pairs"] += matched
            totals["unmatched_case_rows"] += cases - matched
            if cases or controls:
                groups.append({
                    "tile": key[0],
                    "magnitude_bin_index": key[1],
                    "color_bin_index": key[2],
                    "parallax_snr_bin_index": key[3],
                    "additional_bin_indices": list(key[4:]),
                    "case_rows": cases,
                    "clean_control_rows": controls,
                    "matched_pairs": matched,
                })
        comparisons[flag] = {
            **totals,
            "strata": groups,
            "excluded_rows_missing_required_matching_values": exclusions[flag],
        }

    solution_type_available = True
    qualification = [
        "Descriptive matched-stratum counts only; no p-values, anomaly rates, or model scores are produced.",
        "The sweep is not a matched-control scientific baseline unless all tiles are complete.",
        "Gaia astrometric solution type is retained but not used in these exploratory strata; RUWE matching is not fully controlled.",
        "The scanner's cuts and flags are heuristics; no full astrometric covariance propagation or multiple-testing correction is performed.",
        "Bailer-Jones distances use Gaia astrometry and are not an independent measurement.",
    ]
    return {
        "schema_version": 1,
        "baseline_type": "matched_control_stratum_counts",
        "generated_utc": _utc_now(),
        "run_id": run_dir.name,
        "catalogue": "Gaia DR3 gaia_source joined to external.gaiaedr3_distance by source_id",
        "selection": "parallax_over_error > 5, as applied by the archived tile query",
        "healpix_level": level,
        "tiles_completed": len(tile_ids),
        "tiles_total": total_tiles,
        "complete_sweep": len(tile_ids) == total_tiles,
        "exploratory_partial_capture": len(tile_ids) != total_tiles,
        "rows_read": rows_read,
        "rows_without_any_scanner_flag": rows_without_flags,
        "matching_design": {
            "controls": "Only rows with no scanner flag of any kind.",
            "common_strata": [
                "same HEALPix tile",
                f"phot_g_mean_mag bins of width {MAG_BIN}",
                f"bp_rp bins of width {COLOR_BIN}",
                "parallax SNR bins [5,10), [10,20), [20,50), [50,100), [100,infinity)",
            ],
            "high_velocity_additional_strata": f"log10(dist_pc) bins of width {DISTANCE_DEX_BIN}",
            "distance_mismatch_additional_strata": (
                f"log10(dist_bj_pc) bins of width {DISTANCE_DEX_BIN} and "
                "relative Bailer-Jones interval-width bins of width 0.1"
            ),
            "astrometric_solution_type_available": solution_type_available,
            "matched_pairs_per_stratum": "min(flagged cases, clean controls); aggregate only descriptive counts",
        },
        "comparisons": comparisons,
        "input_fingerprint": {
            "sweep_state_sha256": hashlib.sha256(state_bytes).hexdigest(),
            "tile_files": tile_inputs,
        },
        "qualification_limitations": qualification,
        "scientific_inference_allowed": False,
    }


def write_summary(run_dir, output=None, allow_partial=False):
    report = build_summary(run_dir, allow_partial=allow_partial)
    output_dir = Path(output).resolve() if output else Path(run_dir).resolve() / "control_baselines"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / (
        f"matched_control_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{uuid4().hex[:8]}.json"
    )
    temp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    try:
        with temp_path.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, indent=2, allow_nan=False)
            stream.write("\n")
        if output_path.exists():
            raise FileExistsError(output_path)
        os.rename(temp_path, output_path)
    except Exception:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass
        raise
    return output_path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, help="Existing Star Mapper run directory")
    parser.add_argument("--output", help="Output directory (default: <run-dir>/control_baselines)")
    parser.add_argument(
        "--allow-partial", action="store_true",
        help="Create an explicitly exploratory snapshot before all HEALPix tiles are complete",
    )
    args = parser.parse_args(argv)
    path = write_summary(args.run_dir, args.output, args.allow_partial)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
