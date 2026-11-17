"""L11 summary from the saved chain (PREREG_L11_cobaya DEVIATIONS D1)."""
import numpy as np, re, sys; sys.path.insert(0, '.')
from tools.lockbench.provenance import stamp
C = np.loadtxt('field_tests/results/l11_chain/chain.1.txt'); hdr = open('field_tests/results/l11_chain/chain.1.txt').readline().split()[1:]
ix = {n: i for i, n in enumerate(hdr)}; C = C[int(0.3*len(C)):]; w = C[:, ix['weight']]
R = [float(x) for x in re.findall(r'Convergence of means: R-1 = ([0-9.]+)', open('/tmp/claude-0/l11.log').read())][-1]
L = []; ok = True
for p, mp, sg in (('w0', -0.853, 0.053), ('wa', -0.518, 0.200)):
    x = C[:, ix[p]]; m = np.average(x, weights=w); sd = np.sqrt(np.average((x - m)**2, weights=w)); c1 = abs(m - mp) <= 0.5*sg; c2 = abs(sd/sg - 1) <= 0.30; ok &= c1 and c2
    L.append(f'{p}: posterior {m:.3f} ± {sd:.3f} (L7 MAP {mp} ± {sg}) -> C1 {c1} C2 {c2}')
c3 = R < 0.02; ok &= c3; ch = C[:, ix['chi2']]
L.append(f'R-1 (means, last) = {R:.4f} -> C3 {c3}; rows after burn-in {len(C)}, total weight {int(w.sum())}')
L.append(f'chain chi2: min {ch.min():.2f}, weighted median {np.median(np.repeat(ch, w.astype(int))):.2f} (L7 minimum 1422.93; 5 free parameters)')
L.append('L11: ' + ('L7 ERRORS CONFIRMED BY MCMC' if ok else 'DIFFERS (see lines)'))
Rp = 'field_tests/results/janus_lt_l11_cobaya.txt'; open(Rp, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
stamp(Rp, lock='field_tests/rules/PREREG_L11_cobaya.md', code=['theory/janus_lt/l11_summary.py', 'theory/janus_lt/l11_cobaya.py'], data=['field_tests/results/l11_chain/chain.1.txt'])
