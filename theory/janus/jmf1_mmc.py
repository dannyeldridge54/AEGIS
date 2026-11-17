"""JMF1 (locked PREREG_JMF1_mmc)."""
import sys, os, re, math, shutil, subprocess, tempfile, numpy as np; sys.path.insert(0, '.')
from tools.serapis_calc.multifield import run
from tools.janus_calc.twofield import observe_multi
MMC = '/home/claude/ext/mmc'; L = []; ok = True
base = open(f'{MMC}/parameters_multimodecode.txt').read()
def mmc(R):
    d = tempfile.mkdtemp(); p = base
    p = re.sub(r'num_inflaton = \d+', 'num_inflaton = 2', p)
    p = re.sub(r'phi_init0 = .*', 'phi_init0 = 12.0 12.0', p)
    p = re.sub(r'vparams\(1,:\) = .*', f'vparams(1,:) = -11.0 {-11.0 + 2*math.log10(R):.10f}', p)
    for k in (2, 3, 4): p = re.sub(rf'vparams\({k},:\) = .*', f'vparams({k},:) = 1.0 1.0', p)
    open(f'{d}/parameters_multimodecode.txt', 'w').write(p)
    o = subprocess.run([f'{MMC}/powspec'], cwd=d, capture_output=True, text=True, timeout=600).stdout
    g = lambda name: re.search(rf'{name} =\s+([-0-9.E+]+)(?:\s+\(\s*([-0-9.E+]+)\))?', o)
    ns = g('n_s'); lines = o.splitlines(); hi = [i for i, l in enumerate(lines) if l.startswith('"phi0001"')]
    if ns is None or not hi or hi[-1] + 1 >= len(lines): raise RuntimeError('MMC output not found; tail: ' + ' | '.join(lines[-5:]))
    hdr = [h.strip('"') for h in lines[hi[-1]].split(',')]; row = lines[hi[-1] + 1].split(',')
    return float(ns.group(1)), float(ns.group(2)), float(row[hdr.index('r')]), o
for R in (1.0, 3.0, 9.0):
    m2 = np.array([1e-11, 1e-11*R*R])
    V = lambda f: 0.5*float(m2 @ (f*f)); grad = lambda f: m2*f; hess = lambda f: np.diag(m2)
    f0 = np.array([12.0, 12.0]); s, Ne = run(V, grad, f0, Nmax=400, v0=-grad(f0)/V(f0))
    fstar = s.sol(Ne - 55.0)[:2]
    J = observe_multi(V, grad, hess, fstar, h=[1e-3, max(1e-3, abs(fstar[1])/10)])
    try: ns_ex, ns_dn, r_ex, out = mmc(R)
    except Exception as e: L.append(f'R={R:g}: MMC FAILED {e}'); ok = False; print(L[-1]); continue
    c1 = abs(J['ns'] - ns_dn) <= 2e-4; ok &= c1
    L.append(f"R={R:g}: phi* = ({fstar[0]:.4f}, {fstar[1]:.4f}), N_tot {Ne:.2f} | Janus dN ns {J['ns']:.6f} r {J['r']:.5f} fNL {J['fNL']:.4f} | MMC exact ns {ns_ex:.6f} r {r_ex:.5f}, MMC dN-SR ns {ns_dn:.6f}"
             f" | C1 |dN-dN| {abs(J['ns']-ns_dn):.1e} {'PASS' if c1 else 'FAIL'}; dN error vs exact {abs(J['ns']-ns_ex):.1e}; r Janus/MMC-exact {J['r']/r_ex:.4f}")
    print(L[-1], flush=True)
L.append('JMF1: ' + ('JANUS dN AGREES WITH AN INDEPENDENT CODE (C1 all R)' if ok else 'NOT AGREED'))
open('field_tests/results/janus_jmf1_mmc.txt', 'w').write('\n'.join(L) + '\n'); print(L[-1])
