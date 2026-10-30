# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use. AEGIS-ID: 84a751d052c171cf
"""
Full audit of the finished galaxy sweep: every tile, not one random tile every 10 minutes.

For each of the 12,288 tiles:
  1. ESA      a fresh COUNT(*) from the ESA Gaia archive with exactly the sweep's filter (parallax_over_error > 5)
  2. stored   the count AEGIS recorded in sweep_state.json when the tile was swept
  3. on disk  the number of star rows actually inside the tile file (tiles/L5/NNNNN.csv.gz)
A tile passes only if all three agree. Resumable: results are saved as they arrive (cosmos_map/verify_all.json).

    python verify_all_tiles.py            run / resume the audit (4 tiles at a time, polite to ESA)
    python verify_all_tiles.py --report   print the summary only
"""
import gzip, json, os, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from aegis.star_scanner import tap_query
from aegis.sweep import adql_count, LEVEL
from aegis.healpix_lite import tile_source_id_range

OUT = os.path.join(HERE, "cosmos_map")
STATE = os.path.join(OUT, "sweep_state.json")
RESULT = os.path.join(OUT, "verify_all.json")
WORKERS = 4
lock = threading.Lock()


def rows_on_disk(t):
    with gzip.open(os.path.join(OUT, "tiles", f"L{LEVEL}", f"{t:05d}.csv.gz"), "rt", encoding="utf-8") as f:
        return sum(1 for _ in f) - 1                  # minus the header line


def esa_count(t):
    lo, hi = tile_source_id_range(LEVEL, t)
    for attempt in range(6):
        try:
            return int(tap_query(adql_count(lo, hi), timeout=180)[0]["n"])
        except Exception:
            time.sleep(10 * (attempt + 1))
    raise RuntimeError("ESA unreachable")


def load():
    try:
        return json.load(open(RESULT, encoding="utf-8"))
    except (OSError, ValueError):
        return {"tiles": {}}


def save(res):
    tmp = RESULT + ".tmp"
    json.dump(res, open(tmp, "w", encoding="utf-8"))
    os.replace(tmp, RESULT)


def summary(res, total):
    v = list(res["tiles"].values())
    ok = sum(1 for r in v if r["match"])
    stars = sum(r["esa"] for r in v)
    bad = [(int(k), r) for k, r in res["tiles"].items() if not r["match"]]
    print(f"checked {len(v):,}/{total:,} tiles | all three agree: {ok:,} | mismatches: {len(bad):,} | stars confirmed by ESA: {stars:,}")
    for t, r in bad[:20]:
        print(f"  tile {t}: ESA {r['esa']:,}  stored {r['stored']:,}  on disk {r['disk']:,}")
    return ok, len(bad)


def main():
    done = {int(k): v["n"] for k, v in json.load(open(STATE, encoding="utf-8"))["done"].items()}
    res = load()
    if "--report" in sys.argv:
        summary(res, len(done)); return
    todo = [t for t in sorted(done) if str(t) not in res["tiles"]]
    print(f"{len(done):,} swept tiles; {len(todo):,} left to audit with {WORKERS} at a time")
    t0, n = time.time(), 0

    def one(t):
        esa, disk = esa_count(t), rows_on_disk(t)
        return t, {"esa": esa, "stored": done[t], "disk": disk, "match": esa == done[t] == disk, "t": time.time()}

    with ThreadPoolExecutor(WORKERS) as ex:
        futs = [ex.submit(one, t) for t in todo]
        for f in as_completed(futs):
            try:
                t, r = f.result()
            except Exception as e:
                print(f"skipped a tile ({e}); rerun to retry"); continue
            with lock:
                res["tiles"][str(t)] = r; n += 1
                if not r["match"]:
                    print(f"MISMATCH tile {t}: ESA {r['esa']:,} stored {r['stored']:,} disk {r['disk']:,}")
                if n % 100 == 0:
                    save(res)
                    rate = n / (time.time() - t0)
                    print(f"{len(res['tiles']):,}/{len(done):,} audited, {rate * 60:.0f} tiles/min, "
                          f"about {(len(todo) - n) / rate / 60:.0f} min left")
    save(res)
    res["finished"] = time.time(); save(res)
    summary(res, len(done))


if __name__ == "__main__":
    main()
