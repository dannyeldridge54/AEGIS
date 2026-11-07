import csv
import gzip
import json
from pathlib import Path

import pytest

from aegis.star_scanner import ASTROMETRY_FIELDS, STAR_FIELDS, adql, adql_by_id, assess
from aegis.sweep import PAGE_ROWS, SkySweep, adql_range


def test_all_query_paths_retain_raw_astrometry_and_zero_point_inputs():
    for query in (adql(0, 0), adql(0, 0, join=False), adql_by_id([1]), adql_range(0, 100, -1, 50)):
        for field in ASTROMETRY_FIELDS:
            assert f"g.{field}" in query
    assert len(STAR_FIELDS) == len(set(STAR_FIELDS))
    row = dict(source_id="1", ra=10, dec=20, parallax=1.23456789, parallax_error=.1,
               pmra=2, pmdec=3, ruwe=1.0, astrometric_params_solved=31,
               parallax_pmra_corr=-.25, ra_error=.5, dec_error=.6, ecl_lat=12.3)
    record = assess(row)
    assert record["parallax"] == 1.23456789
    assert record["parallax_pmra_corr"] == -.25
    assert record["astrometric_params_solved"] == 31
    assert record["pseudocolour"] is None


@pytest.mark.parametrize("lower,median,upper", [
    (-100, 1000, 1100), (0, 1000, 1100), (1000, 1000, 1000),
    (1100, 1000, 900), (1050, 1000, 1100), (900, 1200, 1100),
])
def test_scanner_rejects_invalid_recorded_distance_intervals(lower, median, upper):
    row = dict(source_id="5853498713190525696", ra=10, dec=20,
               parallax=1, parallax_error=.1, pmra=100, pmdec=0, ruwe=1,
               r_lo_geo=lower, r_med_geo=median, r_hi_geo=upper)
    with pytest.raises(ValueError, match="Bailer-Jones"):
        assess(row)


@pytest.mark.parametrize("state", [
    {"level": 1, "done": {}},
    {"level": 0, "done": {"12": {"n": 0, "conf": 0, "flags": {}}}},
    {"level": 0, "done": {"0": {"n": -1, "conf": 0, "flags": {}}}},
])
def test_resume_rejects_incompatible_or_corrupt_state_without_writes(tmp_path, state):
    path = tmp_path / "sweep_state.json"
    path.write_text(json.dumps(state), encoding="utf-8")
    before = path.read_bytes()
    with pytest.raises(ValueError):
        SkySweep(tmp_path, level=0, log=lambda _: None)
    assert path.read_bytes() == before


def test_resume_does_not_silently_drop_missing_completed_evidence(tmp_path):
    path = tmp_path / "sweep_state.json"
    path.write_text(json.dumps({
        "level": 0, "done": {"0": {"n": 1, "conf": 0, "flags": {}}},
    }), encoding="utf-8")
    with pytest.raises(ValueError, match="missing"):
        SkySweep(tmp_path, level=0, log=lambda _: None)


def test_completed_tiles_record_schema_and_query_provenance(tmp_path):
    row = dict(source_id="1", ra=10, dec=20, parallax=1, parallax_error=.1,
               pmra=2, pmdec=3, ruwe=1.0, astrometric_params_solved=31)
    scanner = SkySweep(tmp_path, level=0, query=lambda *a, **kw: [row], log=lambda _: None)
    scanner.active[0] = {"t0": 0, "rows": 0}
    scanner.sweep_tile(0)
    state = json.loads((tmp_path / "sweep_state.json").read_text(encoding="utf-8"))
    assert state["done"]["0"]["columns"] == STAR_FIELDS
    assert "g.astrometric_params_solved" in state["done"]["0"]["query_template"]
    with gzip.open(tmp_path / "tiles" / "L0" / "00000.csv.gz", "rt", encoding="utf-8") as stream:
        saved = next(csv.DictReader(stream))
    assert saved["parallax"] == "1.0"


