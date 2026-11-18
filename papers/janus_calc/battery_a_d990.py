# AEGIS-FP FHQJSSMQRBKJEKOM · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""D990 (locked PREREG_D990): Janus vs base spectra_fast, n_s and r, 32 points. Usage: python3 ... <worker 0|1> | summary"""
import sys, os, time, math, json, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
OUT = 'field_tests/results/janus_battery_a_d990.txt'; PART = 'field_tests/results/janus_battery_a_d990.part{}.jsonl'
from tools.janus_calc import models as J
from tools.janus_calc.core import Model
from tools.serapis_calc.ms import Background, spectra_fast
s23 = math.sqrt(2/3)
book = {'m2phi2': (lambda p: p*p, lambda p: 2*p, 20.0), 'phi4': (lambda p: p**4, lambda p: 4*p**3, 30.0),
        'starobinsky': (lambda p: (1-math.exp(-s23*p))**2, lambda p: 2*(1-math.exp(-s23*p))*s23*math.exp(-s23*p), 6.5),
        'natural_f5': (lambda p: 1+math.cos(p/5), lambda p: -math.sin(p/5)/5, 0.05)}
pts = [('SERAPIS-E', ('E', C), N) for C in (1.0e-6, 1.15e-6, 1.3e-6) for N in (44, 47, 50, 53)] + \
      [('Chronos', ('chr', e), N) for e in (1.3e-4, 1.45e-4) for N in (44, 47, 50)] + \
      [('SERAPIS-rho', ('rho', 6e-5), N) for N in (44, 46.09, 49.49, 52)] + [('Kairos', ('chr', 0.0), N) for N in (46, 50)] + \
      [('stress', ('book', k), N) for k in book for N in (50, 60)]
_cache = {}
def model(spec):
    if spec in _cache: return _cache[spec]
    kind, par = spec
    m = J.serapis_E(par) if kind == 'E' else J.chronos(par) if kind == 'chr' else J.serapis_rho(par) if kind == 'rho' else Model(*book[par])
    _cache[spec] = m; return m
def worker(w):
    path = PART.format(w); done = set()
    if os.path.exists(path): done = {json.loads(l)['i'] for l in open(path) if l.strip()}
    for i, (fam, spec, N) in enumerate(pts):
        if i % 2 != w or i in done: continue
        m = model(spec); bg = Background(m.V, m.dV, m.sol.y[0][0])
        t = time.time(); j = m.spectra(N); tj = time.time() - t
        t = time.time(); b = spectra_fast(bg, N); tb = time.time() - t
        rec = dict(i=i, fam=fam, spec=str(spec[1]), N=N, ns_j=float(j['ns']), r_j=float(j['r']), ns_b=float(b['ns']), r_b=float(b['r']), tj=tj, tb=tb, e1=float(j['eps'][0]), e2=float(j['eps'][1]))
        open(path, 'a').write(json.dumps(rec) + '\n'); print(rec, flush=True)
def summary():
    recs = []
    for w in (0, 1):
        if os.path.exists(PART.format(w)): recs += [json.loads(l) for l in open(PART.format(w)) if l.strip()]
    recs.sort(key=lambda r: r['i']); L = []; fam_pass = 0; fam_n = 0
    for r in recs:
        dn = r['ns_j'] - r['ns_b']; dr = r['r_j']/r['r_b'] - 1
        if r['fam'] != 'stress':
            ok = abs(dn) <= 1e-4 and abs(dr) <= 0.005; fam_pass += ok; fam_n += 1; tag = 'PASS' if ok else 'FAIL'
        else:
            tag = 'within envelope' if abs(dn) <= 5e-4 and abs(dr) <= 0.02 else 'outside envelope'
        L.append(f"{r['fam']} {r['spec']} N*={r['N']}: ns janus {r['ns_j']:.6f} ref {r['ns_b']:.6f} (d {dn:+.1e}) | r janus {r['r_j']:.5e} ref {r['r_b']:.5e} (d {dr:+.3%}) | eps1 {r['e1']:.1e} eps2 {r['e2']:.3f} | {r['tj']*1e3:.1f} ms vs {r['tb']:.0f} s -> {tag}")
    fam = [r for r in recs if r['fam'] != 'stress']
    if len(recs) < len(pts): L.append(f'INCOMPLETE: {len(recs)}/{len(pts)} points')
    else:
        dns = [abs(r['ns_j']-r['ns_b']) for r in fam]; drs = [abs(r['r_j']/r['r_b']-1) for r in fam]
        v = 'VALIDATED' if fam_pass == fam_n else ('PARTIAL' if fam_pass >= 20 else 'NOT VALIDATED')
        L.append(f"SERAPIS family: {fam_pass}/{fam_n} pass; max |dns| {max(dns):.1e}, median {np.median(dns):.1e}; max |dr/r| {max(drs):.3%}, median {np.median(drs):.3%}; speed-up median {np.median([r['tb']/r['tj'] for r in recs]):.0f}x -> {v}")
    open(OUT, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[-3:]))
if __name__ == '__main__':
    worker(int(sys.argv[1])) if sys.argv[1] in ('0', '1') else summary()
