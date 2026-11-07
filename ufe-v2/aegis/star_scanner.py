# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 with the Military Activities and Mass Surveillance modules (HL3-MIL-SV; see LICENSE): free to everyone, for any use that respects human rights. AEGIS-ID: 67b917a1edbfc415
"""AEGIS star scanner — continuous Gaia DR3 sky survey for the cosmos mapper.

Scan:    pick a random point on the sky (uniform on the sphere), query the ESA Gaia archive for the
         stars inside a 0.75-degree circle (the circle is halved or quartered, and the radius is logged, if the
         archive times out) with a measured parallax (parallax_over_error > 5). The archive returns at most
         2000 rows per patch with no ordering, so a patch of exactly 2000 is truncated: do not use per-patch
         star counts as a density.
Quality pass: the legacy `confirmed` field is true when inverse-parallax distance
         is consistent with the Bailer-Jones et al. (2021) geometric-distance interval
         and RUWE < 1.4. Both distance estimates use Gaia astrometry; this is a
         consistency/quality heuristic, not independent confirmation.
Chart:   every star gets galactic coordinates (l, b) and a 3D position (x, y, z in parsecs, Sun at origin,
         x toward the Galactic centre) for the interactive map.
Flag:    CANDIDATES for follow-up (not discoveries):
           high_velocity       tangential speed > 400 km/s (halo or high-velocity star candidates)
           astrometric_excess  RUWE > 1.4 (often an unresolved binary companion)
           distance_mismatch   inverse-parallax distance differs from the Bailer-Jones median by > 3x the 16-84% width
         Each flag says what it is and what would confirm it.

Output (in the folder passed to StarScanner):
  cosmos_map_stars.csv      one row per unique star (all scans), ready for the mapper
  cosmos_map_patches.jsonl  every scanned patch, one JSON line each (ra, dec, stars found, confirmed, time)
  cosmos_map_flags.csv      flagged candidates with the reason
  star_scan_summary.json    totals for the dashboard / API

Uses only the Python standard library plus numpy. Data: ESA Gaia DR3 (Gaia Collaboration 2023),
distances from Bailer-Jones et al. 2021 (AJ 161, 147), served by the ESA Gaia archive TAP service.
"""
import csv, io, json, math, os, random, threading, time, urllib.parse, urllib.request
import numpy as np

TAP_SYNC = "https://gea.esac.esa.int/tap-server/tap/sync"
RADIUS_DEG = 0.75     # sky patch radius
MAX_ROWS = 2000       # archive limit for synchronous queries
WORKERS = 2           # queries in flight at once (network-bound, light on CPU)
MIN_CYCLE_S = 4.0     # per worker: at most one query every 4 s (polite to the public archive)
SAMPLE_MAX = 20000    # stars kept in memory for the live charts (reservoir sample)
RECENT_PATCHES = 200  # patches kept in memory; full history is appended to cosmos_map_patches.jsonl
RECHECK_BATCH = 400   # stars re-checked per query by the re-confirm worker
REWRITE_EVERY_S = 1800   # write re-checked stars back into the catalogue at most every 30 min (the file is large)
REWRITE_BATCH = 150_000   # ... or sooner once this many stars are waiting to be written

ASTROMETRY_FIELDS = (
    "parallax", "ref_epoch", "astrometric_params_solved", "nu_eff_used_in_astrometry",
    "pseudocolour", "ecl_lat", "ra_error", "dec_error", "ra_dec_corr",
    "ra_parallax_corr", "ra_pmra_corr", "ra_pmdec_corr", "dec_parallax_corr",
    "dec_pmra_corr", "dec_pmdec_corr", "parallax_pmra_corr", "parallax_pmdec_corr",
    "radial_velocity_error",
)
COLUMNS = ["source_id", "ra", "dec", "parallax", "parallax_error", "pmra", "pmra_error", "pmdec",
           "pmdec_error", "pmra_pmdec_corr", "radial_velocity",
           "phot_g_mean_mag", "bp_rp", "ruwe", "r_med_geo", "r_lo_geo", "r_hi_geo"]
GAIA_QUERY_FIELDS = tuple(dict.fromkeys(
    [column for column in COLUMNS if not column.startswith("r_")] + list(ASTROMETRY_FIELDS)
))
GAIA_SELECT = ", ".join(f"g.{column}" for column in GAIA_QUERY_FIELDS)

