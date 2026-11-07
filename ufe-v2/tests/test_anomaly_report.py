"""Bounded offline reporting; no scanner startup, sockets, downloads or model fits."""
import csv
import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from aegis.anomaly_report import build_report, latest_report, to_markdown, write_report


@pytest.fixture(autouse=True)
def forbid_downloads(monkeypatch):
    import urllib.request

    def fail(*args, **kwargs):
        pytest.fail("Offline reports must never access the network")

    monkeypatch.setattr(urllib.request, "urlopen", fail)


@pytest.fixture
def local_inputs(tmp_path):
    out = tmp_path / "ufe-v2" / "cosmos_map"
    out.mkdir(parents=True)
    summary = {
        "stars": 10, "confirmed": 8, "patches": 2,
        "flags": {"high_velocity": 2, "astrometric_excess": 1},
        "last_patches": [{"t": 1700000000}, {"t": 1600000000}],
    }
    (out / "star_scan_summary.json").write_text(json.dumps(summary), encoding="utf-8")
    theory = tmp_path / "theory"
    theory.mkdir()
    (theory / "bi_kahler_lambda.json").write_text('{"lambda_exact": "-2 sqrt(2/3)"}', encoding="utf-8")
    claims = tmp_path / "ufe-v2" / "method"
    claims.mkdir()
    (claims / "claims.json").write_text(
        '{"claims": {"failure": {"status": "failed", "note": "keep original caveat"}}}', encoding="utf-8")
    return tmp_path, out, summary


def write_flags(out, rows):
    with (out / "cosmos_map_flags.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=[
            "source_id", "flags", "flag_notes", "ruwe", "vtan_kms", "parallax_error", "pmra_error",
            "pmdec_error", "pmra_pmdec_corr", "r_lo_geo", "r_hi_geo",
        ])
        writer.writeheader()
        writer.writerows(rows)


def test_summary_only_freshness_and_missing_rows(local_inputs):
    root, out, summary = local_inputs
    report = build_report(root)
    obs = report["observational_evidence"]
    assert obs["saved_star_summary"] == summary
    assert obs["status"] == "saved_summary_not_row_verified"
    assert obs["candidate_export"]["status"] == "missing_not_zero_candidates"
    assert obs["candidate_export"]["rows"] == []
    assert obs["flag_fractions_of_saved_stars"] == {"high_velocity": .2, "astrometric_excess": .1}
    assert report["freshness"]["latest_recorded_patch_utc"] == "2023-11-14T22:13:20+00:00"
    assert report["freshness"]["new_measurements_acquired"] is False
    assert "theory_claims" not in report
    assert "speculative_interpretation" not in report
    assert not any(source["path"].startswith("theory/") for source in report["sources"])
    source = next(s for s in report["sources"] if s["path"].endswith("star_scan_summary.json"))
    assert source["sha256"] == hashlib.sha256((out / "star_scan_summary.json").read_bytes()).hexdigest()
    text = to_markdown(report)
    for heading in ("Dataset and freshness", "Anomaly definitions and controls", "Candidate rows",
                    "Uncertainty and limitations", "Source provenance", "Astronomy tools for independent follow-up"):
        assert heading in text
    assert "not independent measurements" in text
    assert "NOT a calibrated 3-sigma test" in text
    assert "quantum" not in text.lower()
    assert "Gaia Archive" in text and "VizieR" in text and "SIMBAD" in text


