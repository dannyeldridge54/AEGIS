"""olq: run a command only when no EARLIER Ollama job is running (PC v2 runner). Usage: python olq.py <JOBNAME> <command...>
An Ollama job = a file in queue/running whose name starts with one of OLLAMA_JOBS or whose text contains 'olq.py'.
A job waits only for Ollama jobs that STARTED BEFORE IT (older queue/running/<id>.job mtime, name as tie-break): this gives a
strict total order, so two jobs starting together can never wait on each other (the old symmetric 'wait for any other' deadlocked).
Waits (polling 30 s) until no earlier such job remains, then runs the command. Max wait 12 h, then runs anyway."""
import os, sys, time, subprocess
Q = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'queue', 'running')
OLLAMA_JOBS = ('M0', 'M1', 'M2', 'M3', 'P7', 'C2', 'FORGE', 'RETRY', 'GRADE')
me = sys.argv[1]; cmd = ' '.join(sys.argv[2:])
def _mtime(p):
    try: return os.path.getmtime(p)
    except OSError: return 0.0
def earlier():
    """Ollama jobs that started strictly before me (older .job mtime; equal mtime broken by name). No cycles -> no deadlock."""
    my_t = _mtime(os.path.join(Q, me + '.job')) or time.time()
    out = []
    for f in (os.listdir(Q) if os.path.isdir(Q) else []):
        n = f.rsplit('.', 1)[0]
        if n == me: continue
        full = os.path.join(Q, f)
        try: txt = open(full, encoding='utf-8', errors='ignore').read()
        except OSError: txt = ''
        if not (n.upper().startswith(OLLAMA_JOBS) or 'olq.py' in txt): continue
        t = _mtime(full)
        if t < my_t or (t == my_t and n < me): out.append(n)
    return out
t0 = time.time()
while True:
    o = earlier()
    if not o or time.time() - t0 > 12*3600: break
    print(f'olq: {me} waiting for earlier {o}', flush=True); time.sleep(30)
print(f'olq: {me} starting after {time.time()-t0:.0f} s', flush=True)
sys.exit(subprocess.run(cmd, shell=True).returncode)
