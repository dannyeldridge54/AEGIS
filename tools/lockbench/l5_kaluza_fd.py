# AEGIS-FP N4TPM54NGIMR5HEH · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""L5-K (locked PREREG_L5_kaluza_fd_mms)."""
import sys, math, time, numpy as np; sys.path.insert(0, '.'); t0 = time.time()
from tools.kaluza.solvers import fd_schrodinger
from tools.lockbench.verify import observed_order, gci3
from tools.lockbench.provenance import stamp
Ns = [500, 1000, 2000]; hs = [math.pi/(N + 1) for N in Ns]
E = [fd_schrodinger(lambda y: 0*y, lambda y: 2*y, 1e-9, math.sqrt(math.pi), N=N, nmodes=2) for N in Ns]; L = []; ok = True
for n in (1, 2):
    v = [e[n-1] for e in E]; p, err = observed_order(hs, v, n*n); g = gci3(v[2], v[1], v[0], hs[1]/hs[2], hs[0]/hs[1])
    k1 = all(abs(x - 2) <= 0.1 for x in p); k2 = g['GCI_fine'] <= 1e-5 and abs(g['phi_ext'] - n*n)/n**2 <= 1e-7; ok &= k1 and k2
    L.append(f"mode {n}: m2 {v} exact {n*n} | errors {[f'{x:.2e}' for x in err]} | orders {[round(x, 4) for x in p]} K1 {k1} | GCI p {g['p']:.4f} GCI_fine {g['GCI_fine']:.1e} ext err {abs(g['phi_ext']-n*n)/n**2:.1e} K2 {k2}")
    print(L[-1])
L.append('L5-K: ' + ('KALUZA FD OPERATOR VERIFIED (2nd order)' if ok else 'NOT VERIFIED')); print(L[-1])
R = 'field_tests/results/l5_kaluza_fd_mms.txt'; open(R, 'w').write('\n'.join(L) + '\n')
stamp(R, lock='field_tests/rules/PREREG_L5_kaluza_fd_mms.md', code=['tools/lockbench/l5_kaluza_fd.py', 'tools/kaluza/solvers.py', 'tools/lockbench/verify.py'], t0=t0)
