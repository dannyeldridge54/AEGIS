# AEGIS-FP 3X4IX5FEORJQAYCQ · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""L-4: provenance stamp — every results file gets <results>.prov.json recording what produced it.
stamp(results, lock=None, code=[], data=[], t0=None) -> dict ; check(results) -> (ok, problems) re-hashes everything listed."""
import hashlib, json, os, platform, socket, subprocess, sys, time
def _h(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def _pkgs():
    out = {}
    for m in ('numpy', 'scipy', 'sympy', 'mpmath', 'camb'):
        try: out[m] = __import__(m).__version__
        except Exception: pass
    return out
def stamp(results, lock=None, code=(), data=(), t0=None):
    g = lambda *c: subprocess.run(c, capture_output=True, text=True).stdout.strip()
    rec = dict(results=results, results_sha256=_h(results), created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
               git_commit=g('git', 'rev-parse', 'HEAD'), git_dirty=bool(g('git', 'status', '--porcelain', '--', *code)) if code else None,
               lock=lock, lock_sha256=_h(lock) if lock else None, code={c: _h(c) for c in code}, data={d: _h(d) for d in data},
               python=sys.version.split()[0], packages=_pkgs(), machine=f'{socket.gethostname()} {platform.platform()}',
               wall_s=round(time.time() - t0, 1) if t0 else None)
    json.dump(rec, open(results + '.prov.json', 'w'), indent=1); return rec
def check(results):
    P = []
    try: rec = json.load(open(results + '.prov.json'))
    except OSError: return False, ['no provenance stamp']
    if _h(results) != rec['results_sha256']: P.append('results file changed after stamping')
    if rec.get('lock') and _h(rec['lock']) != rec['lock_sha256']: P.append('lock changed after the run')
    for k, v in list(rec['code'].items()) + list(rec['data'].items()):
        if not os.path.exists(k): P.append(f'{k} missing')
        elif _h(k) != v: P.append(f'{k} changed since the run')
    return not P, P
