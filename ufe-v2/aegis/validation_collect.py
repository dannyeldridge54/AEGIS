"""AEGIS validation data collector (8 Nov 2026, for field_tests/validation/V1..V5).

Runs beside the star mapper (separate process, polite: one ESA job at a time, low priority). Stdlib only.
1. Gaia DR3 tidal-stream samples for V3 (dark matter vs stars): Sagittarius and GD-1, pulled with the star mapper's
   own resumable async TAP jobs (aegis/tap_async.py). Broad cuts only; membership is decided later, offline, under a
   locked rule. Stream frames are approximate (poles below) and are used only to cut the query region.
2. Release watch for the locked-prediction steps (V1, V2, V4): once a day, ask the arXiv API whether DESI DR3, Euclid
   DR1 cosmology, Gaia DR4 or Simons Observatory results have appeared, and log new papers.
Outputs: ufe-v2/data/validation/  (streams/*.csv via job dirs, release_watch.json, collect_log.txt, status.json)
    python -m aegis.validation_collect            # streams once, then the daily watch forever
    python -m aegis.validation_collect --once     # one pass of each, then exit
"""
import json
import math
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from aegis.tap_async import query_async, AsyncJobBlockedError

ROOT = Path(__file__).resolve().parent.parent / "data" / "validation"
COLS = ("source_id, ra, dec, l, b, parallax, parallax_error, pmra, pmra_error, pmdec, pmdec_error, "
        "phot_g_mean_mag, bp_rp, radial_velocity, radial_velocity_error, ruwe")

# Sagittarius orbital pole, Galactic (Majewski et al. 2003): l = 273.75 deg, b = -13.46 deg. Band |B| < 12 deg.
SGR_LP, SGR_BP, SGR_HALF = 273.75, -13.46, 12.0
# GD-1 pole, ICRS (Koposov et al. 2010): RA = 34.5987 deg, Dec = 29.7331 deg. Band |phi2| < 5 deg.
GD1_RAP, GD1_DECP, GD1_HALF = 34.5987, 29.7331, 5.0


def _band(lon, lat, lon_p, lat_p, half):
    s, c = math.sin(math.radians(lat_p)), math.cos(math.radians(lat_p))
    return (f"ABS(SIN(RADIANS({lat}))*({s:.8f}) + COS(RADIANS({lat}))*({c:.8f})*COS(RADIANS({lon} - {lon_p})))"
            f" < {math.sin(math.radians(half)):.8f}")


def sgr_query(l0, l1):
    return (f"SELECT {COLS} FROM gaiadr3.gaia_source WHERE l >= {l0} AND l < {l1} AND ABS(b) > 8 "
            f"AND {_band('l', 'b', SGR_LP, SGR_BP, SGR_HALF)} "
            f"AND parallax < 0.15 AND phot_g_mean_mag BETWEEN 13 AND 17.5 AND ruwe < 1.4")


def gd1_query(ra0, ra1):
    return (f"SELECT {COLS} FROM gaiadr3.gaia_source WHERE ra >= {ra0} AND ra < {ra1} "
            f"AND {_band('ra', 'dec', GD1_RAP, GD1_DECP, GD1_HALF)} "
            f"AND parallax < 0.5 AND phot_g_mean_mag BETWEEN 15 AND 20.5 AND ruwe < 1.4 "
            f"AND pmra BETWEEN -15 AND 0 AND pmdec BETWEEN -15 AND 2")


CAP = 50000          # ESA returns at most this many rows per anonymous job: a full chunk is TRUNCATED and is split
MIN_WIDTH = 0.25     # deg; narrower chunks are not split further (kept, marked truncated)
STREAMS = {"sgr": (sgr_query, 0.0, 360.0, 30.0), "gd1": (gd1_query, 120.0, 220.0, 25.0)}

WATCH = {
    "DESI DR3": 'ti:"DESI DR3" OR (ti:"DESI" AND ti:"Data Release 3")',
    "Euclid DR1 cosmology": 'ti:"Euclid" AND ti:"DR1" AND (ti:"cosmolog" OR ti:"constraints")',
    "Gaia DR4": 'ti:"Gaia DR4" OR ti:"Gaia Data Release 4"',
    "Simons Observatory first results": 'ti:"Simons Observatory" AND (ti:"first" OR ti:"results") AND ti:"cosmolog"',
}


