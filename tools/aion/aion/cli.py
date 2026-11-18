# AEGIS-FP 5KMGRH6FMEX2P5VS · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Command line: aion new | lock | deviate | check."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
from . import core, __version__

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="aion", description="AION — lock before you look (pre-registration kit).")
    ap.add_argument("--version", action="version", version=f"aion {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="create a PREREG file from the template")
    n.add_argument("id"); n.add_argument("title"); n.add_argument("--dir", default="field_tests/rules")
    n.add_argument("--script", default=""); n.add_argument("--output", default="")
    l = sub.add_parser("lock", help="hash a PREREG file and commit it (before running anything)")
    l.add_argument("file"); l.add_argument("--no-commit", action="store_true"); l.add_argument("--push", action="store_true")
    d = sub.add_parser("deviate", help="open the DEVIATIONS file for an id (write it BEFORE any rerun)")
    d.add_argument("id"); d.add_argument("--dir", default="field_tests/rules")
    c = sub.add_parser("check", help="verify every result file was preceded by its lock")
    c.add_argument("--repo", default="."); c.add_argument("--all", action="store_true", help="list OK files too")
    c.add_argument("--strict", action="store_true", help="exit 1 on LATE, NO_LOCK or HASH_MISMATCH")
    a = ap.parse_args(argv)
    if a.cmd == "new":
        p = core.new_prereg(Path(a.dir), a.id, a.title, a.script, a.output); print(p); return 0
    if a.cmd == "lock":
        side = core.lock(Path(a.file), commit=not a.no_commit, push=a.push); print(side.read_text().strip()); return 0
    if a.cmd == "deviate":
        print(core.new_deviation(Path(a.dir), a.id)); return 0
    if a.cmd == "check":
        fs = core.check(Path(a.repo))
        for f in fs:
            if a.all or f.status != "OK":
                print(f"{f.status:14s} {f.ident or '-':>6s}  {f.result}  {f.detail}")
        s = core.summary(fs); print("summary:", ", ".join(f"{k} {v}" for k, v in sorted(s.items())))
        bad = sum(s.get(k, 0) for k in ("LATE", "NO_LOCK", "HASH_MISMATCH"))
        return 1 if (a.strict and bad) else 0
    return 2

if __name__ == "__main__":
    sys.exit(main())
