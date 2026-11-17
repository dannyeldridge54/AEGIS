import sys, os, subprocess, tempfile; sys.path.insert(0, os.getcwd()); import tools.lockbench.deviate as D
d = tempfile.mkdtemp(); os.chdir(d); run = lambda *c: subprocess.run(c, capture_output=True, text=True)
run('git', 'init', '-q'); run('git', 'config', 'user.email', 't@t'); run('git', 'config', 'user.name', 't')
open('L.md', 'w').write('# lock\n'); run('git', 'add', '.'); run('git', 'commit', '-qm', 'lock', '--date', '2026-01-01T00:00:00')
assert D.check('L.md', ['r.txt'])[0]
open('r.txt', 'w').write('1\n'); run('git', 'add', '.'); env = dict(os.environ, GIT_COMMITTER_DATE='2026-01-02T00:00:00')
subprocess.run(['git', 'commit', '-qm', 'res'], env=env)
assert not D.check('L.md', ['r.txt'])[0]
assert D.add('L.md', 'fix parser', commit=False) == 'D1'
subprocess.run(['git', 'add', '.']); subprocess.run(['git', 'commit', '-qm', 'dev'], env=dict(os.environ, GIT_COMMITTER_DATE='2026-01-03T00:00:00'))
assert D.check('L.md', ['r.txt'])[0] and D.add('L.md', 'second', commit=False) == 'D2'
assert 'D2' in open('L_DEVIATIONS.md').read() and os.path.exists('L_DEVIATIONS.md.sha256')
print('test_deviate: PASS (first run allowed, rerun refused, deviation numbering, rerun allowed after deviation)')