def log(msg):
    ROOT.mkdir(parents=True, exist_ok=True)
    line = time.strftime("%Y-%m-%d %H:%M:%S ") + msg
    print(line, flush=True)
    with open(ROOT / "collect_log.txt", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def status(update):
    p = ROOT / "status.json"
    st = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    st.update(update)
    p.write_text(json.dumps(st, indent=1), encoding="utf-8")


def _chunk(stream, lo, hi):
    """Fetch one chunk; if it hits the row cap, split it in two and recurse. Returns rows kept."""
    qf = STREAMS[stream][0]
    key = f"{stream}_{lo:07.3f}_{hi:07.3f}"
    done = ROOT / "streams" / f"{key}.done"
    if done.exists():
        info = json.loads(done.read_text(encoding="utf-8"))
        if not info.get("truncated") or hi - lo <= MIN_WIDTH:
            return info["rows"]
    else:
        q = qf(lo, hi)
        log(f"stream job {key} start")
        try:
            rows = query_async(q, ROOT / "streams" / "jobs", wait_seconds=3600, log=lambda m: None)
        except (AsyncJobBlockedError, TimeoutError, OSError, ValueError) as e:
            log(f"stream job {key} NOT DONE: {type(e).__name__}: {str(e)[:300]}")
            status({key: f"not done: {type(e).__name__}"})
            return 0
        n = len(rows)
        trunc = n >= CAP
        (ROOT / "streams").mkdir(parents=True, exist_ok=True)
        done.write_text(json.dumps({"rows": n, "truncated": trunc, "lo": lo, "hi": hi, "query": q}), encoding="utf-8")
        log(f"stream job {key} done: {n} rows" + (" (TRUNCATED at the cap, splitting)" if trunc else ""))
        time.sleep(20)
        if not trunc or hi - lo <= MIN_WIDTH:
            return n
    mid = (lo + hi) / 2
    return _chunk(stream, lo, mid) + _chunk(stream, mid, hi)


def collect_streams():
    for stream, (qf, lo, hi, step) in STREAMS.items():
        total, x = 0, lo
        while x < hi:
            total += _chunk(stream, x, min(x + step, hi))
            x += step
        status({f"{stream}_rows_complete_chunks": total})
        log(f"stream {stream}: {total} rows in complete (untruncated) chunks so far")


def watch_releases():
    p = ROOT / "release_watch.json"
    seen = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    for name, sq in WATCH.items():
        url = ("http://export.arxiv.org/api/query?" +
               urllib.parse.urlencode({"search_query": sq, "sortBy": "submittedDate", "sortOrder": "descending",
                                       "max_results": 10}))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AEGIS-validation-watch"})
            xml = urllib.request.urlopen(req, timeout=60).read()
        except OSError as e:
            log(f"watch {name}: request failed ({e})")
            continue
        ns = {"a": "http://www.w3.org/2005/Atom"}
        entries = [{"id": e.findtext("a:id", "", ns), "title": " ".join(e.findtext("a:title", "", ns).split()),
                    "published": e.findtext("a:published", "", ns)} for e in ET.fromstring(xml).findall("a:entry", ns)]
        baseline = name not in seen
        old = {e["id"] for e in seen.get(name, [])}
        new = [e for e in entries if e["id"] not in old]
        if baseline:
            log(f"watch {name}: baseline of {len(entries)} existing papers recorded (no alert)")
        for e in ([] if baseline else new):
            log(f"WATCH NEW {name}: {e['published'][:10]} {e['title']} {e['id']}")
        seen[name] = (seen.get(name, []) + new)[-50:]
        time.sleep(5)
    p.write_text(json.dumps(seen, indent=1), encoding="utf-8")
    status({"last_watch": time.strftime("%Y-%m-%d %H:%M:%S")})


def main():
    once = "--once" in sys.argv
    import os
    ROOT.mkdir(parents=True, exist_ok=True)
    lock = ROOT / "collector.pid"
    if lock.exists() and time.time() - lock.stat().st_mtime > 26 * 3600:
        lock.unlink()                       # stale: the loop touches it at least daily
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode()); os.close(fd)
    except FileExistsError:
        print(f"another collector is running (delete {lock} if it is not)"); return
    log("collector start (streams then daily release watch)")
    watch_releases()
    collect_streams()
    if once:
        return
    while True:
        lock.touch()
        time.sleep(23 * 3600)
        lock.touch()
        watch_releases()
        collect_streams()          # retries any chunk that did not finish


if __name__ == "__main__":
    main()
