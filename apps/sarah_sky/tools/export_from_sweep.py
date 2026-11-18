"""Export AEGIS Star Mapper results into the sky map's data files. Run on the computer that holds the sweep.

    python apps/skymap/tools/export_from_sweep.py --cosmos-map ufe-v2/cosmos_map --out apps/skymap/data

Reads   <cosmos-map>/sweep_state.json            (finished HEALPix level-5 tiles and their star counts)
        <cosmos-map>/tiles/L5/<tile>.csv.gz      (one gzip CSV per tile, Star Mapper columns)
Writes  aegis_coverage.json  survey coverage + three density bands as HEALPix MOCs (Aladin Lite reads these directly)
        aegis_flags.json     flagged stars: every high-velocity and distance-mismatch star, plus the strongest
                             astrometric-excess (RUWE) stars up to --max-ruwe (default 4000), with the flag criteria
Standard library only. Flags are CANDIDATES for follow-up, never discoveries; the files say so.
"""
from __future__ import annotations
import argparse, csv, datetime as dt, gzip, heapq, io, json, pathlib, sys

CRITERIA = {  # mirrors ufe-v2/aegis/anomaly_report.py CRITERIA
    "high_velocity": {"label": "High velocity", "rule": "tangential speed > 400 km/s",
                      "meaning": "Moving unusually fast across the sky for its distance: a possible halo star or a star flung out of its system.",
                      "confirm": "Needs a radial velocity and an orbit, with the measurement uncertainties carried through."},
    "astrometric_excess": {"label": "Wobbly fit (RUWE > 1.4)", "rule": "RUWE > 1.4",
                           "meaning": "Gaia's single-star model fits this star poorly. Often an unseen companion, but crowding or instrument effects can do it too.",
                           "confirm": "Check Gaia's non-single-star tables, crowding and known systematics."},
    "distance_mismatch": {"label": "Distance mismatch", "rule": "1/parallax differs from the Bailer-Jones distance by > 3x its 16-84% width",
                          "meaning": "Two ways of estimating the distance disagree. A heuristic, not a calibrated test.",
                          "confirm": "Check the parallax zero-point, crowding and the distance posterior."},
}
KEEP = ("source_id", "ra", "dec", "g_mag", "bp_rp", "ruwe", "vtan_kms", "dist_pc", "confirmed", "flags", "flag_notes")

def fnum(x):
    try:
        v = float(x); return v if v == v else None
    except (TypeError, ValueError):
        return None

def compress(tiles: list[int]) -> list[int]:
    return sorted(set(int(t) for t in tiles))

MAPPER_ROOT = None

def _tile_centres(level, tiles):
    """Centres of finished tiles (RA, Dec) via ufe-v2/aegis/healpix_lite if it can be found; else empty."""
    here = pathlib.Path(__file__).resolve()
    for root in ([pathlib.Path(MAPPER_ROOT)] if MAPPER_ROOT else []) + [here.parents[3] / "ufe-v2", here.parent]:
        if (root / "aegis" / "healpix_lite.py").exists():
            sys.path.insert(0, str(root))
            try:
                from aegis.healpix_lite import tile_center_radec
                return [[round(c, 4) for c in tile_center_radec(level, t)] for t in tiles]
            except Exception:
                return []
    return []

