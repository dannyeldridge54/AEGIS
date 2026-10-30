"""Local-only audit, all CPU cores: for every swept tile, rows on disk must equal the count recorded at sweep time."""
import gzip, json, os, sys, time
from multiprocessing import Pool, cpu_count

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cosmos_map")


def rows(t):
    with gzip.open(os.path.join(OUT, "tiles", "L5", f"{t:05d}.csv.gz"), "rb") as f:
        n = 0
        for chunk in iter(lambda: f.read(1 << 22), b""):
            n += chunk.count(b"\n")
    return t, n - 1


if __name__ == "__main__":
    done = {int(k): v["n"] for k, v in json.load(open(os.path.join(OUT, "sweep_state.json"), encoding="utf-8"))["done"].items()}
    t0 = time.time(); bad = []; total = 0
    with Pool(cpu_count()) as p:
        for i, (t, n) in enumerate(p.imap_unordered(rows, sorted(done), chunksize=16), 1):
            total += n
            if n != done[t]:
                bad.append((t, done[t], n))
            if i % 2000 == 0:
                print(f"{i:,}/{len(done):,} tiles, {time.time() - t0:.0f}s")
    print(f"LOCAL AUDIT: {len(done):,} tiles, {total:,} stars on disk, {len(done) - len(bad):,} match the recorded count, "
          f"{len(bad)} mismatches, {time.time() - t0:.0f}s on {cpu_count()} cores")
    for b in bad[:20]:
        print("  mismatch tile %d: recorded %d, on disk %d" % b)
    json.dump({"tiles": len(done), "stars_on_disk": total, "mismatches": bad, "finished": time.time()},
              open(os.path.join(OUT, "verify_local.json"), "w"))
