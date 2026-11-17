"""JMF2 (locked PREREG_JMF2_exact_mf)."""
import sys, numpy as np; sys.path.insert(0, '.')
from tools.janus_calc.mfms import spectra_mf
T = {1.0: (0.963372, 0.14405), 3.0: (0.945477, 0.14464), 9.0: (0.927745, 0.14568)}; dN = {1.0: 1.3e-4, 3.0: 7.6e-4, 9.0: 1.7e-3}
L = []; ok = True
for R, (ns_t, r_t) in T.items():
    m2 = np.array([1e-11, 1e-11*R*R])
    s = spectra_mf(lambda f: 0.5*float(m2 @ (f*f)), lambda f: m2*f, lambda f: np.diag(m2), [12.0, 12.0])
    c1 = abs(s['ns'] - ns_t) <= 2e-4; c2 = abs(s['r']/r_t - 1) <= 2e-3; ok &= c1 and c2
    L.append(f"R={R:g}: Janus-MF ns {s['ns']:.6f} (MMC {ns_t}) |d| {abs(s['ns']-ns_t):.1e} {'PASS' if c1 else 'FAIL'}; r {s['r']:.5f} (MMC {r_t}) rel {abs(s['r']/r_t-1):.1e} {'PASS' if c2 else 'FAIL'}; alpha_s {s['alpha_s']:.2e}; dN error was {dN[R]:.1e}")
    print(L[-1], flush=True)
L.append('JMF2: ' + ('JANUS-MF EXACT VALIDATED' if ok else 'NOT VALIDATED'))
open('field_tests/results/janus_jmf2.txt', 'w').write('\n'.join(L) + '\n'); print(L[-1])
