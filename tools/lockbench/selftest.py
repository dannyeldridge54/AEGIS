# AEGIS-FP BQOXU22LYGREU4WF · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""L-8: pinned environment + one-command self-test.
  python3 tools/lockbench/selftest.py pin     -> writes tools/lockbench/ENV.lock (python, numpy, scipy, sympy, mpmath, gfortran, ASPIC/MMC commits)
  python3 tools/lockbench/selftest.py check   -> compares the running machine to ENV.lock (exit 1 on a major/minor mismatch) and runs every
                                                  tools/*/test_*.py with a 300 s limit each; prints one PASS/FAIL table. Jobs (pcjob, PC runner) call 'check' first."""
import sys, os, json, glob, subprocess, platform
PKG = ('numpy', 'scipy', 'sympy', 'mpmath'); LOCK = 'tools/lockbench/ENV.lock'
def sh(*c, cwd=None):
    try: return subprocess.run(c, capture_output=True, text=True, cwd=cwd).stdout.strip()
    except Exception: return ''
def env():
    e = dict(python=platform.python_version())
    for m in PKG:
        try: e[m] = __import__(m).__version__
        except Exception: e[m] = None
    e['gfortran'] = (sh('gfortran', '-dumpfullversion') or None)
    for name, d in (('aspic', '/home/claude/ext/aspic'), ('mmc', '/home/claude/ext/mmc')):
        e[name] = sh('git', 'rev-parse', '--short', 'HEAD', cwd=d) if os.path.isdir(d) else None
    return e
mm = lambda v: '.'.join(str(v).split('.')[:2]) if v else None
def check_env():
    pin = json.load(open(LOCK)); cur = env(); bad = []
    for k, v in pin.items():
        if k in ('aspic', 'mmc'):
            if cur.get(k) and v and cur[k] != v: bad.append(f'{k} {cur[k]} != pinned {v}')
        elif mm(cur.get(k)) != mm(v) and v is not None: bad.append(f'{k} {cur.get(k)} != pinned {v} (major.minor)')
    return bad, cur
def run_tests():
    R = []
    for t in sorted(glob.glob('tools/*/test_*.py')):
        try: r = subprocess.run([sys.executable, t], capture_output=True, text=True, timeout=300); ok = r.returncode == 0 and 'PASS' in r.stdout
        except subprocess.TimeoutExpired: ok = False
        R.append((t, ok))
    return R
if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ('pin', 'check'): print(__doc__); sys.exit(2)
    if sys.argv[1] == 'pin': json.dump(env(), open(LOCK, 'w'), indent=1); print(open(LOCK).read())
    else:
        bad, cur = check_env(); R = run_tests()
        for t, ok in R: print(f"{'PASS' if ok else 'FAIL'}  {t}")
        print('env:', 'matches ENV.lock' if not bad else 'MISMATCH ' + '; '.join(bad))
        allok = not bad and all(ok for _, ok in R); print('SELFTEST:', 'PASS' if allok else 'FAIL'); sys.exit(0 if allok else 1)
