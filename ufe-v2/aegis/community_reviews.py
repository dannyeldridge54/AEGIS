# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under the Hippocratic License 3.0 (HL3-MIL-SV; see LICENSE).
"""Close the loop: classroom reviews from the AEGIS Sky Map come back into the Star Mapper.

    python -m aegis.community_reviews cosmos_map/reviews_in/*.csv

Each CSV is a Sky Map export (source_id, vote, flags, ra, dec, time_utc). Votes are tallied per star into
cosmos_map/community_reviews.json; stars that reviewers think "look real" (more real than artefact votes) are written,
most-supported first, to cosmos_map/recheck_priority.json so the Star Mapper's recheck work can start with them.
A file is only counted once (its SHA-256 is remembered). Reviews are opinions: they order the queue, they never
confirm or reject a star.
"""
from __future__ import annotations
import csv, hashlib, json, pathlib, sys, datetime as dt

VOTES = {"looks real": "real", "looks like an artefact": "artefact", "not sure": "unsure"}

def load(path: pathlib.Path) -> dict:
    return json.load(open(path, encoding="utf-8")) if path.exists() else {"files": {}, "stars": {}}

def merge(store: dict, csv_path: pathlib.Path) -> int:
    h = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    if h in store["files"]:
        return 0
    n = 0
    with open(csv_path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            sid, v = (r.get("source_id") or "").strip(), VOTES.get((r.get("vote") or "").strip().lower())
            if not sid or not v:
                continue
            s = store["stars"].setdefault(sid, {"real": 0, "artefact": 0, "unsure": 0, "flags": r.get("flags", ""), "ra": r.get("ra"), "dec": r.get("dec")})
            s[v] += 1; n += 1
    store["files"][h] = {"name": csv_path.name, "votes": n, "added": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    return n

def priority(store: dict) -> list:
    rows = [(s["real"] - s["artefact"], s["real"], sid) for sid, s in store["stars"].items() if s["real"] > s["artefact"]]
    return [{"source_id": sid, "real": store["stars"][sid]["real"], "artefact": store["stars"][sid]["artefact"]}
            for _, _, sid in sorted(rows, key=lambda t: (-t[0], -t[1], t[2]))]

def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Tally Sky Map review CSVs into the Star Mapper.")
    ap.add_argument("csv", nargs="+"); ap.add_argument("--cosmos-map", default="cosmos_map")
    a = ap.parse_args(argv)
    out = pathlib.Path(a.cosmos_map); store_path = out / "community_reviews.json"; store = load(store_path)
    added = sum(merge(store, pathlib.Path(f)) for f in a.csv)
    json.dump(store, open(store_path, "w", encoding="utf-8"), indent=1)
    pr = priority(store)
    json.dump({"generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "note": "Ordered by reviewer support; opinions, not confirmations.", "stars": pr},
              open(out / "recheck_priority.json", "w", encoding="utf-8"), indent=1)
    print(f"added {added} votes from {len(a.csv)} file(s); {len(store['stars'])} stars reviewed; {len(pr)} in the recheck priority list")
    return 0

if __name__ == "__main__":
    sys.exit(main())
