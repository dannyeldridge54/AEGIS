"""L11 (locked PREREG_L11_cobaya): Cobaya MCMC on L7's likelihood."""
import sys, time, numpy as np; sys.path.insert(0, '.')
from tools.lockbench.provenance import stamp
t0 = time.time(); src = open('theory/janus_lt/l7_joint.py').read().split('best_l = ')[0]; ns = {'__name__': 'l7lib'}; exec(compile(src, 'l7', 'exec'), ns)
chi2, mu = ns['chi2'], ns['mu']
from cobaya.run import run
def logp(w0, wa, h, wb, wbc): v = chi2([w0, wa, h, wb, wbc]); return -0.5*v if v < 1e8 else -np.inf
sb, sbc = 1.46e-4, 1.22e-3
info = {'likelihood': {'l7': {'external': logp, 'input_params': ['w0', 'wa', 'h', 'wb', 'wbc']}},
        'params': {'w0': {'prior': {'min': -2.0, 'max': 0.0}, 'ref': -0.85, 'proposal': 0.05},
                   'wa': {'prior': {'min': -3.0, 'max': 2.0}, 'ref': -0.5, 'proposal': 0.2},
                   'h': {'prior': {'min': 0.55, 'max': 0.80}, 'ref': 0.675, 'proposal': 0.01},
                   'wb': {'prior': {'min': mu[1] - 10*sb, 'max': mu[1] + 10*sb}, 'ref': float(mu[1]), 'proposal': sb},
                   'wbc': {'prior': {'min': mu[2] - 10*sbc, 'max': mu[2] + 10*sbc}, 'ref': float(mu[2]), 'proposal': sbc}},
        'sampler': {'mcmc': {'Rminus1_stop': 0.02, 'max_tries': 10000, 'burn_in': 0, 'learn_proposal': True}}, 'output': 'field_tests/results/l11_chain/chain', 'force': True}
upd, sampler = run(info)
S = sampler.products(skip_samples=0.3)['sample']; R = float(sampler.Rminus1_last if hasattr(sampler, 'Rminus1_last') else np.nan)
L = []; ok = True
for p, mp, sg in (('w0', -0.853, 0.053), ('wa', -0.518, 0.200)):
    m, sd = float(S.mean(p)), float(np.sqrt(S.cov([p])[0, 0])); c1 = abs(m - mp) <= 0.5*sg; c2 = abs(sd/sg - 1) <= 0.30; ok &= c1 and c2
    L.append(f'{p}: posterior {m:.3f} ± {sd:.3f} (L7 MAP {mp} ± {sg}) -> C1 {c1} C2 {c2}')
c3 = R < 0.02; ok &= c3; L.append(f'R-1 = {R:.4f} -> C3 {c3}; samples after burn-in {len(S)}')
L.append('L11: ' + ('L7 ERRORS CONFIRMED BY MCMC' if ok else 'DIFFERS (see lines)') + f'  ({time.time()-t0:.0f} s)')
Rp = 'field_tests/results/janus_lt_l11_cobaya.txt'; open(Rp, 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
stamp(Rp, lock='field_tests/rules/PREREG_L11_cobaya.md', code=['theory/janus_lt/l11_cobaya.py', 'theory/janus_lt/l7_joint.py'], t0=t0)
