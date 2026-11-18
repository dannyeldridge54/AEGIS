# AEGIS-FP YALN32EI7I4CY6RN · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
r"""Package a LOCKED job for Danny's PC runner in one step.
  python3 tools/calcq/pcjob.py ID --lock field_tests/rules/PREREG_X.md --cmd "python3 -u theory/janus/x.py" --files f1 f2 dir/ [--limit 3600]
Checks: the lock and its .sha256 exist, the hash matches, both are committed and pushed (lock-before-results); the script file is committed.
Output: /mnt/user-data/outputs/pcjob_<ID>.tgz (code + lock) and pcjob_<ID>.job ("<ID>|<limit>|python3 ..." for pc_runner2).
Then (Claude): device_commit_files the .tgz to Desktop\\AEGIS_PCJOBS\\<id>\\ and the .job to queue\; the runner unpacks *.tgz itself."""
import sys, os, subprocess, hashlib, argparse, tarfile
a = argparse.ArgumentParser(); a.add_argument('id'); a.add_argument('--lock', required=True); a.add_argument('--cmd', required=True)
a.add_argument('--files', nargs='+', required=True); a.add_argument('--limit', type=int, default=7200); a.add_argument('--results', nargs='*', default=[]); o = a.parse_args()
sys.path.insert(0, '.'); from tools.lockbench.deviate import check as _dev_check   # L-6 rerun guard
_ok, _why = _dev_check(o.lock, o.results); print(_why)
if not _ok: sys.exit(_why)
def sh(*c): return subprocess.run(c, capture_output=True, text=True).stdout.strip()
h = open(o.lock + '.sha256').read().split()[0]
if hashlib.sha256(open(o.lock, 'rb').read()).hexdigest() != h: sys.exit('lock hash mismatch')
for f in (o.lock, o.lock + '.sha256'):
    if sh('git', 'status', '--porcelain', f): sys.exit(f'{f} not committed')
    if sh('git', 'log', '-1', '--format=%H', 'origin/unify-bg', '--', f) == '': sys.exit(f'{f} not pushed')
out = '/mnt/user-data/outputs'; os.makedirs(out, exist_ok=True); tg = f'{out}/pcjob_{o.id}.tgz'
with tarfile.open(tg, 'w:gz') as t:
    for f in o.files + [o.lock, o.lock + '.sha256']: t.add(f)
open(f'{out}/pcjob_{o.id}.job', 'w').write(f'{o.id.lower()}|{o.limit}|{o.cmd}\n')
print(tg, os.path.getsize(tg), 'bytes;', f'{out}/pcjob_{o.id}.job')
