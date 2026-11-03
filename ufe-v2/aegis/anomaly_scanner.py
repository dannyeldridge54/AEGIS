"""AEGIS anomaly scanner: gravity (LIGO/Virgo/KAGRA events), quantum (NIST Randomness Beacon) and space telemetry
(NOAA SWPC: X-ray, radio, particle, magnetic, geomagnetic).

Reports exactly like the star scanner: every record gets flags (name + note saying how to confirm), flagged records are
appended to cosmos_map/cosmos_map_anomalies.csv, per-flag counts and recent records go into
cosmos_map/anomaly_scan_summary.json, and the monitor serves them at /api/anomalies and in /api/status["anomaly"].
Flags are candidates worth a closer look, never discoveries.
"""
import csv, json, math, os, threading, time, urllib.request
import numpy as np

GWOSC_EVENTS = "https://gwosc.org/eventapi/json/allevents/"
BEACON_LAST = "https://beacon.nist.gov/beacon/2.0/pulse/last"
BEACON_PULSE = "https://beacon.nist.gov/beacon/2.0/chain/{chain}/pulse/{index}"
GRAVITY_EVERY_S = 3600      # the event catalogue changes rarely
QUANTUM_EVERY_S = 60        # the beacon emits one pulse a minute
QUANTUM_BACKFILL = 5        # earlier pulses fetched per cycle, to find new/missed ones
RECENT = 40
P_FLAG = 1e-3               # randomness-test p-value below which a pulse is flagged

FIELDS = ["source", "id", "time", "value", "flags", "flag_notes", "wavelength", "object"]

# category -> (wavelength or messenger, kind of object). Records may override "object" (gravity does).
SOURCE_TAGS = {
    "gravity": ("gravitational", "compact_binary"), "quantum": ("laboratory", "quantum_source"),
    "xray": ("x-ray", "sun"), "flare_catalog": ("x-ray", "sun"), "radio": ("radio", "sun"), "sunspots": ("optical", "sun"),
    "cme": ("optical", "sun"), "particle": ("particle", "sun"), "electron": ("particle", "earth_magnetosphere"),
    "magnetic": ("magnetic_field", "solar_wind"), "solar_wind": ("plasma", "solar_wind"), "solar_wind_density": ("plasma", "solar_wind"),
    "geomagnetic": ("magnetic_field", "earth"), "geomagnetic_field": ("magnetic_field", "earth_magnetosphere"),
    "near_earth": ("optical", "small_body"), "fireball": ("optical", "small_body"),
    "star": ("optical", "star"), "star_vtan": ("optical", "star"), "star_ruwe": ("optical", "star"), "star_dist": ("optical", "star"),
}


def tag_row(r):
    """Fill wavelength and object for a record, from its category unless the record already says."""
    w, o = SOURCE_TAGS.get(str(r.get("source", "")).split("_", 1)[0] if r.get("source") not in SOURCE_TAGS else r["source"], ("unknown", "unknown"))
    r["wavelength"] = r.get("wavelength") or w
    r["object"] = r.get("object") or o
    return r


def query_anomalies(outdir, wavelength=None, obj=None, flag=None, source=None, limit=200, include_stars=True):
    """Filter everything flagged so far: anomaly CSV plus the star scanner's flags. Returns (rows, facets).
    Filters accept comma-separated values. Facets count matches per wavelength, object, flag and source."""
    want = lambda v: set(v.split(",")) if v else None
    fw, fo, ff, fs = want(wavelength), want(obj), want(flag), want(source)
    rows, facets = [], {"wavelength": {}, "object": {}, "flag": {}, "source": {}}

    def take(r):
        tag_row(r); fl = [f for f in str(r.get("flags", "")).split(";") if f]
        if (fw and r["wavelength"] not in fw) or (fo and r["object"] not in fo) or (fs and r["source"] not in fs) or (ff and not ff.intersection(fl)):
            return
        for k, v in (("wavelength", [r["wavelength"]]), ("object", [r["object"]]), ("source", [r["source"]]), ("flag", fl)):
            for x in v:
                facets[k][x] = facets[k].get(x, 0) + 1
        if len(rows) < limit:
            rows.append({k: r.get(k, "") for k in FIELDS})

    path = os.path.join(outdir, "cosmos_map_anomalies.csv")
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                take(r)
    path = os.path.join(outdir, "cosmos_map_flags.csv")
    if include_stars and os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                take(dict(source="star", id=r.get("source_id"), time="", value=f"dist_pc={r.get('dist_pc')} l={r.get('l')} b={r.get('b')}",
                          flags=r.get("flags", ""), flag_notes=r.get("flag_notes", "")))
    return rows, facets


