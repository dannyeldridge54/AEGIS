# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""R4: write tools/TOOLKIT_STATS.md — per toolkit: modules, lines, test files, tests run/passed now, code version.
Run: python3 -m tools.toolkit_stats   (numbers come from running the tests, not from memory)."""
import datetime, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KITS = {'CERN+1': ['tools/lhc'], 'Hyperion': ['tools/janus_astro'], 'Janus': ['tools/janus_calc', 'tools/janus_lt'],
        'Mapper': ['tools/mapper', 'apps/skymap'], 'Shared (CLI, doctor, provenance, guard)': ['tools/tests']}
def count(dirs):
    mods = lines = tests = 0
    for d in dirs:
        for dp, dn, fn in os.walk(os.path.join(ROOT, d)):
            if any(x in dp for x in ('__pycache__', 'vendor', 'node_modules', 'dist')): continue
            for f in fn:
                if f.endswith(('.py', '.js')):
                    p = os.path.join(dp, f); n = sum(1 for _ in open(p, errors='ignore'))
                    if f.startswith('test_'): tests += 1
                    else: mods += 1; lines += n
    return mods, lines, tests
def run_tests(dirs):
    paths = [p for d in dirs for p in [os.path.join(ROOT, d)] if os.path.isdir(p)]
    r = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *paths], cwd=ROOT, capture_output=True, text=True, timeout=900)
    tail = (r.stdout.strip().splitlines() or [''])[-1]
    nums = {k: int(v) for v, k in re.findall(r'(\d+) (passed|failed|error|skipped)', tail)}
    return nums, tail
def main():
    from tools.prov_block import version
    rows = ['| toolkit | modules | lines | test files | passed | failed |', '|---|---|---|---|---|---|']
    for kit, dirs in KITS.items():
        m, l, t = count(dirs); nums, _ = run_tests(dirs)
        rows.append(f"| {kit} | {m} | {l} | {t} | {nums.get('passed', 0)} | {nums.get('failed', 0) + nums.get('error', 0)} |")
    when = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    doc = (f'# AEGIS toolkit stats\nGenerated {when} by `python3 -m tools.toolkit_stats` at code {version()}.\n'
           'Counts are from the files on disk; test numbers are from running pytest now.\n\n' + '\n'.join(rows) + '\n')
    open(os.path.join(ROOT, 'tools', 'TOOLKIT_STATS.md'), 'w').write(doc); print(doc)
if __name__ == '__main__': main()
