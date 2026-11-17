"""J7g (locked PREREG_J7g_pulse_reheating): pulse-2 (ln R_rad route) and pulse-3 ((w, ln rho_reh) route) on every J7f-scored model.
Usage: python3 theory/janus/j7g_pulse_reheat.py aspic | run | summary"""
import sys, os, json, math, time, subprocess, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
import importlib.util
sp = importlib.util.spec_from_file_location('j7f', 'theory/janus/j7f_pulse.py'); F = importlib.util.module_from_spec(sp); sp.loader.exec_module(F)
I = F.I; OUT = 'theory/janus/aspic/pulse'; PART = 'field_tests/results/janus_j7g.part.jsonl'; PSTAR = 2.1127e-9
ROUTES = [('rrad', 0.0), ('rrad', -10.0), ('rhow', -100.0), ('rhow', -150.0)]
def src(m, pars):
    a = ','.join(pars); c = (a + ',') if a else ''; cc = (',' + a) if a else ''
    return f"""program pr
  use infprec, only : kp
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use srreheat, only : Nzero
  use {m}sr
  use {m}reheat
  implicit none
  real(kp) :: x, xe, e(3), bf, P
  P = 2.1127e-9_kp; xe = {m}_x_endinf({a})
  write(*,'(A,ES24.16)') 'NZ ', Nzero
  x = {m}_x_rrad({c}xe, 0._kp, P, bf); e = (/{m}_epsilon_one(x{cc}), {m}_epsilon_two(x{cc}), {m}_epsilon_three(x{cc})/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rrad ', 0.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
  x = {m}_x_rrad({c}xe, -10._kp, P, bf); e = (/{m}_epsilon_one(x{cc}), {m}_epsilon_two(x{cc}), {m}_epsilon_three(x{cc})/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rrad ', -10.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
  x = {m}_x_star({c}xe, 0._kp, -100._kp, P, bf); e = (/{m}_epsilon_one(x{cc}), {m}_epsilon_two(x{cc}), {m}_epsilon_three(x{cc})/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rhow ', -100.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
  x = {m}_x_star({c}xe, 0._kp, -150._kp, P, bf); e = (/{m}_epsilon_one(x{cc}), {m}_epsilon_two(x{cc}), {m}_epsilon_three(x{cc})/)
  write(*,'(A,A,F7.1,5ES24.15)') 'RT ', 'rhow ', -150.0, -bf, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), x
end program pr
"""
def aspic():
    for m, pars in F.P.items():
        d = f'{OUT}/{m}'; os.makedirs(d, exist_ok=True); open(f'{d}/r.f90', 'w').write(src(m, pars))
        cc = subprocess.run(['gfortran', '-O2', '-ffree-line-length-none', f'-I{I}/include/aspic', f'{d}/r.f90', f'-L{I}/lib', '-laspic', f'-Wl,-rpath,{I}/lib', '-o', f'{d}/r'], capture_output=True, text=True)
        if cc.returncode: open(f'{d}/reheat_out.txt', 'w').write('COMPILE ' + cc.stderr[-300:]); print(m, 'compile fail'); continue
        try: r = subprocess.run([f'{d}/r'], capture_output=True, text=True, timeout=60); txt = r.stdout + r.stderr
        except subprocess.TimeoutExpired: txt = 'TIMEOUT'
        open(f'{d}/reheat_out.txt', 'w').write(txt); print(m, 'RT lines:', txt.count('RT '), flush=True)

def parse(m):
    t = open(f'{OUT}/{m}/reheat_out.txt').read(); R = {}; N0 = None
    for l in t.splitlines():
        if l.startswith('NZ '): N0 = float(l.split()[1])
        if l.startswith('RT '): c = l.split(); R[(c[1], float(c[2]))] = dict(dN=float(c[3]), ns=float(c[4]), r=float(c[5]), a=float(c[6]))
    return R, N0