def _gw_object(m1, m2):
    ms = [m for m in (m1, m2) if m is not None]
    if not ms:
        return "compact_binary"
    if min(ms) < 3.0 and max(ms) < 3.0:
        return "neutron_star"
    if min(ms) < 3.0:
        return "neutron_star_black_hole"
    return "black_hole"


MEANING = {
    "lower_mass_gap": ("Lower mass gap", "A component mass between 2.5 and 5 solar masses, where neither neutron stars nor black holes are expected. Confirm with the posterior samples on GWOSC."),
    "upper_mass_gap": ("Upper mass gap", "A component mass between 60 and 130 solar masses, inside the pair-instability gap. Confirm that the mass posterior excludes the gap."),
    "high_spin": ("High spin", "Effective spin above 0.6 in size. Check the parameter-estimation posterior and waveform-model agreement."),
    "far_source": ("Very distant", "Luminosity distance above 5 Gpc, near the detector reach. Check the redshift prior and sensitivity at the time."),
    "weak_detection": ("Marginal detection", "False alarm rate above 1 per year, or network SNR below 8. Treat as a possible noise artefact until confirmed."),
    "bit_bias": ("Bit bias", "The ones and zeros of a beacon pulse are lopsided (monobit test). Re-test on neighbouring pulses; one in a thousand fires by chance."),
    "runs_anomaly": ("Streaky bits", "Too many or too few runs of equal bits in one pulse. Re-test on neighbouring pulses."),
    "dataset_drift": ("Dataset drift", "New data for a category differs from its previous data sets (two-sample KS test p < 0.001). Compare the KS distance with the old-vs-old control in anomaly_compare.csv."),
    "beacon_status": ("Beacon status", "NIST reports a nonzero status code for the pulse (for example a chain restart or missing earlier pulses)."),
}


def _num(x):
    try:
        x = float(x)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None


def _best(d, key):
    """GWOSC gives each parameter as a value plus asymmetric errors; take the value."""
    return _num(d.get(key))


def assess_gw(name, ev):
    """Return (record, flags) for one GWOSC event dictionary."""
    m1, m2 = _best(ev, "mass_1_source"), _best(ev, "mass_2_source")
    chi, dl = _best(ev, "chi_eff"), _best(ev, "luminosity_distance")
    far, snr = _best(ev, "far"), _best(ev, "network_matched_filter_snr")
    flags = []
    for m in (m1, m2):
        if m is not None and 2.5 <= m <= 5.0 and not any(f[0] == "lower_mass_gap" for f in flags):
            flags.append(("lower_mass_gap", f"component mass {m:.1f} Msun"))
        if m is not None and 60.0 <= m <= 130.0 and not any(f[0] == "upper_mass_gap" for f in flags):
            flags.append(("upper_mass_gap", f"component mass {m:.0f} Msun"))
    if chi is not None and abs(chi) > 0.6:
        flags.append(("high_spin", f"chi_eff {chi:.2f}"))
    if dl is not None and dl > 5000:
        flags.append(("far_source", f"{dl / 1000:.1f} Gpc"))
    if (far is not None and far > 1.0) or (snr is not None and snr < 8.0):
        flags.append(("weak_detection", f"FAR {far} per yr, SNR {snr}"))
    rec = dict(source="gravity", id=ev.get("commonName") or name, time=ev.get("GPS", ""), x=m1, object=_gw_object(m1, m2),
               value=f"m1={m1} m2={m2} chi_eff={chi} dl_Mpc={dl}",
               flags=";".join(f[0] for f in flags), flag_notes=" | ".join(f[1] for f in flags))
    return rec


def parse_gw_catalogue(doc):
    """GWOSC allevents JSON -> records. Uses the newest version of each event."""
    out = []
    for name, ev in (doc.get("events") or {}).items():
        try:
            out.append(assess_gw(name, ev))
        except Exception:
            continue
    return out


def _erfc_p(z):
    return math.erfc(abs(z) / math.sqrt(2))


