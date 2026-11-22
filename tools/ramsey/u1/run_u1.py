#!/usr/bin/env python3
"""R(3,10) stage U1 on Danny's PC: build every (3,9,34)-graph that has a degree-6 vertex, from the 477,142 extremal (3,8,27)-graphs.
Splits the list into one chunk per CPU core (leaves one core free), runs u1final.exe on each chunk in parallel, and writes
u1_solutions.txt (lines 'SOL D=<index> <6 attachment sets in hex>') plus u1_progress.log. Resumable: finished chunks are skipped.
Usage: python run_u1.py [path to r38_27.g6.gz]"""
import os, sys, gzip, subprocess, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); EXE = os.path.join(HERE, 'u1final.exe' if os.name == 'nt' else 'u1final')
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser('~'), 'Downloads', 'r38_27.g6.gz')
WORK = os.path.join(HERE, 'u1_work'); os.makedirs(WORK, exist_ok=True)
lines = gzip.open(SRC, 'rt').read().split('\n'); lines = [l for l in lines if l]
assert len(lines) == 477142, 'expected 477,142 graphs, got %d' % len(lines)
cores = max(1, (os.cpu_count() or 2) - 1); CH = 2000
chunks = [(i, lines[i:i + CH]) for i in range(0, len(lines), CH)]
def run(ch):
    start, part = ch; done = os.path.join(WORK, 'c%06d.done' % start)
    if os.path.exists(done): return start, open(done).read()
    inp = os.path.join(WORK, 'c%06d.g6' % start); open(inp, 'w').write('\n'.join(part) + '\n')
    env = dict(os.environ, OFFSET=str(start)); t = time.time()
    r = subprocess.run([EXE, '8'], stdin=open(inp), capture_output=True, text=True, env=env)
    sols = [l for l in r.stdout.splitlines() if l.startswith('SOL')]
    with open(os.path.join(WORK, 'c%06d.sol' % start), 'w') as f: f.write('\n'.join(sols) + ('\n' if sols else ''))
    msg = 'chunk %d: %d graphs, %d solutions, %.0fs | %s' % (start, len(part), len(sols), time.time() - t, r.stderr.strip().splitlines()[-1] if r.stderr.strip() else '')
    open(done, 'w').write(msg); os.remove(inp); return start, msg
print('U1: %d graphs, %d chunks, %d parallel workers' % (len(lines), len(chunks), cores), flush=True)
with ThreadPoolExecutor(cores) as ex, open(os.path.join(HERE, 'u1_progress.log'), 'a') as log:
    for start, msg in ex.map(run, chunks):
        print(msg, flush=True); log.write(msg + '\n'); log.flush()
with open(os.path.join(HERE, 'u1_solutions.txt'), 'w') as out:
    for start, _ in chunks:
        p = os.path.join(WORK, 'c%06d.sol' % start)
        if os.path.exists(p): out.write(open(p).read())
n = sum(1 for _ in open(os.path.join(HERE, 'u1_solutions.txt')))
print('U1 DONE: %d attachment 6-tuples (each one a (3,9,34)-graph with a degree-6 vertex) -> u1_solutions.txt' % n, flush=True)
