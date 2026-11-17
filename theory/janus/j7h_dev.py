"""J7h DEV D1 runner: remaining p1 models one process each with a 20-min wall limit, then p23."""
import sys, json, subprocess, os
PART = 'field_tests/results/janus_j7h_p1.part.jsonl'
done = {json.loads(l)['m'] for l in open(PART) if l.strip()} if os.path.exists(PART) else set()
for m in ('gmlfi', 'ncli', 'rpqti', 'cnbi', 'kmiii', 'hi'):
    if m in done: continue
    code = f"import runpy,sys; sys.argv=['x']; g=runpy.run_path('theory/janus/j7h_fixups.py'); g['F'].P={{'{m}': g['NEW']['{m}']}}; g['G'].F.P=g['F'].P; g['F'].run()"
    try: subprocess.run([sys.executable, '-c', code], timeout=1200)
    except subprocess.TimeoutExpired:
        open(PART, 'a').write(json.dumps(dict(m=m, status='listed', why='per-model wall limit 20 min (DEV D1)')) + '\n'); print(m, 'listed (wall limit)', flush=True)
subprocess.run([sys.executable, 'theory/janus/j7h_fixups.py', 'p23'])
print('J7H DONE', flush=True)
