"""L-6: deviations as a command, and a rerun guard.
  python3 tools/lockbench/deviate.py add LOCK.md "what changed and why"   -> appends D<k> to LOCK_DEVIATIONS.md, rehashes, commits + pushes
  python3 tools/lockbench/deviate.py check LOCK.md RESULTS...             -> exit 1 (REFUSE) if any RESULTS file is committed and no deviation
                                                                             was committed after it (a rerun with nothing written down first)
pcjob.py and job scripts call check() before running."""
import sys, os, re, subprocess, hashlib, time
def sh(*c): return subprocess.run(c, capture_output=True, text=True).stdout.strip()
def devpath(lock): return lock[:-3] + '_DEVIATIONS.md' if lock.endswith('.md') else lock + '_DEVIATIONS.md'
def add(lock, text, commit=True):
    p = devpath(lock); old = open(p).read() if os.path.exists(p) else f'# DEVIATIONS — {os.path.basename(lock)}\n'
    k = 1 + max([int(x) for x in re.findall(r'^D(\d+)\b', old, re.M)] or [0])
    new = old.rstrip('\n') + f"\nD{k} ({time.strftime('%Y-%m-%d %H:%MZ', time.gmtime())}): {text}\n"; open(p, 'w').write(new)
    open(p + '.sha256', 'w').write(f"{hashlib.sha256(new.encode()).hexdigest()}  {p}\n")
    if commit:
        sh('git', 'add', p, p + '.sha256')
        sh('git', 'commit', '-qm', f'{os.path.basename(p)} D{k}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_014Gbstd4JrhrM8iiEauYtjs')
        sh('git', 'push', '-q', 'origin', 'HEAD:unify-bg')
    return f'D{k}'
def _t(path):
    t = sh('git', 'log', '-1', '--format=%ct', '--', path); return int(t) if t else None
def check(lock, results):
    """returns (ok, reason). ok=False when a results file already has a commit and the latest deviation commit is not newer."""
    tr = [x for x in (_t(r) for r in results) if x]
    if not tr: return True, 'first run (no committed results)'
    td = _t(devpath(lock))
    if td and td > max(tr): return True, 'rerun covered by a deviation committed after the last results'
    return False, 'REFUSE: results already committed and no deviation written after them'
if __name__ == '__main__':
    if sys.argv[1] == 'add': print(add(sys.argv[2], sys.argv[3]))
    elif sys.argv[1] == 'check':
        ok, why = check(sys.argv[2], sys.argv[3:]); print(why); sys.exit(0 if ok else 1)
