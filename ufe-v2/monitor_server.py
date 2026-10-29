"""AEGIS v2 — continuous star-catalog scanner and live monitor (for the cosmos mapper).

Runs the Gaia DR3 star scanner forever (aegis/star_scanner.py) and serves:

    http://localhost:8765/               live dashboard: sky chart, galaxy map, flags, scan log
    http://localhost:8765/api/status     JSON: totals, flag counts, recent patches
    http://localhost:8765/api/stars      JSON: charted stars (downsampled to 20,000)
    http://localhost:8765/api/flags      CSV:  flagged candidates
    http://localhost:8765/api/catalog    CSV:  the full star catalog for the mapper
    http://localhost:8765/api/log        plain-text log
    http://localhost:8765/live           livestream view (1920x1080, for OBS "Browser source")
    http://localhost:8765/api/spotlight  JSON: recent confirmed stars and session records
    http://localhost:8765/api/tiles      JSON: galaxy-sweep tiles done / in progress (galactic l, b, stars)
    http://localhost:8765/tiles/L5/NNNNN.csv.gz   raw data of one swept tile (gzip CSV)
    http://localhost:8765/api/science    JSON: torsion-field fit results shown on the stream
    http://localhost:8765/api/guardrails JSON: automatic checks on our own math (fits, pre-registration, theory, data, geometry, authorship)

Data files are written to ./cosmos_map/ and survive restarts (scanning resumes where it left off).
Start: python monitor_server.py   (Windows: double-click START_AEGIS_MONITOR.bat). Stop: close the window.
"""
import json, os, re, sys, threading, time, traceback, webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PORT = int(os.environ.get("AEGIS_MONITOR_PORT", "8765"))
MODE = os.environ.get("AEGIS_MODE", "sweep")   # "sweep" (default) or "random"
OUT = os.path.join(HERE, "cosmos_map")

STATUS = {"state": "starting", "started": time.time(), "error": None}
LOG = []
LOCK = threading.Lock()
SCANNER = {}