def test_report_preserves_extended_raw_inputs_without_reclassification(local_inputs):
    root, out, _ = local_inputs
    row = {"source_id": "5853498713190525696", "flags": "high_velocity",
           "flag_notes": "Original note", "rv": "0", "parallax": "1.234567890123",
           "astrometric_params_solved": "95", "pseudocolour": "1.4",
           "nu_eff_used_in_astrometry": "", "radial_velocity_error": ".25",
           "ra_parallax_corr": "-.2", "pmra_pmdec_corr": "0"}
    with (out / "cosmos_map_flags.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    before = (out / "cosmos_map_flags.csv").read_bytes()
    report = build_report(root)
    candidate = report["observational_evidence"]["candidate_export"]["rows"][0]
    assert candidate["id"] == row["source_id"]
    assert candidate["flags"] == row["flags"] and candidate["flag_notes"] == row["flag_notes"]
    for key in row.keys() - {"source_id", "flags", "flag_notes"}:
        assert candidate["catalog_values"][key] == row[key]
    assert (out / "cosmos_map_flags.csv").read_bytes() == before
    assert any(tool["name"] == "GaiaUnlimited" for tool in report["reference_tools"])


def test_research_channels_are_references_not_new_detections(local_inputs):
    root, _, _ = local_inputs
    report = build_report(root)
    research = report["research_channels"]
    assert research["status"] == "reference_routes_only_no_catalog_ingestion_or_new_detection"
    names = {item["name"] for item in research["channels"]}
    assert {"Asteroids and comets", "Meteors and fireballs", "Interstellar small bodies",
            "Exoplanets", "Pulsars and neutron stars", "Black holes and high-energy counterparts"} <= names
    for item in research["channels"]:
        assert item["inputs_needed"] and item["not_inferred"]
        assert all(ref["url"].startswith("https://") for ref in item["references"])
    assert report["observational_evidence"]["candidate_export"]["rows"] == []
    text = to_markdown(report)
    assert "Research channels and missing evidence" in text
    assert "not an interstellar classification" in text
    assert "not establish a black hole" in text


@pytest.mark.parametrize("source_id", ["not-a-source", "-1", "1.0", "１２３"])
def test_malformed_source_ids_refuse_report(local_inputs, source_id):
    root, out, _ = local_inputs
    write_flags(out, [{"source_id": source_id, "flags": "high_velocity", "flag_notes": ""}])
    with pytest.raises(ValueError, match="Malformed mapper flags row"):
        build_report(root)


def test_markdown_preserves_zero_and_escapes_table_cells(local_inputs):
    root, out, _ = local_inputs
    write_flags(out, [{"source_id": "123", "flags": "custom|flag",
                      "flag_notes": "original", "pmra_pmdec_corr": "0", "vtan_kms": "0"}])
    report = build_report(root)
    row = report["observational_evidence"]["candidate_export"]["rows"][0]
    row["catalog_values"]["rv"] = 0
    text = to_markdown(report)
    table_row = next(line for line in text.splitlines() if line.startswith("| 123 |"))
    assert "custom\\|flag" in table_row
    assert " | 0 |" in table_row
    assert table_row.endswith("| 0 |")

def test_sweep_report_separates_current_tiles_from_stale_legacy_summary(local_inputs):
    root, out, summary = local_inputs
    summary_path = out / "star_scan_summary.json"
    catalog_path = out / "cosmos_map_stars.csv"
    catalog_path.write_text("source_id\n1\n", encoding="utf-8")
    summary_time = summary_path.stat().st_mtime
    os.utime(catalog_path, (summary_time + 10, summary_time + 10))
    state = {
        "level": 0,
        "done": {
            "0": {"n": 7, "conf": 5, "flags": {"high_velocity": 2}},
            "1": {"n": 5, "conf": 2, "flags": {"astrometric_excess": 1}},
        },
        "recent_tiles": [{"t": 1700000100, "tile": 1}],
    }
    (out / "sweep_state.json").write_text(json.dumps(state), encoding="utf-8")
    tile_dir = out / "tiles" / "L0"
    tile_dir.mkdir(parents=True)
    (tile_dir / "00000.csv.gz").touch()
    (tile_dir / "00001.csv.gz").touch()

    report = build_report(root)
    obs = report["observational_evidence"]
    sweep = obs["active_sweep_summary"]
    legacy = obs["legacy_random_patch_snapshot"]
    assert obs["status"] == "separate_sweep_and_legacy_snapshots"
    assert sweep["stars"] == 12 and sweep["confirmed"] == 7
    assert sweep["tiles_done"] == 2 and sweep["tiles_total"] == 12 and not sweep["complete"]
    assert sweep["flags"] == {"high_velocity": 2, "astrometric_excess": 1}
    assert sweep["tile_files"] == {
        "expected_for_completed_tiles": 2, "present": 2, "missing": 0,
    }
    assert obs["saved_star_summary"]["stars"] == 10
    assert legacy["catalog_newer_than_summary"] is True
    assert "rechecked is attempted ID re-queries" in legacy["count_basis"]
    text = to_markdown(report)
    assert "Systematic HEALPix sweep snapshot" in text
    assert "Stored systematic-sweep flag counts" in text
    assert "| astrometric_excess | 1 |" in text
    assert "Legacy random-patch snapshot" in text
    assert "do not compare or add the counts" in text


def test_sweep_report_keeps_all_check_telemetry_and_separates_local_catalogs(local_inputs):
    root, out, _ = local_inputs
    state = {
        "level": 0,
        "done": {"1": {"n": 5, "conf": 4, "flags": {}}},
        "recent_tiles": [{"t": 1700000100, "tile": 1}],
        "checks": [
            {"t": 1700000200, "tile": 1, "ours": 5, "esa": 5, "match": True},
            {"t": 1700000300, "tile": 0, "ours": 7, "esa": 6, "match": False},
        ],
    }
    (out / "sweep_state.json").write_text(json.dumps(state), encoding="utf-8")
    tile_dir = out / "tiles" / "L0"
    tile_dir.mkdir(parents=True)
    (tile_dir / "00001.csv.gz").touch()
    impacts = root / "research" / "impacts"
    impacts.mkdir(parents=True)
    (impacts / "craters.json").write_text(json.dumps([{"name": "A"}, {"name": "B"}]), encoding="utf-8")
    (impacts / "impact_result.json").write_text(json.dumps({
        "n": 2, "Pbest": 27.65, "R": 0.279, "p": 0.3325,
    }), encoding="utf-8")

    report = build_report(root)
    sweep = report["observational_evidence"]["active_sweep_summary"]
    checks = sweep["spot_checks"]
    assert checks["retained"] == 2 and checks["matched"] == 1 and checks["mismatched"] == 1
    assert checks["records"][0]["match"] is True and checks["records"][1]["esa_count"] == 6
    assert report["additional_local_datasets"]["impact_structures"]["rows"] == 2
    assert report["additional_local_datasets"]["exoplanet_periods"]["status"] == "missing_input"
    text = to_markdown(report)
    assert "Other local astronomy datasets (separate analyses)" in text
    assert "scan-corrected p=0.3325" in text
    assert "not merged with Gaia stars" in text


def test_sweep_retains_every_spot_check(tmp_path):
    from aegis.sweep import SkySweep

    scanner = SkySweep(
        tmp_path, query=lambda *_args, **_kwargs: [{"n": 1}],
        log=lambda _message: None, level=0,
    )
    scanner.done[0] = {"n": 1, "conf": 1, "flags": {}, "shells": [0, 0, 0, 1, 0]}
    for _ in range(205):
        scanner.spot_check()

    saved = json.loads((tmp_path / "sweep_state.json").read_text(encoding="utf-8"))
    assert len(scanner.checks) == 205
    assert len(saved["checks"]) == 205
    assert scanner.status["checks_total"] == 205
    assert scanner.status["checks_passed"] == 205

def test_sweep_publishes_active_tile_progress(tmp_path):
    from aegis.sweep import SkySweep

    status = {}
    scanner = SkySweep(tmp_path, status=status, log=lambda _message: None, level=0)
    tile = scanner._next_tile()
    assert status["active"] == [{
        "tile": tile,
        "l": scanner.centres[tile][0],
        "b": scanner.centres[tile][1],
        "rows": 0,
    }]
    scanner.active[tile]["rows"] = 17
    with scanner.lock:
        status["active"] = scanner._active_status()
    assert status["active"][0]["rows"] == 17

def test_sweep_map_exposes_tile_counts_and_heuristic_flags(tmp_path):
    from aegis.sweep import SkySweep

    scanner = SkySweep(tmp_path, log=lambda _message: None, level=0)
    tile = scanner.order[0]
    scanner.done[tile] = {"n": 12, "conf": 8, "flags": {"high_velocity": 2}, "shells": [0] * 5}
    mapped = scanner.tiles_map()
    detail = next(item for item in mapped["done_detail"] if item["tile"] == tile)
    assert detail["stars"] == 12
    assert detail["flags"] == {"high_velocity": 2}


def test_versioned_run_report_writes_inside_run_without_touching_default(local_inputs):
    root, out, _ = local_inputs
    run_out = out / "runs" / "fresh-run"
    original = (out / "star_scan_summary.json").read_bytes()
    json_path, md_path = write_report(root, outdir=run_out)
    assert json.loads(json_path.read_text(encoding="utf-8"))["run_id"] == "fresh-run"
    assert json_path.parent == run_out / "anomaly_reports"
    assert md_path.is_file()
    assert latest_report(run_out) == json_path.read_text(encoding="utf-8")
    assert (out / "star_scan_summary.json").read_bytes() == original
    assert not (out / "anomaly_reports").exists()

@pytest.mark.parametrize("collection,state", [("blocked", "blocked"), ("degraded", "degraded"),
                                               ("scanning", "scanning")])
def test_monitor_status_discloses_blocked_collection(monkeypatch, collection, state):
    import monitor_server
    monkeypatch.setitem(monitor_server.STATUS, "state", "scanning")
    monkeypatch.setitem(monitor_server.SCANNER, "status", {
        "collection_state": collection, "blocked_tiles": [{"tile": 0, "error": "ESA ERROR"}],
    })
    handler = object.__new__(monitor_server.Handler)
    handler.path = "/api/status"
    responses = []
    handler._send = lambda code, body, content_type: responses.append(json.loads(body))
    handler.do_GET()
    assert responses[0]["state"] == state
    assert responses[0]["scan"]["blocked_tiles"][0]["error"] == "ESA ERROR"


def test_monitor_refreshes_and_exposes_anomaly_report_status(local_inputs, monkeypatch):
    root, out, _ = local_inputs
    run_out = out / "runs" / "active-run"
    import monitor_server
    import aegis.anomaly_report as anomaly_report

    monkeypatch.setattr(monitor_server, "log", lambda _: None)
    monkeypatch.setattr(monitor_server, "OUT", str(run_out))
    monkeypatch.setattr(
        anomaly_report, "write_report",
        lambda outdir=None: write_report(root, outdir=outdir),
    )
    report_path = monitor_server.generate_anomaly_report()
    assert report_path is not None and report_path.is_file()
    assert latest_report(run_out) == report_path.read_text(encoding="utf-8")
    assert monitor_server.STATUS["report"]["state"] == "available"
    assert monitor_server.STATUS["report"]["error"] is None
    assert monitor_server.STATUS["report"]["path"].startswith("anomaly_reports")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert "scanner may update them independently" in report["freshness"]["status"]
    assert any("Report generation did not fetch measurements" in item for item in report["limitations"])

def test_random_patch_row_encounters_deduplicate_and_rechecks_do_not_add_stars(tmp_path):
    from aegis.star_scanner import StarScanner

    row = {
        "source_id": "123", "ra": 10, "dec": 20, "parallax": 1,
        "parallax_error": .1, "pmra": 0, "pmra_error": .2, "pmdec": 0, "pmdec_error": .3,
        "pmra_pmdec_corr": -.1, "ruwe": 1.0,
    }
    scanner = StarScanner(
        tmp_path, log=lambda _: None, seed=1, query=lambda *_args, **_kwargs: [row, row],
    )
    patch = scanner.scan_once()
    assert patch["stars"] == 2
    assert patch["new"] == 1
    assert len(scanner.seen) == 1
    assert scanner.status["stars"] == 1
    assert scanner.status["star_count_basis"].startswith("Unique Gaia source IDs")
    with (tmp_path / "cosmos_map_stars.csv").open(newline="", encoding="utf-8") as fh:
        saved = next(csv.DictReader(fh))
    assert saved["pmra_error"] == "0.2" and saved["pmdec_error"] == "0.3"
    assert saved["pmra_pmdec_corr"] == "-0.1"

    scanner.query = lambda *_args, **_kwargs: [
        dict(row, r_med_geo=1000, r_lo_geo=900, r_hi_geo=1100)
    ]
    assert scanner.recheck_once() == 1
    assert scanner.status["stars"] == 1
    assert scanner.status["rechecked"] == 1
    assert scanner.status["rechecks_attempted"] == 1


def test_legacy_catalog_rows_load_with_missing_uncertainties(tmp_path):
    from aegis.star_scanner import ASTROMETRY_FIELDS, STAR_FIELDS, StarScanner

    old_fields = [field for field in STAR_FIELDS if field not in ASTROMETRY_FIELDS][:-6]
    legacy = {key: "" for key in old_fields}
    legacy.update(source_id="123", astrometric_quality_pass="True", confirmed="True", flags="")
    with (tmp_path / "cosmos_map_stars.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=old_fields)
        writer.writeheader()
        writer.writerow(legacy)

    scanner = StarScanner(tmp_path, log=lambda _: None, seed=1)
    assert scanner.sample[0]["confirmed"] == "True"
    assert scanner.sample[0]["pmra_error"] == ""
    assert scanner.sample[0]["r_lo_geo"] == ""
    with (tmp_path / "cosmos_map_stars.csv").open(newline="", encoding="utf-8") as fh:
        normalized = next(csv.DictReader(fh))
    assert normalized["source_id"] == "123"
    assert normalized["pmra_error"] == "" and normalized["r_lo_geo"] == ""


def test_bounded_candidates_preserve_values_no_reclassification(local_inputs):
    root, out, _ = local_inputs
    write_flags(out, [
        {"source_id": "9007199254740993", "flags": "high_velocity;high_velocity;astrometric_excess",
         "flag_notes": "stored candidate", "ruwe": "1.40", "vtan_kms": "400.0",
         "parallax_error": "0.1", "pmra_error": "0.2", "pmdec_error": "0.3",
         "pmra_pmdec_corr": "-0.1", "r_lo_geo": "90", "r_hi_geo": "110"},
        {"source_id": "2", "flags": "distance_mismatch", "flag_notes": "stored mismatch"},
        {"source_id": "3", "flags": "unknown_flag", "flag_notes": "not inspected"},
    ])
    export = build_report(root, max_rows=2)["observational_evidence"]["candidate_export"]
    assert export["rows_inspected"] == 2 and export["truncated"]
    assert export["flags_in_inspected_rows"] == {"high_velocity": 1, "astrometric_excess": 1, "distance_mismatch": 1}
    row = export["rows"][0]
    assert row["id"] == "9007199254740993"
    assert row["catalog_values"]["ruwe"] == "1.40"
    assert row["derived_values"]["vtan_kms"] == "400.0"
    assert row["catalog_values"]["pmra_error"] == "0.2"
    assert row["catalog_values"]["pmra_pmdec_corr"] == "-0.1"
    assert row["derived_values"]["r_lo_geo"] == "90"
    assert row["catalog_values"]["ra"] == ""
    assert row["flags"] == "high_velocity;astrometric_excess"
    assert row["time"] is None
    complete = build_report(root, max_rows=3)
    assert not complete["observational_evidence"]["candidate_export"]["truncated"]
    assert complete["anomaly_definitions_and_controls"]["unknown_flags"] == ["unknown_flag"]
    uncertainty = complete["observational_evidence"]["candidate_export"]["uncertainty_fields"]
    assert uncertainty["available_in_csv"] == [
        "parallax_error", "pmdec_error", "pmra_error", "pmra_pmdec_corr", "r_hi_geo", "r_lo_geo",
    ]
    assert uncertainty["nonempty_rows_inspected"]["pmra_error"] == 1


def test_candidate_display_cap_does_not_change_inspected_counts(local_inputs):
    root, out, _ = local_inputs
    write_flags(out, [{"source_id": str(i), "flags": "high_velocity", "flag_notes": "candidate"} for i in range(50)])
    export = build_report(root)["observational_evidence"]["candidate_export"]
    assert len(export["rows"]) == 40
    assert export["rows_inspected"] == 50 and not export["truncated"]
    assert export["flags_in_inspected_rows"] == {"high_velocity": 50}


def test_report_criteria_match_scanner_strict_thresholds():
    from aegis.anomaly_report import CRITERIA
    from aegis.star_scanner import assess

    row = dict(source_id="1", ra=0, dec=0, parallax=1, parallax_error=.01,
               ruwe=1.4, pmra=0, pmdec=0, r_med_geo=1000, r_lo_geo=900, r_hi_geo=1100)
    assert assess(row)["flags"] == ""
    assert "astrometric_excess" in assess(dict(row, ruwe=1.4001))["flags"]
    assert "high_velocity" not in assess(dict(row, pmra=399 / 4.74047))["flags"]
    assert "high_velocity" in assess(dict(row, pmra=401 / 4.74047))["flags"]
    distance_row = dict(row, parallax=2.5, r_med_geo=100, r_lo_geo=50, r_hi_geo=150)
    assert "distance_mismatch" not in assess(distance_row)["flags"]
    assert "distance_mismatch" in assess(dict(distance_row, parallax=2))["flags"]
    assert CRITERIA["astrometric_excess"]["rule"] == "ruwe > 1.4"
    assert CRITERIA["high_velocity"]["rule"] == "vtan_kms > 400"
    assert "3 * (r_hi_geo - r_lo_geo)" in CRITERIA["distance_mismatch"]["rule"]


def test_empty_inputs_are_unavailable_not_zero(tmp_path):
    report = build_report(tmp_path)
    assert report["observational_evidence"]["saved_star_summary"] is None
    assert report["observational_evidence"]["flag_fractions_of_saved_stars"] == {}
    assert report["freshness"]["latest_recorded_patch_utc"] is None
    assert report["reference_tools"]
    assert "theory_claims" not in report
    assert report["missing_sources"]


def test_default_dashboard_maps_sweep_tiles_and_documents_astronomy_tools():
    dashboard = (Path(__file__).resolve().parents[1] / "monitor.html").read_text(encoding="utf-8").lower()
    assert "gaia star mapper" in dashboard
    assert "systematic-sweep sky map" in dashboard
    assert "not one marker per star" in dashboard
    assert "persisted systematic sweep" in dashboard
    assert "legacy random-patch snapshot" in dashboard
    assert "the legacy random-patch snapshot below is from a different scanner" in dashboard
    assert "recorded candidate rows" in dashboard
    assert all(tool in dashboard for tool in ("topcat", "astropy", "gaia archive", "vizier", "simbad"))
    assert "quantum" not in dashboard and "torsion" not in dashboard
    assert "metatron" not in dashboard and "not a race or a game" not in dashboard


@pytest.mark.parametrize("max_rows", [0, -1, 20001])
def test_invalid_limit_rejected(tmp_path, max_rows):
    with pytest.raises(ValueError, match="max_rows"):
        build_report(tmp_path, max_rows)


def test_malformed_inputs_fail_explicitly(local_inputs):
    root, out, summary = local_inputs
    (out / "cosmos_map_flags.csv").write_text("wrong_header\n1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="requires"):
        build_report(root)
    (out / "cosmos_map_flags.csv").write_text("source_id,flags,flag_notes\n1,high_velocity\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Malformed"):
        build_report(root)
    summary["stars"] = -1
    (out / "star_scan_summary.json").write_text(json.dumps(summary), encoding="utf-8")
    with pytest.raises(ValueError, match="count"):
        build_report(root)
    (out / "star_scan_summary.json").write_text('{"stars": NaN}', encoding="utf-8")
    with pytest.raises(ValueError, match="Non-finite"):
        build_report(root)


def test_reports_append_preserve_evidence_and_select_latest(local_inputs):
    root, out, _ = local_inputs
    (out / "cosmos_map_anomalies.csv").write_text("historic evidence\n", encoding="utf-8")
    (out / "anomaly_scan_summary.json").write_text('{"historic": true}', encoding="utf-8")
    original = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
    assert latest_report(out) is None
    first = write_report(root)
    first_bytes = {p: p.read_bytes() for p in first}
    second = write_report(root)
    assert first != second
    assert len(list((out / "anomaly_reports").glob("*.json"))) == 2
    for path, content in {**original, **first_bytes}.items():
        assert path.read_bytes() == content
    assert latest_report(out) == second[0].read_text(encoding="utf-8")
    assert latest_report(out, markdown=True) == second[1].read_text(encoding="utf-8")
    (out / "anomaly_reports" / "anomaly_report_9999.json.tmp").write_text("unfinished", encoding="utf-8")
    assert json.loads(latest_report(out))["schema_version"] == 4


def test_http_report_routes_read_only_and_missing(local_inputs, monkeypatch):
    import monitor_server
    root, out, _ = local_inputs
    monkeypatch.setattr(monitor_server, "OUT", str(out))
    handler = object.__new__(monitor_server.Handler)
    responses = []
    handler._send = lambda code, body, ctype: responses.append((code, body, ctype))
    handler.path = "/api/anomaly-report.json"
    handler.do_GET()
    assert responses[-1][0] == 404
    assert not (out / "anomaly_reports").exists()
    json_path, md_path = write_report(root)
    handler.do_GET()
    assert responses[-1] == (200, json_path.read_text(encoding="utf-8"), "application/json")
    handler.path = "/api/anomaly-report.md"
    handler.do_GET()
    assert responses[-1] == (200, md_path.read_text(encoding="utf-8"), "text/markdown; charset=utf-8")
    assert len(list((out / "anomaly_reports").glob("*.json"))) == 1
