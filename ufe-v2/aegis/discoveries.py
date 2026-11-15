# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 (HL3-MIL-SV; see LICENSE).
"""Discovery categories for the AEGIS Sky Map (rules locked in field_tests/rules/PREREG_D716_*.md before the real run).

Sorts Star Mapper stars into categories people find interesting and that deserve follow-up. Every entry is a
CANDIDATE; nothing here is a discovery claim. Standard library only, so it runs anywhere the sweep runs.

    python -m aegis.discoveries --tiles cosmos_map/tiles/L5 --out ../apps/skymap/data/aegis_discoveries.json
"""
from __future__ import annotations
import argparse, csv, datetime as dt, gzip, heapq, json, math, pathlib, sys

TOP_N = 5000

CATEGORIES = {
    "nearby": {"label": "The Sun's neighbours (within 20 parsecs)", "color": "#6fd18b",
               "rule": "distance ≤ 20 pc (65 light-years)",
               "why": "Our closest stellar neighbours: the best places to look for planets and to study faint, small stars."},
    "white_dwarf_candidate": {"label": "White dwarf candidates", "color": "#bfe6ff",
                              "rule": "BP−RP < 1.2 and absolute magnitude M_G > 3.3·(BP−RP) + 9.5",
                              "why": "Earth-sized embers of dead stars, far fainter than normal stars of the same colour. This is what our Sun will become."},
    "luminous_giant": {"label": "Luminous giants", "color": "#ffb36b",
                       "rule": "absolute magnitude M_G < −2 (no dust correction, so they are at least this bright)",
                       "why": "Swollen stars near the end of their lives, thousands of times brighter than the Sun; some may explode as supernovae."},
    "fast_mover": {"label": "Fast movers across the sky", "color": "#ffe36b",
                   "rule": "proper motion > 1 arcsecond per year",
                   "why": "Stars that visibly shift position within a human lifetime, usually because they are close or very fast."},
    "hypervelocity_candidate": {"label": "Hypervelocity candidates", "color": "#ff6b7a",
                                "rule": "speed relative to the Sun > 600 km/s (3D when a radial velocity exists, else across-sky only)",
                                "why": "Stars moving fast enough that they may escape the Milky Way, possibly flung out by the central black hole. Most turn out to be measurement problems: these need checking."},
    "strong_wobble": {"label": "Strong wobblers (RUWE > 10)", "color": "#c58bff",
                      "rule": "Gaia RUWE > 10",
                      "why": "Gaia's single-star model fails badly: often a hidden companion star, sometimes crowding or an instrument effect."},
    "very_red": {"label": "Very red stars", "color": "#ff7f50",
                 "rule": "BP−RP > 4",
                 "why": "Extremely cool stars, or stars behind thick dust, or stars wrapped in their own dust."},
}

