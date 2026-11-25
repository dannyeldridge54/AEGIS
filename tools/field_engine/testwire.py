"""Test wire (24 Nov 2026): every section's tests, discovered automatically and run as fast as the machine allows.

- Discovery: every test_*.py under the repo is a job; its SECTION is its tool folder (tools/fusion, theory, ufe-v2, ...).
- Speed: one process per test file, all CPU cores busy, slowest files first (from the last run's timings); a file whose own
  content and whose section's source files are unchanged since its last PASS is skipped (content-hash cache).
- Each file runs with pytest from its own folder first; if collection fails there, once more from the repo root.
- Output: results JSON + a per-section table. Exit code 0 only if nothing failed.
- Honest statuses: PASS, FAIL, TIMEOUT, SKIP_ENV (needs software this machine lacks), CACHED (unchanged since last pass).
Usage:  python testwire.py [--root REPO] [--section tools/fusion] [--all] [--timeout 120] [--jobs N]
        --all ignores the cache. The engine calls run_fast() before its first cycle."""
import argparse, concurrent.futures as cf, hashlib, json, os, re, subprocess, sys, time
from pathlib import Path

SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.pytest_cache', 'papers', 'releases'}   # papers/releases hold frozen copies
ENV_MARKERS = ('ModuleNotFoundError', 'No module named', 'ImportError', 'command not found', 'FileNotFoundError', 'TWIST_PY')

def discover(root):
    root = Path(root); jobs = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if f.startswith('test_') and f.endswith('.py'): jobs.append(Path(dp) / f)
    return sorted(jobs)
def section_of(root, path):
    parts = Path(path).relative_to(root).parts
    if parts[0] in ('tools', 'apps', 'cmb-fit') and len(parts) > 2: return '/'.join(parts[:2])
    return parts[0]
def _hash_dir(d):
    h = hashlib.sha256()
    for p in sorted(Path(d).glob('*.py')):
        try: h.update(p.name.encode()); h.update(p.read_bytes())
        except OSError: pass
    return h.hexdigest()[:16]
def fingerprint(path):
    p = Path(path); d = p.parent
    src = d.parent if d.name == 'tests' else d            # tests/ folder: the code under test sits one level up
    return _hash_dir(d) + (_hash_dir(src) if src != d else '')
