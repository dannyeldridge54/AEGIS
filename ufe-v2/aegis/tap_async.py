"""Durable, bounded public ESA TAP jobs for immutable Gaia range queries."""
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request


ENDPOINT = "https://gea.esac.esa.int/tap-server/tap/async"


class AsyncJobBlockedError(RuntimeError):
    """A durable job cannot safely progress without operator intervention."""


class TerminalJobError(AsyncJobBlockedError):
    """ESA has definitively ended this job; polling it again cannot recover it."""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _submit(query, timeout):
    body = urllib.parse.urlencode({
        "REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv",
        "PHASE": "RUN", "QUERY": query,
    }).encode()
    request = urllib.request.Request(ENDPOINT, data=body, headers={
        "User-Agent": "AEGIS-star-scanner/async",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    try:
        with urllib.request.build_opener(_NoRedirect()).open(request, timeout=timeout) as response:
            raise RuntimeError(f"Expected TAP job redirect, received HTTP {response.status}")
    except urllib.error.HTTPError as error:
        if error.code != 303:
            raise
        return urllib.parse.urljoin(ENDPOINT + "/", error.headers["Location"])


def _get(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read().decode("utf-8", "strict")


def _save(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2), encoding="utf-8")
    temporary.replace(path)


def _rows(text):
    if text.lstrip().startswith("<"):
        raise ValueError("TAP async result is an error/XML page, not CSV")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or "source_id" not in reader.fieldnames:
        raise ValueError("TAP async CSV lacks source_id header")
    rows = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError("TAP async CSV has malformed rows")
    return rows


def query_async(query, job_dir, wait_seconds=900, request_timeout=60, poll_seconds=10, log=print):
    """Resume the same public job after interruption; never silently resubmit."""
    if wait_seconds <= 0 or request_timeout <= 0 or poll_seconds <= 0:
        raise ValueError("TAP time bounds must be positive")
    directory = Path(job_dir)
    directory.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(query.encode()).hexdigest()
    state_path = directory / f"{key}.json"
    result_path = directory / f"{key}.csv"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        if state.get("query") != query:
            raise ValueError("TAP query provenance differs")
        if not state.get("job_url"):
            raise AsyncJobBlockedError(f"TAP submission outcome unknown; inspect {state_path}, do not resubmit")
    else:
        state = {"query": query, "created_unix": time.time(), "phase": "SUBMITTING"}
        with state_path.open("x", encoding="utf-8") as stream:
            json.dump(state, stream)
        # A timeout can occur after acceptance. Keep the intent record for manual recovery.
        state["job_url"] = _submit(query, request_timeout)
        state["phase"] = "SUBMITTED"
        _save(state_path, state)
    job_url = state["job_url"]
    if not re.fullmatch(re.escape(ENDPOINT) + r"/[A-Za-z0-9_-]+", job_url):
        raise ValueError("Unexpected ESA TAP job URL")
    if result_path.exists():
        text = result_path.read_text(encoding="utf-8")
        if state.get("result_sha256") != hashlib.sha256(text.encode()).hexdigest():
            raise ValueError(f"TAP cached result fingerprint differs: {result_path}")
        return _rows(text)
    if state.get("phase") in {"ERROR", "ABORTED"}:
        raise TerminalJobError(f"ESA async job {state['phase']}: {job_url}; preserved at {state_path}")
    deadline = time.monotonic() + wait_seconds
    while time.monotonic() < deadline:
        phase = _get(job_url + "/phase", min(request_timeout, deadline - time.monotonic())).strip()
        state["phase"] = phase
        _save(state_path, state)
        log(f"ESA async job {job_url}: {phase}")
        if phase == "COMPLETED":
            text = _get(job_url + "/results/result", request_timeout).replace("\r\n", "\n").replace("\r", "\n")
            rows = _rows(text)
            temporary = result_path.with_suffix(".csv.tmp")
            with temporary.open("w", encoding="utf-8") as stream:
                stream.write(text)
            state["result_sha256"] = hashlib.sha256(text.encode()).hexdigest()
            _save(state_path, state)
            temporary.replace(result_path)
            return rows
        if phase in {"ERROR", "ABORTED"}:
            raise TerminalJobError(f"ESA async job {phase}: {job_url}; preserved at {state_path}")
        if phase not in {"PENDING", "QUEUED", "EXECUTING", "HELD", "SUSPENDED"}:
            raise AsyncJobBlockedError(f"Unexpected ESA async phase {phase!r}: {job_url}")
        time.sleep(min(poll_seconds, max(0, deadline - time.monotonic())))
    raise TimeoutError(f"ESA async wait exceeded {wait_seconds}s; resume {job_url} using {state_path}")
