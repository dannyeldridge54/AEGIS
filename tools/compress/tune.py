#!/usr/bin/env python3
"""Instrument tuning: poke each node's gain up and down on a tuning slice, keep what helps (coordinate descent). Prints every poke live."""
import subprocess, os, sys, re
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loomz10'); data, maps = sys.argv[1], sys.argv[2]
NAMES = ['o0', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'mlit', 'word', 'wpair', 'class', 'column', 'ltype', 'markup', 'match']
def size(g):
    env = dict(os.environ, EV='1', CLASSMAP=maps, GAINS=','.join('%g' % x for x in g))
    r = subprocess.run([B, 'c', data, data + '.tune.lz'], env=env, capture_output=True, text=True); return int(re.search(r'out (\d+)', r.stderr).group(1))
g = [1.0] * 15; best = size(g); print('START', best, flush=True)
for sweep in range(int(sys.argv[3]) if len(sys.argv) > 3 else 1):
    for i in range(15):
        for f in (2.0, 0.5):
            t = list(g); t[i] *= f; s = size(t); d = 100 * (s - best) / best
            print('poke %-6s x%-4g -> %d (%+.3f%%)%s' % (NAMES[i], f, s, d, '  KEEP' if s < best else ''), flush=True)
            if s < best: g, best = t, s; break
    print('SWEEP', sweep + 1, 'best', best, 'gains', ','.join('%g' % x for x in g), flush=True)
