# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Node sync board for the SERAPIS map (theory/map/map.yaml): keeps all nodes working in tandem.
A node is OUT OF SYNC when one of its inputs (depends) changed in a later D-note than the node's own last D-note:
the node was last checked against an older version of its input. The board ranks the work for the derivation loop:
  1 flagged (ladder recheck)  2 out of sync with an input  3 weakest status (assumed/postulate/estimate/open) longest untouched.
  python tools/ladder/sync.py            -> board (top 12)
  python tools/ladder/sync.py --next     -> the single next node (for the loop)
  python tools/ladder/sync.py --json     -> machine-readable"""
import re, sys, json, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]; MAP = ROOT/'theory/map/map.yaml'; LEDGER = ROOT/'theory/map/sync.yaml'
# sync.yaml: {node: {input: {at: D####, by: D####, verdict: 'no effect: ...' | 'recomputed: ...'}}} — a reviewed pair counts as in sync
WEAK = {'assumed': 0, 'postulate': 1, 'open': 1, 'estimate': 2, 'literature': 3, 'corrected': 4, 'computed': 5, 'frozen': 6, 'killed': 7}
def dnum(s):
    m = re.match(r'D(\d+)([a-z]?)$', s or ''); return int(m.group(1)) + ((ord(m.group(2)) - 96)/100 if m and m.group(2) else 0) if m else 0
def last(n): return max([dnum(x) for x in n.get('d', [])] or [0])
def board(m=None):
    m = m or yaml.safe_load(open(MAP, encoding='utf-8')); nodes = m['nodes']; by = {n['id']: n for n in nodes}
    top = max(last(n) for n in nodes); rows = []
    led = (yaml.safe_load(open(LEDGER, encoding='utf-8')) or {}) if LEDGER.exists() else {}
    for n in nodes:
        L = last(n); rv = led.get(n['id'], {})
        behind = [(p, last(by[p])) for p in n.get('depends', []) if p in by and last(by[p]) > max(L, dnum(rv.get(p, {}).get('at')))]
        rows.append(dict(id=n['id'], title=n.get('title', ''), status=n.get('status'), last=L, age=round(top - L),
                         flag=n.get('flag'), out_of_sync=[f"{p} (D{int(d)} > D{int(L)})" for p, d in behind]))
    key = lambda r: (0 if r['flag'] else 1 if r['out_of_sync'] else 2, WEAK.get(r['status'], 5) if not (r['flag'] or r['out_of_sync']) else 0, -r['age'])
    return sorted(rows, key=key), top
def main(a):
    rows, top = board()
    if '--json' in a: print(json.dumps(rows, indent=1)); return 0
    if '--next' in a:
        r = rows[0]; why = 'flagged: ' + r['flag'] if r['flag'] else ('out of sync with ' + ', '.join(r['out_of_sync']) if r['out_of_sync'] else f"weakest status ({r['status']}), untouched for {r['age']} notes")
        print(f"{r['id']}: {r['title']} — {why}"); return 0
    n_sync = sum(1 for r in rows if r['out_of_sync']); n_flag = sum(1 for r in rows if r['flag'])
    print(f"SERAPIS map, {len(rows)} nodes, latest D{int(top)}: {n_flag} flagged, {n_sync} out of sync with an input")
    for r in rows[:12]:
        tag = 'FLAG' if r['flag'] else ('SYNC' if r['out_of_sync'] else r['status'][:5].upper())
        print(f"  {tag:5s} {r['id']:16s} last D{int(r['last']):<5d} {('behind: ' + '; '.join(r['out_of_sync'])) if r['out_of_sync'] else r['title'][:70]}")
    return 0
if __name__ == '__main__': sys.exit(main(sys.argv[1:]))