def adql(ra0, dec0, join=True, radius=None):
    g = GAIA_SELECT
    where = (f"WHERE 1=CONTAINS(POINT('ICRS', g.ra, g.dec), CIRCLE('ICRS', {ra0:.6f}, {dec0:.6f}, {radius or RADIUS_DEG})) "
             "AND g.parallax_over_error > 5")
    if join:
        return (f"SELECT TOP {MAX_ROWS} {g}, d.r_med_geo, d.r_lo_geo, d.r_hi_geo "
                "FROM gaiadr3.gaia_source AS g LEFT OUTER JOIN external.gaiaedr3_distance AS d "
                f"ON g.source_id = d.source_id {where}")
    return f"SELECT TOP {MAX_ROWS} {g} FROM gaiadr3.gaia_source AS g {where}"

def adql_by_id(ids):
    """Re-query specific stars (by Gaia source_id) with both distance sources."""
    idlist = ",".join(str(int(i)) for i in ids)
    return (f"SELECT {GAIA_SELECT}, d.r_med_geo, d.r_lo_geo, d.r_hi_geo "
            "FROM gaiadr3.gaia_source AS g LEFT OUTER JOIN external.gaiaedr3_distance AS d "
            f"ON g.source_id = d.source_id WHERE g.source_id IN ({idlist})")

