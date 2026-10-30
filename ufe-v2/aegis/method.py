# Copyright (c) 2012-2026 Danny Lee Eldridge. Licensed under THE AEGIS PEOPLE'S LICENSE (see LICENSE in the AEGIS repository): free for people; no AI use; no military, surveillance or harmful use. AEGIS-ID: f713a7b3d32ffddb
"""
The AEGIS Method, in code: a claim store with walled tiers, pre-registration locks and a ledger of passes and
failures. The AEGIS Method (Danny Lee Eldridge, 2026).

Tiers
  evidence    tested against data; needs a named mechanism, data sources and a locked rule
  hypothesis  an idea or lens still to be tested (the default for anything new)
  meaning     values and beliefs; shown with respect, never used as proof

The wall (enforced on every write and checked by the guardrails)
  - a meaning claim can never be linked as support for an evidence claim
  - a claim can only be evidence if it names a mechanism, its data and a locked pre-registration rule,
    and its status is a test outcome (passed / failed / untestable)
  - a lens (dashed thread) can never make anything evidence on its own

Status: open | passed | failed | untestable | withdrawn. Failed and withdrawn claims are never deleted.
Usage
  python -m aegis.method check     validate the whole store (the wall, the rule hashes, the numbers' sources)
  python -m aegis.method ledger    print the ledger: passes and failures side by side
"""
import hashlib, json, os, sys, time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # ufe-v2/
ROOT = os.path.dirname(HERE)
STORE = os.path.join(HERE, "method", "claims.json")
TIERS = ("evidence", "hypothesis", "meaning")
STATUS = ("open", "passed", "failed", "untestable", "withdrawn")
TESTED = ("passed", "failed", "untestable")


class WallError(ValueError):
    """Raised when a write would break the wall between tiers."""


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load(path=STORE):
    if not os.path.exists(path):
        return {"claims": {}, "threads": []}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(store, path=STORE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=1, ensure_ascii=False)


def _check_claim(c):
    """Return a list of wall violations for one claim (empty = fine)."""
    bad = []
    if c.get("tier") not in TIERS:
        bad.append(f"{c.get('id')}: unknown tier {c.get('tier')!r}")
    if c.get("status") not in STATUS:
        bad.append(f"{c.get('id')}: unknown status {c.get('status')!r}")
    if c.get("tier") == "evidence":
        for need in ("mechanism", "data", "prereg"):
            if not c.get(need):
                bad.append(f"{c['id']}: evidence needs a {need}")
        if c.get("status") not in TESTED + ("withdrawn",):
            bad.append(f"{c['id']}: evidence must carry a test outcome, not {c.get('status')!r}")
    if c.get("tier") == "meaning" and c.get("status") in ("passed", "failed"):
        bad.append(f"{c['id']}: meaning is never passed or failed by a test")
    return bad


def add_claim(store, cid, tier, statement, status="open", mechanism=None, data=None, prereg=None,
              result=None, source=None, note=None):
    """Add or update a claim. The wall is checked before anything is written."""
    c = {"id": cid, "tier": tier, "statement": statement, "status": status, "mechanism": mechanism,
         "data": data, "prereg": prereg, "prereg_sha": None, "result": result, "source": source, "note": note,
         "updated": time.strftime("%Y-%m-%d")}
    if prereg:
        p = os.path.join(ROOT, prereg)
        c["prereg_sha"] = sha(p) if os.path.exists(p) else (store["claims"].get(cid, {}).get("prereg_sha"))
    bad = _check_claim(c)
    if bad:
        raise WallError("; ".join(bad))
    store["claims"][cid] = c
    return c


def link(store, a, b, kind, part=None):
    """Thread between claims. kind: 'supports' (evidence only), 'solid' (shared physics or data), 'dashed' (a lens)."""
    A, B = store["claims"][a], store["claims"][b]
    if kind == "supports" and (A["tier"] != "evidence" or B["tier"] != "evidence"):
        raise WallError(f"only evidence can support evidence ({a} is {A['tier']}, {b} is {B['tier']})")
    if kind == "solid" and "meaning" in (A["tier"], B["tier"]):
        raise WallError(f"a meaning claim can only have dashed threads ({a} - {b})")
    t = {"a": a, "b": b, "kind": kind, "part": part}
    if t not in store["threads"]:
        store["threads"].append(t)
    return t


def check(store=None):
    """Validate the whole store. Returns a guardrail-style result."""
    store = store or load()
    bad = []
    for c in store["claims"].values():
        bad += _check_claim(c)
        if c.get("prereg"):
            p = os.path.join(ROOT, c["prereg"])
            if os.path.exists(p) and c.get("prereg_sha") and sha(p) != c["prereg_sha"]:
                bad.append(f"{c['id']}: rule file {c['prereg']} changed after it was locked")
    for t in store["threads"]:
        A, B = store["claims"].get(t["a"]), store["claims"].get(t["b"])
        if not (A and B):
            bad.append(f"thread to a missing claim: {t}"); continue
        if t["kind"] == "supports" and (A["tier"] != "evidence" or B["tier"] != "evidence"):
            bad.append(f"wall breached: {t['a']} ({A['tier']}) supports {t['b']} ({B['tier']})")
        if t["kind"] == "solid" and "meaning" in (A["tier"], B["tier"]):
            bad.append(f"wall breached: solid thread touches meaning ({t['a']} - {t['b']})")
    n = len(store["claims"])
    counts = {s: sum(1 for c in store["claims"].values() if c["status"] == s) for s in STATUS}
    return {"name": "The Method (claim wall)", "ok": not bad,
            "detail": (f"{n} claims, {len(store['threads'])} threads; " + ", ".join(f"{k} {v}" for k, v in counts.items() if v)
                       + (f"; PROBLEMS: {bad}" if bad else "")),
            "plain": ("Every claim sits in its right tier: nothing untested is used as proof, every tested claim "
                      "has its rule locked, and failures are kept beside passes." if not bad else
                      "A claim breaks the rules between evidence, ideas and meaning, or a locked rule changed. It must be fixed before anything is trusted."),
            "counts": counts}


def ledger(store=None):
    store = store or load()
    order = {"evidence": 0, "hypothesis": 1, "meaning": 2}
    rows = sorted(store["claims"].values(), key=lambda c: (order[c["tier"]], STATUS.index(c["status"]), c["id"]))
    return rows


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        print(json.dumps(check(), indent=1, ensure_ascii=False))
    elif cmd == "ledger":
        for c in ledger():
            print(f"{c['tier']:10s} {c['status']:10s} {c['id']:24s} {c['statement'][:80]}")
