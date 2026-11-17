"""JMF4b (locked PREREG_JMF4b_mmc_bug_check): JMF4 with MMC's coded derivatives."""
import sys, re, time, subprocess, tempfile, numpy as np; sys.path.insert(0, '.')
from tools.janus_calc.mfms import spectra_mf
from tools.lockbench.provenance import stamp
MMC = '/home/claude/ext/mmc'; base = open(f'{MMC}/parameters_multimodecode.txt').read(); t0 = time.time()
def mmc(choice, rows, f0):
    d = tempfile.mkdtemp(); p = re.sub(r'num_inflaton = \d+', 'num_inflaton = 2', base)
    p = re.sub(r'potential_choice = \d+', f'potential_choice = {choice}', p)
    p = p.replace('get_runningofrunning = .true.', 'get_runningofrunning = .false.').replace('use_deltaN_SR = .true.', 'use_deltaN_SR = .false.')
    p = re.sub(r'phi_init0 = .*', f'phi_init0 = {f0[0]} {f0[1]}', p)
    for k in (1, 2, 3, 4): p = re.sub(rf'vparams\({k},:\) = .*', f'vparams({k},:) = ' + ' '.join(f'{v:.10f}' for v in rows.get(k, (1.0, 1.0))), p)
    open(f'{d}/parameters_multimodecode.txt', 'w').write(p)
    o = subprocess.run([f'{MMC}/powspec'], cwd=d, capture_output=True, text=True, timeout=900).stdout
    g = lambda n: re.search(rf'{n} =\s+([-0-9.E+]+)', o); ns, nt, rnt = g('n_s'), g('n_t'), g('r/n_t')
    if not (ns and nt and rnt): raise RuntimeError('MMC output not found: ' + o[-200:].replace('\n', ' '))
    return float(ns.group(1)), float(rnt.group(1))*float(nt.group(1))
m = np.array([1e-11, 9e-11]); lam = np.array([1e-12, 1e-12]); e = 1e-12; lg = np.log10
def V1(f): return float(0.5*m @ f**2 + f[0]**2*(lam @ f**2)/24)
def g1(f): return np.array([m[0]*f[0] + (4*lam[0]*f[0]**3 + 2*lam[1]*f[0]*f[1]**2)/24, m[1]*f[1] + 2*lam[1]*f[0]**2*f[1]/24])
def h1(f): o = 4*lam[1]*f[0]*f[1]/24; return np.array([[m[0] + (12*lam[0]*f[0]**2 + 2*lam[1]*f[1]**2)/24, o], [o, m[1] + 2*lam[1]*f[0]**2/24]])
def V2(f): return float(0.5*m @ f**2 + 2*e*f[0]*f[1])
def g2(f): return np.array([m[0]*f[0] + 2*e*f[1], m[1]*f[1] + 2*e*f[0]])
def h2(f): return np.array([[m[0], 2*e], [2*e, m[1]]])
def g1(f): return np.array([m[0]*f[0] + f[0]**3*lam[0]/6, m[1]*f[1] + f[0]**2*lam[1]*f[1]/12])
def h1(f): return np.array([[m[0] + 0.5*lam[0]*f[0]**2, 0.0], [lam[1]*f[0]*f[1]/6, m[1] + lam[1]*f[0]**2/12]])
def g2(f): return np.array([m[0]*f[0] + e*f[1], m[1]*f[1] + e*f[0]])
def h2(f): return np.array([[m[0], e], [e, m[1]]])
M = {'N1 quad+quartic intxn': (11, {1: tuple(lg(m)), 2: tuple(lg(lam))}, [12.0, 12.0], V1, g1, h1),
     'N2 off-diagonal mass': (12, {1: tuple(lg(m)), 2: (lg(e), lg(e))}, [12.0, 12.0], V2, g2, h2)}
def fdcheck(gr, he, f):
    H = np.array([(gr(f + 1e-5*np.eye(2)[i]) - gr(f - 1e-5*np.eye(2)[i]))/2e-5 for i in range(2)]).T; A = he(f)
    return float(np.max(np.abs(H - A))/np.max(np.abs(A)))
L = []; ok = True; partial = False
for name, (ch, rows, f0, V, gr, he) in M.items():
    try:
        fd = max(fdcheck(gr, he, np.array(x)) for x in ([12.0, 12.0], [5.0, 3.0]))   # reported only: MMC's coded set is inconsistent by design here
        ns_m, r_m = mmc(ch, rows, f0); s = spectra_mf(V, gr, he, f0)
    except Exception as ex:
        L.append(f'{name}: LISTED ({str(ex)[:200]})'); partial = True; print(L[-1], flush=True); continue
    c1 = abs(s['ns'] - ns_m) <= 2e-4; c2 = abs(s['r']/r_m - 1) <= 2e-3; ok &= c1 and c2
    L.append(f"{name}: MMC-coded d2V vs FD of MMC dV {fd:.1e} | Janus-MF ns {s['ns']:.6f} r {s['r']:.5f} | MMC ns {ns_m:.6f} r {r_m:.5f} | C1 |d| {abs(s['ns']-ns_m):.1e} {'PASS' if c1 else 'FAIL'}; C2 rel {abs(s['r']/r_m-1):.1e} {'PASS' if c2 else 'FAIL'}")
    print(L[-1], flush=True)
L.append('JMF4b: ' + ('PARTIAL' if partial and ok else "JMF4 FAILURE EXPLAINED BY MMC's DERIVATIVE CODE" if ok else 'NOT EXPLAINED'))
R = 'field_tests/results/janus_jmf4b.txt'; open(R, 'w').write('\n'.join(L) + '\n'); print(L[-1])
stamp(R, lock='field_tests/rules/PREREG_JMF4b_mmc_bug_check.md', code=['theory/janus/jmf4b_mmccoded.py', 'tools/janus_calc/mfms.py'], t0=t0)
