"""J9b (locked PREREG_J9b_beta_s_sharp). Usage: python3 theory/janus/j9b_beta_sharp.py [ncpu]. Resumable part file."""
import sys, os, json, math, numpy as np, importlib.util, multiprocessing as mp, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
PART = 'field_tests/results/janus_j9b.part.jsonl'
def job(args):
    i, N = args
    sp_ = importlib.util.spec_from_file_location('j7b', 'theory/janus/j7b_wide.py'); B = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(B)
    from tools.serapis_calc.ms import Background, spectra_fast
    from tools.janus_calc.core import spectra3
    name, V, dV, y0, m = B.build(i); bg = Background(V, dV, y0, Nmax=3000)
    def beta(lo, n):
        s = spectra_fast(bg, N, dlnk=tuple(np.linspace(-lo, lo, n)), bd=1000.0, return_lp=True); return 6*np.polyfit(s['dlnk'], s['lnPR'], 7)[-4]
    try:
        bA, bB = beta(1.5, 41), beta(1.0, 31); bJ = float(spectra3(m, N)['beta_s'])
        return dict(i=i, N=N, name=name, bA=float(bA), bB=float(bB), bJ=bJ)
    except Exception as e: return dict(i=i, N=N, name=name, err=str(e))
def summary():
    R = [json.loads(l) for l in open(PART) if l.strip()]; L = []; inf = []
    for r in sorted(R, key=lambda r: (r['i'], r['N'])):
        if 'err' in r: L.append(f"{r['name']:12s} N*={r['N']:.0f}: ERROR {r['err'][:80]}"); continue
        sp = abs(r['bA']-r['bB'])/abs(r['bA']); e = abs(r['bJ']/r['bA']-1); I = sp <= 0.05
        if I: inf.append((e, sp))
        L.append(f"{r['name']:12s} N*={r['N']:.0f}: beta_A {r['bA']:.4e} B {r['bB']:.4e} spread {sp:.3f} {'INF' if I else 'not'} | Janus {r['bJ']:.4e} err {e:.3f}")
    C1 = len(inf) >= 20
    if inf:
        me = float(np.median([x[0] for x in inf])); mx = max(x[0] for x in inf); ms = float(np.median([x[1] for x in inf])); C2 = me <= 0.05 and mx <= 0.15
    else: me = mx = ms = float('nan'); C2 = False
    L.append(f"informative {len(inf)}/{len(R)}; median Janus err {me:.3f}, max {mx:.3f}; median reference spread {ms:.3f} -> " + ('UNINFORMATIVE' if not C1 else ('Janus beta_s VALIDATED' if C2 else 'NOT VALIDATED')))
    open('field_tests/results/janus_j9b_beta_s.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L[-3:]))
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'summary': summary(); sys.exit()
    n = int(sys.argv[1]) if len(sys.argv) > 1 else max(1, (os.cpu_count() or 2))
    done = {(json.loads(l)['i'], json.loads(l)['N']) for l in open(PART)} if os.path.exists(PART) else set()
    jobs = [(i, N) for i in range(1, 18) if i != 9 for N in (50.0, 60.0) if (i, N) not in done]
    with mp.Pool(n) as P:
        for r in P.imap_unordered(job, jobs):
            open(PART, 'a').write(json.dumps(r)+'\n'); print(r.get('name'), r.get('N'), 'err' in r, flush=True)
    summary()