def test_smaller_pages_keep_source_id_pagination_and_all_rows(tmp_path, monkeypatch):
    from aegis import sweep
    assert PAGE_ROWS == (8000, 4000, 2000)
    monkeypatch.setattr(sweep, "PAGE_ROWS", (2, 1))
    calls = []

    def query(statement, **kwargs):
        calls.append(statement)
        ids = [1, 2] if len(calls) == 1 else [3]
        return [dict(source_id=str(sid), ra=10, dec=20, parallax=1,
                     parallax_error=.1, pmra=2, pmdec=3, ruwe=1.)
                for sid in ids]

    scanner = SkySweep(tmp_path, level=0, query=query, log=lambda _: None)
    scanner.active[0] = {"t0": 0, "rows": 0}
    scanner.sweep_tile(0)
    assert len(calls) == 2
    assert "SELECT TOP 2" in calls[0]
    assert "BETWEEN 3 AND" in calls[1]
    assert all("parallax_over_error > 5 ORDER BY g.source_id" in call for call in calls)
    with gzip.open(tmp_path / "tiles" / "L0" / "00000.csv.gz", "rt",
                   encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert [row["source_id"] for row in rows] == ["1", "2", "3"]
    assert scanner.done[0]["n"] == 3
    assert scanner.done[0]["query_template"] == calls[0]


def test_async_range_mode_keeps_all_fields_and_does_not_cache_count_checks(tmp_path, monkeypatch):
    from aegis import sweep
    monkeypatch.setenv("AEGIS_TAP_ASYNC", "1")
    scanner = SkySweep(tmp_path, level=0, log=lambda _: None)
    calls = []
    def fake_async(query, directory, **kwargs):
        calls.append((query, directory))
        return [{"source_id": "1"}]
    monkeypatch.setattr(sweep, "query_async", fake_async)
    query = adql_range(0, 100, -1, 50)
    assert scanner._range_query(query) == [{"source_id": "1"}]
    assert calls == [(query, tmp_path / "tap_jobs")]
    assert scanner.query is sweep.tap_query


def test_terminal_async_fallback_preserves_jobs_cursor_and_all_rows(tmp_path, monkeypatch):
    from aegis import sweep, tap_async as tap
    monkeypatch.setenv("AEGIS_TAP_ASYNC", "1")
    monkeypatch.setattr(sweep, "PAGE_ROWS", (4, 2, 1))
    monkeypatch.setattr(sweep.time, "sleep", lambda _: None)
    calls = []

    def submit(query, _):
        calls.append(query)
        return tap.ENDPOINT + f"/fixture{len(calls)}"

    def get(url, _):
        if "fixture1/" in url:
            return "ABORTED"
        if url.endswith("/phase"):
            return "COMPLETED"
        ids = ["1", "2"] if "fixture2/" in url else ["3"]
        return ("source_id,ra,dec,parallax,parallax_error,pmra,pmdec,ruwe\n"
                + "".join(f"{sid},10,20,1,.1,2,3,1\n" for sid in ids))

    monkeypatch.setattr(tap, "_submit", submit)
    monkeypatch.setattr(tap, "_get", get)
    scanner = SkySweep(tmp_path, level=0, log=lambda _: None)
    scanner.active[0] = {"t0": 0, "rows": 0}
    scanner.sweep_tile(0)
    assert len(calls) == 3
    assert "SELECT TOP 4" in calls[0]
    assert "SELECT TOP 2" in calls[1]
    assert calls[0].split("WHERE")[1] == calls[1].split("WHERE")[1]
    assert "BETWEEN 3 AND" in calls[2]
    states = [json.loads(p.read_text()) for p in (tmp_path / "tap_jobs").glob("*.json")]
    assert len(states) == 3
    assert sum(state["phase"] == "ABORTED" for state in states) == 1
    with gzip.open(tmp_path / "tiles" / "L0" / "00000.csv.gz", "rt",
                   encoding="utf-8") as stream:
        assert [row["source_id"] for row in csv.DictReader(stream)] == ["1", "2", "3"]
    assert scanner.done[0]["n"] == 3


def test_terminal_async_exhaustion_blocks_tile_and_continues_other_tiles(tmp_path, monkeypatch):
    from aegis import sweep, tap_async as tap
    monkeypatch.setenv("AEGIS_TAP_ASYNC", "1")
    monkeypatch.setattr(sweep.time, "sleep", lambda _: None)
    calls, messages = [], []
    monkeypatch.setattr(tap, "_submit", lambda query, _: calls.append(query) or tap.ENDPOINT + f"/job{len(calls)}")
    monkeypatch.setattr(tap, "_get", lambda *_: "ERROR")
    scanner = SkySweep(tmp_path, level=0, log=messages.append)
    scanner.order = [0, 1]
    scanner._worker(lambda: False)
    assert len(calls) == 6
    assert len(list((tmp_path / "tap_jobs").glob("*.json"))) == 6
    assert set(scanner.blocked) == {0, 1}
    assert scanner.done == {}
    assert scanner.status["stars"] == 0
    assert scanner.status["collection_state"] == "blocked"
    assert len(scanner.status["blocked_tiles"]) == 2
    assert not list((tmp_path / "tiles" / "L0").glob("*.csv.gz"))
    assert any("catalogue is incomplete" in message for message in messages)
    assert not any("sweep complete:" in message for message in messages)
    assert scanner._next_tile() is None


def test_ambiguous_async_submission_blocks_without_smaller_page_resubmission(tmp_path, monkeypatch):
    import hashlib
    from aegis import sweep
    monkeypatch.setenv("AEGIS_TAP_ASYNC", "1")
    scanner = SkySweep(tmp_path, level=0, log=lambda _: None)
    scanner.order = [0]
    lo, hi = sweep.tile_source_id_range(0, 0)
    query = adql_range(lo, hi, lo - 1, PAGE_ROWS[0])
    directory = tmp_path / "tap_jobs"
    directory.mkdir()
    state = directory / (hashlib.sha256(query.encode()).hexdigest() + ".json")
    saved = json.dumps({"query": query, "phase": "SUBMITTING"})
    state.write_text(saved)
    scanner._worker(lambda: False)
    assert state.read_text() == saved
    assert len(list(directory.glob("*.json"))) == 1
    assert 0 in scanner.blocked


def test_science_view_discloses_historical_status_and_missing_exoplanet_rows():
    root = Path(__file__).resolve().parents[1]
    science = json.loads((root / "science.json").read_text(encoding="utf-8"))
    assert "not live fit status" in science["status_scope"]
    exoplanets = next(thread for thread in science["threads"] if thread["name"] == "Sigil Model exam")
    assert "cannot be reproduced" in exoplanets["status"]
    assert "historical snapshot" in (root / "live.html").read_text(encoding="utf-8")
