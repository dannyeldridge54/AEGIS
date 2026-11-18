# AEGIS-FP CA7NXIV3Y3MVEFKA · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Resumable parallel sweep with a per-task wall limit (the default for every new AEGIS/Janus batch job).
Usage in a job script:
    from tools.calcq.sweep import sweep
    sweep(tasks, fn, part='field_tests/results/X.part.jsonl', key=lambda t: t, limit=1200, ncpu=None)
- tasks: list of picklable task args; fn(task) -> dict (JSON-able). Runs each task in its own process.
- A task already in the part file (by key) is skipped (resume). A task over `limit` seconds is killed and recorded
  {'key':..., 'status':'timeout'}; an exception is recorded {'status':'error','err':...}. Never retried automatically.
"""
import json, os, time, multiprocessing as mp
def _child(fn, task, q):
    try: q.put(('ok', fn(task)))
    except Exception as e: q.put(('error', f'{type(e).__name__}: {e}'[:300]))
def sweep(tasks, fn, part, key=lambda t: t, limit=1200, ncpu=None, log=print):
    ncpu = ncpu or max(1, (os.cpu_count() or 2) - 1)
    done = set()
    if os.path.exists(part):
        for l in open(part):
            if l.strip(): done.add(json.dumps(json.loads(l)['key']))
    todo = [t for t in tasks if json.dumps(key(t)) not in done]
    running = []  # (proc, queue, task, start)
    def write(rec): open(part, 'a').write(json.dumps(rec) + '\n')
    while todo or running:
        while todo and len(running) < ncpu:
            t = todo.pop(0); q = mp.Queue(); p = mp.Process(target=_child, args=(fn, t, q)); p.start(); running.append((p, q, t, time.time()))
        time.sleep(0.5)
        for item in running[:]:
            p, q, t, t0 = item
            if not q.empty():
                st, val = q.get(); p.join(5)
                rec = dict(key=key(t), status='ok', result=val) if st == 'ok' else dict(key=key(t), status='error', err=val)
                write(rec); log(f"[{key(t)}] {rec['status']} ({time.time()-t0:.0f} s)"); running.remove(item)
            elif time.time() - t0 > limit:
                p.kill(); p.join(5); write(dict(key=key(t), status='timeout', limit=limit)); log(f"[{key(t)}] TIMEOUT after {limit} s"); running.remove(item)
            elif not p.is_alive() and q.empty():
                write(dict(key=key(t), status='error', err=f'process died (exit {p.exitcode})')); running.remove(item)
    return [json.loads(l) for l in open(part) if l.strip()] if os.path.exists(part) else []