def build_coverage(state: dict) -> dict:
    done = {int(k): v for k, v in state.get("done", {}).items()}
    counts = {t: int(v.get("n", 0)) for t, v in done.items()}
    vals = sorted(counts.values())
    if vals:
        q1, q2 = vals[len(vals) // 3], vals[2 * len(vals) // 3]
    else:
        q1 = q2 = 0
    bands = {"low": [t for t, n in counts.items() if n <= q1], "mid": [t for t, n in counts.items() if q1 < n <= q2],
             "high": [t for t, n in counts.items() if n > q2]}
    return {"level": int(state.get("level", 5)), "tiles_done": len(counts), "tiles_total": 12 * 4 ** int(state.get("level", 5)),
            "stars": sum(counts.values()), "band_edges": [q1, q2],
            "coverage_moc": {str(state.get("level", 5)): compress(counts)},
            "tiles": [[t, counts[t]] for t in sorted(counts)], "tile_centres": _tile_centres(int(state.get("level", 5)), sorted(counts)),
            "density_moc": {k: {str(state.get("level", 5)): compress(v)} for k, v in bands.items()}}

def scan_flags(tiledir: pathlib.Path, max_ruwe: int):
    keep, ruwe_heap, counts, n_rows = [], [], {k: 0 for k in CRITERIA}, 0
    for path in sorted(tiledir.glob("*.csv.gz")):
        with gzip.open(path, "rt", encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                n_rows += 1
                fl = [f for f in (r.get("flags") or "").split(";") if f]
                if not fl:
                    continue
                for f in fl:
                    counts[f] = counts.get(f, 0) + 1
                rec = {k: r.get(k) for k in KEEP}
                rec["flags"] = fl
                if any(f in ("high_velocity", "distance_mismatch") for f in fl):
                    keep.append(rec)
                elif "astrometric_excess" in fl:
                    ru = fnum(r.get("ruwe")) or 0.0
                    item = (ru, r.get("source_id", ""), rec)
                    if len(ruwe_heap) < max_ruwe:
                        heapq.heappush(ruwe_heap, item)
                    elif ru > ruwe_heap[0][0]:
                        heapq.heapreplace(ruwe_heap, item)
    keep += [it[2] for it in sorted(ruwe_heap, key=lambda t: -t[0])]
    stars = []
    for r in keep:
        ra, dec = fnum(r["ra"]), fnum(r["dec"])
        if ra is None or dec is None:
            continue
        stars.append({"id": str(r["source_id"]), "ra": round(ra, 6), "dec": round(dec, 6), "g": fnum(r["g_mag"]), "bp_rp": fnum(r["bp_rp"]),
                      "ruwe": fnum(r["ruwe"]), "vtan": fnum(r["vtan_kms"]), "dist_pc": fnum(r["dist_pc"]),
                      "confirmed": str(r.get("confirmed", "")).lower() in ("1", "true", "yes"), "flags": r["flags"], "note": r.get("flag_notes") or ""})
    return stars, counts, n_rows

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cosmos-map", required=True, help="folder with sweep_state.json and tiles/L5")
    ap.add_argument("--out", required=True); ap.add_argument("--max-ruwe", type=int, default=4000)
    ap.add_argument("--mapper-root", help="ufe-v2 folder (for tile centres); found automatically inside the AEGIS repo")
    a = ap.parse_args(argv)
    global MAPPER_ROOT; MAPPER_ROOT = a.mapper_root
    cm, out = pathlib.Path(a.cosmos_map), pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    state = json.load(open(cm / "sweep_state.json", encoding="utf-8"))
    cov = build_coverage(state)
    stars, counts, n_rows = scan_flags(cm / "tiles" / f"L{cov['level']}", a.max_ruwe)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    cov.update(generated=now, source="AEGIS Star Mapper sweep of ESA Gaia DR3 (parallax_over_error > 5)", rows_read=n_rows)
    flags = {"generated": now, "status": "CANDIDATES for follow-up, not discoveries",
             "source": "AEGIS Star Mapper sweep of ESA Gaia DR3; flags from ufe-v2/aegis/star_scanner.py",
             "criteria": CRITERIA, "counts_in_sweep": counts, "shown": len(stars),
             "selection": f"all high_velocity and distance_mismatch stars; top {a.max_ruwe} astrometric_excess by RUWE", "stars": stars}
    json.dump(cov, open(out / "aegis_coverage.json", "w", encoding="utf-8"), separators=(",", ":"))
    json.dump(flags, open(out / "aegis_flags.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
    print(f"coverage: {cov['tiles_done']}/{cov['tiles_total']} tiles, {cov['stars']:,} stars; read {n_rows:,} rows; "
          f"flags shown {len(stars):,} (in sweep: {counts})")
    if n_rows and cov["stars"] and n_rows != cov["stars"]:
        print(f"WARNING: rows on disk ({n_rows:,}) differ from the state's star count ({cov['stars']:,})", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