def assess_beacon(pulse):
    """Randomness tests on one NIST beacon pulse (512-bit outputValue, hex)."""
    hexval = pulse.get("outputValue", "")
    bits = bin(int(hexval, 16))[2:].zfill(len(hexval) * 4) if hexval else ""
    n = len(bits)
    flags = []
    if n:
        ones = bits.count("1")
        p_mono = _erfc_p((2 * ones - n) / math.sqrt(n))
        if p_mono < P_FLAG:
            flags.append(("bit_bias", f"{ones}/{n} ones, p={p_mono:.2g}"))
        runs = 1 + sum(1 for a, b in zip(bits, bits[1:]) if a != b)
        pi = ones / n
        if 0 < pi < 1:
            p_runs = math.erfc(abs(runs - 2 * n * pi * (1 - pi)) / (2 * math.sqrt(2 * n) * pi * (1 - pi)))
            if p_runs < P_FLAG:
                flags.append(("runs_anomaly", f"{runs} runs in {n} bits, p={p_runs:.2g}"))
    if pulse.get("statusCode", 0) != 0:
        flags.append(("beacon_status", f"status code {pulse.get('statusCode')}"))
    return dict(source="quantum", id=f"{pulse.get('chainIndex')}:{pulse.get('pulseIndex')}", time=pulse.get("timeStamp", ""),
                x=(bits.count("1") / n) if n else None,
                value=f"bits={n} ones={bits.count('1') if n else 0}",
                flags=";".join(f[0] for f in flags), flag_notes=" | ".join(f[1] for f in flags))


SWPC = "https://services.swpc.noaa.gov/json/"
TELEMETRY_EVERY_S = 300
TELEMETRY_NEW_PER_SERIES = 30   # newest rows ingested per series each cycle; the whole window sets the baseline
OUTLIER_Z = 6.0

# band, url, series key (or None), value key, optional (flag, test, note) rule applied to a single value
TELEMETRY = [
    ("xray", SWPC + "goes/primary/xrays-1-day.json", "energy", "flux",
     ("xray_flare", lambda v, r: r.get("energy") == "0.1-0.8nm" and v >= 1e-5, "GOES 0.1-0.8 nm flux at M-class or stronger (>= 1e-5 W/m2)")),
    ("radio", SWPC + "f107_cm_flux.json", None, "flux", None),
    ("particle", SWPC + "goes/primary/integral-protons-1-day.json", "energy", "flux",
     ("proton_event", lambda v, r: r.get("energy") == ">=10 MeV" and v >= 10, "proton flux above 10 pfu at >=10 MeV (NOAA S1 radiation storm)")),
    ("magnetic", SWPC + "rtsw/rtsw_mag_1m.json", None, "bz_gsm",
     ("southward_bz", lambda v, r: v <= -10, "interplanetary Bz at or below -10 nT, a geomagnetic storm driver")),
    ("geomagnetic", SWPC + "planetary_k_index_1m.json", None, "kp_index",
     ("geomagnetic_storm", lambda v, r: v >= 5, "planetary Kp at or above 5 (NOAA G1 storm)")),
]

def _donki_window(days=30):
    t = time.time()
    f = lambda x: time.strftime("%Y-%m-%d", time.gmtime(x))
    return f"startDate={f(t - days * 86400)}&endDate={f(t)}&api_key=DEMO_KEY"


def _table(doc):
    """JPL SSD APIs return {fields: [...], data: [[...]]}; turn that into a list of dicts."""
    return [dict(zip(doc["fields"], row)) for row in doc.get("data", [])]


def _adapt_cad(doc):
    rows = _table(doc)
    for r in rows:
        r["time_tag"] = r.get("cd")
    return rows


def _adapt_fireball(doc):
    rows = _table(doc)
    for r in rows:
        r["time_tag"] = r.get("date")
    return rows


def _adapt_donki_cme(rows):
    out = []
    for c in rows or []:
        an = next((a for a in c.get("cmeAnalyses") or [] if a.get("isMostAccurate")), (c.get("cmeAnalyses") or [{}])[0])
        out.append(dict(time_tag=c.get("startTime"), speed=an.get("speed"), id=c.get("activityID")))
    return out


def _adapt_donki_flare(rows):
    out = []
    for f in rows or []:
        cls = str(f.get("classType") or "")
        scale = {"A": 1e-8, "B": 1e-7, "C": 1e-6, "M": 1e-5, "X": 1e-4}.get(cls[:1])
        try:
            out.append(dict(time_tag=f.get("peakTime") or f.get("beginTime"), flux=scale * float(cls[1:]), cls=cls))
        except (TypeError, ValueError):
            pass
    return out


