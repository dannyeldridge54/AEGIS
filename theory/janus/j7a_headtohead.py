"""J7a (locked PREREG_J7a_aspic_headtohead): Janus fast vs ASPIC (real library, driver theory/janus/aspic/j7a_aspic.f90)
vs exact Mukhanov-Sasaki. Resumable: field_tests/results/janus_j7a.part.jsonl. Usage: python3 ... run | summary"""
import sys, os, json, time, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_calc.core import Model
from tools.serapis_calc.ms import Background, spectra_fast
PART = 'field_tests/results/janus_j7a.part.jsonl'; ASP = 'theory/janus/aspic/aspic_out.txt'
s23 = math.sqrt(2/3)
def model(i):   # field y with inflation rolling toward smaller y; x0 well beyond ASPIC's x*(60)
    if i in (1, 2, 3):
        p = {1: 2.0, 2: 4.0, 3: 2/3}[i]; return 'LFI p=%.4g' % p, (lambda y: y**p), (lambda y: p*y**(p-1)), 22.0 if p < 3 else 30.0
    if i == 4: return 'SI', (lambda y: (1-math.exp(-s23*y))**2), (lambda y: 2*(1-math.exp(-s23*y))*s23*math.exp(-s23*y)), 8.0
    if i in (5, 6):
        f = {5: 5.0, 6: 10.0}[i]; top = math.pi*f; x60 = {5: 3.028, 6: 16.63}[i]
        return 'NI f=%g' % f, (lambda y: 1-math.cos(y/f)), (lambda y: math.sin(y/f)/f), top - 0.5*x60
    if i == 7: return 'ESI q=1', (lambda y: 1-math.exp(-y)), (lambda y: math.exp(-y)), 7.0
def run():
    done = set()
    if os.path.exists(PART): done = {(json.loads(l)['i'], json.loads(l)['N']) for l in open(PART) if l.strip()}
    for i in range(1, 8):
        name, V, dV, y0 = model(i); m = Model(V, dV, y0, Nmax=2000); bg = Background(V, dV, y0, Nmax=2000)
        for N in (50.0, 60.0):
            if (i, N) in done: continue
            from tools.janus_calc.core import spectra3
            t = time.time(); j = spectra3(m, N); tj = time.time() - t
            t = time.time(); b = spectra_fast(bg, N); tb = time.time() - t
            rec = dict(i=i, name=name, N=N, Ntot=m.Nend, ns_j=float(j['ns']), r_j=float(j['r']), a_j=float(j['alpha_s']),
                       ns_b=float(b['ns']), r_b=float(b['r']), a_b=float(b['alpha_s']), tj=tj, tb=tb)
            open(PART, 'a').write(json.dumps(rec)+'\n'); print(rec, flush=True)
def summary():
    R = {(r['i'], r['N']): r for r in (json.loads(l) for l in open(PART) if l.strip())}
    A = {}
    for l in open(ASP):
        c = l.split(); A[(int(c[0]), float(c[2]))] = dict(ns=float(c[4]), r=float(c[5]), a=float(c[6]), t=float(c[8]))
    L = []; dj = []; da = []; rj = []; ra = []; aj = []; aa = []; tj = []
    for k in sorted(R):
        r, a = R[k], A[k]
        x = (abs(r['ns_j']-r['ns_b']), abs(a['ns']-r['ns_b']), abs(r['r_j']/r['r_b']-1), abs(a['r']/r['r_b']-1),
             abs(r['a_j']-r['a_b']), abs(a['a']-r['a_b']))
        dj.append(x[0]); da.append(x[1]); rj.append(x[2]); ra.append(x[3]); aj.append(x[4]); aa.append(x[5]); tj.append(r['tj'])
        L.append(f"{r['name']:10s} N*={r['N']:.0f} (exact ns {r['ns_b']:.6f} r {r['r_b']:.4e} a {r['a_b']:.3e}) | "
                 f"dns Janus {x[0]:.1e} ASPIC {x[1]:.1e} | dr/r Janus {x[2]:.1e} ASPIC {x[3]:.1e} | da Janus {x[4]:.1e} ASPIC {x[5]:.1e} | "
                 f"t Janus {r['tj']*1e3:.1f} ms, ASPIC {a['t']*1e6:.2f} us, exact {r['tb']:.0f} s")
    md = np.median
    C1 = md(dj) <= md(da)/10 and max(dj) < max(da); C2 = md(rj) <= md(ra)/3; C3 = md(aj) <= md(aa); C4 = md(tj) <= 0.1
    L.append(f"medians: dns Janus {md(dj):.1e} ASPIC {md(da):.1e} (max {max(dj):.1e} vs {max(da):.1e}) | dr/r {md(rj):.1e} vs {md(ra):.1e} | "
             f"da {md(aj):.1e} vs {md(aa):.1e} | Janus time {md(tj)*1e3:.1f} ms")
    L.append(f"C1 {C1}  C2 {C2}  C3 {C3}  C4 {C4}  -> {'JANUS MORE ACCURATE' if (C1 and C2 and C3) else 'NOT SHOWN'}  ({len(R)}/14 points)")
    open('field_tests/results/janus_j7a_headtohead.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
if __name__ == '__main__': run() if sys.argv[1] == 'run' else summary()
