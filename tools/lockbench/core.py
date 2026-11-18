# AEGIS-FP KA2OLC7DKFUVXGSG · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
import hashlib, subprocess
def lock_ok(path, branch='origin/unify-bg'):
    """True only if the lock file's sha256 matches its .sha256, and both are committed and present on the remote branch."""
    sh = lambda *c: subprocess.run(c, capture_output=True, text=True).stdout.strip()
    try: h = open(path + '.sha256').read().split()[0]
    except OSError: return False, 'no .sha256'
    if hashlib.sha256(open(path, 'rb').read()).hexdigest() != h: return False, 'hash mismatch'
    for f in (path, path + '.sha256'):
        if sh('git', 'status', '--porcelain', f): return False, f'{f} uncommitted'
        if not sh('git', 'log', '-1', '--format=%H', branch, '--', f): return False, f'{f} not pushed'
    return True, 'ok'