def run_one(args):
    root, path, timeout = args; t0 = time.time(); path = Path(path)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', MPLBACKEND='Agg')
    def go(cwd, target):
        return subprocess.run([sys.executable, '-m', 'pytest', '-q', '-x', '--no-header', '-p', 'no:cacheprovider', '-c', os.devnull, '--rootdir', str(cwd), str(target)],
                              cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    try:
        r = go(path.parent, path.name)
        if r.returncode not in (0, 1) or 'error' in r.stdout.lower()[-400:] and ' passed' not in r.stdout:
            r2 = go(root, path)
            if r2.returncode == 0: r = r2
    except subprocess.TimeoutExpired:
        return dict(file=str(path), status='TIMEOUT', seconds=round(time.time() - t0, 1), tail=f'over {timeout} s')
    out = (r.stdout + r.stderr); tail = out.strip().splitlines()[-1][:200] if out.strip() else ''
    m = re.search(r'(\d+) passed', out); n = int(m.group(1)) if m else 0
    if r.returncode == 0: st = 'PASS'
    elif r.returncode == 5: st = 'NO_TESTS'
    elif any(k in out for k in ENV_MARKERS) and ' failed' not in out.replace('0 failed', ''): st = 'SKIP_ENV'
    else: st = 'FAIL'
    detail = ''
    if st in ('FAIL', 'SKIP_ENV'):
        lines = [l for l in out.splitlines() if l.startswith(('E ', 'FAILED', 'ERROR')) or any(k in l for k in ENV_MARKERS)]
        detail = ' | '.join(lines[:3])[:300]
    return dict(file=str(path), status=st, passed=n, seconds=round(time.time() - t0, 1), tail=tail, detail=detail)

def run(root, section=None, use_cache=True, timeout=120, jobs=None, quiet=False):
    root = Path(root).resolve(); cache_f = root / 'tools' / 'field_engine' / '.testwire_cache.json'
    cache = json.loads(cache_f.read_text()) if cache_f.exists() else {}
    files = [f for f in discover(root) if section is None or section_of(root, f) == section]
    results, todo = [], []
    for f in files:
        key = str(f.relative_to(root)); fp = fingerprint(f); c = cache.get(key)
        if use_cache and c and c.get('fp') == fp and c.get('status') == 'PASS':
            results.append(dict(file=str(f), status='CACHED', passed=c.get('passed', 0), seconds=0.0, tail='unchanged since last pass', detail=''))
        else: todo.append((f, fp))
    todo.sort(key=lambda x: -cache.get(str(x[0].relative_to(root)), {}).get('seconds', 5))        # slowest first
    t0 = time.time(); jobs = jobs or os.cpu_count() or 2
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:                                              # each job is its own process
        for (f, fp), r in zip(todo, ex.map(run_one, [(root, f, timeout) for f, _ in todo])):
            results.append(r); cache[str(f.relative_to(root))] = dict(fp=fp, status=r['status'], passed=r.get('passed', 0), seconds=r['seconds'])
            if not quiet and r['status'] not in ('PASS',): print(f"  {r['status']:8s} {Path(r['file']).relative_to(root)}  {r.get('detail') or r['tail']}", flush=True)
    cache_f.write_text(json.dumps(cache, indent=0))
    sections = {}
    for r in results:
        s = sections.setdefault(section_of(root, r['file']), dict(files=0, tests=0, PASS=0, CACHED=0, FAIL=0, TIMEOUT=0, SKIP_ENV=0, NO_TESTS=0, seconds=0.0))
        s['files'] += 1; s['tests'] += r.get('passed', 0); s[r['status']] += 1; s['seconds'] = round(s['seconds'] + r['seconds'], 1)
    summary = dict(root=str(root), wall_seconds=round(time.time() - t0, 1), files=len(results), ran=len(todo),
                   tests_passed=sum(r.get('passed', 0) for r in results), failed=sum(1 for r in results if r['status'] in ('FAIL', 'TIMEOUT')),
                   skipped_env=sum(1 for r in results if r['status'] == 'SKIP_ENV'), sections=sections)
    (root / 'tools' / 'field_engine' / 'testwire_last.json').write_text(json.dumps(dict(summary=summary, results=results), indent=1))
    return summary, results
def run_fast(root):
    """For the engine: cached run; returns {section: ok} so areas with failing tests can be held back."""
    s, _ = run(root, quiet=True); return {k: (v['FAIL'] + v['TIMEOUT'] == 0) for k, v in s['sections'].items()}, s
def table(summary):
    rows = ['section                      files tests  pass cached fail timeout skip-env  seconds']
    for k, v in sorted(summary['sections'].items()):
        rows.append(f"{k:28s} {v['files']:5d} {v['tests']:5d} {v['PASS']:5d} {v['CACHED']:6d} {v['FAIL']:4d} {v['TIMEOUT']:7d} {v['SKIP_ENV']:8d} {v['seconds']:8.1f}")
    rows.append(f"TOTAL files {summary['files']} (ran {summary['ran']}), tests passed {summary['tests_passed']}, failed files {summary['failed']}, skipped (environment) {summary['skipped_env']}, wall {summary['wall_seconds']} s")
    return '\n'.join(rows)
if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('--root', default=str(Path(__file__).resolve().parents[2])); a.add_argument('--section')
    a.add_argument('--all', action='store_true'); a.add_argument('--timeout', type=int, default=120); a.add_argument('--jobs', type=int)
    g = a.parse_args(); s, r = run(g.root, g.section, not g.all, g.timeout, g.jobs); print(table(s)); sys.exit(1 if s['failed'] else 0)
