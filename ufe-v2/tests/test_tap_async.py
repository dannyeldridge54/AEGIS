import json

import pytest

from aegis import tap_async as tap


QUERY = "SELECT TOP 1 source_id FROM gaiadr3.gaia_source"
URL = tap.ENDPOINT + "/fixture"


def test_completed_job_preserves_query_and_result_without_resubmission(tmp_path, monkeypatch):
    monkeypatch.setattr(tap, "_submit", lambda *_: URL)
    monkeypatch.setattr(tap, "_get", lambda url, _: "COMPLETED" if url.endswith("/phase") else "source_id\n123\n")
    assert tap.query_async(QUERY, tmp_path) == [{"source_id": "123"}]
    monkeypatch.setattr(tap, "_submit", lambda *_: pytest.fail("Duplicate submission"))
    monkeypatch.setattr(tap, "_get", lambda *_: pytest.fail("Cached result should not refetch"))
    assert tap.query_async(QUERY, tmp_path) == [{"source_id": "123"}]
    assert next(tmp_path.glob("*.json")).read_text().find(QUERY) >= 0


def test_ambiguous_submission_never_retries(tmp_path, monkeypatch):
    def timeout(*_):
        raise TimeoutError("accepted or not unknown")
    monkeypatch.setattr(tap, "_submit", timeout)
    with pytest.raises(TimeoutError):
        tap.query_async(QUERY, tmp_path)
    with pytest.raises(tap.AsyncJobBlockedError, match="outcome unknown"):
        tap.query_async(QUERY, tmp_path)


@pytest.mark.parametrize("phase", ["ERROR", "ABORTED", "UNKNOWN"])
def test_terminal_or_unknown_phase_is_explicit(tmp_path, monkeypatch, phase):
    monkeypatch.setattr(tap, "_submit", lambda *_: URL)
    monkeypatch.setattr(tap, "_get", lambda *_: phase)
    expected = tap.TerminalJobError if phase in ("ERROR", "ABORTED") else tap.AsyncJobBlockedError
    with pytest.raises(expected, match="async"):
        tap.query_async(QUERY, tmp_path)
    assert json.loads(next(tmp_path.glob("*.json")).read_text())["phase"] == phase


def test_unexpected_job_url_is_not_followed(tmp_path, monkeypatch):
    monkeypatch.setattr(tap, "_submit", lambda *_: "https://example.com/job")
    monkeypatch.setattr(tap, "_get", lambda *_: pytest.fail("Unexpected URL fetched"))
    with pytest.raises(ValueError, match="job URL"):
        tap.query_async(QUERY, tmp_path)


@pytest.mark.parametrize("phase", ["ERROR", "ABORTED"])
def test_saved_terminal_job_is_not_polled_or_resubmitted(tmp_path, monkeypatch, phase):
    monkeypatch.setattr(tap, "_submit", lambda *_: URL)
    monkeypatch.setattr(tap, "_get", lambda *_: phase)
    with pytest.raises(tap.TerminalJobError):
        tap.query_async(QUERY, tmp_path)
    state_path = next(tmp_path.glob("*.json"))
    original = state_path.read_bytes()
    monkeypatch.setattr(tap, "_submit", lambda *_: pytest.fail("Terminal job resubmitted"))
    monkeypatch.setattr(tap, "_get", lambda *_: pytest.fail("Terminal job polled again"))
    with pytest.raises(tap.TerminalJobError):
        tap.query_async(QUERY, tmp_path)
    assert state_path.read_bytes() == original


@pytest.mark.parametrize("text", ["<error>broken</error>", "wrong_header\n123\n", "source_id,ra\n123\n"])
def test_invalid_results_are_not_saved(tmp_path, monkeypatch, text):
    monkeypatch.setattr(tap, "_submit", lambda *_: URL)
    monkeypatch.setattr(tap, "_get", lambda url, _: "COMPLETED" if url.endswith("/phase") else text)
    with pytest.raises(ValueError):
        tap.query_async(QUERY, tmp_path)
    assert not list(tmp_path.glob("*.csv"))


def test_changed_cached_results_are_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(tap, "_submit", lambda *_: URL)
    monkeypatch.setattr(tap, "_get", lambda url, _: "COMPLETED" if url.endswith("/phase") else "source_id\n123\n")
    tap.query_async(QUERY, tmp_path)
    next(tmp_path.glob("*.csv")).write_text("source_id\n456\n")
    with pytest.raises(ValueError, match="fingerprint"):
        tap.query_async(QUERY, tmp_path)


def test_wait_timeout_resumes_same_job(tmp_path, monkeypatch):
    monkeypatch.setattr(tap, "_submit", lambda *_: URL)
    monkeypatch.setattr(tap, "_get", lambda *_: "EXECUTING")
    with pytest.raises(TimeoutError, match="resume"):
        tap.query_async(QUERY, tmp_path, wait_seconds=.01, poll_seconds=.005, log=lambda _: None)
    monkeypatch.setattr(tap, "_submit", lambda *_: pytest.fail("Duplicate submission"))
    monkeypatch.setattr(tap, "_get", lambda url, _: "COMPLETED" if url.endswith("/phase") else "source_id\r\n123\r\n")
    assert tap.query_async(QUERY, tmp_path) == [{"source_id":"123"}]
    assert tap.query_async(QUERY, tmp_path) == [{"source_id":"123"}]
