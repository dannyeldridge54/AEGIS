"""J7f (locked PREREG_J7f_aspic_pulse): Janus vs ASPIC vs exact MS on every automatable ASPIC model in one batch.
Usage: python3 theory/janus/j7f_pulse.py aspic | run | summary"""
import sys, os, json, math, time, subprocess, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from scipy.interpolate import CubicSpline
I = '/home/claude/ext/aspic_inst'; OUT = 'theory/janus/aspic/pulse'; PART = 'field_tests/results/janus_j7f.part.jsonl'
# one parameter set per model: from the model's *main.f90 where set there, otherwise a standard value (Fortran literals)
P = {'ahi': ['1._kp'], 'ai': ['1e-2_kp'], 'bei': ['1._kp', '2._kp'], 'cnai': ['0.1_kp'], 'cnbi': ['0.1_kp'],
     'dei': ['0.5_kp', '50._kp'], 'di': ['0.01_kp', '0.1_kp'], 'dwi': ['25._kp'], 'esi': ['1._kp'], 'fi': ['1e-6_kp', '1._kp'],
     'gdwi': ['2._kp', '10._kp'], 'gmlfi': ['2._kp', '1._kp', '0.01_kp'], 'hbi': ['1._kp', '10._kp'], 'hf1i': ['0.1_kp'],
     'hi': ['20000._kp'], 'kmii': ['1.2_kp'], 'kmiii': ['1._kp', '1._kp'], 'lfi': ['2._kp'], 'li': ['0.3_kp'], 'mhi': ['10._kp'],
     'ncli': ['1e-4_kp', '0.18_kp', '2._kp'], 'ni': ['5._kp'], 'oi': ['0.01_kp', '0.5_kp'], 'oripi': ['1e-2_kp'], 'osti': ['100._kp'],
     'pai': ['1._kp'], 'pli': ['0.1_kp'], 'psni': ['1e-3_kp', '5._kp'], 'rchi': ['5._kp'], 'rcmi': ['5e-4_kp'], 'rcqi': ['5e-2_kp'],
     'rgi': ['1._kp'], 'rpqti': ['10._kp', '0.01_kp', '-0.01_kp'], 'saai': ['2._kp'], 'sabi': ['2._kp', '2._kp'], 'sati': ['1._kp', '1._kp'],
     'sbki': ['-0.01_kp'], 'sfi': ['2._kp', '20._kp'], 'si': [], 'ti': ['0.1_kp', '10._kp'], 'vfmi': ['2.5_kp', '0.8_kp'], 'wri': ['10._kp']}
def fsrc(m, pars):
    a = ','.join(pars); c = (',' + a) if a else ''
    return f"""program pp
  use infprec, only : kp
  use srflow, only : scalar_spectral_index, tensor_to_scalar_ratio, scalar_running
  use {m}sr
  implicit none
  real(kp) :: Ns(2) = (/50._kp, 60._kp/), x, xe, e(3), x60, xf, xx
  integer :: j, k
  xe = {m}_x_endinf({a})
  do j = 1, 2
    x = {m}_x_trajectory(-Ns(j), xe{c}); if (j == 2) x60 = x
    e = (/{m}_epsilon_one(x{c}), {m}_epsilon_two(x{c}), {m}_epsilon_three(x{c})/)
    write(*,'(A,F5.1,6ES24.15)') 'PT ', Ns(j), x, scalar_spectral_index(e), tensor_to_scalar_ratio(e), scalar_running(e), xe, e(1)
  end do
  xf = x60 + 4._kp*(x60 - xe)
  do k = 0, 3999
    xx = xe + (xf - xe)*real(k,kp)/3999._kp
    write(*,'(A,3ES24.15)') 'VG ', xx, {m}_norm_potential(xx{c}), {m}_norm_deriv_potential(xx{c})
  end do
end program pp
"""
def aspic():
    for m, pars in P.items():
        d = f'{OUT}/{m}'; os.makedirs(d, exist_ok=True); open(f'{d}/p.f90', 'w').write(fsrc(m, pars))
        cc = subprocess.run(['gfortran', '-O2', f'-I{I}/include/aspic', f'{d}/p.f90', f'-L{I}/lib', '-laspic', f'-Wl,-rpath,{I}/lib', '-o', f'{d}/p'], capture_output=True, text=True)
        if cc.returncode: open(f'{d}/out.txt', 'w').write('COMPILE ' + cc.stderr[-400:]); print(m, 'compile fail'); continue
        try: r = subprocess.run([f'{d}/p'], capture_output=True, text=True, timeout=60); txt = r.stdout + r.stderr
        except subprocess.TimeoutExpired: txt = 'TIMEOUT'
        open(f'{d}/out.txt', 'w').write(txt); print(m, 'PT lines:', txt.count('PT '), flush=True)
def parse(m):
    t = open(f'{OUT}/{m}/out.txt').read(); pts = {}; vg = []
    for l in t.splitlines():
        if l.startswith('PT '): c = l.split(); pts[float(c[1])] = dict(x=float(c[2]), ns=float(c[3]), r=float(c[4]), a=float(c[5]), xe=float(c[6]), e1=float(c[7]))
        elif l.startswith('VG '): c = l.split(); vg.append((float(c[1]), float(c[2]), float(c[3])))
    msg = [l for l in t.splitlines() if not l.startswith(('PT ', 'VG '))][:3]
    return pts, vg, msg
