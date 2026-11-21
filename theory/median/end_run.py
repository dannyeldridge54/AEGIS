import math, json, numpy as np
from scipy.optimize import minimize_scalar, brentq
c = json.load(open('theory/median/centre.json'))
mmu, ud, uu, nu = 105.658/1776.86, 0.0457, 0.00311, math.exp(-7*math.pi/8)
me = 0.51100/1776.86
ladder = [(2, .05), (1.5, .04), (1.3, .03), (1.2, .025), (1.1, .02)]
best = None
for f, td in ladder:
    L = math.log(f)
    data = lambda u: {'m_mu/m_tau': math.log(u/mmu)/L, 'down step': math.log(u/ud)/L, 'Delta_3': c['delta3_residual']/td, 'thread': 0.0}
    r = minimize_scalar(lambda lu: sum(v*v for v in data(math.exp(lu)).values()), bounds=(math.log(1e-3), math.log(.3)), method='bounded')
    u = math.exp(r.x); d = data(u); ok = all(abs(v) <= 1 for v in d.values())
    print('rung x%.1f / D3 tol %.3f: u* = %.4f  %s  | internal nu %.2f | %s' % (f, td, u, ' '.join('%s %+.2f' % kv for kv in d.items()), math.log(u/nu)/L, 'PASS' if ok else 'FAIL'))
    if ok: best = (f, td, u, d)
f, td, u, d = best
ce = brentq(lambda a: (a*u*u + mmu + 1)/(math.sqrt(a)*u + math.sqrt(mmu) + 1)**2 - 2/3, 1e-4, 10)   # Koide with observed mu/tau, solve electron coefficient
print('\nEND RESULT: tightest passing rung x%.1f (Delta_3 tol %.3f); arrow u* = %.4f' % (f, td, u))
print('  electron coefficient from Koide (input): c_e = %.4f -> m_e/m_tau = %.3e (obs %.3e)' % (ce, ce*u*u, me))
print('  up-quark exponent p (u_u = u*^p) = %.2f' % (math.log(uu)/math.log(u)))