def build(m):
    """same potential/start construction as J7f (after its DEVIATIONS D1)."""
    from tools.janus_calc.core import Model
    pts, vg, msg = F.parse(m)
    x, V, dV = (np.array(v) for v in zip(*vg)); o = np.argsort(x); x, V, dV = x[o], V[o], dV[o]
    ok = np.isfinite(V) & np.isfinite(dV) & (V > 0); x, V, dV = x[ok], V[ok], dV[ok]
    x60, xe = pts[60.0]['x'], pts[60.0]['xe']; sgn = 1 if x60 > xe else -1
    s = abs(np.interp(x60, x, dV)/np.interp(x60, x, V))/math.sqrt(2*pts[60.0]['e1'])
    far = x if sgn > 0 else x[::-1]; dd = dV if sgn > 0 else dV[::-1]
    stop = next((i for i in range(1, len(far)) if np.sign(dd[i]) != np.sign(dd[min(len(dd)-1, 5)])), len(far))
    sel = (x >= min(far[0], far[stop-1])) & (x <= max(far[0], far[stop-1])); x, V, dV = x[sel], V[sel], dV[sel]
    SV, SD = CubicSpline(x*s, V), CubicSpline(x*s, dV/s); Vf = lambda p: float(SV(p)); dVf = lambda p: float(SD(p))
    cand = sorted([p for p in x*s if sgn*(p - x60*s) >= 0], key=lambda p: sgn*p)
    for p0 in cand[:: max(1, len(cand)//200)]:
        try:
            mm = Model(Vf, dVf, p0, Nmax=4000)
            if mm.Nend >= 75: return Vf, dVf, p0, mm
        except Exception: continue
    raise RuntimeError('no start')
def run():
    from tools.janus_calc.core import spectra3, CE
    from tools.serapis_calc.ms import Background, spectra_fast
    DL = tuple(np.linspace(-1, 1, 9)); done = set()
    scored = [json.loads(l)['m'] for l in open(F.PART) if l.strip() and json.loads(l)['status'] == 'scored']
    if os.path.exists(PART): done = {json.loads(l)['m'] for l in open(PART) if l.strip()}
    for m in scored:
        if m in done: continue
        rec = dict(m=m)
        try:
            A, N0 = parse(m)
            if len(A) < 4 or N0 is None: raise RuntimeError('ASPIC reheating gave no result')
            Vf, dVf, p0, mm = build(m); bg = Background(Vf, dVf, p0, Nmax=4000)
            Hj = lambda N: math.sqrt(Vf(mm.sol.sol(N)[0])/(3 - 0.5*mm.sol.sol(N)[1]**2)); Hb = lambda N: bg.state(N)[3]
            def rhs(route, val, Hs, He, Phat):
                lnM4 = math.log(PSTAR/Phat)
                lnR = val if route == 'rrad' else (val - (math.log(3) + lnM4 + 2*math.log(He)))/12
                return lnR - N0 + 0.25*lnM4 + math.log(Hs) - 0.5*math.log(He) - 0.25*math.log(3)
            for route, val in ROUTES:
                Hej = Hj(mm.Nend - 1e-9)
                def g(dN):
                    e1, e2, _ = mm.flow(dN); P = Hj(mm.Nend - dN)**2/(8*math.pi**2*e1)*(1 - 2*(1+CE)*e1 - CE*e2)
                    return dN - rhs(route, val, Hj(mm.Nend - dN), Hej, P)
                dNj = brentq(g, 20.0, min(90.0, mm.Nend - 1.0), xtol=1e-10); j = spectra3(mm, dNj)
                Heb = Hb(bg.Nend - 1e-9); dN = dNj
                for it in range(8):
                    b = spectra_fast(bg, dN, dlnk=DL, bd=1000.0); new = rhs(route, val, Hb(bg.Nend - dN), Heb, b['PR'])
                    if abs(new - dN) < 1e-7: dN = new; break
                    dN = new
                b = spectra_fast(bg, dN, dlnk=DL, bd=1000.0); a = A[(route, val)]
                rec[f'{route}{val}'] = dict(dN_j=dNj, dN_b=dN, dN_a=a['dN'], ns_j=float(j['ns']), r_j=float(j['r']), a_j=float(j['alpha_s']),
                                           ns_b=float(b['ns']), r_b=float(b['r']), a_b=float(b['alpha_s']), ns_a=a['ns'], r_a=a['r'], a_a=a['a'])
            rec['status'] = 'scored'
        except Exception as e:
            rec['status'] = 'listed'; rec['why'] = str(e)[:300]
        open(PART, 'a').write(json.dumps(rec) + '\n'); print(m, rec['status'], rec.get('why', ''), flush=True)
def summary():
    R = [json.loads(l) for l in open(PART) if l.strip()]; L = []
    for route in ('rrad', 'rhow'):
        D = {k: [] for k in ('nj', 'na', 'rj', 'ra', 'aj', 'aa', 'Nj', 'Na')}
        for r in R:
            if r['status'] != 'scored': continue
            for key, q in r.items():
                if not key.startswith(route): continue
                x = (abs(q['ns_j']-q['ns_b']), abs(q['ns_a']-q['ns_b']), abs(q['r_j']/q['r_b']-1), abs(q['r_a']/q['r_b']-1), abs(q['a_j']-q['a_b']), abs(q['a_a']-q['a_b']), abs(q['dN_j']-q['dN_b']), abs(q['dN_a']-q['dN_b']))
                for k, v in zip(D, x): D[k].append(v)
        md = np.median; n = len(D['nj']); nb = sum(D['nj'][i] < D['na'][i] for i in range(n))
        C1 = bool(md(D['nj']) <= md(D['na'])/10 and max(D['nj']) < max(D['na'])); C2 = bool(md(D['rj']) <= md(D['ra'])/3); C3 = bool(md(D['aj']) <= md(D['aa']))
        L.append(f"{route}: {n} points; Janus n_s better on {nb}/{n}; medians dns J {md(D['nj']):.1e} A {md(D['na']):.1e} (max {max(D['nj']):.1e} vs {max(D['na']):.1e}) | dr/r {md(D['rj']):.1e} vs {md(D['ra']):.1e} | da {md(D['aj']):.1e} vs {md(D['aa']):.1e} | ASPIC dN* err median {md(D['Na']):.3f} max {max(D['Na']):.3f}{'  [C6 FLAG]' if md(D['Na']) > 0.5 else ''}; C1 {C1} C2 {C2} C3 {C3} -> {'JANUS MORE ACCURATE' if (C1 and C2 and C3) else 'NOT SHOWN'}")
    L += [f"{r['m']}: LISTED {r['why']}" for r in R if r['status'] != 'scored']
    open('field_tests/results/janus_j7g_pulse_reheat.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L))
if __name__ == '__main__': {'aspic': aspic, 'run': run, 'summary': summary}[sys.argv[1]]()
