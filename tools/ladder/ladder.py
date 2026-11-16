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
STATUSES = {"computed", "estimate", "literature", "assumed", "corrected", "killed", "open", "frozen"}
LINE = re.compile(r"MAP:\s*node=(\S+)\s+status=(\S+)(?:\s+touches=\[([^\]]*)\])?(\s+ripple=no)?")
HEAD = re.compile(r"^## D(\d+)", re.M)

def load(p=MAP): return yaml.safe_load(open(p, encoding="utf-8"))
def save(m, p=MAP): open(p, "w", encoding="utf-8").write(yaml.safe_dump(m, sort_keys=False, allow_unicode=True, width=200))

def notes(text):
    """Yield (D-number, body) for each D-note."""
    hs = list(HEAD.finditer(text))
    for i, h in enumerate(hs):
        yield int(h.group(1)), text[h.end(): hs[i + 1].start() if i + 1 < len(hs) else len(text)]

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

def update(m, text, last):
    byid = {n["id"]: n for n in m["nodes"]}
    applied = []
    for dn, body in notes(text):
        if dn <= last:
            continue
        for node, status, touches, noripple in LINE.findall(body):
            if node not in byid:
                raise SystemExit(f"D{dn}: MAP line names unknown node '{node}' (add it to map.yaml first)")
            if status not in STATUSES:
                raise SystemExit(f"D{dn}: unknown status '{status}'")
            n = byid[node]
            if n.get("status") != "frozen":
                n["status"] = status
            n.setdefault("d", [])
            if f"D{dn}" not in n["d"]:
                n["d"].append(f"D{dn}")
            n.pop("flag", None)
            hist = n.setdefault("history", []); hist.append(f"D{dn}: {status}"); n["history"] = hist[-3:]
            t = [x.strip() for x in touches.split(",") if x.strip()]
            for k in (set(t) if noripple else downstream(m, [node] + t) | set(t)):
                if k != node:
                    byid[k]["flag"] = f"recheck (D{dn}, {node})"
            applied.append((dn, node, status))
        last = max(last, dn)
    return applied, last

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
    json.dump(c, open(CARD, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["update", "flags", "clear", "check", "export"]); ap.add_argument("id", nargs="?")
    a = ap.parse_args(argv); m = load()
    st = json.load(open(STATE)) if STATE.exists() else {"last": MAP_FROM - 1}
    text = NOTES.read_text(encoding="utf-8")
    if a.cmd == "update":
        applied, st["last"] = update(m, text, st["last"])
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
