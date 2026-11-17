"""J11 (locked PREREG_J11_beta_scaling)."""
import sys, os, json, math, numpy as np, multiprocessing as mp, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
PART = 'field_tests/results/janus_j11.part.jsonl'
def job(a):
    p, N = a
    from tools.serapis_calc.ms import Background, spectra_fast
    from tools.janus_calc.core import Model, spectra3
    V = lambda y: y**p; dV = lambda y: p*y**(p-1)
    try:
        y0 = math.sqrt(2*p*(N + 40)); m = Model(V, dV, y0, Nmax=3000); bg = Background(V, dV, y0, Nmax=3000)
        def beta(lo, n):
            s = spectra_fast(bg, N, dlnk=tuple(np.linspace(-lo, lo, n)), bd=1000.0, return_lp=True); return 6*np.polyfit(s['dlnk'], s['lnPR'], 7)[-4]
        j = spectra3(m, N)
        return dict(p=p, N=N, bA=float(beta(1.5, 41)), bB=float(beta(1.0, 31)), bJ=float(j['beta_s']), eps=float(j['eps'][0]), Ntot=float(m.Nend))
    except Exception as e: return dict(p=p, N=N, err=str(e))
def summary():
    R = [json.loads(l) for l in open(PART) if l.strip()]; L = []; xs = []; ys = []
    for r in sorted(R, key=lambda r: (r['p'], r['N'])):
        if 'err' in r: L.append(f"p={r['p']} N*={r['N']}: ERROR {r['err'][:80]}"); continue
        sp = abs(r['bA']-r['bB'])/abs(r['bA']); e = abs(r['bJ']/r['bA']-1); use = sp <= 0.05 and e > 0.01
        if use: xs.append(math.log(r['eps'])); ys.append(math.log(e))
        L.append(f"p={r['p']} N*={r['N']:.0f}: eps* {r['eps']:.4e} beta_A {r['bA']:.4e} spread {sp:.3f} | Janus {r['bJ']:.4e} rel err {e:.4f} {'USED' if use else ''}")
    if len(xs) < 5: L.append(f"usable {len(xs)} < 5 -> UNINFORMATIVE")
    else:
        sl = float(np.polyfit(xs, ys, 1)[0]); L.append(f"usable {len(xs)}; log-log slope {sl:.3f} -> " + ('TRUNCATION SCALING CONFIRMED' if abs(sl-1) <= 0.35 else 'NOT CONFIRMED'))
    open('field_tests/results/janus_j11_beta_scaling.txt', 'w').write('\n'.join(L)+'\n'); print(L[-1])
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'summary': summary(); sys.exit()
    n = int(sys.argv[1]) if len(sys.argv) > 1 else max(1, (os.cpu_count() or 2))
    done = {(json.loads(l)['p'], json.loads(l)['N']) for l in open(PART)} if os.path.exists(PART) else set()
    jobs = [(p, N) for p in (1, 2, 3, 4, 5, 6) for N in (50.0, 60.0) if (p, N) not in done]
    with mp.Pool(n) as P:
        for r in P.imap_unordered(job, jobs): open(PART, 'a').write(json.dumps(r)+'\n'); print(r.get('p'), r.get('N'), 'err' in r, flush=True)
    summary()
