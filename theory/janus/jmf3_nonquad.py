"""JMF3 (locked PREREG_JMF3_nonquadratic)."""
import sys, re, math, time, subprocess, tempfile, numpy as np; sys.path.insert(0, '.')
from tools.janus_calc.mfms import spectra_mf
from tools.lockbench.provenance import stamp
MMC = '/home/claude/ext/mmc'; base = open(f'{MMC}/parameters_multimodecode.txt').read(); t0 = time.time()
def mmc(choice, rows, f0):
    d = tempfile.mkdtemp(); p = re.sub(r'num_inflaton = \d+', 'num_inflaton = 2', base)
    p = re.sub(r'potential_choice = \d+', f'potential_choice = {choice}', p)
    p = p.replace('get_runningofrunning = .true.', 'get_runningofrunning = .false.')  # DEV D1
    p = re.sub(r'phi_init0 = .*', f'phi_init0 = {f0[0]} {f0[1]}', p)
    for k in (1, 2, 3, 4): p = re.sub(rf'vparams\({k},:\) = .*', f'vparams({k},:) = ' + ' '.join(f'{v:.10f}' for v in rows.get(k, (1.0, 1.0))), p)
    open(f'{d}/parameters_multimodecode.txt', 'w').write(p)
    o = subprocess.run([f'{MMC}/powspec'], cwd=d, capture_output=True, text=True, timeout=900).stdout
    g = lambda n: re.search(rf'{n} =\s+([-0-9.E+]+)', o); ns, nt, rnt = g('n_s'), g('n_t'), g('r/n_t')
    if not (ns and nt and rnt): raise RuntimeError('MMC output not found: ' + o[-200:].replace('\n', ' '))
    return float(ns.group(1)), float(rnt.group(1))*float(nt.group(1))
lam = np.array([1e-13, 9e-13]); L4 = np.array([10**-2.6]*2)**4; fi = 1/np.array([10**1.0, 10**1.2])
M = {'M1 quartic': (3, {1: (-13.0, -13 + math.log10(9))}, [20.0, 20.0],
                    lambda f: float(0.25*lam @ f**4), lambda f: lam*f**3, lambda f: np.diag(3*lam*f**2)),
     'M2 axions': (2, {1: (-2.6, -2.6), 2: (1.0, 1.2)}, [8.0, 12.0],
                   lambda f: float(L4 @ (1 + np.cos(fi*f))), lambda f: -L4*fi*np.sin(fi*f), lambda f: np.diag(-L4*fi**2*np.cos(fi*f)))}
from tools.serapis_calc.multifield import run as _run   # DEV D2: IC rule for M2
_V2, _g2 = M['M2 axions'][3], M['M2 axions'][4]; f2 = None
for st in range(0, 23):
    f = np.array([8.0 + st, 12.0 + st])
    try: Ne = _run(_V2, _g2, f, Nmax=2000, v0=-_g2(f)/_V2(f))[1]
    except Exception: continue
    if 70 <= Ne <= 200: f2 = [float(f[0]), float(f[1])]; print('DEV D2: M2 phi_init', f2, 'N_tot', round(Ne, 2)); break
if f2 is None: M.pop('M2 axions')
else: M['M2 axions'] = (2, M['M2 axions'][1], f2) + M['M2 axions'][3:]
L = []; ok = True; partial = f2 is None
for name, (ch, rows, f0, V, gr, he) in M.items():
    try:
        ns_m, r_m = mmc(ch, rows, f0); s = spectra_mf(V, gr, he, f0)
    except Exception as e:
        L.append(f'{name}: LISTED ({str(e)[:200]})'); partial = True; print(L[-1], flush=True); continue
    c1 = abs(s['ns'] - ns_m) <= 2e-4; c2 = abs(s['r']/r_m - 1) <= 2e-3; ok &= c1 and c2
    L.append(f"{name}: Janus-MF ns {s['ns']:.6f} r {s['r']:.5f} alpha_s {s['alpha_s']:.2e} | MMC ns {ns_m:.6f} r {r_m:.5f} | C1 |d| {abs(s['ns']-ns_m):.1e} {'PASS' if c1 else 'FAIL'}; C2 rel {abs(s['r']/r_m-1):.1e} {'PASS' if c2 else 'FAIL'}")
    print(L[-1], flush=True)
L.append('JMF3: ' + ('PARTIAL' if partial and ok else 'JANUS-MF VALIDATED BEYOND QUADRATIC' if ok else 'NOT VALIDATED'))
R = 'field_tests/results/janus_jmf3.txt'; open(R, 'w').write('\n'.join(L) + '\n'); print(L[-1])
stamp(R, lock='field_tests/rules/PREREG_JMF3_nonquadratic.md', code=['theory/janus/jmf3_nonquad.py', 'tools/janus_calc/mfms.py'], t0=t0)