# Further feeds: optional dict gives "adapt" (reshape the JSON into rows), "period" (seconds between fetches).
TELEMETRY += [
    ("solar_wind", SWPC + "rtsw/rtsw_wind_1m.json", None, "proton_speed",
     ("fast_wind", lambda v, r: v >= 700, "solar wind speed at or above 700 km/s, a high-speed stream or shock")),
    ("solar_wind_density", SWPC + "rtsw/rtsw_wind_1m.json", None, "proton_density",
     ("dense_wind", lambda v, r: v >= 30, "solar wind proton density at or above 30 /cm3, a compression or shock")),
    ("electron", SWPC + "goes/primary/integral-electrons-1-day.json", "energy", "flux",
     ("electron_event", lambda v, r: r.get("energy") == ">=2 MeV" and v >= 1000, "relativistic electron flux at or above 1000 pfu (>=2 MeV), a satellite-charging hazard")),
    ("geomagnetic_field", SWPC + "goes/primary/magnetometers-1-day.json", None, "Hp",
     ("field_depression", lambda v, r: v <= 20, "GOES Hp field at or below 20 nT, a strongly stretched or compressed magnetosphere")),
    ("sunspots", SWPC + "solar-cycle/observed-solar-cycle-indices.json", None, "ssn", None),
    ("cme", "https://api.nasa.gov/DONKI/CME?", None, "speed",
     ("fast_cme", lambda v, r: v >= 1000, "coronal mass ejection faster than 1000 km/s (NASA DONKI). Confirm with SOHO/LASCO and the DONKI analysis"),
     {"adapt": _adapt_donki_cme, "period": 3600, "donki": True}),
    ("flare_catalog", "https://api.nasa.gov/DONKI/FLR?", None, "flux",
     ("x_class_flare", lambda v, r: v >= 1e-4, "X-class flare in the NASA DONKI catalogue. Confirm on the GOES flare list"),
     {"adapt": _adapt_donki_flare, "period": 3600, "donki": True}),
    ("near_earth", "https://ssd-api.jpl.nasa.gov/cad.api?dist-max=0.05&date-min=now&date-max=%2B60&sort=date", None, "dist",
     ("close_approach", lambda v, r: v <= 0.00257, "asteroid or comet passing inside the Moon's distance (JPL close-approach data). Confirm with the JPL SBDB orbit"),
     {"adapt": _adapt_cad, "period": 3600}),
    ("fireball", "https://ssd-api.jpl.nasa.gov/fireball.api?limit=200", None, "energy",
     ("large_fireball", lambda v, r: v >= 1.0, "fireball of 1 kt TNT or more detected by US government sensors (JPL fireball database)"),
     {"adapt": _adapt_fireball, "period": 3600}),
]

TELEMETRY_MEANING = {
    "fast_wind": ("Fast solar wind", "Solar wind at 700 km/s or more. Confirm with DSCOVR/ACE."),
    "dense_wind": ("Dense solar wind", "Proton density at 30 per cm3 or more, usually a shock or compression."),
    "electron_event": ("Electron event", "Relativistic electrons at 1000 pfu or more. Confirm on GOES electron data."),
    "field_depression": ("Field depression", "GOES Hp field at 20 nT or less. Confirm with ground magnetometers."),
    "fast_cme": ("Fast CME", "Coronal mass ejection of 1000 km/s or more. Confirm with the DONKI analysis."),
    "x_class_flare": ("X-class flare", "Flare of class X or stronger. Confirm on the GOES flare list."),
    "close_approach": ("Close approach", "Small body passing within the Moon's distance. Confirm with JPL SBDB."),
    "large_fireball": ("Large fireball", "Fireball of 1 kt or more. Confirm with JPL fireball data."),
    "xray_flare": ("X-ray flare", "Solar X-ray flux at M-class or stronger. Confirm on the GOES flare list and SWPC events."),
    "proton_event": ("Proton event", "Energetic proton flux above the S1 threshold. Confirm with SOHO/ACE particle data."),
    "southward_bz": ("Southward Bz", "Strongly southward interplanetary field. Confirm with the DSCOVR/ACE solar-wind feeds."),
    "geomagnetic_storm": ("Geomagnetic storm", "Kp at 5 or higher. Confirm with ground magnetometer indices."),
    "telemetry_outlier": ("Telemetry outlier", "A value more than 6 robust sigmas from its own series window (median/MAD). Check for instrument glitches before calling it real."),
}


