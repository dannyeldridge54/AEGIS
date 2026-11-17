"""J8 (locked PREREG_J8_aspic_rhow): as J7c2 but ln R_rad from (w = 0, ln rho_reh) via Martin-Ringeval Eq. 13, iterated with M^4."""
import sys, os, json, time, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from scipy.optimize import brentq
from tools.janus_calc.core import spectra3, CE
from tools.serapis_calc.ms import Background, spectra_fast
import importlib.util
sp = importlib.util.spec_from_file_location('j7b', 'theory/janus/j7b_wide.py'); J7B = importlib.util.module_from_spec(sp); sp.loader.exec_module(J7B)
PART = 'field_tests/results/janus_j8.part.jsonl'; ASP = 'theory/janus/aspic/aspic_j8_clean.txt'; W = 0.0; PSTAR = 2.1127e-9
A = {}; N0 = None
for l in open(ASP):
    c = l.split()
    if c[0] == 'NZERO': N0 = float(c[1]); continue
    A[(int(c[0]), float(c[1]))] = dict(dN=float(c[2]), ns=float(c[3]), r=float(c[4]), a=float(c[5]))
def rhs(LRH, Hs, He, Phat):   # LRH = ln(rho_reh/M_P^4); ln R_rad from Eq. 13 with rho_end = 3 M^4 He^2, then Eq. 15
    lnM4 = math.log(PSTAR/Phat); lnR = (1 - 3*W)/(12*(1 + W))*(LRH - (math.log(3) + lnM4 + 2*math.log(He)))
    return lnR - N0 + 0.25*lnM4 + math.log(Hs) - 0.5*math.log(He) - 0.25*math.log(3)
def janus_dN(m, V, LR):
    H = lambda N: math.sqrt(V(m.sol.sol(N)[0])/(3 - 0.5*m.sol.sol(N)[1]**2)); He = H(m.Nend - 1e-9)
    def g(dN):
        e1, e2, _ = m.flow(dN); P = H(m.Nend - dN)**2/(8*math.pi**2*e1)*(1 - 2*(1+CE)*e1 - CE*e2)
        return dN - rhs(LR, H(m.Nend - dN), He, P)
    return brentq(g, 20.0, min(90.0, m.Nend - 1.0), xtol=1e-10)
def exact_dN(bg, LR, dN0):
    H = lambda N: bg.state(N)[3]; He = H(bg.Nend - 1e-9); dN = dN0
    for it in range(8):
        b = spectra_fast(bg, dN, dlnk=J7B.DL, bd=1000.0); new = rhs(LR, H(bg.Nend - dN), He, b['PR'])
        if abs(new - dN) < 1e-7: dN = new; break
        dN = new
    return dN, spectra_fast(bg, dN, dlnk=J7B.DL, bd=1000.0), it
def run():
    done = set()
    if os.path.exists(PART): done = {(json.loads(l)['i'], json.loads(l)['LR']) for l in open(PART) if l.strip()}
    for i in [k for k in range(1, 18) if k != 9]:
        if all((i, L) in done for L in (-100.0, -150.0)): continue
        name, V, dV, y0, m = J7B.build(i); bg = Background(V, dV, y0, Nmax=3000)
        for LR in (-100.0, -150.0):
            if (i, LR) in done: continue
            t = time.time(); dNj = janus_dN(m, V, LR); j = spectra3(m, dNj); tj = time.time() - t
            dNb, b, it = exact_dN(bg, LR, dNj)
            rec = dict(i=i, name=name, LR=LR, dN_j=dNj, dN_b=dNb, iters=it, ns_j=float(j['ns']), r_j=float(j['r']), a_j=float(j['alpha_s']),
                       ns_b=float(b['ns']), r_b=float(b['r']), a_b=float(b['alpha_s']), tj=tj)
            open(PART, 'a').write(json.dumps(rec)+'\n'); print(rec, flush=True)
def summary():
    R = {(r['i'], r['LR']): r for r in (json.loads(l) for l in open(PART) if l.strip())}
    L = [f"N_0 (ASPIC Nzero) = {N0:.6f}; P* = {PSTAR}; KMII a=2 excluded (no ASPIC prediction)"]; D = {k: [] for k in ('nj', 'na', 'rj', 'ra', 'aj', 'aa', 'Nj', 'Na')}
    for k in sorted(R):
        r, a = R[k], A[k]
        x = (abs(r['ns_j']-r['ns_b']), abs(a['ns']-r['ns_b']), abs(r['r_j']/r['r_b']-1), abs(a['r']/r['r_b']-1),
             abs(r['a_j']-r['a_b']), abs(a['a']-r['a_b']), abs(r['dN_j']-r['dN_b']), abs(a['dN']-r['dN_b']))
        for key, v in zip(('nj', 'na', 'rj', 'ra', 'aj', 'aa', 'Nj', 'Na'), x): D[key].append(v)
        L.append(f"{r['name']:14s} ln rho_reh={r['LR']:+.0f} w=0: exact dN* {r['dN_b']:.4f} (ASPIC {a['dN']:.4f}, Janus {r['dN_j']:.4f}) ns {r['ns_b']:.6f} | dns J {x[0]:.1e} A {x[1]:.1e} | dr/r J {x[2]:.1e} A {x[3]:.1e} | da J {x[4]:.1e} A {x[5]:.1e}")
    md = np.median
    C1 = bool(md(D['nj']) <= md(D['na'])/10 and max(D['nj']) < max(D['na'])); C2 = bool(md(D['rj']) <= md(D['ra'])/3); C3 = bool(md(D['aj']) <= md(D['aa']))
    nb = sum(D['nj'][q] < D['na'][q] for q in range(len(D['nj'])))
    L.append(f"{len(R)} points; Janus n_s better on {nb}/{len(R)}")
    L.append(f"medians: dns J {md(D['nj']):.1e} A {md(D['na']):.1e} (max {max(D['nj']):.1e} vs {max(D['na']):.1e}) | dr/r {md(D['rj']):.1e} vs {md(D['ra']):.1e} | da {md(D['aj']):.1e} vs {md(D['aa']):.1e}")
    L.append(f"C5/C6 dN* error vs exact: ASPIC median {md(D['Na']):.4f} max {max(D['Na']):.4f}; Janus median {md(D['Nj']):.1e} max {max(D['Nj']):.1e}" + ("  [C6 FLAG: >0.5, convention mismatch suspected]" if md(D['Na']) > 0.5 else ""))
    L.append(f"C1 {C1} C2 {C2} C3 {C3} -> {'JANUS MORE ACCURATE (w, rho_reh route)' if (C1 and C2 and C3) else 'NOT SHOWN'}")
    open('field_tests/results/janus_j8_rhow.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
if __name__ == '__main__': {'run': run, 'summary': summary}[sys.argv[1]]()