def run():
    from tools.janus_calc.core import Model, spectra3
    from tools.serapis_calc.ms import Background, spectra_fast
    DL = tuple(np.linspace(-1, 1, 9)); done = set()
    if os.path.exists(PART): done = {json.loads(l)['m'] for l in open(PART) if l.strip()}
    for m in P:
        if m in done: continue
        rec = dict(m=m)
        try:
            pts, vg, msg = parse(m)
            if len(pts) < 2 or len(vg) < 100: raise RuntimeError('ASPIC gave no result: ' + ' | '.join(msg)[:200])
            x, V, dV = (np.array(v) for v in zip(*vg)); o = np.argsort(x); x, V, dV = x[o], V[o], dV[o]
            ok = np.isfinite(V) & np.isfinite(dV) & (V > 0); x, V, dV = x[ok], V[ok], dV[ok]
            x60, xe = pts[60.0]['x'], pts[60.0]['xe']; sgn = 1 if x60 > xe else -1
            s = abs(np.interp(x60, x, dV)/np.interp(x60, x, V))/math.sqrt(2*pts[60.0]['e1'])
            # keep the monotonic-slope branch from x_end outward
            far = x if sgn > 0 else x[::-1]; dd = dV if sgn > 0 else dV[::-1]
            stop = next((i for i in range(1, len(far)) if np.sign(dd[i]) != np.sign(dd[min(len(dd)-1, 5)])), len(far))
            sel = (x >= min(far[0], far[stop-1])) & (x <= max(far[0], far[stop-1])); x, V, dV = x[sel], V[sel], dV[sel]
            SV, SD = CubicSpline(x*s, V), CubicSpline(x*s, dV/s)
            Vf = lambda p: float(SV(p)); dVf = lambda p: float(SD(p))
            cand = sorted([p for p in x*s if sgn*(p - x60*s) >= 0], key=lambda p: sgn*p); m_ok = None   # DEVIATIONS D1: nearest-first
            for p0 in cand[:: max(1, len(cand)//200)]:
                try:
                    mm = Model(Vf, dVf, p0, Nmax=4000)
                    if mm.Nend >= 75: m_ok = (p0, mm); break
                except Exception: continue
            if m_ok is None: raise RuntimeError('grid gives < 75 e-folds or no end')
            p0, mm = m_ok; bg = Background(Vf, dVf, p0, Nmax=4000)
            for N in (50.0, 60.0):
                t = time.time(); j = spectra3(mm, N); tj = time.time() - t; b = spectra_fast(bg, N, dlnk=DL, bd=1000.0); a = pts[N]
                rec[str(N)] = dict(ns_j=float(j['ns']), r_j=float(j['r']), a_j=float(j['alpha_s']), ns_b=float(b['ns']), r_b=float(b['r']), a_b=float(b['alpha_s']),
                                   ns_a=a['ns'], r_a=a['r'], a_a=a['a'], tj=tj)
            rec['status'] = 'scored'
        except Exception as e:
            rec['status'] = 'listed'; rec['why'] = str(e)[:300]
        open(PART, 'a').write(json.dumps(rec) + '\n'); print(m, rec['status'], rec.get('why', ''), flush=True)
def summary():
    R = [json.loads(l) for l in open(PART) if l.strip()]; L = []; D = {k: [] for k in ('nj', 'na', 'rj', 'ra', 'aj', 'aa', 't')}
    for r in R:
        if r['status'] != 'scored': L.append(f"{r['m']:6s} LISTED: {r['why']}"); continue
        for N in ('50.0', '60.0'):
            q = r[N]; x = (abs(q['ns_j']-q['ns_b']), abs(q['ns_a']-q['ns_b']), abs(q['r_j']/q['r_b']-1), abs(q['r_a']/q['r_b']-1), abs(q['a_j']-q['a_b']), abs(q['a_a']-q['a_b']))
            for k, v in zip(('nj', 'na', 'rj', 'ra', 'aj', 'aa'), x): D[k].append(v)
            D['t'].append(q['tj'])
            L.append(f"{r['m']:6s} N*={N[:2]} exact ns {q['ns_b']:.6f} r {q['r_b']:.3e} | dns J {x[0]:.1e} A {x[1]:.1e} | dr/r J {x[2]:.1e} A {x[3]:.1e} | da J {x[4]:.1e} A {x[5]:.1e}")
    md = np.median; n = len(D['nj']); nb = sum(D['nj'][i] < D['na'][i] for i in range(n))
    C1 = bool(md(D['nj']) <= md(D['na'])/10 and max(D['nj']) < max(D['na'])); C2 = bool(md(D['rj']) <= md(D['ra'])/3); C3 = bool(md(D['aj']) <= md(D['aa'])); C4 = bool(md(D['t']) <= 0.1)
    sc = sum(r['status'] == 'scored' for r in R)
    L.append(f"models: {sc} scored, {len(R)-sc} listed; points {n}; Janus n_s better on {nb}/{n}")
    L.append(f"medians: dns J {md(D['nj']):.1e} A {md(D['na']):.1e} (max {max(D['nj']):.1e} vs {max(D['na']):.1e}) | dr/r {md(D['rj']):.1e} vs {md(D['ra']):.1e} | da {md(D['aj']):.1e} vs {md(D['aa']):.1e} | t {md(D['t'])*1e3:.1f} ms")
    L.append(f"C1 {C1} C2 {C2} C3 {C3} C4 {C4} -> {'JANUS MORE ACCURATE' if (C1 and C2 and C3) else 'NOT SHOWN'}")
    open('field_tests/results/janus_j7f_pulse.txt', 'w').write('\n'.join(L)+'\n'); print('\n'.join(L[-3:]))
if __name__ == '__main__': {'aspic': aspic, 'run': run, 'summary': summary}[sys.argv[1]]()
