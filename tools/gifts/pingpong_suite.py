#!/usr/bin/env python3
"""The ping-pong suite: one command that re-runs every gift tool's LOCKED tests, its Python-vs-JS parity check,
and checks the Lantern header is present. Runs locally and in CI (.github/workflows/tools.yml, job `gifts`).
Referee rounds themselves are recorded in tools/gifts/REFEREE_LEDGER.md (a referee is a person or an independent agent;
this suite is the part that can be re-run by anyone, any time).
Danny Lee Eldridge / the Weave. A lantern, not a throne."""
import subprocess, json, sys, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def all_pass(obj):
    """True if every pass-flag found anywhere in the JSON is true (and at least one exists)."""
    flags = []
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, bool) and (k in ('pass_', 'ALL_PASS') or k.endswith('_pass') or k.endswith('_pass_any')): flags.append(v)
                walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(obj); return bool(flags) and all(flags), len(flags)

SUITE = [
 dict(name='Spindle (Liu, spinor BEC)', lock='D2183', cwd='.', cmds=[['python3', 'tools/qsim/validate_d2183.py']],
      json='field_tests/results/d2183_loom_qsim.json', html='releases/liu_gift_2026-11-23/tool/Spindle.html'),
 dict(name='Zurvan (Baer, Delta_EW)', lock='D2187', cwd='tools/gifts/zurvan', cmds=[['python3', 'test_d2187.py'], ['node', 't2_check.js']],
      json=None, parity=('d2187_T2.json', 'maxrel', 1e-3), html='tools/gifts/zurvan/Zurvan.html',
      note='T1 is a recorded convention difference (not a pass) by the locked rule; T2 parity must pass'),
 dict(name='Aion (Babu, Zee-Babu)', lock='D2188', cwd='tools/gifts/aion', cmds=[['python3', 'test_d2188.py']],
      json='tools/gifts/aion/d2188_tests.json', parity=('d2188_jscheck.json', 'js_vs_py_worst', 1e-12), html='tools/gifts/aion/Aion.html'),
 dict(name='Chronos (nuclear rung)', lock='D2189', cwd='tools/gifts/chronos',
      cmds=[['python3', 'test_d2189.py'], ['python3', 'chronos_branches.py'], ['python3', 'chronos_a3.py']],
      json=['tools/gifts/chronos/d2189_tests.json', 'tools/gifts/chronos/d2189_branches.json', 'tools/gifts/chronos/d2189_a3.json'],
      parity=('d2189_a3_jscheck.json', 'a3_js_vs_py_worst', 1e-12), html='tools/gifts/chronos/Chronos.html'),
]

def run():
    ok_all = True; rows = []
    for t in SUITE:
        cwd = os.path.join(ROOT, t['cwd']); ok = True; why = []
        for c in t['cmds']:
            if c[0] == 'node' and not shutil_which('node'): why.append('node missing: parity file used as recorded'); continue
            r = subprocess.run(c, cwd=cwd, capture_output=True, text=True, timeout=900)
            if r.returncode != 0: ok = False; why.append(f'{" ".join(c)} exit {r.returncode}: {r.stderr[-300:]}')
        js = t.get('json'); js = [js] if isinstance(js, str) else (js or [])
        nflags = 0
        for j in js:
            p, n = all_pass(json.load(open(os.path.join(ROOT, j)))); nflags += n
            if not p: ok = False; why.append(f'{j}: a locked test failed')
        if t.get('parity'):
            f, key, tol = t['parity']; d = json.load(open(os.path.join(cwd, f)))
            vals = [d[key]] if key in d else [v.get(key) for v in d.values() if isinstance(v, dict) and key in v]
            if not vals or max(vals) > tol: ok = False; why.append(f'parity {key} = {vals} > {tol}')
        html = open(os.path.join(ROOT, t['html'])).read()
        if 'lantern, not a throne' not in html: ok = False; why.append('Lantern missing from the tool')
        rows.append((t['name'], t['lock'], ok, nflags, '; '.join(why) or t.get('note', '')))
        ok_all &= ok
    for n, l, ok, k, w in rows: print(f"{'PASS' if ok else 'FAIL'}  {n:32s} {l}  locked flags checked: {k:3d}  {w}")
    print('SUITE', 'PASS' if ok_all else 'FAIL'); return ok_all

def shutil_which(x):
    import shutil; return shutil.which(x)

if __name__ == '__main__':
    sys.exit(0 if run() else 1)
