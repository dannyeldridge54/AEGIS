"""J10 (locked PREREG_J10_nstar_sweep). Usage: python3 theory/janus/j10_nstar.py [ncpu] | summary. Resumable."""
import sys, os, json, numpy as np, importlib.util, multiprocessing as mp, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
PART = 'field_tests/results/janus_j10.part.jsonl'
def job(a):
    i, N = a
    s = importlib.util.spec_from_file_location('j7b', 'theory/janus/j7b_wide.py'); B = importlib.util.module_from_spec(s); s.loader.exec_module(B)
    from tools.serapis_calc.ms import Background, spectra_fast
    from tools.janus_calc.core import spectra3
    try:
        name, V, dV, y0, m = B.build(i); bg = Background(V, dV, y0, Nmax=3000)
        j = spectra3(m, N); b = spectra_fast(bg, N, dlnk=B.DL, bd=1000.0)
        return dict(i=i, N=N, name=name, dns=abs(float(j['ns'])-float(b['ns'])), drr=abs(float(j['r'])/float(b['r'])-1), das=abs(float(j['alpha_s'])-float(b['alpha_s'])), ns=float(b['ns']), r=float(b['r']))
    except Exception as e: return dict(i=i, N=N, err=str(e))
def summary():
    R = [json.loads(l) for l in open(PART) if l.strip()]; G = [r for r in R if 'err' not in r]; L = []
    for r in sorted(G, key=lambda r: (r['i'], r['N'])): L.append(f"{r['name']:12s} N*={r['N']:.0f}: ns {r['ns']:.6f} r {r['r']:.3e} | dns {r['dns']:.1e} dr/r {r['drr']:.1e} das {r['das']:.1e}")
    for r in R:
        if 'err' in r: L.append(f"i={r['i']} N*={r['N']}: ERROR {r['err'][:80]}")
    dn = [r['dns'] for r in G]; dr = [r['drr'] for r in G]; da = [r['das'] for r in G]
    C1 = bool(np.median(dn) <= 1e-5 and max(dn) <= 1e-4); C2 = bool(np.median(dr) <= 1e-3); C3 = bool(np.median(da) <= 1e-5)
    L.append(f"{len(G)} points; medians dns {np.median(dn):.1e} (max {max(dn):.1e}) dr/r {np.median(dr):.1e} das {np.median(da):.1e}; C1 {C1} C2 {C2} C3 {C3} -> " + ('JANUS ACCURACY HOLDS AT NEW PIVOTS' if C1 and C2 and C3 else 'NOT ALL HOLD'))
    open('field_tests/results/janus_j10_nstar.txt', 'w').write('\n'.join(L)+'\n'); print(L[-1])
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'summary': summary(); sys.exit()
    n = int(sys.argv[1]) if len(sys.argv) > 1 else max(1, (os.cpu_count() or 2))
    done = {(json.loads(l)['i'], json.loads(l)['N']) for l in open(PART)} if os.path.exists(PART) else set()
    jobs = [(i, N) for i in range(1, 18) if i != 9 for N in (45.0, 55.0, 65.0) if (i, N) not in done]
    with mp.Pool(n) as P:
        for r in P.imap_unordered(job, jobs): open(PART, 'a').write(json.dumps(r)+'\n'); print(r.get('name'), r.get('N'), 'err' in r, flush=True)
    summary()
