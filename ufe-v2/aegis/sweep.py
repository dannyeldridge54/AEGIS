# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: da39abeb145df066
"""AEGIS galaxy sweep: catalogue every Gaia DR3 star with a good parallax, tile by tile.

The sky is cut into 12,288 HEALPix level-5 tiles (about 3.4 square degrees each). Gaia DR3 source_ids encode
their HEALPix pixel, so each tile is one indexed source_id range on the ESA archive: no cone searches, no
2,000-row cap, no duplicates. Tiles are swept in order of angular distance from the Galactic Centre, so the map
fills from the heart of the Milky Way outward.

Storage (cosmos_map/): tiles/L5/<tile>.csv.gz (one gzip CSV per finished tile, same columns as the old catalogue),
sweep_state.json (finished tiles + totals), sweep_view.json (chart sample, spotlight, records, for instant restarts).
Every finished tile is written atomically, so stopping AEGIS at any moment loses at most the tiles in progress.
"""
import csv, gzip, io, json, math, os, random, threading, time

from aegis.healpix_lite import n_tiles, tile_center_radec, tile_source_id_range
from aegis.star_scanner import (STAR_FIELDS, SPOT_KEYS, assess, lower_priority, tap_query, to_galactic)

LEVEL = 5
WORKERS = 2                 # tiles in flight at once (polite to the ESA archive)
PAGE_ROWS = (50000, 20000, 8000)   # rows per request; smaller pages are tried after a timeout
SAMPLE_MAX = 20000
RECENT_STARS = 40
VIEW_SAVE_S = 60
SHELLS_PC = (0, 500, 1000, 2000, 4000, 1e9)   # onion layers: distance shells for the direction analysis
MIN_SKY_FRAC = 0.25                          # fit a shell direction once this much of the sky is swept
SPOT_CHECK_S = 600                           # every 10 min: re-count a random finished tile at ESA and compare

COLS = ("g.source_id, g.ra, g.dec, g.parallax, g.parallax_error, g.pmra, g.pmdec, g.radial_velocity, "
        "g.phot_g_mean_mag, g.bp_rp, g.ruwe, d.r_med_geo, d.r_lo_geo, d.r_hi_geo")


def adql_range(lo, hi, after, top):
    return (f"SELECT TOP {top} {COLS} FROM gaiadr3.gaia_source AS g "
            "LEFT OUTER JOIN external.gaiaedr3_distance AS d ON g.source_id = d.source_id "
            f"WHERE g.source_id BETWEEN {max(lo, after + 1)} AND {hi} AND g.parallax_over_error > 5 "
            "ORDER BY g.source_id")


def adql_count(lo, hi):
    return (f"SELECT COUNT(*) AS n FROM gaiadr3.gaia_source AS g "
            f"WHERE g.source_id BETWEEN {lo} AND {hi} AND g.parallax_over_error > 5")


def _angdist(l1, b1, l2, b2):
    a = math.radians
    c = math.sin(a(b1)) * math.sin(a(b2)) + math.cos(a(b1)) * math.cos(a(b2)) * math.cos(a(l1 - l2))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


