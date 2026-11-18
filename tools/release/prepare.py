# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""One-command release check for the AEGIS toolkits.
  python -m tools.release.prepare                 -> readiness report for the current version (nothing changed)
  python -m tools.release.prepare 2026.12.01      -> also set the new version and start releases/RELEASE_NOTES_v<ver>.md
Checks: version consistent, toolkit tests, 11-check smoke test, snapshot outputs, GitHub CI (toolkits job), release notes present.
It never tags, publishes or uploads: the last step (GitHub "Draft new release") is Danny's."""
import json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); CLI = os.path.join(ROOT, 'tools', 'aegis_cli.py')
TESTS = ['tools/lhc/tests', 'tools/lattice/tests', 'tools/janus_astro/tests', 'tools/janus_lt/tests', 'tools/serapis_calc/tests', 'tools/chem/tests', 'tools/golden/tests']
def sh(cmd, timeout=900):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout, shell=isinstance(cmd, str)); return r.returncode, (r.stdout + r.stderr).strip()
def version():
    return re.search(r"VERSION = '([^']+)'", open(CLI, encoding='utf-8').read()).group(1)
def set_version(v):
    s = open(CLI, encoding='utf-8').read(); open(CLI, 'w', encoding='utf-8').write(re.sub(r"VERSION = '[^']+'", f"VERSION = '{v}'", s))
    notes = os.path.join(ROOT, 'releases', f'RELEASE_NOTES_v{v}.md')
    if not os.path.exists(notes):
        prev = sorted(p for p in os.listdir(os.path.join(ROOT, 'releases')) if p.startswith('RELEASE_NOTES_v'))
        _, log = sh(['git', 'log', '--since=2 weeks ago', '--pretty=- %s', '--', 'tools', 'requirements-tools.txt'])
        open(notes, 'w', encoding='utf-8').write(f"## AEGIS release {v}: public toolkits\n\n(Draft from the commit log - edit before publishing. Previous: {prev[-1] if prev else 'none'})\n\n" + log[:6000] + "\n")
    return notes
def main(argv):
    if argv: print('notes:', set_version(argv[0]))
    v = version(); R = []
    R.append(('version', True, v))
    rc, out = sh([sys.executable, '-m', 'pytest', '-q'] + TESTS); R.append(('toolkit tests', rc == 0, out.splitlines()[-1] if out else ''))
    rc, out = sh([sys.executable, 'tools/release_smoketest.py']); R.append(('smoke test', rc == 0, out.splitlines()[-1] if out else ''))
    rc, out = sh([sys.executable, '-m', 'tools.golden.golden', 'check']); R.append(('snapshot outputs', rc == 0, out.splitlines()[-1] if out else ''))
    notes = os.path.join(ROOT, 'releases', f'RELEASE_NOTES_v{v}.md'); R.append(('release notes', os.path.exists(notes), os.path.relpath(notes, ROOT)))
    rc, out = sh("gh api 'repos/dannyeldridge54/AEGIS/actions/workflows/tools.yml/runs?per_page=10&branch=unify-bg' "
                 "-q '[.workflow_runs[]|select(.status==\"completed\")][0].id'", 60)
    if rc == 0 and out.strip().isdigit():
        rc2, j = sh(f"gh api repos/dannyeldridge54/AEGIS/actions/runs/{out.strip()}/jobs -q '.jobs[]|select(.name==\"toolkits\")|.conclusion'", 60)
        R.append(('GitHub CI (toolkits job)', j.strip() == 'success', j.strip() or 'not found'))
    else: R.append(('GitHub CI (toolkits job)', None, 'gh not available - check the Actions tab'))
    rc, dirty = sh(['git', 'status', '--porcelain', '--', 'tools']); R.append(('tools/ committed', not dirty.strip(), 'clean' if not dirty.strip() else dirty[:200]))
    for name, ok, info in R: print(f"{'PASS' if ok else ('----' if ok is None else 'FAIL')}  {name}: {info}")
    ready = all(ok is not False for _, ok, _ in R)
    print(f"\nRelease v{v}: {'READY' if ready else 'NOT READY'}." + (f" Next (Danny): GitHub -> Releases -> Draft new release, tag v{v}, paste {os.path.relpath(notes, ROOT)}; the Windows/macOS/Linux programs build and attach themselves." if ready else ''))
    return 0 if ready else 1
if __name__ == '__main__': sys.exit(main(sys.argv[1:]))