def assess_telemetry(band, rows, key, vkey, rule):
    """Flag the newest rows of every series in one feed. Rows are NOAA SWPC-style JSON dicts."""
    series = {}
    for r in rows:
        v = _num(r.get(vkey))
        if v is not None and r.get("time_tag"):
            series.setdefault(str(r.get(key, "")) if key else "", []).append((r, v))
    recs = []
    for name, items in series.items():
        vals = sorted(v for _, v in items)
        med = vals[len(vals) // 2]
        mad = sorted(abs(v - med) for v in vals)[len(vals) // 2] * 1.4826
        for r, v in items[-TELEMETRY_NEW_PER_SERIES:]:
            flags = []
            if rule and rule[1](v, r):
                flags.append((rule[0], rule[2]))
            if mad > 0 and abs(v - med) / mad > OUTLIER_Z:
                flags.append(("telemetry_outlier", f"{v:.4g} vs median {med:.4g} (MAD sigma {mad:.3g})"))
            recs.append(dict(source=band, id=f"{name}:{r['time_tag']}" if name else r["time_tag"], time=r["time_tag"], x=v,
                             value=f"{vkey}={v:.6g}", flags=";".join(f[0] for f in flags), flag_notes=" | ".join(f[1] for f in flags)))
    return recs


LOCAL_TILES_PER_CYCLE = 25
LOCAL_SAMPLE = 2000
HISTORY_MAX = 5000      # previous values kept per category
MIN_COMPARE = 20        # samples needed on each side before a comparison means anything
DRIFT_P = 1e-3
COMPARE_FIELDS = ["time", "source", "n_old", "n_new", "ks", "p", "baseline_ks", "wasserstein", "wasserstein_sigma", "verdict"]


def ks_2samp(a, b):
    """Two-sample Kolmogorov-Smirnov distance D (max gap between the two CDFs) and its asymptotic p-value."""
    a, b = np.sort(np.asarray(a, float)), np.sort(np.asarray(b, float))
    grid = np.concatenate([a, b])
    d = float(np.max(np.abs(np.searchsorted(a, grid, side="right") / len(a) - np.searchsorted(b, grid, side="right") / len(b))))
    en = math.sqrt(len(a) * len(b) / (len(a) + len(b)))
    lam = (en + 0.12 + 0.11 / en) * d
    p = 2 * sum((-1) ** (k - 1) * math.exp(-2 * k * k * lam * lam) for k in range(1, 101)) if lam > 0.2 else 1.0
    return d, min(1.0, max(0.0, p))


def wasserstein(a, b):
    """1-D Earth mover's distance between two samples, via matching quantiles."""
    q = np.linspace(0, 1, 201)
    return float(np.mean(np.abs(np.quantile(a, q) - np.quantile(b, q))))


def compare_sets(old, new):
    """Distance between a category's previous data and its new data, plus an old-vs-old control.
    The control splits the old data in two (odd/even) and measures the same distance, so you can see
    what 'no change' looks like for this category before reading the old-vs-new number."""
    old, new = np.asarray(old, float), np.asarray(new, float)
    d, p = ks_2samp(old, new)
    base, _ = ks_2samp(old[::2], old[1::2]) if len(old) >= 4 else (None, None)
    w = wasserstein(old, new)
    sd = float(np.std(old)) or 1.0
    verdict = "drift" if p < DRIFT_P else "consistent"
    return dict(n_old=len(old), n_new=len(new), ks=round(d, 4), p=p, baseline_ks=None if base is None else round(base, 4),
                wasserstein=w, wasserstein_sigma=round(w / sd, 4), verdict=verdict)


def _get_json(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "AEGIS-anomaly-scanner"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


class AnomalyScanner:
    def __init__(self, outdir, status=None, log=print, fetch=_get_json):
        self.outdir, self.status, self.log, self.fetch = outdir, status if status is not None else {}, log, fetch
        os.makedirs(outdir, exist_ok=True)
        self.flags_path = os.path.join(outdir, "cosmos_map_anomalies.csv")
        self.summary_path = os.path.join(outdir, "anomaly_scan_summary.json")
        self.history_path = os.path.join(outdir, "anomaly_history.jsonl")
        self.compare_path = os.path.join(outdir, "anomaly_compare.csv")
        self.history, self.compare, self.feed_due, self.local_done = {}, {}, {}, set()
        self.lock = threading.Lock()
        self.seen = set(); self.counts = {"gravity": 0, "quantum": 0}
        self.counts.update({t[0]: 0 for t in TELEMETRY}); self.flag_counts = {}; self.recent = []
        self._load()

    def _load(self):
        if os.path.exists(self.history_path):          # previous data sets survive restarts
            for line in open(self.history_path, encoding="utf-8"):
                try:
                    d = json.loads(line); h = self.history.setdefault(d["source"], [])
                    h.extend(d["x"]); del h[:-HISTORY_MAX]
                except Exception:
                    pass
        if os.path.exists(self.flags_path):
            with open(self.flags_path, newline="", encoding="utf-8") as fh:
                for r in csv.DictReader(fh):
                    self.seen.add((r["source"], r["id"]))
                    for f in filter(None, r["flags"].split(";")):
                        self.flag_counts[f] = self.flag_counts.get(f, 0) + 1
        try:
            old = json.load(open(self.summary_path, encoding="utf-8"))
            self.counts.update(old.get("scanned", {}))
            self.seen.update(tuple(k) for k in old.get("seen", []))
            self.local_done.update(old.get("local_done", []))
            self.flag_counts = old.get("flags", self.flag_counts)
        except Exception:
            pass

    def ingest(self, recs):
        """Count new records, append flagged ones to the CSV, update the summary."""
        with self.lock:
            uniq = {(r["source"], r["id"]): r for r in recs}
            new = [r for k, r in uniq.items() if k not in self.seen]
            for r in new:
                self.seen.add((r["source"], r["id"])); self.counts[r["source"]] = self.counts.get(r["source"], 0) + 1
                for f in filter(None, r["flags"].split(";")):
                    self.flag_counts[f] = self.flag_counts.get(f, 0) + 1
            self._compare(new)
            for r in new:
                tag_row(r)
            flagged = [r for r in new if r["flags"]]
            if flagged:
                fresh = not os.path.exists(self.flags_path)
                with open(self.flags_path, "a", newline="", encoding="utf-8") as fh:
                    w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
                    if fresh:
                        w.writeheader()
                    w.writerows(flagged)
            self.recent = (flagged + self.recent)[:RECENT]
            self._summary()
        return new, flagged

    def _compare(self, new):
        """For each category: new values vs the previous data sets, then fold the new values into the history."""
        by = {}
        for r in new:
            if r.get("x") is not None:
                by.setdefault(r["source"], []).append(r["x"])
        rows = [c for c in (self.compare_batch(src, xs) for src, xs in by.items()) if c]
        self._write_compare(rows)

    def compare_batch(self, src, xs):
        """Measure xs against the stored history of category src, record a drift flag if needed, then store xs."""
        xs = [float(x) for x in xs if x is not None and math.isfinite(float(x))]
        old = self.history.get(src, [])
        c = None
        if len(old) >= MIN_COMPARE and len(xs) >= MIN_COMPARE:
            c = compare_sets(old, xs)
            c.update(time=time.strftime("%Y-%m-%dT%H:%M:%S"), source=src)
            self.compare[src] = c
            if c["verdict"] == "drift":
                self.flag_counts["dataset_drift"] = self.flag_counts.get("dataset_drift", 0) + 1
                self.recent.insert(0, dict(source=src, id="compare", time=c["time"], value=f"KS={c['ks']}", flags="dataset_drift",
                                           flag_notes=f"new {src} data differs from the previous data sets (KS {c['ks']}, p={c['p']:.2g}, control {c['baseline_ks']})"))
        if xs:
            self.history[src] = (old + xs)[-HISTORY_MAX:]
            with open(self.history_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"source": src, "x": xs}) + "\n")
        return c

    def _write_compare(self, rows):
        if rows:
            fresh = not os.path.exists(self.compare_path)
            with open(self.compare_path, "a", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=COMPARE_FIELDS, extrasaction="ignore")
                if fresh:
                    w.writeheader()
                w.writerows(rows)

    def scan_local(self):
        """Compare data already on this PC against its own past: swept Gaia tiles and files dropped in cosmos_map/incoming/."""
        import gzip, random
        with self.lock:
            done = self.local_done
            rows = []
            tdir = os.path.join(self.outdir, "tiles", "L5")
            tiles = sorted(f for f in os.listdir(tdir) if f.endswith(".csv.gz")) if os.path.isdir(tdir) else []
            for f in [f for f in tiles if "tile:" + f not in done][:LOCAL_TILES_PER_CYCLE]:
                done.add("tile:" + f)
                try:
                    with gzip.open(os.path.join(tdir, f), "rt", encoding="utf-8", newline="") as fh:
                        recs = list(csv.DictReader(fh))
                except Exception:
                    continue
                for col, cat in (("vtan_kms", "star_vtan"), ("ruwe", "star_ruwe"), ("dist_pc", "star_dist")):
                    xs = [_num(r.get(col)) for r in recs]
                    xs = [x for x in xs if x is not None]
                    random.Random(f).shuffle(xs)
                    rows.append(self.compare_batch(cat, xs[:LOCAL_SAMPLE]))
                self.counts["star_tiles"] = self.counts.get("star_tiles", 0) + 1
            idir = os.path.join(self.outdir, "incoming")
            for f in sorted(os.listdir(idir)) if os.path.isdir(idir) else []:
                if f.endswith(".csv") and "file:" + f not in done:      # name.csv: first numeric column, category = file name
                    done.add("file:" + f)
                    with open(os.path.join(idir, f), newline="", encoding="utf-8") as fh:
                        recs = list(csv.reader(fh))
                    xs = [_num(r[0]) for r in recs[1:] if r]
                    rows.append(self.compare_batch("incoming_" + f[:-4], [x for x in xs if x is not None]))
                    self.counts["incoming_files"] = self.counts.get("incoming_files", 0) + 1
            self._write_compare([c for c in rows if c])
            self._summary()
        self.log(f"local: {len(self.local_done)} files compared so far")

    def _summary(self):
        s = dict(scanned=dict(self.counts), flags=dict(self.flag_counts), recent=self.recent, compare=self.compare, local_done=sorted(self.local_done),
                 seen=sorted(list(k) for k in self.seen) if len(self.seen) < 50000 else [], updated=time.time())
        self.status.update({k: v for k, v in s.items() if k not in ("seen", "local_done")})
        json.dump(s, open(self.summary_path, "w"), indent=2)

    def scan_gravity(self):
        new, flagged = self.ingest(parse_gw_catalogue(self.fetch(GWOSC_EVENTS, 120)))
        self.log(f"gravity: {len(new)} new events, {len(flagged)} flagged")

    def scan_quantum(self):
        last = self.fetch(BEACON_LAST)["pulse"]
        pulses = [last]
        chain, idx = last["chainIndex"], last["pulseIndex"]
        for i in range(idx - 1, max(idx - 1 - QUANTUM_BACKFILL, 0), -1):
            try:
                pulses.append(self.fetch(BEACON_PULSE.format(chain=chain, index=i))["pulse"])
            except Exception:
                break
        recs = [assess_beacon(p) for p in pulses]
        new, flagged = self.ingest(recs)
        self.log(f"quantum: {len(new)} new pulses, {len(flagged)} flagged")

    def scan_telemetry(self):
        now = time.time()
        for entry in TELEMETRY:
            band, url, key, vkey, rule = entry[:5]
            opt = entry[5] if len(entry) > 5 else {}
            if now < self.feed_due.get(band, 0):
                continue
            self.feed_due[band] = now + opt.get("period", 0)
            try:
                if opt.get("donki"):
                    url = url + _donki_window()
                rows = self.fetch(url)
                if opt.get("adapt"):
                    rows = opt["adapt"](rows)
                new, flagged = self.ingest(assess_telemetry(band, rows, key, vkey, rule))
                self.log(f"{band}: {len(new)} new rows, {len(flagged)} flagged")
            except Exception as e:
                self.log(f"{band} feed failed: {e}")

    def run_forever(self):
        next_run = {"gravity": 0.0, "quantum": 0.0, "telemetry": 0.0, "local": 0.0}
        period = {"gravity": GRAVITY_EVERY_S, "quantum": QUANTUM_EVERY_S, "telemetry": TELEMETRY_EVERY_S, "local": 120}
        while True:
            for name in ("gravity", "quantum", "telemetry", "local"):
                if time.time() >= next_run[name]:
                    try:
                        getattr(self, "scan_" + name)()
                    except Exception as e:
                        self.log(f"{name} scan failed: {e}")
                    next_run[name] = time.time() + period[name]
            time.sleep(5)
