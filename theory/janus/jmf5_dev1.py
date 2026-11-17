"""JMF5 DEVIATIONS D1: N1 only, phi_init stepped by +0.5 until the patched MMC completes; then score as locked."""
import sys, runpy, numpy as np, time; sys.path.insert(0, '.'); t0 = time.time()
src = open('theory/janus/jmf5_mmcfix.py').read().split('L = []; ok = True; partial = False')[0]
g = {}; exec(compile(src, 'jmf5', 'exec'), g)
ch, rows, _, V, gr, he = g['M']['N1 quad+quartic intxn']
for st in range(1, 41):
    f0 = [12.0 + 0.5*st, 12.0 + 0.5*st]
    try: ns_m, r_m = g['mmc'](ch, rows, f0); print('DEV D1: N1 phi_init', f0, flush=True); break
    except Exception as ex: continue
else: print('N1: LISTED (no phi_init up to 32 worked)'); sys.exit()
s = g['spectra_mf'](V, gr, he, f0); c1 = abs(s['ns'] - ns_m) <= 2e-4; c2 = abs(s['r']/r_m - 1) <= 2e-3
line = f"N1 (DEV D1, phi_init {f0}): Janus-MF ns {s['ns']:.6f} r {s['r']:.5f} | MMC-fixed ns {ns_m:.6f} r {r_m:.5f} | C1 |d| {abs(s['ns']-ns_m):.1e} {'PASS' if c1 else 'FAIL'}; C2 rel {abs(s['r']/r_m-1):.1e} {'PASS' if c2 else 'FAIL'}"
print(line); open('field_tests/results/janus_jmf5.txt', 'a').write(line + '\n')
