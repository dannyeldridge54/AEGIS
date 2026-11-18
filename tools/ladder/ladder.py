# AEGIS-FP VKJA3QFRB3AFOYN4 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""AEGIS update ladder: D-note MAP lines -> theory map -> Whiteboard data -> Star Mapper model card.

    python tools/ladder/ladder.py update     # apply new MAP lines, flag downstream nodes, write exports
    python tools/ladder/ladder.py flags      # list nodes waiting for a recheck (the next Ddl tick starts here)
    python tools/ladder/ladder.py clear ID   # mark a node rechecked (after the D-note that resolves it)
    python tools/ladder/ladder.py check      # CI: every D-note from MAP_FROM on has a MAP line; flags not stale

MAP line (inside a D-note):  MAP: node=<id> status=<status> touches=[id1, id2] [ripple=no]
(ripple=no: the change confirms rather than alters the node, so only the touched nodes are flagged)
Statuses: computed estimate literature assumed corrected killed open frozen.
A frozen node keeps its status; it only gets a recheck flag. AI-assisted.
"""
from __future__ import annotations
import argparse, json, pathlib, re, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
MAP = ROOT / "theory/map/map.yaml"
NOTES = ROOT / "theory/pending_docs/D72_D75_weak_spots.md"
STATE = ROOT / "theory/map/ladder_state.json"
EXPORT = ROOT / "docs/map/map.json"
CARD = ROOT / "ufe-v2/model_current.json"
MAP_FROM = 739            # MAP lines are required from this D-number on
STALE_AFTER = 5           # a flag older than this many D-notes fails `check`
STATUSES = {"computed", "estimate", "literature", "assumed", "corrected", "killed", "open", "frozen", "postulate"}
LINE = re.compile(r"MAP:\s*node=(\S+)\s+status=(\S+)(?:\s+touches=\[([^\]]*)\])?(\s+ripple=no)?")
HEAD = re.compile(r"^## D(\d+)([a-z]?)\b", re.M)

class DN(float):
    """A D-number that orders correction notes (D765a) just after their parent and prints as written."""
    def __new__(cls, n, suf=""):
        o = float.__new__(cls, int(n) + (ord(suf) - 96) / 100 if suf else int(n)); o.label = f"{int(n)}{suf}"; return o
    def __str__(self): return self.label
    __repr__ = __str__
    def __format__(self, spec): return format(self.label, spec)

def load(p=MAP): return yaml.safe_load(open(p, encoding="utf-8"))
def save(m, p=MAP): open(p, "w", encoding="utf-8").write(yaml.safe_dump(m, sort_keys=False, allow_unicode=True, width=200))

def notes(text):
    """Yield (D-number, body) for each D-note."""
    hs = list(HEAD.finditer(text))
    for i, h in enumerate(hs):
        yield DN(h.group(1), h.group(2)), text[h.end(): hs[i + 1].start() if i + 1 < len(hs) else len(text)]

def downstream(m, start):
    kids = {}
    for n in m["nodes"]:
        for d in n.get("depends", []) or []:
            kids.setdefault(d, []).append(n["id"])
    seen, todo = set(), list(start)
    while todo:
        x = todo.pop()
        for k in kids.get(x, []):
            if k not in seen:
                seen.add(k); todo.append(k)
    return seen

def _done_from_watermark(text, last):
    """Migration: replay the old watermark rule to recover exactly which notes it applied (notes written out of order,
    e.g. D1265a after D1280, were skipped by it and are NOT done)."""
    done, run = set(), MAP_FROM - 1
    for dn, _ in notes(text):
        if dn > run and dn <= last:
            done.add(str(dn))
        run = max(run, dn)
    return done

def update(m, text, last, done=None):
    byid = {n["id"]: n for n in m["nodes"]}
    applied = []
    if done is None:
        done = _done_from_watermark(text, last)
    for dn, body in notes(text):
        if dn < MAP_FROM or str(dn) in done:
            continue
        done.add(str(dn))
        for node, status, touches, noripple in LINE.findall(body):
            if node not in byid:
                raise SystemExit(f"D{dn}: MAP line names unknown node '{node}' (add it to map.yaml first)")
            if status not in STATUSES:
                raise SystemExit(f"D{dn}: unknown status '{status}'")
            n = byid[node]
            latest = max([DN(*re.match(r"D(\d+)([a-z]?)$", x).groups()) for x in n.get("d", []) if re.match(r"D\d+[a-z]?$", x)] or [DN(0)])
            if dn < latest:
                # out-of-order note (e.g. a correction written after newer notes): record it, but never roll the
                # node's status or flags back to an older state
                n.setdefault("d", [])
                if f"D{dn}" not in n["d"]:
                    n["d"].append(f"D{dn}")
                hist = n.setdefault("history", []); hist.append(f"D{dn}: {status} (late)"); n["history"] = hist[-3:]
                applied.append((dn, node, status + " (late, recorded only)"))
                continue
            if n.get("status") != "frozen":
                n["status"] = status
            n.setdefault("d", [])
            if f"D{dn}" not in n["d"]:
                n["d"].append(f"D{dn}")
            fm0 = re.match(r"recheck \(D(\d+)([a-z]?),", n.get("flag", ""))
            if not fm0 or DN(*fm0.groups()) <= dn:   # a note clears only flags raised by older notes
                n.pop("flag", None)
            hist = n.setdefault("history", []); hist.append(f"D{dn}: {status}"); n["history"] = hist[-3:]
            t = [x.strip() for x in touches.split(",") if x.strip()]
            for k in (set(t) if noripple else downstream(m, [node] + t) | set(t)):
                if k != node and k in byid:
                    fm = re.match(r"recheck \(D(\d+)([a-z]?),", byid[k].get("flag", ""))
                    if not fm or DN(*fm.groups()) <= dn:   # never replace a newer flag with an older note's
                        byid[k]["flag"] = f"recheck (D{dn}, {node})"
                elif k != node:
                    print(f"ladder: D{dn} touches unknown map id '{k}' (ignored; web-only node?)")
            applied.append((dn, node, status))
        last = max(last, dn)
    return applied, last, done

def export(m):
    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    out = {"layers": {1: "Inputs", 2: "Model core", 3: "Microscopic origin", 4: "After inflation", 5: "Predictions & tests"},
           "nodes": m["nodes"], "observing": m.get("observing", [])}
    json.dump(out, open(EXPORT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def card(m, applied):
    if not CARD.exists():
        return
    c = json.load(open(CARD, encoding="utf-8"))
    ch = c.get("changed_since_freeze", [])
    byid = {n["id"]: n for n in m["nodes"]}
    for dn, node, status in applied:
        ch.append(f"D{dn}: {byid[node]['title']} → {status}")
    c["changed_since_freeze"] = ch[-12:]
    c["open_rechecks"] = [n["title"] for n in m["nodes"] if n.get("flag")]
    import datetime
    c["updated"] = datetime.date.today().isoformat()
    json.dump(c, open(CARD, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["update", "flags", "clear", "check", "export"]); ap.add_argument("id", nargs="?")
    a = ap.parse_args(argv); m = load()
    st = json.load(open(STATE)) if STATE.exists() else {"last": MAP_FROM - 1}
    text = NOTES.read_text(encoding="utf-8")
    if a.cmd == "update":
        applied, st["last"], done = update(m, text, st["last"], set(st["done"]) if "done" in st else None)
        st["done"] = sorted(done)
        save(m); export(m); card(m, applied); json.dump(st, open(STATE, "w"))
        print(f"applied {len(applied)} MAP line(s); last D{st['last']}; flagged: {sum(1 for n in m['nodes'] if n.get('flag'))}")
    elif a.cmd == "flags":
        for n in m["nodes"]:
            if n.get("flag"):
                print(f"{n['id']:16s} {n['flag']:34s} {n['title']}")
    elif a.cmd == "clear":
        n = next((n for n in m["nodes"] if n["id"] == a.id), None)
        if not n: raise SystemExit("unknown node")
        n.pop("flag", None); save(m); export(m); print("cleared", a.id)
    elif a.cmd == "export":
        export(m); print("wrote", EXPORT.relative_to(ROOT))
    else:
        bad = [dn for dn, body in notes(text) if dn >= MAP_FROM and not LINE.search(body) and "MAP: none" not in body]
        top = max((dn for dn, _ in notes(text)), default=0)
        stale = [n["id"] for n in m["nodes"] if n.get("flag") and top - int(re.search(r"D(\d+)", n["flag"]).group(1)) > STALE_AFTER]
        if bad or stale:
            print("D-notes without a MAP line:", bad, "| stale rechecks:", stale); return 1
        print("ladder OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