class SkySweep:
    def __init__(self, outdir, status=None, log=print, query=tap_query, level=LEVEL):
        self.outdir, self.log, self.query, self.level = outdir, log, query, level
        self.tiledir = os.path.join(outdir, "tiles", f"L{level}")
        os.makedirs(self.tiledir, exist_ok=True)
        self.state_path = os.path.join(outdir, "sweep_state.json")
        self.view_path = os.path.join(outdir, "sweep_view.json")
        self.lock = threading.Lock()
        self.status = status if status is not None else {}
        self.rng = random.Random()
        self.ntiles = n_tiles(level)
        # tile centres (galactic) and sweep order: nearest the Galactic Centre first
        self.centres = []
        for t in range(self.ntiles):
            ra, dec = tile_center_radec(level, t)
            l, b, _ = to_galactic(ra, dec)
            self.centres.append((round(l, 3), round(b, 3)))
        self.order = sorted(range(self.ntiles), key=lambda t: _angdist(self.centres[t][0], self.centres[t][1], 0.0, 0.0))
        self.done = {}            # tile -> {"n", "conf", "flags": {...}}
        self.active = {}          # tile -> {"t0", "rows"}
        self.recent_tiles = []
        self.sample, self.n_sampled, self.recent, self.records = [], 0, [], {}
        self.t_start, self.stars_at_start = time.time(), 0
        self.checks = []          # independent spot-checks: our stored count vs a fresh COUNT at ESA
        self._load()
        self._summary()

    # ---------- persistence ----------
    def _load(self):
        try:
            st = json.load(open(self.state_path, encoding="utf-8"))
            self.done = {int(k): v for k, v in st.get("done", {}).items()}
            self.recent_tiles = st.get("recent_tiles", [])
            self.checks = st.get("checks", [])
        except (OSError, ValueError):
            pass
        for t in list(self.done):                       # a tile only counts if its file exists
            if not os.path.exists(self._tile_path(t)):
                del self.done[t]
        try:
            v = json.load(open(self.view_path, encoding="utf-8"))
            self.sample, self.n_sampled = v.get("sample", []), v.get("n_sampled", 0)
            self.recent, self.records = v.get("recent", []), v.get("records", {})
        except (OSError, ValueError):
            pass
        self.stars_at_start = sum(d["n"] for d in self.done.values())
        if self.done:
            self.log(f"sweep resumed: {len(self.done):,} of {self.ntiles:,} tiles done, {self.stars_at_start:,} stars")

    def _tile_path(self, t):
        return os.path.join(self.tiledir, f"{t:05d}.csv.gz")

    def _save_state(self):
        tmp = self.state_path + ".tmp"
        json.dump({"level": self.level, "done": self.done, "recent_tiles": self.recent_tiles[-30:], "checks": self.checks[-200:]}, open(tmp, "w", encoding="utf-8"))
        os.replace(tmp, self.state_path)

    def _save_view(self):
        with self.lock:
            v = {"sample": self.sample, "n_sampled": self.n_sampled, "recent": self.recent, "records": self.records}
        tmp = self.view_path + ".tmp"
        json.dump(v, open(tmp, "w", encoding="utf-8"))
        os.replace(tmp, self.view_path)

    # ---------- per-star bookkeeping ----------
    _CHART_KEYS = ("l", "b", "x_pc", "y_pc", "z_pc", "dist_pc", "g_mag", "bp_rp", "confirmed", "flags")

    def _note(self, r):
        self.n_sampled += 1
        rec = {k: r[k] for k in self._CHART_KEYS}
        if len(self.sample) < SAMPLE_MAX:
            self.sample.append(rec)
        else:
            j = self.rng.randrange(self.n_sampled)
            if j < SAMPLE_MAX:
                self.sample[j] = rec
        if not r["confirmed"]:
            return
        if self.rng.random() < 0.002:                    # a steady trickle of spotlight stars
            self.recent.append({k: r[k] for k in SPOT_KEYS}); self.recent = self.recent[-RECENT_STARS:]
        d, v = r["dist_pc"], r["vtan_kms"]
        for key, val, better in (("farthest", d, lambda a, b: a > b), ("nearest", d, lambda a, b: a < b),
                                 ("fastest", v, lambda a, b: a > b)):
            if val is None:
                continue
            cur = self.records.get(key)
            if cur is None or better(val, cur["value"]):
                self.records[key] = {"value": val, "star": {k: r[k] for k in SPOT_KEYS}}

    # ---------- the sweep ----------
    def _next_tile(self):
        with self.lock:
            for t in self.order:
                if t not in self.done and t not in self.active:
                    self.active[t] = {"t0": time.time(), "rows": 0}
                    return t
        return None

    def sweep_tile(self, t):
        """Page through one tile and stream it to disk; memory use stays at one page however dense the tile."""
        lo, hi = tile_source_id_range(self.level, t)
        t0, after, page_i, fails = time.time(), lo - 1, 0, 0
        n, conf, flags = 0, 0, {}
        shells = [0] * (len(SHELLS_PC) - 1)
        tmp = self._tile_path(t) + ".tmp"
        with gzip.open(tmp, "wt", newline="", encoding="utf-8", compresslevel=6) as fh:
            w = csv.DictWriter(fh, fieldnames=STAR_FIELDS); w.writeheader()
            while True:
                top = PAGE_ROWS[min(page_i, len(PAGE_ROWS) - 1)]
                try:
                    rows = self.query(adql_range(lo, hi, after, top), timeout=180)
                    fails = 0
                except Exception as e:
                    fails += 1; page_i += 1
                    if fails > 8:
                        raise
                    self.log(f"tile {t}: request failed ({e!r}); retrying with {PAGE_ROWS[min(page_i, len(PAGE_ROWS)-1)]:,}-row pages")
                    time.sleep(min(120, 5 * 2 ** fails))
                    continue
                recs = [r for r in (assess(x) for x in rows) if r is not None]
                w.writerows(recs)
                n += len(recs); conf += sum(1 for r in recs if r["confirmed"])
                for r in recs:
                    for f in filter(None, r["flags"].split(";")):
                        flags[f] = flags.get(f, 0) + 1
                    if r["confirmed"]:
                        d = r["dist_pc"]
                        for k in range(len(shells)):
                            if SHELLS_PC[k] <= d < SHELLS_PC[k + 1]:
                                shells[k] += 1; break
                with self.lock:
                    for r in recs:
                        self._note(r)
                    self.active[t]["rows"] = n
                if len(rows) < top:
                    break
                after = int(rows[-1]["source_id"])
        os.replace(tmp, self._tile_path(t))
        l, b = self.centres[t]
        with self.lock:
            self.done[t] = {"n": n, "conf": conf, "flags": flags, "shells": shells}
            self.active.pop(t, None)
            info = dict(t=time.time(), tile=t, l=l, b=b, stars=n, new=n, confirmed=conf,
                        flagged=sum(flags.values()), seconds=round(time.time() - t0, 1), distances="gaia+bailer-jones")
            self.recent_tiles.append(info); self.recent_tiles = self.recent_tiles[-30:]
            self._save_state()
            self._summary()
        self.log(f"tile {t} done (l {l:.1f}, b {b:+.1f}): {n:,} stars, {conf:,} confirmed, "
                 f"{sum(flags.values()):,} flagged, {time.time() - t0:.1f} s · {len(self.done):,}/{self.ntiles:,} tiles")
        return info

    def _summary(self):
        n = sum(d["n"] for d in self.done.values()); c = sum(d["conf"] for d in self.done.values())
        flags = {}
        for d in self.done.values():
            for k, v in d["flags"].items():
                flags[k] = flags.get(k, 0) + v
        el = max(1.0, time.time() - self.t_start)
        rate = (n - self.stars_at_start) / el * 60
        tiles_rate = max(1e-9, (len(self.done) - getattr(self, "_tiles_at_start", len(self.done))) / el)
        left = self.ntiles - len(self.done)
        self.status.update(dict(
            mode="sweep", level=self.level, tiles_total=self.ntiles, tiles_done=len(self.done),
            patches=len(self.done), stars=n, confirmed=c, confirmed_frac=(c / n) if n else 0.0, flags=flags,
            stars_per_min=rate, eta_s=(left / tiles_rate) if tiles_rate > 1e-6 else None,
            last_patches=[dict(p, ra=0.0, dec=0.0) for p in self.recent_tiles[-15:][::-1]],
            active=[dict(tile=t, l=self.centres[t][0], b=self.centres[t][1], rows=a["rows"]) for t, a in self.active.items()],
            awaiting_recheck=0, workers=WORKERS,
            checks_total=len(self.checks), checks_passed=sum(1 for c in self.checks if c["match"]),
            last_checks=self.checks[-5:][::-1],
            query_template=adql_range(0, 0, -1, PAGE_ROWS[0]).replace("BETWEEN 0 AND 0", "BETWEEN <tile start> AND <tile end>")))

    # ---------- API for the monitor ----------
    def chart_points(self, limit=SAMPLE_MAX):
        with self.lock:
            return list(self.sample[:limit])

    def spotlight(self):
        with self.lock:
            return {"recent": list(self.recent[::-1]), "records": dict(self.records)}

    def tiles_map(self):
        with self.lock:
            return {"level": self.level, "total": self.ntiles,
                    "done": [[self.centres[t][0], self.centres[t][1], d["n"]] for t, d in self.done.items()],
                    "active": [[self.centres[t][0], self.centres[t][1], a["rows"]] for t, a in self.active.items()]}

    def shell_directions(self):
        """Onion analysis: for each distance shell, fit star counts per swept tile as N = a (1 + d . u), where u is
        the tile's unit vector, by least squares over the tiles swept so far (a masked dipole fit, so the order of the
        sweep does not bias the direction). Returns the direction (l, b) and strength |d| of the excess per shell."""
        import numpy as np
        with self.lock:
            items = [(t, d["shells"]) for t, d in self.done.items() if "shells" in d]
        frac = len(items) / self.ntiles
        out = {"sky_fraction": frac, "min_sky_fraction": MIN_SKY_FRAC, "shells": []}
        if not items:
            return out
        U = []
        for t, _ in items:
            l, b = (math.radians(v) for v in self.centres[t])
            U.append((math.cos(b) * math.cos(l), math.cos(b) * math.sin(l), math.sin(b)))
        U = np.array(U); X = np.column_stack([np.ones(len(U)), U])
        C = np.array([sh for _, sh in items], dtype=float)
        for k in range(C.shape[1]):
            lo, hi = SHELLS_PC[k], SHELLS_PC[k + 1]
            row = {"lo_pc": lo, "hi_pc": None if hi > 1e8 else hi, "stars": int(C[:, k].sum())}
            if frac >= MIN_SKY_FRAC and C[:, k].sum() > 1000:
                coef, *_ = np.linalg.lstsq(X, C[:, k], rcond=None)
                a, v = coef[0], coef[1:]
                if a > 0:
                    dvec = v / a; amp = float(np.linalg.norm(dvec))
                    # guardrail: noise level of the dipole from the fit residuals (least-squares covariance)
                    resid = C[:, k] - X @ coef; dof = max(1, len(C) - 4)
                    cov = np.linalg.pinv(X.T @ X) * float(resid @ resid) / dof
                    sig_amp = float(np.sqrt(max(1e-30, np.trace(cov[1:, 1:]) / 3))) / a
                    row["sigma"] = amp / sig_amp if sig_amp > 0 else 0.0
                    row.update(amplitude=amp, l=float(math.degrees(math.atan2(dvec[1], dvec[0])) % 360),
                               b=float(math.degrees(math.asin(max(-1, min(1, dvec[2] / amp))))) if amp > 0 else 0.0)
            out["shells"].append(row)
        return out

    @property
    def seen(self):            # compatibility with the old scanner's log line
        return range(sum(d["n"] for d in self.done.values()))

    def _worker(self, stop):
        while not stop():
            t = self._next_tile()
            if t is None:
                self.log("sweep complete: every tile catalogued"); return
            try:
                self.sweep_tile(t)
            except Exception as e:
                with self.lock:
                    self.active.pop(t, None)
                self.log(f"tile {t} failed ({e!r}); will retry later"); time.sleep(30)

    def spot_check(self):
        """Pick a random finished tile, ask ESA for a fresh count with the same filter, compare with what we stored."""
        with self.lock:
            if not self.done:
                return None
            t = self.rng.choice(list(self.done)); ours = self.done[t]["n"]
        lo, hi = tile_source_id_range(self.level, t)
        rows = self.query(adql_count(lo, hi), timeout=120)
        theirs = int(rows[0]["n"])
        c = {"t": time.time(), "tile": t, "ours": ours, "esa": theirs, "match": ours == theirs}
        with self.lock:
            self.checks.append(c); self.checks = self.checks[-200:]
            self._save_state(); self._summary()
        self.log(f"spot-check tile {t}: AEGIS stored {ours:,} stars, ESA counts {theirs:,} -> {'MATCH' if c['match'] else 'MISMATCH'}")
        return c

    def _checker(self, stop):
        time.sleep(int(os.environ.get("AEGIS_CHECK_DELAY", "120")))
        while not stop():
            try:
                self.spot_check()
            except Exception as e:
                self.log(f"spot-check could not reach ESA ({e!r}); will try again")
            time.sleep(SPOT_CHECK_S)

    def _view_saver(self, stop):
        while not stop():
            time.sleep(VIEW_SAVE_S)
            try:
                self._save_view()
            except Exception as e:
                self.log(f"could not save the chart view ({e!r})")
            with self.lock:
                self._summary()

    def run_forever(self):
        lower_priority()
        self._tiles_at_start = len(self.done); self.t_start = time.time()
        stop = lambda: False
        threads = [threading.Thread(target=self._worker, args=(stop,), daemon=True) for _ in range(WORKERS)]
        threads.append(threading.Thread(target=self._view_saver, args=(stop,), daemon=True))
        threads.append(threading.Thread(target=self._checker, args=(stop,), daemon=True))
        for th in threads:
            th.start()
        for th in threads:
            th.join()
