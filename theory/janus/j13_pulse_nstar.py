"""J13 (locked PREREG_J13_pulse_nstar). Usage: python3 theory/janus/j13_pulse_nstar.py [ncpu] | summary."""
import sys, os, json, numpy as np, importlib.util, multiprocessing as mp, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
PART = 'field_tests/results/janus_j13.part.jsonl'
def G():
    s = importlib.util.spec_from_file_location('j7g', 'theory/janus/j7g_pulse_reheat.py'); g = importlib.util.module_from_spec(s); s.loader.exec_module(g); return g
def job(m):
    from tools.janus_calc.core import spectra3
    from tools.serapis_calc.ms import Background, spectra_fast
    out = []
    try:
        Vf, dVf, p0, mm = G().build(m); bg = Background(Vf, dVf, p0, Nmax=4000)
        for N in (45.0, 55.0, 65.0):
            j = spectra3(mm, N); b = spectra_fast(bg, N, dlnk=tuple(np.linspace(-1, 1, 9)), bd=1000.0)
            out.append(dict(m=m, N=N, dns=abs(float(j['ns'])-float(b['ns'])), drr=abs(float(j['r'])/float(b['r'])-1), das=abs(float(j['alpha_s'])-float(b['alpha_s'])), ns=float(b['ns'])))
    except Exception as e: out.append(dict(m=m, err=str(e)[:200]))
    return out
def summary():
    R = [json.loads(l) for l in open(PART) if l.strip()]; G_ = [r for r in R if 'err' not in r]; L = []
    for r in sorted(G_, key=lambda r: (r['m'], r['N'])): L.append(f"{r['m']:8s} N*={r['N']:.0f}: ns {r['ns']:.6f} | dns {r['dns']:.1e} dr/r {r['drr']:.1e} das {r['das']:.1e}")
    for r in R:
        if 'err' in r: L.append(f"{r['m']}: ERROR {r['err'][:80]}")
    dn = [r['dns'] for r in G_]; dnx = [r['dns'] for r in G_ if r['m'] != 'di']; dr = [r['drr'] for r in G_]; da = [r['das'] for r in G_]
    C1 = bool(np.median(dn) <= 1e-5 and max(dnx) <= 2e-4); C2 = bool(np.median(dr) <= 1e-3); C3 = bool(np.median(da) <= 1e-5)
    L.append(f"{len(G_)} points; medians dns {np.median(dn):.1e} (max excl. di {max(dnx):.1e}; di max {max([r['dns'] for r in G_ if r['m']=='di'] or [0]):.1e}) dr/r {np.median(dr):.1e} das {np.median(da):.1e}; C1 {C1} C2 {C2} C3 {C3} -> " + ('HOLDS' if C1 and C2 and C3 else 'NOT ALL HOLD'))
    open('field_tests/results/janus_j13_pulse_nstar.txt', 'w').write('\n'.join(L)+'\n'); print(L[-1])
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'summary': summary(); sys.exit()
    n = int(sys.argv[1]) if len(sys.argv) > 1 else max(1, (os.cpu_count() or 2))
    ms = [json.loads(l)['m'] for l in open('field_tests/results/janus_j7f.part.jsonl') if l.strip() and json.loads(l)['status'] == 'scored']
    done = {json.loads(l)['m'] for l in open(PART)} if os.path.exists(PART) else set()
    with mp.Pool(n) as P:
        for out in P.imap_unordered(job, [m for m in ms if m not in done]):
            for r in out: open(PART, 'a').write(json.dumps(r)+'\n')
            print(out[0].get('m'), len(out), flush=True)
    summary()
