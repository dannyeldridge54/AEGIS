# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Snapshot ("golden") outputs of every aegis command. A change that moves any number beyond the tolerance fails CI and names it.
  python -m tools.golden.golden record   -> rewrite tools/golden/golden.json (only after a deliberate, documented change)
  python -m tools.golden.golden check    -> compare (exit 1 on any drift)"""
import json, math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE)); FILE = os.path.join(HERE, 'golden.json')
CMDS = ['cern xsec 700 14', 'cern life 1000', 'cern limit ATLAS_136', 'cern higgsino 500 14', 'lattice energy E6 1.25',
        'janus 0.5*phi**2 60', 'hyperion orbit 269.452 4.6934 1.8266 -802.8 10362.4 -110.5 MWPotential2014',
        'late dist 1.0', 'late desi -0.75 -0.86', 'late growth 0.5', 'serapis predict 1.15e-6', 'serapis meter 0.9728 0.0027',
        'serapis j 0.2 1.3', 'wavelength line H 2 3', 'wavelength 21cm', 'wavelength convert 500 nm', 'power solar', 'power rc 1000 1000 1e-6']
RTOL = 1e-6
def run(cmd):
    r = subprocess.run([sys.executable, '-m', 'tools.aegis_cli'] + cmd.split(), cwd=ROOT, capture_output=True, text=True, timeout=600)
    t = r.stdout; i = t.find('{')
    if r.returncode or i < 0: raise RuntimeError(f'{cmd}: {r.stderr[-300:] or t[-300:]}')
    return json.loads(t[i:t.rfind('}') + 1])
def numbers(x, path=''):
    if isinstance(x, bool) or x is None: return
    if isinstance(x, (int, float)): yield path, float(x)
    elif isinstance(x, dict):
        for k, v in x.items(): yield from numbers(v, f'{path}.{k}')
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from numbers(v, f'{path}[{i}]')
def compare(old, new):
    a, b = dict(numbers(old)), dict(numbers(new)); bad = []
    for k in a:
        if k not in b: bad.append(f'{k} missing'); continue
        x, y = a[k], b[k]
        if not (math.isclose(x, y, rel_tol=RTOL, abs_tol=1e-12) or (math.isnan(x) and math.isnan(y))): bad.append(f'{k}: {x} -> {y}')
    return bad
def main(argv):
    if argv[:1] == ['record']:
        json.dump({c: run(c) for c in CMDS}, open(FILE, 'w'), indent=1); print('recorded', len(CMDS)); return 0
    G = json.load(open(FILE)); fails = 0
    for c in CMDS:
        bad = compare(G[c], run(c)) if c in G else ['no snapshot']
        print(('PASS ' if not bad else 'DRIFT') + f'  aegis {c}' + ''.join('\n        ' + b for b in bad[:5])); fails += bool(bad)
    print(f'{len(CMDS) - fails}/{len(CMDS)} unchanged'); return 1 if fails else 0
if __name__ == '__main__': sys.exit(main(sys.argv[1:]))
