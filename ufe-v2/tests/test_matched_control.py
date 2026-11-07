import csv
import gzip
import json
from pathlib import Path

import pytest

from aegis.matched_control import _stratum, build_summary, write_summary
from aegis.star_scanner import ASTROMETRY_FIELDS


FIELDS = [
    "source_id", "g_mag", "bp_rp", "parallax_error", "dist_plx_pc", "dist_pc",
    "dist_bj_pc", "r_lo_geo", "r_hi_geo", "vtan_kms", "ruwe", "flags",
] + list(ASTROMETRY_FIELDS)


def _row(source_id, flags="", **overrides):
    row = {
        "source_id": str(source_id),
        "g_mag": "12.2",
        "bp_rp": "0.8",
        "parallax_error": "0.1",
        "dist_plx_pc": "1000",
        "dist_pc": "1000",
        "dist_bj_pc": "1000",
        "r_lo_geo": "900",
        "r_hi_geo": "1100",
        "vtan_kms": "100",
        "ruwe": "1.0",
        "flags": flags,
    }
    row.update({field: "" for field in ASTROMETRY_FIELDS})
    row.update(overrides)
    return row


def _run(tmp_path, tiles):
    run_dir = tmp_path / "run"
    tile_dir = run_dir / "tiles" / "L0"
    tile_dir.mkdir(parents=True)
    done = {}
    for tile, rows in tiles.items():
        path = tile_dir / f"{tile:05d}.csv.gz"
        with gzip.open(path, "wt", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        done[str(tile)] = {"n": len(rows), "conf": len(rows), "flags": {}}
    (run_dir / "sweep_state.json").write_text(
        json.dumps({"level": 0, "done": done}), encoding="utf-8"
    )
    return run_dir


def test_complete_sweep_counts_same_stratum_cases_and_clean_controls(tmp_path):
    tiles = {tile: [] for tile in range(12)}
    tiles[0] = [
        _row(1, "astrometric_excess"),
        _row(2),
        _row(3),
        _row(4, "high_velocity;astrometric_excess", vtan_kms="450"),
        _row(5, "high_velocity", vtan_kms="500"),
    ]
    run_dir = _run(tmp_path, tiles)
    report = build_summary(run_dir)

    assert report["complete_sweep"] is True
    assert report["scientific_inference_allowed"] is False
    assert report["rows_read"] == 5
    ruwe = report["comparisons"]["astrometric_excess"]
    assert ruwe["case_rows"] == 2
    assert ruwe["clean_control_rows"] == 2
    assert ruwe["matched_pairs"] == 2
    speed = report["comparisons"]["high_velocity"]
    assert speed["case_rows"] == 2
    assert speed["clean_control_rows"] == 2
    assert speed["matched_pairs"] == 2
    assert report["matching_design"]["astrometric_solution_type_available"] is True


def test_partial_sweep_is_rejected_unless_explicitly_exploratory(tmp_path):
    run_dir = _run(tmp_path, {0: [_row(1), _row(2, "astrometric_excess")]})
    with pytest.raises(ValueError, match="complete sweep"):
        build_summary(run_dir)
    report = build_summary(run_dir, allow_partial=True)
    assert report["complete_sweep"] is False
    assert report["exploratory_partial_capture"] is True


def test_missing_tile_or_required_field_fails_explicitly(tmp_path):
    run_dir = _run(tmp_path, {tile: [] for tile in range(12)})
    (run_dir / "tiles" / "L0" / "00000.csv.gz").unlink()
    with pytest.raises(ValueError, match="Missing completed tile"):
        build_summary(run_dir)

    run_dir = _run(tmp_path / "second", {tile: [] for tile in range(12)})
    path = run_dir / "tiles" / "L0" / "00000.csv.gz"
    with gzip.open(path, "wt", newline="", encoding="utf-8") as stream:
        stream.write("source_id,flags\n")
    with pytest.raises(ValueError, match="missing required fields"):
        build_summary(run_dir)


def test_legacy_uncertainty_schema_stays_on_hold(tmp_path):
    run_dir = _run(tmp_path, {tile: [] for tile in range(12)})
    path = run_dir / "tiles" / "L0" / "00000.csv.gz"
    with gzip.open(path, "wt", newline="", encoding="utf-8") as stream:
        csv.writer(stream).writerow([field for field in FIELDS if field not in ASTROMETRY_FIELDS])
    with pytest.raises(ValueError, match="on hold"):
        build_summary(run_dir)


def test_tile_row_count_must_match_state(tmp_path):
    run_dir = _run(tmp_path, {tile: [] for tile in range(12)})
    path = run_dir / "tiles" / "L0" / "00000.csv.gz"
    with gzip.open(path, "at", newline="", encoding="utf-8") as stream:
        csv.DictWriter(stream, fieldnames=FIELDS).writerow(_row(1))
    with pytest.raises(ValueError, match="row count differs"):
        build_summary(run_dir)


def test_report_writes_unique_immutable_outputs(tmp_path):
    run_dir = _run(tmp_path, {tile: [] for tile in range(12)})
    out = tmp_path / "reports"
    first = write_summary(run_dir, out)
    first_content = first.read_bytes()
    second = write_summary(run_dir, out)
    assert first != second
    assert first.read_bytes() == first_content
    report = json.loads(second.read_text(encoding="utf-8"))
    assert report["input_fingerprint"]["sweep_state_sha256"]
    assert len(report["input_fingerprint"]["tile_files"]) == 12


def test_required_matching_bins_exclude_rows_with_unusable_values(tmp_path):
    tiles = {tile: [] for tile in range(12)}
    tiles[0] = [
        _row(1, "high_velocity", vtan_kms="450"),
        _row(2, "", bp_rp=""),
    ]
    report = build_summary(_run(tmp_path, tiles))
    high_velocity = report["comparisons"]["high_velocity"]
    assert high_velocity["case_rows"] == 1
    assert high_velocity["excluded_rows_missing_required_matching_values"] == 1


@pytest.mark.parametrize("lower,median,upper", [
    ("-100", "1000", "1100"),
    ("0", "1000", "1100"),
    ("1000", "1000", "1000"),
    ("1100", "1000", "900"),
    ("1050", "1000", "1100"),
    ("900", "1200", "1100"),
])
def test_invalid_distance_intervals_do_not_enter_matched_strata(lower, median, upper):
    row = _row(1, r_lo_geo=lower, dist_bj_pc=median, r_hi_geo=upper)
    assert _stratum("distance_mismatch", row, 0) is None


def test_valid_distance_interval_enters_matched_stratum():
    assert _stratum("distance_mismatch", _row(1), 0) is not None