def log(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line, flush=True)
    with LOCK:
        LOG.append(line)
        try:
            with open(os.path.join(HERE, "monitor_log.txt"), "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except Exception:
            pass

def worker():
    try:
        from aegis.star_scanner import StarScanner
        from aegis.sweep import SkySweep
        scan_status = {}
        try:                                                      # show the last saved numbers while the catalogue loads
            scan_status.update(json.load(open(os.path.join(OUT, "star_scan_summary.json"), encoding="utf-8")))
        except Exception:
            pass
        SCANNER["status"] = scan_status
        with LOCK:
            STATUS["state"] = "loading"
        if MODE == "random":   # the old random-patch scanner (kept for reference)
            log("loading the star catalogue (about 2 minutes for ~2 million stars)...")
            S = StarScanner(OUT, status=scan_status, log=log)
        else:                  # default: systematic galaxy sweep, tile by tile from the Galactic Centre outward
            S = SkySweep(OUT, status=scan_status, log=log)
        SCANNER["s"], SCANNER["status"] = S, scan_status
        with LOCK:
            STATUS["state"] = "scanning"
        log(f"scanner ready: {len(S.seen):,} stars already catalogued; " +
            ("scanning random sky patches" if MODE == "random" else "sweeping the galaxy tile by tile from the Galactic Centre outward"))
        S.run_forever()
    except Exception:
        with LOCK:
            STATUS["state"] = "error"; STATUS["error"] = traceback.format_exc()
        log("ERROR: " + STATUS["error"].splitlines()[-1])

def _read(path, default=""):
    return open(path, encoding="utf-8").read() if os.path.exists(path) else default

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        b = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b))); self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        p = self.path.split("?")[0]
        if p == "/api/status":
            with LOCK:
                s = dict(STATUS); s["uptime_s"] = time.time() - STATUS["started"]
                s["scan"] = {k: v for k, v in SCANNER.get("status", {}).items() if k != "recent_stars"}
            self._send(200, json.dumps(s), "application/json")
        elif p == "/api/stars":
            pts = SCANNER["s"].chart_points() if "s" in SCANNER else []
            self._send(200, json.dumps(pts), "application/json")
        elif p == "/api/flags":
            self._send(200, _read(os.path.join(OUT, "cosmos_map_flags.csv")), "text/csv; charset=utf-8")
        elif p == "/api/catalog":
            self._send(200, _read(os.path.join(OUT, "cosmos_map_stars.csv")), "text/csv; charset=utf-8")
        elif p == "/api/log":
            with LOCK:
                self._send(200, "\n".join(LOG[-500:]), "text/plain; charset=utf-8")
        elif p == "/api/tiles":
            tm = SCANNER["s"].tiles_map() if "s" in SCANNER and hasattr(SCANNER["s"], "tiles_map") else {"done": [], "active": [], "total": 0}
            self._send(200, json.dumps(tm), "application/json")
        elif re.fullmatch(r"/tiles/L\d/\d{5}\.csv\.gz", p):        # raw swept tiles, for anyone who wants to check the data
            fp = os.path.join(OUT, *p.strip("/").split("/"))
            if os.path.exists(fp):
                self._send(200, open(fp, "rb").read(), "application/gzip")
            else:
                self._send(404, "tile not swept yet", "text/plain")
        elif p == "/api/shells":
            sd = SCANNER["s"].shell_directions() if "s" in SCANNER and hasattr(SCANNER["s"], "shell_directions") else {"shells": []}
            self._send(200, json.dumps(sd), "application/json")
        elif p == "/api/spotlight":
            sp = SCANNER["s"].spotlight() if "s" in SCANNER else {"recent": [], "records": {}}
            self._send(200, json.dumps(sp), "application/json")
        elif re.fullmatch(r"/sigils/[a-z0-9_]+\.(svg|json|jpg)", p):        # Danny's sigils and their authorship hashes
            fp = os.path.join(HERE, "sigils", p.split("/")[-1])
            if os.path.exists(fp):
                self._send(200, open(fp, "rb").read(), {"svg": "image/svg+xml", "jpg": "image/jpeg"}.get(fp.rsplit(".", 1)[-1], "application/json"))
            else:
                self._send(404, "not found", "text/plain")
        elif p == "/api/guardrails":                              # automatic checks on our own math
            from aegis.guardrails import run_all
            S = SCANNER.get("s")
            shells = S.shell_directions() if S is not None and hasattr(S, "shell_directions") else None
            res = run_all(status=SCANNER.get("status", {}), shells=shells)
            self._send(200, json.dumps(res, ensure_ascii=False), "application/json")
        elif p == "/api/science":
            self._send(200, _read(os.path.join(HERE, "science.json"), "{}"), "application/json")
        elif p == "/api/method":                                  # the claim store: every claim, its tier and its fate
            from aegis import method as M
            st = M.load()
            self._send(200, json.dumps({"claims": M.ledger(st), "threads": st["threads"], "check": M.check(st)}, ensure_ascii=False).encode("utf-8"),
                       "application/json; charset=utf-8")
        elif p in ("/method", "/method.html"):
            self._send(200, _read(os.path.join(HERE, "method.html")), "text/html; charset=utf-8")
        elif p in ("/locked", "/locked.html"):
            self._send(200, _read(os.path.join(HERE, "locked.html")), "text/html; charset=utf-8")
        elif p in ("/live", "/live.html"):
            self._send(200, _read(os.path.join(HERE, "live.html")), "text/html; charset=utf-8")
        elif p in ("/", "/index.html"):
            self._send(200, _read(os.path.join(HERE, "monitor.html")), "text/html; charset=utf-8")
        else:
            self._send(404, "not found", "text/plain")
    def log_message(self, *a):
        pass

def single_instance():
    """Only one AEGIS scanner may write the catalogue at a time: hold an OS lock on cosmos_map/.scanner.lock."""
    os.makedirs(OUT, exist_ok=True)
    fh = open(os.path.join(OUT, ".scanner.lock"), "a+")
    try:
        if os.name == "nt":
            import msvcrt
            fh.seek(0); msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("\nAEGIS is already running in another window. Close every AEGIS window, then start it once.\n"
              "(Your browser can still use the running copy at http://localhost:%d/)" % PORT, flush=True)
        try:
            input("Press Enter to close this window...")
        except Exception:
            pass
        sys.exit(1)
    return fh

if __name__ == "__main__":
    _lock = single_instance()
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=worker, daemon=True).start()
    url = f"http://localhost:{PORT}/"
    log(f"AEGIS star scanner monitor at {url}   (API: {url}api/status)")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    srv.serve_forever()
