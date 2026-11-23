"""Preflight guard (Danny 13:48 'limit this'): run BEFORE any locked compute. Catches the author's recurring slips:
1) code that does not compile (inline comments eating brackets crashed 3 runs on 23 Nov);
2) a PREREG whose .sha256 no longer matches (edited after locking);
3) goalpost values already corrected in a DEVIATIONS file reappearing in a new lock or test (stale goalposts: L1/L3/L8, R3, U-238).
Usage: python3 preflight.py [files...]  -> exit 1 on any problem."""
import glob, hashlib, os, py_compile, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..')); RULES = os.path.join(ROOT, 'field_tests', 'rules')
STALE = {  # value (as written) -> why it is stale / what replaced it
    r'\b0\.7997\b': 'neutron share: 14.07 shortcut; relativistic 0.7976 (FUSION-1 DEV-1)',
    r'\b14\.07\b': 'neutron energy shortcut; relativistic 14.028 MeV',
    r'5\.9 keV at 15\.7': 'Gamow 5.9 keV is the 15 MK value; 15.7 MK gives 6.07-6.09 keV (FUSION-1 DEV-2)',
    r'\b55\.8\b(?! *-)': 'tritium burn 55.8 kg was a shortcut; derived 56.08 kg/GW-fpy',
    r'3\.0 *<= *a\[.tau_E.\] *<= *4\.4|3\.0-4\.4 s': 'ITER 500 MW tau window relocked to 3.4 s +-15% (FUSION-1 DEV-7)',
    r'\b336\b': 'Mn-55 s-wave resonance ER is 340.7875 eV (N3/N4 DEV-2)',
    r'\b4\.468e9\b': 'U-238 half-life NUBASE2020 4.463e9 y (CM-CARDS DEV-1)',
    r'elif rng\.random\(\) < r:': 'Kalbach-Mann branch swapped (N6-N8 DEV-1): precompound with probability r'}
def main(files):
    bad = []
    for f in files or sorted(glob.glob(os.path.join(HERE, '*.py'))):
        try: py_compile.compile(f, doraise=True)
        except py_compile.PyCompileError as e: bad.append(f'COMPILE {os.path.basename(f)}: {str(e).splitlines()[-1][:160]}')
    for p in sorted(glob.glob(os.path.join(RULES, 'PREREG_*.md'))):
        if p.endswith('_DEVIATIONS.md') or 'DEVIATIONS' in p: continue
        h = p + '.sha256'
        if os.path.exists(h):
            want = open(h).read().split()[0]; got = hashlib.sha256(open(p, 'rb').read()).hexdigest()
            if want != got: bad.append(f'LOCK EDITED {os.path.basename(p)}')
    targets = (files or sorted(glob.glob(os.path.join(HERE, 'test_*.py')))) + [p for p in glob.glob(os.path.join(RULES, 'PREREG_*.md')) if 'DEVIATIONS' not in p]
    for f in targets:
        if f.endswith('preflight.py'): continue
        txt = open(f, encoding='utf-8', errors='ignore').read()
        for pat, why in STALE.items():
            for m in re.finditer(pat, txt):
                line = txt[:m.start()].count('\n') + 1; ctx = txt.splitlines()[line - 1]
                if 'DEV' in ctx or 'stale' in ctx.lower(): continue
                bad.append(f'STALE? {os.path.relpath(f, ROOT)}:{line}: {why}')
    return bad
BASE = os.path.join(HERE, 'preflight_baseline.txt')   # historical findings (the record) accepted once; only NEW findings fail
if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--baseline']; b = main(args)
    if '--baseline' in sys.argv: open(BASE, 'w').write('\n'.join(b) + '\n'); print(f'baseline written ({len(b)} accepted)'); sys.exit(0)
    old = set(open(BASE).read().splitlines()) if os.path.exists(BASE) else set(); new = [x for x in b if x not in old]
    print('\n'.join(new) if new else f'preflight OK ({len(b)} historical findings in baseline)'); sys.exit(1 if new else 0)
