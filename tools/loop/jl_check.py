"""Jl loop mechanical checks (K1 lock-before-compute, K2 labels, K7 map line, beta3 postulate budget, beta4 derived:assumed). AI-assisted.
Usage (repo root): python tools/loop/jl_check.py D762"""
import re, subprocess, sys, pathlib, yaml
R = pathlib.Path(__file__).resolve().parents[2]
def gitt(p):
    o = subprocess.run(["git", "log", "-1", "--format=%ct", "--", str(p)], cwd=R, capture_output=True, text=True).stdout.strip()
    return int(o) if o else None
def main(d):
    n = d.lstrip("D"); ok = True; out = []
    notes = (R/"theory/pending_docs/D72_D75_weak_spots.md").read_text()
    m = re.search(rf"^## D{n}\b.*?(?=^## D|\Z)", notes, re.S | re.M)
    if not m: print(f"FAIL: no note D{n}"); return 1
    body = m.group(0)
    # K1
    locks = list((R/"field_tests/rules").glob(f"PREREG_D{n}_*.md")); locks = [l for l in locks if "DEVIATIONS" not in l.name]
    res = list((R/"field_tests/results").glob(f"*_d{n}*.txt"))
    if res and not locks: ok = False; out.append("K1 FAIL: results but no lock")
    for l in locks:
        tl = gitt(l)
        for r in res:
            tr = gitt(r)
            if tl and tr and tr < tl: ok = False; out.append(f"K1 FAIL: {r.name} committed before {l.name}")
    out.append(f"K1 ok ({len(locks)} lock, {len(res)} result)" if ok else "")
    # K7
    mp = re.findall(r"MAP:\s*(node=\S+\s+status=(\S+)|none)", body)
    if not mp: ok = False; out.append("K7 FAIL: no MAP line")
    else: out.append("K7 ok")
    if "POSTULATE" in body and not any(s == "assumed" for _, s in mp): ok = False; out.append("K7 FAIL: postulate without status=assumed")
    # K2
    log = (R/"theory/derivations/DERIVATION_LOG.md").read_text()
    sec = re.search(rf"^## D{n}\b.*?(?=^## |\Z)", log, re.S | re.M)
    if not sec: ok = False; out.append("K2 FAIL: no DERIVATION_LOG section")
    else:
        steps = [x for x in sec.group(0).splitlines() if re.match(r"\s*\d+\.", x)]
        bad = [x for x in steps if not re.search(r"\[(derived|literature|postulate P\d+|estimate)\]", x)]
        if bad: ok = False; out.append(f"K2 FAIL: {len(bad)} unlabelled step(s)")
        else: out.append(f"K2 ok ({len(steps)} steps)")
    # beta3, beta4
    P = R/"theory/derivations/POSTULATES.md"
    openp = re.findall(r"^## (P\d+).*status: open", P.read_text(), re.M) if P.exists() else []
    out.append(f"b3 {'FLAG' if len(openp) > 2 else 'ok'}: open postulates {len(openp)} {openp}")
    nodes = yaml.safe_load((R/"theory/map/map.yaml").read_text())
    nodes = nodes["nodes"] if isinstance(nodes, dict) else nodes
    cnt = {}
    for x in nodes: cnt[x.get("status")] = cnt.get(x.get("status"), 0) + 1
    out.append(f"b4 map statuses: {dict(sorted(cnt.items(), key=lambda kv: str(kv[0])))}")
    print("\n".join(o for o in out if o)); print("JL CHECK:", "PASS" if ok else "FAIL"); return 0 if ok else 1
if __name__ == "__main__": sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
