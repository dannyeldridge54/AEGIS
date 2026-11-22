#!/usr/bin/env python3
"""D1989 P1.8 (C8): no goalpost in a scored result may read plain 'PASS' when its kind is FIT, or when it is a live PRED depending on a spent fit.
Usage: python3 tools/loom/pass_label_check.py [result.json ...]  -> violations; exit 1 if any."""
import json, sys, glob, os
DEP = {'as': {'m32', 'split'}, 'M2': {'m32'}, 'Y': {'TR', 'MN'}, 'Om': {'TR', 'm32'}, 'ns': {'TR'}, 'u': {'u'}, 'rung': {'u'}, 'MN': {'MN'}}
def check(path):
    o = json.load(open(path)); GP = {g['id']: g for g in json.load(open('tools/loom/goalposts.json'))['goalposts']}; fits = set(o.get('fits_spent', [])); bad = []
    for L, rows in (o.get('scoreboard') or {}).items():
        for r in rows:
            g = GP.get(r['id']); lab = r['final']
            if not g or lab != 'PASS': continue
            if g['kind'] == 'FIT': bad.append((r['id'], 'kind FIT labelled PASS'))
            if g['kind'] == 'PRED' and g['live'] and DEP.get(g['live'], set()) & fits: bad.append((r['id'], 'live PRED at fitted knobs %s labelled PASS' % sorted(DEP[g['live']] & fits)))
    return bad
if __name__ == '__main__':
    files = sys.argv[1:] or sorted(glob.glob('field_tests/results/d19*_woven_run*.json'))
    tot = 0
    for f in files:
        b = check(f); tot += len(b); print(os.path.basename(f), 'violations', len(b), b)
    sys.exit(1 if tot else 0)
