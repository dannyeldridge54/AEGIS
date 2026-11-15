# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 (HL3-MIL-SV; see LICENSE).
"""One command that feeds the AEGIS Sky Map from the Star Mapper, and feeds classroom reviews back.

    python -m aegis.map_feed                (from ufe-v2/; Windows: START_MAP_FEED.bat)

1. Reviews in:  every CSV dropped in cosmos_map/reviews_in/ is tallied (aegis.community_reviews).
2. Flags + coverage out:  apps/skymap/tools/export_from_sweep.py  -> aegis_flags.json, aegis_coverage.json
3. Discoveries out:  aegis.discoveries (rules locked in PREREG_D716)  -> aegis_discoveries.json
4. Reviews out:  the tallies are written to apps/skymap/data/aegis_reviews.json, so the map shows what classes think.
Reads the sweep only; never changes tiles, flags or the sweep state. Safe to run while the monitor is sweeping.
"""
from __future__ import annotations
import argparse, json, pathlib, subprocess, sys, time
from aegis import community_reviews as CR, discoveries as D

HERE = pathlib.Path(__file__).resolve().parents[1]           # ufe-v2/

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cosmos-map", default=str(HERE / "cosmos_map")); ap.add_argument("--skymap", default=str(HERE.parent / "apps" / "skymap"))
    ap.add_argument("--top", type=int, default=D.TOP_N); ap.add_argument("--skip-discoveries", action="store_true")
    a = ap.parse_args(argv)
    cm, sk = pathlib.Path(a.cosmos_map), pathlib.Path(a.skymap); data = sk / "data"; data.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    inbox = cm / "reviews_in"; inbox.mkdir(parents=True, exist_ok=True)
    store = CR.load(cm / "community_reviews.json"); added = sum(CR.merge(store, f) for f in sorted(inbox.glob("*.csv")))
    json.dump(store, open(cm / "community_reviews.json", "w", encoding="utf-8"), indent=1)
    pr = CR.priority(store)
    json.dump({"stars": pr}, open(cm / "recheck_priority.json", "w", encoding="utf-8"), indent=1)
    print(f"[1/4] reviews: +{added} votes, {len(store['stars'])} stars reviewed, {len(pr)} prioritised for recheck")
    r = subprocess.run([sys.executable, str(sk / "tools" / "export_from_sweep.py"), "--cosmos-map", str(cm), "--out", str(data), "--mapper-root", str(HERE)], capture_output=True, text=True)
    print("[2/4] flags + coverage:", (r.stdout or r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr) else r.returncode)
    if r.returncode:
        print(r.stderr, file=sys.stderr); return r.returncode
    if not a.skip_discoveries:
        res = D.scan_tiles(cm / "tiles" / "L5", a.top, lambda i, n, rows: print(f"      discoveries: {i}/{n} tiles, {rows:,} stars", flush=True))
        json.dump(res, open(data / "aegis_discoveries.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
        print("[3/4] discoveries:", json.dumps(res["counts"]))
    tallies = {sid: {k: s[k] for k in ("real", "artefact", "unsure")} for sid, s in store["stars"].items()}
    json.dump({"note": "Classroom reviews collected by the AEGIS Star Mapper; opinions, not confirmations.", "stars": tallies},
              open(data / "aegis_reviews.json", "w", encoding="utf-8"), separators=(",", ":"))
    print(f"[4/4] review tallies written for {len(tallies)} stars. Done in {time.time() - t0:.0f} s. Map data: {data}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