def _f(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None

def _quality(r) -> bool:
    return str(r.get("astrometric_quality_pass", r.get("confirmed", ""))).strip().lower() in ("1", "true", "yes")

def classify(r: dict) -> dict:
    """Return {category: score} for one Star Mapper row (score orders the map's top lists; higher = shown first)."""
    out = {}
    d, g, c = _f(r.get("dist_pc")), _f(r.get("g_mag")), _f(r.get("bp_rp"))
    ruwe, pmra, pmdec, rv, vtan = _f(r.get("ruwe")), _f(r.get("pmra")), _f(r.get("pmdec")), _f(r.get("rv")), _f(r.get("vtan_kms"))
    if ruwe is not None and ruwe > 10:
        out["strong_wobble"] = ruwe
    if not _quality(r):
        return out
    mg = g + 5 - 5 * math.log10(d) if (g is not None and d and d > 0) else None
    if d is not None and 0 < d <= 20:
        out["nearby"] = -d
    if mg is not None and c is not None and c < 1.2 and mg > 3.3 * c + 9.5:
        out["white_dwarf_candidate"] = mg - (3.3 * c + 9.5)
    if mg is not None and mg < -2.0:
        out["luminous_giant"] = -mg
    if pmra is not None and pmdec is not None:
        pm = math.hypot(pmra, pmdec)
        if pm > 1000:
            out["fast_mover"] = pm
    if vtan is not None:
        v = math.hypot(vtan, rv) if rv is not None else vtan
        if v > 600:
            out["hypervelocity_candidate"] = v
    if c is not None and c > 4.0:
        out["very_red"] = c
    return out

KEEP = ("source_id", "ra", "dec", "dist_pc", "g_mag", "bp_rp", "ruwe", "pmra", "pmdec", "rv", "vtan_kms", "flags")

def _slim(r, mg):
    s = {"id": str(r.get("source_id")), "ra": _f(r.get("ra")), "dec": _f(r.get("dec")), "dist_pc": _f(r.get("dist_pc")),
         "g": _f(r.get("g_mag")), "bp_rp": _f(r.get("bp_rp")), "ruwe": _f(r.get("ruwe")), "rv": _f(r.get("rv")), "vtan": _f(r.get("vtan_kms")),
         "flags": [f for f in (r.get("flags") or "").split(";") if f]}
    pmra, pmdec = _f(r.get("pmra")), _f(r.get("pmdec"))
    if pmra is not None and pmdec is not None:
        s["pm_mas_yr"] = round(math.hypot(pmra, pmdec), 1)
    if mg is not None:
        s["abs_g"] = round(mg, 2)
    return {k: (round(v, 6) if isinstance(v, float) else v) for k, v in s.items()}

class Catalogue:
    """Streams rows; keeps counts and the top N per category."""
    def __init__(self, top_n: int = TOP_N):
        self.top_n, self.counts, self.rows = top_n, {k: 0 for k in CATEGORIES}, 0
        self.heaps = {k: [] for k in CATEGORIES}
        self._seq = 0

    def add(self, r: dict):
        self.rows += 1
        cats = classify(r)
        if not cats:
            return
        d, g = _f(r.get("dist_pc")), _f(r.get("g_mag"))
        mg = g + 5 - 5 * math.log10(d) if (g is not None and d and d > 0) else None
        slim = None
        for k, score in cats.items():
            self.counts[k] += 1
            h = self.heaps[k]; self._seq += 1
            if len(h) < self.top_n or score > h[0][0]:
                slim = slim or _slim(r, mg)
                item = (score, self._seq, slim)
                (heapq.heappush if len(h) < self.top_n else heapq.heapreplace)(h, item)

    def result(self) -> dict:
        lists = {k: [it[2] for it in sorted(h, key=lambda t: -t[0])] for k, h in self.heaps.items()}
        return {"generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
                "status": "CANDIDATES, not discoveries: each needs checking",
                "rules_locked_in": "field_tests/rules/PREREG_D716_STAR_MAPPER_DISCOVERY_CATEGORIES_V1.md",
                "rows_read": self.rows, "top_n": self.top_n, "categories": CATEGORIES, "counts": self.counts, "stars": lists}

def scan_tiles(tiledir: pathlib.Path, top_n: int = TOP_N, progress=None) -> dict:
    cat = Catalogue(top_n)
    files = sorted(pathlib.Path(tiledir).glob("*.csv.gz"))
    for i, p in enumerate(files, 1):
        with gzip.open(p, "rt", encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                cat.add(r)
        if progress and (i % 200 == 0 or i == len(files)):
            progress(i, len(files), cat.rows)
    out = cat.result(); out["tiles_read"] = len(files)
    return out

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Sort Star Mapper stars into Sky Map discovery categories (rules: PREREG_D716).")
    ap.add_argument("--tiles", required=True); ap.add_argument("--out", required=True); ap.add_argument("--top", type=int, default=TOP_N)
    a = ap.parse_args(argv)
    res = scan_tiles(pathlib.Path(a.tiles), a.top, lambda i, n, rows: print(f"  {i}/{n} tiles, {rows:,} stars", flush=True))
    pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("counts:", json.dumps(res["counts"]))
    big = {k: v for k, v in res["counts"].items() if k != "strong_wobble" and res["rows_read"] and v > 0.10 * res["rows_read"]}
    if big:
        print("WARNING (locked FAIL rule): category above 10% of all stars:", big, file=sys.stderr); return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
