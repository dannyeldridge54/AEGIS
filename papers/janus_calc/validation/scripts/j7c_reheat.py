"""J7c (locked PREREG_J7c_aspic_reheating). Usage: python3 ... run | summary."""
import sys, os, json, time, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from scipy.optimize import brentq
from tools.janus_calc.core import spectra3
from tools.serapis_calc.ms import Background, spectra_fast
import importlib.util
sp = importlib.util.spec_from_file_location('j7b', 'theory/janus/j7b_wide.py'); J7B = importlib.util.module_from_spec(sp); sp.loader.exec_module(J7B)
PART = 'field_tests/results/janus_j7c.part.jsonl'; ASP = 'theory/janus/aspic/aspic_j7c_clean.txt'
A = {}; N0 = None
for l in open(ASP):
    c = l.split()
    if c[0] == 'NZERO': N0 = float(c[1]); continue
    A[(int(c[0]), float(c[1]))] = dict(dN=float(c[2]), ns=float(c[3]), r=float(c[4]), a=float(c[5]))
def match(Nend, Hof, LR):
    """exact Martin-Ringeval Eq 15 rearranged: Delta N* = LR - N0 + 1/2 ln H* - 1/4 ln(3 H_end^2)."""
    He = Hof(Nend - 1e-9)
    f = lambda Np: (Nend - Np) - (LR - N0 + 0.5*math.log(Hof(Np)) - 0.25*math.log(3*He*He))
    Np = brentq(f, 0.0, Nend - 1.0, xtol=1e-12); return Nend - Np
def run():
    done = set()
    if os.path.exists(PART): done = {(json.loads(l)['i'], json.loads(l)['LR']) for l in open(PART) if l.strip()}
    for i in [k for k in range(1, 18) if k != 9]:
        if all((i, L) in done for L in (0.0, -10.0)): continue
        name, V, dV, y0, m = J7B.build(i); bg = Background(V, dV, y0, Nmax=3000)
        Hj = lambda N: math.sqrt(V(m.sol.sol(N)[0])/(3 - 0.5*m.sol.sol(N)[1]**2))
        Hb = lambda N: bg.state(N)[3]
        for LR in (0.0, -10.0):
            if (i, LR) in done: continue
            t = time.time(); dNj = match(m.Nend, Hj, LR); j = spectra3(m, dNj); tj = time.time() - t
            dNb = match(bg.Nend, Hb, LR); b = spectra_fast(bg, dNb, dlnk=J7B.DL, bd=1000.0)
            rec = dict(i=i, name=name, LR=LR, dN_j=dNj, dN_b=dNb, ns_j=float(j['ns']), r_j=float(j['r']), a_j=float(j['alpha_s']),
                       ns_b=float(b['ns']), r_b=float(b['r']), a_b=float(b['alpha_s']), tj=tj)
            open(PART, 'a').write(json.dumps(rec)+'\n'); print(rec, flush=True)
def summary():
    R = {(r['i'], r['LR']): r for r in (json.loads(l) for l in open(PART) if l.strip())}
    L = [f"N_0 (ASPIC Nzero) = {N0:.6f}; KMII a=2 excluded (no ASPIC prediction, J7b)"]; D = {k: [] for k in ('nj', 'na', 'rj', 'ra', 'aj', 'aa', 'Nj', 'Na')}
    for k in sorted(R):
        r, a = R[k], A[k]
        x = (abs(r['ns_j']-r['ns_b']), abs(a['ns']-r['ns_b']), abs(r['r_j']/r['r_b']-1), abs(a['r']/r['r_b']-1),
             abs(r['a_j']-r['a_b']), abs(a['a']-r['a_b']), abs(r['dN_j']-r['dN_b']), abs(a['dN']-r['dN_b']))
        for key, v in zip(('nj', 'na', 'rj', 'ra', 'aj', 'aa', 'Nj', 'Na'), x): D[key].append(v)
        L.append(f"{r['name']:14s} lnRrad={r['LR']:+.0f}: exact dN* {r['dN_b']:.4f} (ASPIC {a['dN']:.4f}, Janus {r['dN_j']:.4f}) ns {r['ns_b']:.6f} | dns J {x[0]:.1e} A {x[1]:.1e} | dr/r J {x[2]:.1e} A {x[3]:.1e} | da J {x[4]:.1e} A {x[5]:.1e}")
    md = np.median
    C1 = bool(md(D['nj']) <= md(D['na'])/10 and max(D['nj']) < max(D['na'])); C2 = bool(md(D['rj']) <= md(D['ra'])/3); C3 = bool(md(D['aj']) <= md(D['aa']))
    nb = sum(D['nj'][q] < D['na'][q] for q in range(len(D['nj'])))
    L.append(f"{len(R)} points; Janus n_s better on {nb}/{len(R)}")
    L.append(f"medians: dns J {md(D['nj']):.1e} A {md(D['na']):.1e} (max {max(D['nj']):.1e} vs {max(D['na']):.1e}) | dr/r {md(D['rj']):.1e} vs {md(D['ra']):.1e} | da {md(D['aj']):.1e} vs {md(D['aa']):.1e} | C5 ASPIC dN* error median {md(D['Na']):.3f} max {max(D['Na']):.3f} (Janus {md(D['Nj']):.1e})")
    L.append(f"C1 {C1} C2 {C2} C3 {C3} -> {'JANUS MORE ACCURATE (reheating route)' if (C1 and C2 and C3) else 'NOT SHOWN'}")
    open('field_tests/results/janus_j7c_reheat.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
if __name__ == '__main__': {'run': run, 'summary': summary}[sys.argv[1]]()