def tap_query(query, timeout=90):
    body = urllib.parse.urlencode({"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv",
                                   "QUERY": query}).encode()
    req = urllib.request.Request(TAP_SYNC, data=body, headers={"User-Agent": "AEGIS-star-scanner/2.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        text = r.read().decode("utf-8", "replace")
    if text.lstrip().startswith("<"):
        raise RuntimeError("archive returned an error page: " + text[:300].replace("\n", " "))
    return list(csv.DictReader(io.StringIO(text)))

def _f(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None

# ICRS -> Galactic rotation (Hipparcos / Gaia convention)
_R = np.array([[-0.0548755604162154, -0.8734370902348850, -0.4838350155487132],
               [ 0.4941094278755837, -0.4448296299600112,  0.7469822444972189],
               [-0.8676661490190047, -0.1980763734312015,  0.4559837761750669]])

def to_galactic(ra, dec):
    a, d = math.radians(ra), math.radians(dec)
    v = _R @ np.array([math.cos(d) * math.cos(a), math.cos(d) * math.sin(a), math.sin(d)])
    l = math.degrees(math.atan2(v[1], v[0])) % 360.0
    b = math.degrees(math.asin(max(-1.0, min(1.0, v[2]))))
    return l, b, v

def assess(row):
    """Return one Gaia chart record, including the legacy distance-quality flag and candidate flags."""
    plx, eplx = _f(row.get("parallax")), _f(row.get("parallax_error"))
    ra, dec = _f(row.get("ra")), _f(row.get("dec"))
    if None in (plx, eplx, ra, dec) or plx <= 0:
        return None
    ruwe = _f(row.get("ruwe"))
    d_plx = 1000.0 / plx
    rmed, rlo, rhi = _f(row.get("r_med_geo")), _f(row.get("r_lo_geo")), _f(row.get("r_hi_geo"))
    has_bj = None not in (rmed, rlo, rhi)
    if has_bj and (rlo <= 0 or rhi <= rlo or not rlo <= rmed <= rhi):
        raise ValueError(f"Invalid Bailer-Jones distance interval for source {row.get('source_id')}")
    agree = has_bj and (rlo <= d_plx <= rhi or abs(d_plx - rmed) <= 2 * 1000.0 * eplx / plx**2)
    good_fit = ruwe is not None and ruwe < 1.4
    quality_pass = bool(agree and good_fit)
    dist = rmed if has_bj else d_plx
    l, b, unit = to_galactic(ra, dec)
    x, y, z = (unit * dist).tolist()
    pmra, pmdec = _f(row.get("pmra")), _f(row.get("pmdec"))
    vtan = 4.74047 * math.hypot(pmra, pmdec) * dist / 1000.0 if None not in (pmra, pmdec) else None
    flags = []
    if vtan is not None and vtan > 400:
        flags.append(("high_velocity", f"tangential speed {vtan:.0f} km/s; confirm with a radial velocity and orbit"))
    if ruwe is not None and ruwe > 1.4:
        flags.append(("astrometric_excess", f"RUWE {ruwe:.2f}; possible unresolved binary, check Gaia DR3 NSS tables"))
    if has_bj and (rhi - rlo) > 0 and abs(d_plx - rmed) > 3 * (rhi - rlo):
        flags.append(("distance_mismatch", f"1/parallax {d_plx:.0f} pc vs Bailer-Jones {rmed:.0f} pc "
                                           f"[{rlo:.0f}-{rhi:.0f}]; check zero-point and crowding"))
    record = dict(source_id=row.get("source_id"), ra=ra, dec=dec, parallax_error=eplx,
                pmra_error=_f(row.get("pmra_error")), pmdec_error=_f(row.get("pmdec_error")),
                pmra_pmdec_corr=_f(row.get("pmra_pmdec_corr")),
                r_lo_geo=rlo if has_bj else None, r_hi_geo=rhi if has_bj else None,
                l=round(l, 5), b=round(b, 5),
                dist_pc=round(dist, 2), dist_plx_pc=round(d_plx, 2), dist_bj_pc=rmed,
                x_pc=round(x, 2), y_pc=round(y, 2), z_pc=round(z, 2),
                g_mag=_f(row.get("phot_g_mean_mag")), bp_rp=_f(row.get("bp_rp")), ruwe=ruwe,
                pmra=pmra, pmdec=pmdec, rv=_f(row.get("radial_velocity")),
                vtan_kms=round(vtan, 1) if vtan is not None else None,
                astrometric_quality_pass=quality_pass, confirmed=quality_pass,
                flags=";".join(f[0] for f in flags), flag_notes=" | ".join(f[1] for f in flags))
    record.update({field: _f(row.get(field)) for field in ASTROMETRY_FIELDS})
    return record

SPOT_KEYS = ("source_id", "ra", "dec", "l", "b", "dist_pc", "g_mag", "bp_rp", "ruwe", "vtan_kms", "rv",
             "parallax_error", "pmra_error", "pmdec_error", "pmra_pmdec_corr", "r_lo_geo", "r_hi_geo", "flags")
RECENT_STARS = 40

STAR_FIELDS = ["source_id", "ra", "dec", "l", "b", "dist_pc", "dist_plx_pc", "dist_bj_pc", "x_pc", "y_pc", "z_pc",
               "g_mag", "bp_rp", "ruwe", "pmra", "pmdec", "rv", "vtan_kms",
               "astrometric_quality_pass", "confirmed", "flags", "flag_notes",
               "parallax_error", "pmra_error", "pmdec_error", "pmra_pmdec_corr", "r_lo_geo", "r_hi_geo",
               *ASTROMETRY_FIELDS]

def lower_priority():
    """Run below normal CPU priority so the PC stays responsive (Windows; harmless elsewhere)."""
    try:
        if os.name == "nt":
            import ctypes
            ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
        else:
            os.nice(5)
    except Exception:
        pass

class StarScanner:
    def __init__(self, outdir, status=None, log=print, seed=None, query=tap_query):
        os.makedirs(outdir, exist_ok=True)
        self.outdir, self.log, self.query = outdir, log, query
        self.rng = random.Random(seed)
        self.lock = threading.Lock()
        self.status = status if status is not None else {}
        self.stars_path = os.path.join(outdir, "cosmos_map_stars.csv")
        self.flags_path = os.path.join(outdir, "cosmos_map_flags.csv")
        self.patch_path = os.path.join(outdir, "cosmos_map_patches.jsonl")
        self.seen = set(); self.n_conf = 0; self.flag_counts = {}; self.patches = []; self.n_patches = 0
        self.sample = []; self.n_sampled = 0
        self.recent = []; self.records = {}
        self.needs_check = []; self.updates = {}; self.n_rechecked = 0; self.last_rewrite = time.time()
        for path in (self.stars_path, self.flags_path):           # repair: drop duplicate or broken rows (e.g. two scanners ran at once)
            if os.path.exists(path):
                self._dedupe(path)
        if os.path.exists(self.stars_path):                      # resume: read the catalogue once
            for r in csv.DictReader(open(self.stars_path, newline="", encoding="utf-8")):
                self.seen.add(r["source_id"]); self.n_conf += r["confirmed"] == "True"
                if not r.get("dist_bj_pc"):
                    self.needs_check.append(r["source_id"])
                for f in filter(None, r["flags"].split(";")):
                    self.flag_counts[f] = self.flag_counts.get(f, 0) + 1
                self._add_sample(r); self._note_record(r)
                if r["confirmed"] == "True":                     # seed the stream spotlight with recent quality-pass rows
                    self.recent.append({k: r.get(k) for k in SPOT_KEYS}); self.recent = self.recent[-RECENT_STARS:]
        old_json = os.path.join(outdir, "cosmos_map_patches.json")       # earlier format: convert once
        if os.path.exists(old_json) and not os.path.exists(self.patch_path):
            try:
                with open(self.patch_path, "w", encoding="utf-8") as fh:
                    for pch in json.load(open(old_json)): fh.write(json.dumps(pch) + "\n")
                os.replace(old_json, old_json + ".converted")
            except Exception:
                pass
        if os.path.exists(self.patch_path):
            for line in open(self.patch_path, encoding="utf-8"):
                try: self.patches.append(json.loads(line)); self.n_patches += 1
                except Exception: pass
            self.patches = self.patches[-RECENT_PATCHES:]
        self._summary()

    _CHART_KEYS = ("l", "b", "x_pc", "y_pc", "z_pc", "dist_pc", "g_mag", "bp_rp",
                   "parallax_error", "pmra_error", "pmdec_error", "pmra_pmdec_corr", "r_lo_geo", "r_hi_geo",
                   "astrometric_quality_pass", "confirmed", "flags")
    def _add_sample(self, r):
        """Reservoir sampling: a fair random subset of all stars, fixed size, O(1) per star."""
        self.n_sampled += 1
        rec = {k: r.get(k) for k in self._CHART_KEYS if k != "astrometric_quality_pass"}
        rec["astrometric_quality_pass"] = r.get("astrometric_quality_pass", r.get("confirmed"))
        if len(self.sample) < SAMPLE_MAX:
            self.sample.append(rec)
        else:
            j = self.rng.randrange(self.n_sampled)
            if j < SAMPLE_MAX:
                self.sample[j] = rec

    def _dedupe(self, path):
        """Rewrite a catalogue file keeping the first copy of each star and only well-formed rows. Streaming, O(stars) memory."""
        seen, kept, dropped = set(), 0, 0
        tmp = path + ".dedupe"
        with open(path, newline="", encoding="utf-8", errors="replace") as fin, open(tmp, "w", newline="", encoding="utf-8") as fout:
            reader = csv.DictReader(fin)
            schema_changed = reader.fieldnames != STAR_FIELDS
            w = csv.DictWriter(fout, fieldnames=STAR_FIELDS); w.writeheader()
            for r in reader:
                sid = (r.get("source_id") or "").strip()
                legacy_quality = r.get("astrometric_quality_pass", r.get("confirmed"))
                ok = sid.isdigit() and sid not in seen and legacy_quality in ("True", "False") and None not in r
                if not ok:
                    dropped += 1; continue
                seen.add(sid)
                normalized = {k: r.get(k, "") for k in STAR_FIELDS}
                normalized["astrometric_quality_pass"] = legacy_quality
                w.writerow(normalized); kept += 1
        if dropped or schema_changed:
            os.replace(tmp, path)
            self.log(f"catalogue repair: kept {kept:,} stars in {os.path.basename(path)}, "
                     f"removed {dropped:,} duplicate or broken rows; schema updated={schema_changed}")
        else:
            os.remove(tmp)

    def _note_record(self, r):
        """Track extrema among rows that pass the distance-quality heuristic."""
        if r["confirmed"] not in (True, "True"):
            return
        try:
            d = float(r["dist_pc"])
            v = float(r["vtan_kms"]) if r.get("vtan_kms") not in (None, "") else None
        except (TypeError, ValueError):
            return
        star = {k: r.get(k) for k in SPOT_KEYS}
        for key, val, better in (("farthest", d, lambda a, b: a > b), ("nearest", d, lambda a, b: a < b),
                                 ("fastest", v, lambda a, b: a > b)):
            if val is None:
                continue
            cur = self.records.get(key)
            if cur is None or better(val, cur["value"]):
                self.records[key] = {"value": val, "star": star}

    def spotlight(self):
        """Recent distance-quality-pass stars and session records, for the livestream page."""
        with self.lock:
            return {"recent": list(self.recent[::-1]), "records": dict(self.records)}

    def random_point(self):
        ra = self.rng.uniform(0, 360)
        dec = math.degrees(math.asin(self.rng.uniform(-1, 1)))
        return ra, dec

    def scan_once(self):
        with self.lock:
            ra0, dec0 = self.random_point()
        t0 = time.time()
        # Try with both distance sources; on a timeout (dense sky), shrink the circle and retry.
        # Only as a last resort for THIS patch, fall back to Gaia parallaxes alone (marked in the output).
        rows, use_join, used_radius = None, True, RADIUS_DEG
        for radius in (RADIUS_DEG, RADIUS_DEG / 2, RADIUS_DEG / 4):
            try:
                rows = self.query(adql(ra0, dec0, True, radius))   # network wait happens outside the lock
                used_radius = radius
                break
            except Exception as e:
                self.log(f"patch at RA {ra0:.2f}, Dec {dec0:+.2f}: query with r={radius:.2f} deg failed ({e!r})")
        if rows is None:
            use_join, used_radius = False, RADIUS_DEG / 4
            rows = self.query(adql(ra0, dec0, False, RADIUS_DEG / 4))
        recs = [r for r in (assess(x) for x in rows) if r is not None]
        with self.lock:
            new, patch_seen = [], set()
            for record in recs:
                source_id = record["source_id"]
                if source_id not in self.seen and source_id not in patch_seen:
                    new.append(record)
                    patch_seen.add(source_id)
            write_header = not os.path.exists(self.stars_path)
            with open(self.stars_path, "a", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=STAR_FIELDS)
                if write_header: w.writeheader()
                w.writerows(new)
            flagged = [r for r in new if r["flags"]]
            if flagged:
                fh_new = not os.path.exists(self.flags_path)
                with open(self.flags_path, "a", newline="", encoding="utf-8") as fh:
                    w = csv.DictWriter(fh, fieldnames=STAR_FIELDS)
                    if fh_new: w.writeheader()
                    w.writerows(flagged)
            for r in new:
                self.seen.add(r["source_id"]); self.n_conf += r["confirmed"]
                for f in filter(None, r["flags"].split(";")):
                    self.flag_counts[f] = self.flag_counts.get(f, 0) + 1
                self._add_sample(r); self._note_record(r)
                if r["confirmed"]:
                    self.recent.append({k: r[k] for k in SPOT_KEYS}); self.recent = self.recent[-RECENT_STARS:]
                if r["dist_bj_pc"] is None:
                    self.needs_check.append(r["source_id"])
            l0, b0, _ = to_galactic(ra0, dec0)
            patch = dict(t=time.time(), ra=round(ra0, 4), dec=round(dec0, 4), l=round(l0, 4), b=round(b0, 4),
                         stars=len(recs), new=len(new), confirmed=sum(r["confirmed"] for r in new),
                         flagged=len(flagged), seconds=round(time.time() - t0, 1), radius_deg=used_radius,
                         truncated=len(rows) >= MAX_ROWS,
                         distances=("gaia+bailer-jones" if use_join else "gaia parallax only"))
            with open(self.patch_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(patch) + "\n")
            self.patches.append(patch); self.n_patches += 1
            self.patches = self.patches[-RECENT_PATCHES:]
            self._summary()
            n = self.n_patches
        self.log(f"patch {n} at RA {ra0:.2f}, Dec {dec0:+.2f} (l {l0:.1f}, b {b0:+.1f}): "
             f"{len(recs)} row encounters, {len(new)} new unique source IDs, "
             f"{patch['confirmed']} distance-quality passes, {len(flagged)} flagged, {patch['seconds']} s")
        return patch

    def recheck_once(self):
        """Re-query stars that were catalogued without the Bailer-Jones distance and upgrade them."""
        with self.lock:
            batch = self.needs_check[:RECHECK_BATCH]
        if not batch:
            return 0
        rows = self.query(adql_by_id(batch))
        recs = {r["source_id"]: r for r in (assess(x) for x in rows) if r is not None}
        with self.lock:
            self.needs_check = self.needs_check[len(batch):]      # batch was taken from the front; new stars are appended
            for sid, r in recs.items():
                if r["dist_bj_pc"] is not None and sid not in self.updates:
                    self.updates[sid] = r
                    self.n_conf += bool(r["confirmed"])          # live count; the rewrite recomputes it exactly
            self.n_rechecked += len(batch)
            self._summary()
            if self.updates and (time.time() - self.last_rewrite > REWRITE_EVERY_S or len(self.updates) >= REWRITE_BATCH):
                self._rewrite_catalogue()
        self.log(f"re-checked {len(batch)} stars ({sum(r['confirmed'] for r in recs.values())} now pass the distance-quality rule); "
                 f"{len(self.needs_check)} left to re-check")
        return len(batch)

    def _rewrite_catalogue(self):
        """Apply re-checked rows to the catalogue (atomic replace) and rebuild the counts. Caller holds the lock."""
        tmp = self.stars_path + ".tmp"; ftmp = self.flags_path + ".tmp"
        self.n_conf = 0; self.flag_counts = {}; self.sample = []; self.n_sampled = 0
        with open(self.stars_path, newline="", encoding="utf-8") as fin, \
             open(tmp, "w", newline="", encoding="utf-8") as fout, \
             open(ftmp, "w", newline="", encoding="utf-8") as fflag:
            w = csv.DictWriter(fout, fieldnames=STAR_FIELDS); w.writeheader()
            wf = csv.DictWriter(fflag, fieldnames=STAR_FIELDS); wf.writeheader()
            for r in csv.DictReader(fin):
                r = self.updates.get(r["source_id"], r)
                w.writerow(r)
                if r["flags"]: wf.writerow(r)
                conf = r["confirmed"] in (True, "True")
                self.n_conf += conf
                for f in filter(None, str(r["flags"]).split(";")):
                    self.flag_counts[f] = self.flag_counts.get(f, 0) + 1
                self._add_sample({k: (str(r[k]) if k == "confirmed" else r[k]) for k in self._CHART_KEYS})
        os.replace(tmp, self.stars_path); os.replace(ftmp, self.flags_path)
        self.log(f"catalogue updated: {len(self.updates)} stars upgraded with the second distance check")
        self.updates = {}; self.last_rewrite = time.time(); self._summary()

    def _recheck_worker(self, stop):
        while not stop():
            t0 = time.time()
            try:
                n = self.recheck_once()
            except Exception as e:
                self.log(f"re-check failed ({e!r}); retrying in 30 s"); time.sleep(30); continue
            if n == 0:
                with self.lock:
                    if self.updates: self._rewrite_catalogue()
                time.sleep(30)
            else:
                time.sleep(max(0.0, MIN_CYCLE_S - (time.time() - t0)))

    def _summary(self):
        s = dict(patches=self.n_patches, stars=len(self.seen),
                 star_count_basis="Unique Gaia source IDs in the random-patch catalog; overlapping patch encounters are excluded.",
                 confirmed=self.n_conf,
                 confirmed_frac=(self.n_conf / len(self.seen)) if self.seen else 0.0,
                 flags=dict(self.flag_counts), last_patches=self.patches[-15:][::-1],
                 workers=WORKERS, min_cycle_s=MIN_CYCLE_S,
                 awaiting_recheck=len(self.needs_check), rechecked=self.n_rechecked,
                 rechecks_attempted=self.n_rechecked)
        self.status.update(s)
        if self.n_patches % 10 == 0:                               # summary file: every 10 patches is plenty
            json.dump(s, open(os.path.join(self.outdir, "star_scan_summary.json"), "w"), indent=2)

    def chart_points(self, limit=SAMPLE_MAX):
        """Random sample of catalogued stars for the dashboard charts (no disk read)."""
        with self.lock:
            return list(self.sample[:limit])

    def _worker(self, stop, k):
        time.sleep(k * MIN_CYCLE_S / max(1, WORKERS))             # stagger the workers
        fails = 0
        while not stop():
            t0 = time.time()
            try:
                self.scan_once(); fails = 0
            except Exception as e:
                fails += 1
                wait = min(300, 10 * 2 ** fails)
                self.log(f"worker {k}: scan failed ({e!r}); retrying in {wait} s")
                time.sleep(wait); continue
            time.sleep(max(0.0, MIN_CYCLE_S - (time.time() - t0)))

    def run_forever(self, stop=lambda: False):
        lower_priority()
        threads = [threading.Thread(target=self._worker, args=(stop, k), daemon=True) for k in range(WORKERS)]
        threads.append(threading.Thread(target=self._recheck_worker, args=(stop,), daemon=True))
        for t in threads: t.start()
        for t in threads: t.join()
